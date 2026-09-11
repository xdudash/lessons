# SlovakGo A1 — Vocabulary Ownership & Review Matrix

Status: **baseline-derived planning matrix v1.0**

This matrix assigns each of the 1,272 unique Slovak expressions in the 250-lesson baseline an initial ownership lesson and labels each observed occurrence as NEW → REVIEW → TRANSFER → MASTERY. It is a planning control, not a claim that frequency alone proves mastery.

## Counts

- Baseline lessons: 250
- Vocabulary entries: 1,500
- Unique expressions: 1,272
- Repeated expressions: 187
- Single-occurrence expressions needing future review planning: 1,085

## Stage policy

- First observed occurrence → **NEW** (initial owner).
- Second → **REVIEW**.
- Third → **TRANSFER**.
- Fourth and later → **MASTERY** (subject to QA).
- A repeated occurrence is not automatically sufficient evidence of mastery; context, productive use and transfer still require review.

## Data format

`progress/A1_VOCAB_OWNERSHIP.json` contains every expression, translation, first owner, all baseline occurrences, stage labels and a `needs_future_review` flag.

## Control rule

**Do not remove repeated vocabulary.** Use the matrix to decide whether a future lesson should stabilize, contrast, transfer or assess an item. Expressions with only one baseline occurrence require deliberate future review scheduling before being treated as mastered.
