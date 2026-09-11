# A1 S01 L11–L15 Pilot QA

STATUS: CONDITIONAL PASS

SCOPE:
- Pilot expansion lessons S01 L11–L15.
- Structural conformity against the authoritative A1 lesson envelope.
- Exercise answer validity and semantic consistency.
- Progression fit for S01 stabilization band.
- Canonical repository placement and resumability.

CHECKS:
- L11, L12, L13 source pilot content was reviewed and canonicalized into `lessons/a1/`.
- L11–L13 preserve the pilot pedagogical intent: time-of-day greetings, formal/informal greeting choice, and greeting vs goodbye.
- L11–L13 use the canonical top-level `lessons` envelope and canonical `finalSituation`/`resultScreen` structure.
- L14 and L15 were reviewed but remain structurally inconsistent with the authoritative baseline envelope: missing `intro`, `completionMessage`, `updatedAt`, localized `topic`, and canonical final-situation metadata; they therefore cannot be marked production-ready yet.
- L14 contains an orthography defect in the Russian theory text: `Dobre ráno` should be `Dobré ráno`.
- L15 `ex06` is semantically underdetermined in its original form because the correction invents an origin (`Som z Ukrajiny`) without context. It should instead contrast the question `Ako sa voláš?` with an incorrect origin answer and correct it using the already introduced name model.
- L14/L15 exercise types and answer keys are internally coherent at the item level, but envelope normalization is still required.
- UI rendering mismatches previously documented for `prompt`, `dialogue`, `context`, `situation`, and final-step enforcement are application issues and are not used as a reason to alter lesson content.

CANONICALIZED IN THIS QA STEP:
- `lessons/a1/a1-s01-l11.json`
- `lessons/a1/a1-s01-l12.json`
- `lessons/a1/a1-s01-l13.json`

SOURCE PILOT ARTIFACTS RETAINED FOR AUDIT/HISTORY:
- `pilot/a1-s01-l11.json`
- `pilot/a1-s01-l12.json`
- `pilot/a1-s01-l13.json`

BLOCKERS BEFORE FULL PASS:
1. Normalize L14 to the canonical A1 envelope.
2. Normalize L15 to the canonical A1 envelope.
3. Correct the L14 `Dobré ráno` orthography defect.
4. Rewrite L15 `ex06` so the correction is context-supported rather than introducing an arbitrary origin.
5. Re-run the five-lesson pilot QA after normalization.

NEXT TASK:
- Normalize and re-QA `a1-s01-l14.json` and `a1-s01-l15.json`, then update the progress handoff. Do not proceed to S01 L16–L20 until the five-lesson pilot receives FULL PASS.
