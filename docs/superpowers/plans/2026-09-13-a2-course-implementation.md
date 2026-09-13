# SlovakGo A2 Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish the complete 90-lesson SlovakGo A2 course, with A1→A2 ownership control, current SlovakGo runtime/schema validation, five batch gates, and final remote 90/90 verification.

**Architecture:** Author A2 from the approved `A2/LESSON_PLAN.md` through a temporary Python build harness that emits importer-compatible JSON into `lessons/a2/`. Validate every batch with local adversarial/curriculum checks plus the current application `lesson.schema.json` and `scripts/qa-lessons.ts`; publish only green batches, then remove temporary production tooling after the final remote audit.

**Tech Stack:** Python 3.13+, `jsonschema` 4.x, Node.js 22+ native TypeScript stripping for the current `qa-lessons.ts`, GitHub contents/Git-data APIs for durable publication.

**Spec:** `docs/superpowers/specs/2026-09-13-a2-course-design.md`

## Global Constraints

- A2 source of truth is `A2/LESSON_PLAN.md`: 15 sections × 6 mapped lessons = 90 active lessons.
- IDs are exactly `a2-s01-l01` through `a2-s15-l90`; there is no retired gap.
- `a2-s15-l90` is terminal and has no `resultScreen.nextLesson`; every earlier lesson points to the next active A2 ID.
- Learner-facing UI/explanations are Ukrainian; target language is Slovak.
- `isPublished` remains `false`.
- Do not create fake image/audio assets or listening exercises without real audio.
- A1 vocabulary is prerequisite evidence: repeated A1 items are REVIEW/TRANSFER, not falsely presented as new A2 ownership.
- Every normal A2 lesson has 3 theory screens, 14 exercises, a complete rendered vocabulary screen, and a 3-step `interactive_scenario` final situation unless a lesson-specific pedagogical reason is explicitly encoded in its spec.
- Current `xdudash/slovakGo` runtime checker and schema outrank stale repository-local assumptions.
- A failing batch gate blocks publication: repair source specs/generator rules, regenerate the whole affected batch, and rerun all checks.
- `progress/A2_PROGRESS.md` may say 90/90 only after remote verification.

---

### Task 1: Make repository production rules level-generic

**Files:**
- Modify: `AGENTS.md`
- Modify: `MASTER.md`
- Modify: `README.md`
- Create: `tools/a2_build/tests/test_repo_contract.py`

**Interfaces:**
- Consumes: current A1-safe repository rules and current universal application contract.
- Produces: repository instructions that permit A2 IDs, `level: A2`, the current registered exercise set, and `interactive_scenario` without changing completed A1 lesson files.

- [ ] **Step 1: Write the failing repository-contract test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def test_root_docs_are_not_a1_only():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    master = (ROOT / "MASTER.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "A1–C2" in agents
    assert "a2-sNN-lNN" in agents
    assert "interactive_scenario" in agents
    assert "A2/LESSON_PLAN.md" in master
    assert "lessons/a2/" in readme
```

- [ ] **Step 2: Run the test and verify it fails on the current A1-only wording**

Run: `python3 -m unittest tools.a2_build.tests.test_repo_contract -v`
Expected: FAIL because `AGENTS.md` is A1-specific and README/MASTER do not describe active A2 production.

- [ ] **Step 3: Generalize the root docs without rewriting A1 content**

Required wording/behavior:

```text
AGENTS.md: source map is level-specific (`A1` master map for A1; `A2/LESSON_PLAN.md` for A2; corresponding level plan thereafter); canonical IDs are `<level>-sNN-lNN`; level field matches the target level; current app schema/runtime checker define supported exercise/final-situation mechanics.
MASTER.md: add A2/LESSON_PLAN.md as authoritative A2 map and make canonical envelope level-generic.
README.md: list lessons/a1 and lessons/a2 separately and explain level-plan folders A1–C2.
```

Do not weaken any language-policy, QA, hard-failure, or repository-hygiene rule.

- [ ] **Step 4: Rerun the contract test**

Run: `python3 -m unittest tools.a2_build.tests.test_repo_contract -v`
Expected: PASS.

- [ ] **Step 5: Commit the documentation contract change**

```bash
git add AGENTS.md MASTER.md README.md tools/a2_build/tests/test_repo_contract.py
git commit -m "docs: generalize course production contract for A2"
```

---

### Task 2: Build A1→A2 ownership and map validation

**Files:**
- Create: `tools/a2_build/model.py`
- Create: `tools/a2_build/ownership.py`
- Create: `tools/a2_build/tests/test_ownership.py`
- Read: `lessons/a1/*.json`
- Read: `A2/LESSON_PLAN.md`

**Interfaces:**
- Produces `normalize_sk(text: str) -> str`.
- Produces `load_a1_owned(root: Path) -> set[str]` from canonical A1 `words[].sk` values.
- Produces `parse_a2_plan(path: Path) -> list[PlanLesson]` with section, order, title, intent and mapped lexical targets.
- Produces `classify_targets(plan_lesson, a1_owned, prior_a2_owned) -> list[OwnedTarget]` with `NEW|REVIEW|TRANSFER|MASTERY`.

- [ ] **Step 1: Write ownership tests**

```python
from pathlib import Path
from tools.a2_build.ownership import load_a1_owned, normalize_sk, parse_a2_plan

ROOT = Path(__file__).resolve().parents[3]

def test_a1_inventory_and_a2_map():
    a1 = load_a1_owned(ROOT / "lessons" / "a1")
    plan = parse_a2_plan(ROOT / "A2" / "LESSON_PLAN.md")
    assert len(a1) > 100
    assert len(plan) == 90
    assert plan[0].lesson_id == "a2-s01-l01"
    assert plan[-1].lesson_id == "a2-s15-l90"
    assert normalize_sk("  Lekáreň. ") == "lekáreň"
    assert "lekáreň" in a1
```

- [ ] **Step 2: Run tests and verify they fail before the ownership module exists**

Run: `python3 -m unittest tools.a2_build.tests.test_ownership -v`
Expected: FAIL with import/module errors.

- [ ] **Step 3: Implement deterministic plan parsing and A1 ownership extraction**

Use dataclasses:

```python
@dataclass(frozen=True)
class PlanLesson:
    section: int
    order: int
    lesson_id: str
    title: str
    intent: str
    mapped_targets: tuple[str, ...]

@dataclass(frozen=True)
class OwnedTarget:
    sk: str
    status: Literal["NEW", "REVIEW", "TRANSFER", "MASTERY"]
```

Parsing must assert 15 sections, six lessons per section, orders 1–90 exactly once, and non-empty mapped target lists.

- [ ] **Step 4: Rerun ownership tests**

Run: `python3 -m unittest tools.a2_build.tests.test_ownership -v`
Expected: PASS.

- [ ] **Step 5: Commit the ownership foundation**

```bash
git add tools/a2_build/model.py tools/a2_build/ownership.py tools/a2_build/tests/test_ownership.py
git commit -m "test: add A1 to A2 ownership foundation"
```

---

### Task 3: Implement the A2 generator and adversarial QA harness

**Files:**
- Create: `tools/a2_build/generator.py`
- Create: `tools/a2_build/qa_a2.py`
- Create: `tools/a2_build/schema_validate.py`
- Create: `tools/a2_build/tests/test_generator.py`
- Create: `tools/a2_build/tests/test_qa_a2.py`
- Runtime-only copies in `/tmp/slovakgo-a2-runtime/`: current application `lesson.schema.json`, `scripts/qa-lessons.ts`

**Interfaces:**
- `build_lesson(spec: LessonSpec, next_id: str | None) -> dict` returns `{"lessons":[lesson]}`.
- `write_batch(specs: Sequence[LessonSpec], out_dir: Path) -> list[Path]` writes stable UTF-8 JSON.
- `validate_file(path: Path) -> list[str]` returns adversarial/curriculum errors; empty list means green.
- `validate_schema(path: Path, schema_path: Path) -> None` raises on schema failure.

- [ ] **Step 1: Write a failing generator contract test**

```python
def test_generated_lesson_runtime_shape(sample_spec):
    doc = build_lesson(sample_spec, "a2-s01-l02")
    lesson = doc["lessons"][0]
    assert lesson["id"] == "a2-s01-l01"
    assert lesson["level"] == "A2"
    assert len(lesson["theoryScreens"]) == 3
    assert len(lesson["exercises"]) == 14
    assert len(lesson["finalSituation"]["steps"]) == 3
    assert lesson["resultScreen"]["nextLesson"] == "a2-s01-l02"
    assert lesson["localization"] == {"uiLanguages":["uk"], "targetLanguage":"sk", "fallbackUiLanguage":"uk"}
```

- [ ] **Step 2: Write failing adversarial tests**

Include fixtures that must be rejected for: duplicate option labels, two correct final options, unresolved `wordId`, mismatched `wordsScreen.sk`, sentence-builder token mismatch, sentence-order token mismatch, dropdown correct value absent, word-bank correct value absent, Russian-only learner UI leakage, Cyrillic in Slovak word field, and wrong `lessonId`.

- [ ] **Step 3: Run the focused tests and verify failure**

Run: `python3 -m unittest tools.a2_build.tests.test_generator tools.a2_build.tests.test_qa_a2 -v`
Expected: FAIL before generator/QA implementation.

- [ ] **Step 4: Implement only current runtime-safe exercise builders**

Provide explicit builders for the exercise mechanics used by A2:

```python
single_choice(...)
multiple_select(...)
true_false(...)
true_false_list(...)
fill_blank(...)
dropdown_blank(...)
cloze_text(...)
word_bank(...)
matching(...)
collocation(...)
sentence_builder(...)
sentence_order(...)
dialogue_order(...)
dialogue_choose_reply(...)
reading_comprehension(...)
meaning_in_context(...)
natural_phrase(...)
find_error(...)
correct_error(...)
transformation(...)
real_message(...)
real_schedule(...)
real_document(...)
```

Do not emit listening types. Each builder must encode the deterministic answer exactly as the current app checker expects.

- [ ] **Step 5: Implement the lesson shell and semantic QA**

The generator must create canonical `words` first and derive `wordsScreen.items` from those objects so `wordId/sk/uk/pronunciationUk/exampleSk/exampleUk` cannot drift. Final scenario helpers must require one marked correct option per step and take prompt/correct-answer pairs together so intent cannot be separated accidentally.

- [ ] **Step 6: Fetch the current app schema/checker to `/tmp/slovakgo-a2-runtime/` and record their blob SHAs in the build log**

Runtime commands after the files are present:

```bash
python3 tools/a2_build/schema_validate.py lessons/a2 /tmp/slovakgo-a2-runtime/lesson.schema.json
node --experimental-strip-types /tmp/slovakgo-a2-runtime/qa-lessons.ts lessons/a2
```

- [ ] **Step 7: Run all foundation tests**

Run: `python3 -m unittest discover -s tools/a2_build/tests -v`
Expected: PASS.

- [ ] **Step 8: Commit the generator and QA harness**

```bash
git add tools/a2_build
git commit -m "feat: add A2 generation and QA harness"
```

---

### Task 4: Produce and publish Batch 1 — S01–S03 / L01–L18

**Files:**
- Create: `tools/a2_build/specs_s01_s03.py`
- Create: `lessons/a2/a2-s01-l01.json` through `lessons/a2/a2-s03-l18.json`
- Create: `progress/A2_PROGRESS.md`

**Interfaces:**
- Spec module exports `SPECS: tuple[LessonSpec, ...]` containing exactly orders 1–18.
- Batch themes: personality/relationships; routines/habit change; recent-past narration.

- [ ] **Step 1: Author all 18 `LessonSpec` records from the exact mapped titles/intents/targets**

Each record must explicitly define: learner outcomes, three theory points, owned NEW vocabulary (excluding A1-owned repeats), review/transfer language, natural Slovak examples with Ukrainian translations, 14 exercise payloads/profile inputs, reading/dialogue context, and three final prompt/correct-answer pairs.

- [ ] **Step 2: Generate L01–L18**

Run: `python3 tools/a2_build/specs_s01_s03.py --out lessons/a2`
Expected: exactly 18 JSON files.

- [ ] **Step 3: Run batch gate**

```bash
python3 tools/a2_build/qa_a2.py lessons/a2 --from 1 --to 18
python3 tools/a2_build/schema_validate.py lessons/a2 /tmp/slovakgo-a2-runtime/lesson.schema.json --from 1 --to 18
node --experimental-strip-types /tmp/slovakgo-a2-runtime/qa-lessons.ts lessons/a2
```

Expected: all PASS; chain L01→L18 valid inside the known active prefix.

- [ ] **Step 4: Update progress only after the batch is green**

`progress/A2_PROGRESS.md` must say `18 / 90`, mark S01–S03 complete, and list the exact QA gates passed. It must not call A2 complete.

- [ ] **Step 5: Publish/read back remote files and compare Git blob identities or exact text**

Remote `main` must contain all 18 lesson paths and the progress file before the batch is accepted.

- [ ] **Step 6: Commit Batch 1**

```bash
git add tools/a2_build/specs_s01_s03.py lessons/a2 progress/A2_PROGRESS.md
git commit -m "content: add A2 sections 01 to 03"
```

---

### Task 5: Produce and publish Batch 2 — S04–S06 / L19–L36

**Files:**
- Create: `tools/a2_build/specs_s04_s06.py`
- Create: `lessons/a2/a2-s04-l19.json` through `lessons/a2/a2-s06-l36.json`
- Modify: `progress/A2_PROGRESS.md`

**Interfaces:**
- `SPECS` contains exactly orders 19–36.
- Themes: future/intentions/arrangements; home/problems/polite requests; city/routes/transport/duration.

- [ ] **Step 1: Author 18 explicit lesson specs with ownership labels and prerequisite-safe contexts.**
- [ ] **Step 2: Generate L19–L36 with `python3 tools/a2_build/specs_s04_s06.py --out lessons/a2`.**
- [ ] **Step 3: Run adversarial QA, current app schema, and current runtime checker over the full L01–L36 prefix, not only new files.**
- [ ] **Step 4: Verify boundary `a2-s03-l18 -> a2-s04-l19` and internal links through L36.**
- [ ] **Step 5: Update progress to `36 / 90`, publish, read back, then commit `content: add A2 sections 04 to 06`.**

---

### Task 6: Produce and publish Batch 3 — S07–S09 / L37–L54

**Files:**
- Create: `tools/a2_build/specs_s07_s09.py`
- Create: `lessons/a2/a2-s07-l37.json` through `lessons/a2/a2-s09-l54.json`
- Modify: `progress/A2_PROGRESS.md`

**Interfaces:**
- Themes: food/cooking/quantities; shopping/services/reclamations; work/study/deadlines/cooperation.

- [ ] **Step 1: Author 18 explicit lesson specs; flag obvious A1 repeats such as food, price, city/service and basic work words as REVIEW/TRANSFER instead of NEW.**
- [ ] **Step 2: Generate L37–L54.**
- [ ] **Step 3: Run all QA over L01–L54, including ownership collision and sentence-token audits.**
- [ ] **Step 4: Verify boundary `L36 -> L37`, full prefix chain, and exact 54-file prefix inventory.**
- [ ] **Step 5: Update progress to `54 / 90`, publish/read back, then commit `content: add A2 sections 07 to 09`.**

---

### Task 7: Produce and publish Batch 4 — S10–S12 / L55–L72

**Files:**
- Create: `tools/a2_build/specs_s10_s12.py`
- Create: `lessons/a2/a2-s10-l55.json` through `lessons/a2/a2-s12-l72.json`
- Modify: `progress/A2_PROGRESS.md`

**Interfaces:**
- Themes: hobbies/reasons/invitations/refusals; communication repair/problem solving/messages; travel/booking/accommodation/disruptions.

- [ ] **Step 1: Author 18 explicit lesson specs with stronger contextual production and real-message/schedule/document mechanics where natural.**
- [ ] **Step 2: Generate L55–L72.**
- [ ] **Step 3: Run all QA over L01–L72; specifically inspect Ukrainian register and Slovak politeness for invitations, refusals, requests and hotel/service situations.**
- [ ] **Step 4: Verify boundary `L54 -> L55`, full prefix chain and exact 72-file inventory.**
- [ ] **Step 5: Update progress to `72 / 90`, publish/read back, then commit `content: add A2 sections 10 to 12`.**

---

### Task 8: Produce and publish Batch 5 — S13–S15 / L73–L90

**Files:**
- Create: `tools/a2_build/specs_s13_s15.py`
- Create: `lessons/a2/a2-s13-l73.json` through `lessons/a2/a2-s15-l90.json`
- Modify: `progress/A2_PROGRESS.md`

**Interfaces:**
- Themes: health/doctor/pharmacy; opinions/reasons/comparisons/controlled conditional chunks; full A2 integration.

- [ ] **Step 1: Author 18 explicit lesson specs.**

For S14, keep `keby` / `radšej by som` as controlled A2 functional use and do not claim broader conditional mastery. For S15, require integrated use of past narration, future planning, problem solving, comparison/reasoning and communication repair.

- [ ] **Step 2: Generate L73–L90 with L90 terminal.**
- [ ] **Step 3: Run full-course local QA over all 90 files using adversarial QA, current app schema and current runtime checker.**
- [ ] **Step 4: Run final-situation semantic intent audit for every lesson, not a sample.**
- [ ] **Step 5: Run course inventory/chain assertion:**

```python
expected = [f"a2-s{((n-1)//6)+1:02d}-l{n:02d}" for n in range(1, 91)]
assert actual_ids == expected
for current, nxt in zip(lessons, expected[1:]):
    assert current["resultScreen"]["nextLesson"] == nxt
assert lessons[-1]["resultScreen"].get("nextLesson") in (None, "")
```

- [ ] **Step 6: Publish/read back all new files, but keep progress below COMPLETE until the remote audit in Task 9.**
- [ ] **Step 7: Commit Batch 5 as `content: add A2 sections 13 to 15`.**

---

### Task 9: Final remote audit, completion marker and production cleanup

**Files:**
- Modify: `progress/A2_PROGRESS.md`
- Delete: `tools/a2_build/specs_s01_s03.py`
- Delete: `tools/a2_build/specs_s04_s06.py`
- Delete: `tools/a2_build/specs_s07_s09.py`
- Delete: `tools/a2_build/specs_s10_s12.py`
- Delete: `tools/a2_build/specs_s13_s15.py`
- Delete remaining temporary `tools/a2_build/` files unless a specific QA file is deliberately promoted to a general durable tool with an A1–C2 name and continuing value.

**Interfaces:**
- Consumes the remote `main` tree, not local assumptions.
- Produces the only valid A2 completion claim.

- [ ] **Step 1: Fetch remote `main` head and recursive tree after Batch 5.**
- [ ] **Step 2: Assert exactly 90 `lessons/a2/a2-s*-l*.json` files with the exact ID/section/order map and no unexpected A2 lesson files.**
- [ ] **Step 3: Read back every lesson or a SHA-gated manifest sufficient to prove remote bytes equal the validated local outputs.**
- [ ] **Step 4: Re-run chain assertions from remote content, including every section boundary and terminal L90.**
- [ ] **Step 5: Confirm A1 remains 75 active lessons and was not rewritten by A2 production.**
- [ ] **Step 6: Update progress to:**

```text
# SlovakGo A2 — Progress
## Status
COMPLETE — 90 / 90 active lessons
```

Also list S01–S15 complete and record structural/schema/runtime/adversarial/ownership/semantic/remote inventory gates.

- [ ] **Step 7: Remove temporary A2 build/spec tooling, rerun remote-independent course QA from a clean checkout/workspace, and verify the deletion did not remove lesson data.**
- [ ] **Step 8: Commit cleanup and completion marker**

```bash
git add -A tools/a2_build progress/A2_PROGRESS.md
git commit -m "chore: finalize A2 course at 90 lessons"
```

- [ ] **Step 9: Fetch `main` again and require the final head to contain 90/90 lessons, COMPLETE progress, correct terminal chain, and no temporary A2 builder before reporting completion.**

---

## Plan self-review checklist

- Every spec requirement maps to Tasks 1–9: runtime/schema priority, A1 ownership, five batches, varied lesson shape, semantic finals, remote audit, progress gating and cleanup.
- No task permits marking A2 complete from local generation alone.
- The plan explicitly resolves the stale A1-only repository instructions before A2 content is produced.
- Runtime validation uses the current application checker rather than `tools/qa_a1.py`, which is stale and A1-specific.
- Publication remains `isPublished:false`; no app-runtime redesign or A1 rewrite is included.
