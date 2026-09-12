# One-Pass Production Workflow — 3 Sections

This is the default production method for future agents. A batch of three sections is produced as one coherent unit, but **three sections does not mean three lessons per section**.

## 1. Resolve the contract before writing anything
Read:
- `AGENTS.md`
- `AGENT_PROTOCOL.md`
- `MASTER.md` and `README.md`
- `curriculum/COURSE_ARCHITECTURE_V2.md`
- `curriculum/GOLD_STANDARD_LESSON.md`
- `curriculum/A1_MASTER_LESSON_PLAN.md`
- relevant `knowledge/*`, `progress/*`, `audits/*`
- the actual current `main` tree
- one known-working importer example, currently `lesson-181-a1_slovakgo.json`

The working example is a **format contract only**. Its number is never copied. Section numbering and lesson ranges come from the master lesson map.

## 2. Build the batch map first
For the three target sections determine before generation:
- section IDs;
- exact lesson count required by the master plan;
- exact lesson ID/file range;
- atomic linguistic targets;
- communicative functions;
- prerequisite/review dependencies;
- vocabulary ownership;
- lesson-by-lesson purpose;
- final transfer/mastery evidence.

Do not use “3 lessons per section.” Three is only the number of sections in a production batch. A section may require 4, 5, 6, 7, or another pedagogically justified number.

## 3. Generate the whole batch before repository writes
Draft every lesson required for all three sections before making dependent repository writes.

Every lesson must use the same real importer-compatible envelope:
`lessons → lesson metadata → startScreen → theoryScreens → wordsScreen → words → exercises → finalSituation → resultScreen`.

## 4. Pre-write QA — batch wide
Before any write, validate every lesson:
- JSON parses;
- complete, not truncated;
- correct envelope and field types;
- no duplicate keys or accidental nesting;
- filename = lesson ID;
- section ID/order are correct;
- exercise `lessonId` values are local;
- all `wordIds` resolve locally;
- `wordsScreen.items[*].wordId` resolves;
- answer fields are valid for the exercise type;
- sentence token sets/order are exact;
- all `correct` flags are correct;
- Slovak is actual Slovak (`slovenčina`), never Slovenian (`slovenščina`);
- learner-facing text is Ukrainian;
- translations are accurate;
- targets are covered;
- no exercise tests untaught material;
- final situation demonstrates transfer.

## 5. Repair the rule, not one symptom
If a defect class appears, fix the generation rule/template and re-run the full batch QA. Do not patch one occurrence while assuming the others are clean.

## 6. Write only after clean batch QA
Write the complete batch to `main` only after pre-write QA passes. Prefer one Git commit containing the whole batch when technically possible.

## 7. Read back the stored repository state
After writing:
- read every changed lesson from `main`;
- verify stored content against the outgoing version;
- verify exact section sequences;
- verify no duplicate/obsolete lesson files remain;
- verify next/previous links;
- update progress only after durable repository state is correct.

## 8. Import honesty
Distinguish:
1. JSON parse PASS;
2. importer-contract PASS;
3. semantic/adversarial QA PASS;
4. real application import PASS.

Never call step 4 passed unless the real application importer was actually run.

## 9. Hard-failure rule
**STOP → IDENTIFY → REPAIR → REVALIDATE → COMMIT.**

Never continue dependent production on top of a known hard failure.
