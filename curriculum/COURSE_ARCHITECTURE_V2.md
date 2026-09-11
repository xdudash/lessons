# SlovakGo Course Architecture v2

## Status

**ACTIVE — replaces the fixed 10,000-lesson slot model.**

## Core decision

SlovakGo is a complete Slovak CEFR A1–C2 course. The total number of lessons is **not fixed in advance**.

The course is content-led, not quota-led:

1. define CEFR outcomes;
2. define grammar, vocabulary, functions, competencies and prerequisites;
3. define mastery requirements;
4. map the existing content;
5. identify genuine gaps and redundancy;
6. create only the lessons required to reach mastery;
7. stop a topic/section when its mastery gate is genuinely satisfied.

There is therefore no requirement to reach 10,000 lessons. A final count may be lower or higher. **No filler lessons may be created to hit a numerical target.**

## Existing A1 lessons 1–10 are included

The previous expansion model incorrectly treated the existing A1 lessons 1–10 as a finished baseline that could simply be skipped while generating later lessons.

That rule is retired.

For every A1 section, lessons **L01–L10 are part of the same curriculum sequence** and must be mapped, audited and included in progression planning. They are not exempt from QA merely because they pre-existed this architecture.

Existing lessons remain source material and historical evidence. Where they do not meet the new standard, they are candidates for revision; they are not silently discarded.

## Gold-standard lesson

The user's supplied `A1-S01-L01` is the **GOLD STANDARD** for lesson density, completeness and pedagogical architecture.

It is preserved as the canonical reference lesson. Future lessons must be designed against its level of completeness rather than against the undersized pilot lessons produced under the previous slot model.

The gold standard demonstrates, among other things:

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

The exact lesson content must not be copied. Its **quality, density and architecture** are the reference.

## Minimum lesson-quality principle

A lesson is not valid because it has a required number of exercises. It is valid when it provides a complete learning arc appropriate to its target.

A normal full lesson should generally contain:

- clear target and prerequisites;
- concise but substantive theory;
- examples in context;
- appropriate vocabulary/expressions;
- controlled practice;
- discrimination or contrast where relevant;
- contextual practice;
- at least one meaningful production task where appropriate;
- dialogue or communicative use where appropriate;
- reading/context work where appropriate;
- a real-life task where appropriate;
- mastery evidence.

Exercise count is a quality signal, not a quota. The gold-standard lesson is the reference point for expected density.

## Lesson progression

The course retains the pedagogical progression:

**NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY**

These are functions, not mandatory fixed lesson counts.

A topic may need 3 lessons or 12 lessons depending on its complexity. Conversely, two superficially different lessons must not be created if one complete lesson already achieves the required outcome.

## Section completion

A section is complete only when its defined outcomes are covered and its mastery gate is passed.

A section must therefore have:

- foundation targets;
- supporting vocabulary/functions;
- prerequisite links;
- review/transfer points;
- integration;
- an explicit mastery check.

The number of lessons is determined after this analysis.

## Existing 250 A1 package

The existing 250 A1 lessons are the authoritative historical content baseline. They must be:

- preserved;
- mapped to the new curriculum;
- audited for target coverage;
- audited for progression;
- audited for quality against the gold standard;
- revised where necessary;
- supplemented only where genuine gaps remain.

Do not assume that all 250 are perfect merely because they parse or because an earlier structural audit passed.

Do not assume that every one must remain unchanged merely because it exists.

## Superseded model

The former model of `25 sections × 40 lessons = 1,000 A1 slots`, with L01–L10 treated as fixed baseline and L11–L40 as expansion slots, is **SUPERSEDED**.

`curriculum/A1_1000_MAP.md` remains historical evidence of the previous planning model. It must not be used as the production quota.

Likewise, the previous 10,000-lesson allocation by CEFR level is planning history, not a production target.

## Quality gates

Before accepting a lesson:

1. Slovak correctness and naturalness;
2. CEFR appropriateness;
3. pedagogical completeness;
4. prerequisite correctness;
5. meaningful target ownership;
6. exercise answer validity;
7. contextual/natural usage;
8. progression and review integrity;
9. localization quality;
10. duplication/overlap check;
11. mastery contribution;
12. schema validity.

Application/UI limitations must not reduce lesson quality.

## Repetition

Repetition is intentional when it supports:

**NEW → REVIEW → TRANSFER → MASTERY**.

Vocabulary overlap alone is not a defect. The question is whether the learner's use of the item becomes deeper, more flexible or more accurate.

## Next production rule

Do not generate another batch of lessons until the new architecture has been applied to the existing A1 L01–L10 sequence and the gold-standard lesson has been formally registered as the lesson-quality reference.
