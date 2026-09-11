# SlovakGo — Master

## Mission

Build a complete Slovak course from A1 through C2 with **no predetermined lesson quota**. The final lesson count is determined by CEFR outcomes, curriculum coverage, progression and demonstrated mastery.

The former 10,000-lesson target is retired as a production quota. It remains historical project context only.

## Source of truth

The repository is the persistent course memory. Master curriculum, grammar, competencies, lesson-quality standard, exercise mechanics, production rules, review rules, QA rules, worker protocol, and progress files are authoritative.

The existing 250 A1 lessons remain the historical content baseline. They are not automatically accepted as final, and they are not automatically discarded. They must be mapped and audited against the current architecture.

## Gold-standard lesson

The user's supplied `A1-S01-L01` is the canonical **GOLD STANDARD** for lesson quality, completeness, density and pedagogical architecture.

Its content must be preserved as the reference lesson. Future lessons must not copy its content, but must meet its level of completeness rather than the undersized pilot standard used previously.

The gold standard demonstrates:

- 2 theory screens;
- 6 vocabulary items;
- 16 exercises;
- broad exercise-type coverage;
- grammar, vocabulary, reading, dialogue and writing practice;
- contextualized meaning work;
- natural-phrase work;
- a multi-step real-life final situation;
- localized content;
- complete lesson metadata and screen structure.

Exercise count is a quality signal, not a mechanical quota. A lesson must have enough depth to achieve its target.

## Course architecture v2

The course is **content-led, not quota-led**.

Production order:

1. define CEFR outcomes;
2. define grammar, vocabulary, communicative functions and competencies;
3. define prerequisites and mastery gates;
4. map existing lessons, including A1 L01–L10;
5. identify genuine gaps and unnecessary duplication;
6. design complete lessons to close those gaps or deepen required mastery;
7. validate mastery;
8. stop when the defined outcome is genuinely achieved.

The number of lessons is a result of this process, not an input constraint.

See `curriculum/COURSE_ARCHITECTURE_V2.md` for the detailed active architecture.

## A1 L01–L10 rule

Every A1 section begins with its existing L01–L10 sequence as part of the actual curriculum.

They must **not be skipped** when planning the section. They must be:

- mapped to targets;
- checked for prerequisites;
- checked for progression;
- audited for quality against the gold standard;
- revised where necessary;
- used as inputs to later review and transfer decisions.

The old rule "L01–L10 are fixed baseline, generate from L11" is retired.

## Lesson progression

The course retains the progression:

**NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY**

These are pedagogical functions, not fixed lesson numbers. A target may require different numbers of lessons depending on complexity and learner needs.

## Complete lesson principle

A full lesson should normally provide a coherent arc such as:

**TARGET → THEORY → EXAMPLES → VOCABULARY → CONTROLLED PRACTICE → CONTRAST → CONTEXT → PRODUCTION → COMMUNICATION → REAL LIFE → MASTERY EVIDENCE**

Not every lesson needs every exercise type, but lessons must be substantially complete and appropriate to their purpose. The gold-standard lesson is the density and architecture reference.

## No filler

Never create lessons merely to reach a number.

A lesson must advance or consolidate a meaningful target: new knowledge, stabilization, contrast, transfer, fluency, accuracy, register, pragmatics, integrated skills, review or assessment.

## Repetition

Repetition is intentional when it supports:

**NEW → REVIEW → TRANSFER → MASTERY**.

Repeated vocabulary is not inherently a defect. The learner's use should become deeper, more flexible, more accurate or more contextually appropriate.

## CEFR architecture

- A1 — forms and fundamentals
- A2 — systems and controlled expansion
- B1 — connections and independent communication
- B2 — composition, complex syntax, register
- C1 — choice, precision, advanced discourse
- C2 — control, nuance, stylistic flexibility

Important boundary:

**functional exposure ≠ grammatical mastery.**

An A1 learner may encounter a useful high-frequency phrase containing a later-system form without claiming mastery of the complete later grammar.

## Production loop

1. Read current master state and progress.
2. Inspect the complete relevant section, including L01–L10 where they already exist.
3. Check grammar/vocabulary/function inventories and prerequisites.
4. Check existing target ownership and overlap.
5. Design a lesson that meets the current gold-standard quality expectation.
6. Validate schema, answer validity, Slovak naturalness, pedagogy, CEFR fit and progression.
7. Perform adversarial QA.
8. Repair rejected content.
9. Update progress and handoff state.
10. Commit the completed logical unit.

## Quality hierarchy

1. Slovak correctness and naturalness
2. Pedagogical completeness
3. CEFR appropriateness
4. Prerequisite correctness
5. Exercise validity
6. Target ownership and progression
7. Review/mastery integrity
8. Localization quality
9. Schema/UI compatibility

Application limitations must never reduce pedagogical content. Record UI incompatibilities separately.

## Existing A1 audit baseline — 250 lessons

The earlier structural audit remains historical evidence. It confirmed 250 files, 25 sections × 10 lessons, broad exercise coverage and no exact core lesson duplicates. It also identified a title collision and several areas needing explicit curriculum mapping.

Those findings remain relevant, but **passing a structural audit is not equivalent to meeting the new gold-standard lesson quality**.

## Superseded planning model

The former `25 sections × 40 lessons = 1,000 A1 slots` model is retired as a production quota.

`curriculum/A1_1000_MAP.md`, the previous target registry, and the previous 10K allocation are historical planning artifacts. They must not force generation of lessons that the curriculum does not need.

## Current phase

**Phase 1 — Architecture reset and A1 remapping.**

Next gate: formally register the gold-standard lesson, map **all existing A1 L01–L10** against targets and prerequisites, audit their completeness against the new standard, then determine the true A1 lesson requirements before generating further content.
