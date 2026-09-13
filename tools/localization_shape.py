from __future__ import annotations

from typing import Any

import localize_a1_a2 as base


def _localize_field(obj: dict[str, Any], key: str, localize) -> None:
    if key not in obj:
        return
    value = obj[key]
    if base.source_uk(value):
        obj[key] = localize(value)


def _translation_object(source: Any, localize) -> Any:
    if base.source_uk(source):
        return localize(source)
    return source


def safe_migrate_lesson(lesson: dict[str, Any], localize) -> None:
    """Add ru/en localization without deleting or renaming existing lesson fields."""
    loc = lesson.setdefault("localization", {})
    loc["uiLanguages"] = ["uk", "ru", "en"]
    loc["targetLanguage"] = "sk"
    loc["fallbackUiLanguage"] = "uk"

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        _localize_field(lesson, key, localize)

    start = lesson.get("startScreen")
    if isinstance(start, dict):
        for key in ("eyebrow", "title", "shortDescription", "subtitle", "goal"):
            _localize_field(start, key, localize)
        if isinstance(start.get("outcomes"), list):
            start["outcomes"] = [localize(v) if base.source_uk(v) else v for v in start["outcomes"]]

    for screen in lesson.get("theoryScreens", []) or []:
        if not isinstance(screen, dict):
            continue
        for key in ("title", "text", "body", "shortRule"):
            _localize_field(screen, key, localize)
        for example in screen.get("examples", []) or []:
            if not isinstance(example, dict):
                continue
            if base.source_uk(example.get("translation")):
                example["translation"] = localize(example["translation"])
            elif isinstance(example.get("uk"), str):
                example["translation"] = localize(example["uk"])

    words_screen = lesson.get("wordsScreen")
    if isinstance(words_screen, dict):
        for key in ("title", "description", "subtitle"):
            _localize_field(words_screen, key, localize)
        for item in words_screen.get("items", []) or []:
            if not isinstance(item, dict):
                continue
            if isinstance(item.get("uk"), str):
                item["translation"] = localize(item["uk"])
            if isinstance(item.get("exampleUk"), str):
                item["exampleTranslation"] = localize(item["exampleUk"])

    for word in lesson.get("words", []) or []:
        if not isinstance(word, dict):
            continue
        source = word.get("translation") if base.source_uk(word.get("translation")) else word.get("uk")
        if base.source_uk(source):
            word["translation"] = localize(source)
        example = word.get("example")
        if isinstance(example, dict) and base.source_uk(example.get("translation")):
            example["translation"] = localize(example["translation"])
        elif isinstance(word.get("exampleUk"), str):
            if not isinstance(example, dict):
                example = {"sk": word.get("exampleSk", "")}
                word["example"] = example
            example["translation"] = localize(word["exampleUk"])

    text_keys = (
        "instruction", "question", "prompt", "explanation", "hint", "text", "statement",
        "sentence", "displaySentence", "context", "target", "situation", "phrase", "source", "successMessage",
    )
    for exercise in lesson.get("exercises", []) or []:
        if not isinstance(exercise, dict):
            continue
        for key in text_keys:
            _localize_field(exercise, key, localize)
        for option in exercise.get("options", []) or []:
            if isinstance(option, dict):
                _localize_field(option, "text", localize)
        for pair in exercise.get("pairs", []) or []:
            if not isinstance(pair, dict):
                continue
            for side in ("left", "right"):
                value = pair.get(side)
                if base.source_uk(value):
                    pair[f"{side}Translation"] = localize(value)
        for statement in exercise.get("statements", []) or []:
            if isinstance(statement, dict):
                _localize_field(statement, "text", localize)
        for category in exercise.get("categories", []) or []:
            if isinstance(category, dict):
                _localize_field(category, "title", localize)
                _localize_field(category, "label", localize)
        document = exercise.get("document")
        if isinstance(document, dict):
            _localize_field(document, "title", localize)
            for field in document.get("fields", []) or []:
                if isinstance(field, dict):
                    _localize_field(field, "label", localize)
                    _localize_field(field, "value", localize)
        message = exercise.get("message")
        if isinstance(message, dict):
            _localize_field(message, "sender", localize)
            _localize_field(message, "body", localize)
        schedule = exercise.get("schedule")
        if isinstance(schedule, dict):
            _localize_field(schedule, "title", localize)
            for row in schedule.get("rows", []) or []:
                if isinstance(row, dict):
                    _localize_field(row, "day", localize)
                    _localize_field(row, "hours", localize)
        for question in exercise.get("questions", []) or []:
            if not isinstance(question, dict):
                continue
            _localize_field(question, "question", localize)
            _localize_field(question, "correct", localize)
            for option in question.get("options", []) or []:
                if isinstance(option, dict):
                    _localize_field(option, "text", localize)
        for item in exercise.get("items", []) or []:
            if isinstance(item, dict):
                for key in ("text", "label", "title", "question", "prompt"):
                    _localize_field(item, key, localize)

    final = lesson.get("finalSituation")
    if isinstance(final, dict):
        for key in ("title", "description", "successMessage", "scenario", "question", "translation", "explanation"):
            _localize_field(final, key, localize)
        for step in final.get("steps", []) or []:
            if not isinstance(step, dict):
                continue
            _localize_field(step, "prompt", localize)
            for option in step.get("options", []) or []:
                if isinstance(option, dict):
                    _localize_field(option, "text", localize)

    result = lesson.get("resultScreen")
    if isinstance(result, dict):
        for key in ("title", "text", "subtitle", "mistakesMessage"):
            _localize_field(result, key, localize)
        for skill in result.get("skills", []) or []:
            if isinstance(skill, dict):
                _localize_field(skill, "label", localize)
        nxt = result.get("nextLesson")
        if isinstance(nxt, dict):
            _localize_field(nxt, "title", localize)

    assets = lesson.get("assets")
    if isinstance(assets, dict):
        for image in (assets.get("images") or {}).values():
            if isinstance(image, dict):
                _localize_field(image, "alt", localize)

    base.upgrade_locale_maps(lesson, localize)
