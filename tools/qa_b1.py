#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "lessons" / "b1"
CYR = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")
LANGS = {"sk", "uk", "ru", "en"}
TYPES = {
    "single_choice", "multiple_select", "matching", "fill_blank",
    "dropdown_blank", "sentence_order", "sentence_builder",
    "meaning_in_context", "natural_phrase", "reading_comprehension",
    "dialogue_choose_reply", "multiple_choice_translation",
    "reverse_translation", "match_pairs",
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
    m = re.fullmatch(r"b1-s(\d{2})-l(\d{2,3})", lid)
    assert m, f"{path.name}: bad id {lid}"
    section = int(m.group(1))
    order = int(m.group(2))
    assert path.stem == lid, f"{path.name}: filename != id"
    assert lesson["sectionId"] == f"b1_s{section:02d}", f"{path.name}: sectionId"
    assert lesson["level"] == "B1", f"{path.name}: level"
    assert lesson["order"] == order, f"{path.name}: order"
    assert lesson["localization"] == {"uiLanguages": ["uk", "ru", "en"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"}, f"{path.name}: localization"

    for key in ("title", "topic", "description", "intro", "completionMessage"):
        assert_langs(lesson[key], f"{path.name}:{key}")
    assert_langs(lesson["startScreen"]["title"], f"{path.name}:start.title")
    assert_learner_langs(lesson["startScreen"]["shortDescription"], f"{path.name}:start.shortDescription")

    words = lesson["words"]
    assert len(words) >= 8, f"{path.name}: words"
    ids = [w["id"] for w in words]
    assert len(ids) == len(set(ids)), f"{path.name}: duplicate words"
    assert [x["wordId"] for x in lesson["wordsScreen"]["items"]] == ids, f"{path.name}: wordsScreen mismatch"
    for word in words:
        for key in ("id", "sk", "uk", "ru", "en", "exampleSk", "exampleUk", "exampleRu", "exampleEn"):
            assert isinstance(word.get(key), str) and word[key].strip(), f"{path.name}:{word.get('id')} missing {key}"
        assert not CYR.search(word["sk"]), f"{path.name}: Cyrillic in Slovak word"
        assert word["level"] == "B1", f"{path.name}: word level"

    exercises = lesson["exercises"]
    assert len(exercises) == 12, f"{path.name}: exercises"
    assert lesson["startScreen"]["exercisesCount"] == 12, f"{path.name}: start exercise count"
    assert [e["order"] for e in exercises] == list(range(1, 13)), f"{path.name}: exercise order"
    word_set = set(ids)
    for ex in exercises:
        assert ex["lessonId"] == lid, f"{path.name}: foreign lesson"
        assert ex["type"] in TYPES, f"{path.name}: bad type {ex['type']}"
        assert set(ex.get("wordIds", [])) <= word_set, f"{path.name}: foreign wordId"
        if isinstance(ex.get("questionLocalized"), dict):
            assert_learner_langs(ex["questionLocalized"], f"{path.name}:{ex['id']}:questionLocalized")
        if "options" in ex and isinstance(ex["options"], list) and ex["type"] in {"single_choice", "natural_phrase", "dialogue_choose_reply", "meaning_in_context"}:
            assert sum(1 for o in ex["options"] if isinstance(o, dict) and o.get("correct")) == 1, f"{path.name}:{ex['id']}: correct count"
        if ex["type"] in {"reverse_translation", "multiple_choice_translation"}:
            assert ex["correctAnswer"] in ex["options"], f"{path.name}:{ex['id']}: answer not in options"

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
    for n in range(1, 101):
        matches = sorted(D.glob(f"b1-s*-l{n:02d}.json"))
        assert len(matches) == 1, f"lesson {n:02d}: expected one file, found {len(matches)}"
        lessons.append(check(matches[0]))

    ids = [l["id"] for l in lessons]
    assert len(ids) == len(set(ids)) == 100, "duplicate/missing ids"
    for current, nxt in zip(lessons, lessons[1:]):
        assert current["resultScreen"]["nextLesson"] == {"id": nxt["id"]}, f"{current['id']}: bad nextLesson"
    assert lessons[-1]["resultScreen"]["nextLesson"] is None, "terminal nextLesson must be null"
    print("QA PASS: 100 B1 lessons, all language fields and nextLesson chain verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
