from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'tools' / 'build_a1.py'
spec = importlib.util.spec_from_file_location('a1_builder', source)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

mod.LESSON_SECTIONS = [
    ('a1_s06', 31), ('a1_s07', 38), ('a1_s08', 44),
    ('a1_s09', 51), ('a1_s10', 57), ('a1_s11', 63),
    ('a1_s12', 68), ('a1_s13', 73), ('a1_s14', 77),
]

def mk_lesson(section_id, lesson_no, title, theme, pool, all_lessons, idx):
    start = (idx * 3) % len(pool)
    chosen = [pool[(start + i) % len(pool)] for i in range(12)]
    lid = f'a1-{section_id[-3:]}-l{lesson_no:02d}'
    xp = 30 if title in ('Môj deň od rána do večera','Plán a rozvrh','Cesta a doprava','V kaviarni','A1 v praxi') else 25
    words = []
    for i, (sk, uk) in enumerate(chosen, 1):
        words.append({
            'id': f'{lid}-w{i:02d}', 'sk': sk, 'uk': uk,
            'pronunciationUk': mod.pron(sk),
            'exampleSk': sk if sk.endswith(('.', '?', '!')) else sk + '.',
            'exampleUk': uk if uk.endswith(('.', '?', '!')) else uk + '.',
            'level': 'A1', 'topic': theme, 'tags': ['A1', theme.split()[0]]
        })
    wid = lambda i: f'{lid}-w{i:02d}'
    e = []
    e.append({'id':f'{lid}-e01','lessonId':lid,'type':'multiple_choice_translation','question':f'Що означає {words[0]["sk"]}?','options':[words[0]['uk'],words[1]['uk'],words[2]['uk']],'correctAnswer':words[0]['uk'],'explanation':f'{words[0]["sk"]} означає «{words[0]["uk"]}».','wordIds':[wid(1)],'order':1,'difficulty':'easy','button':'Далі'})
    e.append({'id':f'{lid}-e02','lessonId':lid,'type':'multiple_choice_translation','question':'Як сказати це словацькою?','options':[words[1]['sk'],words[3]['sk'],words[4]['sk']],'correctAnswer':words[1]['sk'],'explanation':'Правильний варіант — перша фраза.','wordIds':[wid(2)],'order':2,'difficulty':'easy','button':'Далі'})
    e.append({'id':f'{lid}-e03','lessonId':lid,'type':'match_pairs','question':'З’єднай слово з перекладом.','options':[words[2]['sk'],words[2]['uk'],words[3]['sk'],words[3]['uk']],'correctAnswer':[f'{words[2]["sk"]}|{words[2]["uk"]}',f'{words[3]["sk"]}|{words[3]["uk"]}'],'explanation':'Зістав значення.','wordIds':[wid(3),wid(4)],'order':3,'difficulty':'easy','button':'Далі'})
    e.append({'id':f'{lid}-e04','lessonId':lid,'type':'fill_blank','question':'Доповни правильним варіантом.','options':[words[4]['sk'],words[5]['sk'],words[6]['sk']],'correctAnswer':words[4]['sk'],'explanation':f'Правильно: {words[4]["sk"]}.','wordIds':[wid(5)],'order':4,'difficulty':'easy','button':'Далі','fullSentence':words[4]['exampleSk']})
    e.append({'id':f'{lid}-e05','lessonId':lid,'type':'dropdown_blank','question':'Обери правильний варіант.','sentenceParts':[{'text':'Обери: '},{'blankId':'b1','options':[words[5]['sk'],words[6]['sk'],words[7]['sk']],'correct':words[5]['sk']},{'text':'.'}],'correctAnswer':words[5]['sk'],'explanation':'Правильний варіант відповідає вивченій одиниці.','wordIds':[wid(6)],'order':5,'difficulty':'easy','button':'Далі'})
    toks = words[6]['exampleSk'].split()
    e.append({'id':f'{lid}-e06','lessonId':lid,'type':'sentence_order','question':'Розташуй слова правильно.','tokens':toks,'correctOrder':toks,'explanation':f'Правильно: {words[6]["exampleSk"]}','wordIds':[wid(7)],'order':6,'difficulty':'medium','button':'Далі'})
    toks2 = words[7]['exampleSk'].split()
    e.append({'id':f'{lid}-e07','lessonId':lid,'type':'sentence_builder','question':'Склади правильну фразу.','tokens':toks2,'correctSentence':words[7]['exampleSk'],'explanation':f'Правильно: {words[7]["exampleSk"]}','wordIds':[wid(8)],'order':7,'difficulty':'medium','button':'Далі'})
    e.append({'id':f'{lid}-e08','lessonId':lid,'type':'meaning_in_context','question':'Що означає фраза?','context':words[8]['exampleSk'],'target':words[8]['sk'],'options':[{'id':'a','text':words[8]['uk'],'correct':True},{'id':'b','text':words[9]['uk'],'correct':False},{'id':'c','text':words[10]['uk'],'correct':False}],'explanation':'Зістав значення за контекстом.','wordIds':[wid(9)],'order':8,'difficulty':'medium','button':'Далі'})
    e.append({'id':f'{lid}-e09','lessonId':lid,'type':'natural_phrase','question':'Обери природну фразу.','situation':words[9]['uk'],'options':[{'id':'a','sk':words[9]['sk'],'correct':True},{'id':'b','sk':words[10]['sk'],'correct':False},{'id':'c','sk':words[11]['sk'],'correct':False}],'wordIds':[wid(10),wid(11),wid(12)],'order':9,'difficulty':'medium','button':'Далі'})
    e.append({'id':f'{lid}-e10','lessonId':lid,'type':'multiple_select','question':'Обери правильні фрази.','options':[{'id':'a','sk':words[0]['sk'],'correct':True},{'id':'b','sk':words[4]['sk'],'correct':True},{'id':'c','sk':words[11]['sk'],'correct':False},{'id':'d','sk':'Som zelenina.','correct':False}],'explanation':'Обери два правильні варіанти.','wordIds':[wid(1),wid(5)],'order':10,'difficulty':'medium','button':'Далі'})
    e.append({'id':f'{lid}-e11','lessonId':lid,'type':'reading_comprehension','question':'Прочитай короткий текст.','text':' '.join([words[0]['exampleSk'],words[3]['exampleSk'],words[6]['exampleSk']]),'questions':[{'question':'Що сказано першим?','options':[{'id':'a','sk':words[0]['exampleSk'],'correct':True},{'id':'b','sk':words[1]['exampleSk'],'correct':False},{'id':'c','sk':words[2]['exampleSk'],'correct':False}]}],'wordIds':[wid(1),wid(4),wid(7)],'order':11,'difficulty':'medium','button':'Далі'})
    e.append({'id':f'{lid}-e12','lessonId':lid,'type':'dialogue_choose_reply','question':'Обери правильну відповідь.','dialogue':[{'speaker':'A','text':'Ako to povieš po slovensky?'},{'speaker':'B','text':words[10]['exampleSk']}],'options':[{'id':'a','sk':words[10]['exampleSk'],'correct':True},{'id':'b','sk':words[0]['exampleSk'],'correct':False},{'id':'c','sk':words[1]['exampleSk'],'correct':False}],'wordIds':[wid(11)],'order':12,'difficulty':'medium','button':'Далі'})
    nxt = all_lessons[idx+1]['title'] if idx+1 < len(all_lessons) else None
    lesson = {
        'id':lid,'sectionId':section_id,'level':'A1','title':title,'topic':theme,
        'description':f'Навчися використовувати основні слова й моделі теми: {theme}.',
        'order':lesson_no,'xpReward':xp,'estimatedMinutes':27,'isPublished':False,
        'intro':f'Розберемо практичні слова й готові моделі для теми «{theme}».',
        'completionMessage':f'Ти вже можеш використовувати базові слова й моделі теми «{theme}».',
        'updatedAt':'2026-09-12T12:00:00Z',
        'startScreen':{'screenType':'lesson_start','title':title,'shortDescription':f'Практична словацька: {theme}.','outcomes':['розуміти ключову лексику','будувати прості фрази','використовувати навичку в контексті'],'newWords':[w['sk'] for w in words],'exercisesCount':12,'reward':f'{xp} XP','button':'Почати урок'},
        'theoryScreens':[
            {'screenType':'theory','order':1,'title':f'{title}: основа','text':'Опрацюй перші ключові одиниці разом із готовими прикладами.','examples':[{'sk':words[0]['exampleSk'],'uk':words[0]['exampleUk']},{'sk':words[1]['exampleSk'],'uk':words[1]['exampleUk']}],'exampleSk':words[0]['exampleSk'],'exampleUk':words[0]['exampleUk'],'shortRule':'Вчи фразу разом із її значенням і контекстом.','button':'Далі'},
            {'screenType':'theory','order':2,'title':f'{title}: практика','text':'Поєднай нові одиниці та використай їх у коротких реальних ситуаціях.','examples':[{'sk':words[6]['exampleSk'],'uk':words[6]['exampleUk']},{'sk':words[9]['exampleSk'],'uk':words[9]['exampleUk']}],'exampleSk':words[9]['exampleSk'],'exampleUk':words[9]['exampleUk'],'shortRule':'Перенось вивчену модель у новий контекст.','button':'Далі'}
        ],
        'wordsScreen':{'screenType':'lesson_words','title':title,'description':'Повтори ключову лексику уроку.','items':[{'wordId':w['id'],'sk':w['sk'],'uk':w['uk'],'pronunciationUk':w['pronunciationUk'],'exampleSk':w['exampleSk'],'exampleUk':w['exampleUk']} for w in words],'button':'Почати вправи'},
        'words':words,'exercises':e,
        'finalSituation':{'screenType':'final_life_situation','title':'Ситуація з життя','scenario':f'Ти опинився в реальній ситуації, пов’язаній із темою «{theme}».','question':'Яка фраза найкраще підходить?','options':[words[9]['exampleSk'],words[10]['exampleSk'],words[11]['exampleSk']],'correctAnswer':'1','translation':words[9]['exampleUk'],'explanation':'Обери фразу, яка найточніше виконує комунікативне завдання.','button':'Перевірити'},
        'resultScreen':{'screenType':'lesson_result','title':'Урок завершено','text':f'Ти потренував ключову лексику теми «{theme}».','nowYouKnow':[f'{words[0]["sk"]} — {words[0]["uk"]}',f'{words[1]["sk"]} — {words[1]["uk"]}',f'{words[9]["sk"]} — {words[9]["uk"]}'],'result':f'+{xp} XP','newWordsCount':12,'exercisesCompleted':12,'mistakesMessage':'Матеріал із помилками додано до повторення.','buttons':['Продовжити','Повторити урок','Тренувати помилки'],'nextLesson':nxt}
    }
    return {'lessons':[lesson]}

mod.mk_lesson = mk_lesson
mod.main()
