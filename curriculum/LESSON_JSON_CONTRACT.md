# SlovakGo — Mandatory Lesson JSON Contract

## Status
**ACTIVE / MANDATORY**

This document defines the canonical JSON contract for every lesson in A1–C2. A lesson is production-ready only when it conforms to this contract and passes the applicable QA gates.

The known-working lesson example (`lesson-181-a1_slovakgo.json`) is a **format reference only**. Its number is never copied into lesson numbering.

## 1. Top level

Every file must be a JSON object with exactly one top-level key:

```json
{
  "lessons": [
    { /* exactly one complete lesson object */ }
  ]
}
```

Never upload a bare lesson object. Never put multiple lessons into one lesson file unless explicitly specified by the repository contract.

## 2. Lesson identity and metadata

Required core fields:

- `id` — `a1-sNN-lNN`, `a2-sNN-lNN`, `b1-sNN-lNN` / `b1-sNN-lNNN` when a level exceeds 99 lessons, etc.
- `sectionId` — matching level/section, e.g. `a1-s03`.
- `level` — `A1`, `A2`, `B1`, `B2`, `C1` or `C2`.
- `title` — localized object with `sk` plus learner UI locales used by the project.
- `topic` — localized object.
- `description` — localized object.
- `order` — lesson number represented by `id`.
- `xpReward`.
- `estimatedMinutes`.
- `isPublished`.
- `intro` — localized object.
- `completionMessage` — localized object.
- `updatedAt`.
- `localization`.
- `assets`.

IDs, filename stem, `sectionId`, `level` and `order` must agree.

## 3. Language contract

- Target language: **Slovak (`sk`, slovenčina)**.
- Learner-facing instructions/explanations/UI: **Ukrainian (`uk`)**.
- Do not substitute Slovenian (`slovenščina`).
- Slovak example sentences remain Slovak; translations remain Ukrainian.
- No accidental mixed-language learner-facing strings.

## 4. Required lesson flow

Every lesson uses this ordered structure:

```text
metadata
→ startScreen
→ theoryScreens
→ wordsScreen
→ words
→ exercises
→ finalSituation
→ resultScreen
```

The exact lesson content varies by level and plan, but this envelope is stable.

## 5. startScreen

Required:

```json
{
  "screenType": "lesson_start",
  "title": {},
  "shortDescription": {},
  "outcomes": [],
  "newWords": [],
  "exercisesCount": 0,
  "reward": "",
  "button": ""
}
```

`exercisesCount` must equal the actual number of exercises.

## 6. theoryScreens

At least 2 screens unless an explicit higher-level lesson design has a documented reason for another shape.

Each screen must provide a meaningful explanation, examples and support for what is later tested. Theory must not test untaught material.

## 7. wordsScreen

Required shape:

```json
{
  "screenType": "lesson_words",
  "title": {},
  "description": {},
  "items": [
    { "wordId": "..." }
  ],
  "button": ""
}
```

The `wordId`s must resolve to the local `words` list. Use `wordId`, not `id`, inside `wordsScreen.items`.

## 8. words

Each vocabulary item must have a unique local ID and enough information to support teaching and practice.

Canonical minimum:

```json
{
  "id": "a1-s03-l18-w01",
  "sk": "...",
  "uk": "...",
  "pronunciationUk": "...",
  "exampleSk": "...",
  "exampleUk": "...",
  "level": "A1",
  "topic": "...",
  "tags": []
}
```

Rules:

- `sk` contains Slovak only.
- Every ID is unique within the lesson.
- New vocabulary must come from the approved lesson plan.
- Do not label review vocabulary as new.
- Do not inflate the word list with irrelevant items.

## 9. exercises

Each exercise requires:

```json
{
  "id": "ex01",
  "lessonId": "a1-s03-l18",
  "type": "...",
  "order": 1,
  "question": "..."
}
```

Additional fields depend on exercise type.

All exercise types must have an unambiguous answer model and all referenced `wordIds` must be local to the same lesson.

### Supported canonical types

- `single_choice`
- `multiple_select`
- `matching`
- `fill_blank`
- `dropdown_blank`
- `sentence_order`
- `sentence_builder`
- `meaning_in_context`
- `natural_phrase`
- `reading_comprehension`
- `dialogue_choose_reply`
- `multiple_choice_translation`
- `reverse_translation`
- `match_pairs`

Do not invent a new exercise type inside a production lesson without first updating this contract and the corresponding QA.

### Answer integrity

- Exactly one correct option where the task is single-answer.
- Multiple-select has the intended number of correct choices.
- `correctAnswer` must refer to an actually offered answer.
- `fill_blank.acceptedAnswers` must contain valid answers that solve the prompt.
- `dropdown_blank` options and correct answer must agree.
- `sentence_order` tokens and `correctOrder` must produce the same sentence.
- `sentence_builder` tokens and `correctSentence` must produce the same sentence.
- Reading/dialogue questions must have exactly the intended correct responses.
- Distractors must be plausible but unambiguously wrong.

## 10. finalSituation

Canonical production form:

```json
{
  "id": "final-situation",
  "type": "interactive_scenario",
  "title": {},
  "description": {},
  "steps": [],
  "passRequirement": "3/3"
}
```

The final situation must demonstrate transfer of the lesson target in a realistic context. It must not be a trivial repeat of one vocabulary question.

If a level-specific importer requires a different final-situation field shape, that variation must be documented here before production; agents must not improvise per lesson.

## 11. resultScreen

Canonical production form:

```json
{
  "title": {},
  "subtitle": {},
  "xpReward": 100,
  "nextLesson": {
    "id": "...",
    "title": {}
  }
}
```

For the final lesson of a level, `nextLesson` is `null`.

## 12. Cross-reference rules

Before commit, verify all references:

- filename ↔ lesson `id`;
- `sectionId` ↔ lesson `id`;
- `order` ↔ lesson `id`;
- `wordsScreen.items[].wordId` ↔ local `words[].id`;
- exercise `lessonId` ↔ current lesson `id`;
- exercise `wordIds[]` ↔ local words;
- `resultScreen.nextLesson.id` ↔ the actual next lesson;
- final lesson of a level has `nextLesson: null`.

## 13. Structural QA gate

Reject before commit if any of these fail:

1. JSON parse;
2. top-level envelope;
3. required fields;
4. IDs/filename/order;
5. localization contract;
6. wordsScreen/words consistency;
7. exercise schema and answer integrity;
8. finalSituation contract;
9. resultScreen contract;
10. cross-references;
11. no obsolete duplicate lesson file.

## 14. Content QA gate

After structural QA:

**Slovak correctness → Ukrainian localization → CEFR fit → lesson-plan alignment → pedagogy → vocabulary usefulness → exercise correctness → transfer → progression → overlap.**

A lesson that parses is not automatically a good lesson.

## 15. Change policy

This file is mandatory. If the importer or project intentionally changes the lesson contract:

1. update this contract first;
2. update QA rules;
3. update the gold-standard guidance;
4. only then generate new lessons.

Never create a one-off JSON structure to solve a single lesson problem.
