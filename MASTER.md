# SlovakGo 10K — Master

## Mission

Build a complete Slovak course from A1 through C2 with 10,000 purposeful lessons.

## Source of truth

The repository is the persistent course memory. Master curriculum, grammar, competencies, exercise mechanics, production rules, review rules, QA rules, worker protocol, and progress files are authoritative.

The existing 250 A1 lessons are the baseline for the established A1 sequence and lesson format. Application implementation problems are not curriculum constraints.

## CEFR architecture

- A1 — forms and fundamentals
- A2 — systems and controlled expansion
- B1 — connections and independent communication
- B2 — composition, complex syntax, register
- C1 — choice, precision, advanced discourse
- C2 — control, nuance, stylistic flexibility

## Production loop

1. Read master state and assigned slot range.
2. Check prerequisites and review dependencies.
3. Generate lessons in the established JSON format.
4. Self-check schema, answer validity, Slovak naturalness, pedagogy, and progression.
5. Submit for adversarial review.
6. Repair rejected lessons.
7. Update progress and handoff state.

## Quality hierarchy

1. Slovak correctness and naturalness
2. Pedagogical correctness
3. Prerequisite correctness
4. Exercise validity
5. Progression and review integrity
6. Localization quality
7. UI/schema compatibility

## No-filler rule

A lesson is valid only when it advances or consolidates a defined target: new knowledge, stabilization, contrast, transfer, fluency, accuracy, register, pragmatics, integrated skills, review, or assessment.

## Current phase

Phase 0 — architecture and curriculum foundation.

Next gate: deep analysis of the existing 250 A1 lessons, followed by detailed inventories and a 20–50 lesson pilot before large-scale parallel production.
