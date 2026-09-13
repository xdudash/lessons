from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

UK_SAMPLES = [
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
SK_SAMPLES = [
    "milý",
    "sympatický",
    "veselý",
    "tichý",
    "pokojný",
    "aktívny",
    "lenivý",
    "pracovitý",
    "Som milý a sympatický, väčšinou veselý, ale niekedy tichý.",
    "Som pokojný, aktívny a pracovitý človek.",
    "Nechcem byť lenivý; chcem byť zaujímavý človek.",
]


def translate(text: str, source: str, target: str) -> str:
    params = urllib.parse.urlencode({"client":"gtx","sl":source,"tl":target,"dt":"t","q":text})
    url = "https://translate.googleapis.com/translate_a/single?" + params
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    return "".join(part[0] for part in payload[0] if part and part[0])


def show(samples: list[str], source: str) -> None:
    for text in samples:
        en = translate(text, source, "en")
        ru = translate(text, source, "ru")
        print(f"{source.upper()}:", text, flush=True)
        print("EN:", en, flush=True)
        print("RU:", ru, flush=True)
        print("---", flush=True)
        time.sleep(0.03)


def main() -> None:
    print("=== Ukrainian individual ===", flush=True)
    show(UK_SAMPLES, "uk")
    print("=== Ukrainian marker batch ===", flush=True)
    batch = "\n".join(f"<<<SEG{i:03d}>>> {text}" for i, text in enumerate(UK_SAMPLES))
    print("EN_BATCH:", translate(batch, "uk", "en"), flush=True)
    print("RU_BATCH:", translate(batch, "uk", "ru"), flush=True)
    print("=== Slovak lexical/context ===", flush=True)
    show(SK_SAMPLES, "sk")


if __name__ == "__main__":
    main()
