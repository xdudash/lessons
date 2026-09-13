from __future__ import annotations

import gc
import json
import re
from pathlib import Path
from typing import Any

CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
LANG_KEYS = {"sk", "uk", "ru", "en"}


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
    return (
        isinstance(value, dict)
        and "uk" in value
        and isinstance(value.get("uk"), str)
        and set(value).issubset(LANG_KEYS)
    )


def walk_sources(lesson: dict[str, Any]) -> set[str]:
    out: set[str] = set()

    def add(value: Any) -> None:
        uk = source_uk(value)
        if uk:
            out.add(uk)

    def walk_locale_maps(value: Any) -> None:
        if is_locale_map(value):
            add(value)
        if isinstance(value, dict):
            for child in value.values():
                walk_locale_maps(child)
        elif isinstance(value, list):
            for child in value:
                walk_locale_maps(child)

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
        if screen.get("exampleUk"):
            add(screen.get("exampleUk"))
        for ex in screen.get("examples", []) or []:
            add(ex.get("translation"))
            if ex.get("uk"):
                add(ex.get("uk"))

    ws = lesson.get("wordsScreen", {})
    for key in ("title", "description", "subtitle"):
        add(ws.get(key))

    for word in lesson.get("words", []) or []:
        add(word.get("translation") or word.get("uk"))
        ex = word.get("example")
        if isinstance(ex, dict):
            add(ex.get("translation"))
        else:
            add(word.get("exampleUk"))

    for ex in lesson.get("exercises", []) or []:
        for key in (
            "instruction", "question", "prompt", "explanation", "hint", "text",
            "statement", "sentence", "displaySentence", "context", "target",
            "situation", "phrase", "source", "successMessage",
        ):
            add(ex.get(key))
        for option in ex.get("options", []) or []:
            if isinstance(option, dict):
                add(option.get("text"))
        for pair in ex.get("pairs", []) or []:
            if isinstance(pair, dict):
                add(pair.get("left")); add(pair.get("right"))
        for statement in ex.get("statements", []) or []:
            if isinstance(statement, dict):
                add(statement.get("text") or statement.get("sk"))
        for category in ex.get("categories", []) or []:
            if isinstance(category, dict):
                add(category.get("title")); add(category.get("label"))
        document = ex.get("document")
        if isinstance(document, dict):
            add(document.get("title"))
            for field in document.get("fields", []) or []:
                if isinstance(field, dict):
                    add(field.get("label")); add(field.get("value"))
        message = ex.get("message")
        if isinstance(message, dict):
            add(message.get("sender")); add(message.get("body"))
        schedule = ex.get("schedule")
        if isinstance(schedule, dict):
            add(schedule.get("title"))
            for row in schedule.get("rows", []) or []:
                if isinstance(row, dict):
                    add(row.get("day")); add(row.get("hours"))
        for q in ex.get("questions", []) or []:
            if isinstance(q, dict):
                add(q.get("question")); add(q.get("correct"))
                for option in q.get("options", []) or []:
                    if isinstance(option, dict):
                        add(option.get("text"))
        for item in ex.get("items", []) or []:
            if isinstance(item, dict):
                for key in ("text", "label", "title", "question", "prompt"):
                    add(item.get(key))

    final = lesson.get("finalSituation", {})
    if isinstance(final, dict) and final.get("type") == "interactive_scenario":
        for key in ("title", "description", "successMessage"):
            add(final.get(key))
        for step in final.get("steps", []) or []:
            if not isinstance(step, dict):
                continue
            add(step.get("prompt"))
            for option in step.get("options", []) or []:
                if isinstance(option, dict):
                    add(option.get("text"))

    result = lesson.get("resultScreen", {})
    for key in ("title", "text", "subtitle"):
        add(result.get(key))
    for skill in result.get("skills", []) or []:
        if isinstance(skill, dict):
            add(skill.get("label"))
    nxt = result.get("nextLesson")
    if isinstance(nxt, dict):
        add(nxt.get("title"))

    assets = lesson.get("assets", {})
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict):
                add(image.get("alt"))

    # Catch any already-localized UI map nested in a less common structure.
    walk_locale_maps(lesson)
    return out


def translate_all(strings: list[str], model_name: str) -> dict[str, str]:
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    tok = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    model.eval()
    result: dict[str, str] = {}
    batch_size = 32
    with torch.inference_mode():
        for start in range(0, len(strings), batch_size):
            batch_texts = strings[start:start + batch_size]
            encoded = tok(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
            generated = model.generate(**encoded, max_new_tokens=192, num_beams=1)
            decoded = tok.batch_decode(generated, skip_special_tokens=True)
            for src, dst in zip(batch_texts, decoded):
                dst = dst.strip()
                if not dst:
                    raise RuntimeError(f"empty translation from {model_name}: {src!r}")
                result[src] = dst
            print(f"{model_name}: {min(start + batch_size, len(strings))}/{len(strings)}")
    del model, tok
    gc.collect()
    return result


def localizer(ru: dict[str, str], en: dict[str, str]):
    def localize(value: Any) -> Any:
        uk = source_uk(value)
        if not uk:
            return value
        base = dict(value) if isinstance(value, dict) else {}
        base["uk"] = uk
        base["ru"] = ru[uk]
        base["en"] = en[uk]
        return base
    return localize


def upgrade_locale_maps(value: Any, localize) -> None:
    if isinstance(value, dict):
        if is_locale_map(value):
            upgraded = localize(value)
            value.clear()
            value.update(upgraded)
        for child in list(value.values()):
            upgrade_locale_maps(child, localize)
    elif isinstance(value, list):
        for child in value:
            upgrade_locale_maps(child, localize)


def migrate_lesson(lesson: dict[str, Any], localize) -> None:
    lesson.setdefault("localization", {})["uiLanguages"] = ["uk", "ru", "en"]
    lesson["localization"]["targetLanguage"] = "sk"
    lesson["localization"]["fallbackUiLanguage"] = "uk"

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        lesson[key] = localize(lesson.get(key))

    ss = lesson.get("startScreen", {})
    for key in ("eyebrow", "title", "shortDescription", "subtitle", "goal"):
        if key in ss:
            ss[key] = localize(ss[key])
    if "outcomes" in ss:
        ss["outcomes"] = [localize(v) for v in ss.get("outcomes", [])]
    ss.pop("button", None)

    for screen in lesson.get("theoryScreens", []) or []:
        for key in ("title", "text", "body", "shortRule"):
            if key in screen:
                screen[key] = localize(screen[key])
        if screen.get("exampleUk"):
            screen.setdefault("examples", []).insert(0, {
                "sk": screen.get("exampleSk", ""),
                "translation": localize(screen["exampleUk"]),
            })
            screen.pop("exampleSk", None)
            screen.pop("exampleUk", None)
        for ex in screen.get("examples", []) or []:
            if "translation" in ex:
                ex["translation"] = localize(ex["translation"])
            elif ex.get("uk"):
                ex["translation"] = localize(ex["uk"])
                ex.pop("uk", None)
        screen.pop("button", None)

    ws = lesson.get("wordsScreen", {})
    for key in ("title", "description", "subtitle"):
        if key in ws:
            ws[key] = localize(ws[key])
    ws.pop("items", None)
    ws.pop("button", None)

    for word in lesson.get("words", []) or []:
        word["translation"] = localize(word.get("translation") or word.get("uk"))
        ex = word.get("example")
        if isinstance(ex, dict) and ex.get("sk"):
            ex["translation"] = localize(ex.get("translation") or word.get("exampleUk"))
        elif word.get("exampleSk"):
            word["example"] = {
                "sk": word["exampleSk"],
                "translation": localize(word.get("exampleUk", "")),
            }

    for ex in lesson.get("exercises", []) or []:
        for key in (
            "instruction", "question", "prompt", "explanation", "hint", "text",
            "statement", "sentence", "displaySentence", "context", "target",
            "situation", "phrase", "source", "successMessage",
        ):
            if key in ex:
                ex[key] = localize(ex[key])
        for option in ex.get("options", []) or []:
            if isinstance(option, dict) and "text" in option:
                option["text"] = localize(option["text"])
        for pair in ex.get("pairs", []) or []:
            if not isinstance(pair, dict):
                continue
            for side in ("left", "right"):
                if side in pair and source_uk(pair[side]):
                    pair[side] = localize(pair[side])
        for statement in ex.get("statements", []) or []:
            if isinstance(statement, dict):
                src = statement.get("text") or statement.get("sk")
                if source_uk(src):
                    statement["text"] = localize(src)
        for category in ex.get("categories", []) or []:
            if not isinstance(category, dict):
                continue
            for key in ("title", "label"):
                if key in category:
                    category[key] = localize(category[key])
        document = ex.get("document")
        if isinstance(document, dict):
            if "title" in document:
                document["title"] = localize(document["title"])
            for field in document.get("fields", []) or []:
                if not isinstance(field, dict):
                    continue
                for key in ("label", "value"):
                    if key in field and source_uk(field[key]):
                        field[key] = localize(field[key])
        message = ex.get("message")
        if isinstance(message, dict):
            for key in ("sender", "body"):
                if key in message:
                    message[key] = localize(message[key])
        schedule = ex.get("schedule")
        if isinstance(schedule, dict):
            if "title" in schedule:
                schedule["title"] = localize(schedule["title"])
            for row in schedule.get("rows", []) or []:
                if not isinstance(row, dict):
                    continue
                for key in ("day", "hours"):
                    if key in row and source_uk(row[key]):
                        row[key] = localize(row[key])
        for q in ex.get("questions", []) or []:
            if not isinstance(q, dict):
                continue
            if "question" in q:
                q["question"] = localize(q["question"])
            if "correct" in q and source_uk(q["correct"]):
                q["correct"] = localize(q["correct"])
            for option in q.get("options", []) or []:
                if isinstance(option, dict) and "text" in option:
                    option["text"] = localize(option["text"])
        for item in ex.get("items", []) or []:
            if not isinstance(item, dict):
                continue
            for key in ("text", "label", "title", "question", "prompt"):
                if key in item and source_uk(item[key]):
                    item[key] = localize(item[key])
        ex.pop("button", None)

    final = lesson.get("finalSituation", {})
    if isinstance(final, dict) and final.get("type") == "interactive_scenario":
        for key in ("title", "description", "successMessage"):
            if key in final:
                final[key] = localize(final[key])
        for step in final.get("steps", []) or []:
            if not isinstance(step, dict):
                continue
            if "prompt" in step:
                step["prompt"] = localize(step["prompt"])
            for option in step.get("options", []) or []:
                if isinstance(option, dict) and "text" in option:
                    option["text"] = localize(option["text"])

    result = lesson.get("resultScreen", {})
    for key in ("title", "text", "subtitle"):
        if key in result:
            result[key] = localize(result[key])
    for skill in result.get("skills", []) or []:
        if isinstance(skill, dict) and "label" in skill:
            skill["label"] = localize(skill["label"])
    nxt = result.get("nextLesson")
    if isinstance(nxt, dict) and "title" in nxt:
        nxt["title"] = localize(nxt["title"])
    result.pop("buttons", None)
    result.pop("mistakesMessage", None)
    result.pop("nowYouKnow", None)

    assets = lesson.get("assets", {})
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict) and "alt" in image:
                image["alt"] = localize(image["alt"])

    upgrade_locale_maps(lesson, localize)


def main() -> None:
    paths = [
        *sorted(Path("lessons/a1").glob("a1-s*-l*.json")),
        *sorted(Path("lessons/a2").glob("a2-s*-l*.json")),
    ]
    if len(paths) != 165:
        raise SystemExit(f"expected 165 lessons, got {len(paths)}")

    docs: list[tuple[Path, dict[str, Any]]] = []
    strings: set[str] = set()
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        lesson = doc["lessons"][0]
        docs.append((path, doc))
        strings |= walk_sources(lesson)

    ordered = sorted(strings)
    print(f"unique Ukrainian support strings: {len(ordered)}")
    en = translate_all(ordered, "Helsinki-NLP/opus-mt-uk-en")
    ru = translate_all(ordered, "Helsinki-NLP/opus-mt-uk-ru")
    localize = localizer(ru, en)

    for path, doc in docs:
        migrate_lesson(doc["lessons"][0], localize)
        path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    print(f"localized {len(paths)} lessons")


if __name__ == "__main__":
    main()
