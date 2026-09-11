# SlovakGo A1 Progress

STATUS: COMPLETE

COMPLETED:
- Audited the 250-lesson A1 baseline.
- Encoded the source-derived A1 grammar, vocabulary and communicative-function inventory.
- Encoded the A1 prerequisite graph and A1→A2 handoff dependencies.
- Preserved the distinction between functional exposure and productive mastery.
- Built the complete A1 1,000-slot curriculum map: 25 sections × 40 slots, preserving the existing 250 baseline and defining 750 expansion slots.

FILES CHANGED:
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `curriculum/A1_1000_MAP.md`
- `progress/A1_PROGRESS.md`

KEY FINDINGS:
- Baseline: 250 lessons, 25 sections, 1,500 vocabulary entries, 1,272 unique expressions, 4,256 exercises.
- The 1,000-slot A1 plan is now explicitly bounded: every section keeps authoritative L01–L10 and adds planned L11–L40.
- The 750 expansion slots are organized as stabilization, contrast, transfer, expansion, integration and mastery bands.
- The map intentionally does not invent concrete lesson JSON for the 750 slots before item-level ownership and baseline overlap are checked.
- Functional-but-not-systematic areas remain case forms, plural formation, imperative, reflexive verbs and conjugation families.
- Systematic aspect mastery remains deferred to A2/B1.
- Repetition remains deliberate NEW → REVIEW → TRANSFER → MASTERY.
- The duplicate title `Kde bývaš?` remains a publishing correction item for `a1-s08-l06`.

UNRESOLVED:
- Item-level NEW/REVIEW/TRANSFER/MASTERY ownership for every vocabulary expression.
- Concrete target assignment for each of the 750 expansion slots after corpus-level overlap checking.
- Full external Slovak CEFR/RLD verification of the inventory.
- The broader 10K curriculum files still need to be present in the repository before they can be treated as the durable 10K source of truth.

NEXT TASK:
- Build the item-level vocabulary ownership/review matrix for the 250 baseline, then assign concrete targets to the 750 A1 expansion slots. After that, generate a small reviewed pilot batch rather than mass-producing all 750 lessons.

DEPENDENCIES:
- `MASTER.md`
- `AGENT_PROTOCOL.md`
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `curriculum/A1_1000_MAP.md`
- Existing 250-lesson A1 package
