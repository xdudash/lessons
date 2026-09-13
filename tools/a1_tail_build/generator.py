import json, re, unicodedata
from pathlib import Path
from datetime import datetime, timezone, timedelta

OUT=Path('/tmp/slovakgo-build/lessons/a1')
NOW='2026-09-13T18:35:00+02:00'

def loc(sk=None, uk=None):
    d={}
    if sk is not None: d['sk']=sk
    if uk is not None: d['uk']=uk
    return d

def pron(sk):
    # Ukrainian-friendly approximation, intentionally simple and readable.
    s=sk.lower()
    reps=[('dž','дж'),('ch','х'),('dz','дз'),('ia','іа'),('ie','іє'),('iu','іу'),('ô','уо'),('ľ','ль'),('ĺ','ль'),('ň','нь'),('ď','дь'),('ť','ть'),('č','ч'),('š','ш'),('ž','ж'),('á','аа'),('é','ее'),('í','іі'),('ó','оо'),('ú','уу'),('ý','ии'),('ä','е'),('c','ц'),('j','й'),('y','и'),('q','к'),('w','в'),('x','кс')]
    for a,b in reps: s=s.replace(a,b)
    trans=str.maketrans({'a':'а','b':'б','d':'д','e':'е','f':'ф','g':'ґ','h':'г','i':'і','k':'к','l':'л','m':'м','n':'н','o':'о','p':'п','r':'р','s':'с','t':'т','u':'у','v':'в','z':'з'})
    return s.translate(trans)

def tokenize_sentence(s):
    # Keep punctuation as own token for deterministic sentence builder.
    return re.findall(r"[\wÀ-ž’'-]+|[,.!?;:]", s, flags=re.UNICODE)

def mkword(lid, idx, sk, uk, ex_sk, ex_uk, topic, tags=None, pos='phrase'):
    return {
        'id': f'{lid}-w{idx:02d}', 'sk': sk, 'uk': uk, 'pronunciationUk': pron(sk),
        'exampleSk': ex_sk, 'exampleUk': ex_uk, 'level':'A1','topic':topic,
        'tags': tags or [topic.lower().replace(' ','_')], 'partOfSpeech': pos,
    }

def opt(i, text, correct=False, sk=False):
    return {'id': chr(97+i), 'correct':correct, ('sk' if sk else 'text'):text}

def safe_distractors(words, idx, n=2):
    vals=[]
    for j in range(1,len(words)+1):
        w=words[(idx+j)%len(words)]
        if w['uk'] != words[idx]['uk'] and w['uk'] not in vals:
            vals.append(w['uk'])
        if len(vals)>=n: break
    while len(vals)<n: vals.append('інше значення')
    return vals

def choice_ex(lid, order, words, idx, question=None, typ='single_choice'):
    w=words[idx]
    ds=safe_distractors(words, idx)
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':typ,'order':order,'skill':['vocabulary'],
            'question':question or f'Що означає «{w["sk"]}»?','difficulty':'easy','button':'Далі','wordIds':[w['id']],
            'options':[opt(0,w['uk'],True),opt(1,ds[0]),opt(2,ds[1])],
            'explanation':{'uk':f'{w["sk"]} — «{w["uk"]}».'}}

def matching_ex(lid, order, words, inds):
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'matching','order':order,'skill':['vocabulary','reading'],
            'question':'З’єднай слова або фрази з точними значеннями.','difficulty':'easy','button':'Далі',
            'wordIds':[words[i]['id'] for i in inds],
            'pairs':[{'left':words[i]['sk'],'right':words[i]['uk']} for i in inds]}

def tf_ex(lid, order, words, idx, truth=True):
    w=words[idx]
    shown=w['uk'] if truth else safe_distractors(words,idx,1)[0]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'true_false','order':order,'skill':['vocabulary'],
            'question':f'Правда чи ні? «{w["sk"]}» означає «{shown}».','difficulty':'easy','button':'Далі','wordIds':[w['id']],
            'statement':f'{w["sk"]} = {shown}','correctAnswer':truth,
            'explanation':{'uk':f'Правильне значення: {w["uk"]}.'}}

def fill_ex(lid, order, words, idx):
    w=words[idx]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'fill_blank','order':order,'skill':['writing'],
            'question':f'Впиши словацькою: «{w["uk"]}».','difficulty':'medium','button':'Далі','wordIds':[w['id']],
            'sentence':'______','acceptedAnswers':[w['sk']], 'hint':{'uk':f'Початок: {w["sk"][:1]}…'},
            'explanation':{'uk':f'Правильно: {w["sk"]}.'}}

def sentence_order_ex(lid, order, words, idx):
    w=words[idx]; toks=tokenize_sentence(w['exampleSk']); scrambled=list(reversed(toks))
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'sentence_order','order':order,'skill':['writing'],
            'question':'Склади природне речення з поданих слів.','difficulty':'medium','button':'Далі','wordIds':[w['id']],
            'tokens':scrambled,'correctOrder':toks,'context':{'uk':w['exampleUk']},
            'explanation':{'uk':w['exampleSk']}}

def sentence_builder_ex(lid, order, words, idx):
    w=words[idx]; toks=tokenize_sentence(w['exampleSk']); scrambled=toks[1:]+toks[:1] if len(toks)>2 else list(reversed(toks))
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'sentence_builder','order':order,'skill':['writing'],
            'question':'Склади словацьку фразу за українським змістом.','difficulty':'medium','button':'Далі','wordIds':[w['id']],
            'tokens':scrambled,'correctSentence':w['exampleSk'],'context':{'uk':w['exampleUk']},
            'explanation':{'uk':w['exampleSk']}}

def multi_ex(lid, order, words, inds, wrong_text):
    opts=[{'id':chr(97+k),'correct':True,'sk':words[i]['sk']} for k,i in enumerate(inds)]
    opts.append({'id':chr(97+len(opts)),'correct':False,'sk':wrong_text})
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'multiple_select','order':order,'skill':['vocabulary'],
            'question':'Обери всі варіанти, які належать до теми цього уроку.','difficulty':'medium','button':'Далі',
            'wordIds':[words[i]['id'] for i in inds], 'options':opts}

def dropdown_ex(lid, order, words, idx, before='', after='.'):
    w=words[idx]
    ds=[words[(idx+1)%len(words)]['sk'],words[(idx+2)%len(words)]['sk']]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'dropdown_blank','order':order,'skill':['writing'],
            'question':f'Обери точну фразу для значення «{w["uk"]}».','difficulty':'medium','button':'Далі','wordIds':[w['id']],
            'sentenceParts':[{'text':before},{'blankId':'b1','options':[w['sk']]+ds,'correct':w['sk']},{'text':after}],
            'explanation':{'uk':f'Потрібний варіант: {w["sk"]}.'}}

def natural_ex(lid, order, words, idx, situation, wrongs=None):
    w=words[idx]
    # natural_phrase should test a usable utterance, not a bare vocabulary label.
    correct=w['exampleSk']
    wrongs=wrongs or [words[(idx+1)%len(words)]['exampleSk'], words[(idx+2)%len(words)]['exampleSk']]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'natural_phrase','order':order,'skill':['real_life'],
            'question':'Що тут сказати найприродніше?','difficulty':'medium','button':'Далі','wordIds':[w['id']],
            'situation':{'uk':f'Скажи словацькою природну фразу зі змістом: «{w["exampleUk"]}».'},
            'options':[{'id':'a','correct':True,'sk':correct},{'id':'b','correct':False,'sk':wrongs[0]},{'id':'c','correct':False,'sk':wrongs[1]}],
            'explanation':{'uk':f'У цій ситуації доречно: {correct}'}}

def dialogue_ex(lid, order, correct, wrongs, prompt, wordids):
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'dialogue_choose_reply','order':order,'skill':['dialogue','real_life'],
            'question':prompt,'difficulty':'medium','button':'Далі','wordIds':wordids,
            'options':[{'id':'a','correct':True,'sk':correct},{'id':'b','correct':False,'sk':wrongs[0]},{'id':'c','correct':False,'sk':wrongs[1]}],
            'explanation':{'uk':f'Найприродніша відповідь: {correct}'}}

def tflist_ex(lid, order, words, inds):
    sts=[]
    for k,i in enumerate(inds):
        w=words[i]; truth=(k%2==0); shown=w['uk'] if truth else safe_distractors(words,i,1)[0]
        sts.append({'sk':f'{w["sk"]} = {shown}','correct':truth})
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'true_false_list','order':order,'skill':['review'],
            'question':'Перевір значення кількох одиниць.','difficulty':'hard','button':'Далі','wordIds':[words[i]['id'] for i in inds],
            'text':{'uk':'Познач кожне твердження як правдиве або хибне.'},'statements':sts}

def read_ex(lid, order, words, text_sk, q, correct, wrongs, wordids):
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'reading_comprehension','order':order,'skill':['reading'],
            'question':'Прочитай короткий текст і дай відповідь.','difficulty':'hard','button':'Далі','wordIds':wordids,
            'text':text_sk,'questions':[{'prompt':q,'options':[{'id':'a','correct':True,'sk':correct},{'id':'b','correct':False,'sk':wrongs[0]},{'id':'c','correct':False,'sk':wrongs[1]}]}]}

def category_ex(lid, order, words, categories, items):
    # items: [(word_idx, category_id)]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'drag_to_category','order':order,'skill':['vocabulary'],
            'question':'Розподіли слова за категоріями.','difficulty':'medium','button':'Далі','wordIds':[words[i]['id'] for i,_ in items],
            'categories':[{'id':cid,'label':label} for cid,label in categories],
            'items':[{'sk':words[i]['sk'],'category':cat} for i,cat in items]}

def wordbank_ex(lid, order, words, pairs, extra=None, correct_overrides=None):
    # pairs: [(sentence with ______, word_idx)]. Overrides allow required inflected forms.
    correct_overrides=correct_overrides or {}
    vals=[correct_overrides.get(i, words[i]['sk']) for _,i in pairs]
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'word_bank','order':order,'skill':['writing'],
            'question':'Заповни пропуски словами з банку.','difficulty':'medium','button':'Далі','wordIds':[words[i]['id'] for _,i in pairs],
            'items':[{'sentence':sent,'correct':val} for (sent,_),val in zip(pairs,vals)],
            'wordBank':vals, 'extraWords':extra or []}

def dialogue_order_ex(lid, order, lines, correctOrder, wordids):
    return {'id':f'{lid}-e{order:02d}','lessonId':lid,'type':'dialogue_order','order':order,'skill':['dialogue'],
            'question':'Розташуй репліки так, щоб вийшов природний діалог.','difficulty':'hard','button':'Далі','wordIds':wordids,
            'lines':[{'id':x[0],'speaker':x[1],'sk':x[2]} for x in lines], 'correctOrder':correctOrder}

def make_exercises(spec, words):
    lid=spec['id']; v=spec.get('variant',0)%5
    ex=[]; o=1
    funcs = {
      0:['choice','match','tf','fill','drop','multi','order','build','dialogue','natural','tflist','read'],
      1:['match','choice','fill','build','tf','dialogue','multi','drop','read','natural','order','tflist'],
      2:['choice','category','match','fill','order','dialogue','drop','natural','build','tf','read','tflist'],
      3:['match','choice','wordbank','tf','fill','dialogue','order','multi','natural','drop','read','tflist'],
      4:['choice','match','dialogue_order','fill','tf','build','drop','multi','dialogue','natural','read','tflist'],
    }[v]
    for kind in funcs:
        if kind=='choice': x=choice_ex(lid,o,words,(o+v)%len(words))
        elif kind=='match': x=matching_ex(lid,o,words,[0,1,2,3])
        elif kind=='tf': x=tf_ex(lid,o,words,4,truth=(v%2==0))
        elif kind=='fill': x=fill_ex(lid,o,words,5)
        elif kind=='drop': x=dropdown_ex(lid,o,words,6)
        elif kind=='multi': x=multi_ex(lid,o,words,[0,2,4],spec.get('wrong_topic','autobus'))
        elif kind=='order': x=sentence_order_ex(lid,o,words,0)
        elif kind=='build': x=sentence_builder_ex(lid,o,words,1)
        elif kind=='natural': x=natural_ex(lid,o,words,7,spec.get('situation','Тобі треба використати цю фразу в короткій побутовій ситуації.'))
        elif kind=='dialogue':
            d=spec['dialogue']; x=dialogue_ex(lid,o,d['correct'],d['wrongs'],d['prompt'],[words[i]['id'] for i in d.get('word_indices',[0])])
        elif kind=='tflist': x=tflist_ex(lid,o,words,[0,2,5])
        elif kind=='read':
            r=spec['reading']; x=read_ex(lid,o,words,r['text'],r['q'],r['correct'],r['wrongs'],[words[i]['id'] for i in r.get('word_indices',[0,1])])
        elif kind=='category':
            
            c=spec.get('categories',{'labels':[('a','Перша група'),('b','Друга група')],'items':[(0,'a'),(1,'a'),(2,'b'),(3,'b')]})
            x=category_ex(lid,o,words,c['labels'],c['items'])
        elif kind=='wordbank':
            
            pairs=spec.get('wordbank_pairs', [('______',0),('______',1)])
            x=wordbank_ex(lid,o,words,pairs,spec.get('wordbank_extra',[]),spec.get('wordbank_correct_overrides'))
        elif kind=='dialogue_order':
            lines=[('l1','A',spec['dialogue']['prompt'].replace('—','').strip()),('l2','B',spec['dialogue']['correct']),('l3','A','Ďakujem.')]
            x=dialogue_order_ex(lid,o,lines,['l1','l2','l3'],[words[i]['id'] for i in spec['dialogue'].get('word_indices',[0])])
        ex.append(x); o+=1
    return ex

def build_lesson(spec, next_id):
    lid=spec['id']; topic=spec['topic_sk']; words=[]
    for i,w in enumerate(spec['words'],1):
        words.append(mkword(lid,i,w[0],w[1],w[2],w[3],topic,w[4] if len(w)>4 else None,w[5] if len(w)>5 else 'phrase'))
    theory=[]
    for i,t in enumerate(spec['theory'],1):
        theory.append({'id':f't{i}','screenType':'theory','order':i,'title':{'uk':t['title']},'body':{'uk':t['body']},
                       'examples':[{'sk':a,'translation':{'uk':b}} for a,b in t['examples']], 'shortRule':{'uk':t['rule']},'button':'Далі'})
    ex=make_exercises(spec,words)
    fs=[]
    for i,st in enumerate(spec['final'],1):
        fs.append({'id':f'f{i}','prompt':{'uk':st['prompt']},'options':[{'sk':st['correct'],'correct':True}]+[{'sk':x,'correct':False} for x in st['wrongs']]})
    lesson={
      'id':lid,'sectionId':spec['sectionId'],'level':'A1','title':{'sk':spec['title_sk'],'uk':spec['title_uk']},
      'topic':{'sk':spec['topic_sk'],'uk':spec['topic_uk']},'description':{'sk':spec['desc_sk'],'uk':spec['desc_uk']},
      'order':spec['order'],'xpReward':100,'estimatedMinutes':spec.get('minutes',32),'isPublished':False,
      'intro':{'sk':spec['desc_sk'],'uk':spec['desc_uk']},'completionMessage':{'sk':spec.get('done_sk','Výborne. Pokračuj.'),'uk':spec.get('done_uk','Чудово. Ти готовий рухатися далі.')},
      'updatedAt':NOW,'localization':{'uiLanguages':['uk'],'targetLanguage':'sk','fallbackUiLanguage':'uk'},'assets':{'images':{},'audio':{}},
      'startScreen':{'screenType':'lesson_start','title':{'sk':spec['title_sk'],'uk':spec['title_uk']},'shortDescription':{'sk':spec['desc_sk'],'uk':spec['desc_uk']},
                     'outcomes':spec['outcomes'],'newWords':[w['id'] for w in words],'exercisesCount':len(ex),'reward':'+100 XP','estimatedMinutes':spec.get('minutes',32),'button':'Почати урок'},
      'theoryScreens':theory,
      'wordsScreen':{'screenType':'lesson_words','title':{'uk':'Цільові слова й фрази'},'description':{'uk':'Прочитай приклади й зверни увагу, як цільові слова працюють у живій фразі.'},
                     'items':[{'wordId':w['id'],'sk':w['sk'],'uk':w['uk'],'pronunciationUk':w['pronunciationUk'],'exampleSk':w['exampleSk'],'exampleUk':w['exampleUk']} for w in words], 'button':'До практики'},
      'words':words,'exercises':ex,
      'finalSituation':{'id':'final-situation','type':'interactive_scenario','title':{'uk':spec['final_title']},'description':{'uk':spec['final_desc']},
                        'steps':fs,'passRequirement':f'{len(fs)}/{len(fs)}','successMessage':{'uk':'Готово: ти застосував матеріал уроку в новій ситуації.'}},
      'resultScreen':{'screenType':'lesson_result','title':{'uk':'Урок завершено'},'subtitle':{'uk':'Тепер перенеси ці фрази у власні реальні ситуації.'},
                      'xpReward':100,'newWordsCount':len(words),'exercisesCompleted':len(ex),'nowYouKnow':spec['outcomes'],
                      'mistakesMessage':{'uk':'Повтори тільки ті місця, де відповідь ще не стала автоматичною.'},
                      'buttons':['Продовжити','Повторити урок','Тренувати помилки'],
                      'skills':[{'id':'vocabulary','label':{'uk':'лексика'},'weight':0.3},{'id':'grammar','label':{'uk':'структури'},'weight':0.3},{'id':'real_life','label':{'uk':'застосування'},'weight':0.4}]}
    }
    if next_id: lesson['resultScreen']['nextLesson']={'id':next_id}
    return {'lessons':[lesson]}

def save_specs(specs, next_map):
    OUT.mkdir(parents=True,exist_ok=True)
    for s in specs:
        doc=build_lesson(s,next_map.get(s['id']))
        p=OUT/f"{s['id']}.json"
        p.write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
