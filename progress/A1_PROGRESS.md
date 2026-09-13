# A1 Progress

## Current state
**Sections 01–02 rebuilt, validated and committed. Section 03 is next.**

`lessons/a1/` currently contains 11 active lesson JSON files: Section 01 (`l01–l06`) and Section 02 (`l07–l11`). Later A1 sections remain planned work and must not be reported as generated until their files actually exist in `main`.

## Canonical rules
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Lesson IDs, section ranges and ordering come from `curriculum/A1_MASTER_LESSON_PLAN.md`.
- Runtime compatibility is checked against the current `xdudash/slovakGo` importer, renderers, `exerciseChecking.ts`, schema and `scripts/qa-lessons.ts`.
- `main` is the source of truth for committed lesson content.
- Historical lesson JSON is reference material only and is not automatically canonical.
- Retired lesson numbers `l12–l17` are not recreated merely to make numbering continuous.

## Section 01 — committed production
- `a1-s01-l01` — Slovenská abeceda
- `a1-s01-l02` — Samohlásky a spoluhlásky
- `a1-s01-l03` — Slabičné r a l
- `a1-s01-l04` — Mäkké spoluhlásky
- `a1-s01-l05` — Dĺžka a dvojhlásky
- `a1-s01-l06` — Prízvuk, intonácia a krátke správy

## Section 02 — committed production
- `a1-s02-l07` — Kto som?
- `a1-s02-l08` — Odkiaľ som?
- `a1-s02-l09` — Kde bývam?
- `a1-s02-l10` — Akým jazykom hovorím?
- `a1-s02-l11` — Predstavím sa

Section 02 deliberately avoids introducing age/numbers and a broad verb paradigm as new material. The current master progression places numbers in Section 07 and systematic present-tense work in Section 06. L11 therefore integrates name, origin, residence and language instead of leaking those later prerequisites.

## QA state — 11 committed lessons
Completed checks on the full current A1 set:
- JSON parse: 11/11;
- current runtime schema constraints: 11/11 pass;
- current application `qa:lessons` semantic/runtime-contract checks: 11/11 pass;
- word IDs and complete `wordsScreen` canonical consistency;
- unique exercise IDs and order values;
- deterministic answer paths using current checker encodings;
- final-situation determinism;
- learner-facing Ukrainian and Slovak language review;
- adversarial target-vocabulary coverage review;
- remote verification: committed GitHub blob SHA values match the locally validated minified JSON byte-for-byte.

Adversarial review of Section 02 found six target items that were originally visible on vocabulary cards but not retrieved in practice (`Bratislava`, `Košice`, `ulica`, `jazyk`, and two `dobre` ownership occurrences). Those gaps were repaired before commit and the complete 11-lesson set was retested successfully.

The content repository's legacy `tools/qa_a1.py` is not a runtime source of truth in its current form: it only whitelists an older exercise subset, requires the legacy `final_life_situation` shape and contains an obsolete `nextLesson` assertion. The current app runtime/schema/checker and `scripts/qa-lessons.ts` take precedence. The legacy script should be modernized before it is used as a level-completion gate.

## Active roadmap
The authoritative A1 map is `curriculum/A1_MASTER_LESSON_PLAN.md`. Current next range is Section 03, `a1-s03-l18`–`a1-s03-l22`, theme: people, family and describing people.

## Next work
Build Section 03 (`a1-s03-l18`–`a1-s03-l22`) in order, validate and commit each lesson with the same runtime-first QA cycle, then continue through the remaining A1 master-map sections before full A1 cross-lesson and cross-section QA.
