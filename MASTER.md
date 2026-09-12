# SlovakGo — Master Rules

## 1. Mission

Build a complete Slovak course from A1 through C2. Completeness is defined by CEFR outcomes, Slovak-specific grammar/vocabulary/functions, communicative competence, progression and demonstrated mastery.

**The final number of lessons is not known in advance.**

The old 10,000-lesson target, 1,000-lesson A1 target and 40-lessons-per-section model are retired and must not influence production.

## 2. Source of truth

GitHub `main` is the authoritative durable state. Chat is not the project database.

An agent must never claim that a lesson, batch, fix or instruction exists until it has verified the actual GitHub state.

## 3. Course architecture

CEFR progression:

- A1 — forms and fundamentals
- A2 — systems and controlled expansion
- B1 — connections and independent communication
- B2 — composition, complex syntax and register
- C1 — choice, precision and advanced discourse
- C2 — control, nuance and stylistic flexibility

Core pedagogical progression:

**NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY**

These are learning functions, not fixed lesson slots.

**Functional exposure is not grammatical mastery.** A learner may meet a useful expression before mastering the grammar system behind it.

## 4. Sections and lessons

Each CEFR level is divided into coherent sections. The number of lessons per section is dynamic.

When a section requires production, the initial production unit contains **3–6 complete lessons**. Three is the minimum starting point; six is not a quota. More lessons may be added only when mastery evidence requires them.

Never manufacture lessons to reach a number.

## 5. Production batches

Production is performed in batches of **3 consecutive/coherent sections**.

For every batch:

- determine targets before writing lessons;
- determine lesson count independently for each section;
- create the complete lessons;
- QA the whole batch;
- repair failures;
- QA again;
- update progress;
- make one main Git commit whenever technically possible;
- verify the committed tree.

Do not create one commit per lesson.

## 6. Canonical lesson

`lessons/a1/a1-s01-l01.json` is the canonical gold-standard lesson. Its content is reference material and must not be copied.

It establishes the expected quality, density and architecture. Its reference shape includes:

- complete lesson envelope;
- 2 theory screens;
- 6 vocabulary items;
- 16 exercises;
- varied exercise mechanics;
- grammar, vocabulary, reading, dialogue and writing practice;
- contextual meaning;
- natural phrases;
- multi-step final situation;
- localization;
- result/completion structure.

These counts are a default reference, not a reason to create shallow or repetitive material.

## 7. JSON contract

Every lesson file intended for import MUST be a valid JSON document with this top-level shape:

```json
{
  "lessons": [
    { "id": "a1-sXX-lYY", "sectionId": "a1-sXX", "level": "A1" }
  ]
}
```

A bare lesson object is invalid for this importer.

Before commit, every lesson file must be parsed by a real JSON parser. Visual inspection is not enough.

Duplicate object keys, truncated JSON, Python representations, malformed arrays, missing braces and misplaced fields are hard failures.

## 8. Required lesson architecture

A normal full lesson contains the established complete envelope:

- id
- sectionId
- level
- title
- topic
- description
- order
- xpReward
- estimatedMinutes
- isPublished
- intro
- completionMessage
- updatedAt
- localization
- assets
- startScreen
- theoryScreens
- wordsScreen
- words
- exercises
- finalSituation
- resultScreen

The canonical reference is the final authority when an implementation detail is uncertain.

## 9. Exercise integrity

Every exercise must be solvable from its visible data.

For every exercise QA must check:

- type is supported;
- instruction matches the task;
- prompt/context/situation matches the target;
- options are relevant;
- exactly the intended answers are marked correct;
- `acceptedAnswers` actually answer the prompt;
- ordering/building answers correspond to the supplied tokens;
- translations do not contradict the Slovak;
- no placeholder or list representation is serialized into learner-facing text.

A lesson with invalid exercise logic is rejected even if its JSON parses.

## 10. Slovak quality

Slovak is the target language and is the highest-priority content constraint.

Reject:

- invented or malformed Slovak;
- unnatural sentences created by templates;
- incomplete fragments presented as complete sentences;
- wrong inflection or agreement;
- semantically impossible answer choices;
- translations that change the intended meaning.

When uncertain, do not guess. Mark the item for review and resolve it before commit.

## 11. Localization

Learner-facing UI translations must be complete and natural in the supported UI languages.

Do not serialize programming-language lists, objects or debugging representations into text fields.

Slovak content belongs in Slovak fields; translations belong in translation/localization objects according to the established schema.

## 12. Vocabulary ownership

Vocabulary may repeat when repetition has a pedagogical role:

**NEW → REVIEW → TRANSFER → MASTERY**.

Do not duplicate a word merely because it is convenient for a lesson template.

Check existing ownership before assigning new targets.

## 13. QA gates

A lesson/batch is accepted only after all applicable gates pass:

1. valid JSON/schema;
2. complete lesson envelope;
3. Slovak correctness/naturalness;
4. CEFR fit;
5. prerequisite correctness;
6. exercise validity;
7. answer correctness;
8. localization;
9. target ownership;
10. progression;
11. meaningful review/transfer;
12. no accidental duplication;
13. mastery contribution;
14. GitHub state verified.

**Parsing success is only the first gate.**

## 14. UI compatibility

Do not delete or weaken valid pedagogical fields because the application currently fails to render them.

Known UI limitations are implementation issues and must be tracked separately from content quality.

## 15. Existing material

Historical lessons and audits are evidence, not automatic approval. Existing material must be mapped and audited before being treated as production-final.

Do not silently resurrect superseded fixed-slot content.

## 16. Completion definition

A section is complete when its defined outcomes, prerequisites, supporting vocabulary/functions, review/transfer requirements and mastery gate are satisfied.

A batch is complete only when all lessons in it pass QA and the GitHub tree has been verified.

## 17. Failure handling

If any hard failure appears:

**STOP → IDENTIFY → REPAIR → REVALIDATE → COMMIT.**

Never continue generating more dependent content on top of known invalid content.

## 18. Handoff

Every production unit must leave durable progress containing:

- STATUS;
- completed work;
- files changed;
- QA result;
- unresolved issues;
- exact next task;
- dependencies.

The next agent must be able to continue from GitHub alone.
