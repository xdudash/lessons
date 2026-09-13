# A1 Progress

## Current state
**Section 01 rebuilt / QA review in progress**

The repository contains the accepted active lesson set for Sections 01–05. Section 01 is the current rebuilt batch and follows the authoritative master lesson map: six lessons, `l01–l06`.

## Canonical rules
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- `lesson-181-a1_slovakgo.json` is a format/importer reference only; its number is never reused for lesson numbering.
- Lesson IDs and counts come only from `curriculum/A1_MASTER_LESSON_PLAN.md`.
- `main` is the source of truth.

## Active lessons
| Section | Theme | Active lesson range |
|---|---|---|
| 01 | Sounds, reading and basic word structure | `l01–l06` |
| 02 | Me, you, he/she: introductions and personal data | `l07–l11` |
| 03 | People, family and describing people | `l18–l22` |
| 04 | Things, possession and my world | `l23–l26` |
| 05 | Home, rooms and location of things | `l27–l30` |

## Section 01 production
- `a1-s01-l01` — Slovenská abeceda
- `a1-s01-l02` — Samohlásky a spoluhlásky
- `a1-s01-l03` — Slabičné r a l
- `a1-s01-l04` — Mäkké spoluhlásky
- `a1-s01-l05` — Dĺžka a dvojhlásky
- `a1-s01-l06` — Prízvuk, intonácia a krátke správy

## QA state
Section 01 files have been reviewed against the mandatory lesson envelope, supported exercise types, local cross-references, vocabulary/screen consistency and the semantic QA rules. L04–L05 were repaired after review to remove untaught transfer items and improve lesson-target coverage.

The repository's `tools/qa_a1.py` contains a known `nextLesson` assertion that conflicts with the mandatory JSON contract/AGENTS format at the Section 01 → Section 02 boundary. Do not claim repository-wide QA PASS until that canonical inconsistency is resolved and the script is actually executed.

Real application import is a separate state and must not be claimed unless actually run.

## Full roadmap
The full 14-section roadmap and lesson-by-lesson map is maintained in:
- `curriculum/A1_MASTER_LESSON_PLAN.md` — authoritative lesson map.
- `curriculum/COURSE_ARCHITECTURE_V2.md` — curriculum architecture and section goals.
- `curriculum/GOLD_STANDARD_LESSON.md` — pedagogical/lesson quality reference.
