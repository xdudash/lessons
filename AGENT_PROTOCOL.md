# SlovakGo — Agent Protocol

## Purpose

This file is the operational contract for any AI agent continuing SlovakGo. The agent must be able to continue correctly from GitHub without relying on chat history.

## A. Startup — mandatory

Before changing anything:

1. Read `README.md`.
2. Read `MASTER.md`.
3. Read `curriculum/COURSE_ARCHITECTURE_V2.md`.
4. Read `curriculum/GOLD_STANDARD_LESSON.md`.
5. Read relevant `knowledge/*` files.
6. Read relevant `progress/*` and `audits/*`.
7. Inspect the current `main` tree and recent commits.
8. Determine the exact unfinished section/batch.

Never trust a previous agent's chat claim over the actual repository.

## B. Production unit

The production unit is **3 coherent consecutive sections**.

For each section:

- start with 3 complete lessons when production is required;
- allow up to 6 lessons in the batch when the section's targets justify them;
- do not use 6 as a quota;
- add more only in a later explicitly justified production unit.

The agent chooses the next three sections automatically. Do not ask the user what to produce next when the repository makes the next batch clear.

## C. Design before generation

For the three sections, determine:

- CEFR outcomes;
- grammar targets;
- vocabulary/functions;
- prerequisites;
- target ownership;
- review and transfer needs;
- lesson purpose;
- mastery evidence;
- required lesson count.

Only then write lesson JSON.

## D. Lesson construction

Use `lessons/a1/a1-s01-l01.json` as the canonical structural and quality reference.

Default complete shape:

- top-level `{ "lessons": [ ... ] }` envelope;
- complete lesson metadata;
- 2 theory screens;
- 6 vocabulary items;
- 16 meaningful exercises;
- 3 final-situation steps;
- localized learner-facing content;
- result/completion structure.

Counts may change only for a pedagogical reason. Never reduce content merely to save time.

## E. Hard JSON rule

Every generated file MUST be independently parseable JSON before it reaches GitHub.

Mandatory checks:

- file is complete, not truncated;
- exactly one valid top-level JSON object;
- top-level `lessons` exists and is an array;
- lesson object is inside that array;
- no duplicate keys;
- no Python list/dict string representations;
- no accidental extra nesting;
- all brackets/braces are balanced;
- required fields exist;
- arrays contain objects of the expected form.

A parser error is a hard stop.

## F. Semantic QA

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
- complete translations/localization.

Do not rely on templates as proof of correctness.

## G. Adversarial QA

Actively try to break each lesson:

- Can every exercise be solved from its own data?
- Does the marked answer really answer the prompt?
- Does every `correct` flag make sense?
- Does `correctOrder` use exactly the supplied tokens?
- Do accepted answers match the sentence?
- Is every Slovak sentence complete and natural?
- Is any learner-facing field accidentally a serialized array/object?
- Is any lesson merely a reworded duplicate?
- Is the theory sufficient for the exercises?
- Does the final situation demonstrate the target?

If any answer is no, repair before committing.

## H. Batch QA

Do not QA lessons only in isolation. Also check the batch for:

- target coverage;
- progression;
- vocabulary ownership;
- unnecessary overlap;
- prerequisite violations;
- repeated exercises with no pedagogical reason;
- missing section outcomes;
- weak mastery evidence.

## I. Git discipline

Prefer one bulk commit for one completed three-section batch.

Do not make one commit per lesson.

Before reporting completion:

1. commit changes;
2. verify the commit exists;
3. verify the branch points to it;
4. verify every expected file exists in the committed tree;
5. if anything is missing, repair immediately and verify again.

Never report a planned change as completed.

## J. Progress

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

UNRESOLVED:
- none / ...

NEXT TASK:
- ...
```

## K. Failure protocol

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

## L. No filler / no rework

Never create content merely to hit a number.

Never overwrite good content with a weaker template-generated version.

Never redo a completed section without evidence that it needs revision.

Never change pedagogical content to compensate for an application bug.

## M. User interaction

The user's continuation signal is `+`.

When the user sends `+`, the agent should execute the next repository-defined production task without asking what to do next, unless the repository contains a genuine blocker requiring user input.

Status messages should be concise and factual.

## N. Core rule

**Quality and repository truth beat speed.**

A smaller number of valid lessons is better than a larger number of broken lessons.
