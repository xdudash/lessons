# SlovakGo — Master Rules

## Purpose
Build a complete Slovak course from A1 through C2. Completeness is defined by CEFR outcomes, Slovak-specific grammar/vocabulary/functions, communicative competence, progression and demonstrated mastery.

## Source of truth
- GitHub `main` is the durable repository state.
- `curriculum/A1_MASTER_LESSON_PLAN.md` is the authoritative current A1 lesson map.
- `curriculum/COURSE_ARCHITECTURE_V2.md` defines the curriculum architecture and section goals.
- `AGENTS.md` is the single operational contract for AI agents.
- `curriculum/GOLD_STANDARD_LESSON.md` defines the lesson-quality floor.
- Level folders `A1/` through `C2/` contain the lesson plans for each CEFR level.
- Chat history is never a substitute for checking the repository.

## Language
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Slovenian (`slovenščina`) must never be substituted for Slovak.

## Course volume targets
These are practical working targets for course planning, not official CEFR vocabulary quotas or rigid lesson quotas:

| Level | Target lesson volume |
|---|---:|
| A1 | ~80 lessons |
| A2 | ~90 lessons |
| B1 | ~100 lessons |
| B2 | ~100 lessons |
| C1 | ~90 lessons |
| C2 | ~70 lessons |
| **Total** | **~530 lessons** |

The final count can change when curriculum and mastery evidence justify it. Do not add filler lessons solely to hit a number.

For each level, the corresponding folder contains its lesson-plan document. Lesson JSON is stored separately in the active lesson tree.

## A1 production model
The current A1 plan is the working roadmap. Lesson counts come from the master lesson map and can be revised only deliberately when pedagogical evidence requires it.

Production may be organized in batches of three coherent sections, but **three sections never means three lessons per section**. The section's own approved lesson count always wins.

## Learning progression
The default learning arc is:

**NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY**

These are learning functions, not mandatory fixed screens.

## Lesson format
The importer-compatible lesson format is established by the known-working lesson example used by the project. In particular, `lesson-181-a1_slovakgo.json` is a **format reference only**. Its number must never be copied into lesson numbering.

The canonical top-level form is:

```json
{"lessons":[{"id":"a1-sXX-lYY", "sectionId":"a1_sXX", "level":"A1"}]}
```

The complete lesson structure must follow `AGENTS.md` and the real working importer contract.

## Quality gates
A lesson is production-final only after applicable checks pass:

1. JSON/schema validity;
2. complete importer-compatible envelope;
3. correct and natural Slovak;
4. learner-facing Ukrainian;
5. CEFR and prerequisite fit;
6. exercise integrity and answer correctness;
7. vocabulary ownership and meaningful review;
8. progression and transfer;
9. no accidental duplicates or obsolete files;
10. GitHub tree/read-back verification.

Real application import is a separate gate and must never be claimed unless actually run.

## Repository hygiene
Keep one authoritative instruction document: `AGENTS.md`.
Keep one authoritative A1 lesson map: `curriculum/A1_MASTER_LESSON_PLAN.md`.
Keep one lesson-plan document inside each level folder `A1/` through `C2/`.
Do not preserve obsolete generators, protocol duplicates, retired audits or historical lesson files in the active tree.
Do not weaken valid lesson content to work around an application bug; track UI limitations separately.

## Failure handling
If a hard failure appears:

**STOP → IDENTIFY → REPAIR → REVALIDATE THE WHOLE AFFECTED SET → COMMIT.**

Never continue dependent production on top of a known invalid state.
