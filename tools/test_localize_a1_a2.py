from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("localize_a1_a2.py")
spec = importlib.util.spec_from_file_location("localize_a1_a2", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_mixed_slovak_tokens_are_never_sent_to_translation() -> None:
    splitter = getattr(module, "split_translation_segments", None)
    assert splitter is not None, "split_translation_segments must exist"

    text = "Обери č, š, ž, ď, ľ, ň, ô та слово môj у реченні."
    parts = splitter(text)

    assert "".join(piece for _translate, piece in parts) == text
    translated = [piece for translate, piece in parts if translate]
    literal = [piece for translate, piece in parts if not translate]

    assert translated, "the Ukrainian part must still be translated"
    assert all(not module.LATIN_TOKEN.search(piece) for piece in translated)
    for token in ("č", "š", "ž", "ď", "ľ", "ň", "ô", "môj"):
        assert any(token in piece for piece in literal), token


def test_pure_ukrainian_sentence_is_one_translatable_segment() -> None:
    splitter = getattr(module, "split_translation_segments", None)
    assert splitter is not None, "split_translation_segments must exist"
    text = "Продовжуй читати точно."
    assert splitter(text) == [(True, text)]


if __name__ == "__main__":
    test_mixed_slovak_tokens_are_never_sent_to_translation()
    test_pure_ukrainian_sentence_is_one_translatable_segment()
    print("segment tests passed")
