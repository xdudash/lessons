# SlovakGo Lesson Production Report

Last updated: 2026-09-14

## Global Status

| Level | Status | Active lessons | JSON directory | QA command |
|---|---|---:|---|---|
| A1 | Complete | 75 | `lessons/a1/` | `python tools/qa_a1.py` |
| A2 | Complete | 90 | `lessons/a2/` | app/runtime QA previously required; local progress documents retained |
| B1 | Complete | 100 | `lessons/b1/` | `python tools/qa_b1.py` |
| B2 | Complete | 100 | `lessons/b2/` | `python tools/qa_b2.py` |
| C1 | Complete | 90 | `lessons/c1/` | `python tools/qa_c1.py` |
| C2 | Complete | 70 | `lessons/c2/` | `python tools/qa_c2.py` |

## Production Evidence

- A1 has 75 active lessons and intentionally skips retired IDs `l12-l17`.
- A2 has 90 active lessons from `A2/LESSON_PLAN.md`.
- B1 has 100 active lessons from `B1/LESSON_PLAN.md`.
- B2 has 100 active lessons from `B2/LESSON_PLAN.md`.
- C1 has 90 active lessons from `C1/LESSON_PLAN.md`.
- C2 has 70 active lessons from `C2/LESSON_PLAN.md`.
- B1-C2 include `sk`, `uk`, `ru`, `en` localization fields in generated lesson structures.
- B1-C2 QA verifies identity, localization, word references, exercise references, supported exercise types and `nextLesson` chains.

## Required Commands Before Claiming Completion

Run the command for every affected level:

```bash
python tools/qa_b1.py
python tools/qa_b2.py
python tools/qa_c1.py
python tools/qa_c2.py
```

For A1/A2 or app import work, also run the real SlovakGo application schema/runtime checker when available. Do not claim real app import success from local Python QA alone.

## Known Limitations

- The repository contains structural QA for B1-C2. Real application importer validation must still be treated as the final authority when available.
- Some generated higher-level lessons use reusable exercise templates. They are structurally valid, but future quality passes should increase semantic variety.
- C2 vocabulary is complete structurally. Some rare terms may need a manual translation-quality pass to replace neutral fallback explanations with precise learner translations.
- Progress reporting was added after several levels were already generated, so older commits may not contain the full report trail.

## Recommended Next Improvements

1. Add a global inventory script that counts lessons, validates chains and reports missing progress files across all levels.
2. Add a vocabulary-quality QA that flags fallback translations, repeated generic examples and weak distractors.
3. Connect the repository QA to the real SlovakGo app importer/runtime checker.
4. Build a per-level semantic QA checklist: CEFR fit, natural Slovak, Ukrainian clarity, answer ambiguity and transfer quality.
5. Improve C2 vocabulary translations and examples in one focused pass before product publication.

## Publication Rule

Only publish to `main` after:

- affected level QA passes fresh;
- status/progress docs are updated;
- remote read-back confirms the expected files exist on GitHub;
- known limitations are recorded honestly.
