# AGENTS.md — SlovakGo A1 production contract

## Source of truth
Read the current repository state before editing. The authoritative course roadmap is `curriculum/A1_MASTER_LESSON_PLAN.md`. Curriculum architecture is `curriculum/COURSE_ARCHITECTURE_V2.md`. The lesson format must follow the known-working importer example `lesson-181-a1_slovakgo.json` as a FORMAT CONTRACT ONLY: its number is not lesson numbering.

`main` is the durable source of truth. Never trust an old conversation message over the current repository.

## Language rules
- Target language: Slovak (`slovenčina`). Never substitute Slovenian (`slovenščina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Slovak examples stay Slovak; Ukrainian translations stay Ukrainian.

## Numbering and curriculum
Lesson IDs and filenames come from `A1_MASTER_LESSON_PLAN.md`, not from the example lesson.
Never invent a new numbering scheme.
Never use “3 lessons per section”. A production batch may contain 3 sections, while each section keeps its own planned lesson count.
Never leave duplicate legacy lesson files when a canonical lesson replaces them.

## Canonical lesson JSON
Every lesson is a single top-level object with exactly:

```json
{"lessons":[{"id":"..."}]}
```

The lesson uses this canonical screen/order contract:
`metadata → startScreen → theoryScreens → wordsScreen → words → exercises → finalSituation → resultScreen`.

Core lesson metadata:
- `id`: `a1-sNN-lNN` and must match the filename stem.
- `sectionId`: matching `a1_sNN` section.
- `level`: `A1`.
- `title`, `topic`, `description`, `intro`, `completionMessage`.
- `order` must equal the lesson number.
- `xpReward`, `estimatedMinutes`, `isPublished`, `updatedAt`.

`startScreen`:
- `screenType: "lesson_start"`
- `title`, `shortDescription`, `outcomes`
- `newWords`: the lesson's local vocabulary list
- `exercisesCount`
- `reward`
- `button`

`theoryScreens`:
- at least 2 theory screens;
- clear Ukrainian explanation;
- Slovak examples with Ukrainian translations;
- teach the target before testing it;
- explain grammar/patterns only to the depth needed for the lesson.

`wordsScreen`:
- `screenType: "lesson_words"`
- `title`, `description`, `items`, `button`;
- every item uses `wordId`, not `id`;
- item `wordId`s exactly match the lesson's local `words` IDs.

`words`:
- each item has a unique local `id` such as `a1-s02-l07-w01`;
- `sk`, `uk`, `pronunciationUk`, `exampleSk`, `exampleUk`, `level`, `topic`, `tags`;
- Slovak field `sk` must contain Slovak, not Cyrillic.

`exercises`:
- normally 12 exercises for the dense lesson format unless the approved lesson design explicitly says otherwise;
- every exercise has local `id`, matching `lessonId`, supported `type`, `question`, `order`, `difficulty`, `button` and the fields required by its type;
- supported types: `multiple_choice_translation`, `reverse_translation`, `match_pairs`, `fill_blank`, `dropdown_blank`, `sentence_order`, `sentence_builder`, `meaning_in_context`, `natural_phrase`, `multiple_select`, `reading_comprehension`, `dialogue_choose_reply`;
- every `wordIds` entry must resolve inside the same lesson;
- never reference another lesson's word IDs;
- `correctAnswer` must be an actually offered answer;
- `sentence_order` token list and `correctOrder` must represent exactly the same sentence;
- `sentence_builder` tokens and `correctSentence` must match exactly;
- `dropdown_blank` blank definition, options and `correctAnswer` must agree;
- object-option types must have exactly the intended number of correct choices;
- distractors must be plausible and unambiguously wrong.

`finalSituation` must use the importer contract:
```json
{
  "screenType":"final_life_situation",
  "title":"...",
  "scenario":"...",
  "question":"...",
  "options":["..."],
  "correctAnswer":"1",
  "translation":"...",
  "explanation":"...",
  "button":"Перевірити"
}
```
It must test transfer in a realistic situation, not repeat a trivial vocabulary question.

`resultScreen` must use the importer contract:
```json
{
  "screenType":"lesson_result",
  "title":"Урок завершено",
  "text":"...",
  "nowYouKnow":["..."],
  "result":"+15 XP",
  "newWordsCount":4,
  "exercisesCompleted":12,
  "mistakesMessage":"...",
  "buttons":["..."],
  "nextLesson":"..."
}
```
For the final canonical lesson, `nextLesson` is `null`.

## Content quality
Each lesson must have a clear atomic purpose, not generic filler.
Vocabulary should be rich enough to support real communication and should be reused across theory, exercises and the final situation. Do not inflate vocabulary artificially.
Exercise progression should move from recognition to controlled production to contextual use/transfer.
Do not test untaught grammar or vocabulary just because it is easy to generate.
Use natural Slovak and natural Ukrainian. Fix typos, accidental mixed languages and malformed transliteration before commit.

## Production workflow — one pass
1. Read the current master plan, relevant architecture/knowledge docs, current progress and current `main` tree.
2. Inspect one known-working importer example when the format is involved.
3. Build the complete lesson map for the target section(s): exact IDs, lesson purposes, targets, prerequisites, vocabulary ownership and transfer evidence.
4. Draft the whole batch before repository writes.
5. Run batch-wide structural and semantic QA before writing.
6. If a defect class appears, fix the generation rule/template and rerun the full batch QA; do not patch one occurrence and assume the rest are clean.
7. Only after clean QA, write to `main`.
8. Read every changed file back from `main` and compare to the intended version.
9. Verify no obsolete/duplicate lesson files remain and all sequential links are correct.
10. Update `progress/A1_PROGRESS.md` only after the repository state is durable.

## Hard-failure gate
STOP → IDENTIFY → REPAIR THE RULE → REVALIDATE THE WHOLE AFFECTED SET → COMMIT.

Do not continue production on top of a known hard failure.
Do not claim “import PASS” unless the real application importer was actually run.
Distinguish JSON parse PASS, importer-contract PASS, semantic/adversarial QA PASS, and real application import PASS.

## Repository hygiene
Do not maintain parallel instruction documents that restate or contradict this file. Keep one canonical agent instruction file.
Keep the master lesson plan authoritative; keep progress factual and current; keep architecture/knowledge documents only when they contain unique, still-valid project information.
Delete or rewrite obsolete generated lessons, stale audits and old protocol documents instead of leaving competing truths in the repository.
