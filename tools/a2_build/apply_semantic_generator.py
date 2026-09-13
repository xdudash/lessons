from pathlib import Path

PATH = Path('tools/a2_build/generator.py')
text = PATH.read_text(encoding='utf-8')

import_anchor = 'from .natural_examples import EXAMPLES\n'
semantic_import = 'from .semantic_profiles import PROFILES as SEMANTIC_PROFILES\n'
if semantic_import not in text:
    if import_anchor not in text:
        raise SystemExit('natural_examples import anchor not found')
    text = text.replace(import_anchor, import_anchor + semantic_import, 1)

old_theory = '''    groups=[list(range(0,min(3,len(words)))), list(range(min(3,len(words)),min(6,len(words)))), list(range(max(0,len(words)-3),len(words)))]
    # ensure every theory screen has at least one example
    groups=[g or [0] for g in groups]
    focus=SECTION_FOCUS[plan.section]
    bodies=[copy.intent_uk, focus[1], focus[2]]
    titles=[focus[0], 'Як це працює', 'Перенесення в реальну ситуацію']
    theory=[]
    for j,(title,body,inds) in enumerate(zip(titles,bodies,groups),1):
        theory.append({'id':f't{j}','screenType':'theory','order':j,'title':{'uk':title},'body':{'uk':body},'examples':[{'sk':words[i]['exampleSk'],'translation':{'uk':words[i]['exampleUk']}} for i in inds],'shortRule':{'uk':'Використовуй модель коротко й точно; спочатку зміст, потім форма.'},'button':'Далі'})
    exercises=build_exercises(lid,words,plan.order)
'''
new_theory = '''    groups=[list(range(0,min(3,len(words)))), list(range(min(3,len(words)),min(6,len(words)))), list(range(max(0,len(words)-3),len(words)))]
    # ensure every theory screen has at least one vocabulary example
    groups=[g or [0] for g in groups]
    profile=SEMANTIC_PROFILES[plan.order]
    focus=SECTION_FOCUS[plan.section]
    bodies=[copy.intent_uk, focus[1], focus[2]]
    titles=[focus[0], 'Як це працює', 'Перенесення в реальну ситуацію']
    theory=[]
    for j,(title,body,inds) in enumerate(zip(titles,bodies,groups),1):
        model_sk,model_uk=profile.models[j-1]
        examples=[{'sk':model_sk,'translation':{'uk':model_uk}}]
        examples.extend(
            {'sk':words[i]['exampleSk'],'translation':{'uk':words[i]['exampleUk']}}
            for i in inds if words[i]['exampleSk'] != model_sk
        )
        theory.append({'id':f't{j}','screenType':'theory','order':j,'title':{'uk':title},'body':{'uk':body},'examples':examples,'shortRule':{'uk':'Використовуй модель коротко й точно; спочатку зміст, потім форма.'},'button':'Далі'})
    exercises=build_exercises(lid,words,plan.order)
'''
if old_theory not in text:
    raise SystemExit('theory block anchor not found')
text = text.replace(old_theory, new_theory, 1)

old_final = '''    final_inds=[]
    for cand in [0,len(words)//2,len(words)-1]:
        if cand not in final_inds: final_inds.append(cand)
    while len(final_inds)<3: final_inds.append((final_inds[-1]+1)%len(words))
    steps=[]
    for k,i in enumerate(final_inds[:3],1):
        w=words[i]; ds=unique_other(words,i,'exampleSk')
        steps.append({'id':f'f{k}','prompt':{'uk':f'У ситуації «{copy.title_uk}» скажи: «{w["exampleUk"]}»'},'options':[{'sk':w['exampleSk'],'correct':True},{'sk':ds[0],'correct':False},{'sk':ds[1],'correct':False}]})
'''
new_final = '''    steps=[]
    model_sks=[model[0] for model in profile.models]
    if len(set(model_sks)) != 3:
        raise ValueError(f'{lid}: semantic final models must be distinct')
    for idx,(prompt,(model_sk,_model_uk)) in enumerate(zip(profile.prompts_uk,profile.models),1):
        distractors=[sk for j,sk in enumerate(model_sks) if j != idx-1]
        steps.append({'id':f'f{idx}','prompt':{'uk':prompt},'options':[{'sk':model_sk,'correct':True},{'sk':distractors[0],'correct':False},{'sk':distractors[1],'correct':False}]})
'''
if old_final not in text:
    raise SystemExit('final block anchor not found')
text = text.replace(old_final, new_final, 1)

PATH.write_text(text, encoding='utf-8')
