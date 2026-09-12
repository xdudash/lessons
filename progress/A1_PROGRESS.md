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
- Audited A1 Section 01 L01–L10 against the gold standard and rebuilt the block into a coherent progression.
- Audited the existing S02 L01–L10 baseline under Architecture v2; old versions were not accepted automatically because several repeated prior theory instead of progressing the dependency chain.
- Rebuilt S02 L01 as the new S02 entry lesson: 2 theory screens, 6 target expressions, 20 exercises, 14 exercise types, reading with 2 questions, contextual meaning work, dialogues, real-life production, 3-step final scenario and result screen. QA FULL PASS.
- Rebuilt S02 L02 as the group/plural identity lesson: 2 theory screens, 6 target expressions, 20 exercises, 3 final-situation steps and result screen. QA FULL PASS.
- Rebuilt S02 L03 around origin vs residence: 2 theory screens, 6 target expressions, 20 exercises, reading, dialogues, contextual meaning, real-message production, and a 3-step final scenario. QA FULL PASS in `audits/A1_S02_L03_QA.md`.

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
- L07: REBUILT + QA FULL PASS — vowel-length discrimination expanded to gold-standard depth.
- L08: REBUILT + QA FULL PASS — classroom instructions, comprehension repair and polite repetition requests.
- L09: REBUILT + QA FULL PASS — integrated first-meeting scenario.
- L10: REBUILT + QA FULL PASS — section mastery/check.

S02 REBUILD STATUS:
- L01: REBUILT + QA FULL PASS — `ja som / ty si / on/ona je`; pronoun→form decision; controlled practice → contextual comprehension → dialogue → production.
- L02: REBUILT + QA FULL PASS — group identity with `my / sme`, `Kto sme?`, group roles and productive transfer.
- L03: REBUILT + QA FULL PASS — origin vs residence; `Odkiaľ?` / `Som z...` vs `Kde bývam?` / `Bývam v...`; meaningful transfer.
- L04–L10: AUDITED, not yet rebuilt.

UNRESOLVED:
- Complete A1 remapping of every existing section's L01–L10 against grammar, vocabulary, communicative functions, prerequisites and mastery outcomes.
- Determine the true number of A1 lessons required after remapping and mastery analysis.
- Review/revision plan for S01 L11–L40 under Architecture v2.
- The title correction `a1-s08-l06` → `Bývam v byte alebo dome?` remains to be applied if not already done in the source package.
- Full external Slovak CEFR/RLD verification remains pending.

NEXT TASK:
- Rebuild **S02 L04** under Architecture v2. Extend origin/residence into a distinct communicative function rather than repeating the previous lesson.

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
