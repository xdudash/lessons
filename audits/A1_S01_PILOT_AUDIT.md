# A1 S01 Pilot Audit — L11–L13

STATUS: PILOT REVIEW COMPLETE / CONDITIONAL PASS

## Scope

Pilot lessons:
- `a1-s01-l11` — Ráno, deň a večer
- `a1-s01-l12` — Ahoj alebo Dobrý deň?
- `a1-s01-l13` — Správna rozlúčka

## Checks

### 1. Structural envelope
PASS — all three files use the established `lessons` array envelope and preserve the core lesson metadata, localization, start screen, theory, words, exercises, final check and result screen structure.

### 2. Section/level/slot identity
PASS — all are A1, section `a1-s01`, and occupy L11–L13 expansion slots.

### 3. Progression role
PASS — L11–L13 are stabilization lessons, matching the target registry. They do not introduce a new advanced grammatical system.

### 4. Vocabulary discipline
PASS — pilot vocabulary is drawn from the established S01 baseline expressions visible in the authoritative source sample: `Ahoj`, `Dobrý deň`, `Dobré ráno`, `Dobrý večer`, `Dovidenia`. The pilot therefore tests controlled variation before adding new lexical inventory.

### 5. Duplication control
PASS WITH NOTE — the pilot deliberately reuses the core S01 greeting set because its role is STAB. Distinct lesson jobs are: time-of-day selection (L11), register/situation selection (L12), and greeting-vs-goodbye distinction (L13). These are not intended as exact duplicate lessons.

### 6. Answer validity
PASS — each multiple-choice/final item has one intended correct answer; sentence-builder/order answers are explicitly specified; correction items provide accepted answers.

### 7. CEFR/progression safety
PASS — content remains within the established A1 first-contact scope. No systematic case paradigm, aspect system, advanced subordination, or other deferred content is introduced.

### 8. UI-contract discipline
PASS — content retains semantically meaningful `prompt`, `dialogue`, `context`, `target`, `situation`, `skill` and other fields even where the current application has known rendering gaps. The content was not rewritten to hide those application issues.

## Findings / required follow-up

1. The pilot should be tested in the application before S01 expansion continues.
2. Application-level rendering bugs previously documented remain application work, not content work.
3. The pilot intentionally does not prove that exact item-level ownership is complete for every future lesson; it proves the generation/QA workflow on a bounded stabilization batch.
4. Do not mass-generate from this pilot until application testing and content review confirm the pattern.

## Decision

**CONDITIONAL PASS.** The three lessons are suitable as a controlled pilot artifact. The next project action is application/content validation of these exact files, followed by a second pilot band only if no content/schema defects are found.
