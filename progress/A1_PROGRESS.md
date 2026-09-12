# A1 Progress

## Status

**CLEAN / STABLE — Sections 01–05 are the current active lesson set. Sections 06–14 remain planned and are not stored as generated lessons until rebuilt against the canonical workflow.**

## Canonical production rules
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, prompts, explanations and UI text: Ukrainian.
- `lesson-181-a1_slovakgo.json` is a working importer-format reference only. Its number is never reused for numbering.
- Lesson count follows the current master lesson plan and pedagogical need.
- One production batch may contain three sections, but each section keeps its own planned lesson count.
- GitHub `main` is the durable source of truth.

## Active lesson set
### Section 01
`a1-s01-l01` through `a1-s01-l06`

### Section 02
`a1-s02-l07` through `a1-s02-l11` — five denser accepted lessons.

### Section 03
`a1-s03-l18` through `a1-s03-l22` — current rebuilt set.

### Section 04
`a1-s04-l23` through `a1-s04-l26` — current rebuilt set.

### Section 05
`a1-s05-l27` through `a1-s05-l30` — current rebuilt set.

## Retired / removed content
- Historical numerical `a1-s03-l12` through `a1-s03-l17` files are retired and removed from the active tree.
- Temporary generated lesson files for Sections 06–14 were removed during repository cleanup because they were not sufficiently quality-controlled.
- Temporary automatic-generation workflow/scripts that could recreate those low-quality files were removed/disabled pending a clean rebuild.

## Planned curriculum
The full 14-section A1 roadmap remains in `curriculum/A1_MASTER_LESSON_PLAN.md` and `curriculum/COURSE_ARCHITECTURE_V2.md`.

Sections 06–14 are planned as:
- Section 06 — l31–l37
- Section 07 — l38–l43
- Section 08 — l44–l50
- Section 09 — l51–l56
- Section 10 — l57–l62
- Section 11 — l63–l67
- Section 12 — l68–l72
- Section 13 — l73–l76
- Section 14 — l77–l81

These are roadmap IDs, not claims that the lesson files are currently present.

## QA state
- Active lesson tree contains only the accepted current set.
- Structural/reference QA is configured for active Sections 01–05 in `tools/qa_a1.py`.
- Full semantic QA must be completed before a newly rebuilt section is called complete.
- Real application importer: NOT CLAIMED unless actually run in the application.

## Operating rule after cleanup
Do not restore or generate future lesson files by copying old temporary generators. Rebuild future sections from the master lesson plan and the known-working importer contract, then run batch-wide structural, semantic and adversarial QA before committing them.
