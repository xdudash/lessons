from __future__ import annotations

import argparse
import gc
import json
import re
from pathlib import Path
from typing import Any, Callable

from translation_fixes import fixed_translation, normalize_translation

CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
LATIN_TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ž]+(?:[’'/-][A-Za-zÀ-ÖØ-öø-ž]+)*")
CYR_QUOTE = re.compile(r'([«“„"])([^»”"]*[А-Яа-яЁёІіЇїЄєҐґ][^»”"]*)([»”"])')

LOCALIZED_KEYS = {
    "title", "topic", "description", "intro", "completionMessage",
    "eyebrow", "shortDescription", "subtitle", "goal",
    "body", "shortRule", "instruction", "question", "prompt",
    "explanation", "hint", "text", "statement", "sentence",
    "displaySentence", "context", "target", "situation", "phrase",
    "source", "successMessage", "alt", "label",
}
LOCALIZED_LIST_KEYS = {"outcomes"}
SIBLING_KEYS = {"left", "right", "sender", "body", "day", "hours", "value"}


def has_cyr(value: Any) -> bool:
    return isinstance(value, str) and bool(CYR.search(value))


def _split_cyr_quotes(parts: list[tuple[bool, str]]) -> list[tuple[bool, str]]:
    out: list[tuple[bool, str]] = []
    for flag, piece in parts:
        if not flag:
            out.append((flag, piece))
            continue
        pos = 0
        for match in CYR_QUOTE.finditer(piece):
            before = piece[pos:match.start()]
            if before:
                out.append((has_cyr(before), before))
            out.append((False, match.group(1)))
            out.append((True, match.group(2)))
            out.append((False, match.group(3)))
            pos = match.end()
        tail = piece[pos:]
        if tail:
            out.append((has_cyr(tail), tail))

    merged: list[tuple[bool, str]] = []
    for flag, piece in out:
        if not piece:
            continue
        if merged and merged[-1][0] == flag:
            merged[-1] = (flag, merged[-1][1] + piece)
        else:
            merged.append((flag, piece))
    return merged


def split_segments(text: str) -> list[tuple[bool, str]]:
    parts: list[tuple[bool, str]] = []
    pos = 0
    for match in LATIN_TOKEN.finditer(text):
        if match.start() > pos:
            chunk = text[pos:match.start()]
            parts.append((has_cyr(chunk), chunk))
        parts.append((False, match.group(0)))
        pos = match.end()
    if pos < len(text):
        chunk = text[pos:]
        parts.append((has_cyr(chunk), chunk))
    if not parts:
        parts = [(has_cyr(text), text)]
    return _split_cyr_quotes(parts)


def collect_sources(value: Any) -> set[str]:
    out: set[str] = set()

    def walk(v: Any) -> None:
        if isinstance(v, dict):
            uk = v.get("uk")
            if has_cyr(uk):
                out.add(uk)
            ex_uk = v.get("exampleUk")
            if has_cyr(ex_uk):
                out.add(ex_uk)
            for key, child in v.items():
                if key in LOCALIZED_KEYS and has_cyr(child):
                    out.add(child)
                if key in SIBLING_KEYS and has_cyr(child):
                    out.add(child)
                if key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    for item in child:
                        if has_cyr(item):
                            out.add(item)
                walk(child)
        elif isinstance(v, list):
            for child in v:
                walk(child)

    walk(value)
    return out


def localize_text(text: str, translate: Callable[[str, str], str]) -> dict[str, str]:
    return {"uk": text, "ru": translate("ru", text), "en": translate("en", text)}


def localize_document(doc: dict[str, Any], translate: Callable[[str, str], str]) -> dict[str, Any]:
    def walk(v: Any) -> None:
        if isinstance(v, dict):
            loc = v.get("localization")
            if isinstance(loc, dict) and "uiLanguages" in loc:
                loc["uiLanguages"] = ["uk", "ru", "en"]
                loc["targetLanguage"] = "sk"
                loc.setdefault("fallbackUiLanguage", "uk")

            uk = v.get("uk")
            if has_cyr(uk):
                v["ru"] = translate("ru", uk)
                v["en"] = translate("en", uk)

            ex_uk = v.get("exampleUk")
            if has_cyr(ex_uk):
                v["exampleRu"] = translate("ru", ex_uk)
                v["exampleEn"] = translate("en", ex_uk)

            for key in list(v.keys()):
                child = v[key]
                if key in LOCALIZED_KEYS and has_cyr(child):
                    v[key] = localize_text(child, translate)
                    child = v[key]
                elif key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    v[key] = [localize_text(x, translate) if has_cyr(x) else x for x in child]
                    child = v[key]
                elif key in SIBLING_KEYS and has_cyr(child):
                    v.setdefault(f"{key}Ru", translate("ru", child))
                    v.setdefault(f"{key}En", translate("en", child))
                walk(child)
        elif isinstance(v, list):
            for child in v:
                walk(child)

    walk(doc)
    return doc


def invalid(target: str, text: str) -> bool:
    if not text.strip() or WEIRD.search(text):
        return True
    if target == "en" and CYR.search(text):
        return True
    if target == "ru" and UK_ONLY.search(text):
        return True
    return False


def batch_translate(chunks: list[str], target: str) -> dict[str, str]:
    if not chunks:
        return {}
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    primary = "Helsinki-NLP/opus-mt-uk-en" if target == "en" else "Helsinki-NLP/opus-mt-uk-ru"
    tokenizer = AutoTokenizer.from_pretrained(primary)
    model = AutoModelForSeq2SeqLM.from_pretrained(primary)
    model.eval()
    out: dict[str, str] = {}
    bad: list[str] = []
    batch_size = 72
    with torch.inference_mode():
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
            generated = model.generate(**inputs, max_new_tokens=192, num_beams=1)
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for src, dst in zip(batch, decoded):
                dst = dst.strip()
                if invalid(target, dst):
                    bad.append(src)
                else:
                    out[src] = dst
            print(f"{target} primary {min(start + batch_size, len(chunks))}/{len(chunks)} fallback={len(bad)}", flush=True)
    del model, tokenizer
    gc.collect()

    if bad:
        tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang="ukr_Cyrl")
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        model.eval()
        bos = tokenizer.convert_tokens_to_ids("eng_Latn" if target == "en" else "rus_Cyrl")
        with torch.inference_mode():
            for start in range(0, len(bad), 32):
                batch = bad[start:start + 32]
                inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
                generated = model.generate(**inputs, forced_bos_token_id=bos, max_new_tokens=192, num_beams=1)
                decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
                for src, dst in zip(batch, decoded):
                    dst = dst.strip()
                    if invalid(target, dst):
                        raise RuntimeError(f"invalid {target} translation: {src!r} -> {dst!r}")
                    out[src] = dst
                print(f"{target} fallback {min(start + 32, len(bad))}/{len(bad)}", flush=True)
        del model, tokenizer
        gc.collect()
    return out


def build_translator(sources: set[str]) -> Callable[[str, str], str]:
    segmented = {source: split_segments(source) for source in sources}
    fixed: dict[tuple[str, str], str] = {}
    for source in sources:
        for target in ("ru", "en"):
            value = fixed_translation(target, source)
            if value is not None:
                fixed[(target, source)] = value

    chunks = sorted({
        piece.strip()
        for source, parts in segmented.items()
        if ("ru", source) not in fixed or ("en", source) not in fixed
        for flag, piece in parts
        if flag and piece.strip()
    })
    ru_chunks = batch_translate(chunks, "ru")
    en_chunks = batch_translate(chunks, "en")
    cache: dict[tuple[str, str], str] = dict(fixed)

    def translate(target: str, source: str) -> str:
        key = (target, source)
        if key in cache:
            return cache[key]
        parts = segmented[source]
        table = en_chunks if target == "en" else ru_chunks
        built: list[str] = []
        for flag, piece in parts:
            if flag and piece.strip():
                prefix = piece[:len(piece) - len(piece.lstrip())]
                suffix = piece[len(piece.rstrip()):]
                built.append(prefix + table[piece.strip()] + suffix)
            else:
                built.append(piece)
        machine = "".join(built)
        value = normalize_translation(target, source, machine)
        if invalid(target, value):
            raise RuntimeError(f"invalid normalized {target}: {source!r} -> {value!r}")
        cache[key] = value
        return value

    return translate


def audit(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def walk(v: Any, path: str) -> None:
        if isinstance(v, dict):
            uk = v.get("uk")
            if has_cyr(uk):
                for lang in ("ru", "en"):
                    if not isinstance(v.get(lang), str) or not v[lang].strip():
                        errors.append(f"{path}: missing {lang}")
            if has_cyr(v.get("exampleUk")):
                if not isinstance(v.get("exampleRu"), str):
                    errors.append(f"{path}: missing exampleRu")
                if not isinstance(v.get("exampleEn"), str):
                    errors.append(f"{path}: missing exampleEn")
            for key, child in v.items():
                if key in LOCALIZED_KEYS and has_cyr(child):
                    errors.append(f"{path}.{key}: raw Cyrillic not localized")
                if key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    for i, item in enumerate(child):
                        if has_cyr(item):
                            errors.append(f"{path}.{key}[{i}]: raw Cyrillic not localized")
                walk(child, f"{path}.{key}")
        elif isinstance(v, list):
            for i, child in enumerate(v):
                walk(child, f"{path}[{i}]")

    walk(doc, "root")
    for lesson in doc.get("lessons", []):
        loc = lesson.get("localization", {})
        if loc.get("uiLanguages") != ["uk", "ru", "en"]:
            errors.append(f"{lesson.get('id')}: uiLanguages")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=("a1", "a2"), required=True)
    args = parser.parse_args()
    expected = 75 if args.level == "a1" else 90
    paths = sorted(Path("lessons", args.level).glob(f"{args.level}-s*-l*.json"))
    if len(paths) != expected:
        raise SystemExit(f"expected {expected}, got {len(paths)}")

    docs: list[tuple[Path, dict[str, Any]]] = []
    sources: set[str] = set()
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        docs.append((path, doc))
        sources |= collect_sources(doc)
    print(f"{args.level}: {len(paths)} lessons, {len(sources)} unique UI strings", flush=True)

    translate = build_translator(sources)
    total_errors: list[str] = []
    for path, doc in docs:
        localize_document(doc, translate)
        errors = audit(doc)
        total_errors.extend(f"{path.name}: {error}" for error in errors)
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    if total_errors:
        print("\n".join(total_errors[:100]))
        raise SystemExit(f"audit errors: {len(total_errors)}")
    print(f"localized {len(paths)} {args.level} lessons; audit OK", flush=True)


if __name__ == "__main__":
    main()
