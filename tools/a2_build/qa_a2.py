from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path
from typing import Any
from .ownership import parse_a2_plan

CYR = re.compile(r'[А-Яа-яЁёІіЇїЄєҐґ]')
RUS = re.compile(r'\b(что|будет|нужно|почему|когда|где|выберите|следующий|завершен)\b', re.I)
CHOICE_ONE={'single_choice','dialogue_choose_reply','meaning_in_context','natural_phrase','real_message','real_schedule','real_document'}


def flat_strings(x:Any):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for y in x: yield from flat_strings(y)
    elif isinstance(x,dict):
        for y in x.values(): yield from flat_strings(y)

def token_norm(s:str): return re.findall(r"[\wÀ-ž’'-]+|[,.!?;:]", s, flags=re.UNICODE)

def label(o):
    if isinstance(o,str): return o.strip()
    if not isinstance(o,dict): return repr(o)
    v=o.get('sk',o.get('text',''))
    if isinstance(v,dict): v=v.get('uk') or v.get('sk') or repr(v)
    return str(v).strip()

def check_file(path:Path, expected_id:str, expected_next:str|None)->list[str]:
    E=[]
    def err(m): E.append(f'{path.name}: {m}')
    try: doc=json.loads(path.read_text(encoding='utf-8'))
    except Exception as e: return [f'{path.name}: JSON parse: {e}']
    if list(doc)!=['lessons'] or len(doc.get('lessons',[]))!=1: return [f'{path.name}: root must be exactly lessons[1]']
    l=doc['lessons'][0]; lid=l.get('id')
    if lid!=expected_id: err(f'id {lid!r} != {expected_id!r}')
    if path.stem!=lid: err('filename != id')
    if l.get('level')!='A2': err('level != A2')
    m=re.fullmatch(r'a2-s(\d\d)-l(\d\d)',str(lid))
    if not m: err('bad id format')
    else:
        sec=int(m.group(1)); order=int(m.group(2))
        if l.get('sectionId')!=f'a2_s{sec:02d}': err('sectionId mismatch')
        if l.get('order')!=order: err('order mismatch')
    if l.get('isPublished') is not False: err('isPublished must remain false')
    loc=l.get('localization',{})
    if loc.get('uiLanguages')!=['uk'] or loc.get('targetLanguage')!='sk' or loc.get('fallbackUiLanguage')!='uk': err('localization mismatch')
    if len(l.get('theoryScreens',[]))!=3: err('expected exactly 3 theory screens')
    words=l.get('words',[])
    if not words: err('no words'); return E
    ids=[w.get('id') for w in words]
    if len(ids)!=len(set(ids)): err('duplicate word ids')
    for w in words:
        if CYR.search(str(w.get('sk',''))): err(f'Cyrillic in Slovak word {w.get("id")}')
        if w.get('ownership') not in {'NEW','REVIEW','TRANSFER','MASTERY'}: err(f'bad ownership {w.get("id")}')
    ws=l.get('wordsScreen',{}).get('items',[])
    if len(ws)!=len(words): err('wordsScreen length mismatch')
    byid={w['id']:w for w in words if w.get('id')}
    for x in ws:
        w=byid.get(x.get('wordId'))
        if not w: err(f'unresolved wordsScreen wordId {x.get("wordId")}'); continue
        for key in ('sk','uk','pronunciationUk','exampleSk','exampleUk','ownership'):
            if x.get(key)!=w.get(key): err(f'wordsScreen {x.get("wordId")} {key} drift')
    new_expected=[w['id'] for w in words if w.get('ownership')=='NEW']
    if l.get('startScreen',{}).get('newWords')!=new_expected: err('startScreen.newWords must equal NEW ownership ids')
    exs=l.get('exercises',[])
    if len(exs)!=14 or l.get('startScreen',{}).get('exercisesCount')!=14: err('exercise count must be 14')
    exids=[x.get('id') for x in exs]; orders=[x.get('order') for x in exs]
    if len(exids)!=len(set(exids)): err('duplicate exercise ids')
    if orders!=list(range(1,15)): err('exercise orders must be 1..14')
    wordset=set(ids)
    for x in exs:
        xid=x.get('id','?'); typ=x.get('type')
        if x.get('lessonId')!=lid: err(f'{xid} foreign lessonId')
        if not set(x.get('wordIds',[]))<=wordset: err(f'{xid} unresolved wordIds')
        opts=x.get('options')
        if isinstance(opts,list):
            labs=[label(o) for o in opts]
            if any(not z for z in labs): err(f'{xid} empty option label')
            if len(labs)!=len(set(labs)): err(f'{xid} duplicate option labels')
        if typ in CHOICE_ONE:
            if not isinstance(opts,list) or sum(isinstance(o,dict) and o.get('correct') is True for o in opts)!=1: err(f'{xid} choice correct count')
        elif typ=='multiple_select':
            if not isinstance(opts,list) or sum(o.get('correct') is True for o in opts if isinstance(o,dict))<2 or not any(o.get('correct') is False for o in opts if isinstance(o,dict)): err(f'{xid} multiple_select shape')
        elif typ=='true_false':
            if not isinstance(x.get('correctAnswer'),bool): err(f'{xid} true_false answer')
        elif typ=='true_false_list':
            sts=x.get('statements',[])
            if not sts or any(not isinstance(s.get('correct'),bool) for s in sts): err(f'{xid} true_false_list')
        elif typ=='fill_blank' or typ=='transformation':
            if not x.get('acceptedAnswers'): err(f'{xid} acceptedAnswers')
        elif typ=='dropdown_blank':
            blanks=[p for p in x.get('sentenceParts',[]) if isinstance(p,dict) and p.get('blankId')]
            if len(blanks)!=1 or blanks[0].get('correct') not in blanks[0].get('options',[]): err(f'{xid} dropdown encoding')
        elif typ=='sentence_order':
            if Counter(x.get('tokens',[]))!=Counter(x.get('correctOrder',[])): err(f'{xid} sentence_order token multiset')
        elif typ=='sentence_builder':
            if Counter(x.get('tokens',[]))!=Counter(token_norm(str(x.get('correctSentence','')))): err(f'{xid} sentence_builder token multiset')
        elif typ=='word_bank':
            bank=x.get('wordBank',[])
            if not x.get('items') or any(i.get('correct') not in bank for i in x.get('items',[]) if isinstance(i,dict)): err(f'{xid} word_bank encoding')
        elif typ in {'matching','collocation'}:
            pairs=x.get('pairs',[])
            if not pairs or len({(p.get('left'),p.get('right')) for p in pairs})!=len(pairs): err(f'{xid} pairs encoding')
        elif typ=='dialogue_order':
            lines=x.get('lines',[]); corr=x.get('correctOrder',[])
            if not lines or set(corr)!={z.get('id') for z in lines}: err(f'{xid} dialogue_order')
        elif typ=='reading_comprehension':
            qs=x.get('questions',[])
            if not qs: err(f'{xid} reading questions')
            for q in qs:
                qo=q.get('options',[])
                if sum(o.get('correct') is True for o in qo if isinstance(o,dict))!=1: err(f'{xid} reading correct count')
    final=l.get('finalSituation',{})
    if final.get('type')!='interactive_scenario' or len(final.get('steps',[]))!=3: err('finalSituation must be 3-step interactive_scenario')
    examples={(w.get('exampleUk'),w.get('exampleSk')) for w in words}
    for st in final.get('steps',[]):
        opts=st.get('options',[]); labs=[label(o) for o in opts]
        if len(labs)!=len(set(labs)): err(f'final {st.get("id")} duplicate labels')
        corr=[o for o in opts if isinstance(o,dict) and o.get('correct') is True]
        if len(corr)!=1: err(f'final {st.get("id")} correct count'); continue
        prompt=st.get('prompt',{}); ptxt=prompt.get('uk','') if isinstance(prompt,dict) else str(prompt)
        if not any(uk and uk in ptxt and corr[0].get('sk')==sk for uk,sk in examples): err(f'final {st.get("id")} prompt/answer intent mismatch')
    res=l.get('resultScreen',{})
    nxt=res.get('nextLesson')
    if expected_next is None:
        if 'nextLesson' in res: err('terminal lesson must omit nextLesson')
    else:
        got=nxt.get('id') if isinstance(nxt,dict) else nxt
        if got!=expected_next: err(f'nextLesson {got!r} != {expected_next!r}')
    # Russian-only UI leakage guard.
    for s in flat_strings(l):
        if RUS.search(s): err(f'Russian UI leak: {s[:80]!r}'); break
    return E


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory'); ap.add_argument('--plan',default='A2/LESSON_PLAN.md'); ap.add_argument('--from',dest='lo',type=int,default=1); ap.add_argument('--to',dest='hi',type=int,default=90); ns=ap.parse_args()
    plan=parse_a2_plan(Path(ns.plan)); ids=[x.lesson_id for x in plan]; next_map={ids[i]:ids[i+1] for i in range(89)}
    errors=[]; checked=0
    for x in plan:
        if ns.lo<=x.order<=ns.hi:
            p=Path(ns.directory)/f'{x.lesson_id}.json'
            if not p.exists(): errors.append(f'{p.name}: missing'); continue
            errors += check_file(p,x.lesson_id,next_map.get(x.lesson_id)); checked+=1
    if errors:
        print(f'QA FAILED: {len(errors)} issue(s) across {checked} files.')
        for e in errors: print('-',e)
        raise SystemExit(1)
    print(f'QA PASSED: {checked} A2 lesson files ({ns.lo}-{ns.hi}). Adversarial + curriculum-shape checks passed.')
if __name__=='__main__': main()
