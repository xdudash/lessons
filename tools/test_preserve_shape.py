from __future__ import annotations

import copy
import importlib


def main() -> None:
    m = importlib.import_module("localize_google")
    migrate = getattr(m, "safe_migrate_lesson", None)
    assert migrate is not None, "safe_migrate_lesson is missing"

    lesson = {
        "title": {"sk": "Test", "uk": "Тест"},
        "localization": {"uiLanguages": ["uk"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
        "startScreen": {"title": {"uk": "Старт"}, "outcomes": ["результат"], "button": "Почати урок"},
        "theoryScreens": [{"title": {"uk": "Теорія"}, "button": "Далі", "examples": [{"sk": "Som tu.", "translation": {"uk": "Я тут."}}]}],
        "wordsScreen": {"title": {"uk": "Слова"}, "items": [{"sk": "dom", "uk": "дім"}], "button": "До практики"},
        "words": [{"id": "w1", "sk": "dom", "uk": "дім", "exampleSk": "To je dom.", "exampleUk": "Це дім."}],
        "exercises": [{"id": "e1", "lessonId": "x", "type": "single_choice", "order": 1, "question": "Що це?", "button": "Далі", "options": [{"id": "a", "text": "дім", "correct": True}]}],
        "finalSituation": {"type": "interactive_scenario", "steps": [{"id": "s1", "prompt": {"uk": "Обери"}, "options": [{"sk": "Áno", "correct": True}, {"sk": "Nie", "correct": False}]}]},
        "resultScreen": {"title": {"uk": "Готово"}, "buttons": ["Далі"], "nowYouKnow": ["слово"]},
    }
    before = copy.deepcopy(lesson)

    table = {
        "Тест": {"ru": "Тест", "en": "Test"}, "Старт": {"ru": "Старт", "en": "Start"},
        "результат": {"ru": "результат", "en": "outcome"}, "Теорія": {"ru": "Теория", "en": "Theory"},
        "Я тут.": {"ru": "Я здесь.", "en": "I am here."}, "Слова": {"ru": "Слова", "en": "Words"},
        "дім": {"ru": "дом", "en": "house"}, "Це дім.": {"ru": "Это дом.", "en": "This is a house."},
        "Що це?": {"ru": "Что это?", "en": "What is this?"}, "Обери": {"ru": "Выбери", "en": "Choose"},
        "Готово": {"ru": "Готово", "en": "Done"},
    }

    def localize(value):
        uk = value.get("uk") if isinstance(value, dict) else value
        if not isinstance(uk, str) or uk not in table:
            return value
        base = dict(value) if isinstance(value, dict) else {"uk": uk}
        base.update(table[uk])
        return base

    migrate(lesson, localize)

    assert lesson["startScreen"]["button"] == before["startScreen"]["button"]
    assert lesson["theoryScreens"][0]["button"] == before["theoryScreens"][0]["button"]
    assert lesson["wordsScreen"]["items"] == before["wordsScreen"]["items"]
    assert lesson["wordsScreen"]["button"] == before["wordsScreen"]["button"]
    assert lesson["exercises"][0]["button"] == before["exercises"][0]["button"]
    assert lesson["resultScreen"]["buttons"] == before["resultScreen"]["buttons"]
    assert lesson["resultScreen"]["nowYouKnow"] == before["resultScreen"]["nowYouKnow"]
    assert lesson["title"] == {"sk": "Test", "uk": "Тест", "ru": "Тест", "en": "Test"}
    assert lesson["localization"]["uiLanguages"] == ["uk", "ru", "en"]
    assert lesson["exercises"][0]["question"] == {"uk": "Що це?", "ru": "Что это?", "en": "What is this?"}
    print("shape preservation regression passed")


if __name__ == "__main__":
    main()
