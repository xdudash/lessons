# SlovakGo — Dynamic CEFR Course

This repository is the persistent source of truth for the SlovakGo Slovak-language course, A1–C2.

## Non-negotiable project model

- The course is **dynamic**. There is no predetermined total number of lessons.
- There is no quota such as 10,000 lessons, 1,000 A1 lessons, or 40 lessons per section.
- Lessons are created only when they are pedagogically required.
- A section normally starts with **at least 3 lessons** when lessons are required.
- A section may contain **3–6 lessons in a production batch**. If mastery later requires more, that is decided explicitly from evidence; never add filler to hit six.
- Production is done in **batches of exactly 3 consecutive/coherent sections**.
- The agent chooses the next batch automatically from the unfinished curriculum. The user only needs to confirm continuation.
- The repository, not chat history, is the durable project memory.

## Lesson quality

`curriculum/GOLD_STANDARD_LESSON.md` and the canonical `lessons/a1/a1-s01-l01.json` define the quality floor.

A production lesson must preserve the complete lesson envelope and must be materially substantial. The canonical reference contains 2 theory screens, 6 vocabulary items, 16 exercises and a 3-step final situation; these are the default production shape, not excuses for thin content or blind quotas.

Every lesson must be valid JSON and use the required top-level envelope:

```json
{"lessons":[{ /* complete lesson object */ }]}
```

Never upload a bare lesson object when the importer expects the `lessons` array.

## Mandatory batch workflow

For each 3-section batch:

1. Read `MASTER.md`, `AGENT_PROTOCOL.md`, active curriculum/knowledge files and progress.
2. Inspect the current GitHub tree. Never assume previous work exists.
3. Determine the three sections and their actual targets.
4. Determine **3–6 lessons per section** from pedagogy, prerequisites, review, transfer and mastery needs.
5. Write the complete lessons.
6. Validate every JSON file before committing.
7. Perform content QA: Slovak naturalness/correctness, CEFR fit, exercise-answer validity, localization, progression, duplication and structure.
8. Repair every failed item.
9. Run the validation again.
10. Update progress/handoff.
11. Commit the complete batch in one main commit whenever technically possible.
12. Verify the resulting GitHub branch and file tree before reporting completion.

**No lesson is considered completed merely because a file was generated.**

## Never optimize around application bugs

If the application fails to render a valid field, keep the pedagogically correct source and record the UI problem separately. Do not remove dialogue, context, target, situation, skill, result or other valid lesson data merely to make a broken UI accept it.

## Superseded models

The old 10,000-lesson plan, fixed A1 1,000-slot plan and 25×40 lesson map are historical only. They must never be used as generation quotas.

## Repository map

- `MASTER.md` — authoritative project rules
- `AGENT_PROTOCOL.md` — exact continuation/production protocol
- `curriculum/COURSE_ARCHITECTURE_V2.md` — curriculum model
- `curriculum/GOLD_STANDARD_LESSON.md` — lesson quality contract
- `knowledge/` — targets, prerequisites and vocabulary ownership
- `lessons/` — active lesson JSON
- `audits/` — QA evidence
- `progress/` — durable progress and handoff state
