from __future__ import annotations

import re
from typing import Iterable

import localize_clean_v2 as v2

base = v2.base
NLLB = "facebook/nllb-200-distilled-600M"
TARGET_CODES = {"en": "eng_Latn", "ru": "rus_Cyrl"}
PLACEHOLDER_RE = re.compile(r"XQZ\s*TOKEN\s*(\d+)\s*QZX", re.IGNORECASE)

_MODEL = None
_TOKENIZER = None

LOCAL_EXACT = {
    "Яка я людина?": {"en": "What kind of person am I?", "ru": "Какой я человек?"},
    "Розширюємо опис характеру, особистості та звичок і вчимося порівнювати себе з іншими.": {
        "en": "We expand how we describe character, personality and habits, and learn to compare ourselves with others.",
        "ru": "Расширяем описание характера, личности и привычек и учимся сравнивать себя с другими.",
    },
    "Чудово. Тепер перенеси ці моделі у власні реальні ситуації.": {
        "en": "Great. Now apply these patterns to real situations from your own life.",
        "ru": "Отлично. Теперь перенеси эти модели в реальные ситуации из своей жизни.",
    },
    "Характер і порівняння": {"en": "Character and comparison", "ru": "Характер и сравнение"},
    "Як це працює": {"en": "How it works", "ru": "Как это работает"},
    "Перенесення в реальну ситуацію": {"en": "Using it in a real situation", "ru": "Применение в реальной ситуации"},
    "Цільові слова й фрази": {"en": "Target words and phrases", "ru": "Целевые слова и фразы"},
    "Використовуй модель коротко й точно; спочатку зміст, потім форма.": {
        "en": "Use the pattern briefly and precisely: meaning first, then form.",
        "ru": "Используй модель кратко и точно: сначала смысл, затем форма.",
    },
    "Описуй людину короткими прикметниками й додавай звичку або ставлення.": {
        "en": "Describe a person with short adjectives and add a habit or attitude.",
        "ru": "Описывай человека короткими прилагательными и добавляй привычку или отношение.",
    },
    "Порівнюй людей лише за однією ознакою за раз: так вислів залишається ясним.": {
        "en": "Compare people by one feature at a time so the sentence stays clear.",
        "ru": "Сравнивай людей по одному признаку за раз, чтобы высказывание оставалось ясным.",
    },
}

_original_fixed = base.fixed_translation


def fixed_translation(target: str, source: str) -> str | None:
    if source in LOCAL_EXACT:
        return LOCAL_EXACT[source][target]
    return _original_fixed(target, source)


def protect_latin(text: str) -> tuple[str, list[str]]:
    literals: list[str] = []

    def repl(match: re.Match[str]) -> str:
        index = len(literals)
        literals.append(match.group(0))
        return f"XQZTOKEN{index}QZX"

    return base.LATIN.sub(repl, text), literals


def restore_latin(text: str, literals: list[str]) -> str:
    seen: set[int] = set()

    def repl(match: re.Match[str]) -> str:
        index = int(match.group(1))
        if index >= len(literals):
            return match.group(0)
        seen.add(index)
        return literals[index]

    restored = PLACEHOLDER_RE.sub(repl, text)
    missing = [index for index in range(len(literals)) if index not in seen]
    if missing:
        raise ValueError(f"missing protected literals: {missing}")
    return restored


def _get_model():
    global _MODEL, _TOKENIZER
    if _MODEL is None or _TOKENIZER is None:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        torch.set_num_threads(4)
        _TOKENIZER = AutoTokenizer.from_pretrained(NLLB, src_lang="ukr_Cyrl")
        _MODEL = AutoModelForSeq2SeqLM.from_pretrained(NLLB)
        _MODEL.eval()
    return _TOKENIZER, _MODEL


def _nllb_many(texts: list[str], target: str) -> list[str]:
    if not texts:
        return []
    import torch
    tokenizer, model = _get_model()
    protected: list[str] = []
    mappings: list[list[str]] = []
    for text in texts:
        value, literals = protect_latin(text)
        protected.append(value)
        mappings.append(literals)

    forced_bos = tokenizer.convert_tokens_to_ids(TARGET_CODES[target])
    results: list[str] = []
    batch_size = 64
    with torch.inference_mode():
        for start in range(0, len(protected), batch_size):
            batch = protected[start:start + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
            generated = model.generate(
                **inputs,
                forced_bos_token_id=forced_bos,
                max_new_tokens=192,
                num_beams=1,
            )
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for source, translated, literals in zip(texts[start:start + batch_size], decoded, mappings[start:start + batch_size]):
                translated = translated.strip()
                try:
                    translated = restore_latin(translated, literals)
                except ValueError:
                    translated = _segmented_fallback(source, target)
                results.append(translated)
            print(f"NLLB uk->{target}: {min(start + batch_size, len(texts))}/{len(texts)}", flush=True)
    return results


def _segmented_fallback(text: str, target: str) -> str:
    """Last resort: translate Cyrillic spans and preserve Latin/Slovak tokens exactly."""
    tokenizer, model = _get_model()
    import torch
    parts: list[tuple[bool, str]] = []
    pos = 0
    for match in base.LATIN.finditer(text):
        if match.start() > pos:
            chunk = text[pos:match.start()]
            parts.append((bool(base.CYR.search(chunk)), chunk))
        parts.append((False, match.group(0)))
        pos = match.end()
    if pos < len(text):
        chunk = text[pos:]
        parts.append((bool(base.CYR.search(chunk)), chunk))
    forced_bos = tokenizer.convert_tokens_to_ids(TARGET_CODES[target])
    built: list[str] = []
    with torch.inference_mode():
        for should_translate, piece in parts:
            if not should_translate or not piece.strip():
                built.append(piece)
                continue
            prefix = piece[: len(piece) - len(piece.lstrip())]
            suffix = piece[len(piece.rstrip()):]
            core = piece.strip()
            inputs = tokenizer([core], return_tensors="pt", padding=True, truncation=True, max_length=384)
            generated = model.generate(**inputs, forced_bos_token_id=forced_bos, max_new_tokens=192, num_beams=1)
            translated = tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()
            built.append(prefix + translated + suffix)
    return "".join(built)


def _pattern_inner_sources(strings: Iterable[str]) -> set[str]:
    extras: set[str] = set()
    for source in strings:
        for pattern, group in ((base.FILL_RE, 1), (base.TRUE_FALSE_RE, 2), (base.CHOOSE_RE, 1), (base.REPLY_RE, 1)):
            match = pattern.match(source)
            if match and base.CYR.search(match.group(group)):
                extras.add(match.group(group))
    return extras


def _sanity(target: str, source: str, value: str) -> None:
    if not value.strip() or base.WEIRD.search(value):
        raise RuntimeError(f"invalid {target}: {source!r} -> {value!r}")
    if target == "en" and base.CYR.search(value):
        raise RuntimeError(f"Cyrillic leaked into English: {source!r} -> {value!r}")
    if target == "ru" and base.UK_ONLY.search(value):
        raise RuntimeError(f"Ukrainian letters leaked into Russian: {source!r} -> {value!r}")


def translate_sources(strings: list[str], target: str) -> dict[str, str]:
    direct: dict[str, str] = {}
    pending: list[str] = []
    for source in strings:
        fixed = fixed_translation(target, source)
        if fixed is not None:
            direct[source] = fixed
        else:
            pending.append(source)

    extras = sorted(_pattern_inner_sources(strings) - set(strings))
    machine_sources = pending + extras
    machine_values = _nllb_many(machine_sources, target)
    raw = dict(zip(machine_sources, machine_values))

    def inner_value(text: str) -> str:
        fixed = fixed_translation(target, text)
        return fixed if fixed is not None else raw[text]

    out = dict(direct)
    for source in pending:
        value = raw[source]
        match = base.FILL_RE.match(source)
        if match:
            inner = inner_value(match.group(1))
            value = f"Write in Slovak: «{inner}»." if target == "en" else f"Напиши по-словацки: «{inner}»."
        match = base.TRUE_FALSE_RE.match(source)
        if match:
            inner = inner_value(match.group(2))
            value = (f"True or false? «{match.group(1)}» means «{inner}»." if target == "en"
                     else f"Правда или нет? «{match.group(1)}» означает «{inner}».")
        match = base.CHOOSE_RE.match(source)
        if match:
            inner = inner_value(match.group(1))
            value = (f"Choose the exact Slovak item for the meaning «{inner}»." if target == "en"
                     else f"Выбери точную словацкую единицу для значения «{inner}».")
        match = base.REPLY_RE.match(source)
        if match:
            inner = inner_value(match.group(1))
            value = (f"Which line conveys the meaning «{inner}»?" if target == "en"
                     else f"Какая реплика передаёт смысл «{inner}»?")
        _sanity(target, source, value)
        out[source] = value

    for source, value in direct.items():
        _sanity(target, source, value)
    return out


base.fixed_translation = fixed_translation
base.translate_sources = translate_sources

localize_lesson = v2.localize_lesson
quality_audit = v2.quality_audit
verify = v2.verify
validate_schema = v2.validate_schema

if __name__ == "__main__":
    base.main()
