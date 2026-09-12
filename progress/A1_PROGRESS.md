# A1 Progress

## Current state
**CLEAN / STABLE**

The repository currently contains the accepted active lesson set for Sections 01–05 only. Sections 06–14 are roadmap content and are not represented by generated lesson files.

## Canonical rules
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- `lesson-181-a1_slovakgo.json` is a format/importer reference only; its number is never reused for lesson numbering.
- Lesson IDs and counts come only from `curriculum/A1_MASTER_LESSON_PLAN.md`.
- A production batch may contain three sections, but each section keeps its own planned lesson count.
- `main` is the source of truth.

## Active lessons
| Section | Theme | Active lesson range |
|---|---|---|
| 01 | Sounds, reading and basic word structure | `l01–l06` |
| 02 | Me, you, he/she: introductions and personal data | `l07–l11` |
| 03 | People, family and describing people | `l18–l22` |
| 04 | Things, possession and my world | `l23–l26` |
| 05 | Home, rooms and location of things | `l27–l30` |

## Retired material
- Historical numerical `a1-s03-l12`–`l17` files are retired and removed. Numbers/time/dates belong to Section 07 in the canonical plan.
- Temporary generated `l31–l81` lesson files were removed because they were not quality-controlled to the required standard.
- Automatic generation scripts/workflows that could recreate those temporary files were removed.
- Duplicate documents that restated the agent protocol were removed; `AGENTS.md` is now the single agent instruction source.
- The old `audits/A1_250_AUDIT.md` document was removed because it described an obsolete build state.

## Full roadmap
The full 14-section roadmap and lesson-by-lesson map is maintained in:
- `curriculum/A1_MASTER_LESSON_PLAN.md` — authoritative lesson map.
- `curriculum/COURSE_ARCHITECTURE_V2.md` — curriculum architecture and section goals.
- `curriculum/GOLD_STANDARD_LESSON.md` — pedagogical/lesson quality reference.

## Supporting knowledge
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `knowledge/a1_vocab_matrix/README.md`

## QA state
The active lesson set is the cleaned repository state. Future rebuilt sections must pass JSON/schema checks, semantic/adversarial review and repository read-back before being marked complete. Real application import is a separate state and must not be claimed unless actually run.

## Next production rule
When future sections are created, use the master lesson plan for exact IDs/counts, use the known-working lesson JSON only for format, generate the complete section before commit, QA the complete set, then read it back from `main`. Never restore the removed universal generators.
