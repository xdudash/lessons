# SlovakGo C1 — Progress

## Status

**COMPLETE — 90 / 90 active lessons**

C1 follows `C1/LESSON_PLAN.md`. The active JSON lessons are stored in `lessons/c1/`.

## Sections

- S01 `l001-l006` — complete
- S02 `l007-l012` — complete
- S03 `l013-l018` — complete
- S04 `l019-l024` — complete
- S05 `l025-l030` — complete
- S06 `l031-l036` — complete
- S07 `l037-l042` — complete
- S08 `l043-l048` — complete
- S09 `l049-l054` — complete
- S10 `l055-l060` — complete
- S11 `l061-l066` — complete
- S12 `l067-l072` — complete
- S13 `l073-l078` — complete
- S14 `l079-l084` — complete
- S15 `l085-l090` — complete

## QA Gates

- 90 lesson files generated from `C1/LESSON_PLAN.md`.
- Each active lesson has `sk`, `uk`, `ru`, `en` in core localized fields.
- `localization.uiLanguages = ["uk", "ru", "en"]`, `targetLanguage = "sk"`, `fallbackUiLanguage = "uk"`.
- Vocabulary, `wordsScreen`, exercises and `finalSituation` are structurally checked by `tools/qa_c1.py`.
- Full `nextLesson` chain L001→L090 is verified; L090 is terminal.

## Follow-Up

C1 is content-complete. Future changes should focus on semantic richness, manually reviewed vocabulary translations, app-runtime QA and more varied C1 production tasks.
