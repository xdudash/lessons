# SlovakGo — Agent Protocol

## Purpose
This file is the operational contract for any AI agent continuing SlovakGo. The agent must be able to continue correctly from GitHub without relying on chat history.

## 0. FORMAT CONTRACT OVERRIDES GENERIC COUNTS
For lesson JSON format, use `AGENTS.md` and the actual known-working importer example as the source of truth.

A user-provided working file such as `lesson-181-a1_slovakgo.json` is a **format reference only**. Its file number, lesson ID, order, and section identity must NOT be copied to another section.

The actual target section determines its own numbering. Example: Section 01 ends at `a1-s01-l06`; Section 02 therefore begins at `a1-s02-l07`.

The older numeric examples in this protocol (such as 2 theory screens, 6 vocabulary items, 16 exercises) are quality/reference guidance, not universal importer quotas. A richer lesson may contain more vocabulary, more theory screens, or a different exercise count when pedagogically justified and compatible with the real importer contract.

## A. Startup — mandatory

Before changing anything:

1. Read `README.md`.
2. Read `MASTER.md`.
3. Read `AGENTS.md`.
4. Read `curriculum/COURSE_ARCHITECTURE_V2.md`.
5. Read `curriculum/GOLD_STANDARD_LESSON.md`.
6. Read relevant `knowledge/*` files.
7. Read relevant `progress/*` and `audits/*`.
8. Inspect the current `main` tree and recent commits.
9. Inspect a known-working importer-compatible lesson JSON.
10. Determine the exact unfinished section, its real numbering, and its current files.

Never trust a previous agent's chat claim over the actual repository.

## B. Production unit

The production unit is **3 coherent consecutive sections**.

For each section:

- start with 3 complete lessons when production is required;
- allow up to 6 lessons in the batch when the section's targets justify them;
- do not use 6 as a quota;
- reduce lesson count when targets can be combined without sacrificing learning or mastery;
- add lessons only when pedagogically justified.

## C. Design before generation

For the sections, determine:

- CEFR outcomes;
- grammar targets;
- vocabulary/functions;
- prerequisites;
- target ownership;
- review and transfer needs;
- lesson purpose;
- mastery evidence;
- required pedagogically justified lesson count.

Only then write lesson JSON.

## D. Language rules

- Target language: **Slovak (slovenčina)**.
- Never substitute Slovenian (slovenščina).
- Student-facing instructions, prompts, explanations, hints and learning UI: **Ukrainian** unless explicitly overridden by repository instructions.
- Slovak examples and target answers must be natural, correct Slovak.

## E. Lesson construction

Use the known-working importer-compatible lesson format described in `AGENTS.md`.

Canonical structure includes, as applicable to the real working contract:

- top-level `{ "lessons": [ ... ] }` envelope;
- lesson metadata: `id`, `sectionId`, `level`, `title`, `topic`, `description`, `order`, `xpReward`, `estimatedMinutes`, `isPublished`, `intro`, `completionMessage`, `updatedAt`;
- `startScreen` with `screenType`, `title`, `shortDescription`, `outcomes`, `newWords`, `exercisesCount`, `reward`, `button`;
- `theoryScreens` with actual working fields such as `screenType`, `order`, `title`, `text`, `examples`, `exampleSk`, `exampleUk`, `shortRule`, `button`;
- `wordsScreen` with its actual working fields, including `items` and `wordId` references;
- `words` with `id`, `sk`, `uk`, `pronunciationUk` when used, `exampleSk`, `exampleUk`, `level`, `topic`, `tags`;
- `exercises` with common fields such as `id`, `lessonId`, `type`, `question`, `options`, `correctAnswer`, `explanation`, `wordIds`, `order`, `difficulty`, `button`, plus type-specific fields supported by working lessons;
- `finalSituation` using the actual working final-situation format;
- `resultScreen` using the actual working result format.

Do not invent localization-object wrappers or alternative field names when the real importer expects strings/scalars.

## F. Exercise types

Only use exercise types already supported by a real working lesson. Inspect the real example before using a type.

Known working patterns include:

- `multiple_choice_translation` — string options + `correctAnswer` string;
- `match_pairs` — flat `options` array + pair strings like `left|right` in `correctAnswer`;
- `fill_blank` — options + correct answer + optional `fullSentence`;
- `reverse_translation` — options + correct answer;
- `dropdown_blank` — `sentenceParts` with text and blank objects;
- `sentence_builder` — `tokens` + `correctSentence`;
- `sentence_order` — `tokens` + `correctOrder`;
- `dialogue_choose_reply` — dialogue array + option objects with Slovak text and `correct` flag;
- `correct_error` — `sentence` + `acceptedAnswers`;
- `reading_comprehension` — `text` + `questions`;
- `meaning_in_context` — `context` + `target` + option objects containing Ukrainian `text` and `correct`;
- `natural_phrase` — `situation` + Slovak option objects;
- `multiple_select` — option objects with multiple possible `correct` answers.

Never create a new exercise schema from intuition.

## G. Vocabulary

Vocabulary count is not a fixed quota.

- Prefer enough meaningful words/phrases to support the lesson's communicative outcome.
- 12–20+ meaningful lexical items is a useful current density target for a substantial A1 lesson, not a hard maximum or minimum.
- Add more when the lesson needs them.
- Reuse new vocabulary in theory, examples, exercises and transfer.
- Do not add irrelevant words solely to increase a count.

## H. Hard JSON rule

Every generated file MUST be independently parseable JSON before it reaches GitHub.

Mandatory checks:

- file is complete, not truncated;
- exactly one valid top-level JSON object;
- top-level `lessons` exists and is an array;
- no duplicate keys;
- no Python list/dict string representations;
- no accidental extra nesting;
- all brackets/braces/quotes are balanced;
- required fields exist;
- field types match the working importer contract;
- all internal references resolve;
- JSON Unicode is intact.

A parser error is a hard stop.

## I. Semantic QA

After structural parsing, inspect every lesson for:

- natural and correct Slovak;
- correct morphology/agreement;
- coherent meaning;
- correct CEFR level;
- correct prerequisite order;
- exercises that actually test the stated target;
- correct marked answers;
- valid accepted answers;
- valid sentence-builder/order solutions;
- relevant distractors;
- coherent dialogues;
- coherent reading/context tasks;
- natural phrases;
- realistic final situations;
- complete Ukrainian learner-facing text.

Do not rely on templates as proof of correctness.

## J. Adversarial QA

Actively try to break each lesson:

- Can every exercise be solved from its own data?
- Does the marked answer really answer the prompt?
- Does every `correct` flag make sense?
- Does `correctOrder` use exactly the supplied tokens?
- Do accepted answers match the sentence?
- Is every Slovak sentence complete and natural?
- Is any learner-facing field accidentally a serialized array/object?
- Is any Slovak content accidentally Slovenian?
- Is any lesson merely a reworded duplicate?
- Is the theory sufficient for the exercises?
- Does the final situation demonstrate the target?

If any answer is no, repair before committing.

## K. Batch QA

Do not QA lessons only in isolation. Also check the batch for:

- target coverage;
- progression;
- vocabulary ownership;
- meaningful overlap/repetition;
- prerequisite violations;
- repeated exercises with no pedagogical reason;
- missing section outcomes;
- weak mastery evidence;
- unnecessary lessons.

## L. Git discipline

Prefer one coherent bulk commit for one completed production batch when practical.

Before reporting completion:

1. commit changes;
2. verify the commit exists;
3. verify the branch points to the expected state;
4. verify every expected file exists in the committed tree;
5. verify obsolete/mistaken files are removed;
6. if anything is missing or wrong, repair immediately and verify again.

Never report a planned change as completed.

## M. Progress

Update durable progress only after QA has passed.

Use:

```text
STATUS: COMPLETE

BATCH:
- ...

COMPLETED:
- ...

FILES CHANGED:
- ...

QA:
- JSON: PASS
- Schema: PASS
- Slovak: PASS
- Exercise logic: PASS
- Localization: PASS
- Progression/overlap: PASS
- GitHub tree: PASS
- Importer: PASS only if actually run

UNRESOLVED:
- none / ...

NEXT TASK:
- ...
```

## N. Failure protocol

If a hard defect is found:

**STOP. Do not generate dependent content.**

Then:

1. identify the defect;
2. repair it;
3. parse again;
4. repeat semantic/adversarial QA;
5. commit the repair;
6. verify GitHub;
7. continue only after the repository is clean.

## O. No filler / no destructive rework

Never create content merely to hit a number.

Never overwrite good content with a weaker template-generated version.

Never redo a completed section without evidence that it needs revision.

Never change pedagogical content to compensate for an application bug.

When a section is rebuilt, replace obsolete files instead of keeping competing versions.

## P. User interaction

The user's continuation signal is `+`.

When the user sends `+`, execute the next repository-defined production task without asking what to do next, unless the repository contains a genuine blocker requiring user input.

Status messages should be concise and factual.

## Q. Core rule

**Quality and repository truth beat speed. A smaller number of valid, meaningful lessons is better than a larger number of broken, thin, or duplicated lessons.**
