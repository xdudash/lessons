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
- Rebuilt S01 L06 to materially match the gold lesson's depth rather than only its minimum structure: 2 theory screens, 6 target expressions, 20 exercises, 13 exercise types, 3 final-situation steps and a result screen. Commit: `1d289bde24a1111f58525fa8737de9a7be4c77d7`.
- QA for S01 L06 recorded as FULL PASS. Commit: `2d8e34f07926c8386e867c63d4a25ed04a0c3f55`.
- Rebuilt S01 L07 around vowel-length discrimination and expanded it to gold-standard depth: 20 exercises, 13 exercise types, reading, dialogues, contextual practice and a 3-step final scenario. Commit: `215f9725a667a0bf033e7fa57edd85942936dd2a`.
- Rebuilt S01 L08 to gold-standard depth: 22 exercises, 13 exercise types, reading, dialogues, real-life practice and a 3-step final scenario. Commit: `27e8c61b29a6c132ea8ae11d3191a96f106aee8b`.
- QA for S01 L08 recorded as FULL PASS. Commit: `3ab6a45167c74739b0ac2bdba5814b77f96a9ef9`.
- Rebuilt S01 L09 as a genuine integrated first-meeting lesson: 20 exercises, 13 types, 2 theory blocks, 2 reading tasks, dialogue/real-life transfer, 3-step final scenario and result screen. Commit: `01900d85030beef68b13e46574efe6ec40cc96fc`.
- QA for S01 L09 recorded as FULL PASS. Commit: `8837a4ed9de408e3ed3d47f45241fcc16171f380`.

HISTORICAL WORK UNDER SUPERSEDED MODEL:
- The previous A1 1,000-slot map and 750-slot expansion registry were created under the former quota model.
- S01 L11–L40 were generated and QA-approved under that former model.
- Those lessons are preserved as historical generated work, but they are NOT automatically accepted as final under Architecture v2.
- The previous 10K numerical allocation is historical planning data, not a production quota.

KEY FINDINGS:
- Existing A1 baseline: 250 lessons, 25 sections × 10.
- The former rule to skip L01–L10 and begin new production at L11 is retired.
- Every section must now be planned from L01 onward, including the existing first ten lessons.
- Structural validity is not equivalent to gold-standard pedagogical completeness.
- The gold-standard lesson is the quality reference; lesson count is not.
- Repetition remains intentional when it supports NEW → REVIEW → TRANSFER → MASTERY.
- Application/UI limitations must not cause pedagogical fields or lesson depth to be removed.
- Lesson quality must be judged by actual instructional depth and learner work, not by hitting a fixed exercise count.

S01 REBUILD STATUS:
- L01: GOLD — preserved unchanged.
- L02: REBUILT — focused on `Ako sa voláš?` → `Volám sa...`.
- L03: REBUILT — focused on `ty/vy` choice and `si/ste` contrast.
- L04: REBUILT — focused on politeness functions.
- L05: REBUILT — genuine integrated retrieval/review with minimal new grammar.
- L06: REBUILT + QA FULL PASS — spelling/name-writing task expanded to a gold-standard depth.
- L07: REBUILT — vowel-length discrimination expanded to gold-standard depth; final QA follow-up remains required.
- L08: REBUILT + QA FULL PASS — classroom instructions, comprehension repair and polite repetition requests.
- L09: REBUILT + QA FULL PASS — integrated first-meeting scenario.

UNRESOLVED:
- QA S01 L07 against the canonical schema and gold-standard quality.
- Rebuild and QA S01 L10.
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Rebuild **S01 L10** as the true Section 01 mastery/check lesson, then QA it. Do not generate later lessons yet.

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
