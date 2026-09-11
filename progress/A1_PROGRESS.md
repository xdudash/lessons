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

UNRESOLVED:
- Full A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Quality audit of L01–L10 against the gold-standard completeness requirement.
- Determination of the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Audit and remap **A1 Section 01 L01–L10** against the new gold standard. Do not generate new lessons yet. Establish what each existing lesson teaches, what it assumes, what it lacks, what is duplicated, and what must be revised. Then record the S01 L01–L10 findings and exact next action in a new audit/progress commit.

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
