from __future__ import annotations

import importlib
import importlib.util


def fixes_module():
    spec = importlib.util.find_spec("translation_fixes")
    assert spec is not None, "translation_fixes module is missing"
    return importlib.import_module("translation_fixes")


def check(target: str, source: str, expected: str) -> None:
    m = fixes_module()
    got = m.fixed_translation(target, source)
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
