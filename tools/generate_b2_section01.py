#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "lessons" / "b2"
UPDATED_AT = "2026-09-14T00:00:00Z"


def loc(sk: str, uk: str, ru: str, en: str) -> dict[str, str]:
    return {"sk": sk, "uk": uk, "ru": ru, "en": en}


def l10n(uk: str, ru: str, en: str) -> dict[str, str]:
    return {"uk": uk, "ru": ru, "en": en}


def pron(sk: str) -> str:
    mapping = {"á": "а", "ä": "е", "č": "ч", "ď": "дь", "é": "е", "í": "і", "ľ": "ль", "ĺ": "л", "ň": "нь", "ó": "о", "ô": "уо", "ŕ": "р", "š": "ш", "ť": "ть", "ú": "у", "ý": "и", "ž": "ж"}
    out = sk.lower()
    for src, dst in mapping.items():
        out = out.replace(src, dst)
    return out


LESSONS = [
    {
        "n": 1,
        "title": "Ako to myslíš?",
        "topic": "уточнення сенсу й наміру співрозмовника",
        "goal": "навчитися не губитися, коли фраза звучить двозначно: уточнити, чи людина говорить буквально, натякає або просто формулює нечітко.",
        "scenario": "Колега написав коротке повідомлення, яке можна зрозуміти двома способами. Потрібно зберегти тон і уточнити зміст.",
        "words": [
            ("myslieť tým", "мати цим на увазі", "иметь этим в виду", "to mean by that", "Čo tým presne myslíš?", "Що саме ти цим маєш на увазі?"),
            ("chápať", "розуміти", "понимать", "to understand", "Chápem to správne?", "Я правильно це розумію?"),
            ("chápanie", "розуміння", "понимание", "understanding", "Moje chápanie situácie je trochu iné.", "Моє розуміння ситуації трохи інше."),
            ("narážka", "натяк, колючий натяк", "намёк, колкий намёк", "hint, pointed remark", "Bola to narážka na včerajší problém?", "Це був натяк на вчорашню проблему?"),
            ("naznačiť", "натякнути", "намекнуть", "to imply", "Chcel si naznačiť, že máme zmeniť plán?", "Ти хотів натякнути, що нам треба змінити план?"),
            ("doslova", "буквально", "буквально", "literally", "Myslíš to doslova alebo obrazne?", "Ти маєш це на увазі буквально чи образно?"),
            ("v prenesenom zmysle", "у переносному значенні", "в переносном смысле", "figuratively", "Povedala to v prenesenom zmysle.", "Вона сказала це в переносному значенні."),
            ("pointa", "суть, головна думка", "суть, главная мысль", "main point", "Pointa je, že potrebujeme viac času.", "Суть у тому, що нам потрібно більше часу."),
        ],
    },
    {
        "n": 2,
        "title": "Záleží na tom",
        "topic": "умови, залежність від ситуації й важливі фактори",
        "goal": "говорити не чорно-біло, а з умовами: від чого залежить рішення, що є суттєвим і що другорядним.",
        "scenario": "Друг питає, чи варто приймати пропозицію. Потрібно пояснити, що відповідь залежить від умов.",
        "words": [
            ("záležať na", "залежати від / бути важливим", "зависеть от / быть важным", "to depend on / to matter", "Záleží na tom, koľko času máme.", "Це залежить від того, скільки часу ми маємо."),
            ("závisieť od", "залежати від", "зависеть от", "to depend on", "Výsledok závisí od dohody.", "Результат залежить від домовленості."),
            ("v závislosti od", "залежно від", "в зависимости от", "depending on", "Cena sa mení v závislosti od rozsahu.", "Ціна змінюється залежно від обсягу."),
            ("podmienka", "умова", "условие", "condition", "Hlavná podmienka je jasný termín.", "Головна умова - чіткий термін."),
            ("okolnosť", "обставина", "обстоятельство", "circumstance", "Za týchto okolností je to rozumné.", "За цих обставин це розумно."),
            ("situácia", "ситуація", "ситуация", "situation", "Situácia sa môže rýchlo zmeniť.", "Ситуація може швидко змінитися."),
            ("rozhodujúci", "вирішальний", "решающий", "decisive", "Rozhodujúci bude čas.", "Вирішальним буде час."),
            ("podstatný", "суттєвий", "существенный", "substantial, essential", "To je podstatný rozdiel.", "Це суттєва різниця."),
        ],
    },
    {
        "n": 3,
        "title": "To nie je celkom pravda",
        "topic": "м'яке заперечення, корекція й точніше формулювання",
        "goal": "не ламати розмову прямим конфліктом, а коректно показати, що твердження неточне або лише частково правильне.",
        "scenario": "На зустрічі хтось спростив проблему. Потрібно ввічливо уточнити, що реальність складніша.",
        "words": [
            ("nesúhlasiť", "не погоджуватися", "не соглашаться", "to disagree", "S tým úplne nesúhlasím.", "З цим я не повністю погоджуюся."),
            ("čiastočne", "частково", "частично", "partly", "Čiastočne máš pravdu.", "Частково ти маєш рацію."),
            ("celkom", "повністю / зовсім", "полностью / совсем", "completely / quite", "To nie je celkom presné.", "Це не зовсім точно."),
            ("presne", "точно", "точно", "exactly", "Presne o to mi ide.", "Саме це я маю на увазі."),
            ("opraviť", "виправити", "исправить", "to correct", "Dovoľ mi to trochu opraviť.", "Дозволь мені це трохи виправити."),
            ("upresniť", "уточнити", "уточнить", "to clarify", "Chcem to upresniť, aby nevznikol omyl.", "Хочу це уточнити, щоб не виникла помилка."),
            ("tvrdenie", "твердження", "утверждение", "claim, statement", "Toto tvrdenie je príliš všeobecné.", "Це твердження занадто загальне."),
            ("pohľad", "погляд, точка зору", "взгляд, точка зрения", "viewpoint", "Z môjho pohľadu je problém inde.", "З моєї точки зору проблема в іншому."),
        ],
    },
    {
        "n": 4,
        "title": "Ako reagovať slušne",
        "topic": "ввічлива реакція в напружених або чутливих ситуаціях",
        "goal": "реагувати спокійно, поважно й достатньо прямо, коли тема незручна або людина може образитися.",
        "scenario": "Клієнт або знайомий різко коментує ситуацію. Потрібно відповісти без агресії і без втрати меж.",
        "words": [
            ("slušne", "ввічливо", "вежливо", "politely", "Odpoviem slušne, ale jasne.", "Я відповім ввічливо, але чітко."),
            ("zdvorilo", "чемно, ввічливо", "учтиво, вежливо", "courteously", "Zdvorilo som vysvetlil svoj pohľad.", "Я чемно пояснив свою точку зору."),
            ("vhodné", "доречно", "уместно", "appropriate", "V tejto situácii to nie je vhodné.", "У цій ситуації це недоречно."),
            ("nevhodné", "недоречно", "неуместно", "inappropriate", "Tá poznámka bola nevhodná.", "Ця репліка була недоречною."),
            ("uraziť", "образити", "обидеть", "to offend", "Nechcem ťa uraziť.", "Я не хочу тебе образити."),
            ("rešpektovať", "поважати", "уважать", "to respect", "Rešpektujem tvoj názor.", "Я поважаю твою думку."),
            ("reagovať", "реагувати", "реагировать", "to react", "Skúsim reagovať pokojne.", "Спробую реагувати спокійно."),
            ("ohľaduplný", "тактовний, уважний до інших", "тактичный, внимательный к другим", "considerate", "Ohľaduplná reakcia pomôže udržať rozhovor.", "Тактовна реакція допоможе зберегти розмову."),
        ],
    },
    {
        "n": 5,
        "title": "Medzi riadkami",
        "topic": "підтекст, тон і непряме значення",
        "goal": "читати не лише слова, а й тон: помічати непрямий зміст у повідомленнях, побутових діалогах і коротких репліках.",
        "scenario": "Отримав повідомлення, де прямо нічого не сказано, але тон натякає на проблему. Потрібно правильно інтерпретувати і не перебільшити.",
        "words": [
            ("medzi riadkami", "між рядками, підтекст", "между строк, подтекст", "between the lines", "Treba čítať aj medzi riadkami.", "Треба читати також між рядками."),
            ("nepriamo", "непрямо", "непрямо", "indirectly", "Povedal to nepriamo.", "Він сказав це непрямо."),
            ("náznak", "натяк", "намёк", "hint", "V správe bol jasný náznak nespokojnosti.", "У повідомленні був чіткий натяк на невдоволення."),
            ("tón", "тон", "тон", "tone", "Tón správy bol dosť chladný.", "Тон повідомлення був досить холодний."),
            ("vyjadrenie", "висловлювання, формулювання", "высказывание, формулировка", "expression, statement", "To vyjadrenie môže znieť tvrdo.", "Це формулювання може звучати жорстко."),
            ("narážka", "натяк, непряма репліка", "намёк, непрямая реплика", "allusion, pointed remark", "Nebola to kritika, skôr narážka.", "Це була не критика, радше натяк."),
            ("pochopiť", "зрозуміти", "понять", "to understand", "Chcem pochopiť, čo tým myslíš.", "Я хочу зрозуміти, що ти цим маєш на увазі."),
            ("interpretovať", "інтерпретувати", "интерпретировать", "to interpret", "Možno to interpretujem nesprávne.", "Можливо, я це неправильно інтерпретую."),
        ],
    },
    {
        "n": 6,
        "title": "Sociálne situácie v praxi",
        "topic": "інтеграція уточнення, незгоди, ввічливості й інтерпретації",
        "goal": "поєднати все з першої секції: уточнити сенс, ввічливо не погодитися, прочитати тон і завершити розмову конструктивно.",
        "scenario": "У груповому чаті виникло непорозуміння. Потрібно зупинити конфлікт і повернути розмову до рішення.",
        "words": [
            ("reagovať primerane", "реагувати відповідно до ситуації", "реагировать уместно", "to react appropriately", "Treba reagovať primerane, nie útočne.", "Треба реагувати доречно, не нападати."),
            ("vyjadriť sa", "висловитися", "высказаться", "to express oneself", "Chcem sa k tomu jasne vyjadriť.", "Хочу чітко щодо цього висловитися."),
            ("zachovať pokoj", "зберегти спокій", "сохранить спокойствие", "to stay calm", "Aj pri kritike sa dá zachovať pokoj.", "Навіть під час критики можна зберегти спокій."),
            ("ujasniť si", "прояснити для себе", "прояснить для себя", "to clarify for oneself", "Najprv si ujasnime, čo sa stalo.", "Спочатку прояснімо, що сталося."),
            ("zareagovať", "відреагувати", "отреагировать", "to respond", "Skúsim zareagovať vecne.", "Спробую відреагувати по суті."),
            ("vysvetliť svoj postoj", "пояснити свою позицію", "объяснить свою позицию", "to explain one's position", "Potrebujem vysvetliť svoj postoj.", "Мені потрібно пояснити свою позицію."),
            ("zhrnúť dohodu", "підсумувати домовленість", "подытожить договорённость", "to summarize an agreement", "Na konci zhrniem dohodu.", "Наприкінці я підсумую домовленість."),
            ("predísť nedorozumeniu", "запобігти непорозумінню", "предотвратить недоразумение", "to prevent misunderstanding", "Presná otázka môže predísť nedorozumeniu.", "Точне питання може запобігти непорозумінню."),
        ],
    },
]

RU_TOPIC = {
    1: "уточнение смысла и намерения собеседника",
    2: "условия, зависимость от ситуации и важные факторы",
    3: "мягкое несогласие, коррекция и точная формулировка",
    4: "вежливая реакция в напряженных ситуациях",
    5: "подтекст, тон и непрямой смысл",
    6: "интеграция уточнения, несогласия, вежливости и интерпретации",
}

EN_TOPIC = {
    1: "clarifying meaning and speaker intention",
    2: "conditions, dependence on context and key factors",
    3: "soft disagreement, correction and precise wording",
    4: "polite responses in sensitive situations",
    5: "subtext, tone and indirect meaning",
    6: "integrating clarification, disagreement, politeness and interpretation",
}

UK_GOAL = {
    1: "навчитися уточнювати двозначну фразу без конфлікту",
    2: "пояснювати, від яких умов залежить рішення",
    3: "коректно показувати, що твердження неточне або часткове",
    4: "відповідати ввічливо й прямо у чутливій ситуації",
    5: "помічати підтекст і тон у повідомленнях",
    6: "поєднувати уточнення, незгоду, ввічливість і конструктивний фінал",
}

RU_GOAL = {
    1: "научиться уточнять двусмысленную фразу без конфликта",
    2: "объяснять, от каких условий зависит решение",
    3: "корректно показывать, что утверждение неточное или частичное",
    4: "отвечать вежливо и прямо в чувствительной ситуации",
    5: "замечать подтекст и тон в сообщениях",
    6: "соединять уточнение, несогласие, вежливость и конструктивное завершение",
}

EN_GOAL = {
    1: "learn to clarify an ambiguous phrase without conflict",
    2: "explain which conditions a decision depends on",
    3: "politely show that a claim is imprecise or only partly true",
    4: "respond politely and clearly in a sensitive situation",
    5: "notice subtext and tone in messages",
    6: "combine clarification, disagreement, politeness and a constructive close",
}

RU_SCENARIO = {
    1: "Сообщение можно понять двумя способами. Нужно спокойно уточнить смысл.",
    2: "Ответ зависит от условий. Нужно объяснить, что важно, а что второстепенно.",
    3: "Кто-то упростил проблему. Нужно мягко уточнить реальную картину.",
    4: "Реплика звучит резко. Нужно ответить без агрессии и без потери границ.",
    5: "В сообщении есть подтекст. Нужно правильно понять тон и не преувеличить.",
    6: "В чате возникло недоразумение. Нужно вернуть разговор к решению.",
}

EN_SCENARIO = {
    1: "A message can be understood in two ways. Clarify the meaning calmly.",
    2: "The answer depends on conditions. Explain what matters and what is secondary.",
    3: "Someone oversimplified a problem. Clarify the real situation politely.",
    4: "A remark sounds sharp. Respond without aggression while keeping boundaries.",
    5: "A message has subtext. Interpret the tone without overreacting.",
    6: "A group chat has a misunderstanding. Bring the conversation back to a solution.",
}


def make_word(lesson_id: str, idx: int, row: tuple[str, str, str, str, str, str], title: str) -> dict[str, object]:
    sk, uk, ru, en, ex_sk, ex_uk = row
    return {
        "id": f"{lesson_id}-w{idx:02d}",
        "sk": sk,
        "uk": uk,
        "ru": ru,
        "en": en,
        "pronunciationUk": pron(sk),
        "exampleSk": ex_sk,
        "exampleUk": ex_uk,
        "exampleRu": ex_uk,
        "exampleEn": en,
        "level": "B2",
        "topic": title,
        "tags": ["b2_s01", "nuance", "social-interaction", "ownership:new"],
        "ownership": "NEW",
    }


def option_text(w: dict[str, object]) -> dict[str, str]:
    return {"uk": str(w["uk"]), "ru": str(w["ru"]), "en": str(w["en"])}


def exercises(lid: str, title: str, goal: str, words: list[dict[str, object]]) -> list[dict[str, object]]:
    w = words
    return [
        {"id": f"{lid}-e01", "lessonId": lid, "type": "single_choice", "order": 1, "question": f"Що означає «{w[0]['sk']}»?", "questionLocalized": l10n(f"Що означає «{w[0]['sk']}»?", f"Что означает «{w[0]['sk']}»?", f"What does “{w[0]['sk']}” mean?"), "wordIds": [w[0]["id"]], "options": [{"id": "a", "text": option_text(w[0]), "correct": True}, {"id": "b", "text": option_text(w[3]), "correct": False}, {"id": "c", "text": option_text(w[6]), "correct": False}]},
        {"id": f"{lid}-e02", "lessonId": lid, "type": "matching", "order": 2, "question": "З'єднай словацькі фрази з точним значенням.", "questionLocalized": l10n("З'єднай словацькі фрази з точним значенням.", "Соедини словацкие фразы с точным значением.", "Match the Slovak phrases with their exact meaning."), "wordIds": [x["id"] for x in w[:4]], "pairs": [{"left": x["sk"], "right": x["uk"], "rightRu": x["ru"], "rightEn": x["en"]} for x in w[:4]]},
        {"id": f"{lid}-e03", "lessonId": lid, "type": "meaning_in_context", "order": 3, "question": f"Що найкраще підходить до контексту «{title}»?", "questionLocalized": l10n(f"Що найкраще підходить до контексту «{title}»?", f"Что лучше всего подходит к контексту «{title}»?", f"What best fits the context “{title}”?"), "wordIds": [w[1]["id"]], "context": {"sk": f"Nechcem reagovať automaticky. Najprv potrebujem {w[1]['sk']} situáciu."}, "options": [{"id": "a", "text": option_text(w[1]), "correct": True}, {"id": "b", "text": option_text(w[4]), "correct": False}, {"id": "c", "text": option_text(w[7]), "correct": False}]},
        {"id": f"{lid}-e04", "lessonId": lid, "type": "fill_blank", "order": 4, "question": f"Впиши словацькою: {w[2]['uk']}.", "questionLocalized": l10n(f"Впиши словацькою: {w[2]['uk']}.", f"Впиши по-словацки: {w[2]['ru']}.", f"Write in Slovak: {w[2]['en']}."), "wordIds": [w[2]["id"]], "sentence": "______", "acceptedAnswers": [w[2]["sk"]], "hint": l10n(f"Початок: {str(w[2]['sk'])[:2]}...", f"Начало: {str(w[2]['sk'])[:2]}...", f"Start: {str(w[2]['sk'])[:2]}...")},
        {"id": f"{lid}-e05", "lessonId": lid, "type": "dropdown_blank", "order": 5, "question": "Обери природну фразу для речення.", "questionLocalized": l10n("Обери природну фразу для речення.", "Выбери естественную фразу для предложения.", "Choose the natural phrase for the sentence."), "wordIds": [w[3]["id"]], "sentenceParts": [{"text": "V tejto poznámke cítim "}, {"blankId": "blank1", "options": [w[3]["sk"], w[0]["sk"], w[5]["sk"]], "correct": w[3]["sk"]}, {"text": ", preto sa radšej spýtam."}]},
        {"id": f"{lid}-e06", "lessonId": lid, "type": "sentence_builder", "order": 6, "question": "Склади B2-речення з уточненням.", "questionLocalized": l10n("Склади B2-речення з уточненням.", "Собери B2-предложение с уточнением.", "Build a B2 sentence with clarification."), "wordIds": [w[4]["id"]], "tokens": ["Nechcem", "to", "zle", "pochopiť,", "môžeš", "to", "upresniť?"], "correctSentence": "Nechcem to zle pochopiť, môžeš to upresniť?"},
        {"id": f"{lid}-e07", "lessonId": lid, "type": "multiple_select", "order": 7, "question": "Обери реакції, які зберігають ввічливий тон.", "questionLocalized": l10n("Обери реакції, які зберігають ввічливий тон.", "Выбери реакции, которые сохраняют вежливый тон.", "Select replies that keep a polite tone."), "wordIds": [w[5]["id"], w[6]["id"]], "options": [{"id": "a", "sk": "Chápem, ale potrebujem to trochu upresniť.", "correct": True}, {"id": "b", "sk": "To je hlúposť a nemá zmysel o tom hovoriť.", "correct": False}, {"id": "c", "sk": "Možno som to pochopil inak, vysvetlíš mi pointu?", "correct": True}]},
        {"id": f"{lid}-e08", "lessonId": lid, "type": "reading_comprehension", "order": 8, "question": "Прочитай повідомлення і знайди підтекст.", "questionLocalized": l10n("Прочитай повідомлення і знайди підтекст.", "Прочитай сообщение и найди подтекст.", "Read the message and identify the subtext."), "wordIds": [w[6]["id"], w[7]["id"]], "text": f"Správa znie neutrálne, ale {w[6]['sk']} naznačuje, že druhá strana čaká vysvetlenie. Pointa nie je útok, ale potreba vyjasniť situáciu.", "questions": [{"prompt": l10n("Яка головна думка тексту?", "Какая главная мысль текста?", "What is the main point of the text?"), "options": [{"id": "a", "sk": "Treba vyjasniť situáciu bez útoku.", "correct": True}, {"id": "b", "sk": "Treba okamžite ukončiť kontakt.", "correct": False}, {"id": "c", "sk": "Netreba reagovať vôbec.", "correct": False}]}]},
        {"id": f"{lid}-e09", "lessonId": lid, "type": "dialogue_choose_reply", "order": 9, "question": "Обери найкращу відповідь у чутливому діалозі.", "questionLocalized": l10n("Обери найкращу відповідь у чутливому діалозі.", "Выбери лучший ответ в чувствительном диалоге.", "Choose the best reply in a sensitive dialogue."), "wordIds": [w[0]["id"], w[7]["id"]], "dialogue": [{"speaker": "A", "sk": "Asi sme sa nepochopili."}], "options": [{"id": "a", "sk": f"Možno áno. Povedz mi, čo tým myslíš, aby som pochopil pointu.", "correct": True}, {"id": "b", "sk": "To je tvoj problém, nie môj.", "correct": False}, {"id": "c", "sk": "Nemám čas na také veci.", "correct": False}]},
        {"id": f"{lid}-e10", "lessonId": lid, "type": "natural_phrase", "order": 10, "question": "Що звучить найприродніше на рівні B2?", "questionLocalized": l10n("Що звучить найприродніше на рівні B2?", "Что звучит естественнее всего на уровне B2?", "What sounds most natural at B2 level?"), "wordIds": [w[5]["id"]], "situation": l10n("Ти не впевнений, чи фразу сказали буквально.", "Ты не уверен, сказали ли фразу буквально.", "You are not sure whether the phrase was meant literally."), "options": [{"id": "a", "sk": "Myslíš to doslova, alebo skôr v prenesenom zmysle?", "correct": True}, {"id": "b", "sk": "Toto slovo je doslova stolička.", "correct": False}, {"id": "c", "sk": "Nič nepýtam, všetko viem.", "correct": False}]},
        {"id": f"{lid}-e11", "lessonId": lid, "type": "reverse_translation", "order": 11, "question": f"Обери словацький варіант для: {w[4]['uk']}.", "questionLocalized": l10n(f"Обери словацький варіант для: {w[4]['uk']}.", f"Выбери словацкий вариант для: {w[4]['ru']}.", f"Choose the Slovak item for: {w[4]['en']}."), "wordIds": [w[4]["id"]], "options": [w[4]["sk"], w[2]["sk"], w[1]["sk"]], "correctAnswer": w[4]["sk"]},
        {"id": f"{lid}-e12", "lessonId": lid, "type": "multiple_choice_translation", "order": 12, "question": f"Що відповідає словацькому «{w[7]['sk']}»?", "questionLocalized": l10n(f"Що відповідає словацькому «{w[7]['sk']}»?", f"Что соответствует словацкому «{w[7]['sk']}»?", f"What matches the Slovak “{w[7]['sk']}”?"), "wordIds": [w[7]["id"]], "options": [w[7]["uk"], w[0]["uk"], w[3]["uk"]], "correctAnswer": w[7]["uk"]},
    ]


def make_lesson(spec: dict[str, object], next_id: str) -> dict[str, object]:
    n = int(spec["n"])
    lid = f"b2-s01-l{n:03d}"
    title = str(spec["title"])
    desc = loc(
        f"Precvičíš si B2 komunikáciu: {spec['topic']}.",
        f"Тренуємо B2-комунікацію: {spec['goal']}",
        f"Тренируем B2-коммуникацию: {spec['goal']}",
        f"Practice B2 communication: {spec['topic']}.",
    )
    words = [make_word(lid, i, row, title) for i, row in enumerate(spec["words"], 1)]
    exs = exercises(lid, title, str(spec["goal"]), words)
    theory = [
        {"id": "t1", "screenType": "theory", "order": 1, "title": l10n("Навіщо це на B2", "Зачем это на B2", "Why this matters at B2"), "body": l10n(str(spec["goal"]), str(spec["goal"]), f"You learn to handle nuance: {spec['topic']}."), "examples": [{"sk": words[0]["exampleSk"], "translation": l10n(words[0]["exampleUk"], words[0]["exampleRu"], words[0]["exampleEn"])}, {"sk": words[1]["exampleSk"], "translation": l10n(words[1]["exampleUk"], words[1]["exampleRu"], words[1]["exampleEn"])}], "shortRule": l10n("B2 = не просто сказати фразу, а керувати тоном, підтекстом і наслідком.", "B2 = не просто сказать фразу, а управлять тоном, подтекстом и последствием.", "B2 means managing tone, implication and consequence."), "button": "Далі"},
        {"id": "t2", "screenType": "theory", "order": 2, "title": l10n("Робоча модель відповіді", "Рабочая модель ответа", "Response model"), "body": l10n("Будуй репліку так: визнай контекст -> уточни або скоригуй -> запропонуй наступний крок.", "Строй реплику так: признай контекст -> уточни или скорректируй -> предложи следующий шаг.", "Build the reply as: acknowledge context -> clarify or correct -> suggest a next step."), "examples": [{"sk": "Rozumiem, ako to myslíš, ale potrebujem to trochu upresniť.", "translation": l10n("Розумію, як ти це маєш на увазі, але мені треба це трохи уточнити.", "Понимаю, как ты это имеешь в виду, но мне нужно это немного уточнить.", "I understand what you mean, but I need to clarify it a bit.")}, {"sk": "Z môjho pohľadu je podstatné, aby sme zachovali pokoj.", "translation": l10n("З моєї точки зору суттєво, щоб ми зберегли спокій.", "С моей точки зрения важно, чтобы мы сохранили спокойствие.", "From my point of view, it is essential that we stay calm.")}], "shortRule": l10n("Спокійна точність звучить сильніше, ніж різке заперечення.", "Спокойная точность звучит сильнее, чем резкое отрицание.", "Calm precision is stronger than a sharp denial."), "button": "Далі"},
        {"id": "t3", "screenType": "theory", "order": 3, "title": l10n("Типова помилка", "Типичная ошибка", "Typical mistake"), "body": l10n("Не перекладай дослівно з української або російської. У словацькій часто природніше звучить коротша, м'якша фраза з уточненням.", "Не переводи дословно с украинского или русского. В словацком часто естественнее звучит более короткая и мягкая фраза с уточнением.", "Do not translate word for word. Slovak often prefers a shorter, softer clarifying phrase."), "examples": [{"sk": "Chápem. Môžeš mi povedať pointu?", "translation": l10n("Розумію. Можеш сказати головну думку?", "Понимаю. Можешь сказать главную мысль?", "I understand. Can you tell me the main point?")}, {"sk": "Nechcem to interpretovať nesprávne.", "translation": l10n("Не хочу інтерпретувати це неправильно.", "Не хочу интерпретировать это неправильно.", "I do not want to interpret it incorrectly.")}], "shortRule": l10n("Коли є ризик конфлікту, спочатку уточни.", "Когда есть риск конфликта, сначала уточни.", "When there is risk of conflict, clarify first."), "button": "До слів"},
    ]
    doc = {"lessons": [{
        "id": lid, "sectionId": "b2_s01", "level": "B2",
        "title": loc(title, title, title, title),
        "topic": loc(str(spec["topic"]), str(spec["topic"]), str(spec["topic"]), str(spec["topic"])),
        "description": desc, "order": n, "xpReward": 180, "estimatedMinutes": 32, "isPublished": False,
        "intro": desc,
        "completionMessage": loc("Výborne. Dokážeš reagovať presnejšie a pokojnejšie.", "Супер. Тепер ти можеш реагувати точніше й спокійніше.", "Отлично. Теперь ты можешь реагировать точнее и спокойнее.", "Great. You can now respond more precisely and calmly."),
        "updatedAt": UPDATED_AT,
        "localization": {"uiLanguages": ["uk", "ru", "en"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
        "assets": {"images": {}, "audio": {}},
        "startScreen": {"screenType": "lesson_start", "title": loc(title, title, title, title), "shortDescription": l10n(desc["uk"], desc["ru"], desc["en"]), "outcomes": [l10n("уточнювати сенс без конфлікту", "уточнять смысл без конфликта", "clarify meaning without conflict"), l10n("розрізняти буквальний і непрямий зміст", "различать буквальный и непрямой смысл", "distinguish literal and indirect meaning"), l10n("вибирати природну B2-реакцію", "выбирать естественную B2-реакцию", "choose a natural B2-level response")], "newWords": [x["id"] for x in words], "exercisesCount": len(exs), "reward": "+180 XP", "estimatedMinutes": 32, "button": "Почати урок"},
        "theoryScreens": theory,
        "wordsScreen": {"screenType": "lesson_words", "title": l10n("Ключові B2-фрази", "Ключевые B2-фразы", "Key B2 phrases"), "description": l10n("Ці слова потрібні для нюансованої соціальної комунікації.", "Эти слова нужны для нюансированной социальной коммуникации.", "These items support nuanced social communication."), "items": [{"wordId": x["id"], "sk": x["sk"], "uk": x["uk"], "ru": x["ru"], "en": x["en"], "pronunciationUk": x["pronunciationUk"], "exampleSk": x["exampleSk"], "exampleUk": x["exampleUk"], "exampleRu": x["exampleRu"], "exampleEn": x["exampleEn"]} for x in words], "button": "До практики"},
        "words": words, "exercises": exs,
        "finalSituation": {"id": "final-situation", "type": "interactive_scenario", "title": l10n(f"{title}: реальна розмова", f"{title}: реальный разговор", f"{title}: real conversation"), "description": l10n(str(spec["scenario"]), str(spec["scenario"]), "Choose replies that clarify meaning, keep the tone calm and move the conversation forward."), "steps": [{"id": "f1", "prompt": l10n("Повідомлення звучить двозначно. Перша реакція?", "Сообщение звучит двусмысленно. Первая реакция?", "The message sounds ambiguous. First response?"), "options": [{"sk": "Chcem si to najprv ujasniť, aby som nereagoval zle.", "correct": True}, {"sk": "Určite to myslíš zle.", "correct": False}, {"sk": "Nebudem sa pýtať nič.", "correct": False}]}, {"id": "f2", "prompt": l10n("Ти частково не погоджуєшся. Як сказати м'яко?", "Ты частично не согласен. Как сказать мягко?", "You partly disagree. How do you say it softly?"), "options": [{"sk": "Čiastočne rozumiem, ale z môjho pohľadu to nie je celkom presné.", "correct": True}, {"sk": "Nemáš pravdu a koniec.", "correct": False}, {"sk": "To ma nezaujíma.", "correct": False}]}, {"id": "f3", "prompt": l10n("Потрібно завершити розмову конструктивно.", "Нужно завершить разговор конструктивно.", "You need to close constructively."), "options": [{"sk": "Zhrňme si pointu a dohodnime sa na ďalšom kroku.", "correct": True}, {"sk": "Nechajme to tak navždy.", "correct": False}, {"sk": "Každý si myslí svoje, nič neriešme.", "correct": False}]}], "passRequirement": "3/3", "successMessage": l10n("Готово: ти впорався з нюансованою B2-ситуацією.", "Готово: ты справился с нюансированной B2-ситуацией.", "Done: you handled a nuanced B2 situation.")},
        "resultScreen": {"screenType": "lesson_result", "title": l10n("Урок завершено", "Урок завершён", "Lesson complete"), "subtitle": l10n("Ти закрив ще один крок B2-комунікації.", "Ты закрыл ещё один шаг B2-коммуникации.", "You completed another B2 communication step."), "xpReward": 180, "newWordsCount": len(words), "exercisesCompleted": len(exs), "nowYouKnow": ["уточнювати зміст", "реагувати ввічливо", "читати підтекст"], "mistakesMessage": l10n("Повтори вправи, де тон або зміст ще плутаються.", "Повтори упражнения, где тон или смысл ещё путаются.", "Repeat exercises where tone or meaning is still unclear."), "buttons": ["Продовжити", "Повторити урок", "Тренувати помилки"], "skills": [{"id": "nuance", "label": l10n("нюанс", "нюанс", "nuance"), "weight": 0.35}, {"id": "interaction", "label": l10n("діалог", "диалог", "interaction"), "weight": 0.35}, {"id": "transfer", "label": l10n("перенесення", "перенос", "transfer"), "weight": 0.3}], "nextLesson": {"id": next_id}},
    }]}
    clean_language(doc)
    return doc


def clean_language(doc: dict[str, object]) -> None:
    lesson = doc["lessons"][0]
    n = int(lesson["order"])
    title = lesson["title"]["sk"]
    lesson["topic"] = {"sk": title, "uk": lesson["topic"]["uk"], "ru": RU_TOPIC[n], "en": EN_TOPIC[n]}
    lesson["description"] = {
        "sk": f"Precvičíš si komunikáciu na úrovni B2: {title}.",
        "uk": f"Тренуємо B2-комунікацію: {UK_GOAL[n]}.",
        "ru": f"Тренируем B2-коммуникацию: {RU_GOAL[n]}.",
        "en": f"Practice B2 communication: {EN_GOAL[n]}.",
    }
    lesson["intro"] = dict(lesson["description"])
    lesson["startScreen"]["shortDescription"] = {
        "uk": lesson["description"]["uk"],
        "ru": lesson["description"]["ru"],
        "en": lesson["description"]["en"],
    }
    lesson["theoryScreens"][0]["body"] = {"uk": UK_GOAL[n] + ".", "ru": RU_GOAL[n] + ".", "en": EN_GOAL[n] + "."}
    lesson["finalSituation"]["description"]["ru"] = RU_SCENARIO[n]
    lesson["finalSituation"]["description"]["en"] = EN_SCENARIO[n]
    for word in lesson["words"]:
        if word.get("exampleRu") == word.get("exampleUk"):
            word["exampleRu"] = f"Пример: {word['ru']}."
        if word.get("exampleEn") == word.get("en"):
            word["exampleEn"] = f"Example phrase for: {word['en']}."
    words_by_id = {word["id"]: word for word in lesson["words"]}
    for item in lesson["wordsScreen"]["items"]:
        word = words_by_id[item["wordId"]]
        item["exampleRu"] = word["exampleRu"]
        item["exampleEn"] = word["exampleEn"]
    for exercise in lesson["exercises"]:
        if exercise["type"] == "meaning_in_context":
            exercise["context"] = {"sk": "Nechcem reagovať automaticky. Najprv potrebujem lepšie pochopiť situáciu."}
        if exercise["type"] == "reading_comprehension":
            exercise["text"] = "Správa znie neutrálne, ale jej tón naznačuje, že druhá strana čaká vysvetlenie. Pointa nie je útok, ale potreba vyjasniť situáciu."


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, spec in enumerate(LESSONS):
        next_id = f"b2-s01-l{i + 2:03d}" if i < len(LESSONS) - 1 else "b2-s02-l007"
        doc = make_lesson(spec, next_id)
        path = OUT / f"b2-s01-l{int(spec['n']):03d}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("# SlovakGo B2 Lessons\n\nSection 01 has 6 active lessons generated from `B2/LESSON_PLAN.md`.\n", encoding="utf-8")
    print(f"Generated {len(LESSONS)} B2 section 01 lessons in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
