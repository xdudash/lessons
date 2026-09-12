# AGENTS.md — Mandatory lesson-production workflow

## Purpose
This file is the durable operating contract for every agent working in this repository. Read it before editing or creating lessons.

## 1. Source of truth
- GitHub `main` is the authoritative durable state.
- Repository instructions and the actual working lesson files take precedence over an agent's assumptions.
- Do not invent or silently replace the project's lesson JSON contract.

## 2. Critical distinction: FORMAT vs NUMBERING
The user's provided working example (for example, `lesson-181-a1_slovakgo.json`) is an **example of the importer-compatible JSON FORMAT**.

It is NOT a template for lesson numbering.

For a section, always preserve that section's own numbering. Example:
- Section 01 ends at `a1-s01-l06`.
- Section 02 therefore uses `a1-s02-l07`, `a1-s02-l08`, etc.

Never turn an example file number such as `181` into the numbering of a new section merely because it was used as the format reference.

## 3. Language rules
- Target language being learned/tested: **Slovak (slovenčina)**.
- Do NOT use Slovenian (slovenščina).
- Student-facing instructions, prompts, explanations and UI learning text: **Ukrainian** unless repository instructions explicitly say otherwise.
- Slovak examples, answers and target-language content must be actual Slovak.

## 4. Lesson architecture
Lesson count is pedagogical, not quota-driven.
- Prefer fewer, denser lessons when atomic targets can be taught together without losing mastery.
- Do not create filler lessons just to hit a predetermined number.
- Increase vocabulary when it improves the communicative target and supports exercises, context, review and transfer.
- New vocabulary must be meaningful and actually used; do not inflate counts with irrelevant words.

## 5. Use the real importer-compatible example
When the user supplies a known-working lesson JSON, inspect it directly and treat its actual field structure as the importer contract.

Preserve the real pattern, including (as applicable to the example):
- top-level `{"lessons":[...]}` envelope;
- lesson-level scalar/string fields in the same shape;
- `startScreen`;
- `theoryScreens`;
- `wordsScreen`;
- `words`;
- exercise objects with the real exercise fields such as `correctAnswer`, `explanation`, `wordIds`, `difficulty`, `button`, and type-specific fields;
- `finalSituation`;
- `resultScreen`.

Do not replace working scalar fields with invented localization objects such as `{sk, uk, ru, en}` when the real importer example uses strings.

Do not copy the example lesson's number, IDs or section identity unless the section genuinely requires them.

## 6. Required production workflow
For every new or rebuilt section:

### Step A — Read first
1. Read the repository instructions.
2. Read the relevant progress/plan files.
3. Read the current section files.
4. Read the known working importer-compatible example.
5. Determine the section's real lesson numbering from the repository.

### Step B — Plan
1. Define the section outcomes.
2. Group atomic targets into the smallest sensible number of complete lessons.
3. Decide the vocabulary needed for communication, not for quota.
4. Define progression: introduce → stabilize → contrast → transfer → integrate → mastery.

### Step C — Build locally first
Create/edit lesson JSON outside GitHub first when possible.

Before writing to GitHub, verify:
- valid JSON syntax;
- exactly the required top-level envelope;
- lesson IDs and filenames match the section numbering;
- all internal references point to existing IDs;
- `wordIds` exist;
- `correctAnswer` values match available options where applicable;
- type-specific fields match the real importer contract;
- lesson language is Slovak and learner-facing instructional language is Ukrainian;
- no accidental Slovenian language content;
- no malformed quotes, commas, escapes or Unicode corruption.

### Step D — Content QA
Check:
- Slovak grammar and naturalness;
- Ukrainian clarity;
- exercise answer correctness;
- distractor quality;
- vocabulary is purposeful and reused in context;
- reading/dialogue/transfer tasks actually test the stated outcomes;
- final situation is communicative rather than another trivial recognition question.

### Step E — Replace, do not duplicate
When rebuilding a section, replace the old section files.
Do not leave two competing versions of the same section in `main`.
Old temporary/mistaken files must be removed after the correct files are in place.

### Step F — GitHub verification
After writing:
1. Read the files back from GitHub `main`.
2. Verify the actual stored content, not merely the payload that was sent.
3. Verify the section directory contains the intended lesson sequence.
4. Verify old duplicate/mistaken lesson files are gone.
5. Update progress documentation only after the durable state is correct.

## 7. Import QA honesty
Do not claim that a lesson "passes import" unless the actual importer was run successfully.
Structural JSON validation is not the same as importer validation.
If the importer cannot be run, state that clearly and report only the checks actually completed.

## 8. Section 02 reference implementation
The current Section 02 architecture is five lessons:
1. `a1-s02-l07` — Kto som?
2. `a1-s02-l08` — Ja, ty, on, ona, ono
3. `a1-s02-l09` — Zoznámime sa
4. `a1-s02-l10` — O mne
5. `a1-s02-l11` — Predstavím sa

These use the section numbering above while following the importer-compatible JSON style established by the user's working example.

## 9. Anti-error checklist
Before every commit, explicitly ask:

- Am I copying the **format** from the example, or accidentally copying its **numbering**?
- Is the target language **Slovak**, not Slovenian?
- Are learner-facing instructions in **Ukrainian**?
- Am I using the **actual importer contract**, rather than an invented schema?
- Am I replacing obsolete section files rather than creating duplicates?
- Did I verify the files again after writing them to GitHub?

If any answer is uncertain, stop and inspect the repository/example before committing.
