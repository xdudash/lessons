# SlovakGo — Dynamic CEFR Course

This repository is the persistent source of truth for the SlovakGo A1–C2 course.

## Project model

- CEFR A1–C2
- no predetermined total lesson count
- no fixed lesson quota per level
- no fixed lesson quota per section
- minimum 3 lessons per section when lessons are required
- larger sections receive more lessons when mastery requires them
- no filler lessons
- production in batches of at least 5 sections
- batch-level QA and minimal Git commits

## Production philosophy

The curriculum determines the number of lessons. We first define outcomes, targets, prerequisites and mastery requirements; then we create the minimum number of substantial lessons needed to achieve them.

The pedagogical progression is:

**NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY**

These are learning functions, not fixed lesson slots.

## Batch workflow

For each production batch:

1. select at least 5 consecutive/coherent unfinished sections;
2. determine the lesson count for every selected section, minimum 3;
3. design the complete progression for each section;
4. generate all planned lessons;
5. run full batch QA, including cross-lesson overlap and progression;
6. repair failures;
7. run QA again;
8. update progress at batch/section level;
9. commit the batch with one main commit whenever possible;
10. verify GitHub state.

## Quality

The supplied `A1-S01-L01` is the canonical gold-standard reference. It defines the expected completeness and density, while allowing justified variation by lesson purpose.

Content must remain pedagogically complete even when application/UI components have compatibility problems.

## Repository map

- `MASTER.md` — master project rules and state
- `AGENT_PROTOCOL.md` — continuation and production protocol
- `curriculum/` — active course architecture and lesson-quality standard
- `knowledge/` — inventories, prerequisites and target ownership intelligence
- `lessons/` — active lesson JSON files
- `audits/` — QA and historical evidence
- `progress/` — durable batch/section progress and handoffs

## Current state

The active lesson tree has been reset. No lessons are currently active. The next production command starts from the beginning under the dynamic mastery model.

## Historical note

The former 10,000-lesson plan and fixed 1,000-lesson A1 allocation are retired. They must not be used as production quotas.
