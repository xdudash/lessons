from __future__ import annotations

import copy

from localize_json_only import localize_document


def fake_translate(target: str, text: str) -> str:
    return f"{target}:{text}"


def main() -> None:
    original = {
        "lessons": [{
            "id": "x",
            "localization": {"uiLanguages": ["uk"], "targetLanguage": "sk", "fallbackUiLanguage": "uk"},
            "title": {"sk": "Názov", "uk": "Назва"},
            "startScreen": {
                "button": "Почати урок",
                "outcomes": ["розуміти зміст"],
            },
            "wordsScreen": {
                "title": {"uk": "Слова"},
                "items": [{"sk": "čaj", "uk": "чай", "exampleSk": "Čaj je teplý.", "exampleUk": "Чай теплий."}],
                "button": "До практики",
            },
            "exercises": [{
                "id": "e1",
                "type": "single_choice",
                "question": "Що означає «čaj»?",
                "button": "Далі",
                "options": [{"id": "a", "text": "чай", "correct": True}],
            }],
        }]
    }
    before = copy.deepcopy(original)
    out = localize_document(original, fake_translate)
    lesson = out["lessons"][0]

    assert lesson["localization"]["uiLanguages"] == ["uk", "ru", "en"]
    assert lesson["title"] == {"sk": "Názov", "uk": "Назва", "ru": "ru:Назва", "en": "en:Назва"}
    assert lesson["startScreen"]["button"] == before["lessons"][0]["startScreen"]["button"]
    assert lesson["wordsScreen"]["items"][0]["sk"] == "čaj"
    assert lesson["wordsScreen"]["items"][0]["uk"] == "чай"
    assert lesson["wordsScreen"]["items"][0]["ru"] == "ru:чай"
    assert lesson["wordsScreen"]["items"][0]["en"] == "en:чай"
    assert lesson["wordsScreen"]["items"][0]["exampleUk"] == "Чай теплий."
    assert lesson["wordsScreen"]["items"][0]["exampleRu"] == "ru:Чай теплий."
    assert lesson["wordsScreen"]["items"][0]["exampleEn"] == "en:Чай теплий."
    assert lesson["exercises"][0]["question"]["uk"] == "Що означає «čaj»?"
    assert lesson["exercises"][0]["question"]["ru"] == "ru:Що означає «čaj»?"
    assert lesson["exercises"][0]["question"]["en"] == "en:Що означає «čaj»?"
    assert lesson["exercises"][0]["button"] == "Далі"
    assert lesson["exercises"][0]["options"][0]["text"]["uk"] == "чай"

    print("json-only localization regression passed")


if __name__ == "__main__":
    main()
