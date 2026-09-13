from __future__ import annotations

import argparse
import gc
import json
import re
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from quality_overrides import LEXICAL, OVERRIDES, SUSPICIOUS_EN
from translation_fixes import fixed_translation, normalize_translation

MODEL = "facebook/nllb-200-distilled-600M"
CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
LATIN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ž]+(?:[’'/-][A-Za-zÀ-ÖØ-öø-ž]+)*")
LOCALIZED_KEYS = {
    "title", "topic", "description", "intro", "completionMessage", "eyebrow",
    "shortDescription", "subtitle", "goal", "body", "shortRule", "instruction",
    "question", "prompt", "explanation", "hint", "text", "statement", "sentence",
    "displaySentence", "context", "target", "situation", "phrase", "source",
    "successMessage", "alt", "label",
}
LOCALIZED_LIST_KEYS = {"outcomes"}
SIBLING_KEYS = {"left", "right", "sender", "day", "hours", "value"}


def has_cyr(value: Any) -> bool:
    return isinstance(value, str) and bool(CYR.search(value))


def collect(doc: dict[str, Any]) -> tuple[set[str], dict[str, str]]:
    sources: set[str] = set()
    preferred: dict[str, str] = {}

    def add(value: Any) -> None:
        if has_cyr(value):
            sources.add(value)

    def pref(uk: Any, sk: Any) -> None:
        if has_cyr(uk) and isinstance(sk, str) and LATIN.search(sk):
            preferred.setdefault(uk, sk)
            sources.add(uk)

    def walk(v: Any) -> None:
        if isinstance(v, dict):
            uk = v.get("uk")
            add(uk)
            if has_cyr(v.get("exampleUk")):
                add(v["exampleUk"])
                pref(v["exampleUk"], v.get("exampleSk"))
            if isinstance(v.get("sk"), str) and has_cyr(uk) and any(k in v for k in ("wordId", "pronunciationUk", "partOfSpeech", "ownership")):
                pref(uk, v["sk"])
            trans = v.get("translation")
            if isinstance(v.get("sk"), str) and isinstance(trans, dict):
                pref(trans.get("uk"), v["sk"])
            left, right = v.get("left"), v.get("right")
            if isinstance(left, str) and LATIN.search(left) and has_cyr(right):
                pref(right, left)
            if isinstance(right, str) and LATIN.search(right) and has_cyr(left):
                pref(left, right)
            for key, child in v.items():
                if key in LOCALIZED_KEYS and has_cyr(child):
                    add(child)
                elif key in SIBLING_KEYS and has_cyr(child):
                    add(child)
                elif key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    for item in child:
                        add(item)
                walk(child)
        elif isinstance(v, list):
            for child in v:
                walk(child)

    walk(doc)
    return sources, preferred


def invalid(target: str, text: str) -> bool:
    if not text.strip() or WEIRD.search(text):
        return True
    if target == "en" and CYR.search(text):
        return True
    if target == "ru" and UK_ONLY.search(text):
        return True
    if target == "en" and any(token in text.lower() for token in SUSPICIOUS_EN):
        return True
    return False


def meaningful_latin_tokens(source: str) -> list[str]:
    ignore = {"a1", "a2", "new", "review", "transfer", "mastery", "xp"}
    return [x for x in LATIN.findall(source) if len(x) >= 2 and x.lower() not in ignore]


def split_keep_latin(text: str) -> list[tuple[bool, str]]:
    parts: list[tuple[bool, str]] = []
    pos = 0
    for m in LATIN.finditer(text):
        if m.start() > pos:
            chunk = text[pos:m.start()]
            parts.append((has_cyr(chunk), chunk))
        parts.append((False, m.group(0)))
        pos = m.end()
    if pos < len(text):
        chunk = text[pos:]
        parts.append((has_cyr(chunk), chunk))
    return parts or [(has_cyr(text), text)]


class NLLB:
    def __init__(self) -> None:
        torch.set_num_threads(4)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
        self.model.eval()
        self.tokenizers = {
            "uk": AutoTokenizer.from_pretrained(MODEL, src_lang="ukr_Cyrl"),
            "sk": AutoTokenizer.from_pretrained(MODEL, src_lang="slk_Latn"),
        }

    def translate_batch(self, texts: list[str], source: str, target: str, batch_size: int = 48) -> dict[str, str]:
        if not texts:
            return {}
        tok = self.tokenizers[source]
        bos = tok.convert_tokens_to_ids("eng_Latn" if target == "en" else "rus_Cyrl")
        result: dict[str, str] = {}
        with torch.inference_mode():
            for start in range(0, len(texts), batch_size):
                batch = texts[start:start + batch_size]
                inputs = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
                generated = self.model.generate(
                    **inputs,
                    forced_bos_token_id=bos,
                    max_new_tokens=192,
                    num_beams=2,
                )
                decoded = tok.batch_decode(generated, skip_special_tokens=True)
                result.update((src, dst.strip()) for src, dst in zip(batch, decoded))
                print(f"{source}->{target}: {min(start + batch_size, len(texts))}/{len(texts)}", flush=True)
        return result


def build_tables(sources: set[str], preferred: dict[str, str]) -> dict[tuple[str, str], str]:
    engine = NLLB()
    table: dict[tuple[str, str], str] = {}

    for source in sources:
        for target in ("ru", "en"):
            if source in OVERRIDES:
                table[(target, source)] = OVERRIDES[source][target]
                continue
            fixed = fixed_translation(target, source)
            if fixed is not None:
                table[(target, source)] = fixed
                continue
            sk = preferred.get(source)
            if sk in LEXICAL:
                table[(target, source)] = LEXICAL[sk][target]

    for target in ("ru", "en"):
        unresolved = [s for s in sorted(sources) if (target, s) not in table]
        uk_sources = [s for s in unresolved if s not in preferred]
        sk_pairs = [(s, preferred[s]) for s in unresolved if s in preferred]
        sk_unique = sorted({sk for _, sk in sk_pairs})

        uk_out = engine.translate_batch(uk_sources, "uk", target)
        sk_out = engine.translate_batch(sk_unique, "sk", target)
        sk_by_source = {source: sk_out[sk] for source, sk in sk_pairs}

        retry: list[str] = []
        for source in unresolved:
            raw = sk_by_source[source] if source in sk_by_source else uk_out[source]
            value = normalize_translation(target, source, raw)
            lost = source not in preferred and any(tok not in value for tok in meaningful_latin_tokens(source))
            if invalid(target, value) or lost:
                retry.append(source)
            else:
                table[(target, source)] = value

        if retry:
            segmented = {source: split_keep_latin(source) for source in retry}
            chunks = sorted({piece.strip() for parts in segmented.values() for flag, piece in parts if flag and piece.strip()})
            translated_chunks = engine.translate_batch(chunks, "uk", target, batch_size=32)
            for source in retry:
                built: list[str] = []
                for flag, piece in segmented[source]:
                    if flag and piece.strip():
                        prefix = piece[:len(piece) - len(piece.lstrip())]
                        suffix = piece[len(piece.rstrip()):]
                        built.append(prefix + translated_chunks[piece.strip()] + suffix)
                    else:
                        built.append(piece)
                value = normalize_translation(target, source, "".join(built))
                if invalid(target, value) or any(tok not in value for tok in meaningful_latin_tokens(source)):
                    raise RuntimeError(f"quality check failed {target}: {source!r} -> {value!r}")
                table[(target, source)] = value

    del engine
    gc.collect()
    return table


def localize_document(doc: dict[str, Any], table: dict[tuple[str, str], str]) -> None:
    def localized(text: str) -> dict[str, str]:
        return {"uk": text, "ru": table[("ru", text)], "en": table[("en", text)]}

    def walk(v: Any) -> None:
        if isinstance(v, dict):
            loc = v.get("localization")
            if isinstance(loc, dict) and "uiLanguages" in loc:
                loc["uiLanguages"] = ["uk", "ru", "en"]
                loc["targetLanguage"] = "sk"
                loc.setdefault("fallbackUiLanguage", "uk")

            uk = v.get("uk")
            if has_cyr(uk):
                v["ru"] = table[("ru", uk)]
                v["en"] = table[("en", uk)]
            ex_uk = v.get("exampleUk")
            if has_cyr(ex_uk):
                v["exampleRu"] = table[("ru", ex_uk)]
                v["exampleEn"] = table[("en", ex_uk)]

            for key in list(v.keys()):
                child = v[key]
                if key in LOCALIZED_KEYS and has_cyr(child):
                    v[key] = localized(child)
                    child = v[key]
                elif key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    v[key] = [localized(x) if has_cyr(x) else x for x in child]
                    child = v[key]
                elif key in SIBLING_KEYS and has_cyr(child):
                    v.setdefault(f"{key}Ru", table[("ru", child)])
                    v.setdefault(f"{key}En", table[("en", child)])
                walk(child)
        elif isinstance(v, list):
            for child in v:
                walk(child)

    walk(doc)


def audit(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def walk(v: Any, path: str) -> None:
        if isinstance(v, dict):
            uk = v.get("uk")
            if has_cyr(uk):
                for lang in ("ru", "en"):
                    val = v.get(lang)
                    if not isinstance(val, str) or not val.strip():
                        errors.append(f"{path}: missing {lang}")
                    elif invalid(lang, val):
                        errors.append(f"{path}: invalid {lang}={val!r}")
            if has_cyr(v.get("exampleUk")):
                for lang in ("Ru", "En"):
                    val = v.get(f"example{lang}")
                    target = lang.lower()
                    if not isinstance(val, str) or invalid(target, val):
                        errors.append(f"{path}: bad example{lang}")
            for key, child in v.items():
                if key in LOCALIZED_KEYS and has_cyr(child):
                    errors.append(f"{path}.{key}: raw Cyrillic UI string")
                if key in LOCALIZED_LIST_KEYS and isinstance(child, list):
                    for i, item in enumerate(child):
                        if has_cyr(item):
                            errors.append(f"{path}.{key}[{i}]: raw Cyrillic UI string")
                walk(child, f"{path}.{key}")
        elif isinstance(v, list):
            for i, child in enumerate(v):
                walk(child, f"{path}[{i}]")
    walk(doc, "root")
    for lesson in doc.get("lessons", []):
        if lesson.get("localization", {}).get("uiLanguages") != ["uk", "ru", "en"]:
            errors.append(f"{lesson.get('id')}: uiLanguages")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", choices=("a1", "a2"), required=True)
    args = ap.parse_args()
    expected = 75 if args.level == "a1" else 90
    paths = sorted(Path("lessons", args.level).glob(f"{args.level}-s*-l*.json"))
    if len(paths) != expected:
        raise SystemExit(f"expected {expected} lessons, got {len(paths)}")

    docs: list[tuple[Path, dict[str, Any]]] = []
    sources: set[str] = set()
    preferred: dict[str, str] = {}
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        docs.append((path, doc))
        src, pref = collect(doc)
        sources |= src
        for uk, sk in pref.items():
            preferred.setdefault(uk, sk)
    print(f"{args.level}: lessons={len(paths)} ui_strings={len(sources)} glossary={len(preferred)}", flush=True)

    table = build_tables(sources, preferred)
    all_errors: list[str] = []
    for path, doc in docs:
        localize_document(doc, table)
        errors = audit(doc)
        all_errors.extend(f"{path.name}: {e}" for e in errors)
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    if all_errors:
        print("\n".join(all_errors[:100]))
        raise SystemExit(f"audit errors={len(all_errors)}")
    print(f"QUALITY AUDIT {args.level}: {len(paths)}/{expected} OK", flush=True)

if __name__ == "__main__":
    main()
