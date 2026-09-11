# SlovakGo A1 Progress

STATUS: IN_PROGRESS

COMPLETED:
- Audited the 250-lesson A1 baseline.
- Encoded the source-derived A1 grammar, vocabulary and communicative-function inventory.
- Encoded the A1 prerequisite graph and A1→A2 handoff dependencies.
- Preserved the distinction between functional exposure and productive mastery.
- Built the complete A1 1,000-slot curriculum map: 25 sections × 40 slots, preserving the existing 250 baseline and defining 750 expansion slots.
- Derived a local item-level vocabulary ownership/review analysis from the authoritative 250-lesson package: 1,500 entries, 1,272 unique expressions, 187 repeated expressions and 1,085 single-occurrence expressions.
- Applied the planning stage model NEW → REVIEW → TRANSFER → MASTERY to observed baseline occurrences without treating frequency alone as proof of mastery.

FILES CHANGED:
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `curriculum/A1_1000_MAP.md`
- `progress/A1_PROGRESS.md`

KEY FINDINGS:
- Baseline: 250 lessons, 25 sections, 1,500 vocabulary entries, 1,272 unique expressions, 4,256 exercises.
- 187 expressions already recur in the baseline; these occurrences can be classified for review/transfer planning.
- 1,085 expressions occur only once in the baseline and therefore need deliberate future review before being treated as mastered.
- First occurrence is the initial ownership point; later occurrences are classified as REVIEW, TRANSFER or MASTERY for planning purposes.
- This classification is heuristic curriculum metadata and must be overridden when pedagogical context shows that an occurrence is not genuine review, transfer or mastery.
- The full item-level matrix was successfully derived from the uploaded 250-lesson source package locally, but the complete source package is not currently stored in GitHub. Therefore the repository currently stores the matrix policy and coverage findings, not a fabricated partial JSON pretending to be the complete matrix.
- The 750 expansion slots must not receive concrete vocabulary targets until the baseline source is durably available to the next agent or the targets are independently encoded in GitHub.

UNRESOLVED:
- Durable GitHub storage of the complete 250-lesson source package or an equivalent complete item-level vocabulary matrix.
- Concrete target assignment for each of the 750 A1 expansion slots after durable corpus-level overlap checking.
- Full external Slovak CEFR/RLD verification of the inventory.
- The broader 10K curriculum files still need to be present in the repository before they can be treated as the durable 10K source of truth.
- Publishing correction: rename `a1-s08-l06` from `Kde bývaš?` to `Bývam v byte alebo dome?`.

NEXT TASK:
- Make the vocabulary matrix fully resumable from GitHub: encode the complete item-level ownership/review data (or durably add the authoritative 250-lesson source), then use it to assign concrete targets to all 750 A1 expansion slots. Only after that should a small reviewed pilot batch be generated.

DEPENDENCIES:
- `MASTER.md`
- `AGENT_PROTOCOL.md`
- `knowledge/A1_INVENTORY.md`
- `knowledge/A1_PREREQUISITE_GRAPH.md`
- `knowledge/A1_VOCAB_OWNERSHIP.md`
- `curriculum/A1_1000_MAP.md`
- Existing 250-lesson A1 package
