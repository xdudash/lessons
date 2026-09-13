from __future__ import annotations

import localize_a1_a2 as m


def fixed(target: str, source: str):
    fn = getattr(m, "fixed_translation", None)
    return fn(target, source) if fn else None


def check(target: str, source: str, expected: str) -> None:
    got = fixed(target, source)
    assert got == expected, f"{target} {source!r}: expected {expected!r}, got {got!r}"


def main() -> None:
    cases = [
        ("en", "Що тут сказати найприродніше?", "What sounds most natural here?"),
        ("ru", "Що тут сказати найприродніше?", "Что здесь звучит естественнее всего?"),
        ("en", "Що означає «veselý»?", "What does «veselý» mean?"),
        ("ru", "Що означає «veselý»?", "Что означает «veselý»?"),
        ("en", "Впиши словацькою: «як / ніж».", "Write in Slovak: «as / than»."),
        ("ru", "Впиши словацькою: «як / ніж».", "Напиши по-словацки: «как / чем»."),
        ("en", "Правда чи ні? «zaujímavý» означає «цікавий».", "True or false? «zaujímavý» means «interesting»."),
        ("ru", "Правда чи ні? «zaujímavý» означає «цікавий».", "Правда или нет? «zaujímavý» означает «интересный»."),
    ]
    for target, source, expected in cases:
        check(target, source, expected)
    print(f"translation regression cases: {len(cases)} passed")


if __name__ == "__main__":
    main()
