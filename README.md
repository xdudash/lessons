# SlovakGo — Slovak language course

This repository is the durable source of truth for the SlovakGo CEFR course A1-C2.

## Start Here

Before changing lessons, read these files in this order:

1. `docs/SSD_CONCEPT.md` — source/status/decisions model for returning to the project without losing context.
2. `docs/LESSON_PRODUCTION_REPORT.md` — current production state, known risks and QA evidence.
3. `docs/NEXT_WORK_CHECKLIST.md` — required checklist before any new generation, fix or publication.
4. `AGENTS.md` — operational contract for agents.
5. The target level plan and progress file.

## Current Status

| Level | Active lessons | Plan | JSON directory | Progress |
|---|---:|---|---|---|
| A1 | 75 | `curriculum/A1_MASTER_LESSON_PLAN.md` | `lessons/a1/` | `progress/A1_PROGRESS.md` |
| A2 | 90 | `A2/LESSON_PLAN.md` | `lessons/a2/` | `progress/A2_PROGRESS.md` |
| B1 | 100 | `B1/LESSON_PLAN.md` | `lessons/b1/` | `progress/B1_PROGRESS.md` |
| B2 | 100 | `B2/LESSON_PLAN.md` | `lessons/b2/` | `progress/B2_PROGRESS.md` |
| C1 | 90 | `C1/LESSON_PLAN.md` | `lessons/c1/` | `progress/C1_PROGRESS.md` |
| C2 | 70 | `C2/LESSON_PLAN.md` | `lessons/c2/` | `progress/C2_PROGRESS.md` |

## Project Model

- Curriculum is CEFR-based and content-led.
- Lesson count follows pedagogical targets, prerequisites, review, transfer and mastery needs.
- Production may use batches of coherent sections; this does not change the approved lesson count.
- GitHub `main` is the durable branch after verified publication.
- SSD means every meaningful change must leave a source reference, a status update and a decision trail.

## Language Policy

- Target language: Slovak (`slovenčina`).
- Learner-facing instructions, explanations and UI text: Ukrainian by default.
- Current generated higher-level lessons include `uk`, `ru` and `en` localization fields where the production contract requires them.
- Slovenian (`slovenščina`) is never acceptable.

## Lesson JSON

All active lesson files use the current importer/runtime-compatible format:

```json
{"lessons":[{"id":"c2-s01-l001","sectionId":"c2_s01","level":"C2"}]}
```

The detailed authoring/production contract is `AGENTS.md`; the current SlovakGo application schema and runtime checker define machine/runtime validity.

## Repository Map

- `AGENTS.md` — operational production contract.
- `MASTER.md` — concise project rules.
- `docs/SSD_CONCEPT.md` — durable return-to-work concept.
- `docs/LESSON_PRODUCTION_REPORT.md` — level status, QA evidence and known follow-up areas.
- `docs/NEXT_WORK_CHECKLIST.md` — checklist before any lesson work.
- `A1/` ... `C2/` — level lesson plans/reference material.
- `curriculum/` — architecture and curriculum contracts.
- `knowledge/` — target, prerequisite and vocabulary guidance.
- `lessons/<level>/` — active lesson JSON files.
- `progress/` — durable progress reports per level.
- `tools/qa_*.py` — level-specific structural QA where present.
- `tools/generate_*.py` — retained generators with continuing value for regeneration/fixes.

## Hygiene Rule

Obsolete lesson files, temporary one-shot workflows, stale audits and duplicate instruction documents are removed rather than kept as competing sources of truth. If a generator or report stays in the repository, it must explain current production value.
