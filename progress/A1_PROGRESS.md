# A1 Progress

## Status

**IN_PROGRESS — Sections 03–05 produced; dedicated semantic/import QA remains required**

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

## Section 03 — Ľudia, rodina a opis
Section 03 has now been produced as five coherent lessons:
1. `a1-s03-l18` — Ľudia a vzťahy — people, family and basic relationships
2. `a1-s03-l19` — Rod a súhlas — gender and basic adjective agreement
3. `a1-s03-l20` — Opis človeka — basic description with adjectives
4. `a1-s03-l21` — Rodina a osobné údaje — family, age and professions
5. `a1-s03-l22` — Opis a integrácia — integrated description and dialogue

The lesson count was reduced/optimized where targets could be grouped without a filler lesson. Vocabulary is richer than the old six-item baseline where useful and is reused for stabilization, transfer and integration.

## Section 04 — Veci, vlastníctvo a môj svet
Section 04 has now been produced as four coherent lessons:
1. `a1-s04-l23` — Čo je to? — objects and basic identification
2. `a1-s04-l24` — Môj, moja, moje — possessive forms in simple phrases
3. `a1-s04-l25` — Jeho, jej a naše veci — his/her/our possession
4. `a1-s04-l26` — Mám a nemám — possession and negation

The four-lesson design covers object naming, gender-sensitive possessives, other-person/group possession and practical have/do-not-have communication.

## Section 05 — Dom, izby a miesto vecí
Section 05 has now been produced as four coherent lessons:
1. `a1-s05-l27` — Domov a izby — home and rooms
2. `a1-s05-l28` — Nábytok a predmety — furniture and objects
3. `a1-s05-l29` — Kde je vec? — location and core spatial models
4. `a1-s05-l30` — Môj domov — integrated home description and object location

The four-lesson design covers home/rooms, furniture/objects, basic spatial preposition models and integrated room/home description.

## Production QA status for Sections 03–05
- File creation: PASS — new lessons `l18–l30` were written to `lessons/a1/`.
- Numbering: PASS — Section 03 starts at `l18`, Section 04 continues at `l23`, Section 05 continues at `l27`.
- Section sequencing: PASS — `l22 → l23 → l26 → l27 → l30` references are designed to continue across sections; final `l30` currently has `nextLesson: null` because Section 06 is not yet produced.
- JSON envelope: authored with `{"lessons":[...]}` and created as UTF-8 JSON files.
- Target language: Slovak (slovenčina), not Slovenian.
- Learner-facing language: Ukrainian.
- Vocabulary: intentionally expanded and reused rather than held to an artificial six-item quota.
- Exercise variety: each produced lesson includes mixed exercise mechanics and a final transfer situation.
- Importer: NOT CLAIMED — the real application importer is not available in this environment.
- Dedicated semantic QA: REQUIRED — before these sections can be marked complete, review every exercise, answer, `wordId`, Slovak form, Ukrainian learner-facing string and final situation as one batch and run the actual importer when available.

## Next task
Run a dedicated batch semantic/import QA on Sections 03–05 as a single production batch, repair all hard failures, verify the GitHub tree again, and only then mark the batch complete and proceed to Section 06.