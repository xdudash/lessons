from __future__ import annotations

import argparse
import gc
import json
import re
from pathlib import Path
from typing import Any

CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
UK_ONLY = re.compile(r"[ІіЇїЄєҐґ]")
LATIN_TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ž]+(?:[’'/-][A-Za-zÀ-ÖØ-öø-ž]+)*")
WEIRD = re.compile(r"[\u0370-\u03ff\u0590-\u05ff\u2190-\u21ff]")
LANG_KEYS = {"sk", "uk", "ru", "en"}
MODELS = {
    "en": "Helsinki-NLP/opus-mt-uk-en",
    "ru": "Helsinki-NLP/opus-mt-uk-ru",
}


def has_support_text(value: Any) -> bool:
    return isinstance(value, str) and bool(CYR.search(value))


def source_uk(value: Any) -> str | None:
    if isinstance(value, dict):
        uk = value.get("uk")
        return uk if isinstance(uk, str) and uk.strip() else None
    if has_support_text(value):
        return value
    return None


def is_locale_map(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("uk"), str) and set(value).issubset(LANG_KEYS)


def split_translation_segments(text: str) -> list[tuple[bool, str]]:
    """Keep Latin/Slovak tokens byte-for-byte; translate only chunks containing Cyrillic."""
    parts: list[tuple[bool, str]] = []
    pos = 0
    for match in LATIN_TOKEN.finditer(text):
        if match.start() > pos:
            chunk = text[pos:match.start()]
            parts.append((bool(CYR.search(chunk)), chunk))
        parts.append((False, match.group(0)))
        pos = match.end()
    if pos < len(text):
        chunk = text[pos:]
        parts.append((bool(CYR.search(chunk)), chunk))
    if not parts:
        return [(bool(CYR.search(text)), text)]
    merged: list[tuple[bool, str]] = []
    for flag, chunk in parts:
        if not chunk:
            continue
        if merged and merged[-1][0] == flag:
            merged[-1] = (flag, merged[-1][1] + chunk)
        else:
            merged.append((flag, chunk))
    return merged


def collect_sources(lesson: dict[str, Any]) -> set[str]:
    out: set[str] = set()

    def add(value: Any) -> None:
        uk = source_uk(value)
        if uk:
            out.add(uk)

    def walk_maps(value: Any) -> None:
        if is_locale_map(value):
            add(value)
        if isinstance(value, dict):
            for child in value.values():
                walk_maps(child)
        elif isinstance(value, list):
            for child in value:
                walk_maps(child)

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        add(lesson.get(key))
    ss = lesson.get("startScreen", {})
    for key in ("eyebrow", "title", "shortDescription", "subtitle", "goal"):
        add(ss.get(key))
    for value in ss.get("outcomes", []) or []:
        add(value)
    for screen in lesson.get("theoryScreens", []) or []:
        for key in ("title", "text", "body", "shortRule"):
            add(screen.get(key))
        add(screen.get("exampleUk"))
        for ex in screen.get("examples", []) or []:
            add(ex.get("translation")); add(ex.get("uk"))
    ws = lesson.get("wordsScreen", {})
    for key in ("title", "description", "subtitle"):
        add(ws.get(key))
    for word in lesson.get("words", []) or []:
        add(word.get("translation") or word.get("uk"))
        ex = word.get("example")
        if isinstance(ex, dict): add(ex.get("translation"))
        else: add(word.get("exampleUk"))
    for ex in lesson.get("exercises", []) or []:
        for key in ("instruction", "question", "prompt", "explanation", "hint", "text", "statement", "sentence", "displaySentence", "context", "target", "situation", "phrase", "source", "successMessage"):
            add(ex.get(key))
        for option in ex.get("options", []) or []:
            if isinstance(option, dict): add(option.get("text"))
        for pair in ex.get("pairs", []) or []:
            if isinstance(pair, dict): add(pair.get("left")); add(pair.get("right"))
        for statement in ex.get("statements", []) or []:
            if isinstance(statement, dict): add(statement.get("text"))
        for category in ex.get("categories", []) or []:
            if isinstance(category, dict): add(category.get("title")); add(category.get("label"))
        document = ex.get("document")
        if isinstance(document, dict):
            add(document.get("title"))
            for field in document.get("fields", []) or []:
                if isinstance(field, dict): add(field.get("label")); add(field.get("value"))
        message = ex.get("message")
        if isinstance(message, dict): add(message.get("sender")); add(message.get("body"))
        schedule = ex.get("schedule")
        if isinstance(schedule, dict):
            add(schedule.get("title"))
            for row in schedule.get("rows", []) or []:
                if isinstance(row, dict): add(row.get("day")); add(row.get("hours"))
        for q in ex.get("questions", []) or []:
            if isinstance(q, dict):
                add(q.get("question")); add(q.get("correct"))
                for option in q.get("options", []) or []:
                    if isinstance(option, dict): add(option.get("text"))
        for item in ex.get("items", []) or []:
            if isinstance(item, dict):
                for key in ("text", "label", "title", "question", "prompt"): add(item.get(key))
    final = lesson.get("finalSituation", {})
    if isinstance(final, dict) and final.get("type") == "interactive_scenario":
        for key in ("title", "description", "successMessage"): add(final.get(key))
        for step in final.get("steps", []) or []:
            if isinstance(step, dict):
                add(step.get("prompt"))
                for option in step.get("options", []) or []:
                    if isinstance(option, dict): add(option.get("text"))
    result = lesson.get("resultScreen", {})
    for key in ("title", "text", "subtitle"): add(result.get(key))
    for skill in result.get("skills", []) or []:
        if isinstance(skill, dict): add(skill.get("label"))
    nxt = result.get("nextLesson")
    if isinstance(nxt, dict): add(nxt.get("title"))
    assets = lesson.get("assets", {})
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict): add(image.get("alt"))
    walk_maps(lesson)
    return out


def translate_sources(strings: list[str], target: str) -> dict[str, str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    model_name = MODELS[target]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()

    segmented = {s: split_translation_segments(s) for s in strings}
    chunks = sorted({piece for parts in segmented.values() for translate, piece in parts if translate and piece.strip()})
    translated: dict[str, str] = {}
    batch_size = 48
    with torch.inference_mode():
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=384)
            generated = model.generate(**inputs, max_new_tokens=192, num_beams=1)
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for src, dst in zip(batch, decoded):
                dst = dst.strip()
                if not dst:
                    raise RuntimeError(f"empty {target} translation for {src!r}")
                if WEIRD.search(dst):
                    raise RuntimeError(f"weird script in {target} translation: {src!r} -> {dst!r}")
                if target == "en" and CYR.search(dst):
                    raise RuntimeError(f"Cyrillic leaked into English: {src!r} -> {dst!r}")
                if target == "ru" and UK_ONLY.search(dst):
                    raise RuntimeError(f"Ukrainian letters leaked into Russian: {src!r} -> {dst!r}")
                translated[src] = dst
            print(f"{target}: {min(start + batch_size, len(chunks))}/{len(chunks)} chunks", flush=True)

    result: dict[str, str] = {}
    for source, parts in segmented.items():
        built: list[str] = []
        for translate, piece in parts:
            if translate and piece.strip():
                prefix = piece[: len(piece) - len(piece.lstrip())]
                suffix = piece[len(piece.rstrip()):]
                core = piece.strip()
                built.append(prefix + translated[core] + suffix)
            else:
                built.append(piece)
        value = "".join(built)
        for _flag, literal in parts:
            if LATIN_TOKEN.fullmatch(literal) and literal not in value:
                raise RuntimeError(f"lost literal token {literal!r} in {source!r}")
        result[source] = value

    del model, tokenizer
    gc.collect()
    return result


def make_localizer(ru: dict[str, str], en: dict[str, str]):
    def localize(value: Any) -> Any:
        uk = source_uk(value)
        if not uk:
            return value
        base = dict(value) if isinstance(value, dict) else {}
        base["uk"] = uk; base["ru"] = ru[uk]; base["en"] = en[uk]
        return base
    return localize


def upgrade_locale_maps(value: Any, localize) -> None:
    if isinstance(value, dict):
        if is_locale_map(value):
            upgraded = localize(value); value.clear(); value.update(upgraded)
        for child in list(value.values()): upgrade_locale_maps(child, localize)
    elif isinstance(value, list):
        for child in value: upgrade_locale_maps(child, localize)


def migrate_lesson(lesson: dict[str, Any], localize) -> None:
    loc = lesson.setdefault("localization", {})
    loc["uiLanguages"] = ["uk", "ru", "en"]; loc["targetLanguage"] = "sk"; loc["fallbackUiLanguage"] = "uk"
    for key in ("title", "topic", "description", "intro", "completionMessage"):
        if key in lesson: lesson[key] = localize(lesson[key])
    ss = lesson.get("startScreen", {})
    for key in ("eyebrow", "title", "shortDescription", "subtitle", "goal"):
        if key in ss: ss[key] = localize(ss[key])
    if "outcomes" in ss: ss["outcomes"] = [localize(v) for v in ss.get("outcomes", [])]
    ss.pop("button", None)
    for screen in lesson.get("theoryScreens", []) or []:
        for key in ("title", "text", "body", "shortRule"):
            if key in screen: screen[key] = localize(screen[key])
        if screen.get("exampleUk"):
            screen.setdefault("examples", []).insert(0, {"sk": screen.get("exampleSk", ""), "translation": localize(screen["exampleUk"])})
            screen.pop("exampleSk", None); screen.pop("exampleUk", None)
        for ex in screen.get("examples", []) or []:
            if "translation" in ex: ex["translation"] = localize(ex["translation"])
            elif ex.get("uk"): ex["translation"] = localize(ex["uk"]); ex.pop("uk", None)
        screen.pop("button", None)
    ws = lesson.get("wordsScreen", {})
    for key in ("title", "description", "subtitle"):
        if key in ws: ws[key] = localize(ws[key])
    ws.pop("items", None); ws.pop("button", None)
    for word in lesson.get("words", []) or []:
        word["translation"] = localize(word.get("translation") or word.get("uk"))
        ex = word.get("example")
        if isinstance(ex, dict) and ex.get("sk"):
            ex["translation"] = localize(ex.get("translation") or word.get("exampleUk"))
        elif word.get("exampleSk"):
            word["example"] = {"sk": word["exampleSk"], "translation": localize(word.get("exampleUk", ""))}
    for ex in lesson.get("exercises", []) or []:
        for key in ("instruction", "question", "prompt", "explanation", "hint", "text", "statement", "sentence", "displaySentence", "context", "target", "situation", "phrase", "source", "successMessage"):
            if key in ex and source_uk(ex[key]): ex[key] = localize(ex[key])
        for option in ex.get("options", []) or []:
            if isinstance(option, dict) and "text" in option and source_uk(option["text"]): option["text"] = localize(option["text"])
        for pair in ex.get("pairs", []) or []:
            if isinstance(pair, dict):
                for side in ("left", "right"):
                    if side in pair and source_uk(pair[side]): pair[side] = localize(pair[side])
        for statement in ex.get("statements", []) or []:
            if isinstance(statement, dict) and "text" in statement and source_uk(statement["text"]): statement["text"] = localize(statement["text"])
        for category in ex.get("categories", []) or []:
            if isinstance(category, dict):
                for key in ("title", "label"):
                    if key in category and source_uk(category[key]): category[key] = localize(category[key])
        document = ex.get("document")
        if isinstance(document, dict):
            if "title" in document and source_uk(document["title"]): document["title"] = localize(document["title"])
            for field in document.get("fields", []) or []:
                if isinstance(field, dict):
                    for key in ("label", "value"):
                        if key in field and source_uk(field[key]): field[key] = localize(field[key])
        message = ex.get("message")
        if isinstance(message, dict):
            for key in ("sender", "body"):
                if key in message and source_uk(message[key]): message[key] = localize(message[key])
        schedule = ex.get("schedule")
        if isinstance(schedule, dict):
            if "title" in schedule and source_uk(schedule["title"]): schedule["title"] = localize(schedule["title"])
            for row in schedule.get("rows", []) or []:
                if isinstance(row, dict):
                    for key in ("day", "hours"):
                        if key in row and source_uk(row[key]): row[key] = localize(row[key])
        for q in ex.get("questions", []) or []:
            if isinstance(q, dict):
                if "question" in q and source_uk(q["question"]): q["question"] = localize(q["question"])
                if "correct" in q and source_uk(q["correct"]): q["correct"] = localize(q["correct"])
                for option in q.get("options", []) or []:
                    if isinstance(option, dict) and "text" in option and source_uk(option["text"]): option["text"] = localize(option["text"])
        for item in ex.get("items", []) or []:
            if isinstance(item, dict):
                for key in ("text", "label", "title", "question", "prompt"):
                    if key in item and source_uk(item[key]): item[key] = localize(item[key])
        ex.pop("button", None)
    final = lesson.get("finalSituation", {})
    if isinstance(final, dict) and final.get("type") == "interactive_scenario":
        for key in ("title", "description", "successMessage"):
            if key in final and source_uk(final[key]): final[key] = localize(final[key])
        for step in final.get("steps", []) or []:
            if isinstance(step, dict):
                if "prompt" in step and source_uk(step["prompt"]): step["prompt"] = localize(step["prompt"])
                for option in step.get("options", []) or []:
                    if isinstance(option, dict) and "text" in option and source_uk(option["text"]): option["text"] = localize(option["text"])
    result = lesson.get("resultScreen", {})
    for key in ("title", "text", "subtitle"):
        if key in result and source_uk(result[key]): result[key] = localize(result[key])
    for skill in result.get("skills", []) or []:
        if isinstance(skill, dict) and "label" in skill and source_uk(skill["label"]): skill["label"] = localize(skill["label"])
    nxt = result.get("nextLesson")
    if isinstance(nxt, dict) and "title" in nxt and source_uk(nxt["title"]): nxt["title"] = localize(nxt["title"])
    result.pop("buttons", None); result.pop("mistakesMessage", None); result.pop("nowYouKnow", None)
    assets = lesson.get("assets", {})
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict) and "alt" in image and source_uk(image["alt"]): image["alt"] = localize(image["alt"])
    upgrade_locale_maps(lesson, localize)


def audit_level(level: str) -> None:
    expected = 75 if level == "a1" else 90
    files = sorted(Path("lessons", level).glob(f"{level}-s*-l*.json"))
    errors: list[str] = []
    if len(files) != expected: errors.append(f"expected {expected} files, got {len(files)}")

    def walk(v: Any, where: str) -> None:
        if is_locale_map(v):
            for lang in ("uk", "ru", "en"):
                if not isinstance(v.get(lang), str) or not v[lang].strip(): errors.append(f"{where}: missing {lang}")
            if isinstance(v.get("en"), str) and CYR.search(v["en"]): errors.append(f"{where}: Cyrillic in en")
            if isinstance(v.get("ru"), str) and UK_ONLY.search(v["ru"]): errors.append(f"{where}: Ukrainian letter in ru")
            for lang in ("ru", "en"):
                if isinstance(v.get(lang), str) and WEIRD.search(v[lang]): errors.append(f"{where}: weird script in {lang}")
        if isinstance(v, dict):
            for k, x in v.items(): walk(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v): walk(x, f"{where}[{i}]")

    for p in files:
        lesson = json.loads(p.read_text(encoding="utf-8"))["lessons"][0]
        loc = lesson.get("localization", {})
        if set(loc.get("uiLanguages", [])) != {"uk", "ru", "en"}: errors.append(f"{p.name}: uiLanguages")
        if loc.get("targetLanguage") != "sk": errors.append(f"{p.name}: targetLanguage")
        for key in ("title", "topic", "description", "intro", "completionMessage"):
            if not is_locale_map(lesson.get(key)): errors.append(f"{p.name}:{key} not localized")
        if "button" in lesson.get("startScreen", {}): errors.append(f"{p.name}: hardcoded start button")
        if "items" in lesson.get("wordsScreen", {}): errors.append(f"{p.name}: legacy wordsScreen.items")
        walk(lesson, p.name)
    print(f"AUDIT {level}: files={len(files)} errors={len(errors)}")
    for e in errors[:100]: print(e)
    if errors: raise SystemExit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", choices=("a1", "a2"), required=True)
    ap.add_argument("--audit-only", action="store_true")
    args = ap.parse_args()
    if args.audit_only:
        audit_level(args.level); return
    expected = 75 if args.level == "a1" else 90
    paths = sorted(Path("lessons", args.level).glob(f"{args.level}-s*-l*.json"))
    if len(paths) != expected: raise SystemExit(f"expected {expected} lessons, got {len(paths)}")
    docs: list[tuple[Path, dict[str, Any]]] = []; strings: set[str] = set()
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8")); lesson = doc["lessons"][0]
        docs.append((path, doc)); strings |= collect_sources(lesson)
    ordered = sorted(strings)
    print(f"{args.level}: unique support strings={len(ordered)}", flush=True)
    en = translate_sources(ordered, "en")
    ru = translate_sources(ordered, "ru")
    localize = make_localizer(ru, en)
    for path, doc in docs:
        migrate_lesson(doc["lessons"][0], localize)
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    audit_level(args.level)
    print(f"localized {len(paths)} {args.level} lessons", flush=True)


if __name__ == "__main__": main()
