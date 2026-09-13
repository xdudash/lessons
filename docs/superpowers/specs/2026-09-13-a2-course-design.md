# SlovakGo A2 Course Production Design

Date: 2026-09-13
Status: approved in chat, pending written-spec review

## Goal

Build the complete SlovakGo A2 level from the current approved `A2/LESSON_PLAN.md`, using the current SlovakGo importer/runtime contract and the completed A1 level as prerequisite knowledge.

The current A2 map contains 15 consecutive sections with 6 lessons each, for 90 active lessons total. This design treats that map as the production source of truth. If implementation uncovers a pedagogical contradiction that cannot be solved inside the mapped lesson, the lesson plan must be revised explicitly rather than silently adding filler or changing the active count.

## Sources of truth

In descending priority:

1. Current SlovakGo runtime/checker behavior and `curriculum/LESSON_RUNTIME_CONTRACT.md` in the application repository.
2. Current application `curriculum/lesson.schema.json`.
3. `A2/LESSON_PLAN.md` for A2 lesson topics, order and intended new lexical targets.
4. `curriculum/COURSE_ARCHITECTURE_V2.md` for CEFR progression and mastery principles.
5. Completed A1 lesson corpus for prerequisite vocabulary, structures and transfer targets.

Historical content may inform examples but must not override current runtime or the approved A2 map.

## Active A2 inventory

IDs are sequential with no retired gap:

- S01: `a2-s01-l01`–`a2-s01-l06`
- S02: `a2-s02-l07`–`a2-s02-l12`
- S03: `a2-s03-l13`–`a2-s03-l18`
- S04: `a2-s04-l19`–`a2-s04-l24`
- S05: `a2-s05-l25`–`a2-s05-l30`
- S06: `a2-s06-l31`–`a2-s06-l36`
- S07: `a2-s07-l37`–`a2-s07-l42`
- S08: `a2-s08-l43`–`a2-s08-l48`
- S09: `a2-s09-l49`–`a2-s09-l54`
- S10: `a2-s10-l55`–`a2-s10-l60`
- S11: `a2-s11-l61`–`a2-s11-l66`
- S12: `a2-s12-l67`–`a2-s12-l72`
- S13: `a2-s13-l73`–`a2-s13-l78`
- S14: `a2-s14-l79`–`a2-s14-l84`
- S15: `a2-s15-l85`–`a2-s15-l90`

`a2-s15-l90` is terminal and must omit `resultScreen.nextLesson`. Every other lesson points to the next active A2 lesson.

## Production batching

Production is split into five coherent batches of three consecutive sections:

1. S01–S03: people/relationships, routines, recent past.
2. S04–S06: future/plans, home/problems, city/transport.
3. S07–S09: food/cooking, shopping/services, work/study.
4. S10–S12: free time/social life, communication/problem solving, travel/accommodation.
5. S13–S15: health, opinions/comparisons, A2 integration.

Each batch must pass its own QA gate before the next batch is considered complete. Batch boundaries are production checkpoints only; the final course remains one continuous `nextLesson` chain.

## Lesson architecture

Each lesson is a complete learner-facing product, not a JSON skeleton. Normal lesson shape:

- start screen with specific learner outcomes;
- 3 theory screens;
- 8–10 target vocabulary/phrase items when the mapped lesson contains that many genuinely new targets;
- canonical `words` and a fully rendered `wordsScreen` with matching `wordId`, Slovak, Ukrainian, pronunciation and examples;
- 14 exercises using a varied profile of runtime-supported mechanics;
- contextual reading/dialogue/production work;
- a 3-step `interactive_scenario` final situation with semantically aligned prompts and answers;
- result screen with the correct next lesson;
- `isPublished: false` until product publication controls explicitly change it;
- Ukrainian learner UI and Slovak target language;
- no fake image/audio assets.

The exact exercise profile varies by lesson purpose. A2 must not become 90 copies of one template.

## Exercise design

Use only mechanics supported by the current application checker/renderer. Profiles should rotate among appropriate mechanics such as:

- `single_choice`, `multiple_select`, `true_false`, `true_false_list`;
- `fill_blank`, `dropdown_blank`, `cloze_text`, `word_bank`;
- `matching`, `collocation`, `drag_to_category`;
- `sentence_builder`, `sentence_order`, `dialogue_order`;
- `dialogue_choose_reply`, `branching_dialogue` where runtime-safe;
- `reading_comprehension`, `meaning_in_context`, `natural_phrase`;
- `find_error`, `correct_error`, `transformation`;
- `real_message`, `real_schedule`, `real_document` when the lesson naturally calls for them.

Listening mechanics are excluded unless real audio assets exist. Every deterministic checker encoding must match actual runtime semantics.

## A1 → A2 ownership model

Before A2 generation, build an ownership inventory from the completed A1 corpus.

For each A2 lexical/functional target classify it as:

- NEW — first controlled ownership in A2;
- REVIEW — known from A1 and intentionally recalled;
- TRANSFER — known language used in a new A2 function or grammatical environment;
- MASTERY — previously learned material used independently in integrated production.

An item already owned by A1 must not be presented as newly learned merely because it appears in `A2/LESSON_PLAN.md`. Repeated high-frequency items such as city places, transport, food, shopping, health and problem-solving language are used as review/transfer where appropriate.

## Grammar/function progression

Grammar is taught through communicative tasks, not as isolated grammar-only filler.

- S01: richer adjective/personality description, agreement, comparison, relationship language.
- S02: frequency, routines, sequencing, habit change and time-pressure language.
- S03: systematic recent-past narration and common past forms.
- S04: future forms, intentions, probability, arrangements and changed plans.
- S05: detailed spatial description, household problems and polite requests.
- S06: routes, movement, transport, duration and clarification.
- S07: quantities, containers, procedural/recipe sequencing.
- S08: comparison, fitting/selection, complaints and service transactions.
- S09: duties, deadlines, work/study sequencing and cooperation.
- S10: reasons for preferences, invitations, refusals and social arrangements.
- S11: communication repair, help requests, explaining problems and proposing solutions.
- S12: travel sequence, booking, accommodation and disruption handling.
- S13: symptoms, duration, recommendations and practical health communication.
- S14: opinions, reasons, comparisons, choices and controlled conditional chunks such as `radšej by som`/`keby` only to the degree planned for A2.
- S15: independent integration across narration, planning, problem solving and explanation.

Forms formally beyond A2 may appear only as functional chunks when useful; their presence must not be described as mastery of a later grammatical system.

## Content-quality constraints

- Slovak examples and dialogues must sound natural and match the stated learner intent.
- Ukrainian prompts/translations must be idiomatic and must not leak Russian-only UI language.
- Final-situation prompts must describe exactly the action performed by their marked correct answer.
- Reading/dialogue contexts must not rely heavily on unintroduced later structures.
- Distractors must be plausible but unambiguously wrong and must not duplicate labels.
- Sentence-builder/order token multisets must reconstruct the declared correct answer exactly.
- Vocabulary examples must demonstrate the actual target, not generic unrelated sentences.
- Repetition must serve review or transfer rather than accidental duplication.

## QA architecture

Validation has several independent layers.

### Structural/runtime

- application JSON schema;
- SlovakGo runtime QA/checker contract;
- supported exercise types only;
- required deterministic answer encodings;
- valid word references, lesson references, unique IDs and orders.

### Adversarial data QA

- duplicate option/label detection;
- sentence-builder and sentence-order multiset equality;
- dropdown correct value present in options;
- word-bank correct values present in bank;
- matching/category/runtime encoding validation;
- final-situation unique choices and exactly one correct response;
- `wordsScreen`/canonical word consistency.

### Curriculum QA

- A1/A2 vocabulary ownership audit;
- prerequisite leakage audit;
- grammar/function progression audit;
- target coverage per lesson and per section;
- section integration/mastery evidence;
- Ukrainian UI-language audit;
- semantic prompt/answer intent audit for final situations.

### Course-level QA

Before completion:

- exactly 90 active A2 lesson JSON files;
- IDs exactly match the 15-section map;
- orders 1–90 unique and complete;
- `nextLesson` chain valid from L01 to L90;
- L90 has no next lesson;
- all five batches pass runtime/adversarial/curriculum QA;
- remote `main` inventory is checked after publication, not inferred from local files.

## Publication and progress tracking

Lessons are published to `lessons/a2/` only after their production batch passes its gate. `progress/A2_PROGRESS.md` is updated as batches complete and finally marked complete only after the remote 90/90 audit.

Temporary generators, specs used only for transport/build, and one-shot workflows must be removed from `main` after successful generation. Durable QA scripts or ownership manifests may remain only if they have continuing repository value.

## Error handling

A failing QA gate blocks publication of the affected batch. Fix source specs/generator logic first; do not patch generated JSON repeatedly unless the defect is genuinely lesson-specific.

Any mismatch between local/frozen content and remote Git blobs must be treated as a transfer failure and resolved with SHA-gated publication before the batch is accepted.

If a conflict appears between the 90-lesson map and the course-architecture principle of pedagogically derived counts, the implementation does not silently add or delete lessons. The conflict is surfaced as a plan revision requirement.

## Non-goals

- Do not publish lessons to learners (`isPublished` remains false).
- Do not create fake audio, images or external media references.
- Do not redesign the SlovakGo application runtime.
- Do not rewrite completed A1 except for separately identified errata.
- Do not expand A2 beyond the approved lesson map without an explicit curriculum-plan revision.

## Completion criteria

A2 is complete only when:

1. all 90 mapped lessons exist on remote `main`;
2. all 15 sections meet their declared learning purposes;
3. structural, runtime, adversarial and curriculum QA are green;
4. A1→A2 ownership and prerequisite checks are green;
5. the complete lesson chain is correct and L90 is terminal;
6. `progress/A2_PROGRESS.md` says 90/90 only after remote verification;
7. temporary production tooling has been cleaned up.
