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
- Started the S01 expansion pilot and reviewed L11–L15 as one stabilization block.
- Canonicalized L11–L13 into `lessons/a1/` using the established lesson envelope while retaining their original pilot artifacts for audit history.
- Recorded the five-lesson pilot QA as CONDITIONAL PASS in `audits/A1_S01_L11_L15_PILOT_QA.md`.

FILES CHANGED:
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `knowledge/a1_vocab_matrix/A1_COMPLETE.json.gz.b64`
- `knowledge/a1_vocab_matrix/README.md`
- `curriculum/A1_1000_MAP.md`
- `progress/A1_1000_TARGET_REGISTRY.md`
- `lessons/a1/a1-s01-l11.json`
- `lessons/a1/a1-s01-l12.json`
- `lessons/a1/a1-s01-l13.json`
- `lessons/a1/a1-s01-l14.json`
- `lessons/a1/a1-s01-l15.json`
- `audits/A1_S01_L11_L15_PILOT_QA.md`
- `progress/A1_PROGRESS.md`

KEY FINDINGS:
- Baseline: 250 lessons, 25 sections, 1,500 vocabulary entries, 1,272 unique expressions, 4,256 exercises.
- 187 expressions already recur in the baseline; these occurrences can be classified for review/transfer planning.
- 1,085 expressions occur only once in the baseline and therefore need deliberate future review before being treated as mastered.
- First occurrence is the initial ownership point; later occurrences are classified as REVIEW, TRANSFER or MASTERY for planning purposes.
- This classification is heuristic curriculum metadata and must be overridden when pedagogical context shows that an occurrence is not genuine review, transfer or mastery.
- The complete matrix is now resumable from GitHub without requiring the original uploaded ZIP or chat history. The compressed artifact's uncompressed payload has SHA-256 `283c8ae1586d5dd9218fe13b02a302b8a39575c572ea5d4fd14e93f648b7aa0c`.
- The target registry now covers all 750 expansion slots at the pedagogical-band level.
- S01 L11–L13 are now in canonical lesson storage. L14–L15 exist in canonical storage but still require envelope normalization before the pilot can receive FULL PASS.
- L14 has an orthography defect in theory text (`Dobre ráno` → `Dobré ráno`).
- L15 `ex06` needs a context-supported correction rather than an arbitrary origin assertion.

UNRESOLVED:
- Normalize and re-QA S01 L14–L15.
- Exact item-level vocabulary selection for each remaining expansion lesson.
- Full external Slovak CEFR/RLD verification of the inventory.
- The broader 10K curriculum files still need to be present in the repository before they can be treated as the durable 10K source of truth.
- Publishing correction: rename `a1-s08-l06` from `Kde bývaš?` to `Bývam v byte alebo dome?`.

NEXT TASK:
- Normalize `a1-s01-l14.json` and `a1-s01-l15.json` to the authoritative A1 envelope, fix the two identified content defects, then re-run the full S01 L11–L15 pilot QA. Do not start S01 L16–L20 until the pilot receives FULL PASS.

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
- Existing 250-lesson A1 package
