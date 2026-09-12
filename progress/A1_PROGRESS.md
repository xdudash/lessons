# A1 Progress

## Status

**IN_PROGRESS — Section 01 production**

## Active production model
- Complete Slovak A1–C2 course.
- No predetermined total lesson quota.
- Lesson count is derived from atomic targets, prerequisites, review, transfer and mastery evidence.
- No filler lessons.
- GitHub `main` is the authoritative durable state.

## Current A1 architecture
A1 currently has 14 thematic units with an initial working estimate of 82 lessons. The 82 count is provisional and is not a quota.

## Completed current work

### A1 Section 01 — Sounds, reading and basic word structure
Current planned lessons:
1. Slovenská abeceda
2. Samohlásky a spoluhlásky
3. Slabikotvorné r, ŕ, l, ĺ
4. Mäkké spoluhlásky a výslovnosť
5. Dĺžka, dvojhlásky a rytmus
6. Prízvuk, intonácia a krátke správy

All six current lesson files are present in `lessons/a1/`.

## Lesson quality model
Each lesson follows the complete lesson envelope and the quality arc:
**TARGET → THEORY → EXAMPLES → VOCABULARY → CONTROLLED PRACTICE → CONTEXT → PRODUCTION → COMMUNICATION → REAL LIFE → MASTERY EVIDENCE**.

The canonical gold standard remains `lessons/a1/a1-s01-l01.json` from the previous production history; its exact content is not copied as a template.

## QA
The Section 01 files have been structurally authored against the current lesson contract: top-level `lessons` envelope, metadata, theory, vocabulary, exercises, final situation and result screen. A dedicated semantic QA pass is still required before the section is considered production-final.

## Next task
Run the Section 01 QA pass, repair any hard failures, verify the GitHub tree, and only then mark Section 01 production-final. After that continue to the next curriculum-defined section.
