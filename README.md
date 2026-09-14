# SlovakGo — Slovak language course

This repository is the durable source of truth for the SlovakGo CEFR course A1–C2.

## Current project model
- Curriculum is CEFR-based and content-led.
- Each level has one authoritative lesson map: A1 uses `curriculum/A1_MASTER_LESSON_PLAN.md`; A2 uses `A2/LESSON_PLAN.md`; B1–C2 use their level-folder plans.
- Lesson count follows pedagogical targets, prerequisites, review, transfer and mastery needs.
- Production may use batches of three coherent sections; this does not mean three lessons per section.
- GitHub `main` is the durable source of truth.

## Language policy
- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.

## Lesson JSON
All active lesson files use the current importer/runtime-compatible format. Canonical IDs are level-specific, for example:

```json
{"lessons":[{"id":"a2-s01-l01","sectionId":"a2_s01","level":"A2"}]}
```

The detailed authoring/production contract is `AGENTS.md`; the current SlovakGo application schema and runtime checker define machine/runtime validity.

## Repository map
- `AGENTS.md` — operational production contract.
- `MASTER.md` — concise project rules.
- `A1/` … `C2/` — level lesson plans/reference material.
- `A2/LESSON_PLAN.md` — authoritative A2 map (90 active lessons).
- `curriculum/` — architecture and curriculum contracts.
- `knowledge/` — target, prerequisite and vocabulary guidance.
- `lessons/a1/` — completed active A1 lesson JSON.
- `lessons/a2/` — completed active A2 lesson JSON.
- `lessons/b1/` — completed active B1 lesson JSON.
- `progress/A1_PROGRESS.md`, `progress/A2_PROGRESS.md`, `progress/B1_PROGRESS.md` — durable level progress.

## Hygiene rule
Obsolete lesson files, temporary generators, one-shot workflows, stale audits and duplicate instruction documents are removed rather than kept as competing sources of truth.
