#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'lessons' / 'a1'

# Current active, cleaned lesson map. Future sections remain planned in
# curriculum/A1_MASTER_LESSON_PLAN.md and are intentionally not generated here.
EXPECTED = {
    'a1_s01': (1, 6),
    'a1_s02': (7, 11),
    'a1_s03': (18, 22),
    'a1_s04': (23, 26),
    'a1_s05': (27, 30),
}
TYPES = {
    'multiple_choice_translation', 'reverse_translation', 'match_pairs',
    'fill_blank', 'dropdown_blank', 'sentence_order', 'sentence_builder',
    'meaning_in_context', 'natural_phrase', 'multiple_select',
    'reading_comprehension', 'dialogue_choose_reply'
}
CYR = re.compile(r'[А-Яа-яЁёІіЇїЄєҐґ]')


def flat_strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from flat_strings(y)
    elif isinstance(x, dict):
        for y in x.values():
            yield from flat_strings(y)


def token_norm(s):
    return re.findall(r'\S+', s)


def check_file(path):
    doc = json.loads(path.read_text(encoding='utf-8'))
    assert list(doc) == ['lessons'], f'{path.name}: top-level keys'
    assert len(doc['lessons']) == 1, f'{path.name}: lesson count'
    lesson = doc['lessons'][0]
    lid = lesson['id']
    m = re.fullmatch(r'a1-s(\d\d)-l(\d\d)', lid)
    assert m, f'{path.name}: bad lesson id'
    assert path.stem == lid, f'{path.name}: filename != id'
    section = lesson['sectionId']
    assert section in EXPECTED, f'{path.name}: inactive section {section}'
    n = int(m.group(2))
    lo, hi = EXPECTED[section]
    assert lo <= n <= hi, f'{path.name}: number {n}'
    assert lesson['order'] == n, f'{path.name}: order'
    all_text = [s.lower() for s in flat_strings(lesson)]
    assert not any('slovenščina' in s or 'slovenski' in s for s in all_text), f'{path.name}: Slovenian leak'
    assert len(lesson['theoryScreens']) >= 2, f'{path.name}: theory screens'

    words = lesson['words']
    assert len(words) >= 6, f'{path.name}: too few words'
    word_ids = [w['id'] for w in words]
    assert len(word_ids) == len(set(word_ids)), f'{path.name}: duplicate word ids'
    assert all(not CYR.search(w['sk']) for w in words), f'{path.name}: Cyrillic in sk'
    screen_ids = [x['wordId'] for x in lesson['wordsScreen']['items']]
    assert screen_ids == word_ids, f'{path.name}: wordsScreen mismatch'

    exercises = lesson['exercises']
    assert len(exercises) == lesson['startScreen']['exercisesCount'], f'{path.name}: exercise count mismatch'
    assert len(exercises) >= 12, f'{path.name}: too few exercises'
    assert [e['order'] for e in exercises] == list(range(1, len(exercises) + 1)), f'{path.name}: exercise order'
    word_set = set(word_ids)

    for ex in exercises:
        assert ex['lessonId'] == lid, f'{path.name}: foreign lessonId'
        assert ex['type'] in TYPES, f'{path.name}: unsupported type {ex["type"]}'
        assert set(ex.get('wordIds', [])) <= word_set, f'{path.name}: foreign wordId'
        typ = ex['type']
        if typ in ('multiple_choice_translation', 'reverse_translation', 'fill_blank'):
            assert ex['correctAnswer'] in ex['options'], f'{path.name}: answer/options mismatch'
        elif typ == 'match_pairs':
            assert len(ex['options']) == 2 * len(ex['correctAnswer']), f'{path.name}: match shape'
        elif typ == 'dropdown_blank':
            blanks = [x for x in ex['sentenceParts'] if isinstance(x, dict) and x.get('blankId')]
            assert len(blanks) == 1, f'{path.name}: dropdown blank count'
            assert ex['correctAnswer'] == blanks[0]['correct'], f'{path.name}: dropdown answer'
            assert ex['correctAnswer'] in blanks[0]['options'], f'{path.name}: dropdown options'
        elif typ == 'sentence_order':
            assert token_norm(' '.join(ex['tokens'])) == token_norm(' '.join(ex['correctOrder'])), f'{path.name}: sentence_order'
        elif typ == 'sentence_builder':
            assert token_norm(' '.join(ex['tokens'])) == token_norm(ex['correctSentence']), f'{path.name}: sentence_builder'
        elif typ in ('meaning_in_context', 'natural_phrase', 'dialogue_choose_reply'):
            assert sum(1 for o in ex['options'] if o.get('correct')) == 1, f'{path.name}: correct flag count'
        elif typ == 'multiple_select':
            assert sum(1 for o in ex['options'] if o.get('correct')) >= 2, f'{path.name}: multiple_select positives'
            assert sum(1 for o in ex['options'] if not o.get('correct')) >= 1, f'{path.name}: multiple_select distractors'
        elif typ == 'reading_comprehension':
            for q in ex['questions']:
                assert sum(1 for o in q['options'] if o.get('correct')) == 1, f'{path.name}: reading answer count'

    final = lesson['finalSituation']
    assert final.get('screenType') == 'final_life_situation', f'{path.name}: finalSituation type'
    assert final['correctAnswer'] in [str(i) for i in range(1, len(final['options']) + 1)], f'{path.name}: final answer'
    result = lesson['resultScreen']
    assert result.get('screenType') == 'lesson_result', f'{path.name}: resultScreen type'
    return lesson


def main():
    lessons = []
    for section, (lo, hi) in EXPECTED.items():
        for n in range(lo, hi + 1):
            path = D / f'a1-s{section[-2:]}-l{n:02d}.json'
            assert path.exists(), f'Missing {path.name}'
            lessons.append(check_file(path))

    active_ids = {l['id'] for l in lessons}
    for path in D.glob('a1-s*-l*.json'):
        assert path.stem in active_ids, f'Unexpected lesson file: {path.name}'

    lessons.sort(key=lambda x: (int(x['sectionId'][-2:]), x['order']))
    for current, nxt in zip(lessons, lessons[1:]):
        assert current['resultScreen']['nextLesson'] == nxt['title'], f'{current["id"]}: bad nextLesson'
    assert lessons[-1]['resultScreen']['nextLesson'] is None, 'last active lesson nextLesson must be null'

    print(f'QA PASS: {len(lessons)} active lessons across Sections 01–05.')


if __name__ == '__main__':
    main()
