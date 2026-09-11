# SlovakGo — 10K Slovak Course

This repository is the persistent source of truth for the SlovakGo CEFR A1–C2 course.

The curriculum is planned for 10,000 lessons. Master rules, curriculum intelligence, lesson schema, review rules, QA rules, worker protocol, and progress state live here so production can continue across independent AI workers without relying on chat history.

## Principles

- The current/new lesson format is authoritative.
- Content is not distorted to accommodate application UI bugs.
- Every lesson must have a real pedagogical purpose.
- Generation is followed by adversarial review and progression QA.
- Review is spiral: NEW → REVIEW → TRANSFER → MASTERY.
- GitHub state is persistent; individual worker chats are disposable.

## Current phase

Phase 0: architecture and curriculum foundation.

Next: deep analysis of the existing 250 A1 lessons, detailed grammar/vocabulary/function/competency inventories, prerequisite graph, pilot generation, review, then scale-out.

See `MASTER.md` and `MASTER_CURRICULUM_10K.md` for the authoritative plan.
