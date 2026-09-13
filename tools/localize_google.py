from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

MARKER_RE = re.compile(r"(?m)^<<<SEG(\d{4,})>>> ?")
CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-žА-Яа-яЁёІіЇїЄєҐґ]+")

BAD_EN = (
    "smudge",
    "ministations",
    "truth or no",
    "word-word",
    "diptong",
    "delete values",
    "real real",
    "what kind of man am i",
    "oh, honey",
    "slovak is a reality",
)
BAD_RU = (
    "как/нож",
    "как / нож",
    "разыщи",
    "словами наклейки",
    "миниситац",
)


def pack_batches(texts: list[str], *, max_chars: int = 1200, max_items: int = 25) -> list[list[tuple[int, str]]]:
    """Pack indexed strings without reordering them."""
    if max_chars <= 0 or max_items <= 0:
        raise ValueError("max_chars and max_items must be positive")

    batches: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    current_chars = 0

    for idx, text in enumerate(texts):
        if not isinstance(text, str):
            raise TypeError(f"text {idx} is not a string")
        marker_cost = len(f"<<<SEG{idx:04d}>>> ") + 1
        item_chars = len(text) + marker_cost
        if current and (len(current) >= max_items or current_chars + item_chars > max_chars):
            batches.append(current)
            current = []
            current_chars = 0
        current.append((idx, text))
        current_chars += item_chars
    if current:
        batches.append(current)
    return batches


def build_marked(batch: list[tuple[int, str]]) -> str:
    return "\n".join(f"<<<SEG{idx:04d}>>> {text}" for idx, text in batch)


def parse_marked(raw: str, expected_ids: Iterable[int]) -> dict[int, str]:
    """Parse translated marker batches and require exact marker preservation."""
    expected = list(expected_ids)
    matches = list(MARKER_RE.finditer(raw))
    if not matches:
        raise ValueError("no SEG markers found")

    out: dict[int, str] = {}
    for pos, match in enumerate(matches):
        seg_id = int(match.group(1))
        if seg_id in out:
            raise ValueError(f"duplicate SEG marker {seg_id}")
        start = match.end()
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(raw)
        out[seg_id] = raw[start:end].strip()

    if set(out) != set(expected):
        missing = sorted(set(expected) - set(out))
        extra = sorted(set(out) - set(expected))
        raise ValueError(f"SEG marker mismatch: missing={missing} extra={extra}")
    if any(not out[idx] for idx in expected):
        raise ValueError("empty translated SEG")
    return out


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold().replace("ё", "е")
    return "".join(ch for ch in text if ch.isalnum())


def choose_lexical_candidate(
    *,
    source_uk: str,
    uk_candidate: str,
    uk_back: str,
    sk_candidate: str,
    sk_back: str,
) -> str:
    """Prefer the candidate whose round-trip returns to the Ukrainian source."""
    source = _norm(source_uk)
    uk_matches = _norm(uk_back) == source
    sk_matches = _norm(sk_back) == source
    if sk_matches and not uk_matches:
        return sk_candidate
    return uk_candidate


def google_translate(text: str, source_lang: str, target_lang: str, *, attempts: int = 5) -> str:
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        "q": text,
    })
    url = "https://translate.googleapis.com/translate_a/single?" + params
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.load(response)
            value = "".join(part[0] for part in payload[0] if part and part[0]).strip()
            if not value:
                raise RuntimeError("empty Google translation")
            return value
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 >= attempts:
                break
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"Google translation failed after {attempts} attempts: {last_error}")


def translate_batch(batch: list[tuple[int, str]], source_lang: str, target_lang: str) -> dict[int, str]:
    marked = build_marked(batch)
    expected = [idx for idx, _ in batch]
    try:
        translated = google_translate(marked, source_lang, target_lang)
        return parse_marked(translated, expected)
    except (ValueError, RuntimeError):
        return {idx: google_translate(text, source_lang, target_lang) for idx, text in batch}


def translate_many(texts: list[str], source_lang: str, target_lang: str, *, max_chars: int = 1200, max_items: int = 25) -> list[str]:
    if not texts:
        return []
    out: list[str | None] = [None] * len(texts)
    batches = pack_batches(texts, max_chars=max_chars, max_items=max_items)
    for number, batch in enumerate(batches, 1):
        translated = translate_batch(batch, source_lang, target_lang)
        for idx, value in translated.items():
            out[idx] = value
        print(f"{source_lang}->{target_lang}: batch {number}/{len(batches)}", flush=True)
    if any(value is None for value in out):
        raise RuntimeError("translation batch left missing results")
    return [value for value in out if value is not None]


def _sanity(target: str, source: str, value: str) -> None:
    if not value.strip():
        raise RuntimeError(f"empty {target} translation for {source!r}")
    if WEIRD.search(value):
        raise RuntimeError(f"foreign script in {target}: {source!r} -> {value!r}")
    if target == "en" and CYR.search(value):
        raise RuntimeError(f"Cyrillic leaked into English: {source!r} -> {value!r}")
    if target == "ru" and UK_ONLY.search(value):
        raise RuntimeError(f"Ukrainian letters leaked into Russian: {source!r} -> {value!r}")


def make_support_translator():
    import localize_a1_a2 as base
    import translation_fixes as fixes

    def translate_sources(strings: list[str], target: str) -> dict[str, str]:
        result: dict[str, str] = {}
        pending: list[str] = []
        for source in strings:
            fixed = fixes.fixed_translation(target, source)
            if fixed is not None:
                result[source] = fixed
            else:
                pending.append(source)

        segmented = {source: base.split_translation_segments(source) for source in pending}
        cores = sorted({piece.strip() for parts in segmented.values() for translate, piece in parts if translate and piece.strip()})
        translated_values = translate_many(cores, "uk", target)
        translated = dict(zip(cores, translated_values))

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
            for flag, literal in parts:
                if not flag and base.LATIN_TOKEN.fullmatch(literal) and literal not in value:
                    raise RuntimeError(f"lost Slovak/Latin token {literal!r}: {source!r} -> {value!r}")
            _sanity(target, source, value)
            result[source] = value
        return result

    return translate_sources


def _is_sentence(sk: str) -> bool:
    return len(WORD_RE.findall(sk)) >= 2


def anchor_slovak_examples(docs: list[dict[str, Any]]) -> None:
    """Use the target Slovak sentence as the semantic anchor for full examples."""
    refs: list[tuple[str, dict[str, Any]]] = []
    for doc in docs:
        lesson = doc["lessons"][0]
        for screen in lesson.get("theoryScreens", []) or []:
            for example in screen.get("examples", []) or []:
                sk = example.get("sk")
                tr = example.get("translation")
                if isinstance(sk, str) and _is_sentence(sk) and isinstance(tr, dict):
                    refs.append((sk, tr))
        for word in lesson.get("words", []) or []:
            example = word.get("example")
            if isinstance(example, dict):
                sk = example.get("sk")
                tr = example.get("translation")
                if isinstance(sk, str) and _is_sentence(sk) and isinstance(tr, dict):
                    refs.append((sk, tr))

    unique = sorted({sk for sk, _ in refs})
    if not unique:
        return
    en = dict(zip(unique, translate_many(unique, "sk", "en")))
    ru = dict(zip(unique, translate_many(unique, "sk", "ru")))
    for sk, tr in refs:
        tr["en"] = en[sk]
        tr["ru"] = ru[sk]
    print(f"Slovak-anchored examples: {len(unique)}", flush=True)


def refine_word_lexicon(docs: list[dict[str, Any]]) -> None:
    """Resolve short English lexical ambiguity with Slovak candidates + round trip."""
    import translation_fixes as fixes

    refs: list[tuple[str, str, dict[str, Any]]] = []
    for doc in docs:
        for word in doc["lessons"][0].get("words", []) or []:
            sk = word.get("sk")
            uk = word.get("uk")
            tr = word.get("translation")
            if isinstance(sk, str) and isinstance(uk, str) and isinstance(tr, dict):
                refs.append((sk, uk, tr))

    pairs = sorted({(sk, uk) for sk, uk, _ in refs})
    if not pairs:
        return

    sk_texts = [sk for sk, _ in pairs]
    sk_en_values = translate_many(sk_texts, "sk", "en")
    sk_en = dict(zip(pairs, sk_en_values))

    uk_candidates = [next(tr["en"] for sk2, uk2, tr in refs if sk2 == sk and uk2 == uk) for sk, uk in pairs]
    uk_back_values = translate_many(uk_candidates, "en", "uk")
    sk_back_values = translate_many(sk_en_values, "en", "uk")

    chosen: dict[tuple[str, str], str] = {}
    for pair, uk_candidate, uk_back, sk_candidate, sk_back in zip(
        pairs, uk_candidates, uk_back_values, sk_en_values, sk_back_values
    ):
        sk, uk = pair
        fixed = fixes.lexical("en", uk)
        chosen[pair] = fixed or choose_lexical_candidate(
            source_uk=uk,
            uk_candidate=uk_candidate,
            uk_back=uk_back,
            sk_candidate=sk_candidate,
            sk_back=sk_back,
        )

    for sk, uk, tr in refs:
        fixed_ru = fixes.lexical("ru", uk)
        if fixed_ru:
            tr["ru"] = fixed_ru
        tr["en"] = chosen[(sk, uk)]
    print(f"Lexical entries refined: {len(pairs)}", flush=True)


def quality_audit(level: str) -> None:
    files = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"))
    errors: list[str] = []

    def walk(value: Any, where: str) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("en"), str):
                low = value["en"].casefold()
                for bad in BAD_EN:
                    if bad in low:
                        errors.append(f"{where}.en contains {bad!r}: {value['en']!r}")
            if isinstance(value.get("ru"), str):
                low = value["ru"].casefold()
                for bad in BAD_RU:
                    if bad in low:
                        errors.append(f"{where}.ru contains {bad!r}: {value['ru']!r}")
            for key, child in value.items():
                walk(child, f"{where}.{key}")
        elif isinstance(value, list):
            for idx, child in enumerate(value):
                walk(child, f"{where}[{idx}]")

    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        walk(doc, path.name)

    if level == "a2":
        first = json.loads(Path("lessons/a2/a2-s01-l01.json").read_text(encoding="utf-8"))["lessons"][0]
        if first["title"].get("en") != "What kind of person am I?":
            errors.append(f"A2 L01 title EN: {first['title'].get('en')!r}")
        if first["title"].get("ru") != "Какой я человек?":
            errors.append(f"A2 L01 title RU: {first['title'].get('ru')!r}")
        words = {word["sk"]: word for word in first.get("words", [])}
        if words.get("sympatický", {}).get("translation", {}).get("en") not in {"likable", "likeable", "nice", "pleasant"}:
            errors.append(f"A2 sympatický EN: {words.get('sympatický', {}).get('translation', {}).get('en')!r}")

    print(f"QUALITY {level}: files={len(files)} errors={len(errors)}", flush=True)
    for error in errors[:100]:
        print(error, flush=True)
    if errors:
        raise SystemExit(1)


def run_level(level: str) -> None:
    import localize_a1_a2 as base

    expected = 75 if level == "a1" else 90
    paths = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"))
    if len(paths) != expected:
        raise SystemExit(f"expected {expected} lessons, got {len(paths)}")

    docs: list[tuple[Path, dict[str, Any]]] = []
    sources: set[str] = set()
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        docs.append((path, doc))
        sources |= base.collect_sources(doc["lessons"][0])

    ordered = sorted(sources)
    print(f"{level}: unique support strings={len(ordered)}", flush=True)
    translator = make_support_translator()
    en = translator(ordered, "en")
    ru = translator(ordered, "ru")
    localize = base.make_localizer(ru, en)

    for _path, doc in docs:
        base.migrate_lesson(doc["lessons"][0], localize)

    documents = [doc for _, doc in docs]
    refine_word_lexicon(documents)
    anchor_slovak_examples(documents)

    for path, doc in docs:
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    base.WEIRD = WEIRD
    base.audit_level(level)
    quality_audit(level)
    print(f"Google-localized {len(paths)} {level} lessons", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=("a1", "a2"), required=True)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    if args.audit_only:
        quality_audit(args.level)
    else:
        run_level(args.level)


if __name__ == "__main__":
    main()
