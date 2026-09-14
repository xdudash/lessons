#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "lessons" / "a1"
CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
LANGS = {"sk", "uk", "ru", "en"}
TYPES = {
    "single_choice", "multiple_select", "matching", "fill_blank",
    "dropdown_blank", "sentence_order", "sentence_builder",
    "meaning_in_context", "natural_phrase", "reading_comprehension",
    "dialogue_choose_reply", "multiple_choice_translation",
    "reverse_translation", "match_pairs",
}

EXPECTED = {
    1: (1, 6),
    2: (7, 11),
    3: (18, 22),
    4: (23, 26),
    5: (27, 30),
    6: (31, 37),
    7: (38, 43),
    8: (44, 50),
    9: (51, 56),
    10: (57, 62),
    11: (63, 67),
    12: (68, 72),
    13: (73, 76),
    14: (77, 81),
}


def flat(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from flat(y)
    elif isinstance(x, dict):
        for y in x.values():
            yield from flat(y)


def assert_langs(obj, path):
    assert isinstance(obj, dict), f"{path}: not object"
    missing = LANGS - set(obj)
    assert not missing, f"{path}: missing languages {sorted(missing)}"
    for lang in LANGS:
        assert isinstance(obj[lang], str) and obj[lang].strip(), f"{path}: empty {lang}"


def assert_learner_langs(obj, path):
    assert isinstance(obj, dict), f"{path}: not object"
    for lang in ("uk", "ru", "en"):
        assert isinstance(obj.get(lang), str) and obj[lang].strip(), f"{path}: empty {lang}"


def check(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert list(doc) == ["lessons"], f"{path.name}: top-level keys"
    assert len(doc["lessons"]) == 1, f"{path.name}: lesson count"
    lesson = doc["lessons"][0]

    lid = lesson["id"]
    m = re.fullmatch(r"a1-s(\d{2})-l(\d{2})", lid)
    assert m, f"{path.name}: bad id {lid}"
    section = int(m.group(1))
    order = int(m.group(2))
    assert section in EXPECTED, f"{path.name}: inactive section {section}"
    lo, hi = EXPECTED[section]
    assert lo <= order <= hi, f"{path.name}: lesson number {order} outside section range"
    assert path.stem == lid, f"{path.name}: filename != id"
    assert lesson["sectionId"] == f"a1_s{section:02d}", f"{path.name}: sectionId"
    assert lesson["level"] == "A1", f"{path.name}: level"
    assert lesson["order"] == order, f"{path.name}: order"
    assert lesson["localization"] == {
        "uiLanguages": ["uk", "ru", "en"],
        "targetLanguage": "sk",
        "fallbackUiLanguage": "uk",
    }, f"{path.name}: localization"

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        assert_langs(lesson[key], f"{path.name}:{key}")
    assert_learner_langs(lesson["startScreen"]["title"], f"{path.name}:start.title")
    assert_learner_langs(lesson["startScreen"]["shortDescription"], f"{path.name}:start.shortDescription")

    assert len(lesson["theoryScreens"]) >= 2, f"{path.name}: theory screens"

    words = lesson["words"]
    assert len(words) >= 6, f"{path.name}: words"
    ids = [w["id"] for w in words]
    assert len(ids) == len(set(ids)), f"{path.name}: duplicate words"
    assert [x["wordId"] for x in lesson["wordsScreen"]["items"]] == ids, f"{path.name}: wordsScreen mismatch"
    for word in words:
        for key in ("id", "sk", "uk", "pronunciationUk", "exampleSk", "exampleUk"):
            assert isinstance(word.get(key), str) and word[key].strip(), f"{path.name}:{word.get('id')} missing {key}"
        assert not CYR.search(word["sk"]), f"{path.name}: Cyrillic in Slovak word"
        assert word["level"] == "A1", f"{path.name}: word level"

    exercises = lesson["exercises"]
    assert len(exercises) >= 12, f"{path.name}: too few exercises"
    assert lesson["startScreen"]["exercisesCount"] == len(exercises), f"{path.name}: exercise count"
    assert [e["order"] for e in exercises] == list(range(1, len(exercises) + 1)), f"{path.name}: exercise order"
    word_set = set(ids)
    for ex in exercises:
        assert ex["lessonId"] == lid, f"{path.name}: foreign lesson"
        assert ex["type"] in TYPES, f"{path.name}: bad type {ex['type']}"
        assert set(ex.get("wordIds", [])) <= word_set, f"{path.name}: foreign wordId"
        if isinstance(ex.get("questionLocalized"), dict):
            assert_learner_langs(ex["questionLocalized"], f"{path.name}:{ex['id']}:questionLocalized")
        if ex["type"] in {"single_choice", "natural_phrase", "dialogue_choose_reply", "meaning_in_context"} and isinstance(ex.get("options"), list):
            assert sum(1 for o in ex["options"] if isinstance(o, dict) and o.get("correct")) == 1, f"{path.name}:{ex['id']}: correct count"
        if ex["type"] in {"reverse_translation", "multiple_choice_translation"}:
            assert ex["correctAnswer"] in ex["options"], f"{path.name}:{ex['id']}: answer not in options"
        if ex["type"] == "multiple_select":
            assert sum(1 for o in ex["options"] if o.get("correct")) >= 2, f"{path.name}:{ex['id']}: multiple_select positives"
            assert sum(1 for o in ex["options"] if not o.get("correct")) >= 1, f"{path.name}:{ex['id']}: multiple_select distractors"

    final = lesson["finalSituation"]
    assert final["type"] == "interactive_scenario", f"{path.name}: final type"
    assert_learner_langs(final["title"], f"{path.name}:final.title")
    assert_learner_langs(final["description"], f"{path.name}:final.description")
    assert len(final["steps"]) == 3, f"{path.name}: final steps"
    for step in final["steps"]:
        assert sum(1 for o in step["options"] if o.get("correct")) == 1, f"{path.name}:{step['id']}: final correct count"

    all_text = [s.lower() for s in flat(lesson)]
    assert not any("slovenščina" in s or "slovenski" in s for s in all_text), f"{path.name}: Slovenian leak"
    return lesson


def main() -> int:
    lessons = []
    for section, (lo, hi) in EXPECTED.items():
        for order in range(lo, hi + 1):
            path = D / f"a1-s{section:02d}-l{order:02d}.json"
            assert path.exists(), f"Missing {path.name}"
            lessons.append(check(path))

    active_ids = {lesson["id"] for lesson in lessons}
    assert len(active_ids) == 75, f"expected 75 active lessons, found {len(active_ids)}"
    for path in D.glob("a1-s*-l*.json"):
        assert path.stem in active_ids, f"Unexpected lesson file: {path.name}"

    lessons.sort(key=lambda x: x["order"])
    assert [lesson["id"] for lesson in lessons] == [
        f"a1-s{section:02d}-l{order:02d}"
        for section, (lo, hi) in EXPECTED.items()
        for order in range(lo, hi + 1)
    ], "active lesson inventory/order mismatch"

    for current, nxt in zip(lessons, lessons[1:]):
        assert current["resultScreen"]["nextLesson"] == {"id": nxt["id"]}, f"{current['id']}: bad nextLesson"
    assert lessons[-1]["resultScreen"]["nextLesson"] is None, "terminal nextLesson must be null"

    print("QA PASS: 75 active A1 lessons across Sections 01–14.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
