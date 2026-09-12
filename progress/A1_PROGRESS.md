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
- Rebuilt and committed `lessons/a1/a1-s01-l03.json`. Commit: `c2e95b65d4482ab72f0548f87d84dc100313cb71`.
- Rebuilt and committed `lessons/a1/a1-s01-l04.json`. Commit: `c70285a031b8e13cf3f2a4b06e0156783ac5af2e`.
- Rebuilt and committed `lessons/a1/a1-s01-l05.json`. Commit: `2f67b1895fa16674210e2b11019d21277204e872`.
- QA for S01 L03–L05 recorded as FULL PASS in `audits/A1_S01_L03_L05_QA.md`. Commit: `c94572f214f97dbb1d37ca501965b0f8260ac246`.
- Rebuilt and normalized `lessons/a1/a1-s01-l06.json` against the gold-standard envelope. Added the missing `resultScreen` and replaced the weak vocabulary example `pán Urban` with the more useful/relevant `priezvisko`. Commit: `4a0cee56d4895d8fb5837de3d1113d78dd7e4885`.
- Rebuilt and committed `lessons/a1/a1-s01-l07.json` around the actual target of Slovak vowel-length discrimination, avoiding the former duplicated theory from L01. Commit: `d823d8a9ad505bb6dc7d7a26b0cf439fe973ace9`.

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

S01 REBUILD STATUS:
- L01: GOLD — preserved unchanged.
- L02: REBUILT — focused on `Ako sa voláš?` → `Volám sa...`.
- L03: REBUILT — focused on `ty/vy` choice and `si/ste` contrast.
- L04: REBUILT — focused on politeness functions.
- L05: REBUILT — genuine integrated retrieval/review with minimal new grammar.
- L06: REBUILT + NORMALIZED — spelling/name-writing task with complete lesson envelope.
- L07: REBUILT — vowel-length discrimination using familiar, meaningful examples.

UNRESOLVED:
- QA S01 L06–L07 against the canonical schema and gold-standard quality before treating them as final.
- Rebuild and QA S01 L08–L10.
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- QA **S01 L06–L07** against the gold standard and schema. Then rebuild **S01 L08**, followed by L09 and L10. Do not generate later lessons yet.

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
