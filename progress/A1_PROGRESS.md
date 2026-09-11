# SlovakGo A1 Progress

STATUS: IN_PROGRESS

COMPLETED:
- Audited the 250-lesson A1 baseline.
- Encoded the source-derived A1 grammar, vocabulary and communicative-function inventory.
- Encoded the A1 prerequisite graph and A1→A2 handoff dependencies.
- Preserved the distinction between functional exposure and productive mastery.
- Built the complete A1 1,000-slot curriculum map: 25 sections × 40 slots, preserving the existing 250 baseline and defining 750 expansion slots.
- Derived the complete item-level vocabulary ownership/review analysis from the authoritative 250-lesson package: 1,500 entries, 1,272 unique expressions, 187 repeated expressions and 1,085 single-occurrence expressions.
- Applied the planning stage model NEW → REVIEW → TRANSFER → MASTERY to observed baseline occurrences without treating frequency alone as proof of mastery.
- Stored the complete item-level matrix durably in GitHub as a gzip+base64 JSON artifact at `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`, with decoding instructions and an integrity hash in `knowledge/a1_vocab_matrix/README.md`.
- Added `progress/A1_1000_TARGET_REGISTRY.md`, assigning a concrete pedagogical target band to all 750 expansion slots while deliberately deferring exact item selection until pilot QA.
- Completed and QA-approved the bounded S01 expansion pilot L11–L15. The five-lesson pilot is FULL PASS.
- Completed and QA-approved S01 L16–L20. The five-lesson CONTRAST block is FULL PASS.
- Completed and QA-approved S01 L21–L25. The five-lesson TRANSFER block is FULL PASS.
- L14–L15 were normalized to the canonical A1 envelope and corrected during final QA.
- L18 was corrected during final QA: title `Kto ste?` was changed to `Odkiaľ ste?` so the title matches the actual lesson target/content.

COMPLETED S01 EXPANSION:
- L11–L15: STAB — FULL PASS
- L16–L20: CON — FULL PASS
- L21–L25: TRN — FULL PASS

KEY FINDINGS:
- Baseline: 250 lessons, 25 sections, 1,500 vocabulary entries, 1,272 unique expressions, 4,256 exercises.
- 187 expressions already recur in the baseline; these occurrences can be classified for review/transfer planning.
- 1,085 expressions occur only once in the baseline and therefore need deliberate future review before being treated as mastered.
- First occurrence is the initial ownership point; later occurrences are classified as REVIEW, TRANSFER or MASTERY for planning purposes.
- This classification is heuristic curriculum metadata and must be overridden when pedagogical context shows that an occurrence is not genuine review, transfer or mastery.
- The complete matrix is resumable from GitHub without requiring the original uploaded ZIP or chat history. The compressed artifact's uncompressed payload has SHA-256 `283c8ae1586d5dd9218fe13b02a302b8a39575c572ea5d4fd14e93f648b7aa0c`.
- The target registry covers all 750 A1 expansion slots at the pedagogical-band level.
- The S01 L11–L15 pilot demonstrates the bounded generation + QA workflow and is FULL PASS.
- The S01 L16–L20 CONTRAST block demonstrates deliberate contrast work around ty/vy, informal/formal politeness and first-contact situations and is FULL PASS.
- The S01 L21–L25 TRANSFER block demonstrates transfer of established first-contact patterns into varied contexts without introducing a new grammar system and is FULL PASS.

UNRESOLVED:
- Exact item-level vocabulary selection for each remaining expansion lesson.
- Full external Slovak CEFR/RLD verification of the inventory.
- The broader 10K curriculum files still need to be present in the repository before they can be treated as the durable 10K source of truth.
- Publishing correction: rename `a1-s08-l06` from `Kde bývaš?` to `Bývam v byte alebo dome?`.
- Known application rendering/enforcement issues remain application-side and are intentionally not being solved by distorting lesson content.

NEXT TASK:
- Generate the next bounded pilot block S01 L26–L30 (EXPANSION band). Before generation, select exact targets against `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`, `knowledge/A1_VOCAB_OWNERSHIP.md`, and `knowledge/A1_PREREQUISITE_GRAPH.md`; then generate the five lessons, run structural/answer-validity/duplication/CEFR-progression/naturalness QA, and commit only after review.

DEPENDENCIES:
- `MASTER.md`
- `AGENT_PROTOCOL.md`
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`
- `knowledge/a1_vocab_matrix/README.md`
- `curriculum/A1_1000_MAP.md`
- `progress/A1_1000_TARGET_REGISTRY.md`
- `audits/A1_S01_L11_L15_PILOT_QA.md`
- `audits/A1_S01_L16_L20_QA.md`
- `audits/A1_S01_L21_L25_QA.md`
- Existing 250-lesson A1 package
