# One-Pass Production Workflow — 3 Sections

This is the default production method for future agents. The goal is to finish a three-section batch in one coherent pass instead of creating a lesson, finding one defect, creating the next lesson, and repeating.

## 1. Resolve the contract before writing anything
Read:
- `AGENTS.md`
- `AGENT_PROTOCOL.md`
- `MASTER.md` and `README.md`
- `curriculum/COURSE_ARCHITECTURE_V2.md`
- `curriculum/GOLD_STANDARD_LESSON.md`
- relevant `knowledge/*`, `progress/*`, `audits/*`
- the actual current `main` tree
- one known-working importer example, currently `lesson-181-a1_slovakgo.json`

The working example is a **format contract only**. Its number is never copied. Section numbering comes from the course map.

## 2. Build a batch map first
For the three target sections, determine before generation:
- section IDs;
- lesson ranges and next numbers;
- atomic linguistic targets;
- communicative functions;
- prerequisite/review dependencies;
- vocabulary ownership (NEW / REVIEW / TRANSFER / MASTERY);
- lesson purpose and progression;
- final transfer/mastery evidence.

Choose the smallest pedagogically sufficient lesson count. Do not use historical quotas.

## 3. Generate the whole batch in memory
Draft every lesson in the three sections before making repository writes.

Every lesson must use the same real importer-compatible envelope:
`lessons → lesson metadata → startScreen → theoryScreens → wordsScreen → words → exercises → finalSituation → resultScreen`.

Do not invent localization objects or alternative schemas. Keep scalar types scalar when the working importer uses scalar fields.

## 4. Run one pre-write QA pass over the entire batch
For every file check:
- JSON parses;
- file is complete, not truncated;
- no duplicate keys;
- correct envelope and field types;
- filename = lesson ID = section ID = order;
- all exercise `lessonId` values are local;
- all `wordIds` resolve to local `words`;
- every `wordsScreen.items[*].wordId` resolves;
- every correct answer is present/valid for its exercise type;
- sentence builder/order token sets are exact;
- all `correct` flags are correct;
- no accidental Slovenian;
- target language is Slovak (`slovenčina`);
- learner-facing text is Ukrainian;
- examples are actual, natural Slovak;
- translations are accurate;
- target coverage is complete;
- no exercise tests an untaught feature;
- final situation demonstrates transfer.

## 5. Fix the batch, not symptoms
If QA finds a repeated defect class, repair the generation rule/template and re-run the whole batch check. Do not patch one occurrence and assume the others are clean.

## 6. Write only clean files to GitHub
Create/update the complete batch only after the pre-write QA passes.
Do not leave half-created dependent lessons when a batch-wide defect is known.

## 7. Read-back verification
After the writes:
- read every changed file from `main`;
- verify stored content, not only outgoing payloads;
- verify the exact section tree and lesson sequence;
- verify no duplicate/obsolete files were left behind;
- verify cross-lesson `nextLesson` targets;
- update `A1_PROGRESS.md` only after durable state is correct.

## 8. Status honesty
Never call a section importer-approved unless the actual application importer was run. Distinguish:
1. JSON parse PASS;
2. importer-contract PASS;
3. semantic QA PASS;
4. real application import PASS.

## 9. Language guard
Slovak = `slovenčina`.
Slovenian = `slovenščina` and must not appear as the target language.
Learner-facing instructions/explanations = Ukrainian.
Slovak belongs in target examples, answers and vocabulary.

## 10. Failure rule
When a hard failure is found: stop dependent production, repair the root cause, re-run the batch QA, then continue. Never hide a defect by changing progress text.
