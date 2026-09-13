from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

import localize_clean as base


def rate_limit_delay(attempt: int) -> int:
    return min(8 * (2 ** attempt), 45)


def robust_google(text: str, source: str, target: str, attempts: int = 8) -> str:
    params = urllib.parse.urlencode({"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text})
    url = "https://translate.googleapis.com/translate_a/single?" + params
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.load(response)
            result = "".join(part[0] for part in payload[0] if part and part[0]).strip()
            if not result:
                raise RuntimeError("empty translation")
            return result
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code == 429 and attempt + 1 < attempts:
                delay = rate_limit_delay(attempt)
                print(f"Google 429: sleeping {delay}s before retry {attempt + 2}/{attempts}", flush=True)
                time.sleep(delay)
                continue
            if attempt + 1 >= attempts:
                break
            time.sleep(min(2 ** attempt, 8))
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            last = exc
            if attempt + 1 >= attempts:
                break
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"Google translation failed after {attempts} attempts: {last}")


def pack_batches(texts: list[str], max_chars: int = 4200, max_items: int = 60):
    batches = []
    current = []
    size = 0
    for index, text in enumerate(texts):
        cost = len(text) + 24
        if current and (len(current) >= max_items or size + cost > max_chars):
            batches.append(current)
            current = []
            size = 0
        current.append((index, text))
        size += cost
    if current:
        batches.append(current)
    return batches


def translate_many(texts: list[str], source: str, target: str) -> list[str]:
    if not texts:
        return []
    result: list[str | None] = [None] * len(texts)
    batches = pack_batches(texts)
    for number, batch in enumerate(batches, 1):
        ids = [index for index, _ in batch]
        raw = robust_google(base._marked(batch), source, target)
        try:
            values = base._parse_marked(raw, ids)
        except ValueError:
            # Marker corruption is not a rate-limit condition. Fall back only in
            # this case, with a small pause between individual requests.
            values = {}
            for index, text in batch:
                values[index] = robust_google(text, source, target)
                time.sleep(0.25)
        for index, value in values.items():
            result[index] = value
        print(f"{source}->{target}: {number}/{len(batches)} batches", flush=True)
        time.sleep(0.65)
    if any(value is None for value in result):
        raise RuntimeError("missing translation result")
    return [value for value in result if value is not None]


def suffix_localize(obj, key, translations):
    value = obj.get(key)
    if not isinstance(value, str) or not base.CYR.search(value):
        return
    if key == "uk":
        obj["ru"] = translations["ru"][value]
        obj["en"] = translations["en"][value]
        return
    root = key[:-2] if key.endswith("Uk") else key
    obj[root + "Ru"] = translations["ru"][value]
    obj[root + "En"] = translations["en"][value]


_original_collect_sources = base.collect_sources
LEGACY_SUPPORT_KEYS = {"left", "right", "value", "sender", "body", "day", "hours", "correct"}


def collect_sources(value, out, key=None):
    _original_collect_sources(value, out, key)

    def walk(node):
        if isinstance(node, dict):
            for k, child in node.items():
                if k in LEGACY_SUPPORT_KEYS and isinstance(child, str) and base.CYR.search(child):
                    out.add(child)
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)


base._google = robust_google
base._pack = pack_batches
base.translate_many = translate_many
base.suffix_localize = suffix_localize
base.collect_sources = collect_sources

fixed_translation = base.fixed_translation
localize_lesson = base.localize_lesson
quality_audit = base.quality_audit
verify = base.verify
validate_schema = base.validate_schema

if __name__ == "__main__":
    base.main()
