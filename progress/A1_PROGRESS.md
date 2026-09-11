# SlovakGo A1 Progress

STATUS: IN_PROGRESS

COMPLETED:
- Audited the 250-lesson A1 baseline.
- Encoded the source-derived A1 grammar, vocabulary and communicative-function inventory.
- Encoded the A1 prerequisite graph and A1→A2 handoff dependencies.
- Preserved the distinction between functional exposure and productive mastery.
- Derived the complete item-level vocabulary ownership/review analysis from the authoritative 250-lesson package.
- Stored the complete item-level matrix durably in GitHub at `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`.
- Registered the user's `A1-S01-L01` as the canonical gold-standard lesson reference in `curriculum/GOLD_STANDARD_LESSON.md`.
- Adopted content-led Course Architecture v2 in `curriculum/COURSE_ARCHITECTURE_V2.md` and `MASTER.md`.
- Audited A1 Section 01 L01–L10 against the gold standard: L01 remains GOLD; L02–L10 require revision for pedagogical alignment, sequencing and repeated theory rather than for structural density.
- Rebuilt and committed `lessons/a1/a1-s01-l02.json` against Architecture v2. Commit: `c3b7e4984c5d0c23eca693c7a90bd49b63c53d54`.

HISTORICAL WORK UNDER SUPERSEDED MODEL:
- The previous A1 1,000-slot map and 750-slot expansion registry were created under the former quota model.
- S01 L11–L40 were generated and QA-approved under that former model.
- Those lessons are preserved as historical generated work, but they are NOT automatically accepted as final under Architecture v2.
- The previous 10K numerical allocation is historical planning data, not a production quota.

KEY FINDINGS:
- Existing A1 baseline: 250 lessons, 25 sections × 10 lessons.
- The former rule to skip L01–L10 and begin new production at L11 is retired.
- Every section must now be planned from L01 onward, including the existing first ten lessons.
- Structural validity is not equivalent to gold-standard pedagogical completeness.
- The gold-standard lesson is the quality reference; lesson count is not.
- Repetition remains intentional when it supports NEW → REVIEW → TRANSFER → MASTERY.
- Application/UI limitations must not cause pedagogical fields or lesson depth to be removed.

S01 L01–L10 AUDIT DECISIONS:
- L01: GOLD — preserve unchanged.
- L02: REBUILT — target is the name-question/name-answer pattern; theory no longer copies L03/L05.
- L03: REBUILD — focus ty/vy choice and ty → si / vy → ste.
- L04: REBUILD — focus politeness functions; remove unrelated re-teaching.
- L05: REBUILD — genuine integrated review of L01–L04 with little/no new grammar.
- L06: REBUILD — spelling/name handling must be aligned to its actual target.
- L07: REBUILD — vowel length target must be supported without repeating unrelated L01 theory.
- L08: REBUILD — classroom commands and repair strategy must be sequenced and contextualized.
- L09: REBUILD — first-contact integration, not copied ty/vy/name theory.
- L10: REBUILD — true mastery/checkpoint lesson with minimal new theory and stronger transfer evidence.

UNRESOLVED:
- Commit rebuilt L03–L05 and QA them before proceeding to L06–L10.
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Rebuild **A1 Section 01 L03–L05** against the gold standard, preserving L01 and the newly rebuilt L02. QA each lesson before committing. Do not generate L06–L10 yet.

DEPENDENCIES:
- `MASTER.md`
- `AGENT_PROTOCOL.md`
- `curriculum/COURSE_ARCHITECTURE_V2.md`
- `curriculum/GOLD_STANDARD_LESSON.md`
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`
- Existing 250-lesson A1 package
