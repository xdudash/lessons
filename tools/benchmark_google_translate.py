from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

SAMPLES = [
    "Яка я людина?",
    "Розширюємо опис характеру, особистості та звичок і вчимося порівнювати себе з іншими.",
    "Чудово. Тепер перенеси ці моделі у власні реальні ситуації.",
    "використовувати цільові слова й фрази теми «Яка я людина?»",
    "застосувати їх у реальній мініситуації",
    "Перенесення в реальну ситуацію",
    "Використовуй модель коротко й точно; спочатку зміст, потім форма.",
    "милий",
    "симпатичний",
    "веселий",
    "Впиши словацькою: «як / ніж».",
    "Що тут сказати найприродніше?",
]


def translate(text: str, target: str) -> str:
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "uk",
        "tl": target,
        "dt": "t",
        "q": text,
    })
    url = "https://translate.googleapis.com/translate_a/single?" + params
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    return "".join(part[0] for part in payload[0] if part and part[0])


def main() -> None:
    print("=== individual ===", flush=True)
    for source in SAMPLES:
        en = translate(source, "en")
        ru = translate(source, "ru")
        print("UK:", source, flush=True)
        print("EN:", en, flush=True)
        print("RU:", ru, flush=True)
        print("---", flush=True)
        time.sleep(0.05)

    print("=== marker batch ===", flush=True)
    batch = "\n".join(f"<<<SEG{i:03d}>>> {text}" for i, text in enumerate(SAMPLES))
    print("EN_BATCH:", translate(batch, "en"), flush=True)
    print("RU_BATCH:", translate(batch, "ru"), flush=True)


if __name__ == "__main__":
    main()
