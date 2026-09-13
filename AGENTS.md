# AGENTS.md — SlovakGo A1–C2 production contract

## Source of truth
Read the current repository state before editing. GitHub `main` is the durable source of truth.

Level roadmaps are level-specific:
- A1: `curriculum/A1_MASTER_LESSON_PLAN.md`.
- A2: `A2/LESSON_PLAN.md`.
- B1–C2: the corresponding `B1/LESSON_PLAN.md` … `C2/LESSON_PLAN.md`.

Curriculum architecture is `curriculum/COURSE_ARCHITECTURE_V2.md`. The current SlovakGo application schema/runtime checker outrank stale local assumptions about fields or exercise mechanics.

## Language rules
- Target language: Slovak (`slovenčina`). Never substitute Slovenian (`slovenščina`).
- Learner-facing instructions, explanations and UI text: Ukrainian.
- Slovak examples stay Slovak; Ukrainian translations stay Ukrainian.

## Numbering and curriculum
Canonical IDs are level-specific: `a1-sNN-lNN`, `a2-sNN-lNN`, … `c2-sNN-lNN`; `sectionId` is `<level>_sNN`; `level` matches the target CEFR level.
Lesson IDs, order and section membership come from the authoritative level plan. Never invent numbering or duplicate legacy files.
Production may use batches of three coherent sections; this never changes the section's approved lesson count.

## Canonical lesson JSON
Every active lesson file is a single top-level object:

```json
{"lessons":[{"id":"a2-sNN-lNN"}]}
```

Canonical lifecycle: metadata → `startScreen` → `theoryScreens` → `wordsScreen` → `words` → `exercises` → `finalSituation` → `resultScreen`.

Required lesson metadata includes `id`, `sectionId`, `level`, localized title/topic/description, `order`, XP/time, `isPublished`, intro/completion text, localization and the complete lesson screens.

`wordsScreen.items` must be fully rendered and agree with canonical `words`: `wordId`, `sk`, `uk`, pronunciation and examples. Never create reference-only empty vocabulary rows.

Exercises must use only mechanics supported by the current application `curriculum/lesson.schema.json` and `scripts/qa-lessons.ts`. Deterministic answers, `wordIds`, `lessonId`, option correctness, token order and type-specific structures must match the actual runtime checker. Supported mechanics evolve with the application; do not freeze an old A1-only list here.

`finalSituation` may use any current runtime-supported final contract, including the richer `interactive_scenario`. It must test transfer in a realistic situation and its marked answer must match the learner prompt semantically.

`resultScreen.nextLesson` points to the next active lesson ID/object as accepted by the current runtime contract. The terminal lesson for a level omits `nextLesson` when that is the active application contract.

## Content quality
Every lesson has a distinct learning purpose. Vocabulary is rich enough for real communication but is not inflated. Practice moves from recognition to controlled production, context, communication and transfer.
Do not test unintroduced grammar or vocabulary merely because it is easy to generate. Use natural Slovak and natural Ukrainian.

## Ownership and progression
Use NEW → STABILIZE → CONTRAST → TRANSFER → INTEGRATE → MASTERY as learning functions.
Vocabulary repetition is intentional only when it serves review, transfer or mastery. For A2, completed A1 content is prerequisite evidence: an A1-owned item must not be relabeled as newly learned merely because it appears in the A2 map.

## Production workflow
1. Read the current level plan, architecture, progress and `main` tree.
2. Read the current application schema/runtime contract when lesson format is involved.
3. Build the exact lesson map for the target batch: IDs, outcomes, prerequisites, ownership and transfer evidence.
4. Draft/generate the complete batch before publication.
5. Run structural schema validation, real runtime QA and semantic/adversarial curriculum QA.
6. If a defect class appears, repair the source rule/generator and revalidate the whole affected set.
7. Only green batches are written to the durable branch/main.
8. Read back remote files and verify inventory, links and progress after publication.

## Hard-failure gate
STOP → IDENTIFY → REPAIR THE RULE → REVALIDATE THE WHOLE AFFECTED SET → COMMIT.

Do not continue dependent production on a known hard failure. Do not claim real application import/QA unless the actual application checker/importer was run.

## Repository hygiene
Keep one canonical agent instruction file. Keep one authoritative lesson map per level. Remove temporary generators, one-shot workflows and stale audits when production is complete unless they have continuing repository value.
Do not rewrite completed A1 while building A2 except for separately identified errata.
