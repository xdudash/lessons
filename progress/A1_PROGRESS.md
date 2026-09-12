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
- Rebuilt S01 L02–L05 against Architecture v2.
- Rebuilt S01 L06 to materially match the gold lesson's depth: 20 exercises, 13 types, 3 final-situation steps and result screen. QA FULL PASS.
- Rebuilt S01 L07 around vowel-length discrimination and expanded it to gold-standard depth: 20 exercises, 13 types, reading, dialogues, contextual practice and 3-step final scenario. QA follow-up remains unresolved.
- Rebuilt S01 L08 to gold-standard depth: 22 exercises, 13 types, reading, dialogues, real-life practice and 3-step final scenario. QA FULL PASS.
- Rebuilt S01 L09 as a genuine integrated first-meeting lesson: 20 exercises, 13 types, 2 theory blocks, 2 reading tasks, dialogue/real-life transfer, 3-step final scenario and result screen. QA FULL PASS.
- Rebuilt S01 L10 as the Section 01 mastery/check lesson: 22 exercises, 13 types, review/strategy theory, reading, dialogue, writing, real-life practice, 3-step final scenario and result screen. QA FULL PASS. QA file: `audits/A1_S01_L10_QA.md`.

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
- L10: REBUILT + QA FULL PASS — section mastery/check.

UNRESOLVED:
- QA S01 L07 against the canonical schema and gold-standard quality.
- Close Section 01 consistency review after L07 QA.
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- QA **S01 L07** against the canonical schema and gold-standard quality. Then perform a consistency review of S01 L01–L10 before moving to the next section. Do not generate later lessons yet.

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
