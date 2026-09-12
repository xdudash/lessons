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
- Added the exact user-provided canonical gold-standard lesson JSON to `lessons/a1/a1-s01-l01.json` unchanged; source SHA-256: `791187eccecc56fe7617706392f2d1e2d3bdce9af8b7c274505439c98ea91cd0`.
- Adopted content-led Course Architecture v2 in `curriculum/COURSE_ARCHITECTURE_V2.md`.
- Audited and rebuilt S01 L01–L10 under Architecture v2.
- Rebuilt S02 L01–L12 under Architecture v2; all recorded QA FULL PASS.
- Rebuilt S02 L15–L19 under Architecture v2; batch QA FULL PASS in `audits/A1_S02_L15_L19_QA.md`.

S01 REBUILD STATUS:
- L01: GOLD — preserved unchanged.
- L02–L10: REBUILT + QA FULL PASS.

S02 REBUILD STATUS:
- L01: REBUILT + QA FULL PASS — `ja som / ty si / on/ona je`.
- L02: REBUILT + QA FULL PASS — group identity with `my / sme`.
- L03: REBUILT + QA FULL PASS — origin vs residence.
- L04: REBUILT + QA FULL PASS — introducing/identifying another person.
- L05: REBUILT + QA FULL PASS — integration/transfer.
- L06: REBUILT + QA FULL PASS — language ability and comprehension management.
- L07: REBUILT + QA FULL PASS — contact information.
- L08: REBUILT + QA FULL PASS — arranging a simple meeting by day/time.
- L09: REBUILT + QA FULL PASS — agreeing on a meeting place.
- L10: REBUILT + QA FULL PASS — inviting, accepting and declining a simple invitation.
- L11: REBUILT + QA FULL PASS — giving a simple home address and linking it to residence.
- L12: REBUILT + QA FULL PASS — simple registration and checking personal data.
- L13–L14: REPOSITORY GAP — not falsely marked complete.
- L15: REBUILT + QA FULL PASS — simple preferences with `Mám rád / Mám rada`.
- L16: REBUILT + QA FULL PASS — preferred activities with familiar action verbs.
- L17: REBUILT + QA FULL PASS — simple frequency with `často / niekedy`.
- L18: REBUILT + QA FULL PASS — weekend activities using established preference/frequency models.
- L19: REBUILT + QA FULL PASS — integration/mastery of personal information in a short conversation.

ACCELERATED BATCH NOTE:
- Production now uses multi-lesson batches when schema and pedagogical verification remain reliable.
- L15–L19 were reviewed as one pedagogical sequence; no weak preliminary drafts were promoted to production.
- Lesson count remains dynamic; no filler lessons are created merely to increase the number.

HISTORICAL WORK UNDER SUPERSEDED MODEL:
- The previous A1 1,000-slot map and 750-slot expansion registry were created under the former quota model.
- S01 L11–L40 were generated and QA-approved under that former model.
- Those lessons were removed from the active lesson tree and are not automatically accepted as final under Architecture v2.
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

UNRESOLVED:
- Resolve the S02 L13–L14 repository gap before treating S02 as continuous end-to-end.
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for superseded S01 L11–L40 is still required only if those functions are needed by the dynamic curriculum.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Resolve **S02 L13–L14** as the next repository/content decision, then continue the dynamic S02 sequence. Do not create filler solely to restore numbering.

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
