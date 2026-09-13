from __future__ import annotations

from copy import deepcopy

import localize_clean_v2 as m


def fake_translations():
    return {
        "en": {
            "Яка я людина?": "What kind of person am I?",
            "Почати урок": "Start lesson",
            "милий": "nice",
            "Він милий.": "He is nice.",
            "Що означає «veselý»?": "What does «veselý» mean?",
        },
        "ru": {
            "Яка я людина?": "Какой я человек?",
            "Почати урок": "Начать урок",
            "милий": "милый",
            "Він милий.": "Он милый.",
            "Що означає «veselý»?": "Что означает «veselý»?",
        },
    }


def test_structure_preserved():
    lesson = {
        "id": "x",
        "localization": {"uiLanguages": ["uk"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
        "title": {"sk": "Aký som človek?", "uk": "Яка я людина?"},
        "startScreen": {"title": {"uk": "Яка я людина?"}, "button": "Почати урок"},
        "wordsScreen": {"items": [{"wordId": "w1", "sk": "milý", "uk": "милий", "exampleSk": "Je milý.", "exampleUk": "Він милий."}], "button": "До практики"},
        "words": [{"id": "w1", "sk": "milý", "uk": "милий", "exampleSk": "Je milý.", "exampleUk": "Він милий."}],
        "exercises": [{"id": "e1", "type": "single_choice", "question": "Що означає «veselý»?", "button": "Далі", "options": [{"id": "a", "text": "милий", "correct": True}]}],
    }
    before = deepcopy(lesson)
    m.localize_lesson(lesson, fake_translations())

    assert lesson["id"] == before["id"]
    assert lesson["startScreen"]["button"] == before["startScreen"]["button"]
    assert lesson["wordsScreen"]["button"] == before["wordsScreen"]["button"]
    assert lesson["wordsScreen"]["items"][0]["wordId"] == "w1"
    assert lesson["exercises"][0]["type"] == "single_choice"
    assert lesson["exercises"][0]["button"] == "Далі"
    assert lesson["title"] == {"sk": "Aký som človek?", "uk": "Яка я людина?", "ru": "Какой я человек?", "en": "What kind of person am I?"}
    assert lesson["words"][0]["ru"] == "милый"
    assert lesson["words"][0]["en"] == "nice"
    assert lesson["words"][0]["exampleRu"] == "Он милый."
    assert lesson["words"][0]["exampleEn"] == "He is nice."
    assert lesson["exercises"][0]["question"]["en"] == "What does «veselý» mean?"
    assert lesson["exercises"][0]["options"][0]["text"]["ru"] == "милый"
    assert lesson["localization"]["uiLanguages"] == ["uk", "ru", "en"]


def test_regression_templates():
    assert m.fixed_translation("en", "Що тут сказати найприродніше?") == "What sounds most natural here?"
    assert m.fixed_translation("ru", "Що тут сказати найприродніше?") == "Что здесь звучит естественнее всего?"
    assert m.fixed_translation("en", "Що означає «veselý»?") == "What does «veselý» mean?"
    assert m.fixed_translation("ru", "Що означає «veselý»?") == "Что означает «veselý»?"
    assert m.fixed_translation("en", "Впиши словацькою: «як / ніж».") == "Write in Slovak: «as / than»."
    assert m.fixed_translation("ru", "Впиши словацькою: «як / ніж».") == "Напиши по-словацки: «как / чем»."


def test_rate_limit_backoff_policy():
    assert m.rate_limit_delay(0) == 8
    assert m.rate_limit_delay(1) == 16
    assert m.rate_limit_delay(2) == 32
    assert m.rate_limit_delay(3) == 45


if __name__ == "__main__":
    test_structure_preserved()
    test_regression_templates()
    test_rate_limit_backoff_policy()
    print("clean localization regression tests passed")
