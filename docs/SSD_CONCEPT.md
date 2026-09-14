# SlovakGo SSD Concept

SSD is the durable working model for the lesson repository: **Source / Status / Decisions**.

The goal is simple: after any break, a future session must be able to return to the repository, understand what is true, what was verified, what is still weak and how to continue without relying on chat history.

## 1. Source

Source means the files that define what may be produced.

Authoritative sources:

- `README.md` — entrypoint and current map.
- `MASTER.md` — concise master rules.
- `AGENTS.md` — operational contract for agents.
- `curriculum/COURSE_ARCHITECTURE_V2.md` — CEFR/course architecture.
- `curriculum/LESSON_JSON_CONTRACT.md` — lesson JSON contract.
- `curriculum/lesson.schema.json` — local schema reference.
- Level plans:
  - A1: `curriculum/A1_MASTER_LESSON_PLAN.md`
  - A2: `A2/LESSON_PLAN.md`
  - B1: `B1/LESSON_PLAN.md`
  - B2: `B2/LESSON_PLAN.md`
  - C1: `C1/LESSON_PLAN.md`
  - C2: `C2/LESSON_PLAN.md`
- Current application importer/runtime checker, when available, outranks stale local assumptions.

Rule: if a lesson contradicts its level plan or runtime contract, fix the generator/source rule and regenerate the affected set. Do not patch random JSON files blindly unless doing a clearly bounded erratum.

## 2. Status

Status means the current state of production and verification.

Durable status files:

- `docs/LESSON_PRODUCTION_REPORT.md` — global production report.
- `progress/A1_PROGRESS.md`
- `progress/A2_PROGRESS.md`
- `progress/B1_PROGRESS.md`
- `progress/B2_PROGRESS.md`
- `progress/C1_PROGRESS.md`
- `progress/C2_PROGRESS.md`

Each progress file must say:

- complete/incomplete state;
- active lesson count;
- authoritative plan;
- JSON directory;
- section ranges;
- QA gates passed;
- known limitations or next improvement area.

## 3. Decisions

Decisions are rules that prevent future accidental regressions.

Current decisions:

- Slovak is the target language. Slovenian is a hard failure.
- Learner-facing UI/explanations are Ukrainian by default.
- Higher-level generated lessons may include `uk`, `ru` and `en` fields when the importer contract requires them.
- Lesson counts are pedagogical outputs, not filler quotas.
- A production batch must be validated as a whole affected set after any generator or contract change.
- `resultScreen.nextLesson` must form a complete chain and end with `null` on the terminal lesson.
- Temporary generation scripts are removed unless they have continuing value for regeneration, QA or repair.
- Known generated-content limitations must be reported honestly instead of hidden.

## Return Protocol

Use this protocol before any lesson work:

1. Read `README.md`.
2. Read this SSD concept.
3. Read `docs/LESSON_PRODUCTION_REPORT.md`.
4. Read `docs/NEXT_WORK_CHECKLIST.md`.
5. Read the target level plan and progress file.
6. Inspect current Git status and recent commits.
7. Decide whether the task is production, errata, QA hardening, localization repair or documentation.
8. Make changes through the smallest responsible source: plan, contract, generator, QA or lesson JSON.
9. Run full affected validation.
10. Update status/report documents.
11. Commit and publish only after fresh verification.

## Known SSD Debt

- B1-C2 were generated with level-specific Python QA, not necessarily the real application importer. Application-runtime validation should be run when the app checker is available.
- C2 contains complete structural lessons, but some rare vocabulary translations use a neutral C2 fallback rather than a manually curated dictionary. This is acceptable for structural import but should be improved in a vocabulary-quality pass.
- A1/A2 have stronger historical curriculum documentation than B2/C1/C2. Future work should gradually raise all levels to the same documentation depth.
