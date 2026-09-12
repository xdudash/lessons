# SlovakGo A1 Progress

STATUS: IN_PROGRESS

COMPLETED:
- Audited the original 250-lesson A1 baseline and preserved its source-derived inventories and vocabulary matrix as reference data.
- Adopted content-led Course Architecture v2 and the dynamic lesson-count model.
- Registered the user's `A1-S01-L01` as the canonical gold-standard lesson reference and preserved its exact source SHA-256: `791187eccecc56fe7617706392f2d1e2d3bdce9af8b7c274505439c98ea91cd0`.
- Rebuilt S01 L01–L10 under Architecture v2; L01 remains the canonical gold-standard lesson.
- Removed superseded S01 L11–L40 from the active lesson tree. They were thin/fixed-slot lessons from the retired quota model and are not production-final.
- Removed the obsolete S01 pilot QA artifacts tied specifically to the deleted L11–L40 batch.
- Removed the obsolete fixed-slot A1 1,000-lesson map from the curriculum tree.
- Rebuilt S02 L01–L19 under Architecture v2 with recorded QA FULL PASS.

S01 CURRENT STATE:
- L01: GOLD — preserved unchanged.
- L02–L10: REBUILT + QA FULL PASS.
- Active S01 ends at L10 for now. No filler lessons are implied by this endpoint.
- If the prerequisite graph later shows that an S01 function is missing, create a new Architecture v2 lesson only for that distinct pedagogical need.

S02 CURRENT STATE:
- L01–L19: REBUILT + QA FULL PASS.

CLEANUP DECISION:
- The former fixed-slot model (including the old 10K allocation and S01 L11–L40 production) is superseded.
- Deleted lessons are not archived in the active repository. Useful functions from them may be rebuilt later in the correct section and prerequisite position rather than restored as-is.
- Structural validity alone is not enough; lesson quality is judged by instructional depth, learner work, transfer, and mastery progression against Architecture v2 and the gold standard.

UNRESOLVED:
- Complete A1 remapping of every section against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Apply the pending title correction `a1-s08-l06` → `Bývam v byte alebo dome?` if it is still present in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Continue S02 beyond L19 with the next distinct communicative function under Architecture v2, while keeping the dynamic lesson-count rule and performing batch QA where reliable.

DEPENDENCIES:
- `MASTER.md`
- `AGENT_PROTOCOL.md`
- `curriculum/COURSE_ARCHITECTURE_V2.md`
- `curriculum/GOLD_STANDARD_LESSON.md`
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`
