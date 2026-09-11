# A1 S01 L11–L15 Pilot QA

STATUS: FULL PASS

SCOPE:
- Pilot expansion lessons S01 L11–L15.
- Structural conformity against the established canonical A1 lesson envelope.
- Exercise answer validity and semantic consistency.
- Progression fit for the S01 stabilization band.
- Canonical repository placement and resumability.

FINAL CHECKS:
- L11–L13 are canonicalized under `lessons/a1/` and preserve the intended stabilization progression.
- L14 is normalized to the canonical envelope with localized topic, intro, completion message, updated timestamp, and canonical interactive final-situation metadata.
- L14 Russian theory orthography was corrected from `Dobre ráno` to `Dobré ráno`.
- L15 is normalized to the canonical envelope with localized topic, intro, completion message, updated timestamp, and canonical interactive final-situation metadata.
- L15 `ex06` was corrected so the task is context-supported: `Ako sa voláš? — Som z Ukrajiny.` → `Ako sa voláš? — Volám sa Martin.` This tests the already introduced name-answer model rather than inventing an arbitrary origin.
- L11–L15 have unique lesson IDs/orders and coherent section membership `a1-s01`.
- Exercise IDs are unique within each lesson; answer keys are internally consistent with the prompts/scenarios.
- Final situations use `3/3` pass requirements with three answerable steps.
- No application/UI mismatch was used as a reason to distort lesson content; previously documented rendering issues remain application work.

PEDAGOGICAL CHECK:
- L11–L15 remain within the S01 stabilization role: greetings, time-of-day greetings, greeting/goodbye distinction, and first-meeting question models.
- No new advanced grammar system is introduced.
- Vocabulary remains review/stabilization-oriented rather than pretending that repeated exposure alone proves mastery.

FILES IN PILOT:
- `lessons/a1/a1-s01-l11.json`
- `lessons/a1/a1-s01-l12.json`
- `lessons/a1/a1-s01-l13.json`
- `lessons/a1/a1-s01-l14.json`
- `lessons/a1/a1-s01-l15.json`

SOURCE PILOT ARTIFACTS RETAINED FOR AUDIT/HISTORY:
- `pilot/a1-s01-l11.json`
- `pilot/a1-s01-l12.json`
- `pilot/a1-s01-l13.json`

RESULT:
- Five-lesson S01 pilot is FULL PASS and may advance to the next bounded generation stage.

NEXT TASK:
- Proceed to S01 L16–L20 (CONTRAST band) only after selecting exact targets against the durable A1 vocabulary ownership data and prerequisite graph. Generate boundedly, then run the same QA gates before committing.
