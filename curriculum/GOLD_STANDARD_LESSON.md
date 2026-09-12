# SlovakGo — Gold Standard Lesson

## Status
ACTIVE

The gold standard is a **quality contract**, not a rigid lesson-count template. Use the known-working importer example to preserve the real JSON contract, and use the current master plan for IDs and lesson counts.

## Required learning arc
A strong lesson should move the learner through an appropriate combination of:

1. clear target;
2. understandable explanation;
3. useful Slovak examples with Ukrainian support;
4. controlled recognition and production;
5. contextual practice;
6. communication or transfer;
7. evidence of learning.

## Content density
Use enough vocabulary and examples to make the target usable. Twelve meaningful lexical items is a useful current dense-lesson reference, not a blind quota. Add or reduce when the pedagogical target requires it.

## JSON contract
Every importable file must use the real working envelope:

```json
{
  "lessons": [
    {
      "id": "a1-sXX-lYY",
      "sectionId": "a1_sXX",
      "level": "A1",
      "startScreen": {},
      "theoryScreens": [],
      "wordsScreen": {},
      "words": [],
      "exercises": [],
      "finalSituation": {},
      "resultScreen": {}
    }
  ]
}
```

Field-level details and supported exercise types are maintained in `AGENTS.md`, which is the operational source of truth.

## Language contract
- Slovak (`slovenčina`) is the target language.
- Learner-facing instructions, prompts, explanations and UI text are Ukrainian.
- Do not use Slovenian (`slovenščina`).

## Hard failures
Reject a lesson when:
- JSON does not parse or is truncated;
- it uses a non-working schema or invented field names;
- IDs/filenames/section numbers disagree with the master plan;
- internal `wordId` or `lessonId` references are broken;
- marked answers are wrong or unavailable;
- Slovak is unnatural, malformed or semantically wrong;
- Ukrainian learner-facing text contains accidental Slovak or debugging text;
- theory does not support the exercises;
- the final situation does not demonstrate the lesson target;
- the lesson is filler, a thin word list, or repetitive without pedagogical purpose.

## QA order
**JSON → importer contract → Slovak → pedagogy → exercises → localization → progression → overlap → transfer → GitHub read-back.**

Real application import is a separate gate and is only PASS when actually run.
