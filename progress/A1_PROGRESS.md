# A1 Progress

## Status

**IN_PROGRESS — Section 01 QA**

## Active production model
- Complete Slovak A1–C2 course.
- No predetermined total lesson quota.
- Lesson count is derived from atomic targets, prerequisites, review, transfer and mastery evidence.
- No filler lessons.
- GitHub `main` is the authoritative durable state.

## A1 architecture
A1 currently has 14 thematic units with an initial working estimate of 82 lessons. The 82 count is provisional and is not a quota.

## Section 01 — Sounds, reading and basic word structure
Six lessons are rebuilt from a clean importable lesson contract:
1. `a1-s01-l01` — Slovenská abeceda
2. `a1-s01-l02` — Samohlásky a spoluhlásky
3. `a1-s01-l03` — Slabikotvorné r, ŕ, l, ĺ
4. `a1-s01-l04` — Mäkké spoluhlásky a výslovnosť
5. `a1-s01-l05` — Dĺžka, dvojhlásky a rytmus
6. `a1-s01-l06` — Prízvuk, intonácia a krátke správy

The previous six lesson files were deleted before this rebuild. The obsolete A1_S01_S05 batch QA artifact was also removed.

## Import contract
The files use the application's supported top-level import envelope:
`{"lessons":[...]}`

Each lesson contains metadata, words, theory screens, start screen, words screen, 16 exercises, interactive final situation and result screen. Exercise types are limited to the application's declared exercise library.

## QA gate
Before Section 01 is marked production-final:
1. JSON parse check
2. importer contract check against `parseImportJson`
3. Slovak language/orthography QA
4. exercise-answer QA
5. pedagogy and progression QA
6. localization QA
7. mastery/transfer QA
8. final GitHub tree verification

## Next task
Run the complete Section 01 QA gate. Do not add Section 02 until Section 01 passes.
