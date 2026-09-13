from __future__ import annotations

import gc
import re

import localize_a1_a2 as base
import translation_fixes as fixes

PRIMARY = {
    "en": "Helsinki-NLP/opus-mt-uk-en",
    "ru": "Helsinki-NLP/opus-mt-uk-ru",
}
NLLB = "facebook/nllb-200-distilled-600M"
TARGET_CODES = {"en": "eng_Latn", "ru": "rus_Cyrl"}
base.WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
QUOTE_RE = re.compile(r'([«“„"])([^»”"]*[А-Яа-яЁёІіЇїЄєҐґ][^»”"]*)([»”"])')


def invalid(target: str, text: str) -> bool:
    if not text.strip() or base.WEIRD.search(text):
        return True
    if target == "en" and base.CYR.search(text):
        return True
    if target == "ru" and base.UK_ONLY.search(text):
        return True
    return False


def split_quotes(parts: list[tuple[bool, str]]) -> list[tuple[bool, str]]:
    out: list[tuple[bool, str]] = []
    for flag, piece in parts:
        if not flag:
            out.append((flag, piece))
            continue
        pos = 0
        for match in QUOTE_RE.finditer(piece):
            before = piece[pos:match.start()]
            if before:
                out.append((bool(base.CYR.search(before)), before))
            out.append((False, match.group(1)))
            out.append((True, match.group(2)))
            out.append((False, match.group(3)))
            pos = match.end()
        tail = piece[pos:]
        if tail:
            out.append((bool(base.CYR.search(tail)), tail))
    merged: list[tuple[bool, str]] = []
    for flag, piece in out:
        if not piece:
            continue
        if merged and merged[-1][0] == flag:
            merged[-1] = (flag, merged[-1][1] + piece)
        else:
            merged.append((flag, piece))
    return merged


def primary_translate(chunks: list[str], target: str) -> tuple[dict[str, str], list[str]]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(PRIMARY[target])
    model = AutoModelForSeq2SeqLM.from_pretrained(PRIMARY[target])
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
            print(f"{target} Marian: {min(start + batch_size, len(chunks))}/{len(chunks)}; fallback={len(bad)}", flush=True)
    del model, tokenizer
    gc.collect()
    return out, bad


def nllb_pass(chunks: list[str], target: str, src_lang: str) -> tuple[dict[str, str], list[str]]:
    if not chunks:
        return {}, []
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(NLLB, src_lang=src_lang)
    model = AutoModelForSeq2SeqLM.from_pretrained(NLLB)
    model.eval()
    forced_bos = tokenizer.convert_tokens_to_ids(TARGET_CODES[target])
    out: dict[str, str] = {}
    bad: list[str] = []
    batch_size = 32
    with torch.inference_mode():
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
            generated = model.generate(**inputs, forced_bos_token_id=forced_bos, max_new_tokens=192, num_beams=1)
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for src, dst in zip(batch, decoded):
                dst = dst.strip()
                if invalid(target, dst):
                    bad.append(src)
                else:
                    out[src] = dst
            print(f"{target} NLLB {src_lang}: {min(start + batch_size, len(chunks))}/{len(chunks)}; retry={len(bad)}", flush=True)
    del model, tokenizer
    gc.collect()
    return out, bad


def fallback_translate(chunks: list[str], target: str) -> dict[str, str]:
    out, bad = nllb_pass(chunks, target, "ukr_Cyrl")
    if bad and target == "en":
        retry, bad = nllb_pass(bad, target, "rus_Cyrl")
        out.update(retry)
    if bad:
        raise RuntimeError(f"fallback still invalid for {target}: {bad[:10]!r}")
    return out


def translate_sources(strings: list[str], target: str) -> dict[str, str]:
    result: dict[str, str] = {}
    pending: list[str] = []
    for source in strings:
        fixed = fixes.fixed_translation(target, source)
        if fixed is None:
            pending.append(source)
        else:
            result[source] = fixed

    segmented = {s: split_quotes(base.split_translation_segments(s)) for s in pending}
    chunks = sorted({piece.strip() for parts in segmented.values() for translate, piece in parts if translate and piece.strip()})
    translated, bad = primary_translate(chunks, target)
    translated.update(fallback_translate(bad, target))

    for source, parts in segmented.items():
        built: list[str] = []
        for translate, piece in parts:
            if translate and piece.strip():
                prefix = piece[: len(piece) - len(piece.lstrip())]
                suffix = piece[len(piece.rstrip()):]
                built.append(prefix + translated[piece.strip()] + suffix)
            else:
                built.append(piece)
        value = fixes.normalize_translation(target, source, "".join(built))
        literal_tokens = [p for flag, p in parts if not flag and base.LATIN_TOKEN.fullmatch(p)]
        for token in literal_tokens:
            if token not in value:
                raise RuntimeError(f"lost Slovak/Latin token {token!r}: {source!r} -> {value!r}")
        result[source] = value

    return result


base.translate_sources = translate_sources
base.main()
