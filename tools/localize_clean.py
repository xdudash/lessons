from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff]")
LATIN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ž]+(?:[’'/-][A-Za-zÀ-ÖØ-öø-ž]+)*")
MARKER = re.compile(r"(?m)^<<<SEG(\d{4,})>>> ?")

EXACT = {
    "Що тут сказати найприродніше?": {"en": "What sounds most natural here?", "ru": "Что здесь звучит естественнее всего?"},
    "З’єднай слова або фрази з точними значеннями.": {"en": "Match the words or phrases with their exact meanings.", "ru": "Соедини слова или фразы с точными значениями."},
    "Заповни пропуски словами з банку.": {"en": "Fill in the blanks using the word bank.", "ru": "Заполни пропуски словами из банка."},
    "Склади словацьке речення за українським змістом.": {"en": "Build the Slovak sentence that matches the Ukrainian meaning.", "ru": "Составь словацкое предложение по украинскому смыслу."},
    "Розташуй репліки в логічній послідовності.": {"en": "Put the lines in a logical order.", "ru": "Расположи реплики в логической последовательности."},
    "Обери всі цільові одиниці цього уроку.": {"en": "Select all target items from this lesson.", "ru": "Выбери все целевые единицы этого урока."},
    "Прочитай короткий контекст і знайди точну інформацію.": {"en": "Read the short context and find the exact information.", "ru": "Прочитай короткий контекст и найди точную информацию."},
    "З’єднай цільову одиницю з її значенням.": {"en": "Match the target item with its meaning.", "ru": "Соедини целевую единицу с её значением."},
    "Передай цей зміст словацькою, використавши модель уроку.": {"en": "Express this meaning in Slovak using the lesson pattern.", "ru": "Передай этот смысл по-словацки, используя модель урока."},
    "Перевір кілька тверджень про значення.": {"en": "Check the statements about meaning.", "ru": "Проверь несколько утверждений о значении."},
    "Яка відповідь точно передає потрібний зміст повідомлення?": {"en": "Which answer conveys the intended message accurately?", "ru": "Какой ответ точно передаёт нужный смысл сообщения?"},
    "Розташуй слова в природному порядку.": {"en": "Put the words in a natural order.", "ru": "Расположи слова в естественном порядке."},
    "Почати урок": {"en": "Start lesson", "ru": "Начать урок"},
    "Далі": {"en": "Next", "ru": "Далее"},
    "До практики": {"en": "Start practice", "ru": "К практике"},
}

LEXICAL = {
    "як / ніж": {"en": "as / than", "ru": "как / чем"},
    "милий": {"en": "nice", "ru": "милый"},
    "симпатичний": {"en": "likeable", "ru": "симпатичный"},
    "веселий": {"en": "cheerful", "ru": "весёлый"},
    "тихий": {"en": "quiet", "ru": "тихий"},
    "спокійний": {"en": "calm", "ru": "спокойный"},
    "активний": {"en": "active", "ru": "активный"},
    "лінивий": {"en": "lazy", "ru": "ленивый"},
    "працьовитий": {"en": "hardworking", "ru": "трудолюбивый"},
    "цікавий": {"en": "interesting", "ru": "интересный"},
    "двоюрідний брат": {"en": "cousin", "ru": "двоюродный брат"},
    "одружений": {"en": "married", "ru": "женатый"},
    "іноді": {"en": "sometimes", "ru": "иногда"},
    "часто": {"en": "often", "ru": "часто"},
    "дядько": {"en": "uncle", "ru": "дядя"},
    "менше": {"en": "less", "ru": "меньше"},
    "подруга": {"en": "female friend", "ru": "подруга"},
    "друг": {"en": "friend", "ru": "друг"},
}

MEANING_RE = re.compile(r"^Що означає «([^»]+)»\?$")
FILL_RE = re.compile(r"^Впиши словацькою: «([^»]+)»\.$")
TRUE_FALSE_RE = re.compile(r"^Правда чи ні\? «([^»]+)» означає «([^»]+)»\.$")
CONTEXT_RE = re.compile(r"^Що означає виділена одиниця в контексті: «([^»]+)»\?$")
CHOOSE_RE = re.compile(r"^Обери точну словацьку одиницю для значення «([^»]+)»\.$")
REPLY_RE = re.compile(r"^Яка репліка передає зміст «([^»]+)»\?$")

SAFE_TEXT_KEYS = {
    "title", "topic", "description", "intro", "completionMessage", "eyebrow",
    "shortDescription", "subtitle", "goal", "body", "text", "shortRule",
    "instruction", "question", "prompt", "explanation", "hint", "statement",
    "sentence", "displaySentence", "context", "target", "situation", "phrase",
    "source", "successMessage", "label", "mistakesMessage", "alt",
}

BAD_EN = ("truth or no", "word-word", "smudge", "ministations", "what kind of man am i")
BAD_RU = ("как / нож", "как/нож", "разыщи", "словами наклейки")


def support_text(value: Any) -> str | None:
    if isinstance(value, str) and CYR.search(value):
        return value
    if isinstance(value, dict) and isinstance(value.get("uk"), str) and value["uk"].strip():
        return value["uk"]
    return None


def fixed_translation(target: str, source: str) -> str | None:
    if source in EXACT:
        return EXACT[source][target]
    if source in LEXICAL:
        return LEXICAL[source][target]
    m = MEANING_RE.match(source)
    if m and not CYR.search(m.group(1)):
        return f"What does «{m.group(1)}» mean?" if target == "en" else f"Что означает «{m.group(1)}»?"
    m = CONTEXT_RE.match(source)
    if m and not CYR.search(m.group(1)):
        return (f"What does the highlighted item mean in context: «{m.group(1)}»?" if target == "en"
                else f"Что означает выделенная единица в контексте: «{m.group(1)}»?")
    m = FILL_RE.match(source)
    if m and m.group(1) in LEXICAL:
        inner = LEXICAL[m.group(1)][target]
        return f"Write in Slovak: «{inner}»." if target == "en" else f"Напиши по-словацки: «{inner}»."
    m = TRUE_FALSE_RE.match(source)
    if m and m.group(2) in LEXICAL:
        inner = LEXICAL[m.group(2)][target]
        return (f"True or false? «{m.group(1)}» means «{inner}»." if target == "en"
                else f"Правда или нет? «{m.group(1)}» означает «{inner}».")
    return None


def _google(text: str, source: str, target: str, attempts: int = 6) -> str:
    params = urllib.parse.urlencode({"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text})
    url = "https://translate.googleapis.com/translate_a/single?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                payload = json.load(response)
            out = "".join(part[0] for part in payload[0] if part and part[0]).strip()
            if not out:
                raise RuntimeError("empty translation")
            return out
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            last = exc
            if attempt + 1 == attempts:
                break
            time.sleep(min(2 ** attempt, 10))
    raise RuntimeError(f"Google translation failed: {last}")


def _pack(texts: list[str], max_chars: int = 2200, max_items: int = 35) -> list[list[tuple[int, str]]]:
    batches: list[list[tuple[int, str]]] = []
    cur: list[tuple[int, str]] = []
    size = 0
    for i, text in enumerate(texts):
        cost = len(text) + 24
        if cur and (len(cur) >= max_items or size + cost > max_chars):
            batches.append(cur); cur = []; size = 0
        cur.append((i, text)); size += cost
    if cur:
        batches.append(cur)
    return batches


def _marked(batch: list[tuple[int, str]]) -> str:
    return "\n".join(f"<<<SEG{i:04d}>>> {text}" for i, text in batch)


def _parse_marked(raw: str, ids: Iterable[int]) -> dict[int, str]:
    matches = list(MARKER.finditer(raw))
    out: dict[int, str] = {}
    for pos, match in enumerate(matches):
        i = int(match.group(1)); start = match.end(); end = matches[pos + 1].start() if pos + 1 < len(matches) else len(raw)
        out[i] = raw[start:end].strip()
    expected = set(ids)
    if set(out) != expected or any(not out[i] for i in expected):
        raise ValueError("marker mismatch")
    return out


def translate_many(texts: list[str], source: str, target: str) -> list[str]:
    result: list[str | None] = [None] * len(texts)
    batches = _pack(texts)
    for n, batch in enumerate(batches, 1):
        ids = [i for i, _ in batch]
        try:
            values = _parse_marked(_google(_marked(batch), source, target), ids)
        except (ValueError, RuntimeError):
            values = {i: _google(text, source, target) for i, text in batch}
        for i, value in values.items():
            result[i] = value
        print(f"{source}->{target}: {n}/{len(batches)} batches", flush=True)
    if any(v is None for v in result):
        raise RuntimeError("missing translation result")
    return [v for v in result if v is not None]


def _sanity(target: str, source: str, value: str) -> None:
    if not value.strip() or WEIRD.search(value):
        raise RuntimeError(f"bad {target}: {source!r} -> {value!r}")
    if target == "en" and CYR.search(value):
        raise RuntimeError(f"Cyrillic leaked into English: {source!r} -> {value!r}")
    if target == "ru" and UK_ONLY.search(value):
        raise RuntimeError(f"Ukrainian letters leaked into Russian: {source!r} -> {value!r}")


def _translate_inner(target: str, text: str) -> str:
    fixed = fixed_translation(target, text)
    if fixed:
        return fixed
    return _google(text, "uk", target)


def normalize(target: str, source: str, machine: str) -> str:
    fixed = fixed_translation(target, source)
    if fixed:
        return fixed
    m = FILL_RE.match(source)
    if m:
        inner = fixed_translation(target, m.group(1)) or _translate_inner(target, m.group(1))
        return f"Write in Slovak: «{inner}»." if target == "en" else f"Напиши по-словацки: «{inner}»."
    m = TRUE_FALSE_RE.match(source)
    if m:
        inner = fixed_translation(target, m.group(2)) or _translate_inner(target, m.group(2))
        return (f"True or false? «{m.group(1)}» means «{inner}»." if target == "en"
                else f"Правда или нет? «{m.group(1)}» означает «{inner}».")
    m = CHOOSE_RE.match(source)
    if m:
        inner = fixed_translation(target, m.group(1)) or _translate_inner(target, m.group(1))
        return (f"Choose the exact Slovak item for the meaning «{inner}»." if target == "en"
                else f"Выбери точную словацкую единицу для значения «{inner}».")
    m = REPLY_RE.match(source)
    if m:
        inner = _translate_inner(target, m.group(1))
        return (f"Which line conveys the meaning «{inner}»?" if target == "en"
                else f"Какая реплика передаёт смысл «{inner}»?")
    return machine


def translate_sources(sources: list[str], target: str) -> dict[str, str]:
    out: dict[str, str] = {}
    pending: list[str] = []
    for source in sources:
        fixed = fixed_translation(target, source)
        if fixed is not None:
            out[source] = fixed
        else:
            pending.append(source)
    machine = translate_many(pending, "uk", target)
    for source, value in zip(pending, machine):
        value = normalize(target, source, value)
        _sanity(target, source, value)
        out[source] = value
    return out


def add_source(out: set[str], value: Any) -> None:
    source = support_text(value)
    if source:
        out.add(source)


def collect_sources(value: Any, out: set[str], key: str | None = None) -> None:
    if isinstance(value, dict):
        if isinstance(value.get("uk"), str):
            add_source(out, value["uk"])
        for k, child in value.items():
            if k.endswith("Uk") and k != "pronunciationUk" and isinstance(child, str):
                add_source(out, child)
            elif k in SAFE_TEXT_KEYS:
                add_source(out, child)
            collect_sources(child, out, k)
    elif isinstance(value, list):
        for child in value:
            collect_sources(child, out, key)


def localized(value: Any, translations: dict[str, dict[str, str]]) -> Any:
    source = support_text(value)
    if not source:
        return value
    base = dict(value) if isinstance(value, dict) else {"uk": source}
    base.setdefault("uk", source)
    base["ru"] = translations["ru"][source]
    base["en"] = translations["en"][source]
    return base


def suffix_localize(obj: dict[str, Any], key: str, translations: dict[str, dict[str, str]]) -> None:
    value = obj.get(key)
    if not isinstance(value, str) or not CYR.search(value):
        return
    obj[key + "Ru"] = translations["ru"][value]
    obj[key + "En"] = translations["en"][value]


def enrich_direct_maps(value: Any, translations: dict[str, dict[str, str]]) -> None:
    if isinstance(value, dict):
        uk = value.get("uk")
        if isinstance(uk, str) and CYR.search(uk):
            value["ru"] = translations["ru"][uk]
            value["en"] = translations["en"][uk]
        for k in list(value):
            if k.endswith("Uk") and k != "pronunciationUk":
                suffix_localize(value, k, translations)
        for child in list(value.values()):
            enrich_direct_maps(child, translations)
    elif isinstance(value, list):
        for child in value:
            enrich_direct_maps(child, translations)


def _localize_key(obj: dict[str, Any], key: str, translations: dict[str, dict[str, str]]) -> None:
    if key in obj and support_text(obj[key]):
        obj[key] = localized(obj[key], translations)


def _legacy_siblings(obj: dict[str, Any], keys: Iterable[str], translations: dict[str, dict[str, str]]) -> None:
    for key in keys:
        suffix_localize(obj, key, translations)


def localize_lesson(lesson: dict[str, Any], translations: dict[str, dict[str, str]]) -> None:
    loc = lesson.setdefault("localization", {})
    loc["uiLanguages"] = ["uk", "ru", "en"]
    loc["targetLanguage"] = "sk"
    loc["fallbackUiLanguage"] = "uk"

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        _localize_key(lesson, key, translations)

    start = lesson.get("startScreen") or {}
    for key in ("eyebrow", "title", "shortDescription", "subtitle", "goal"):
        _localize_key(start, key, translations)
    if isinstance(start.get("outcomes"), list):
        start["outcomes"] = [localized(x, translations) if support_text(x) else x for x in start["outcomes"]]

    for screen in lesson.get("theoryScreens", []) or []:
        if not isinstance(screen, dict):
            continue
        for key in ("title", "text", "body", "shortRule"):
            _localize_key(screen, key, translations)
        _legacy_siblings(screen, ("exampleUk",), translations)
        for example in screen.get("examples", []) or []:
            if isinstance(example, dict):
                if "translation" in example:
                    _localize_key(example, "translation", translations)
                _legacy_siblings(example, ("uk",), translations)

    ws = lesson.get("wordsScreen") or {}
    for key in ("title", "description", "subtitle"):
        _localize_key(ws, key, translations)
    for item in ws.get("items", []) or []:
        if isinstance(item, dict):
            _legacy_siblings(item, ("uk", "exampleUk"), translations)

    for word in lesson.get("words", []) or []:
        if not isinstance(word, dict):
            continue
        _legacy_siblings(word, ("uk", "exampleUk"), translations)
        if isinstance(word.get("uk"), str) and CYR.search(word["uk"]):
            source = word["uk"]
            word["translation"] = localized(word.get("translation") or source, translations)
        example = word.get("example")
        if isinstance(example, dict) and "translation" in example:
            _localize_key(example, "translation", translations)

    for ex in lesson.get("exercises", []) or []:
        if not isinstance(ex, dict):
            continue
        for key in ("instruction", "question", "prompt", "explanation", "hint", "text", "statement", "sentence", "displaySentence", "context", "target", "situation", "phrase", "source", "successMessage"):
            _localize_key(ex, key, translations)
        for option in ex.get("options", []) or []:
            if isinstance(option, dict):
                _localize_key(option, "text", translations)
        for pair in ex.get("pairs", []) or []:
            if isinstance(pair, dict):
                _legacy_siblings(pair, ("left", "right"), translations)
        for statement in ex.get("statements", []) or []:
            if isinstance(statement, dict):
                _legacy_siblings(statement, ("text",), translations)
        for category in ex.get("categories", []) or []:
            if isinstance(category, dict):
                _legacy_siblings(category, ("title", "label"), translations)
        document = ex.get("document")
        if isinstance(document, dict):
            _legacy_siblings(document, ("title",), translations)
            for field in document.get("fields", []) or []:
                if isinstance(field, dict): _legacy_siblings(field, ("label", "value"), translations)
        message = ex.get("message")
        if isinstance(message, dict): _legacy_siblings(message, ("sender", "body"), translations)
        schedule = ex.get("schedule")
        if isinstance(schedule, dict):
            _legacy_siblings(schedule, ("title",), translations)
            for row in schedule.get("rows", []) or []:
                if isinstance(row, dict): _legacy_siblings(row, ("day", "hours"), translations)
        for q in ex.get("questions", []) or []:
            if isinstance(q, dict):
                _legacy_siblings(q, ("question", "correct"), translations)
                for option in q.get("options", []) or []:
                    if isinstance(option, dict): _legacy_siblings(option, ("text",), translations)
        for item in ex.get("items", []) or []:
            if isinstance(item, dict): _legacy_siblings(item, ("text", "label", "title", "question", "prompt"), translations)

    final = lesson.get("finalSituation") or {}
    if isinstance(final, dict):
        for key in ("title", "description", "successMessage"):
            _localize_key(final, key, translations)
        for step in final.get("steps", []) or []:
            if isinstance(step, dict):
                _localize_key(step, "prompt", translations)
                for option in step.get("options", []) or []:
                    if isinstance(option, dict): _localize_key(option, "text", translations)

    result = lesson.get("resultScreen") or {}
    for key in ("title", "subtitle", "text", "mistakesMessage"):
        _localize_key(result, key, translations)
    for skill in result.get("skills", []) or []:
        if isinstance(skill, dict): _localize_key(skill, "label", translations)
    nxt = result.get("nextLesson")
    if isinstance(nxt, dict): _localize_key(nxt, "title", translations)

    assets = lesson.get("assets") or {}
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict): _localize_key(image, "alt", translations)

    enrich_direct_maps(lesson, translations)


def audit_lesson(lesson: dict[str, Any], where: str, errors: list[str]) -> None:
    loc = lesson.get("localization", {})
    if loc.get("uiLanguages") != ["uk", "ru", "en"]:
        errors.append(f"{where}: uiLanguages")
    if loc.get("targetLanguage") != "sk":
        errors.append(f"{where}: targetLanguage")

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("uk"), str) and CYR.search(value["uk"]):
                for lang in ("ru", "en"):
                    if not isinstance(value.get(lang), str) or not value[lang].strip():
                        errors.append(f"{path}: missing {lang}")
                if isinstance(value.get("en"), str) and CYR.search(value["en"]): errors.append(f"{path}: Cyrillic in en")
                if isinstance(value.get("ru"), str) and UK_ONLY.search(value["ru"]): errors.append(f"{path}: Ukrainian in ru")
                for lang in ("ru", "en"):
                    if isinstance(value.get(lang), str) and WEIRD.search(value[lang]): errors.append(f"{path}: foreign script in {lang}")
            for key, child in value.items():
                if key.endswith("Uk") and key != "pronunciationUk" and isinstance(child, str) and CYR.search(child):
                    root = key[:-2]
                    if not isinstance(value.get(root + "Ru"), str): errors.append(f"{path}.{key}: missing {root}Ru")
                    if not isinstance(value.get(root + "En"), str): errors.append(f"{path}.{key}: missing {root}En")
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for i, child in enumerate(value): walk(child, f"{path}[{i}]")
    walk(lesson, where)


def quality_audit(levels: list[str]) -> None:
    errors: list[str] = []
    for level in levels:
        expected = 75 if level == "a1" else 90
        files = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"))
        if len(files) != expected: errors.append(f"{level}: expected {expected}, got {len(files)}")
        for path in files:
            lesson = json.loads(path.read_text(encoding="utf-8"))["lessons"][0]
            audit_lesson(lesson, path.name, errors)
            raw = json.dumps(lesson, ensure_ascii=False).casefold()
            for bad in BAD_EN:
                if bad in raw: errors.append(f"{path.name}: bad EN phrase {bad!r}")
            for bad in BAD_RU:
                if bad in raw: errors.append(f"{path.name}: bad RU phrase {bad!r}")
    print(f"MULTILINGUAL/QUALITY AUDIT: errors={len(errors)}")
    for error in errors[:100]: print(error)
    if errors: raise SystemExit(1)


def verify(levels: list[str]) -> None:
    for level in levels:
        expected = 75 if level == "a1" else 90
        files = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"), key=lambda p: int(re.search(r"-l(\d+)\.json$", p.name).group(1)))
        assert len(files) == expected, (level, len(files))
        lessons = [json.loads(p.read_text(encoding="utf-8"))["lessons"][0] for p in files]
        assert len({x["id"] for x in lessons}) == expected
        for left, right in zip(lessons, lessons[1:]):
            nxt = left.get("resultScreen", {}).get("nextLesson")
            got = nxt.get("id") if isinstance(nxt, dict) else nxt
            assert got == right["id"], (left["id"], got, right["id"])
        assert "nextLesson" not in lessons[-1].get("resultScreen", {})
        print(f"{level}: {expected} lessons, chain OK")


def validate_schema(levels: list[str], schema_path: str) -> None:
    from jsonschema import Draft202012Validator
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for level in levels:
        for path in sorted(Path("lessons", level).glob(f"{level}-s*-l*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            for error in validator.iter_errors(doc):
                errors.append(f"{path.name}: {error.message}")
    print(f"CURRENT APP SCHEMA: errors={len(errors)}")
    for error in errors[:100]: print(error)
    if errors: raise SystemExit(1)


def run(levels: list[str]) -> None:
    paths: list[Path] = []
    sources: set[str] = set()
    docs: list[tuple[Path, dict[str, Any]]] = []
    for level in levels:
        expected = 75 if level == "a1" else 90
        current = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"))
        if len(current) != expected: raise SystemExit(f"{level}: expected {expected}, got {len(current)}")
        paths.extend(current)
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8")); docs.append((path, doc))
        collect_sources(doc["lessons"][0], sources)
    ordered = sorted(sources)
    print(f"support strings: {len(ordered)}", flush=True)
    translations = {"en": translate_sources(ordered, "en"), "ru": translate_sources(ordered, "ru")}
    for path, doc in docs:
        localize_lesson(doc["lessons"][0], translations)
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    quality_audit(levels)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", nargs="+", choices=("a1", "a2"), required=True)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--schema")
    args = parser.parse_args()
    if args.verify_only:
        verify(args.levels); return
    if args.audit_only:
        quality_audit(args.levels)
        if args.schema: validate_schema(args.levels, args.schema)
        return
    run(args.levels)


if __name__ == "__main__":
    main()
