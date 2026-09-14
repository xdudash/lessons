#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "C2" / "LESSON_PLAN.md"
OUT = ROOT / "lessons" / "c2"
UPDATED_AT = "2026-09-14T03:30:00Z"

SECTION_RE = re.compile(r"^## Section (\d{2}) — (.+)$")
LESSON_RE = re.compile(r"^### (\d{2,3})\. (.+)$")


def loc(sk: str, uk: str, ru: str, en: str) -> dict[str, str]:
    return {"sk": sk, "uk": uk, "ru": ru, "en": en}


def l10n(uk: str, ru: str, en: str) -> dict[str, str]:
    return {"uk": uk, "ru": ru, "en": en}


def pron(sk: str) -> str:
    mapping = {"á": "a", "ä": "e", "č": "ch", "ď": "d'", "é": "e", "í": "i", "ľ": "l'", "ĺ": "l", "ň": "n'", "ó": "o", "ô": "uo", "ŕ": "r", "š": "sh", "ť": "t'", "ú": "u", "ý": "y", "ž": "zh"}
    out = sk.lower()
    for src, dst in mapping.items():
        out = out.replace(src, dst)
    return out


def extract_lessons() -> list[dict[str, object]]:
    lessons: list[dict[str, object]] = []
    section: dict[str, object] | None = None
    current: dict[str, object] | None = None
    for raw in PLAN.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        sm = SECTION_RE.match(line)
        if sm:
            section = {"number": int(sm.group(1)), "title_en": sm.group(2)}
            current = None
            continue
        lm = LESSON_RE.match(line)
        if lm and section:
            current = {"number": int(lm.group(1)), "title_sk": lm.group(2), "section": section["number"], "section_title_en": section["title_en"]}
            lessons.append(current)
            continue
        if current and line.startswith("**Что будет:**"):
            current["what_ru"] = line.replace("**Что будет:**", "").strip()
        if current and line.startswith("**Новые слова/фразы:**"):
            current["words"] = [w.strip() for w in line.replace("**Новые слова/фразы:**", "").split(",") if w.strip()]
    if len(lessons) != 70:
        raise RuntimeError(f"Expected 70 C2 lessons, found {len(lessons)}")
    return lessons


TRANSLATIONS: dict[str, tuple[str, str, str]] = {
    "presný": ("точний", "точный", "precise"),
    "nepresný": ("неточний", "неточный", "imprecise"),
    "vhodný": ("доречний", "подходящий, уместный", "suitable, appropriate"),
    "nevhodný": ("недоречний", "неподходящий, неуместный", "unsuitable, inappropriate"),
    "výstižný": ("влучний, точний", "меткий, точный", "apt, concise and precise"),
    "presne povedané": ("точніше кажучи", "точнее говоря", "more precisely"),
    "inými slovami": ("іншими словами", "иными словами", "in other words"),
    "takmer": ("майже", "почти", "almost"),
    "formálny": ("формальний, офіційний", "формальный, официальный", "formal"),
    "neformálny": ("неформальний", "неформальный", "informal"),
    "neutrálny": ("нейтральний", "нейтральный", "neutral"),
    "zdvorilý": ("ввічливий", "вежливый", "polite"),
    "hovorový": ("розмовний", "разговорный", "colloquial"),
    "oficiálne": ("офіційно", "официально", "officially"),
    "medzi priateľmi": ("між друзями", "между друзьями", "among friends"),
    "v bežnej reči": ("у звичайному мовленні", "в обычной речи", "in everyday speech"),
    "rozdiel": ("різниця", "разница", "difference"),
    "odtieň": ("відтінок", "оттенок", "shade, nuance"),
    "význam": ("значення", "значение", "meaning"),
    "dôraz": ("наголос, акцент", "акцент, упор", "emphasis"),
    "prenesene": ("переносно", "переносно", "figuratively"),
    "implicitne": ("неявно", "неявно", "implicitly"),
    "znieť": ("звучати", "звучать", "to sound"),
    "pôsobiť": ("справляти враження", "производить впечатление", "to come across"),
    "vyznieť": ("прозвучати, сприйнятися", "прозвучать, восприняться", "to come across, to sound in effect"),
    "prirodzene": ("природно", "естественно", "naturally"),
    "stroho": ("сухо, стримано", "сухо, строго", "tersely"),
    "tvrdo": ("жорстко", "жестко", "harshly"),
    "jemne": ("м'яко, тонко", "мягко, тонко", "gently, subtly"),
    "nepríjemne": ("неприємно", "неприятно", "unpleasantly"),
    "kontextový dôraz": ("контекстний акцент", "контекстный акцент", "contextual emphasis"),
    "štýlová voľba": ("стилістичний вибір", "стилистический выбор", "stylistic choice"),
    "významový posun": ("зміщення значення", "сдвиг значения", "shift in meaning"),
    "jemná formulácia": ("м'яке формулювання", "мягкая формулировка", "subtle wording"),
    "presná reakcia": ("точна реакція", "точная реакция", "precise response"),
    "myslieť tým": ("мати цим на увазі", "иметь этим в виду", "to mean by that"),
    "chápať": ("розуміти", "понимать", "to understand"),
    "chápanie": ("розуміння", "понимание", "understanding"),
    "narážka": ("натяк", "намек", "hint, pointed remark"),
    "naznačiť": ("натякнути", "намекнуть", "to imply"),
    "doslova": ("буквально", "буквально", "literally"),
    "v prenesenom zmysle": ("у переносному значенні", "в переносном смысле", "figuratively"),
    "pointa": ("суть, головна думка", "суть, главная мысль", "main point"),
    "záležať na": ("залежати від / бути важливим", "зависеть от / быть важным", "to depend on / to matter"),
    "závisieť od": ("залежати від", "зависеть от", "to depend on"),
    "v závislosti od": ("залежно від", "в зависимости от", "depending on"),
    "podmienka": ("умова", "условие", "condition"),
    "okolnosť": ("обставина", "обстоятельство", "circumstance"),
    "situácia": ("ситуація", "ситуация", "situation"),
    "rozhodujúci": ("вирішальний", "решающий", "decisive"),
    "podstatný": ("суттєвий", "существенный", "essential"),
    "nesúhlasiť": ("не погоджуватися", "не соглашаться", "to disagree"),
    "čiastočne": ("частково", "частично", "partly"),
    "celkom": ("повністю / зовсім", "полностью / совсем", "completely / quite"),
    "presne": ("точно", "точно", "exactly"),
    "opraviť": ("виправити", "исправить", "to correct"),
    "upresniť": ("уточнити", "уточнить", "to clarify"),
    "tvrdenie": ("твердження", "утверждение", "claim"),
    "pohľad": ("погляд, точка зору", "взгляд, точка зрения", "viewpoint"),
    "slušne": ("ввічливо", "вежливо", "politely"),
    "zdvorilo": ("чемно, ввічливо", "учтиво, вежливо", "courteously"),
    "vhodné": ("доречно", "уместно", "appropriate"),
    "nevhodné": ("недоречно", "неуместно", "inappropriate"),
    "uraziť": ("образити", "обидеть", "to offend"),
    "rešpektovať": ("поважати", "уважать", "to respect"),
    "reagovať": ("реагувати", "реагировать", "to react"),
    "ohľaduplný": ("тактовний", "тактичный", "considerate"),
    "medzi riadkami": ("між рядками, підтекст", "между строк, подтекст", "between the lines"),
    "nepriamo": ("непрямо", "непрямо", "indirectly"),
    "náznak": ("натяк", "намек", "hint"),
    "tón": ("тон", "тон", "tone"),
    "vyjadrenie": ("висловлювання", "высказывание", "statement"),
    "pochopiť": ("зрозуміти", "понять", "to understand"),
    "interpretovať": ("інтерпретувати", "интерпретировать", "to interpret"),
}


def existing_translations() -> dict[str, tuple[str, str, str]]:
    found: dict[str, tuple[str, str, str]] = {}
    bad_fragments = ("вираз «", "выражение «", "the expression “", "словацьке слово/вираз", "словацкое слово/выражение", "praktická fráza")
    for lessons_dir in ("a1", "a2", "b1", "b2", "c1"):
        for path in (ROOT / "lessons" / lessons_dir).glob("*.json"):
            doc = json.loads(path.read_text(encoding="utf-8"))
            for lesson in doc.get("lessons", []):
                for word in lesson.get("words", []):
                    sk = word.get("sk")
                    if sk and all(word.get(k) for k in ("uk", "ru", "en")):
                        values = (word["uk"], word["ru"], word["en"])
                        if any(fragment in value for value in values for fragment in bad_fragments):
                            continue
                        found.setdefault(sk, (word["uk"], word["ru"], word["en"]))
    return found


TRANSLATIONS = existing_translations() | TRANSLATIONS


def tr(sk: str, title: str) -> tuple[str, str, str]:
    if sk in TRANSLATIONS:
        return TRANSLATIONS[sk]
    return (f"C2-поняття: {sk}", f"C2-понятие: {sk}", f"C2 concept: {sk}")


def make_words(lesson_id: str, lesson: dict[str, object]) -> list[dict[str, object]]:
    title = str(lesson["title_sk"])
    raw_words = list(lesson.get("words") or [])[:8]
    fallback_words = ["kontextový dôraz", "štýlová voľba", "významový posun", "jemná formulácia", "presná reakcia"]
    while len(raw_words) < 8:
        raw_words.append(fallback_words[len(raw_words) % len(fallback_words)])
    words = []
    for idx, sk in enumerate(raw_words, 1):
        uk, ru, en = tr(sk, title)
        words.append({
            "id": f"{lesson_id}-w{idx:02d}",
            "sk": sk,
            "uk": uk,
            "ru": ru,
            "en": en,
            "pronunciationUk": pron(sk),
            "exampleSk": f"V téme {title} použijem výraz: {sk}.",
            "exampleUk": f"У темі «{title}» використовую: {uk}.",
            "exampleRu": f"В теме «{title}» использую: {ru}.",
            "exampleEn": f"In “{title}”, I use: {en}.",
            "level": "C2",
            "topic": title,
            "tags": [str(lesson["section_id"]), "c2", "ownership:new"],
            "ownership": "NEW",
        })
    return words


def option_text(w: dict[str, object]) -> dict[str, str]:
    return {"uk": str(w["uk"]), "ru": str(w["ru"]), "en": str(w["en"])}


def make_exercises(lid: str, title: str, words: list[dict[str, object]]) -> list[dict[str, object]]:
    w = words
    return [
        {"id": f"{lid}-e01", "lessonId": lid, "type": "single_choice", "order": 1, "question": f"Що означає «{w[0]['sk']}»?", "questionLocalized": l10n(f"Що означає «{w[0]['sk']}»?", f"Что означает «{w[0]['sk']}»?", f"What does “{w[0]['sk']}” mean?"), "wordIds": [w[0]["id"]], "options": [{"id": "a", "text": option_text(w[0]), "correct": True}, {"id": "b", "text": option_text(w[1]), "correct": False}, {"id": "c", "text": option_text(w[2]), "correct": False}]},
        {"id": f"{lid}-e02", "lessonId": lid, "type": "matching", "order": 2, "question": "З'єднай фрази з поясненнями.", "questionLocalized": l10n("З'єднай фрази з поясненнями.", "Соедини фразы с объяснениями.", "Match phrases with explanations."), "wordIds": [x["id"] for x in w[:4]], "pairs": [{"left": x["sk"], "right": x["uk"], "rightRu": x["ru"], "rightEn": x["en"]} for x in w[:4]]},
        {"id": f"{lid}-e03", "lessonId": lid, "type": "fill_blank", "order": 3, "question": f"Впиши словацькою: {w[2]['uk']}.", "questionLocalized": l10n(f"Впиши словацькою: {w[2]['uk']}.", f"Впиши по-словацки: {w[2]['ru']}.", f"Write in Slovak: {w[2]['en']}."), "wordIds": [w[2]["id"]], "sentence": "______", "acceptedAnswers": [w[2]["sk"]], "hint": l10n(f"Початок: {str(w[2]['sk'])[:2]}...", f"Начало: {str(w[2]['sk'])[:2]}...", f"Start: {str(w[2]['sk'])[:2]}...")},
        {"id": f"{lid}-e04", "lessonId": lid, "type": "dropdown_blank", "order": 4, "question": "Обери точну фразу для C2-речення.", "questionLocalized": l10n("Обери точну фразу для C2-речення.", "Выбери точную фразу для C2-предложения.", "Choose the precise phrase for a C2 sentence."), "wordIds": [w[3]["id"]], "sentenceParts": [{"text": "V tejto situácii je dôležité použiť "}, {"blankId": "blank1", "options": [w[3]["sk"], w[0]["sk"], w[1]["sk"]], "correct": w[3]["sk"]}, {"text": "."}]},
        {"id": f"{lid}-e05", "lessonId": lid, "type": "sentence_builder", "order": 5, "question": "Склади природну словацьку репліку.", "questionLocalized": l10n("Склади природну словацьку репліку.", "Собери естественную словацкую реплику.", "Build a natural Slovak reply."), "wordIds": [w[4]["id"]], "tokens": ["Rozumiem", "situácii,", "ale", "potrebujem", "ju", "ešte", "upresniť."], "correctSentence": "Rozumiem situácii, ale potrebujem ju ešte upresniť."},
        {"id": f"{lid}-e06", "lessonId": lid, "type": "multiple_select", "order": 6, "question": "Обери C2-репліки з природним тоном.", "questionLocalized": l10n("Обери C2-репліки з природним тоном.", "Выбери C2-реплики с естественным тоном.", "Select C2 replies with a natural tone."), "wordIds": [w[0]["id"], w[5]["id"]], "options": [{"id": "a", "sk": "Rozumiem, ale potrebujem to presnejšie vysvetliť.", "correct": True}, {"id": "b", "sk": "To je úplne mimo a nemá zmysel hovoriť.", "correct": False}, {"id": "c", "sk": "Z môjho pohľadu je dôležitý aj kontext.", "correct": True}]},
        {"id": f"{lid}-e07", "lessonId": lid, "type": "reading_comprehension", "order": 7, "question": "Прочитай текст і вибери головну думку.", "questionLocalized": l10n("Прочитай текст і вибери головну думку.", "Прочитай текст и выбери главную мысль.", "Read the text and choose the main idea."), "wordIds": [x["id"] for x in w[5:8]], "text": f"Téma {title} si vyžaduje presnosť. Nestačí poznať slová; treba reagovať podľa kontextu, vysvetliť dôvod a navrhnúť ďalší krok.", "questions": [{"prompt": l10n("Що є головною думкою?", "Что является главной мыслью?", "What is the main idea?"), "options": [{"id": "a", "sk": "Treba reagovať presne podľa kontextu.", "correct": True}, {"id": "b", "sk": "Stačí opakovať jedno slovo.", "correct": False}, {"id": "c", "sk": "Najlepšie je nereagovať.", "correct": False}]}]},
        {"id": f"{lid}-e08", "lessonId": lid, "type": "dialogue_choose_reply", "order": 8, "question": "Обери найкращу відповідь у діалозі.", "questionLocalized": l10n("Обери найкращу відповідь у діалозі.", "Выбери лучший ответ в диалоге.", "Choose the best reply in the dialogue."), "wordIds": [w[6]["id"]], "dialogue": [{"speaker": "A", "sk": "Ako by si to vysvetlil?"}], "options": [{"id": "a", "sk": "Najprv zhrniem situáciu a potom poviem svoj návrh.", "correct": True}, {"id": "b", "sk": "Nepoviem nič, lebo je to ťažké.", "correct": False}, {"id": "c", "sk": "Odpoviem jedným náhodným slovom.", "correct": False}]},
        {"id": f"{lid}-e09", "lessonId": lid, "type": "meaning_in_context", "order": 9, "question": f"Що означає «{w[1]['sk']}» у контексті?", "questionLocalized": l10n(f"Що означає «{w[1]['sk']}» у контексті?", f"Что означает «{w[1]['sk']}» в контексте?", f"What does “{w[1]['sk']}” mean in context?"), "wordIds": [w[1]["id"]], "context": {"sk": "Rozhovor je citlivý, preto si najprv overím význam a tón."}, "options": [{"id": "a", "text": option_text(w[1]), "correct": True}, {"id": "b", "text": option_text(w[4]), "correct": False}, {"id": "c", "text": option_text(w[7]), "correct": False}]},
        {"id": f"{lid}-e10", "lessonId": lid, "type": "natural_phrase", "order": 10, "question": "Що звучить найприродніше?", "questionLocalized": l10n("Що звучить найприродніше?", "Что звучит естественнее всего?", "What sounds most natural?"), "wordIds": [w[7]["id"]], "situation": l10n("Потрібно відповісти точно, але без різкого тону.", "Нужно ответить точно, но без резкого тона.", "You need to answer precisely but without a sharp tone."), "options": [{"id": "a", "sk": "Chápem tvoj pohľad, ale doplnil by som ešte jednu vec.", "correct": True}, {"id": "b", "sk": "Ty ničomu nerozumieš.", "correct": False}, {"id": "c", "sk": "Áno nie možno včera.", "correct": False}]},
        {"id": f"{lid}-e11", "lessonId": lid, "type": "reverse_translation", "order": 11, "question": f"Обери словацький варіант для: {w[4]['uk']}.", "questionLocalized": l10n(f"Обери словацький варіант для: {w[4]['uk']}.", f"Выбери словацкий вариант для: {w[4]['ru']}.", f"Choose the Slovak item for: {w[4]['en']}."), "wordIds": [w[4]["id"]], "options": [w[4]["sk"], w[2]["sk"], w[0]["sk"]], "correctAnswer": w[4]["sk"]},
        {"id": f"{lid}-e12", "lessonId": lid, "type": "sentence_order", "order": 12, "question": "Віднови логічний порядок C2-відповіді.", "questionLocalized": l10n("Віднови логічний порядок C2-відповіді.", "Восстанови логический порядок C2-ответа.", "Restore the logical order of a C2 answer."), "wordIds": [w[0]["id"], w[1]["id"]], "items": ["Najprv treba pomenovať kontext.", "Potom možno doplniť presnejší výraz.", "Napokon z toho vyplýva konkrétny záver."], "correctOrder": ["Najprv treba pomenovať kontext.", "Potom možno doplniť presnejší výraz.", "Napokon z toho vyplýva konkrétny záver."]},
        {"id": f"{lid}-e13", "lessonId": lid, "type": "dialogue_choose_reply", "order": 13, "question": "Обери відповідь з точним регістром.", "questionLocalized": l10n("Обери відповідь з точним регістром.", "Выбери ответ с точным регистром.", "Choose the reply with the right register."), "wordIds": [w[2]["id"], w[3]["id"]], "dialogue": [{"speaker": "A", "sk": "Potrebujem to povedať odborne, ale nie zbytočne tvrdo."}], "options": [{"id": "a", "sk": "Rozumiem. Preformuloval by som to vecne a zároveň opatrne.", "correct": True}, {"id": "b", "sk": "Napíš tam čokoľvek, hlavne rýchlo.", "correct": False}, {"id": "c", "sk": "Daj tam najtvrdšiu možnú formuláciu.", "correct": False}]},
        {"id": f"{lid}-e14", "lessonId": lid, "type": "multiple_choice_translation", "order": 14, "question": f"Що відповідає словацькому «{w[7]['sk']}»?", "questionLocalized": l10n(f"Що відповідає словацькому «{w[7]['sk']}»?", f"Что соответствует словацкому «{w[7]['sk']}»?", f"What matches the Slovak “{w[7]['sk']}”?"), "wordIds": [w[7]["id"]], "options": [w[7]["uk"], w[1]["uk"], w[2]["uk"]], "correctAnswer": w[7]["uk"]},
        {"id": f"{lid}-e15", "lessonId": lid, "type": "meaning_in_context", "order": 15, "question": "Обери найточніше читання підтексту.", "questionLocalized": l10n("Обери найточніше читання підтексту.", "Выбери самое точное чтение подтекста.", "Choose the most precise reading of the subtext."), "wordIds": [w[0]["id"], w[3]["id"], w[6]["id"]], "context": {"sk": f"V téme {title} nejde iba o slovnú zásobu, ale aj o to, čo hovoriaci naznačuje, čo zamlčí a aký register si zvolí."}, "options": [{"id": "a", "text": l10n("Treba rozumieť aj nepriamemu významu a štýlu.", "Нужно понимать и непрямой смысл, и стиль.", "One has to understand indirect meaning and style as well."), "correct": True}, {"id": "b", "text": l10n("Stačí preložiť každé slovo osobitne.", "Достаточно перевести каждое слово отдельно.", "It is enough to translate every word separately."), "correct": False}, {"id": "c", "text": l10n("Register v C2 komunikácii nehrá žiadnu úlohu.", "Регистр в C2-коммуникации не играет роли.", "Register plays no role in C2 communication."), "correct": False}]},
        {"id": f"{lid}-e16", "lessonId": lid, "type": "sentence_order", "order": 16, "question": "Побудуй C2-відповідь: теза, застереження, висновок.", "questionLocalized": l10n("Побудуй C2-відповідь: теза, застереження, висновок.", "Построй C2-ответ: тезис, оговорка, вывод.", "Build a C2 answer: thesis, caveat, conclusion."), "wordIds": [w[1]["id"], w[4]["id"], w[7]["id"]], "items": ["Na prvý pohľad sa zdá, že riešenie je jednoznačné.", "Pri bližšom pohľade však treba zohľadniť aj kontext a možné dôsledky.", "Preto by som volil formuláciu, ktorá je presná, ale necháva priestor na doplnenie."], "correctOrder": ["Na prvý pohľad sa zdá, že riešenie je jednoznačné.", "Pri bližšom pohľade však treba zohľadniť aj kontext a možné dôsledky.", "Preto by som volil formuláciu, ktorá je presná, ale necháva priestor na doplnenie."]},
    ]


def make_lesson(lesson: dict[str, object], next_id: str | None) -> dict[str, object]:
    n = int(lesson["number"])
    section = int(lesson["section"])
    lid = f"c2-s{section:02d}-l{n:03d}"
    lesson["section_id"] = f"c2_s{section:02d}"
    title = str(lesson["title_sk"])
    section_title = str(lesson["section_title_en"])
    what_ru = str(lesson.get("what_ru", f"Тренируем тему {title}."))
    words = make_words(lid, lesson)
    desc = loc(
        f"Precvičíš si tému {title} v komplexnej komunikácii na úrovni C2.",
        f"Тренуємо тему «{title}»: аргументовано, точно й у реальному контексті.",
        what_ru,
        f"Practice the C2 topic “{title}” in complex communication. Section: {section_title}.",
    )
    exs = make_exercises(lid, title, words)
    return {"lessons": [{
        "id": lid,
        "sectionId": f"c2_s{section:02d}",
        "level": "C2",
        "title": loc(title, title, title, title),
        "topic": loc(title, title, title, title),
        "description": desc,
        "order": n,
        "xpReward": 260,
        "estimatedMinutes": 45,
        "isPublished": False,
        "intro": desc,
        "completionMessage": loc("Výborne. Tému vieš použiť v náročnejšej komunikácii.", "Добре. Тепер можеш використати тему в складнішій розмові.", "Хорошо. Теперь можешь использовать тему в более сложном разговоре.", "Good. You can now use the topic in more complex communication."),
        "updatedAt": UPDATED_AT,
        "localization": {"uiLanguages": ["uk", "ru", "en"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
        "assets": {"images": {}, "audio": {}},
        "startScreen": {
            "screenType": "lesson_start",
            "title": loc(title, title, title, title),
            "shortDescription": l10n(desc["uk"], desc["ru"], desc["en"]),
            "outcomes": [
                l10n("пояснити думку точніше й довше", "объяснить мысль точнее и длиннее", "explain an idea more precisely and at greater length"),
                l10n("використати нові C2-фрази в контексті", "использовать новые C2-фразы в контексте", "use new C2 phrases in context"),
                l10n("обрати природну реакцію в реальній ситуації", "выбрать естественную реакцию в реальной ситуации", "choose a natural reply in a real situation"),
            ],
            "newWords": [x["id"] for x in words],
            "exercisesCount": len(exs),
            "reward": "+260 XP",
            "estimatedMinutes": 45,
            "button": "Почати урок",
        },
        "theoryScreens": [
            {"id": "t1", "screenType": "theory", "order": 1, "title": l10n("Фокус уроку", "Фокус урока", "Lesson focus"), "body": l10n(desc["uk"], desc["ru"], desc["en"]), "examples": [{"sk": words[0]["exampleSk"], "translation": l10n(words[0]["exampleUk"], words[0]["exampleRu"], words[0]["exampleEn"])}, {"sk": words[1]["exampleSk"], "translation": l10n(words[1]["exampleUk"], words[1]["exampleRu"], words[1]["exampleEn"])}], "shortRule": l10n("На C2 важливо не просто відповісти, а показати причину, умову, наслідок або нюанс.", "На C2 важно не просто ответить, а показать причину, условие, последствие или нюанс.", "At C2, show a reason, condition, consequence or nuance."), "button": "Далі"},
            {"id": "t2", "screenType": "theory", "order": 2, "title": l10n("Модель відповіді", "Модель ответа", "Answer model"), "body": l10n("Будуй відповідь за схемою: контекст -> позиція -> аргумент -> приклад -> наступний крок.", "Строй ответ по схеме: контекст -> позиция -> аргумент -> пример -> следующий шаг.", "Build the answer as: context -> position -> argument -> example -> next step."), "examples": [{"sk": "Z môjho pohľadu je dôležité najprv vysvetliť kontext.", "translation": l10n("З моєї точки зору важливо спочатку пояснити контекст.", "С моей точки зрения важно сначала объяснить контекст.", "From my point of view, it is important to explain the context first.")}, {"sk": "Na druhej strane treba zohľadniť aj praktické dôsledky.", "translation": l10n("З іншого боку, треба врахувати також практичні наслідки.", "С другой стороны, нужно учесть и практические последствия.", "On the other hand, practical consequences must also be considered.")}], "shortRule": l10n("Одна сильна відповідь має структуру, а не лише правильні слова.", "Один сильный ответ имеет структуру, а не только правильные слова.", "A strong answer has structure, not only correct words."), "button": "Далі"},
            {"id": "t3", "screenType": "theory", "order": 3, "title": l10n("Перенесення в життя", "Перенос в жизнь", "Real-life transfer"), "body": l10n("У фіналі потрібно вибрати репліку, яка реально рухає ситуацію вперед.", "В финале нужно выбрать реплику, которая реально двигает ситуацию дальше.", "In the final task, choose the reply that moves the situation forward."), "examples": [{"sk": "Navrhujem, aby sme si najprv ujasnili priority.", "translation": l10n("Пропоную спочатку прояснити пріоритети.", "Предлагаю сначала прояснить приоритеты.", "I suggest clarifying priorities first.")}], "shortRule": l10n("C2 = самостійна, зв'язна й доречна комунікація.", "C2 = самостоятельная, связная и уместная коммуникация.", "C2 means independent, connected and appropriate communication."), "button": "До слів"},
        ],
        "wordsScreen": {"screenType": "lesson_words", "title": l10n("Цільові слова й фрази", "Целевые слова и фразы", "Target words and phrases"), "description": l10n("Ці одиниці взяті з затвердженого C2-плану.", "Эти единицы взяты из утвержденного C2-плана.", "These items come from the approved C2 plan."), "items": [{"wordId": x["id"], "sk": x["sk"], "uk": x["uk"], "ru": x["ru"], "en": x["en"], "pronunciationUk": x["pronunciationUk"], "exampleSk": x["exampleSk"], "exampleUk": x["exampleUk"], "exampleRu": x["exampleRu"], "exampleEn": x["exampleEn"]} for x in words], "button": "До практики"},
        "words": words,
        "exercises": exs,
        "finalSituation": {
            "id": "final-situation",
            "type": "interactive_scenario",
            "title": l10n(f"{title}: реальна ситуація", f"{title}: реальная ситуация", f"{title}: real situation"),
            "description": l10n("Обери репліки, які звучать природно, точно й доречно на рівні C2.", "Выбери реплики, которые звучат естественно, точно и уместно на уровне C2.", "Choose replies that sound natural, precise and appropriate at C2 level."),
            "steps": [
                {"id": "f1", "prompt": l10n("Потрібно почати відповідь без різкості.", "Нужно начать ответ без резкости.", "You need to start without sounding harsh."), "options": [{"sk": "Rozumiem, skúsim to najprv zhrnúť vlastnými slovami.", "correct": True}, {"sk": "Nemáš pravdu a viac sa o tom nebavme.", "correct": False}, {"sk": "Neviem a nechcem reagovať.", "correct": False}]},
                {"id": "f2", "prompt": l10n("Потрібно додати аргумент.", "Нужно добавить аргумент.", "You need to add an argument."), "options": [{"sk": "Dôvod je podľa mňa v tom, že situácia má viac okolností.", "correct": True}, {"sk": "Pretože áno.", "correct": False}, {"sk": "To nesúvisí s ničím.", "correct": False}]},
                {"id": "f3", "prompt": l10n("Потрібно завершити практично.", "Нужно завершить практически.", "You need to close practically."), "options": [{"sk": "Navrhujem ďalší krok a potom si to potvrdíme písomne.", "correct": True}, {"sk": "Nechajme to bez riešenia.", "correct": False}, {"sk": "Každý nech si domyslí zvyšok.", "correct": False}]},
            ],
            "passRequirement": "3/3",
            "successMessage": l10n("Готово: тема перенесена в реальну C2-комунікацію.", "Готово: тема перенесена в реальную C2-коммуникацию.", "Done: the topic was transferred into real C2 communication."),
        },
        "resultScreen": {"screenType": "lesson_result", "title": l10n("Урок завершено", "Урок завершён", "Lesson complete"), "subtitle": l10n("Ти пройшов ще один крок рівня C2.", "Ты прошёл ещё один шаг уровня C2.", "You completed another C2 step."), "xpReward": 260, "newWordsCount": len(words), "exercisesCompleted": len(exs), "nowYouKnow": ["структурувати відповідь", "пояснювати нюанс", "реагувати доречно"], "mistakesMessage": l10n("Повтори вправи, де плутається значення або тон.", "Повтори упражнения, где путается значение или тон.", "Repeat exercises where meaning or tone is unclear."), "buttons": ["Продовжити", "Повторити урок", "Тренувати помилки"], "skills": [{"id": "vocabulary", "label": l10n("лексика", "лексика", "vocabulary"), "weight": 0.3}, {"id": "composition", "label": l10n("структура", "структура", "composition"), "weight": 0.4}, {"id": "transfer", "label": l10n("перенесення", "перенос", "transfer"), "weight": 0.3}], "nextLesson": {"id": next_id} if next_id else None},
    }]}


def main() -> int:
    lessons = extract_lessons()
    OUT.mkdir(parents=True, exist_ok=True)
    for lesson, next_lesson in zip(lessons, lessons[1:] + [None]):
        next_id = None if next_lesson is None else f"c2-s{int(next_lesson['section']):02d}-l{int(next_lesson['number']):03d}"
        doc = make_lesson(lesson, next_id)
        path = OUT / doc["lessons"][0]["id"]
        path = path.with_suffix(".json")
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("# SlovakGo C2 Lessons\n\n70 active C2 lessons generated from `C2/LESSON_PLAN.md`.\n", encoding="utf-8")
    print(f"Generated {len(lessons)} C2 lessons in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
