# A1 Progress

## Current state
**Sections 01–03 rebuilt, validated and committed. Section 04 is next.**

`lessons/a1/` currently contains 16 active lesson JSON files: Section 01 (`l01–l06`), Section 02 (`l07–l11`) and Section 03 (`l18–l22`). Retired `l12–l17` are intentionally absent. Later A1 sections remain planned work and must not be reported as generated until their files actually exist in `main`.

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

## Section 03 — committed production
- `a1-s03-l18` — Rodina
- `a1-s03-l19` — Ľudia
- `a1-s03-l20` — Môj, moja, moje
- `a1-s03-l21` — Aký je? Aká je?
- `a1-s03-l22` — Moja rodina

Section 03 follows the current master theme “people, family and describing people” while keeping current IDs `l18–l22`. It does not restore retired old IDs. The progression is family vocabulary → people and polite address → possessive agreement → simple person description → integrated family-photo situation.

## QA state — 16 committed lessons
Completed checks on the full current A1 set:
- JSON parse: 16/16;
- current runtime schema constraints: 16/16 pass;
- current application `qa:lessons` semantic/runtime-contract checks: 16/16 pass;
- word IDs and complete `wordsScreen` canonical consistency;
- unique exercise IDs and order values;
- deterministic answer paths using current checker encodings;
- final-situation determinism;
- learner-facing Ukrainian and Slovak language review;
- adversarial target-vocabulary coverage review;
- remote verification: committed GitHub blob SHA values match the locally validated minified JSON byte-for-byte.

Adversarial review of Section 02 found six target items that were originally visible on vocabulary cards but not retrieved in practice (`Bratislava`, `Košice`, `ulica`, `jazyk`, and two `dobre` ownership occurrences). Those gaps were repaired before commit.

Section 03 review also removed a premature `sme` example from L22 so the lesson stays within the current prerequisite progression; the final version uses already-supported `je/sú` chunks instead. The complete 16-lesson set was retested after that correction.

The content repository's legacy `tools/qa_a1.py` is not a runtime source of truth in its current form: it only whitelists an older exercise subset, requires the legacy `final_life_situation` shape and contains an obsolete `nextLesson` assertion. The current app runtime/schema/checker and `scripts/qa-lessons.ts` take precedence. The legacy script should be modernized before it is used as a level-completion gate.

## Active roadmap
The authoritative A1 map is `curriculum/A1_MASTER_LESSON_PLAN.md`. Current next range is Section 04, `a1-s04-l23`–`a1-s04-l26`.

## Next work
Build Section 04 (`a1-s04-l23`–`a1-s04-l26`) in order, validate and commit each lesson with the same runtime-first QA cycle, then continue through the remaining A1 master-map sections before full A1 cross-lesson and cross-section QA.
