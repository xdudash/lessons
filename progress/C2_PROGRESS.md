# SlovakGo C2 — Progress

## Status

**COMPLETE — 70 / 70 active lessons**

C2 follows `C2/LESSON_PLAN.md`. The active JSON lessons are stored in `lessons/c2/`.

## Sections

- S01 `l001-l005` — complete
- S02 `l006-l010` — complete
- S03 `l011-l015` — complete
- S04 `l016-l020` — complete
- S05 `l021-l025` — complete
- S06 `l026-l030` — complete
- S07 `l031-l035` — complete
- S08 `l036-l040` — complete
- S09 `l041-l045` — complete
- S10 `l046-l050` — complete
- S11 `l051-l055` — complete
- S12 `l056-l060` — complete
- S13 `l061-l065` — complete
- S14 `l066-l070` — complete

## QA Gates

- 70 lesson files generated from `C2/LESSON_PLAN.md`.
- Each active lesson has `sk`, `uk`, `ru`, `en` in core localized fields.
- `localization.uiLanguages = ["uk", "ru", "en"]`, `targetLanguage = "sk"`, `fallbackUiLanguage = "uk"`.
- Vocabulary, `wordsScreen`, exercises and `finalSituation` are structurally checked by `tools/qa_c2.py`.
- Full `nextLesson` chain L001→L070 is verified; L070 is terminal.
- `tools/qa_c2.py` rejects old generic fallback fragments such as `вираз`, `выражение`, `the expression` and `praktická fráza`.

## Known Limitation

C2 is structurally complete and import-shaped. Some rare vocabulary items still need a manual translation-quality pass to replace neutral C2 fallback wording with exact Ukrainian/Russian/English learner translations.

## Follow-Up

Recommended next C2 pass: improve vocabulary translations, diversify advanced examples and add more C2-specific discourse tasks for style, implication, argumentation and editing.
