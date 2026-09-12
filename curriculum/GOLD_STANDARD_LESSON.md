# SlovakGo — Gold Standard Lesson

## STATUS: ACTIVE

`lessons/a1/a1-s01-l01.json` is the canonical lesson-quality reference.

Its exact content is not a template to copy. Its **completeness, density, learner flow and structural integrity** are the reference.

## Canonical shape

The reference lesson contains:

- valid top-level `{ "lessons": [ ... ] }` JSON envelope;
- complete metadata;
- title/topic/description;
- 2 theory screens;
- 6 vocabulary items;
- 16 exercises;
- varied exercise types;
- grammar practice;
- vocabulary practice;
- reading/context practice;
- dialogue practice;
- writing/production practice;
- contextualized meaning;
- natural-phrase practice;
- 3-step final real-life situation;
- localized learner-facing content;
- result/completion structure.

## Quality contract

A production lesson must provide a coherent learning arc:

1. clear target;
2. sufficient explanation;
3. useful examples;
4. controlled recognition/use;
5. contextual practice;
6. meaningful production when appropriate;
7. communication/real-life use;
8. evidence of learning.

The exact exercise count is a reference, not a blind quota. However, a lesson must never be made materially thinner merely for speed or convenience.

## Hard failures

Reject the lesson if:

- JSON does not parse;
- the top-level `lessons` array is missing;
- required fields are missing;
- the structure differs from the established schema without explicit justification;
- exercises have incorrect answers;
- accepted answers do not solve the task;
- Slovak is unnatural or incorrect;
- translations contradict the Slovak;
- learner-facing fields contain serialized arrays/objects;
- theory does not support the exercises;
- the lesson is primarily a thin word list or repetitive quiz;
- the final situation does not demonstrate the target.

## QA order

**JSON → schema → Slovak → pedagogy → exercises → localization → progression → overlap → mastery.**

Only after all applicable gates pass is the lesson production-final.

## UI rule

Application rendering bugs do not justify removing valid pedagogical fields. Source quality and application compatibility are separate concerns.
