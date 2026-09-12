#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / 'lessons' / 'a1'

TOPICS = {
  'a1_s06':'Дії та мій щоденний день','a1_s07':'Числа, кількість, час і дати','a1_s08':'Місто, місце та рух',
  'a1_s09':'Їжа, напої та кафе','a1_s10':'Покупки, гроші, одяг і послуги','a1_s11':'Навчання, робота та щоденні обов’язки',
  'a1_s12':'Вільний час, інтереси та соціальне спілкування','a1_s13':'Тіло, здоров’я, проблеми та допомога','a1_s14':'Інтеграція A1: реальне життя'
}
GOALS = {
'Čo robím každý deň':'Розповідати про основні щоденні дії.','Ako sa menia slovesá':'Розуміти й уживати часті форми дієслів у теперішньому часі.','Môj deň':'Розповідати про свій день у часовій послідовності.','Byť a mať':'Використовувати базові форми byť і mať.','Každý deň sa učím':'Говорити про щоденні рефлексивні дії з sa.','Nie každý deň':'Будувати прості заперечні речення про щоденні дії.','Môj deň od rána do večera':'Інтегрувати дії, час і заперечення в короткій розповіді.',
'Čísla a množstvo':'Називати числа й базову кількість.','Koľko?':'Питати й відповідати про кількість, вік, телефони та ціни.','Koľko je hodín?':'Питати та називати час на годиннику.','Dni a časti dňa':'Називати дні тижня та частини дня.','Dátumy a mesiace':'Розуміти й називати дати та місяці.','Plán a rozvrh':'Домовлятися про час і простий розклад.',
'Miesta v meste':'Називати основні місця в місті.','Kde som?':'Говорити, де ти знаходишся.','Kam idem?':'Говорити, куди ти йдеш або їдеш.','V meste a do mesta':'Використовувати базові просторові моделі руху.','Ako sa tam dostanem?':'Питати, як дістатися до місця.','Ako sa tam ide?':'Пояснювати простий маршрут.','Cesta a doprava':'Користуватися мовою міста, дороги та транспорту.',
'Jedlo a nápoje':'Називати базові їжу та напої.','Čo mám rád?':'Говорити про свої смаки та вподобання.','Koľko porcií?':'Питати про кількість і порції.','V jedálnom lístku':'Розуміти базову мову меню.','Objednávka v kaviarni':'Робити просте замовлення в кафе.','V kaviarni':'Обрати, замовити, уточнити й оплатити.',
'V obchode':'Розуміти базову мову магазину й товарів.','Koľko to stojí?':'Питати й говорити про ціну та кількість.','Farba a veľkosť':'Говорити про колір і розмір.','Oblečenie':'Називати базовий одяг.','Chcem to':'Робити прості запити, вибирати й оплачувати.','Problém v obchode':'Пояснювати просту проблему в магазині або сервісі.',
'Študujem':'Говорити про навчання та навчальні дії.','Pracujem':'Говорити про роботу та професії.','Kde pracujem a čo robím?':'Розповідати, де працюєш або навчаєшся і що робиш.','Môj rozvrh':'Говорити про розклад і щоденні обов’язки.','Môj deň v škole alebo v práci':'Описувати типовий день у школі або на роботі.',
'Vo voľnom čase':'Говорити про хобі та вільний час.','Páči sa mi':'Висловлювати вподобання й невподобання.','Poďme spolu':'Запрошувати й пропонувати спільні дії.','Čo budeme robiť?':'Домовлятися про прості плани.','Dohodneme sa':'Приймати, відмовлятися та погоджуватися у простому діалозі.',
'Moje telo':'Називати частини тіла та базовий стан.','Nie som v poriadku':'Говорити про прості проблеми зі здоров’ям.','Potrebujem pomoc':'Просити про допомогу в аптеці, у лікаря чи в іншій ситуації.','Čo mi je?':'Описувати проблему та розуміти просту пораду.',
'Ja a môj život':'Поєднати особисті дані, родину, дім і день.','V meste':'Поєднати місце, транспорт, напрямок і час.','Nakupovanie a služby':'Поєднати товар, ціну, кількість, запит і проблему.','Spoločenský deň':'Поєднати знайомство, кафе, запрошення, плани й повідомлення.','A1 v praxi':'Використати A1 для реальної практичної комунікації.'}

def translit(sk):
    table=str.maketrans({'č':'ч','Č':'Ч','š':'ш','Š':'Ш','ž':'ж','Ž':'Ж','ľ':'ль','ť':'ть','ď':'дь','ň':'нь','ä':'е','á':'а','é':'е','í':'і','ó':'о','ú':'у','ô':'уо','ý':'и','ö':'о','ŕ':'р','ĺ':'л'})
    return sk.translate(table)

def ex(term, section, uk):
    t=term.strip()
    overrides={
      ('a1_s07','nula'):'Mám nula lístkov.',('a1_s07','jeden'):'Mám jeden lístok.',('a1_s07','dva'):'Mám dva lístky.',('a1_s07','tri'):'Mám tri lístky.',('a1_s07','štyri'):'Mám štyri lístky.',('a1_s07','päť'):'Mám päť lístkov.',('a1_s07','desať'):'Mám desať lístkov.',('a1_s07','dvadsať'):'Mám dvadsať lístkov.',('a1_s07','koľko'):'Koľko ich je?',('a1_s07','veľa'):'Mám veľa času.',('a1_s07','málo'):'Mám málo času.',('a1_s07','tridsať rokov'):'Mám tridsať rokov.',('a1_s07','v pondelok'):'V pondelok pracujem.',('a1_s07','dnes'):'Dnes pracujem.',('a1_s07','zajtra'):'Zajtra pracujem.',('a1_s07','v piatok o tretej'):'Stretneme sa v piatok o tretej.',
      ('a1_s08','banka'):'Banka je v centre.',('a1_s08','pošta'):'Pošta je v centre.',('a1_s08','stanica'):'Stanica je v centre.',('a1_s08','obchod'):'Obchod je v centre.',('a1_s08','lekáreň'):'Lekáreň je v centre.',('a1_s08','reštaurácia'):'Reštaurácia je v centre.',('a1_s08','škola'):'Škola je v centre.',('a1_s08','nemocnica'):'Nemocnica je v centre.',('a1_s08','centrum'):'Som v centre.',('a1_s08','vpravo'):'Obchod je vpravo.',('a1_s08','vľavo'):'Obchod je vľavo.',('a1_s08','rovno'):'Choď rovno.',('a1_s08','na rohu'):'Banka je na rohu.',
      ('a1_s09','chlieb'):'Mám chlieb.',('a1_s09','mlieko'):'Pijem mlieko.',('a1_s09','voda'):'Pijem vodu.',('a1_s09','káva'):'Mám rád kávu.',('a1_s09','čaj'):'Pijem čaj.',('a1_s09','polievka'):'Mám polievku.',('a1_s09','šalát'):'Mám šalát.',('a1_s09','mäso'):'Mám mäso.',('a1_s09','ovocie'):'Mám ovocie.',('a1_s09','účtenku, prosím'):'Účtenku, prosím.',('a1_s09','ďakujem'):'Ďakujem.',
      ('a1_s10','obchod'):'Som v obchode.',('a1_s10','tričko'):'Chcem tričko.',('a1_s10','košeľa'):'Chcem košeľu.',('a1_s10','nohavice'):'Chcem nohavice.',('a1_s10','topánky'):'Chcem topánky.',('a1_s10','bunda'):'Chcem bundu.',('a1_s10','čierny'):'Môj kabát je čierny.',('a1_s10','biely'):'Môj kabát je biely.',('a1_s10','modrý'):'Môj kabát je modrý.',('a1_s10','veľkosť M'):'Mám veľkosť M.',('a1_s10','prosím tašku'):'Môžem dostať tašku, prosím?',
      ('a1_s11','učiteľ'):'Učiteľ je v škole.',('a1_s11','študent'):'Som študent.',('a1_s11','práca'):'Som v práci.',
      ('a1_s13','hlava'):'Bolí ma hlava.',('a1_s13','ruka'):'Bolí ma ruka.',('a1_s13','noha'):'Bolí ma noha.',('a1_s13','oko'):'Bolí ma oko.',('a1_s13','ucho'):'Bolí ma ucho.',('a1_s13','chrbát'):'Bolí ma chrbát.',('a1_s13','prosím pomoc'):'Prosím, pomôžte mi.',
      ('a1_s14','volám sa'):'Volám sa Nina.',('a1_s14','som z'):'Som z Ukrajiny.',('a1_s14','bývam v'):'Bývam v Bratislave.',('a1_s14','môj byt'):'Môj byt je malý.',('a1_s14','vo voľnom čase'):'Vo voľnom čase čítam.'
    }
    if (section,t) in overrides: return overrides[(section,t)]
    if t.endswith(('.', '?', '!')): return t[0].upper()+t[1:]
    # Most first-person verb forms are valid standalone sentences.
    first_person={'vstávam','raňajkujem','pracujem','študujem','čítam','píšem','počúvam','oddychujem','športujem'}
    if t in first_person: return t[0].upper()+t[1:]+'.'
    if ' ' in t:
        return t[0].upper()+t[1:]+('.' if not t.endswith('?') else '')
    return t[0].upper()+t[1:]+'.'

def repair(path):
    doc=json.loads(path.read_text(encoding='utf-8'))
    lesson=doc['lessons'][0]; section=lesson['sectionId']; title=lesson['title']; topic=TOPICS.get(section,lesson.get('topic',''))
    goal=GOALS.get(title,'Практично використовувати ключову лексику й моделі уроку.')
    # Normalize a few known bad lexical entries.
    for w in lesson.get('words',[]):
        if section=='a1_s09' and w['sk']=='účtenku, prosím': w['uk']='чек, будь ласка'
        if section=='a1_s10' and w['sk']=='prosím tašku': w['sk']='Môžem dostať tašku, prosím?'; w['uk']='Можна пакет, будь ласка?'
        if section=='a1_s13' and w['sk']=='prosím pomoc': w['sk']='Prosím, pomôžte mi.'; w['uk']='Допоможіть, будь ласка.'
        w['pronunciationUk']=translit(w['sk'])
        w['exampleSk']=ex(w['sk'],section,w['uk'])
        w['exampleUk']=w['uk'] if w['uk'].endswith(('.', '?','!')) else w['uk']+'.'
    words=lesson['words']; ids=[w['id'] for w in words]
    lesson['topic']=topic; lesson['description']=f'{goal}'; lesson['intro']=f'У цьому уроці: {goal}' ; lesson['completionMessage']=f'Ти вже можеш: {goal[0].lower()+goal[1:]}'
    lesson['startScreen']['shortDescription']=goal; lesson['startScreen']['outcomes']=[goal,'розуміти ключову лексику в простому контексті','використовувати модель у короткій реальній ситуації']; lesson['startScreen']['newWords']=[w['sk'] for w in words]; lesson['startScreen']['exercisesCount']=12
    # Four compact theory screens, all learner-facing text in Ukrainian.
    lesson['theoryScreens']=[]
    for n,inds in enumerate(([0,1,2],[3,4,5],[6,7,8],[9,10,11]),1):
        a,b=words[inds[0]],words[inds[1]]
        lesson['theoryScreens'].append({'screenType':'theory','order':n,'title':f'{title}: {n}','text':f'{goal} Опрацюй ці одиниці разом із готовими прикладами.','examples':[{'sk':a['exampleSk'],'uk':a['exampleUk']},{'sk':b['exampleSk'],'uk':b['exampleUk']}],'exampleSk':a['exampleSk'],'exampleUk':a['exampleUk'],'shortRule':'Запам’ятовуй модель разом із прикладом і значенням.','button':'Далі'})
    lesson['wordsScreen']['title']=topic; lesson['wordsScreen']['description']='Повтори слова й готові моделі уроку.'; lesson['wordsScreen']['items']=[{'wordId':w['id'],'sk':w['sk'],'uk':w['uk'],'pronunciationUk':w['pronunciationUk'],'exampleSk':w['exampleSk'],'exampleUk':w['exampleUk']} for w in words]
    W=lambda i: words[i-1]['sk']; U=lambda i: words[i-1]['uk']; I=lambda i: words[i-1]['id']; E=lambda i: words[i-1]['exampleSk']
    def blank(i): return re.sub(re.escape(W(i)), '___', E(i), count=1, flags=re.I)
    ex=[]
    ex.append({'id':f"{lesson['id']}-e01",'lessonId':lesson['id'],'type':'multiple_choice_translation','question':f'Що означає {W(1)}?','options':[U(1),U(2),U(3)],'correctAnswer':U(1),'explanation':f'{W(1)} означає «{U(1)}».','wordIds':[I(1)],'order':1,'difficulty':'easy','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e02",'lessonId':lesson['id'],'type':'reverse_translation','question':f'Як сказати «{U(2)}»?','options':[W(2),W(3),W(4)],'correctAnswer':W(2),'explanation':f'Правильний варіант: {W(2)}.','wordIds':[I(2)],'order':2,'difficulty':'easy','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e03",'lessonId':lesson['id'],'type':'match_pairs','question':'З’єднай слово з перекладом.','options':[W(3),U(3),W(4),U(4)],'correctAnswer':[f'{W(3)}|{U(3)}',f'{W(4)}|{U(4)}'],'explanation':'Зістав дві нові одиниці.','wordIds':[I(3),I(4)],'order':3,'difficulty':'easy','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e04",'lessonId':lesson['id'],'type':'fill_blank','question':f'Доповни: {blank(5)}','options':[W(5),W(6),W(7)],'correctAnswer':W(5),'explanation':f'Повне речення: {E(5)}','wordIds':[I(5)],'order':4,'difficulty':'easy','button':'Далі','fullSentence':E(5)})
    p=blank(6); before,after=(p.split('___',1)+[''])[:2] if '___' in p else ('','')
    ex.append({'id':f"{lesson['id']}-e05",'lessonId':lesson['id'],'type':'dropdown_blank','question':'Обери правильне слово у реченні.','sentenceParts':[{'text':before},{'blankId':'b1','options':[W(6),W(7),W(8)],'correct':W(6)},{'text':after}],'correctAnswer':W(6),'explanation':f'Правильно: {E(6)}','wordIds':[I(6)],'order':5,'difficulty':'easy','button':'Далі'})
    toks=E(7).split(); ex.append({'id':f"{lesson['id']}-e06",'lessonId':lesson['id'],'type':'sentence_order','question':'Розташуй слова правильно.','tokens':toks,'correctOrder':toks,'explanation':f'Правильно: {E(7)}','wordIds':[I(7)],'order':6,'difficulty':'medium','button':'Далі'})
    toks=E(8).split(); ex.append({'id':f"{lesson['id']}-e07",'lessonId':lesson['id'],'type':'sentence_builder','question':'Склади правильне речення.','tokens':toks,'correctSentence':E(8),'explanation':f'Правильно: {E(8)}','wordIds':[I(8)],'order':7,'difficulty':'medium','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e08",'lessonId':lesson['id'],'type':'meaning_in_context','question':'Що означає ця фраза в контексті?','context':E(9),'target':W(9),'options':[{'id':'a','text':U(9),'correct':True},{'id':'b','text':U(10),'correct':False},{'id':'c','text':U(11),'correct':False}],'explanation':'Знайди значення цілого вислову.','wordIds':[I(9)],'order':8,'difficulty':'medium','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e09",'lessonId':lesson['id'],'type':'natural_phrase','question':'Обери природну фразу для ситуації.','situation':U(9),'options':[{'id':'a','sk':E(9),'correct':True},{'id':'b','sk':E(10),'correct':False},{'id':'c','sk':E(11),'correct':False}],'wordIds':[I(9),I(10),I(11)],'order':9,'difficulty':'medium','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e10",'lessonId':lesson['id'],'type':'multiple_select','question':'Обери два речення, які безпосередньо тренують тему уроку.','options':[{'id':'a','sk':E(1),'correct':True},{'id':'b','sk':E(5),'correct':True},{'id':'c','sk':'Mám psa.','correct':False},{'id':'d','sk':'Som zelenina.','correct':False}],'explanation':'Правильні два варіанти взяті з цільової лексики уроку.','wordIds':[I(1),I(5)],'order':10,'difficulty':'medium','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e11",'lessonId':lesson['id'],'type':'reading_comprehension','question':'Прочитай короткий текст і відповідай на запитання.','text':' '.join([E(1),E(2),E(3)]),'questions':[{'question':f'Що означає перша фраза?','options':[{'id':'a','sk':U(1),'correct':True},{'id':'b','sk':U(2),'correct':False},{'id':'c','sk':U(3),'correct':False}]}],'wordIds':[I(1),I(2),I(3)],'order':11,'difficulty':'medium','button':'Далі'})
    ex.append({'id':f"{lesson['id']}-e12",'lessonId':lesson['id'],'type':'dialogue_choose_reply','question':'Обери правильну відповідь у діалозі.','dialogue':[{'speaker':'A','text':'Čo povieš?'} ,{'speaker':'B','text':E(10)}],'options':[{'id':'a','sk':E(10),'correct':True},{'id':'b','sk':E(11),'correct':False},{'id':'c','sk':E(9),'correct':False}],'wordIds':[I(10)],'order':12,'difficulty':'medium','button':'Далі'})
    lesson['exercises']=ex
    lesson['finalSituation']={'screenType':'final_life_situation','title':'Ситуація з життя','scenario':f'Ти використовуєш словацьку в ситуації за темою «{topic}».','question':f'Як сказати «{U(9)}»?','options':[E(9),E(10),E(11)],'correctAnswer':'1','translation':U(9),'explanation':'Перенеси вивчену модель у нову практичну ситуацію.','button':'Перевірити'}
    lesson['resultScreen']={'screenType':'lesson_result','title':'Урок завершено','text':f'Ти попрактикував тему «{topic}».','nowYouKnow':[f'{W(1)} — {U(1)}',f'{W(2)} — {U(2)}',f'{W(9)} — {U(9)}'],'result':f"+{lesson.get('xpReward',25)} XP",'newWordsCount':12,'exercisesCompleted':12,'mistakesMessage':'Матеріал із помилками додано до повторення.','buttons':['Продовжити','Повторити урок','Тренувати помилки'],'nextLesson':None}
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    files=sorted(LESSON_DIR.glob('a1-s*.json'))
    for p in files:
        m=re.match(r'a1-s(0[6-9]|1[0-4])-l(\d+)\.json$',p.name)
        if m: repair(p)
    print('Repaired Sections 06–14.')
if __name__=='__main__': main()
