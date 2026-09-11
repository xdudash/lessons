# A1 — Audit of 250 baseline lessons

Date: 2026-09-12
Status: PASS with targeted corrections

## Scope

Audited all 250 lesson JSON files in the A1 baseline: 25 sections × 10 lessons.

## Findings

### Duplicates

- Exact duplicate lesson payloads: **0**.
- Accidental cross-section vocabulary duplicates: **none at a high threshold**.
- Exact title collision: **1** — `a1-s02-l07` and `a1-s08-l06` both use `Kde bývaš?`.
  - `a1-s02-l07`: general place of residence and `bývať`.
  - `a1-s08-l06`: housing type/location (`v byte`, `v dome`).
  - Action: rename `a1-s08-l06` to `Bývam v byte alebo dome?`.
- Repeated exercise prompt scaffolds: **93 collision groups**. These are mainly recurring exercise mechanics, not duplicate lessons. Keep the mechanics, but require prompt variation unless repetition is intentional review.

### Structural checks

- 250 lesson files found.
- Every lesson declares level `A1`.
- Every section contains exactly 10 lessons.
- Core lesson envelope is structurally consistent.
- Exercise-type distribution is broad and consistent.

### Curriculum gaps to encode in the master inventory

1. Cases are present through useful forms/chunks, but there is no explicit productive A1 case map separating exposure from mastery.
2. Plural forms occur, but plural formation is not represented as a single explicit progression.
3. Imperatives occur as functional commands, but the high-frequency imperative is not tracked as a grammar dependency.
4. Reflexive verbs occur in useful chunks, but reflexive structure is not tracked explicitly.
5. Verb conjugation families are used, but productive paradigms are not yet represented in an inventory.
6. Systematic aspect is not established in A1; this should be a deliberate A2/B1 dependency.
7. The package is text-only, so acoustic listening and actual spoken production are not assessed. Treat this as a media-layer gap, not a reason to rewrite the content baseline.

## CEFR judgement

The baseline is broadly A1-appropriate: personal information, immediate needs, concrete everyday situations, short routine exchanges, simple questions, memorized patterns and basic connected language dominate the course.

Rule for future generation:

> Functional exposure to a form at A1 is not the same as productive mastery of the grammatical system behind that form.

This is especially important for case forms, prepositions, verb government and other forms that appear naturally inside A1 communication.

## Required MASTER changes

- Differentiate the duplicate title.
- Create A1 grammar inventory with four states: introduced form / productive target / review / deferred to A2+.
- Create prerequisite graph for cases, plural, adjective agreement, imperative and reflexive verbs.
- Tag lexicalized case chunks separately from productive case rules.
- Explicitly defer systematic aspect to A2/B1.
- Add prompt-variation rule for future generation.
- Preserve intentional repetition and spiral review.
- Add media-layer flag for future audio/speech.
- Add QA rule: functional exposure ≠ grammatical mastery.
- Re-run the same audit at every CEFR level before mass production.

## Next step

Build the A1 grammar/vocabulary/function inventory and prerequisite graph from the audited 250 lessons. This becomes the foundation for refining the 10K curriculum.
