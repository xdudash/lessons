from __future__ import annotations

import gc
import re

import localize_a1_a2 as base

PRIMARY = {
    "en": "Helsinki-NLP/opus-mt-uk-en",
    "ru": "Helsinki-NLP/opus-mt-uk-ru",
}
NLLB = "facebook/nllb-200-distilled-600M"
TARGET_CODES = {"en": "eng_Latn", "ru": "rus_Cyrl"}
base.WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")


def invalid(target: str, text: str) -> bool:
    if not text.strip() or base.WEIRD.search(text):
        return True
    if target == "en" and base.CYR.search(text):
        return True
    if target == "ru" and base.UK_ONLY.search(text):
        return True
    return False


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


def fallback_translate(chunks: list[str], target: str) -> dict[str, str]:
    if not chunks:
        return {}
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(NLLB, src_lang="ukr_Cyrl")
    model = AutoModelForSeq2SeqLM.from_pretrained(NLLB)
    model.eval()
    forced_bos = tokenizer.convert_tokens_to_ids(TARGET_CODES[target])
    out: dict[str, str] = {}
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
                    raise RuntimeError(f"fallback still invalid for {target}: {src!r} -> {dst!r}")
                out[src] = dst
            print(f"{target} NLLB fallback: {min(start + batch_size, len(chunks))}/{len(chunks)}", flush=True)
    del model, tokenizer
    gc.collect()
    return out


def translate_sources(strings: list[str], target: str) -> dict[str, str]:
    segmented = {s: base.split_translation_segments(s) for s in strings}
    chunks = sorted({piece.strip() for parts in segmented.values() for translate, piece in parts if translate and piece.strip()})
    translated, bad = primary_translate(chunks, target)
    translated.update(fallback_translate(bad, target))

    result: dict[str, str] = {}
    for source, parts in segmented.items():
        built: list[str] = []
        for translate, piece in parts:
            if translate and piece.strip():
                prefix = piece[: len(piece) - len(piece.lstrip())]
                suffix = piece[len(piece.rstrip()):]
                built.append(prefix + translated[piece.strip()] + suffix)
            else:
                built.append(piece)
        value = "".join(built)
        literal_tokens = [p for flag, p in parts if not flag and base.LATIN_TOKEN.fullmatch(p)]
        for token in literal_tokens:
            if token not in value:
                raise RuntimeError(f"lost Slovak/Latin token {token!r}: {source!r} -> {value!r}")
        result[source] = value
    return result


base.translate_sources = translate_sources
base.main()
