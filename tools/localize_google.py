from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterable

MARKER_RE = re.compile(r"(?m)^<<<SEG(\d{4,})>>> ?")


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
    out: list[str | None] = [None] * len(texts)
    for batch in pack_batches(texts, max_chars=max_chars, max_items=max_items):
        translated = translate_batch(batch, source_lang, target_lang)
        for idx, value in translated.items():
            out[idx] = value
    if any(value is None for value in out):
        raise RuntimeError("translation batch left missing results")
    return [value for value in out if value is not None]
