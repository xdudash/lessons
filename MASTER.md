# SlovakGo 10K — Master

## Mission

Build a complete Slovak course from A1 through C2 with 10,000 purposeful lessons.

## Source of truth

The repository is the persistent course memory. Master curriculum, grammar, competencies, exercise mechanics, production rules, review rules, QA rules, worker protocol, and progress files are authoritative.

The existing 250 A1 lessons are the baseline for the established A1 sequence and lesson format. Application implementation problems are not curriculum constraints.

## CEFR architecture

- A1 — forms and fundamentals
- A2 — systems and controlled expansion
- B1 — connections and independent communication
- B2 — composition, complex syntax, register
- C1 — choice, precision, advanced discourse
- C2 — control, nuance, stylistic flexibility

## Production loop

1. Read master state and assigned slot range.
2. Check prerequisites and review dependencies.
3. Generate lessons in the established JSON format.
4. Self-check schema, answer validity, Slovak naturalness, pedagogy, and progression.
5. Submit for adversarial review.
6. Repair rejected lessons.
7. Update progress and handoff state.

## Quality hierarchy

1. Slovak correctness and naturalness
2. Pedagogical correctness
3. Prerequisite correctness
4. Exercise validity
5. Progression and review integrity
6. Localization quality
7. UI/schema compatibility

## No-filler rule

A lesson is valid only when it advances or consolidates a defined target: new knowledge, stabilization, contrast, transfer, fluency, accuracy, register, pragmatics, integrated skills, review, or assessment.

## A1 audit baseline — 250 lessons

Audit status: **PASS with targeted corrections required**.

### What the audit confirms

- Exactly 250 lesson files are present: 25 sections × 10 lessons.
- All lessons declare level A1 and follow the same established JSON envelope.
- No exact duplicate lesson was found when comparing the core lesson payload (title/topic/description/theory/words/exercises/final situation).
- No cross-section vocabulary overlap reached a high enough threshold to classify lessons as accidental vocabulary duplicates.
- The exercise-type distribution is broad and structurally consistent.

### Duplicate / overlap findings

1. **Exact lesson duplicates: none found.** Do not delete lessons merely because they repeat material; reinforcement is part of the design.
2. **Exact title collision: 1 case.** `a1-s02-l07` and `a1-s08-l06` are both titled `Kde bývaš?`. They teach different content (general place of residence vs. housing type/location), so this is not a content duplicate, but the title should be differentiated to avoid ambiguity. Proposed rename: `a1-s08-l06` → `Bývam v byte alebo dome?`.
3. **Repeated exercise prompt scaffolds: 93 collision groups were detected.** These are mostly reusable mechanics such as matching and standard fill-in prompts, so they are not evidence of duplicate lessons. Future generation must nevertheless avoid copying the same prompt wording when the communicative target is different; repetition should be intentional and tagged as review.
4. **Repeated vocabulary inside sections is mostly legitimate spiral reinforcement.** Do not optimize for minimum repetition. Optimize for controlled NEW → REVIEW → TRANSFER → MASTERY progression.

### Gaps / under-specified A1 areas

These are not reasons to discard the 250 lessons. They are requirements for the A1 master inventory and future A1 expansion:

- **Case system:** accusative, locative, genitive, dative and instrumental appear through useful phrases and contexts, but the 250 lessons do not yet form a clean, explicit A1 case inventory. Record which forms are taught as productive patterns versus memorized chunks; move systematic case paradigms to A2 where appropriate.
- **Plural formation:** plural forms occur, but noun/adjective plural formation is not organized as a single explicit progression. Add a controlled inventory and prerequisite links.
- **Imperative:** commands such as `čítajte`, `píšte`, `opakujte`, `zavolajte`, `pomôžte` occur as functional language, but the imperative is mostly chunk-based rather than explicitly mapped. Add a micro-progression for high-frequency imperative forms.
- **Reflexive verbs:** forms such as `učiť sa`, `objednať sa`, `stretnúť sa` occur, but reflexive structure is not yet tracked as a grammar dependency. Add it to the inventory without forcing a full paradigm into A1.
- **Verb paradigms:** many high-frequency verbs are introduced through useful first/second/third-person forms, but conjugation families are not yet represented as a formal inventory. Track productive patterns separately from lexicalized forms.
- **Aspect:** the 250 lessons do not establish a systematic perfective/imperfective aspect system. This is acceptable for the current A1 baseline; aspect must become an explicit A2/B1 dependency rather than being smuggled into A1 as advanced grammar.
- **Listening/speaking assessment:** the current A1 package is text-only. It contains reading, writing/message, dialogue and communicative simulations, but it does not actually assess acoustic listening or spoken production. Treat audio/speech as a future course-media layer, not as a reason to rewrite the lesson content.

### CEFR boundary findings

The 250 lessons are broadly compatible with A1 because they concentrate on personal information, immediate needs, concrete everyday situations, short routine exchanges, simple questions, memorized patterns and very basic connected language. This is consistent with the CEFR A1 global scale and spoken-language descriptors.

The following rule is now mandatory for future generation:

> A1 may introduce a form as a useful high-frequency chunk when the learner needs it for an immediate communicative task, but must not silently claim mastery of the whole grammatical system from that exposure.

Therefore:

- `v Bratislave`, `do mesta`, `s bratom`, etc. may appear as functional chunks at A1.
- Full case paradigms, broad verb government, systematic aspect contrasts, complex subordination and advanced stylistic choices must be scheduled through later CEFR dependencies unless there is a clear A1 communicative justification.
- A lesson may contain an A1-useful form whose complete grammatical system belongs later; lesson metadata must distinguish **functional exposure** from **productive mastery**.

The Council of Europe notes that CEFR global descriptors are language-independent and that language-specific Reference Level Descriptions are needed to specify concrete forms, grammar, vocabulary, functions and other content. Therefore this A1 audit is a curriculum-engineering baseline, not a claim that these 250 lessons alone constitute a complete Slovak A1 RLD.

### Required corrections before using A1 as the template for 10K generation

1. Rename the duplicate title `Kde bývaš?` in section 8.
2. Build an explicit A1 grammar inventory from the 250 lessons: **introduced form / productive target / review / deferred to A2+**.
3. Build a prerequisite graph for cases, plural, adjective agreement, imperative and reflexive verbs.
4. Mark lexicalized case forms versus productive case rules.
5. Mark aspect as deferred from A1 systematic mastery to A2/B1.
6. Add a prompt-variation rule so repeated exercise mechanics do not become textual duplication.
7. Preserve legitimate repetition; do not remove reinforcement simply because vocabulary overlaps.
8. Add an explicit media-layer flag: text-only A1 is the current baseline; future audio/speech modules must be added without changing the pedagogical core.
9. Add a CEFR-boundary check to QA: **functional exposure ≠ grammatical mastery**.
10. Before mass generation, run the same audit against every future level and compare the result with the master prerequisite graph.

## Current phase

Phase 0 — architecture and curriculum foundation.

A1 audit is complete. The next gate is to encode the A1 grammar/vocabulary/function inventories and prerequisite graph, then use them to refine the 10K curriculum before pilot generation.
