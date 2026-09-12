# A1 Progress

## Status

**IN_PROGRESS — Sections 06–08 added in the new one-pass three-section workflow; semantic/import QA remains the final gate.**

## Active production model
- Complete Slovak A1–C2 course.
- No fixed total lesson quota.
- Lesson count follows atomic targets, prerequisites, review, transfer and mastery needs.
- Slovak is the target language; learner-facing instructions, prompts and explanations are Ukrainian.
- GitHub `main` is the durable source of truth.
- Three coherent sections are produced as one batch before moving to the next batch.

## Section 02
Section 02 uses five denser lessons:
- `a1-s02-l07` — Kto som?
- `a1-s02-l08` — Ja, ty, on, ona, ono
- `a1-s02-l09` — Zoznámime sa
- `a1-s02-l10` — O mne
- `a1-s02-l11` — Predstavím sa

## Section 03 — Ľudia, rodina a opis
Active rebuilt set: `a1-s03-l18` through `a1-s03-l22`.

## Section 04 — Veci, vlastníctvo a môj svet
Active rebuilt set: `a1-s04-l23` through `a1-s04-l26`.

## Section 05 — Dom, izby a miesto vecí
Active rebuilt set: `a1-s05-l27` through `a1-s05-l30`.

## Section 06 — Actions and my everyday day
New batch:
- `a1-s06-l31` — Čo robím každý deň
- `a1-s06-l32` — Ako sa menia slovesá
- `a1-s06-l33` — Môj deň

The three lessons cover core everyday actions, present-tense person forms, infinitive exposure, sequence/time language and an integrated short account of the learner's day.

## Section 07 — Numbers, quantity, time and dates
New batch:
- `a1-s07-l34` — Čísla a množstvo
- `a1-s07-l35` — Koľko je hodín?
- `a1-s07-l36` — Plán a rozvrh

The three lessons cover core numbers/quantity, simple clock time, days/dates, schedules and basic arrangements.

## Section 08 — City, place and movement
New batch:
- `a1-s08-l37` — Miesta v meste
- `a1-s08-l38` — Kam idem?
- `a1-s08-l39` — Cesta a doprava

The three lessons cover city places, current location, movement, directions, transport, route questions and a practical travel situation.

## Legacy numerical block requiring later remap
The existing files `a1-s03-l12` through `a1-s03-l17` contain the earlier numerical curriculum block. The current architecture places numerical/quantity/time/date content in thematic unit 07, while these legacy files still carry `a1-s03` identifiers. They are intentionally not silently relabeled in this batch; a later remap must use the complete lesson-number map and preserve repository integrity.

## One-pass workflow
The durable production workflow is documented in `AGENT_ONE_PASS_WORKFLOW.md`. Future agents must treat a three-section batch as one coherent production unit: map targets first, generate the whole batch, run batch-wide structural/semantic/adversarial checks, then write to GitHub and read back the stored state before updating progress.

## QA state
- New Sections 06–08 use the canonical importer-oriented envelope based on the known-working lesson example.
- Section numbering/IDs for `l31–l39`: PASS on the repository tree.
- Learner-facing language: Ukrainian; target content: Slovak.
- Vocabulary: 12 working entries per new lesson with reuse in exercises/context.
- Real application importer: NOT CLAIMED. The importer is not available in this environment.
- Full semantic QA: still required for `l31–l39`.

## Next gate
Run batch-wide semantic/adversarial QA for Sections 06–08, then use the real application importer when available. Do not mark the batch complete based only on JSON syntax or repository presence.