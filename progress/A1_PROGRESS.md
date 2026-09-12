# A1 Progress

## Status

**IN_PROGRESS — Section 03 produced; semantic/import QA pending**

## Active production model
- Complete Slovak A1–C2 course.
- No predetermined total lesson quota.
- Lesson count is derived from atomic targets, prerequisites, review, transfer and mastery evidence.
- No filler lessons.
- GitHub `main` is the authoritative durable state.
- Student-facing instructions and exercise prompts are in Ukrainian; Slovak is the target language being learned/tested.

## Current A1 architecture
A1 currently has 14 thematic units. The working total remains provisional and is not a quota.

## Section 01
Section 01 — Sounds, reading and basic word structure — 6 lessons.
The six lesson files remain in `lessons/a1/` and require dedicated semantic/import QA.

## Section 02 — O mne
Section 02 was rebuilt from seven narrow lessons into five denser lessons:
1. `a1-s02-l07` — Kto som?
2. `a1-s02-l08` — Ja, ty, on, ona, ono
3. `a1-s02-l09` — Zoznámime sa
4. `a1-s02-l10` — O mne
5. `a1-s02-l11` — Predstavím sa

The five-lesson design increases lexical depth, contextual practice and transfer while preserving the section outcomes. Dedicated semantic/import QA remains a separate gate.

## Section 03 — Čísla a údaje
Section 03 has now been produced as six coherent lessons, following the current pedagogical architecture for this section:

1. `a1-s03-l12` — Čísla 0–20 — number recognition, naming and Koľko?
2. `a1-s03-l13` — Vek a čísla — age questions and answers
3. `a1-s03-l14` — Telefónne číslo — phone numbers, digit sequences and repetition repair
4. `a1-s03-l15` — Adresa — street, house number and simple address exchange
5. `a1-s03-l16` — Cena a množstvo — price, quantity and euro expressions
6. `a1-s03-l17` — Čísla v praxi — integrated numerical information across real situations

### Lesson design
The Section 03 lessons use the importer-compatible lesson JSON structure established by the project's known-working examples and the active `AGENTS.md` contract. Vocabulary is deliberately richer than the old six-item baseline where useful; each lesson contains meaningful new items and repeated functional language.

The section progresses from isolated number recognition to functional numerical communication. It covers age, phone numbers, addresses, price, quantity and integrated identification of what a numerical question is asking for.

### QA status
- File/tree presence: PASS — `a1-s03-l12` through `a1-s03-l17` are present in `lessons/a1/`.
- Lesson numbering: PASS — sequence follows Section 02's l07–l11 and Section 03 continues at l12.
- Cross-reference repair: PASS — detected broken `l12` sequence and broken `l17` word reference were repaired before continuing.
- Structural JSON: authored in valid `{"lessons":[...]}` form; dedicated semantic/import QA remains to be run as a separate gate.
- Importer: NOT CLAIMED — no actual application importer run is available in this environment.

## Next task
Run dedicated semantic/import QA on Section 03, repair every hard failure, then proceed to the next coherent section/batch according to the repository protocol.
