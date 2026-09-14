# SlovakGo B1 — Progress

## Status
**COMPLETE — 100 / 100 active lessons**

B1 follows `B1/LESSON_PLAN.md`. The active JSON lessons are stored in `lessons/b1/`.

## Sections
- S01 `l01–l06` — complete
- S02 `l07–l12` — complete
- S03 `l13–l18` — complete
- S04 `l19–l24` — complete
- S05 `l25–l30` — complete
- S06 `l31–l36` — complete
- S07 `l37–l42` — complete
- S08 `l43–l48` — complete
- S09 `l49–l54` — complete
- S10 `l55–l60` — complete
- S11 `l61–l66` — complete
- S12 `l67–l72` — complete
- S13 `l73–l78` — complete
- S14 `l79–l84` — complete
- S15 `l85–l90` — complete
- S16 `l91–l100` — complete

## QA gates
- 100 lesson files generated from `B1/LESSON_PLAN.md`.
- Each active lesson has `sk`, `uk`, `ru`, `en` in core localized fields.
- `localization.uiLanguages = ["uk", "ru", "en"]`, `targetLanguage = "sk"`, `fallbackUiLanguage = "uk"`.
- Vocabulary, `wordsScreen`, exercises and `finalSituation` are structurally checked by `tools/qa_b1.py`.
- Full `nextLesson` chain L01→L100 is verified; L100 is terminal.
