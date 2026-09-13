from __future__ import annotations

import importlib


def main() -> None:
    m = importlib.import_module("localize_google")

    raw = "<<<SEG0000>>> First line\ncontinues.\n<<<SEG0001>>> Second line."
    parsed = m.parse_marked(raw, [0, 1])
    assert parsed == {0: "First line\ncontinues.", 1: "Second line."}, parsed

    texts = ["a" * 700, "b" * 700, "short"]
    batches = m.pack_batches(texts, max_chars=1000, max_items=10)
    assert [len(x) for x in batches] == [1, 2], batches
    assert sum(len(x) for x in batches) == 3

    assert m.choose_lexical_candidate(
        source_uk="симпатичний",
        uk_candidate="sympathetic",
        uk_back="співчутливий",
        sk_candidate="likable",
        sk_back="симпатичний",
    ) == "likable"
    assert m.choose_lexical_candidate(
        source_uk="спокійний",
        uk_candidate="calm",
        uk_back="спокійний",
        sk_candidate="peaceful",
        sk_back="мирний",
    ) == "calm"
    assert m.choose_lexical_candidate(
        source_uk="милий",
        uk_candidate="nice",
        uk_back="приємний",
        sk_candidate="dear",
        sk_back="дорогий",
    ) == "nice"

    print("google batch and lexical-selection tests passed")


if __name__ == "__main__":
    main()
