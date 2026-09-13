# A1 Progress

## Current state
**Section 01 rebuilt, validated and committed. Section 02 is next.**

`lessons/a1/` currently contains the six active Section 01 lesson JSON files (`l01–l06`). Later A1 sections are still planned work and must not be reported as generated until their files actually exist in `main`.

## Canonical rules
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Lesson IDs, section ranges and ordering come from `curriculum/A1_MASTER_LESSON_PLAN.md`.
- Runtime compatibility is checked against the current `xdudash/slovakGo` importer, renderers, `exerciseChecking.ts`, schema and `scripts/qa-lessons.ts`.
- `main` is the source of truth for committed lesson content.
- Historical lesson JSON is reference material only and is not automatically canonical.

## Section 01 — committed production
- `a1-s01-l01` — Slovenská abeceda
- `a1-s01-l02` — Samohlásky a spoluhlásky
- `a1-s01-l03` — Slabičné r a l
- `a1-s01-l04` — Mäkké spoluhlásky
- `a1-s01-l05` — Dĺžka a dvojhlásky
- `a1-s01-l06` — Prízvuk, intonácia a krátke správy

Each lesson contains three theory screens, a complete `wordsScreen` with runtime-visible fields, target vocabulary, twelve deterministic exercises, an interactive final situation and a result screen. `a1-s01-l06` links forward to the current master-map next lesson `a1-s02-l07`.

## QA state for Section 01
Completed checks:
- JSON parse for all six files;
- current runtime schema constraints for all six files;
- current application `qa:lessons` semantic/runtime-contract checks: 6/6 pass;
- word IDs and `wordsScreen` canonical consistency;
- unique exercise IDs and order values;
- deterministic answer paths using current checker encodings;
- final-situation determinism;
- manual adversarial review for vocabulary coverage, repeated questions, distractors and learner-facing Ukrainian;
- Slovak language review, including correction of the overgeneralized soft-consonant explanation in L04;
- remote verification: committed GitHub blob SHA values match the locally validated minified JSON byte-for-byte.

The content repository's legacy `tools/qa_a1.py` is not a runtime source of truth in its current form: it only whitelists an older exercise subset, requires the legacy `final_life_situation` shape and contains an obsolete `nextLesson` assertion. The current app runtime/schema/checker and `scripts/qa-lessons.ts` take precedence. The legacy script should be modernized before it is used as a level-completion gate.

## Active roadmap
The authoritative A1 map is `curriculum/A1_MASTER_LESSON_PLAN.md`. Important: retired old lesson numbers are not to be recreated merely to make numbering continuous; current master-map ranges are authoritative.

## Next work
Build Section 02 (`a1-s02-l07`–`a1-s02-l11`) in order, then validate and commit it with the same runtime-first QA cycle. Continue through the remaining A1 master-map sections before performing full A1 cross-lesson and cross-section QA.
