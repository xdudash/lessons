# SlovakGo — Slovak language course

This repository is the durable source of truth for the SlovakGo course.

## Current project model
- The curriculum is CEFR-based and content-led.
- A1 has one authoritative lesson map in `curriculum/A1_MASTER_LESSON_PLAN.md`.
- Lesson count follows pedagogical targets, prerequisites, review, transfer and mastery needs.
- Production may use batches of three coherent sections; this does **not** mean three lessons per section.
- GitHub `main` is the source of truth.

## Language policy
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.

## Lesson JSON
All active lesson files use the real importer-compatible format. The known-working `lesson-181-a1_slovakgo.json` is a **format reference only**; its number is not used for numbering.

Canonical envelope:

```json
{"lessons":[{"id":"a1-sXX-lYY"}]}
```

The detailed field-level contract is maintained in `AGENTS.md`.

## Repository map
- `AGENTS.md` — single operational contract for agents.
- `MASTER.md` — concise project rules.
- `curriculum/A1_MASTER_LESSON_PLAN.md` — authoritative A1 lesson-by-lesson map.
- `curriculum/COURSE_ARCHITECTURE_V2.md` — curriculum architecture and learning goals.
- `curriculum/GOLD_STANDARD_LESSON.md` — lesson quality reference.
- `knowledge/` — current target, prerequisite and vocabulary guidance.
- `lessons/a1/` — active A1 lesson JSON.
- `progress/A1_PROGRESS.md` — current durable progress and next task.

## Hygiene rule
Obsolete lesson files, generators, audits and duplicate instruction documents are removed rather than kept as competing sources of truth.
