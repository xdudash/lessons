#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'lessons'/'a1'
EXPECTED={
'a1_s06':(31,37),'a1_s07':(38,43),'a1_s08':(44,50),'a1_s09':(51,56),
'a1_s10':(57,62),'a1_s11':(63,67),'a1_s12':(68,72),'a1_s13':(73,76),'a1_s14':(77,81)}
TYPES={'multiple_choice_translation','reverse_translation','match_pairs','fill_blank','dropdown_blank','sentence_order','sentence_builder','meaning_in_context','natural_phrase','multiple_select','reading_comprehension','dialogue_choose_reply'}
CYR=re.compile(r'[А-Яа-яЁёІіЇїЄєҐґ]')


def flat_strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for y in x: yield from flat_strings(y)
    elif isinstance(x,dict):
        for y in x.values(): yield from flat_strings(y)


def token_norm(s): return re.findall(r'\S+',s)


def check_file(p):
    doc=json.loads(p.read_text(encoding='utf-8'))
    assert list(doc)==['lessons'], f'{p.name}: top-level keys'
    assert len(doc['lessons'])==1, f'{p.name}: lesson count'
    l=doc['lessons'][0]; lid=l['id']; m=re.fullmatch(r'a1-s(\d\d)-l(\d\d)',lid); assert m, f'{p.name}: bad id'
    assert p.stem==lid, f'{p.name}: filename != id'
    sec=l['sectionId']; assert sec in EXPECTED, f'{p.name}: unexpected section {sec}'
    n=int(m.group(2)); lo,hi=EXPECTED[sec]; assert lo<=n<=hi, f'{p.name}: number {n}'
    assert l['order']==n, f'{p.name}: order'
    assert not any('slovenščina' in s.lower() or 'slovenski' in s.lower() for s in flat_strings(l)), f'{p.name}: Slovenian leak'
    assert len(l['theoryScreens'])>=2, f'{p.name}: theory screens'
    words=l['words']; assert len(words)==12, f'{p.name}: words={len(words)}'
    ids=[w['id'] for w in words]; assert len(ids)==len(set(ids))==12, f'{p.name}: duplicate word ids'
    assert all(not CYR.search(w['sk']) for w in words), f'{p.name}: Cyrillic in sk word'
    wi=l['wordsScreen']['items']; assert [x['wordId'] for x in wi]==ids, f'{p.name}: wordsScreen mismatch'
    ex=l['exercises']; assert len(ex)==l['startScreen']['exercisesCount']==12, f'{p.name}: exercise count'
    assert [e['order'] for e in ex]==list(range(1,13)), f'{p.name}: exercise order'
    widset=set(ids)
    for e in ex:
        assert e['lessonId']==lid, f'{p.name}: foreign lessonId'
        assert e['type'] in TYPES, f'{p.name}: unsupported type {e["type"]}'
        assert set(e.get('wordIds',[]))<=widset, f'{p.name}: foreign wordId'
        typ=e['type']
        if typ in ('multiple_choice_translation','reverse_translation','fill_blank'):
            assert e['correctAnswer'] in e['options'], f'{p.name}: answer not in options {typ}'
        elif typ=='match_pairs':
            assert len(e['options'])==2*len(e['correctAnswer']), f'{p.name}: match shape'
        elif typ=='dropdown_blank':
            blanks=[x for x in e['sentenceParts'] if isinstance(x,dict) and x.get('blankId')]
            assert len(blanks)==1 and e['correctAnswer']==blanks[0]['correct'] and e['correctAnswer'] in blanks[0]['options'], f'{p.name}: dropdown'
        elif typ=='sentence_order':
            assert token_norm(' '.join(e['tokens']))==token_norm(' '.join(e['correctOrder'])), f'{p.name}: sentence_order'
        elif typ=='sentence_builder':
            assert token_norm(' '.join(e['tokens']))==token_norm(e['correctSentence']), f'{p.name}: sentence_builder'
        elif typ in ('meaning_in_context','natural_phrase','dialogue_choose_reply'):
            opts=e['options']; assert sum(1 for o in opts if o.get('correct'))==1, f'{p.name}: {typ} correct count'
        elif typ=='multiple_select':
            opts=e['options']; assert sum(1 for o in opts if o.get('correct'))>=2 and sum(1 for o in opts if not o.get('correct'))>=1, f'{p.name}: multiple_select'
        elif typ=='reading_comprehension':
            for q in e['questions']: assert sum(1 for o in q['options'] if o.get('correct'))==1, f'{p.name}: reading answer count'
    fs=l['finalSituation']; assert fs.get('screenType')=='final_life_situation', f'{p.name}: final screen'
    assert fs['correctAnswer'] in [str(i) for i in range(1,len(fs['options'])+1)], f'{p.name}: final answer'
    rs=l['resultScreen']; assert rs.get('screenType')=='lesson_result', f'{p.name}: result screen'
    assert isinstance(l['startScreen']['newWords'],list) and len(l['startScreen']['newWords'])==12, f'{p.name}: newWords'
    return l


def main():
    lessons=[]
    for sec,(lo,hi) in EXPECTED.items():
        for n in range(lo,hi+1):
            p=D/f'a1-s{sec[-2:]}-l{n:02d}.json'
            assert p.exists(), f'Missing {p.name}'
            lessons.append(check_file(p))
    assert not any((D/f'a1-s03-l{n:02d}.json').exists() for n in range(12,18)), 'legacy numerical files still present'
    lessons.sort(key=lambda x:x['order'])
    for i,l in enumerate(lessons[:-1]):
        assert l['resultScreen']['nextLesson']==lessons[i+1]['title'], f'{l["id"]}: bad nextLesson'
    assert lessons[-1]['resultScreen']['nextLesson'] is None, 'last nextLesson must be null'
    print(f'QA PASS: {len(lessons)} lessons, 9 sections, structural/reference checks passed.')

if __name__=='__main__': main()
