from __future__ import annotations
import json, re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
from .model import PlanLesson, LessonCopy, OwnedTarget
from .natural_examples import EXAMPLES
from .semantic_profiles import PROFILES as SEMANTIC_PROFILES

NOW='2026-09-13T21:30:00+02:00'

SECTION_FOCUS = {
1:("Характер і порівняння","Описуй людину короткими прикметниками й додавай звичку або ставлення.","Порівнюй людей лише за однією ознакою за раз: так вислів залишається ясним."),
2:("Рутина й частотність","Поєднуй дію з маркером частотності або часу, щоб розповідь про день була зв’язною.","Для послідовності використовуй najprv, potom, neskôr, nakoniec; вони організують коротку розповідь."),
3:("Минулий час у розповіді","У минулому важливо одразу показати часову рамку: včera, minulý víkend, minulý týždeň.","Зв’язуй події маркерами potom/neskôr/nakoniec і не змішуй часові плани без потреби."),
4:("Плани й майбутнє","Говори про майбутнє через конкретний план, намір або ймовірність: це різні комунікативні задачі.","Для домовленостей завжди уточнюй час, місце й можливість іншої людини."),
5:("Дім і побутові проблеми","Спершу назви місце або предмет, потім проблему, а вже після цього прохання чи рішення.","У проханнях до сусідів і майстрів використовуй ввічливу форму, особливо mohli by ste."),
6:("Місто й транспорт","Маршрут зручніше будувати кроками: напрямок → орієнтир → зупинка або пересадка.","Коли не впевнений, став коротке уточнювальне питання про напрямок, тривалість або потрібну зупинку."),
7:("Їжа й приготування","Поєднуй назву продукту з кількістю, смаком або дією; так лексика працює в реальному контексті.","У рецепті порядок дій важливий: спочатку підготуй, потім додай/змішай, наприкінці перевір результат."),
8:("Покупки й послуги","Під час вибору товару поєднуй запит, характеристику й ціну, а проблему формулюй конкретно.","Для рекламації назви дефект і бажане рішення: vrátiť, vymeniť або opraviť."),
9:("Робота й навчання","Описуй день через завдання, строки й пріоритети; це робить розповідь зрозумілою.","У спільній роботі називай, хто що робить, і підтверджуй домовленість."),
10:("Вільний час і соціальні плани","До запрошення додавай конкретну активність, час або місце, а відмову супроводжуй альтернативою.","Причину вподобання можна коротко пояснити через pretože або інший простий зв’язок."),
11:("Уточнення й розв’язання проблем","Якщо не розумієш, спочатку попроси повторити або пояснити, а не вгадуй зміст.","Проблему зручно будувати як ланцюжок: що сталося → що потрібно → яке рішення пропонуєш."),
12:("Подорож і проживання","У поїздці тримай окремо етапи: відправлення, маршрут, заселення, перебування, повернення.","За зміни плану назви проблему й одразу уточни новий варіант маршруту або бронювання."),
13:("Самопочуття й допомога","Симптом описуй коротко: що болить, як довго, чи є температура або інша ознака.","У лікаря чи аптеці слухай рекомендацію до кінця й уточнюй спосіб застосування ліків."),
14:("Думка, причина й вибір","Вислови позицію, додай одну чітку причину й за потреби порівняй два варіанти.","Конструкції radšej by som або keby тут працюють як контрольовані готові моделі, а не як повна система умовного способу."),
15:("A2: інтеграція","Поєднуй уже відомі моделі без підказки: опис, минуле, план, проблема, рішення й пояснення.","У фінальних ситуаціях важливі зрозумілість, послідовність і здатність уточнити або виправити комунікацію."),
}

PLURAL_NOUNS={'rodičia','starí rodičia','raňajky','cestoviny','domáce práce','povinnosti','tekutiny','posledné dni'}
ADVERBS={'často','niekedy','málokedy','vôbec','ráno','dopoludnia','popoludní','večer','najprv','potom','neskôr','nakoniec','zvyčajne','pravidelne','občas','včera','zrazu','našťastie','bohužiaľ','možno','asi','pravdepodobne','vpravo','vľavo','hore','dole','vpredu','vzadu','blízko','ďaleko','približne','úspešne','hneď','pomalšie','inak','lepšie','horšie','hlavne','najmä','teraz','momentálne','kedysi'}
NEUTER_ADJ={'zaujímavé','nudné','príjemné','nepríjemné','pokojné','rušné','pripravené','čerstvé','teplé','studené','malé','veľké','rozbité','otvorené','zatvorené'}


def pron(sk:str)->str:
    s=sk.lower()
    reps=[('dž','дж'),('ch','х'),('dz','дз'),('ia','іа'),('ie','іє'),('iu','іу'),('ô','уо'),('ľ','ль'),('ĺ','ль'),('ň','нь'),('ď','дь'),('ť','ть'),('č','ч'),('š','ш'),('ž','ж'),('á','аа'),('é','ее'),('í','іі'),('ó','оо'),('ú','уу'),('ý','ии'),('ä','е'),('c','ц'),('j','й'),('y','и'),('q','к'),('w','в'),('x','кс')]
    for a,b in reps: s=s.replace(a,b)
    return s.translate(str.maketrans({'a':'а','b':'б','d':'д','e':'е','f':'ф','g':'ґ','h':'г','i':'і','k':'к','l':'л','m':'м','n':'н','o':'о','p':'п','r':'р','s':'с','t':'т','u':'у','v':'в','z':'з'}))


def cap(s:str)->str: return s[:1].upper()+s[1:] if s else s

def punct(s:str)->str:
    s=s.strip()
    return s if s.endswith(('.', '!', '?')) else s+'.'


def example_for(sk:str, uk:str)->tuple[str,str]:
    low=sk.lower().strip()
    if low in EXAMPLES: return EXAMPLES[low]
    # controlled overrides for forms that are awkward under generic templates
    special={
      'byť taký/á':('Chcem byť taký.','Я хочу бути таким.'),
      'myslím, že':('Myslím, že je to dobré.','Я думаю, що це добре.'),
      'kvôli tomu, že':('Meškám kvôli tomu, že nejde autobus.','Я запізнююся, бо автобус не їде.'),
      'záleží na':('Záleží na situácii.','Це залежить від ситуації.'),
      'keby':('Keby som mal čas, išiel by som.','Якби я мав час, я б пішов.'),
      'zajtra namiesto':('Prídem zajtra, nie dnes.','Я прийду завтра, не сьогодні.'),
      'doma byť':('Zajtra budem doma.','Завтра я буду вдома.'),
      'potreba opravy':('Je tu potreba opravy.','Тут потрібен ремонт.'),
      'radšej by som':('Radšej by som zostal doma.','Я б радше залишився вдома.'),
      'podľa situácie':('Rozhodnem sa podľa situácie.','Я вирішу залежно від ситуації.'),
      'z tohto dôvodu':('Z tohto dôvodu prídem neskôr.','З цієї причини я прийду пізніше.'),
      'cena za noc':('Cena za noc je osemdesiat eur.','Ціна за ніч — вісімдесят євро.'),
      'check-in':('Check-in je od druhej.','Заселення — від другої.'),
      'check-out':('Check-out je do desiatej.','Виїзд — до десятої.'),
      'môžem poprosiť':('Môžem poprosiť o pomoc?','Можна попросити про допомогу?'),
      'mohli by ste':('Mohli by ste mi pomôcť?','Чи могли б ви мені допомогти?'),
      'prosím vás':('Prosím vás, môžete hovoriť tichšie?','Будь ласка, можете говорити тихіше?'),
      'čo povieš':('Čo povieš na kávu?','Що скажеш щодо кави?'),
      'nechceš ísť':('Nechceš ísť so mnou?','Не хочеш піти зі мною?'),
      'ak bude čas':('Pôjdeme von, ak bude čas.','Ми підемо кудись, якщо буде час.'),
      'nebude to možné':('Žiaľ, nebude to možné.','На жаль, це буде неможливо.'),
      'myslím si':('Myslím si, že je to dobré.','Я думаю, що це добре.'),
      'podľa mňa':('Podľa mňa je to lepšie.','На мою думку, це краще.'),
      'podľa mňa áno':('Podľa mňa áno.','На мою думку, так.'),
      'podľa mňa nie':('Podľa mňa nie.','На мою думку, ні.'),
      'večer budem':('Večer budem doma.','Увечері я буду вдома.'),
      'možno budem':('Možno budem doma.','Можливо, я буду вдома.'),
      'možno pôjdem':('Možno pôjdem do mesta.','Можливо, я піду до міста.'),
      'cez víkend chcem':('Cez víkend chcem oddychovať.','На вихідних я хочу відпочивати.'),
      'potrebujem pomoc':('Potrebujem pomoc.','Мені потрібна допомога.'),
      'problém vyriešiť':('Chcem problém vyriešiť dnes.','Я хочу вирішити проблему сьогодні.'),
      'dokončiť načas':('Musíme to dokončiť načas.','Ми маємо завершити це вчасно.'),
      'cesta späť':('Cesta späť trvá dve hodiny.','Дорога назад триває дві години.'),
      'dnes nemôžem':('Dnes nemôžem pracovať.','Сьогодні я не можу працювати.'),
      'zajtra snáď':('Zajtra snáď budem lepšie.','Завтра, сподіваюся, мені буде краще.'),
      'budeme spolu':('Večer budeme spolu.','Увечері ми будемо разом.'),
    }
    if low in special: return special[low]
    # High-risk lexical classes need grammatical context before generic suffix rules.
    natural={
      'včera':('Včera som bol doma.','Учора я був удома.'),
      'ráno som':('Ráno som bol doma.','Вранці я був удома.'),
      'potom som':('Potom som išiel domov.','Потім я пішов додому.'),
      'večer som':('Večer som bol doma.','Увечері я був удома.'),
      'minulý víkend':('Minulý víkend som bol doma.','Минулі вихідні я був удома.'),
      'minulý týždeň':('Minulý týždeň som veľa pracoval.','Минулого тижня я багато працював.'),
      'často':('Často chodím pešo.','Я часто ходжу пішки.'),
      'vpravo':('Obchod je vpravo.','Магазин праворуч.'),
      'na rohu':('Stretneme sa na rohu.','Зустрінемося на розі.'),
      'aktívny':('Je aktívny.','Він активний.'),
      'skúsenosť':('To je skúsenosť.','Це досвід.'),
      'pôjdem':('Pôjdem zajtra.','Я піду / поїду завтра.'),
    }
    if low in natural: return natural[low]

    uk_low=uk.lower().strip()
    if ' ' in low:
        parts=low.split()
        # Finite clauses already contain person/tense; never prepend Chcem to them.
        if uk_low.startswith(('я ','ми ','він ','вона ','вони ')):
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith(' sa'):
            if parts[0].endswith('ť'):
                base=sk[:-3]
                return (f'Chcem sa {base}.', f'Я хочу: {uk}.')
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith(' si'):
            if parts[0].endswith('ť'):
                base=sk[:-3]
                return (f'Chcem si {base}.', f'Я хочу: {uk}.')
            return (punct(cap(sk)), punct(cap(uk)))
        # A future auxiliary + infinitive is already a complete clause.
        if parts[0] in {'budem','budeme','budeš','budete','bude','budú'}:
            return (punct(cap(sk)), punct(cap(uk)))
        if low.endswith('ť') and parts[0].endswith('ť'):
            return (f'Chcem {sk}.', f'Я хочу: {uk}.')
        # If a phrase visibly carries a finite auxiliary, keep its original tense/person.
        if any(x in {'som','sme','ste','budem','budeme','budeš','budete','mám','máme','musím','musíme','môžem','môžeme','chcem','chceme'} for x in parts):
            return (punct(cap(sk)), punct(cap(uk)))
        return (punct(cap(sk)), punct(cap(uk)))

    if low.endswith('osť'):
        return (f'To je {sk}.', f'Це {uk}.')
    if low in ADVERBS:
        return (f'{cap(sk)} to zvládnem.', f'{cap(uk)} я з цим упораюся.')
    if low in PLURAL_NOUNS:
        return (f'To sú {sk}.', f'Це {uk}.')
    if low in NEUTER_ADJ or low.endswith(('šie','nejšie')):
        return (f'Je to {sk}.', f'Це {uk}.')
    if low.endswith(('ť','ť?')):
        return (f'Chcem {sk}.', f'Я хочу {uk}.')
    if uk_low.startswith(('я ','ми ','він ','вона ','вони ')):
        return (punct(cap(sk)), punct(cap(uk)))
    # likely adjective/comparative; -ny covers rhythmic-law forms such as aktívny.
    if low.endswith(('ý','á','í','ny')):
        return (f'Je {sk}.', f'Він {uk}.')
    return (f'To je {sk}.', f'Це {uk}.')


def tok(s:str)->list[str]:
    return re.findall(r"[\wÀ-ž’'-]+|[,.!?;:]", s, flags=re.UNICODE)


def oid(lid, n): return f'{lid}-e{n:02d}'

def wids(words, inds): return [words[i]['id'] for i in inds]

def unique_other(words, idx, field='uk', n=2):
    base=words[idx][field]; out=[]
    for k in range(1,len(words)+1):
        v=words[(idx+k)%len(words)][field]
        if v != base and v not in out: out.append(v)
        if len(out)==n: break
    while len(out)<n: out.append('інший варіант' if field=='uk' else 'Dnes prší.')
    return out


def single_choice(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'uk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'single_choice','order':o,'skill':['vocabulary'],'question':f'Що означає «{w["sk"]}»?','difficulty':'easy','button':'Далі','wordIds':[w['id']], 'options':[{'id':'a','text':w['uk'],'correct':True},{'id':'b','text':ds[0],'correct':False},{'id':'c','text':ds[1],'correct':False}], 'explanation':{'uk':f'{w["sk"]} — «{w["uk"]}».'}}

def matching(lid,o,words,inds):
    return {'id':oid(lid,o),'lessonId':lid,'type':'matching','order':o,'skill':['vocabulary','reading'],'question':'З’єднай слова або фрази з точними значеннями.','difficulty':'easy','button':'Далі','wordIds':wids(words,inds),'pairs':[{'left':words[i]['sk'],'right':words[i]['uk']} for i in inds]}

def true_false(lid,o,words,idx,truth=True):
    w=words[idx]; shown=w['uk'] if truth else unique_other(words,idx,'uk',1)[0]
    return {'id':oid(lid,o),'lessonId':lid,'type':'true_false','order':o,'skill':['vocabulary'],'question':f'Правда чи ні? «{w["sk"]}» означає «{shown}».','difficulty':'easy','button':'Далі','wordIds':[w['id']],'statement':f'{w["sk"]} = {shown}','correctAnswer':truth,'explanation':{'uk':f'Правильне значення: {w["uk"]}.'}}

def fill_blank(lid,o,words,idx):
    w=words[idx]
    return {'id':oid(lid,o),'lessonId':lid,'type':'fill_blank','order':o,'skill':['writing'],'question':f'Впиши словацькою: «{w["uk"]}».','difficulty':'medium','button':'Далі','wordIds':[w['id']],'sentence':'______','acceptedAnswers':[w['sk']],'hint':{'uk':f'Початок: {w["sk"][:1]}…'},'explanation':{'uk':f'Правильно: {w["sk"]}.'}}

def dropdown(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'sk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'dropdown_blank','order':o,'skill':['writing'],'question':f'Обери точну словацьку одиницю для значення «{w["uk"]}».','difficulty':'medium','button':'Далі','wordIds':[w['id']],'sentenceParts':[{'text':''},{'blankId':'b1','options':[w['sk'],*ds],'correct':w['sk']},{'text':'.'}],'explanation':{'uk':f'Потрібний варіант: {w["sk"]}.'}}

def multiple_select(lid,o,words,inds):
    opts=[{'id':chr(97+k),'sk':words[i]['sk'],'correct':True} for k,i in enumerate(inds)]
    opts.append({'id':chr(97+len(opts)),'sk':'Dnes prší.','correct':False})
    return {'id':oid(lid,o),'lessonId':lid,'type':'multiple_select','order':o,'skill':['vocabulary'],'question':'Обери всі цільові одиниці цього уроку.','difficulty':'medium','button':'Далі','wordIds':wids(words,inds),'options':opts}

def sentence_order(lid,o,words,idx):
    w=words[idx]; t=tok(w['exampleSk']); scrambled=t[1:]+t[:1] if len(t)>2 else list(reversed(t))
    return {'id':oid(lid,o),'lessonId':lid,'type':'sentence_order','order':o,'skill':['writing'],'question':'Розташуй слова в природному порядку.','difficulty':'medium','button':'Далі','wordIds':[w['id']],'tokens':scrambled,'correctOrder':t,'context':{'uk':w['exampleUk']}}

def sentence_builder(lid,o,words,idx):
    w=words[idx]; t=tok(w['exampleSk']); scrambled=list(reversed(t))
    return {'id':oid(lid,o),'lessonId':lid,'type':'sentence_builder','order':o,'skill':['writing'],'question':'Склади словацьке речення за українським змістом.','difficulty':'medium','button':'Далі','wordIds':[w['id']],'tokens':scrambled,'correctSentence':w['exampleSk'],'context':{'uk':w['exampleUk']}}

def dialogue_choice(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'exampleSk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'dialogue_choose_reply','order':o,'skill':['dialogue','real_life'],'question':f'Яка репліка передає зміст «{w["exampleUk"]}»?','difficulty':'medium','button':'Далі','wordIds':[w['id']],'options':[{'id':'a','sk':w['exampleSk'],'correct':True},{'id':'b','sk':ds[0],'correct':False},{'id':'c','sk':ds[1],'correct':False}], 'explanation':{'uk':f'Природна відповідь: {w["exampleSk"]}'}}

def natural_phrase(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'exampleSk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'natural_phrase','order':o,'skill':['real_life'],'question':'Що тут сказати найприродніше?','difficulty':'medium','button':'Далі','wordIds':[w['id']],'situation':{'uk':f'Тобі потрібно передати зміст: «{w["exampleUk"]}».'},'options':[{'id':'a','sk':w['exampleSk'],'correct':True},{'id':'b','sk':ds[0],'correct':False},{'id':'c','sk':ds[1],'correct':False}], 'explanation':{'uk':f'Доречно: {w["exampleSk"]}'}}

def tf_list(lid,o,words,inds):
    sts=[]
    for k,i in enumerate(inds):
        truth=(k%2==0); shown=words[i]['uk'] if truth else unique_other(words,i,'uk',1)[0]
        sts.append({'sk':f'{words[i]["sk"]} = {shown}','correct':truth})
    return {'id':oid(lid,o),'lessonId':lid,'type':'true_false_list','order':o,'skill':['review'],'question':'Перевір кілька тверджень про значення.','difficulty':'hard','button':'Далі','wordIds':wids(words,inds),'statements':sts}

def reading(lid,o,words,inds):
    examples=[words[i]['exampleSk'] for i in inds]; answer=examples[0]
    return {'id':oid(lid,o),'lessonId':lid,'type':'reading_comprehension','order':o,'skill':['reading'],'question':'Прочитай короткий контекст і знайди точну інформацію.','difficulty':'hard','button':'Далі','wordIds':wids(words,inds),'text':' '.join(examples),'questions':[{'prompt':'Яке речення прямо є в тексті?','options':[{'id':'a','sk':answer,'correct':True},{'id':'b','sk':'Dnes prší.','correct':False},{'id':'c','sk':'Zajtra sneží.','correct':False}]}]}

def word_bank(lid,o,words,inds):
    vals=[words[i]['sk'] for i in inds]
    return {'id':oid(lid,o),'lessonId':lid,'type':'word_bank','order':o,'skill':['writing'],'question':'Заповни пропуски словами з банку.','difficulty':'medium','button':'Далі','wordIds':wids(words,inds),'items':[{'sentence':'______','correct':v} for v in vals],'wordBank':vals,'extraWords':[]}

def transformation(lid,o,words,idx):
    w=words[idx]
    return {'id':oid(lid,o),'lessonId':lid,'type':'transformation','order':o,'skill':['writing','transfer'],'question':'Передай цей зміст словацькою, використавши модель уроку.','difficulty':'hard','button':'Далі','wordIds':[w['id']],'prompt':{'uk':w['exampleUk']},'acceptedAnswers':[w['exampleSk']],'explanation':{'uk':w['exampleSk']}}

def meaning_context(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'uk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'meaning_in_context','order':o,'skill':['reading','vocabulary'],'question':f'Що означає виділена одиниця в контексті: «{w["exampleSk"]}»?','difficulty':'medium','button':'Далі','wordIds':[w['id']],'context':{'sk':w['exampleSk']},'options':[{'id':'a','text':w['uk'],'correct':True},{'id':'b','text':ds[0],'correct':False},{'id':'c','text':ds[1],'correct':False}]}

def collocation(lid,o,words,inds):
    return {'id':oid(lid,o),'lessonId':lid,'type':'collocation','order':o,'skill':['vocabulary'],'question':'З’єднай цільову одиницю з її значенням.','difficulty':'medium','button':'Далі','wordIds':wids(words,inds),'pairs':[{'left':words[i]['sk'],'right':words[i]['uk']} for i in inds]}

def dialogue_order(lid,o,words,inds):
    lines=[]; order=[]
    for k,i in enumerate(inds,1):
        xid=f'l{k}'; order.append(xid); lines.append({'id':xid,'speaker':'A' if k%2 else 'B','sk':words[i]['exampleSk']})
    return {'id':oid(lid,o),'lessonId':lid,'type':'dialogue_order','order':o,'skill':['dialogue'],'question':'Розташуй репліки в логічній послідовності.','difficulty':'hard','button':'Далі','wordIds':wids(words,inds),'lines':lines,'correctOrder':order}

def real_message(lid,o,words,idx):
    w=words[idx]; ds=unique_other(words,idx,'exampleSk')
    return {'id':oid(lid,o),'lessonId':lid,'type':'real_message','order':o,'skill':['reading','real_life'],'question':'Яка відповідь точно передає потрібний зміст повідомлення?','difficulty':'medium','button':'Далі','wordIds':[w['id']],'message':{'sender':'Marek','text':w['exampleSk']},'options':[{'id':'a','sk':w['exampleSk'],'correct':True},{'id':'b','sk':ds[0],'correct':False},{'id':'c','sk':ds[1],'correct':False}]}

PROFILES=[
['matching','single','tf','fill','drop','multi','order','build','dialogue','natural','tflist','reading','bank','transform'],
['single','matching','meaning','fill','bank','build','tf','dialogue_order','natural','multi','drop','reading','collocation','transform'],
['matching','collocation','single','tflist','fill','order','meaning','multi','dialogue','bank','natural','reading','transform','tf'],
['single','real_message','matching','fill','drop','build','collocation','dialogue_order','multi','natural','tf','reading','bank','transform'],
['matching','single','bank','meaning','tf','order','drop','multi','dialogue','natural','reading','transform','collocation','tflist'],
]

def build_exercises(lid:str, words:list[dict], variant:int)->list[dict]:
    prof=PROFILES[variant%len(PROFILES)]; n=len(words); out=[]
    for o,kind in enumerate(prof,1):
        i=(o+variant)%n; inds=[(i+k)%n for k in range(min(3,n))]
        inds4=[(i+k)%n for k in range(min(4,n))]
        if kind=='single': x=single_choice(lid,o,words,i)
        elif kind=='matching': x=matching(lid,o,words,inds4)
        elif kind=='tf': x=true_false(lid,o,words,i,truth=(o+variant)%2==0)
        elif kind=='fill': x=fill_blank(lid,o,words,i)
        elif kind=='drop': x=dropdown(lid,o,words,i)
        elif kind=='multi': x=multiple_select(lid,o,words,inds[:2])
        elif kind=='order': x=sentence_order(lid,o,words,i)
        elif kind=='build': x=sentence_builder(lid,o,words,i)
        elif kind=='dialogue': x=dialogue_choice(lid,o,words,i)
        elif kind=='natural': x=natural_phrase(lid,o,words,i)
        elif kind=='tflist': x=tf_list(lid,o,words,inds)
        elif kind=='reading': x=reading(lid,o,words,inds)
        elif kind=='bank': x=word_bank(lid,o,words,inds[:2])
        elif kind=='transform': x=transformation(lid,o,words,i)
        elif kind=='meaning': x=meaning_context(lid,o,words,i)
        elif kind=='collocation': x=collocation(lid,o,words,inds)
        elif kind=='dialogue_order': x=dialogue_order(lid,o,words,inds)
        elif kind=='real_message': x=real_message(lid,o,words,i)
        else: raise AssertionError(kind)
        out.append(x)
    return out


def slug(s:str)->str:
    return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_') or 'a2'


def build_lesson(plan:PlanLesson, copy:LessonCopy, owned:Sequence[OwnedTarget], next_id:str|None)->dict:
    lid=plan.lesson_id; words=[]
    for k,t in enumerate(owned,1):
        ex_sk,ex_uk=example_for(t.sk,t.uk)
        words.append({'id':f'{lid}-w{k:02d}','sk':t.sk,'uk':t.uk,'pronunciationUk':pron(t.sk),'exampleSk':ex_sk,'exampleUk':ex_uk,'level':'A2','topic':plan.title,'tags':[f'a2_s{plan.section:02d}',f'ownership:{t.status.lower()}'],'partOfSpeech':'phrase','ownership':t.status})
    assert words, lid
    groups=[list(range(0,min(3,len(words)))), list(range(min(3,len(words)),min(6,len(words)))), list(range(max(0,len(words)-3),len(words)))]
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
    steps=[]
    model_sks=[model[0] for model in profile.models]
    if len(set(model_sks)) != 3:
        raise ValueError(f'{lid}: semantic final models must be distinct')
    for idx,(prompt,(model_sk,_model_uk)) in enumerate(zip(profile.prompts_uk,profile.models),1):
        distractors=[sk for j,sk in enumerate(model_sks) if j != idx-1]
        steps.append({'id':f'f{idx}','prompt':{'uk':prompt},'options':[{'sk':model_sk,'correct':True},{'sk':distractors[0],'correct':False},{'sk':distractors[1],'correct':False}]})
    new_ids=[w['id'] for w in words if w['ownership']=='NEW']
    lesson={
      'id':lid,'sectionId':f'a2_s{plan.section:02d}','level':'A2','title':{'sk':plan.title,'uk':copy.title_uk},'topic':{'sk':plan.title,'uk':copy.title_uk},
      'description':{'sk':f'V tejto lekcii si precvičíš tému „{plan.title}“ v každodenných situáciách.','uk':copy.intent_uk},'order':plan.order,'xpReward':120,'estimatedMinutes':34,'isPublished':False,
      'intro':{'sk':f'Precvič si tému „{plan.title}“ krok za krokom.','uk':copy.intent_uk},'completionMessage':{'sk':'Výborne. Pokračuj v prenose do reálnych situácií.','uk':'Чудово. Тепер перенеси ці моделі у власні реальні ситуації.'},
      'updatedAt':NOW,'localization':{'uiLanguages':['uk'],'targetLanguage':'sk','fallbackUiLanguage':'uk'},'assets':{'images':{},'audio':{}},
      'startScreen':{'screenType':'lesson_start','title':{'sk':plan.title,'uk':copy.title_uk},'shortDescription':{'uk':copy.intent_uk},'outcomes':[f'використовувати цільові слова й фрази теми «{copy.title_uk}»','розуміти їх у короткому контексті','застосувати їх у реальній мініситуації'],'newWords':new_ids,'exercisesCount':14,'reward':'+120 XP','estimatedMinutes':34,'button':'Почати урок'},
      'theoryScreens':theory,
      'wordsScreen':{'screenType':'lesson_words','title':{'uk':'Цільові слова й фрази'},'description':{'uk':'NEW — нове для A2; REVIEW/TRANSFER/MASTERY — свідоме повторення й перенесення вже відомого матеріалу.'},'items':[{'wordId':w['id'],'sk':w['sk'],'uk':w['uk'],'pronunciationUk':w['pronunciationUk'],'exampleSk':w['exampleSk'],'exampleUk':w['exampleUk'],'ownership':w['ownership']} for w in words],'button':'До практики'},
      'words':words,'exercises':exercises,
      'finalSituation':{'id':'final-situation','type':'interactive_scenario','title':{'uk':f'{copy.title_uk}: мініситуація'},'description':{'uk':copy.intent_uk},'steps':steps,'passRequirement':'3/3','successMessage':{'uk':'Готово: ти застосував матеріал уроку в новій ситуації.'}},
      'resultScreen':{'screenType':'lesson_result','title':{'uk':'Урок завершено'},'subtitle':{'uk':'Ти завершив ще один крок рівня A2.'},'xpReward':120,'newWordsCount':len(new_ids),'exercisesCompleted':14,'nowYouKnow':[f'говорити на тему «{copy.title_uk}»','розуміти ключові моделі в контексті','переносити їх у коротку реальну ситуацію'],'mistakesMessage':{'uk':'Повтори лише ті місця, де відповідь ще не стала автоматичною.'},'buttons':['Продовжити','Повторити урок','Тренувати помилки'],'skills':[{'id':'vocabulary','label':{'uk':'лексика'},'weight':0.25},{'id':'grammar','label':{'uk':'структури'},'weight':0.3},{'id':'communication','label':{'uk':'комунікація'},'weight':0.45}]}
    }
    if next_id is not None: lesson['resultScreen']['nextLesson']={'id':next_id}
    return {'lessons':[lesson]}


def write_lessons(rows:Sequence[tuple[PlanLesson,LessonCopy,Sequence[OwnedTarget]]], out_dir:Path, all_ids:Sequence[str]) -> list[Path]:
    out_dir.mkdir(parents=True,exist_ok=True); paths=[]
    next_map={all_ids[i]:all_ids[i+1] for i in range(len(all_ids)-1)}
    for plan,copy,owned in rows:
        doc=build_lesson(plan,copy,owned,next_map.get(plan.lesson_id))
        p=out_dir/f'{plan.lesson_id}.json'; p.write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8'); paths.append(p)
    return paths
