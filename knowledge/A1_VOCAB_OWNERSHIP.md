# SlovakGo A1 — Vocabulary Ownership

## Status
ACTIVE / planning guidance

Vocabulary is assigned to lessons by communicative purpose and prerequisite order. A word or phrase may intentionally recur across lessons.

## Ownership rule
The first lesson that deliberately teaches a lexical item as a target owns the item for planning purposes. Later appearances should have a reason:

**NEW → REVIEW → TRANSFER → MASTERY**

A repeated occurrence is not automatically mastery evidence. Productive use and successful transfer matter.

## Lesson rules
- Do not create duplicate lexical targets merely to fill a word-count quota.
- Prefer phrases that support the lesson's communicative outcome.
- Reuse important vocabulary in new contexts.
- Keep `wordId` local to the lesson JSON unless the actual importer contract explicitly supports cross-lesson references.
- Check neighbouring lessons before introducing a new target to avoid accidental duplication.

## Current source of truth
The exact ownership map should be derived from the active lessons and the master lesson plan. The retired 250-lesson baseline and its numerical counts are not production rules and are not maintained here.
