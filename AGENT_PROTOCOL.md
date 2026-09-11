# SlovakGo — Agent Continuation Protocol

## Purpose

This repository is the persistent memory of the SlovakGo A1–C2, 10,000-lesson project.

A new AI agent MUST be able to continue the project without relying on the previous agent's chat history.

## Rule 1 — GitHub is the source of truth

Before doing any work, inspect the repository state. Do not assume what another agent completed.

Read, in this order when present:

1. `README.md`
2. `MASTER.md`
3. `MASTER_CURRICULUM_10K.md`
4. relevant `curriculum/*`
5. relevant `knowledge/*`
6. `production/*`
7. `progress/*`
8. relevant `audits/*`

If these files disagree, the newest explicit project decision in Git history/master state wins; do not silently overwrite it.

## Rule 2 — Find the exact stopping point

The current state is defined by committed files, not by chat memory.

Before starting:

- inspect recent commits;
- inspect `progress/`;
- identify the last completed phase/task;
- identify incomplete or blocked tasks;
- check for files marked `IN_PROGRESS`, `BLOCKED`, `TODO`, `NEXT`, or similar;
- inspect the relevant audit/report before changing content.

Never restart a completed phase merely because the current chat does not contain its details.

## Rule 3 — One agent = one explicit work unit

Every agent must work on a bounded task.

Before editing, record mentally or in the relevant progress file:

- task;
- input files;
- output files;
- acceptance criteria;
- dependencies;
- next task after completion.

Do not modify unrelated areas “while you are here”.

## Rule 4 — Continue, do not duplicate

Before generating anything:

- search for existing lessons/content covering the same target;
- check the slot registry;
- check progress files;
- check review dependencies;
- check whether another lesson already owns the target.

If content already exists, improve, review, or reference it instead of creating a second copy.

Legitimate repetition is allowed when it serves NEW → REVIEW → TRANSFER → MASTERY.

## Rule 5 — Protect the lesson format

The established/new lesson JSON format is authoritative.

Never simplify lesson content to accommodate application/UI bugs.

If the application cannot render a valid field, record the compatibility issue separately. Do not corrupt the pedagogical source to work around it.

## Rule 6 — CEFR discipline

Every lesson must have:

- a clear CEFR level;
- a defined communicative or linguistic target;
- prerequisites;
- a reason for appearing at this point in the course;
- appropriate productive expectations.

Important distinction:

**functional exposure is not grammatical mastery.**

An A1 learner may encounter a useful phrase containing a later-system form, but the lesson must not pretend the learner has mastered the complete later grammar system.

## Rule 7 — No filler

Do not create lessons merely to reach 10,000.

A lesson must advance at least one meaningful dimension:

- NEW knowledge;
- stabilization;
- contrast;
- transfer;
- fluency;
- accuracy;
- register;
- pragmatics;
- integrated skills;
- review;
- assessment.

## Rule 8 — Review before generation

Generated content must be reviewed for:

1. Slovak correctness and naturalness;
2. pedagogy;
3. CEFR fit;
4. prerequisites;
5. exercise validity;
6. localization;
7. duplication/overlap;
8. review progression;
9. schema validity.

Do not treat a generated lesson as final merely because it parses as JSON.

## Rule 9 — Atomic GitHub commits

Commit completed logical units with clear messages.

Examples:

- `Audit A1 250 lessons`
- `Add A1 grammar inventory`
- `Add A1 prerequisite graph`
- `Generate A1 pilot lessons 251-270`
- `Review A1 pilot lessons 251-270`
- `Repair A1 pilot lessons 251-270`
- `Update course progress`

Do not claim completion until the relevant changes are actually committed.

## Rule 10 — Always leave a handoff

At the end of a work unit, update the relevant progress/handoff file with:

- `STATUS`: COMPLETE / IN_PROGRESS / BLOCKED
- what was completed;
- files changed;
- important findings;
- unresolved issues;
- exact next recommended task;
- dependencies for the next agent.

A future agent should be able to continue from the repository alone.

## Rule 11 — Never erase evidence

Audits and reports are historical project evidence.

Do not rewrite an old audit to make it look cleaner. If a finding changes, add a dated/versioned correction or update the master state while preserving the original audit where practical.

## Rule 12 — If blocked

Do not invent missing information.

Record:

- what is missing;
- why it matters;
- what can still be done safely;
- the exact unblock action.

Continue with independent work that does not depend on the blocker when possible.

## Standard handoff format

Use this structure in progress files:

```text
STATUS: COMPLETE

COMPLETED:
- ...

FILES CHANGED:
- ...

KEY FINDINGS:
- ...

UNRESOLVED:
- ...

NEXT TASK:
- ...

DEPENDENCIES:
- ...
```

## Agent startup checklist

Before work:

- [ ] Read `MASTER.md`
- [ ] Read the relevant curriculum/knowledge/production files
- [ ] Read progress and audit state
- [ ] Inspect recent Git commits
- [ ] Identify exact next task
- [ ] Check for existing work to avoid duplication

Before finishing:

- [ ] Validate changed content
- [ ] Run/perform applicable QA
- [ ] Update progress/handoff
- [ ] Commit changes
- [ ] State the exact next task

## Core principle

**The project must be resumable by a completely different agent tomorrow with zero access to today's conversation.**

If an important decision exists only in chat and not in the repository, it is not yet part of the durable project state.
