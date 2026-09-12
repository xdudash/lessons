# A1 Progress

## Status

**IN_PROGRESS — Sections 03–05 rebuilt to the canonical importer-oriented lesson format; semantic/import QA remains the final gate.**

## Active production model
- Complete Slovak A1–C2 course.
- No fixed total lesson quota.
- Lesson count follows atomic targets, prerequisites, review, transfer and mastery needs.
- Slovak is the target language; learner-facing instructions, prompts and explanations are Ukrainian.
- GitHub `main` is the durable source of truth.

## Section 02
Section 02 uses five denser lessons:
- `a1-s02-l07` — Kto som?
- `a1-s02-l08` — Ja, ty, on, ona, ono
- `a1-s02-l09` — Zoznámime sa
- `a1-s02-l10` — O mne
- `a1-s02-l11` — Predstavím sa

## Section 03 — Ľudia, rodina a opis
Active rebuilt set:
- `a1-s03-l18` — Ľudia a vzťahy
- `a1-s03-l19` — Rod a súhlas
- `a1-s03-l20` — Opis človeka
- `a1-s03-l21` — Rodina a osobné údaje
- `a1-s03-l22` — Opis a integrácia

All five were rewritten to the same canonical lesson structure as the known-working importer example: `lessons` envelope, scalar lesson metadata, `startScreen`, `theoryScreens`, `wordsScreen`, `words`, 12 exercises, `finalSituation`, and `resultScreen`.

## Section 04 — Veci, vlastníctvo a môj svet
Active rebuilt set:
- `a1-s04-l23` — Čo je to?
- `a1-s04-l24` — Môj, moja, moje
- `a1-s04-l25` — Jeho, jej a naše veci
- `a1-s04-l26` — Mám a nemám

## Section 05 — Dom, izby a miesto vecí
Active rebuilt set:
- `a1-s05-l27` — Domov a izby
- `a1-s05-l28` — Nábytok a predmety
- `a1-s05-l29` — Kde je vec?
- `a1-s05-l30` — Môj domov

## Legacy numerical block requiring remap
The existing files `a1-s03-l12` through `a1-s03-l17` contain the earlier numerical curriculum block (Čísla a údaje). Current course architecture places numerical/quantity/time/date content in thematic unit 07, not Section 03. These files must be remapped only after the complete lesson-number map for Sections 06–07 is established; they are not being silently relabeled in this pass.

## QA state
- Structural envelope for rebuilt Sections 03–05: PASS by construction against the known-working lesson contract.
- Section numbering/IDs: PASS for the rebuilt files (`l18–l30`).
- Learner-facing language: rebuilt in Ukrainian; target content in Slovak.
- Final/result structures: normalized to the known-working example contract.
- Vocabulary: 12 meaningful entries per rebuilt lesson, with contextual examples and exercise reuse.
- Real application importer: NOT CLAIMED. The importer is not available in this environment.
- Full semantic QA: still required before declaring Sections 03–05 complete.

## Next gate
Run a final semantic review of `l18–l30`, then run the real application import test when the importer is available. Only after those gates pass should these sections be marked complete.