# SlovakGo — Master Rules

## Purpose
Build a complete Slovak course from A1 through C2. Completeness is defined by CEFR outcomes, Slovak-specific grammar/vocabulary/functions, communicative competence, progression and demonstrated mastery.

## Source of truth
- GitHub `main` is the durable repository state.
- `docs/SSD_CONCEPT.md` defines how to return to the project, understand status and continue safely.
- `docs/LESSON_PRODUCTION_REPORT.md` records current production evidence and known follow-up areas.
- `docs/NEXT_WORK_CHECKLIST.md` is the required pre-flight checklist before lesson edits.
- A1: `curriculum/A1_MASTER_LESSON_PLAN.md`.
- A2: `A2/LESSON_PLAN.md`.
- B1–C2: the corresponding level-folder `LESSON_PLAN.md`.
- `curriculum/COURSE_ARCHITECTURE_V2.md` defines curriculum architecture.
- `AGENTS.md` is the single operational contract for AI agents.
- Current SlovakGo application schema/runtime behavior is the lesson-format authority when it differs from stale local assumptions.

## Language
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Slovenian (`slovenščina`) must never be substituted for Slovak.

## Course volume targets
Working volumes guide planning but are not CEFR quotas: A1 ~80, A2 ~90, B1 ~100, B2 ~100, C1 ~90, C2 ~70. Final counts change only through deliberate curriculum revision; never add filler just to hit a number.

The current approved A2 map contains 15 sections × 6 lessons = 90 active lessons. A2 expands completed A1 rather than restarting it.

## Learning progression
NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY.
These are learning functions, not mandatory fixed screens.

## Lesson format
The canonical envelope is level-generic:

```json
{"lessons":[{"id":"a2-sNN-lNN", "sectionId":"a2_sNN", "level":"A2"}]}
```

The complete lesson structure follows `AGENTS.md` plus the current SlovakGo application schema/runtime checker. Do not preserve an old A1-only mechanics list as a universal contract.

## Quality gates
A production-final lesson must pass applicable gates: JSON/schema validity; runtime-compatible envelope and exercise encoding; natural Slovak; Ukrainian learner UI; CEFR/prerequisite fit; answer integrity; vocabulary ownership/review; progression/transfer; duplicate/obsolete-file checks; and remote GitHub read-back.

A2 additionally requires A1→A2 ownership control and a full 90-lesson chain ending at terminal `a2-s15-l90`.

## SSD concept
SSD means **Source / Status / Decisions**:

- **Source:** every lesson change starts from the authoritative level plan, JSON contract, schema/runtime checker and current GitHub `main`.
- **Status:** every completed batch updates the relevant progress file and production report.
- **Decisions:** every non-obvious rule, trade-off or known limitation is written down before the next session forgets it.

This repository must be understandable after a cold start. A future agent should be able to open `README.md`, follow the SSD documents and continue without relying on chat memory.

## Repository hygiene
Keep one authoritative instruction document (`AGENTS.md`) and one authoritative lesson map per level. Temporary generators, one-shot workflows and stale audits are removed after successful production unless they have continuing value.

## Failure handling
STOP → IDENTIFY → REPAIR → REVALIDATE THE WHOLE AFFECTED SET → COMMIT.
Never continue dependent production on top of a known invalid state.

## Return-to-work protocol
1. Pull/read current `main`.
2. Read `README.md`, `docs/SSD_CONCEPT.md`, `docs/LESSON_PRODUCTION_REPORT.md` and `docs/NEXT_WORK_CHECKLIST.md`.
3. Read the target level plan and progress file.
4. Identify whether the work is production, errata, QA hardening or documentation.
5. Update source rules/generators before regenerating affected lessons.
6. Run the full affected QA.
7. Update status/report documents.
8. Commit and publish only after fresh verification.
