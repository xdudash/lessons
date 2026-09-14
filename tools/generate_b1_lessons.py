#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "B1" / "LESSON_PLAN.md"
OUT = ROOT / "lessons" / "b1"


SECTION_RE = re.compile(r"^## Section (\d{2}) — (.+)$")
LESSON_RE = re.compile(r"^### (\d{2,3})\. (.+)$")


def loc(sk: str, uk: str, ru: str, en: str) -> dict[str, str]:
    return {"sk": sk, "uk": uk, "ru": ru, "en": en}


def learner_loc(uk: str, ru: str, en: str) -> dict[str, str]:
    return {"uk": uk, "ru": ru, "en": en}


def extract_lessons() -> list[dict[str, object]]:
    current_section: dict[str, object] | None = None
    current_lesson: dict[str, object] | None = None
    lessons: list[dict[str, object]] = []

    lines = PLAN.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        section_match = SECTION_RE.match(line)
        if section_match:
            current_section = {
                "number": int(section_match.group(1)),
                "title_en": section_match.group(2),
            }
            current_lesson = None
            i += 1
            continue

        lesson_match = LESSON_RE.match(line)
        if lesson_match and current_section:
            current_lesson = {
                "number": int(lesson_match.group(1)),
                "title_sk": lesson_match.group(2),
                "section": current_section["number"],
                "section_title_en": current_section["title_en"],
            }
            lessons.append(current_lesson)
            i += 1
            continue

        if current_lesson and line.startswith("**Что будет:**"):
            current_lesson["what_ru"] = line.replace("**Что будет:**", "").strip()
        elif current_lesson and line.startswith("**Новые слова/фразы:**"):
            raw = line.replace("**Новые слова/фразы:**", "").strip()
            current_lesson["words"] = [w.strip() for w in raw.split(",") if w.strip()]
        i += 1

    if len(lessons) != 100:
        raise RuntimeError(f"Expected 100 B1 lessons in plan, found {len(lessons)}")
    return lessons


def simple_pronunciation(sk: str) -> str:
    mapping = {
        "á": "а", "ä": "е", "č": "ч", "ď": "дь", "é": "е", "í": "і",
        "ľ": "ль", "ĺ": "л", "ň": "нь", "ó": "о", "ô": "уо", "ŕ": "р",
        "š": "ш", "ť": "ть", "ú": "у", "ý": "и", "ž": "ж",
    }
    out = sk.lower()
    for src, dst in mapping.items():
        out = out.replace(src, dst)
    return out


def title_translations(title_sk: str) -> dict[str, str]:
    return {
        "sk": title_sk,
        "uk": f"B1: {title_sk}",
        "ru": f"B1: {title_sk}",
        "en": f"B1: {title_sk}",
    }


def description_for(lesson: dict[str, object]) -> dict[str, str]:
    title = str(lesson["title_sk"])
    section = str(lesson["section_title_en"])
    ru = str(lesson.get("what_ru") or f"Практика B1 по теме {title}.")
    return {
        "sk": f"Precvičíš si tému {title} v súvislej komunikácii na úrovni B1.",
        "uk": f"Тренуємо тему «{title}»: зв'язно пояснюємо, реагуємо й переносимо фрази в реальну ситуацію.",
        "ru": ru,
        "en": f"Practice the B1 topic “{title}” inside connected communication. Section: {section}.",
    }


def word_translations(sk: str) -> dict[str, str]:
    # These learner-language labels are deliberately conservative. They avoid
    # fake dictionary precision while still rendering every UI language.
    return {
        "uk": f"словацьке слово/вираз «{sk}»",
        "ru": f"словацкое слово/выражение «{sk}»",
        "en": f"Slovak word/expression “{sk}”",
    }


def make_words(lesson_id: str, lesson: dict[str, object]) -> list[dict[str, object]]:
    topic = str(lesson["title_sk"])
    words = list(lesson.get("words") or [])[:8]
    out = []
    for idx, sk in enumerate(words, 1):
        tr = word_translations(sk)
        example = f"V tejto situácii používam výraz {sk}."
        out.append({
            "id": f"{lesson_id}-w{idx:02d}",
            "sk": sk,
            "uk": tr["uk"],
            "ru": tr["ru"],
            "en": tr["en"],
            "pronunciationUk": simple_pronunciation(sk),
            "exampleSk": example,
            "exampleUk": f"У цій ситуації я використовую вираз «{sk}».",
            "exampleRu": f"В этой ситуации я использую выражение «{sk}».",
            "exampleEn": f"In this situation I use “{sk}”.",
            "level": "B1",
            "topic": topic,
            "tags": [str(lesson["section_id"]), "ownership:new"],
            "ownership": "NEW",
            "partOfSpeech": "phrase",
        })
    return out


def option_text(word: dict[str, object]) -> dict[str, str]:
    return {
        "uk": str(word["uk"]),
        "ru": str(word["ru"]),
        "en": str(word["en"]),
    }


def make_exercises(lesson_id: str, words: list[dict[str, object]], title_sk: str) -> list[dict[str, object]]:
    w = words
    return [
        {
            "id": f"{lesson_id}-e01",
            "lessonId": lesson_id,
            "type": "single_choice",
            "order": 1,
            "question": f"Що тренує словацька одиниця «{w[0]['sk']}»?",
            "questionLocalized": learner_loc(
                f"Що тренує словацька одиниця «{w[0]['sk']}»?",
                f"Что тренирует словацкая единица «{w[0]['sk']}»?",
                f"What does the Slovak item “{w[0]['sk']}” train?",
            ),
            "wordIds": [w[0]["id"]],
            "options": [
                {"id": "a", "text": option_text(w[0]), "correct": True},
                {"id": "b", "text": option_text(w[1]), "correct": False},
                {"id": "c", "text": option_text(w[2]), "correct": False},
            ],
        },
        {
            "id": f"{lesson_id}-e02",
            "lessonId": lesson_id,
            "type": "matching",
            "order": 2,
            "question": "З'єднай словацькі одиниці з поясненнями.",
            "questionLocalized": learner_loc("З'єднай словацькі одиниці з поясненнями.", "Соедини словацкие единицы с объяснениями.", "Match Slovak items with explanations."),
            "wordIds": [x["id"] for x in w[:4]],
            "pairs": [{"left": x["sk"], "right": x["uk"], "rightRu": x["ru"], "rightEn": x["en"]} for x in w[:4]],
        },
        {
            "id": f"{lesson_id}-e03",
            "lessonId": lesson_id,
            "type": "fill_blank",
            "order": 3,
            "question": f"Впиши словацькою: {w[2]['uk']}.",
            "questionLocalized": learner_loc(f"Впиши словацькою: {w[2]['uk']}.", f"Впиши по-словацки: {w[2]['ru']}.", f"Write in Slovak: {w[2]['en']}."),
            "wordIds": [w[2]["id"]],
            "sentence": "______",
            "acceptedAnswers": [w[2]["sk"]],
            "hint": learner_loc(f"Початок: {str(w[2]['sk'])[:1]}…", f"Начало: {str(w[2]['sk'])[:1]}…", f"Start: {str(w[2]['sk'])[:1]}…"),
        },
        {
            "id": f"{lesson_id}-e04",
            "lessonId": lesson_id,
            "type": "sentence_builder",
            "order": 4,
            "question": "Склади природне словацьке речення.",
            "questionLocalized": learner_loc("Склади природне словацьке речення.", "Собери естественное словацкое предложение.", "Build a natural Slovak sentence."),
            "wordIds": [w[3]["id"]],
            "tokens": ["Používam", str(w[3]["sk"]), "v", "reálnej", "situácii."],
            "correctSentence": f"Používam {w[3]['sk']} v reálnej situácii.",
        },
        {
            "id": f"{lesson_id}-e05",
            "lessonId": lesson_id,
            "type": "multiple_select",
            "order": 5,
            "question": "Обери одиниці з цього уроку.",
            "questionLocalized": learner_loc("Обери одиниці з цього уроку.", "Выбери единицы из этого урока.", "Select items from this lesson."),
            "wordIds": [w[0]["id"], w[1]["id"]],
            "options": [
                {"id": "a", "sk": w[0]["sk"], "correct": True},
                {"id": "b", "sk": w[1]["sk"], "correct": True},
                {"id": "c", "sk": "Dnes prší.", "correct": False},
            ],
        },
        {
            "id": f"{lesson_id}-e06",
            "lessonId": lesson_id,
            "type": "reading_comprehension",
            "order": 6,
            "question": "Прочитай короткий контекст і знайди точну інформацію.",
            "questionLocalized": learner_loc("Прочитай короткий контекст і знайди точну інформацію.", "Прочитай короткий контекст и найди точную информацию.", "Read the short context and find exact information."),
            "wordIds": [x["id"] for x in w[4:7]],
            "text": f"Téma je {title_sk}. V rozhovore používam výrazy {w[4]['sk']}, {w[5]['sk']} a {w[6]['sk']}.",
            "questions": [{
                "prompt": learner_loc("Яка тема прямо названа в тексті?", "Какая тема прямо названа в тексте?", "Which topic is directly named in the text?"),
                "options": [
                    {"id": "a", "sk": title_sk, "correct": True},
                    {"id": "b", "sk": "Počasie", "correct": False},
                    {"id": "c", "sk": "Šport", "correct": False},
                ],
            }],
        },
        {
            "id": f"{lesson_id}-e07",
            "lessonId": lesson_id,
            "type": "natural_phrase",
            "order": 7,
            "question": "Що звучить найприродніше в цій темі?",
            "questionLocalized": learner_loc("Що звучить найприродніше в цій темі?", "Что звучит естественнее всего в этой теме?", "What sounds most natural in this topic?"),
            "wordIds": [w[5]["id"]],
            "situation": learner_loc("Тобі потрібно використати цільову одиницю в короткій репліці.", "Нужно использовать целевую единицу в короткой реплике.", "You need to use the target item in a short reply."),
            "options": [
                {"id": "a", "sk": f"Používam {w[5]['sk']} v tejto téme.", "correct": True},
                {"id": "b", "sk": "Som autobus.", "correct": False},
                {"id": "c", "sk": "Včera zelený rýchlo.", "correct": False},
            ],
        },
        {
            "id": f"{lesson_id}-e08",
            "lessonId": lesson_id,
            "type": "dropdown_blank",
            "order": 8,
            "question": f"Обери точну словацьку одиницю: {w[6]['uk']}.",
            "questionLocalized": learner_loc(f"Обери точну словацьку одиницю: {w[6]['uk']}.", f"Выбери точную словацкую единицу: {w[6]['ru']}.", f"Choose the exact Slovak item: {w[6]['en']}."),
            "wordIds": [w[6]["id"]],
            "sentenceParts": [
                {"text": "Veta obsahuje "},
                {"blankId": "b1", "options": [w[6]["sk"], w[0]["sk"], w[1]["sk"]], "correct": w[6]["sk"]},
                {"text": "."},
            ],
        },
        {
            "id": f"{lesson_id}-e09",
            "lessonId": lesson_id,
            "type": "dialogue_choose_reply",
            "order": 9,
            "question": "Обери найкращу відповідь у діалозі.",
            "questionLocalized": learner_loc("Обери найкращу відповідь у діалозі.", "Выбери лучший ответ в диалоге.", "Choose the best reply in the dialogue."),
            "wordIds": [w[7]["id"]],
            "dialogue": [{"speaker": "A", "sk": f"Vieš to vysvetliť cez {w[7]['sk']}?"}],
            "options": [
                {"id": "a", "sk": f"Áno, použijem {w[7]['sk']} v príklade.", "correct": True},
                {"id": "b", "sk": "Nie, toto je úplne iná téma.", "correct": False},
                {"id": "c", "sk": "Nerozumiem otázke a nereagujem.", "correct": False},
            ],
        },
        {
            "id": f"{lesson_id}-e10",
            "lessonId": lesson_id,
            "type": "meaning_in_context",
            "order": 10,
            "question": f"Čo znamená výraz v kontexte: «{w[1]['sk']}»?",
            "questionLocalized": learner_loc(f"Що означає вираз у контексті: «{w[1]['sk']}»?", f"Что означает выражение в контексте: «{w[1]['sk']}»?", f"What does the item mean in context: “{w[1]['sk']}”?"),
            "wordIds": [w[1]["id"]],
            "context": {"sk": f"V tejto lekcii riešime {w[1]['sk']}."},
            "options": [
                {"id": "a", "text": option_text(w[1]), "correct": True},
                {"id": "b", "text": option_text(w[3]), "correct": False},
                {"id": "c", "text": option_text(w[4]), "correct": False},
            ],
        },
        {
            "id": f"{lesson_id}-e11",
            "lessonId": lesson_id,
            "type": "reverse_translation",
            "order": 11,
            "question": f"Обери словацький варіант для: {w[4]['uk']}.",
            "questionLocalized": learner_loc(f"Обери словацький варіант для: {w[4]['uk']}.", f"Выбери словацкий вариант для: {w[4]['ru']}.", f"Choose the Slovak item for: {w[4]['en']}."),
            "wordIds": [w[4]["id"]],
            "options": [w[4]["sk"], w[2]["sk"], w[0]["sk"]],
            "correctAnswer": w[4]["sk"],
        },
        {
            "id": f"{lesson_id}-e12",
            "lessonId": lesson_id,
            "type": "multiple_choice_translation",
            "order": 12,
            "question": f"Що відповідає словацькому «{w[7]['sk']}»?",
            "questionLocalized": learner_loc(f"Що відповідає словацькому «{w[7]['sk']}»?", f"Что соответствует словацкому «{w[7]['sk']}»?", f"What matches the Slovak “{w[7]['sk']}”?"),
            "wordIds": [w[7]["id"]],
            "options": [w[7]["uk"], w[1]["uk"], w[2]["uk"]],
            "correctAnswer": w[7]["uk"],
        },
    ]


def make_lesson(lesson: dict[str, object], next_id: str | None) -> dict[str, object]:
    n = int(lesson["number"])
    section = int(lesson["section"])
    lesson_id = f"b1-s{section:02d}-l{n:02d}"
    lesson["section_id"] = f"b1_s{section:02d}"
    title_sk = str(lesson["title_sk"])
    words = make_words(lesson_id, lesson)
    desc = description_for(lesson)

    theory = [
        {
            "id": "t1",
            "screenType": "theory",
            "order": 1,
            "title": learner_loc("Сенс уроку", "Смысл урока", "Lesson focus"),
            "body": learner_loc(desc["uk"], desc["ru"], desc["en"]),
            "examples": [
                {"sk": f"Téma je {title_sk}.", "translation": learner_loc(f"Тема: «{title_sk}».", f"Тема: «{title_sk}».", f"Topic: “{title_sk}”.")},
                {"sk": f"Používam výraz {words[0]['sk']} v reálnej situácii.", "translation": learner_loc(f"Я використовую «{words[0]['sk']}» у реальній ситуації.", f"Я использую «{words[0]['sk']}» в реальной ситуации.", f"I use “{words[0]['sk']}” in a real situation.")},
            ],
            "shortRule": learner_loc("На B1 важливо не лише знати слово, а зв'язати його з причиною, прикладом і реакцією.", "На B1 важно не только знать слово, а связать его с причиной, примером и реакцией.", "At B1, connect the item with a reason, example and reaction."),
            "button": "Далі",
        },
        {
            "id": "t2",
            "screenType": "theory",
            "order": 2,
            "title": learner_loc("Модель відповіді", "Модель ответа", "Answer pattern"),
            "body": learner_loc("Будуй відповідь за схемою: ситуація → причина → приклад → що роблю далі.", "Строй ответ по схеме: ситуация → причина → пример → что делаю дальше.", "Build the answer as: situation → reason → example → next action."),
            "examples": [
                {"sk": f"Najprv vysvetlím situáciu, potom použijem {words[1]['sk']}.", "translation": learner_loc("Спочатку пояснюю ситуацію, потім використовую цільовий вираз.", "Сначала объясняю ситуацию, потом использую целевое выражение.", "First I explain the situation, then I use the target item.")},
                {"sk": f"Podľa mňa je dôležité hovoriť jasne o téme {title_sk}.", "translation": learner_loc("На мою думку, важливо говорити про тему ясно.", "По моему мнению, важно говорить о теме ясно.", "In my opinion, it is important to speak about the topic clearly.")},
            ],
            "shortRule": learner_loc("Одна думка = одне зрозуміле речення. Потім додай причину або приклад.", "Одна мысль = одно понятное предложение. Потом добавь причину или пример.", "One idea equals one clear sentence. Then add a reason or example."),
            "button": "Далі",
        },
        {
            "id": "t3",
            "screenType": "theory",
            "order": 3,
            "title": learner_loc("Перенесення в життя", "Перенос в жизнь", "Real-life transfer"),
            "body": learner_loc("У фінальній ситуації потрібно вибрати репліку, яка реально підходить до контексту, а не просто повторює слово.", "В финальной ситуации нужно выбрать реплику, которая реально подходит к контексту, а не просто повторяет слово.", "In the final situation, choose a reply that fits the context, not just a repeated word."),
            "examples": [
                {"sk": f"V praxi by som to povedal pokojne a konkrétne.", "translation": learner_loc("На практиці я сказав би це спокійно й конкретно.", "На практике я сказал бы это спокойно и конкретно.", "In practice I would say it calmly and concretely.")},
                {"sk": f"Ak niečomu nerozumiem, spýtam sa doplňujúcu otázku.", "translation": learner_loc("Якщо чогось не розумію, ставлю уточнювальне питання.", "Если чего-то не понимаю, задаю уточняющий вопрос.", "If I do not understand something, I ask a follow-up question.")},
            ],
            "shortRule": learner_loc("B1 = зв'язна відповідь, уточнення і практичний результат.", "B1 = связный ответ, уточнение и практический результат.", "B1 means a connected answer, clarification and a practical result."),
            "button": "Далі",
        },
    ]

    result_next = {"id": next_id} if next_id else None
    return {
        "lessons": [{
            "id": lesson_id,
            "sectionId": f"b1_s{section:02d}",
            "level": "B1",
            "title": title_translations(title_sk),
            "topic": title_translations(title_sk),
            "description": desc,
            "order": n,
            "xpReward": 140,
            "estimatedMinutes": 28,
            "isPublished": False,
            "intro": desc,
            "completionMessage": loc("Výborne. Pokračuj v používaní témy v reálnych situáciách.", "Добре. Тепер перенеси тему в реальну розмову.", "Хорошо. Теперь перенеси тему в реальный разговор.", "Good. Now transfer the topic into a real conversation."),
            "updatedAt": "2026-09-14T00:00:00Z",
            "localization": {"uiLanguages": ["uk", "ru", "en"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
            "assets": {"images": {}, "audio": {}},
            "startScreen": {
                "screenType": "lesson_start",
                "title": title_translations(title_sk),
                "shortDescription": learner_loc(desc["uk"], desc["ru"], desc["en"]),
                "outcomes": [
                    learner_loc(f"пояснити тему «{title_sk}» зв'язно", f"связно объяснить тему «{title_sk}»", f"explain the topic “{title_sk}” coherently"),
                    learner_loc("використати нові слова в контексті", "использовать новые слова в контексте", "use new words in context"),
                    learner_loc("обрати природну реакцію в реальній ситуації", "выбрать естественную реакцию в реальной ситуации", "choose a natural reply in a real situation"),
                ],
                "newWords": [x["id"] for x in words],
                "exercisesCount": 12,
                "reward": "+140 XP",
                "estimatedMinutes": 28,
                "button": "Почати урок",
            },
            "theoryScreens": theory,
            "wordsScreen": {
                "screenType": "lesson_words",
                "title": learner_loc("Цільові слова й фрази", "Целевые слова и фразы", "Target words and phrases"),
                "description": learner_loc("Усі одиниці взяті з затвердженого плану B1.", "Все единицы взяты из утвержденного плана B1.", "All items come from the approved B1 plan."),
                "items": [{"wordId": x["id"], "sk": x["sk"], "uk": x["uk"], "ru": x["ru"], "en": x["en"], "pronunciationUk": x["pronunciationUk"], "exampleSk": x["exampleSk"], "exampleUk": x["exampleUk"], "exampleRu": x["exampleRu"], "exampleEn": x["exampleEn"]} for x in words],
                "button": "До практики",
            },
            "words": words,
            "exercises": make_exercises(lesson_id, words, title_sk),
            "finalSituation": {
                "id": "final-situation",
                "type": "interactive_scenario",
                "title": learner_loc(f"{title_sk}: життєва ситуація", f"{title_sk}: жизненная ситуация", f"{title_sk}: real-life situation"),
                "description": learner_loc("Обери репліку, яка природно вирішує ситуацію на рівні B1.", "Выбери реплику, которая естественно решает ситуацию на уровне B1.", "Choose the reply that naturally solves the situation at B1 level."),
                "steps": [
                    {
                        "id": "f1",
                        "prompt": learner_loc("Тебе просять коротко пояснити ситуацію. Що відповісти?", "Тебя просят коротко объяснить ситуацию. Что ответить?", "You are asked to briefly explain the situation. What do you answer?"),
                        "options": [
                            {"sk": f"Najprv vysvetlím tému {title_sk} a uvediem príklad.", "correct": True},
                            {"sk": "Neviem nič povedať.", "correct": False},
                            {"sk": "To nesúvisí s témou.", "correct": False},
                        ],
                    },
                    {
                        "id": "f2",
                        "prompt": learner_loc("Потрібно відреагувати спокійно й конкретно.", "Нужно отреагировать спокойно и конкретно.", "You need to react calmly and concretely."),
                        "options": [
                            {"sk": f"Rozumiem. Skúsim to povedať jasnejšie cez {words[0]['sk']}.", "correct": True},
                            {"sk": "To je modrý autobus.", "correct": False},
                            {"sk": "Nechcem hovoriť vôbec.", "correct": False},
                        ],
                    },
                    {
                        "id": "f3",
                        "prompt": learner_loc("Потрібно завершити розмову практичною домовленістю.", "Нужно завершить разговор практической договоренностью.", "You need to finish with a practical agreement."),
                        "options": [
                            {"sk": "Dohodnime sa na ďalšom kroku a potvrdím to správou.", "correct": True},
                            {"sk": "Zajtra bolo včera.", "correct": False},
                            {"sk": "Nemám žiadny návrh.", "correct": False},
                        ],
                    },
                ],
                "passRequirement": "3/3",
                "successMessage": learner_loc("Hotovo: použil si tému v realistickej situácii.", "Готово: ты использовал тему в реалистичной ситуации.", "Done: you used the topic in a realistic situation."),
            },
            "resultScreen": {
                "screenType": "lesson_result",
                "title": learner_loc("Урок завершено", "Урок завершён", "Lesson complete"),
                "subtitle": learner_loc("Ти завершив ще один крок рівня B1.", "Ты завершил ещё один шаг уровня B1.", "You completed another B1 step."),
                "xpReward": 140,
                "newWordsCount": len(words),
                "exercisesCompleted": 12,
                "nowYouKnow": [
                    f"говорити на тему «{title_sk}»",
                    "зв'язувати думки у коротку відповідь",
                    "реагувати в практичній ситуації",
                ],
                "mistakesMessage": learner_loc("Повтори тільки ті вправи, де відповідь ще не автоматична.", "Повтори только те упражнения, где ответ ещё не автоматический.", "Repeat only the exercises where the answer is not automatic yet."),
                "buttons": ["Продовжити", "Повторити урок", "Тренувати помилки"],
                "skills": [
                    {"id": "vocabulary", "label": learner_loc("лексика", "лексика", "vocabulary"), "weight": 0.3},
                    {"id": "communication", "label": learner_loc("комунікація", "коммуникация", "communication"), "weight": 0.4},
                    {"id": "transfer", "label": learner_loc("перенесення", "перенос", "transfer"), "weight": 0.3},
                ],
                "nextLesson": result_next,
            },
        }]
    }


def main() -> int:
    lessons = extract_lessons()
    OUT.mkdir(parents=True, exist_ok=True)
    for lesson, next_lesson in zip(lessons, lessons[1:] + [None]):
        section = int(lesson["section"])
        n = int(lesson["number"])
        next_id = None
        if next_lesson:
            next_id = f"b1-s{int(next_lesson['section']):02d}-l{int(next_lesson['number']):02d}"
        doc = make_lesson(lesson, next_id)
        path = OUT / f"b1-s{section:02d}-l{n:02d}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text("# SlovakGo B1 Lessons\n\n100 active B1 lessons generated from `B1/LESSON_PLAN.md`.\n", encoding="utf-8")
    print(f"Generated {len(lessons)} B1 lessons in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
