# SlovakGo Next Work Checklist

Use this checklist before any lesson generation, correction, localization repair or publication.

## 1. Orient

- [ ] Read `README.md`.
- [ ] Read `docs/SSD_CONCEPT.md`.
- [ ] Read `docs/LESSON_PRODUCTION_REPORT.md`.
- [ ] Read this checklist.
- [ ] Read `AGENTS.md`.
- [ ] Read the target level plan.
- [ ] Read the target level progress file.
- [ ] Check `git status --short`.
- [ ] Check recent commits with `git log --oneline -6`.

## 2. Classify The Work

Choose exactly one primary type:

- [ ] New lesson production.
- [ ] Errata fix in existing lessons.
- [ ] Localization repair.
- [ ] QA hardening.
- [ ] Schema/runtime alignment.
- [ ] Documentation/report update.

## 3. Define Affected Set

- [ ] Identify affected level.
- [ ] Identify affected sections.
- [ ] Identify affected lesson IDs.
- [ ] Decide whether the source plan, generator, QA or individual JSON files must change.
- [ ] If a defect appears in multiple files, fix the generator/source rule first.

## 4. Content Rules

- [ ] Target language is Slovak (`sk`, `slovenčina`).
- [ ] No Slovenian (`slovenščina`) terms.
- [ ] Learner-facing explanations are Ukrainian by default.
- [ ] Localization fields required by the current contract are complete.
- [ ] Vocabulary comes from the approved lesson plan or documented review/transfer needs.
- [ ] Exercises test introduced material.
- [ ] Distractors are plausible but unambiguously wrong.
- [ ] Final situation tests real transfer, not only vocabulary recall.

## 5. Structural Rules

- [ ] Filename matches lesson `id`.
- [ ] `sectionId` matches lesson section.
- [ ] `level` matches target level.
- [ ] `order` matches lesson number.
- [ ] `wordsScreen.items[].wordId` resolves to `words[].id`.
- [ ] Every exercise `lessonId` equals the current lesson ID.
- [ ] Every exercise `wordIds[]` resolves locally.
- [ ] `startScreen.exercisesCount` equals actual exercise count.
- [ ] `resultScreen.nextLesson` forms a valid chain.
- [ ] Final lesson has `nextLesson: null`.

## 6. Verification

Run all commands for affected levels:

```bash
python tools/qa_b1.py
python tools/qa_b2.py
python tools/qa_c1.py
python tools/qa_c2.py
```

When available, also run the real app schema/import/runtime QA.

## 7. Reporting

- [ ] Update the relevant `progress/<LEVEL>_PROGRESS.md`.
- [ ] Update `docs/LESSON_PRODUCTION_REPORT.md` if status, QA evidence or known limitations changed.
- [ ] Update `docs/SSD_CONCEPT.md` if a new durable decision was made.
- [ ] Keep README current if entrypoints or status changed.

## 8. Publish

- [ ] Commit related changes together.
- [ ] Push only after fresh verification.
- [ ] Read back remote files or compare GitHub `main`.
- [ ] Report commit SHA and verification command output.
