#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / 'lessons' / 'a1'

SECTION_DATA = {
'a1_s06': {'theme':'Actions and my everyday day','titles':['Čo robím každý deň','Ako sa menia slovesá','Môj deň','Byť a mať','Každý deň sa učím','Nie každý deň','Môj deň od rána do večera'],'pool':[
('vstávam','встаю'),('raňajkujem','снідаю'),('pracujem','працюю'),('študujem','навчаюся'),('čítam','читаю'),('píšem','пишу'),('počúvam','слухаю'),('jem obed','обідаю'),('idem domov','іду додому'),('vraciam sa domov','повертаюся додому'),('oddychujem','відпочиваю'),('večer idem spať','увечері йду спати'),('som doma','я вдома'),('mám čas','я маю час'),('učím sa každý deň','я вчуся щодня'),('dnes nepracujem','сьогодні я не працюю'),('zajtra nejdem do práce','завтра я не йду на роботу'),('každý deň sa umývam','я щодня вмиваюся') ]},
'a1_s07': {'theme':'Numbers, quantity, time and dates','titles':['Čísla a množstvo','Koľko?','Koľko je hodín?','Dni a časti dňa','Dátumy a mesiace','Plán a rozvrh'],'pool':[
('nula','нуль'),('jeden','один'),('dva','два'),('tri','три'),('štyri','чотири'),('päť','п’ять'),('desať','десять'),('dvadsať','двадцять'),('koľko','скільки'),('veľa','багато'),('málo','мало'),('tridsať rokov','тридцять років'),('Koľko je hodín?','Котра година?'),('Sú tri hodiny.','Третя година.'),('v pondelok','у понеділок'),('dnes','сьогодні'),('zajtra','завтра'),('v piatok o tretej','у п’ятницю о третій') ]},
'a1_s08': {'theme':'City, place and movement','titles':['Miesta v meste','Kde som?','Kam idem?','V meste a do mesta','Ako sa tam dostanem?','Ako sa tam ide?','Cesta a doprava'],'pool':[
('banka','банк'),('pošta','пошта'),('stanica','станція'),('obchod','магазин'),('lekáreň','аптека'),('reštaurácia','ресторан'),('škola','школа'),('nemocnica','лікарня'),('centrum','центр'),('som v centre','я в центрі'),('idem do centra','я йду до центру'),('idem na stanicu','я йду на станцію'),('kde je banka?','де банк?'),('vpravo','праворуч'),('vľavo','ліворуч'),('rovno','прямо'),('na rohu','на розі'),('idem autobusom','я їду автобусом') ]},
'a1_s09': {'theme':'Food, drinks and café','titles':['Jedlo a nápoje','Čo mám rád?','Koľko porcií?','V jedálnom lístku','Objednávka v kaviarni','V kaviarni'],'pool':[
('chlieb','хліб'),('mlieko','молоко'),('voda','вода'),('káva','кава'),('čaj','чай'),('polievka','суп'),('šalát','салат'),('mäso','м’ясо'),('ovocie','фрукти'),('mám rád kávu','я люблю каву'),('nemám rád čaj','я не люблю чай'),('chcem vodu','я хочу воду'),('prosím si kávu','я хотів би каву'),('dám si polievku','я візьму суп'),('koľko to stojí?','скільки це коштує?'),('účtenku, prosím','рахунок, будь ласка'),('platím kartou','я плачу карткою'),('ďakujem','дякую') ]},
'a1_s10': {'theme':'Shopping, money, clothing and services','titles':['V obchode','Koľko to stojí?','Farba a veľkosť','Oblečenie','Chcem to','Problém v obchode'],'pool':[
('obchod','магазин'),('tričko','футболка'),('košeľa','сорочка'),('nohavice','штани'),('topánky','взуття'),('bunda','куртка'),('čierny','чорний'),('biely','білий'),('modrý','синій'),('veľkosť M','розмір M'),('koľko to stojí?','скільки це коштує?'),('je to lacné','це дешево'),('je to drahé','це дорого'),('chcem toto tričko','я хочу цю футболку'),('prosím tašku','будь ласка, пакет'),('platím kartou','я плачу карткою'),('chcem to vymeniť','я хочу це обміняти'),('účtenku, prosím','чек, будь ласка') ]},
'a1_s11': {'theme':'Study, work and everyday responsibilities','titles':['Študujem','Pracujem','Kde pracujem a čo robím?','Môj rozvrh','Môj deň v škole alebo v práci'],'pool':[
('študujem','навчаюся'),('učím sa slovenčinu','вчу словацьку'),('čítam','читаю'),('píšem','пишу'),('počúvam','слухаю'),('učiteľ','учитель'),('študent','студент'),('práca','робота'),('pracujem v kancelárii','працюю в офісі'),('pracujem dnes','я працюю сьогодні'),('mám úlohu','у мене є завдання'),('mám test','у мене тест'),('začínam o ôsmej','починаю о восьмій'),('končím o piatej','закінчую о п’ятій'),('mám prestávku','маю перерву'),('som v práci','я на роботі'),('som v škole','я в школі'),('zajtra mám prácu','завтра я працюю') ]},
'a1_s12': {'theme':'Free time, interests, plans and social communication','titles':['Vo voľnom čase','Páči sa mi','Poďme spolu','Čo budeme robiť?','Dohodneme sa'],'pool':[
('vo voľnom čase','у вільний час'),('čítam knihy','читаю книжки'),('počúvam hudbu','слухаю музику'),('pozerám film','дивлюся фільм'),('športujem','займаюся спортом'),('chodím na prechádzku','ходжу на прогулянку'),('mám rád hudbu','я люблю музику'),('nemám rád futbal','я не люблю футбол'),('páči sa mi film','мені подобається фільм'),('poďme spolu','ходімо разом'),('môžeme ísť','ми можемо піти'),('chceš ísť?','хочеш піти?'),('dnes mám čas','сьогодні я маю час'),('zajtra nemám čas','завтра я не маю часу'),('stretneme sa večer','зустрінемося ввечері'),('áno, rád','так, із задоволенням'),('nie, nemôžem','ні, не можу'),('dobre, dohodnuté','добре, домовились') ]},
'a1_s13': {'theme':'Body, health, problems and help','titles':['Moje telo','Nie som v poriadku','Potrebujem pomoc','Čo mi je?'],'pool':[
('hlava','голова'),('ruka','рука'),('noha','нога'),('oko','око'),('ucho','вухо'),('chrbát','спина'),('som unavený','я втомлений'),('som chorý','я хворий'),('bolí ma hlava','у мене болить голова'),('bolí ma hrdlo','у мене болить горло'),('potrebujem lekára','мені потрібен лікар'),('potrebujem liek','мені потрібні ліки'),('kde je lekáreň?','де аптека?'),('prosím pomoc','допоможіть, будь ласка'),('mám teplotu','у мене температура'),('nemôžem chodiť','я не можу ходити'),('čo mi je?','що зі мною?'),('potrebujem pomoc','мені потрібна допомога') ]},
'a1_s14': {'theme':'A1 integration: real life','titles':['Ja a môj život','V meste','Nakupovanie a služby','Spoločenský deň','A1 v praxi'],'pool':[
('volám sa','мене звати'),('som z','я з'),('bývam v','я живу в'),('mám rodinu','у мене є родина'),('mám prácu','у мене є робота'),('môj byt','моя квартира'),('ráno pracujem','вранці я працюю'),('idem do mesta','я йду в місто'),('hľadám stanicu','я шукаю станцію'),('chcem kávu','я хочу каву'),('koľko to stojí?','скільки це коштує?'),('chcem to kúpiť','я хочу це купити'),('stretneme sa večer','зустрінемося ввечері'),('môžeme ísť spolu','ми можемо піти разом'),('nemám čas','я не маю часу'),('potrebujem pomoc','мені потрібна допомога'),('prosím zopakujte','повторіть, будь ласка'),('ďakujem, dovidenia','дякую, до побачення') ]}
}

LESSON_SECTIONS = [('a1_s06',31),('a1_s07',38),('a1_s08',44),('a1_s09',51),('a1_s10',57),('a1_s11',63),('a1_s12',68),('a1_s13',73),('a1_s14',77)]

def pron(sk: str) -> str:
    table = str.maketrans({'č':'ч','Č':'Ч','š':'ш','Š':'Ш','ž':'ж','Ž':'Ж','ľ':'ль','Ľ':'Ль','ť':'ть','Ť':'Ть','ď':'дь','Ď':'Дь','ň':'нь','Ň':'Нь','ä':'е','á':'а','é':'е','í':'і','ó':'о','ú':'у','ô':'уо','ý':'и','ö':'о','ŕ':'р','ĺ':'л'})
    return sk.translate(table)

def mk_lesson(section_id, lesson_no, title, theme, pool, all_lessons, idx):
    start = (idx * 3) % len(pool)
    chosen = [pool[(start+i)%len(pool)] for i in range(12)]
    lid = f'a1-{section_id[-3:]}-l{lesson_no:02d}'
    words = []
    for i,(sk,uk) in enumerate(chosen,1):
        words.append({'id':f'{lid}-w{i:02d}','sk':sk,'uk':uk,'pronunciationUk':pron(sk),'exampleSk':sk if sk.endswith(('.', '?','!')) else sk+'.','exampleUk':uk if uk.endswith(('.', '?','!')) else uk+'.','level':'A1','topic':theme,'tags':['A1',theme.split()[0]]})
    def exsk(i): return words[i-1]['exampleSk']
    def exuk(i): return words[i-1]['exampleUk']
    def wid(i): return f'{lid}-w{i:02d}'
    exercises=[]
    exercises.append({'id':f'{lid}-e01','lessonId':lid,'type':'multiple_choice_translation','question':f'Що означає {words[0]["sk"]}?','options':[words[0]['uk'],words[1]['uk'],words[2]['uk']], 'correctAnswer':words[0]['uk'],'explanation':f'{words[0]["sk"]} означає «{words[0]["uk"]}».','wordIds':[wid(1)],'order':1,'difficulty':'easy','button':'Далі'})
    exercises.append({'id':f'{lid}-e02','lessonId':lid,'type':'multiple_choice_translation','question':'Як сказати це словацькою?','options':[words[1]['sk'],words[3]['sk'],words[4]['sk']], 'correctAnswer':words[1]['sk'],'explanation':f'Правильна фраза: {words[1]["sk"]}.','wordIds':[wid(2)],'order':2,'difficulty':'easy','button':'Далі'})
    exercises.append({'id':f'{lid}-e03','lessonId':lid,'type':'match_pairs','question':'З’єднай фрази з перекладом.','options':[words[2]['sk'],words[2]['uk'],words[3]['sk'],words[3]['uk']], 'correctAnswer':[f'{words[2]["sk"]}|{words[2]["uk"]}',f'{words[3]["sk"]}|{words[3]["uk"]}'],'explanation':'Перевір значення двох нових одиниць.','wordIds':[wid(3),wid(4)],'order':3,'difficulty':'easy','button':'Далі'})
    exercises.append({'id':f'{lid}-e04','lessonId':lid,'type':'fill_blank','question':'Доповни правильним варіантом.','options':[words[4]['sk'],words[5]['sk'],words[6]['sk']], 'correctAnswer':words[4]['sk'],'explanation':f'Правильно: {words[4]["sk"]}.','wordIds':[wid(5)],'order':4,'difficulty':'easy','button':'Далі','fullSentence':words[4]['exampleSk']})
    exercises.append({'id':f'{lid}-e05','lessonId':lid,'type':'dropdown_blank','question':'Обери правильну фразу.','sentenceParts':[{'text':'Обери: '},{'blankId':'b1','options':[words[5]['sk'],words[6]['sk'],words[7]['sk']],'correct':words[5]['sk']},{'text':'.'}], 'correctAnswer':words[5]['sk'],'explanation':'Правильний вибір відповідає новій фразі.','wordIds':[wid(6)],'order':5,'difficulty':'easy','button':'Далі'})
    toks = words[6]['exampleSk'].split()
    exercises.append({'id':f'{lid}-e06','lessonId':lid,'type':'sentence_order','question':'Розташуй слова правильно.','tokens':toks,'correctOrder':toks,'explanation':f'Правильно: {words[6]["exampleSk"]}','wordIds':[wid(7)],'order':6,'difficulty':'medium','button':'Далі'})
    toks2 = words[7]['exampleSk'].split()
    exercises.append({'id':f'{lid}-e07','lessonId':lid,'type':'sentence_builder','question':'Склади правильну фразу.','tokens':toks2,'correctSentence':words[7]['exampleSk'],'explanation':f'Правильно: {words[7]["exampleSk"]}','wordIds':[wid(8)],'order':7,'difficulty':'medium','button':'Далі'})
    exercises.append({'id':f'{lid}-e08','lessonId':lid,'type':'meaning_in_context','question':'Що означає ця фраза в контексті?','context':words[8]['exampleSk'],'target':words[8]['sk'],'options':[{'id':'a','text':words[8]['uk'],'correct':True},{'id':'b','text':words[9]['uk'],'correct':False},{'id':'c','text':words[10]['uk'],'correct':False}],'explanation':'Зістав словацьку фразу з правильним значенням.','wordIds':[wid(9)],'order':8,'difficulty':'medium','button':'Далі'})
    exercises.append({'id':f'{lid}-e09','lessonId':lid,'type':'natural_phrase','question':'Обери природну фразу для ситуації.','situation':words[9]['uk'],'options':[{'id':'a','sk':words[9]['sk'],'correct':True},{'id':'b','sk':words[10]['sk'],'correct':False},{'id':'c','sk':words[11]['sk'],'correct':False}],'wordIds':[wid(10),wid(11),wid(12)],'order':9,'difficulty':'medium','button':'Далі'})
    exercises.append({'id':f'{lid}-e10','lessonId':lid,'type':'multiple_select','question':'Обери дві фрази, які відповідають темі уроку.','options':[{'id':'a','sk':words[0]['sk'],'correct':True},{'id':'b','sk':words[4]['sk'],'correct':True},{'id':'c','sk':words[11]['sk'],'correct':False},{'id':'d','sk':'Som zelenina.','correct':False}],'explanation':'Перевір, які фрази справді належать до цього уроку.','wordIds':[wid(1),wid(5)],'order':10,'difficulty':'medium','button':'Далі'})
    exercises.append({'id':f'{lid}-e11','lessonId':lid,'type':'reading_comprehension','question':'Прочитай короткий текст.','text':' '.join([words[0]['exampleSk'],words[3]['exampleSk'],words[6]['exampleSk']]),'questions':[{'question':'Яка фраза відповідає першій частині тексту?','options':[{'id':'a','sk':words[0]['exampleSk'],'correct':True},{'id':'b','sk':words[1]['exampleSk'],'correct':False},{'id':'c','sk':words[2]['exampleSk'],'correct':False}]}],'wordIds':[wid(1),wid(4),wid(7)],'order':11,'difficulty':'medium','button':'Далі'})
    exercises.append({'id':f'{lid}-e12','lessonId':lid,'type':'dialogue_choose_reply','question':'Обери правильну відповідь у короткому діалозі.','dialogue':[{'speaker':'A','text':'Ako to povieš po slovensky?'},{'speaker':'B','text':words[10]['exampleSk']}],'options':[{'id':'a','sk':words[10]['exampleSk'],'correct':True},{'id':'b','sk':words[0]['exampleSk'],'correct':False},{'id':'c','sk':words[1]['exampleSk'],'correct':False}],'wordIds':[wid(11)],'order':12,'difficulty':'medium','button':'Далі'})
    next_title = all_lessons[idx+1]['title'] if idx+1 < len(all_lessons) else None
    scenario = f'Ти опинився в реальній ситуації, пов’язаній із темою «{theme}». Обери найкращу словацьку фразу.'
    final_correct = words[9]['exampleSk']
    final_options=[final_correct,words[10]['exampleSk'],words[11]['exampleSk']]
    lesson={'id':lid,'sectionId':section_id,'level':'A1','title':title,'topic':theme,'description':f'Навчися використовувати основні слова й моделі теми: {theme}.','order':lesson_no,'xpReward':30 if title in ('Môj deň','V kaviarni','Cesta a doprava','A1 v praxi') else 25,'estimatedMinutes':27,'isPublished':False,'intro':f'Розберемо практичні слова й готові моделі для теми «{theme}».','completionMessage':f'Ти вже можеш використовувати базові слова й моделі теми «{theme}».','updatedAt':'2026-09-12T12:00:00Z','startScreen':{'screenType':'lesson_start','title':title,'shortDescription':f'Практична словацька: {theme}.','outcomes':['розуміти ключову лексику','будувати прості фрази','використовувати навичку в контексті'],'newWords':[w['sk'] for w in words],'exercisesCount':12,'reward':f"{lesson['xpReward']} XP",'button':'Почати урок'},'theoryScreens':[{'screenType':'theory','order':1,'title':f'{title}: основа','text':'Почни з перших ключових одиниць і вчи їх разом із готовими прикладами.','examples':[{'sk':words[0]['exampleSk'],'uk':words[0]['exampleUk']},{'sk':words[1]['exampleSk'],'uk':words[1]['exampleUk']}],'exampleSk':words[0]['exampleSk'],'exampleUk':words[0]['exampleUk'],'shortRule':'Вчи фразу разом із її значенням і контекстом.','button':'Далі'},{'screenType':'theory','order':2,'title':f'{title}: у контексті','text':'Далі поєднай нову лексику з іншими словами й короткими реченнями.','examples':[{'sk':words[6]['exampleSk'],'uk':words[6]['exampleUk']},{'sk':words[9]['exampleSk'],'uk':words[9]['exampleUk']}],'exampleSk':words[9]['exampleSk'],'exampleUk':words[9]['exampleUk'],'shortRule':'Використовуй ключову фразу в реальній ситуації.','button':'Далі'}],'wordsScreen':{'screenType':'lesson_words','title':title,'description':'Повтори ключову лексику уроку.','items':[{'wordId':w['id'],'sk':w['sk'],'uk':w['uk'],'pronunciationUk':w['pronunciationUk'],'exampleSk':w['exampleSk'],'exampleUk':w['exampleUk']} for w in words],'button':'Почати вправи'},'words':words,'exercises':exercises,'finalSituation':{'screenType':'final_life_situation','title':'Ситуація з життя','scenario':scenario,'question':'Яка відповідь найкраще підходить?','options':final_options,'correctAnswer':'1','translation':words[9]['exampleUk'],'explanation':'Обери фразу, яка найточніше передає потрібну дію або інформацію.','button':'Перевірити'},'resultScreen':{'screenType':'lesson_result','title':'Урок завершено','text':f'Ти вже потренував ключову лексику теми «{theme}».','nowYouKnow':[f'{words[0]["sk"]} — {words[0]["uk"]}',f'{words[1]["sk"]} — {words[1]["uk"]}',f'{words[9]["sk"]} — {words[9]["uk"]}'],'result':f"+{lesson['xpReward']} XP",'newWordsCount':12,'exercisesCompleted':12,'mistakesMessage':'Матеріал із помилками додано до повторення.','buttons':['Продовжити','Повторити урок','Тренувати помилки'],'nextLesson':next_title}}
    return {'lessons':[lesson]}

def validate(doc):
    assert list(doc.keys()) == ['lessons']
    assert len(doc['lessons']) == 1
    lesson = doc['lessons'][0]
    assert isinstance(lesson['id'],str) and lesson['id'].startswith('a1-s')
    assert lesson['sectionId'] in SECTION_DATA
    assert lesson['startScreen']['exercisesCount'] == len(lesson['exercises']) == 12
    assert len(lesson['words']) == len(lesson['wordsScreen']['items']) == 12
    word_ids={w['id'] for w in lesson['words']}
    assert {i['wordId'] for i in lesson['wordsScreen']['items']} == word_ids
    for e in lesson['exercises']:
        assert e['lessonId']==lesson['id']
        assert set(e.get('wordIds',[])).issubset(word_ids)
    assert lesson['finalSituation']['correctAnswer'] == '1'
    assert lesson['finalSituation']['options'][0]


def main():
    LESSON_DIR.mkdir(parents=True, exist_ok=True)
    # Remove obsolete legacy numerical block and old temporary l34-l39 variants.
    for n in range(12,18):
        p=LESSON_DIR/f'a1-s03-l{n:02d}.json'
        if p.exists(): p.unlink()
    for n in range(31,82):
        p=LESSON_DIR/f'a1-s{6 if n<=37 else 7 if n<=43 else 8 if n<=50 else 9 if n<=56 else 10 if n<=62 else 11 if n<=67 else 12 if n<=72 else 13 if n<=76 else 14:02d}-l{n:02d}.json'
        if p.exists(): p.unlink()
    all_lessons=[]
    seq=31
    for sid, first in LESSON_SECTIONS:
        data=SECTION_DATA[sid]
        for title in data['titles']:
            all_lessons.append({'sectionId':sid,'title':title,'number':seq})
            seq += 1
    idx=0
    for item in all_lessons:
        data=SECTION_DATA[item['sectionId']]
        doc=mk_lesson(item['sectionId'],item['number'],item['title'],data['theme'],data['pool'],all_lessons,idx)
        validate(doc)
        fn=LESSON_DIR/f'a1-s{item["sectionId"][-2:]}-l{item["number"]:02d}.json'
        fn.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        idx += 1
    print(f'Generated {len(all_lessons)} A1 lessons.')

if __name__ == '__main__':
    main()
