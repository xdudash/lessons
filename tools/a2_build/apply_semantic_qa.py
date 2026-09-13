from pathlib import Path

PATH = Path('tools/a2_build/qa_a2.py')
text = PATH.read_text(encoding='utf-8')

import_anchor = 'from .ownership import parse_a2_plan\n'
semantic_import = 'from .semantic_profiles import PROFILES as SEMANTIC_PROFILES\n'
if semantic_import not in text:
    if import_anchor not in text:
        raise SystemExit('ownership import anchor not found')
    text = text.replace(import_anchor, import_anchor + semantic_import, 1)

old_order = "    m=re.fullmatch(r'a2-s(\\d\\d)-l(\\d\\d)',str(lid))\n"
new_order = "    order=None\n    m=re.fullmatch(r'a2-s(\\d\\d)-l(\\d\\d)',str(lid))\n"
if old_order not in text:
    raise SystemExit('order anchor not found')
text = text.replace(old_order, new_order, 1)

old_final = '''    final=l.get('finalSituation',{})
    if final.get('type')!='interactive_scenario' or len(final.get('steps',[]))!=3: err('finalSituation must be 3-step interactive_scenario')
    examples={(w.get('exampleUk'),w.get('exampleSk')) for w in words}
    for st in final.get('steps',[]):
        opts=st.get('options',[]); labs=[label(o) for o in opts]
        if len(labs)!=len(set(labs)): err(f'final {st.get("id")} duplicate labels')
        corr=[o for o in opts if isinstance(o,dict) and o.get('correct') is True]
        if len(corr)!=1: err(f'final {st.get("id")} correct count'); continue
        prompt=st.get('prompt',{}); ptxt=prompt.get('uk','') if isinstance(prompt,dict) else str(prompt)
        if not any(uk and uk in ptxt and corr[0].get('sk')==sk for uk,sk in examples): err(f'final {st.get("id")} prompt/answer intent mismatch')
'''
new_final = '''    final=l.get('finalSituation',{})
    steps=final.get('steps',[])
    if final.get('type')!='interactive_scenario' or len(steps)!=3:
        err('finalSituation must be 3-step interactive_scenario')
    profile=SEMANTIC_PROFILES.get(order) if order is not None else None
    if profile is None:
        err('missing semantic profile for finalSituation')
    for idx,st in enumerate(steps):
        sid=st.get('id')
        if sid!=f'f{idx+1}': err(f'final step id {sid!r} != f{idx+1!s}')
        opts=st.get('options',[]); labs=[label(o) for o in opts]
        if len(labs)!=len(set(labs)): err(f'final {sid} duplicate labels')
        corr=[o for o in opts if isinstance(o,dict) and o.get('correct') is True]
        if len(corr)!=1:
            err(f'final {sid} correct count')
            continue
        if profile is None or idx>=len(profile.models):
            continue
        prompt=st.get('prompt',{}); ptxt=prompt.get('uk','') if isinstance(prompt,dict) else str(prompt)
        expected_prompt=profile.prompts_uk[idx]
        expected_answer=profile.models[idx][0]
        if ptxt!=expected_prompt:
            err(f'final {sid} semantic final prompt mismatch')
        if corr[0].get('sk')!=expected_answer:
            err(f'final {sid} semantic final answer mismatch')
'''
if old_final not in text:
    raise SystemExit('final QA block anchor not found')
text = text.replace(old_final, new_final, 1)

PATH.write_text(text, encoding='utf-8')
