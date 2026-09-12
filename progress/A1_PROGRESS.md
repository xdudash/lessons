# A1 Progress

## Status

**IN_PROGRESS — Section 02 production**

## Active production model
- Complete Slovak A1–C2 course.
- No predetermined total lesson quota.
- Lesson count is derived from atomic targets, prerequisites, review, transfer and mastery evidence.
- No filler lessons.
- GitHub `main` is the authoritative durable state.
- Student-facing instructions and exercise prompts are in Ukrainian; Slovak is the target language being learned/tested.

## Current A1 architecture
A1 currently has 14 thematic units with an initial working estimate of 82 lessons. The 82 count is provisional and is not a quota.

## Section 01
Section 01 — Sounds, reading and basic word structure — 6 lessons.
The six lesson files remain in `lessons/a1/` and are considered draft pending dedicated semantic/import QA.

## Current production
### A1 Section 02 — Me, you, he/she: introductions and personal data
Current planned lessons:
1. Kto som?
2. Ja, ty, on, ona, ono
3. My, vy, oni, ony
4. Pozdravy a lúčenie
5. Ako sa voláš?
6. Meno, vek, národnosť, adresa a telefón
7. Krátke predstavenie

All seven current lesson files have been authored in the real SlovakGo lesson contract.

## Lesson quality model
Each lesson follows the complete lesson envelope and the quality arc:
**TARGET → THEORY → EXAMPLES → VOCABULARY → CONTROLLED PRACTICE → CONTEXT → PRODUCTION → COMMUNICATION → REAL LIFE → MASTERY EVIDENCE**.

## Import/language contract
- Repository lesson JSON uses the actual SlovakGo `Lesson` contract.
- The file is wrapped as `{"lessons":[...]}` for import.
- Student-facing instructions, questions, hints and explanatory feedback are Ukrainian.
- Slovak is used for target-language forms and answer choices where the learner is testing Slovak.
- Do not return to Slovak-only exercise instructions.

## QA
A dedicated import/semantic QA pass is required after the section batch is written. Passing JSON syntax alone is not enough.

## Next task
Run Section 02 import/semantic QA, repair hard failures, then continue with Section 03.
