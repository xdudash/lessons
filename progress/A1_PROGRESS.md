# A1 Progress

## Status

**IN_PROGRESS — Section 02 rebuilt**

## Active production model
- Complete Slovak A1–C2 course.
- No predetermined total lesson quota.
- Lesson count is derived from atomic targets, prerequisites, review, transfer and mastery evidence.
- No filler lessons.
- GitHub `main` is the authoritative durable state.
- Student-facing instructions and exercise prompts are in Ukrainian; Slovak is the target language being learned/tested.

## Current A1 architecture
A1 currently has 14 thematic units. The working total remains provisional and is not a quota.

## Section 01
Section 01 — Sounds, reading and basic word structure — 6 lessons.
The six lesson files remain in `lessons/a1/` and require dedicated semantic/import QA.

## Section 02 — O mne
Section 02 has been rebuilt from seven narrow lessons into five denser lessons. The five-lesson design preserves the section outcomes while increasing lexical depth, contextual practice and transfer.

### Lesson sequence
1. `a1-s02-l07` — Kto som? — identity, byť, professions, languages and basic self-description
2. `a1-s02-l08` — Ja, ty, on, ona, ono — singular pronouns, agreement cues and reference in context
3. `a1-s02-l09` — Zoznámime sa — greetings, formal/informal contact, asking and giving names, polite meeting formulas
4. `a1-s02-l10` — O mne — age, origin, residence, city, address, phone number and languages
5. `a1-s02-l11` — Predstavím sa — integrated introduction, form completion, question-answer exchange, short message and transfer

### Lesson design
Each lesson is a complete lesson envelope with:
- 2 theory screens;
- expanded working vocabulary, normally 12–20 meaningful lexical items/phrases;
- 16 varied exercises;
- contextual reading/dialogue practice;
- production-oriented transfer;
- 3-step final real-life situation;
- Ukrainian learner-facing instructions with Slovak target language.

### QA policy
Section 02 is considered rebuilt only after JSON parsing, structural checks, Slovak naturalness, exercise-answer validity, localization, progression and overlap checks pass.

## Next task
Run dedicated semantic/import QA on the rebuilt Section 02, repair any hard failures, then proceed to Section 03.
