# AGENTS.md — Mandatory lesson-production workflow

## Purpose
This file is the durable operating contract for every agent working in this repository. Read it before editing or creating lessons. Repository truth beats assumptions, shortcuts, or a previous agent's chat claims.

## 1. Source of truth and instruction precedence
- GitHub `main` is the authoritative durable state.
- Read and follow `README.md`, `MASTER.md`, `AGENT_PROTOCOL.md`, `curriculum/COURSE_ARCHITECTURE_V2.md`, `curriculum/GOLD_STANDARD_LESSON.md`, relevant `knowledge/*`, `progress/*`, `audits/*`, and the actual lesson files.
- When the user supplies a known-working importer example, inspect the actual file and use its real field structure. Do not invent a new JSON schema from memory.
- The current working repository and its importer-compatible examples take precedence over an agent's assumptions.

## 2. CRITICAL: FORMAT IS NOT NUMBERING
A user-provided working example such as `lesson-181-a1_slovakgo.json` is an **example of importer-compatible FORMAT**.

It is NOT a template for lesson numbering, lesson IDs, section IDs, or file names.

The section determines numbering. Example:
- Section 01 ends at `a1-s01-l06`.
- Section 02 therefore uses `a1-s02-l07`, `a1-s02-l08`, `a1-s02-l09`, etc.

Never copy `181` into a new section merely because `lesson-181-a1_slovakgo.json` was used as the format reference.

For every new lesson, independently determine:
- section ID;
- next lesson number;
- lesson ID;
- file name;
- `order`;
- previous/next lesson links.

All of these must match the actual repository sequence.

## 3. LANGUAGE: SLOVAK, NOT SLOVENIAN
- Target language being learned/tested: **Slovak — slovenčina**.
- **Do not use Slovenian — slovenščina.**
- Student-facing instructions, prompts, explanations, hints, feedback and learning UI text: **Ukrainian** unless a repository instruction explicitly says otherwise.
- Slovak examples, answers, target phrases and vocabulary must be actual Slovak.
- Do not accidentally translate Slovak forms into Slovenian or use Slovenian grammar/vocabulary.
- Be especially careful with strings that look superficially similar across Slovak and Slovenian.

## 4. PEDAGOGICAL ARCHITECTURE
Lesson count is determined by pedagogical need, not an arbitrary quota.
- Prefer fewer, denser lessons when targets can be combined without sacrificing mastery.
- Do not create filler lessons to reach a number.
- Do not make a lesson artificially short just to save time.
- Increase vocabulary when needed to make the lesson communicatively useful and sufficiently rich.
- More vocabulary is good when it is purposeful, teachable, reused and connected to the lesson target.
- Never inflate vocabulary counts with irrelevant or decorative words.
- New vocabulary should appear in theory/examples and be reused in exercises and context whenever practical.
- Progression should support: introduce → stabilize → contrast → transfer → integrate → mastery.
- A lesson is not merely a list of words or a repetitive quiz. It needs a coherent learning arc and evidence of learning.

## 5. THE REAL IMPORTER JSON CONTRACT
When a working lesson JSON is available, use its actual structure as the importer contract.

### Canonical envelope
```json
{
  "lessons": [
    {
      "id": "a1-sXX-lYY",
      "sectionId": "a1_sXX",
      "level": "A1",
      "title": "Slovak lesson title",
      "topic": "Українська тема",
      "description": "Український опис",
      "order": 7,
      "xpReward": 25,
      "estimatedMinutes": 25,
      "isPublished": false,
      "intro": "Український вступ",
      "completionMessage": "Українське повідомлення про завершення",
      "updatedAt": "2026-09-12T12:00:00.000Z",

      "startScreen": {
        "screenType": "lesson_start",
        "title": "Kto som?",
        "shortDescription": "Український короткий опис",
        "outcomes": [
          "Український результат 1",
          "Український результат 2",
          "Український результат 3"
        ],
        "newWords": ["ja", "som", "kto"],
        "exercisesCount": 12,
        "reward": "25 XP",
        "button": "Почати урок"
      },

      "theoryScreens": [
        {
          "screenType": "theory",
          "order": 1,
          "title": "Український заголовок",
          "text": "Українське пояснення правила.",
          "examples": [
            {"sk": "Ja som Nina.", "uk": "Я Ніна."}
          ],
          "exampleSk": "Ja som Nina.",
          "exampleUk": "Я Ніна.",
          "shortRule": "Українське коротке правило",
          "button": "Далі"
        }
      ],

      "wordsScreen": {
        "screenType": "lesson_words",
        "title": "Слова й моделі уроку",
        "description": "Український опис роботи зі словами",
        "items": [
          {
            "wordId": "a1-sXX-lYY-w01",
            "sk": "ja",
            "uk": "я",
            "pronunciationUk": "я",
            "exampleSk": "Ja som Nina.",
            "exampleUk": "Я Ніна."
          }
        ],
        "button": "Почати вправи"
      },

      "words": [
        {
          "id": "a1-sXX-lYY-w01",
          "sk": "ja",
          "uk": "я",
          "pronunciationUk": "я",
          "exampleSk": "Ja som Nina.",
          "exampleUk": "Я Ніна.",
          "level": "A1",
          "topic": "Українська назва теми",
          "tags": ["A1", "займенники"]
        }
      ],

      "exercises": [
        {
          "id": "a1-sXX-lYY-e01",
          "lessonId": "a1-sXX-lYY",
          "type": "multiple_choice_translation",
          "question": "Українське питання",
          "options": ["ja", "ty", "on", "ona"],
          "correctAnswer": "ja",
          "explanation": "Українське пояснення",
          "wordIds": ["a1-sXX-lYY-w01"],
          "order": 1,
          "difficulty": "easy",
          "button": "Далі"
        }
      ],

      "finalSituation": {
        "screenType": "final_life_situation",
        "title": "Український заголовок",
        "scenario": "Український реальний контекст",
        "question": "Українське завдання",
        "options": [
          "Slovak option 1",
          "Slovak option 2"
        ],
        "correctAnswer": "1",
        "translation": "Український переклад/пояснення",
        "explanation": "Українське пояснення",
        "button": "Перевірити"
      },

      "resultScreen": {
        "screenType": "lesson_result",
        "title": "Урок завершено",
        "text": "Український текст",
        "nowYouKnow": ["ja — я", "som — я є"],
        "result": "+25 XP",
        "newWordsCount": 16,
        "exercisesCompleted": 12,
        "mistakesMessage": "Матеріал із помилками додано до повторення.",
        "buttons": [
          "Продовжити",
          "Повторити урок",
          "Тренувати помилки"
        ],
        "nextLesson": "Next lesson title or null when unknown"
      }
    }
  ]
}
```

### Important structural rules
- The top-level object must have `"lessons": [...]`.
- Lesson-level scalar fields must remain scalar when the working importer example uses scalars.
- Do **not** replace scalar fields with invented localization objects such as `{ "sk": ..., "uk": ..., "ru": ..., "en": ... }` unless the actual importer contract explicitly requires them.
- `startScreen`, `theoryScreens`, `wordsScreen`, `words`, `exercises`, `finalSituation`, and `resultScreen` belong to the lesson contract when present in the working example.
- Preserve the actual working field names and value types.
- Do not add made-up fields just because they seem useful.
- Do not remove pedagogically or technically required fields to simplify the JSON.
- A syntactically valid JSON file can still be importer-invalid. Syntax is necessary, not sufficient.

## 6. THEORY SCREEN RULES
Theory exists to teach what the exercises later require.
Each theory screen should contain the real fields supported by the working contract, typically:
- `screenType: "theory"`;
- `order`;
- Ukrainian `title`;
- Ukrainian `text`;
- `examples` with actual Slovak `sk` and Ukrainian `uk`;
- `exampleSk`;
- `exampleUk`;
- Ukrainian `shortRule`;
- `button`.

Do not teach a form that is never practiced. Do not test a form the theory did not support.

The number of theory screens is not a blind quota. Current accepted Section 02 lessons are denser and may use four theory screens even though older quality notes mention two as a minimum/reference.

## 7. WORDS / VOCABULARY RULES
Vocabulary is a working teaching set, not a cosmetic count.

For each `words` item:
- `id` must be unique within the lesson and referenced consistently.
- `sk` is Slovak.
- `uk` is Ukrainian meaning.
- `pronunciationUk` is a Ukrainian-friendly pronunciation aid when the project uses it.
- `exampleSk` must be actual Slovak and natural.
- `exampleUk` must accurately translate the Slovak.
- `level`, `topic`, and `tags` must be coherent.

`wordsScreen.items[*].wordId` must reference an existing `words[*].id`.

Prefer approximately 12–20+ meaningful lexical items in a substantial lesson when that density is useful. This is a design guideline, not a quota.

Word count may be higher when the communication target benefits from it. More words are preferred to a thin lesson when they remain purposeful and are actually practiced.

Avoid duplicates such as teaching the same item twice under slightly different labels unless there is a clear pedagogical reason (for example, a useful fixed expression vs an independently useful word).

## 8. EXERCISE CONTRACT
Use only exercise types and field structures that are evidenced by a real working lesson. Do not invent an exercise schema.

Common working types include:

### `multiple_choice_translation`
Typical fields:
```json
{
  "id": "a1-sXX-lYY-e01",
  "lessonId": "a1-sXX-lYY",
  "type": "multiple_choice_translation",
  "question": "Українське питання",
  "options": ["Slovak 1", "Slovak 2", "Slovak 3"],
  "correctAnswer": "Slovak 1",
  "explanation": "Українське пояснення",
  "wordIds": ["a1-sXX-lYY-w01"],
  "order": 1,
  "difficulty": "easy",
  "button": "Далі"
}
```

### `match_pairs`
Typical working pattern:
- `options` is a flat array alternating source and meaning strings;
- `correctAnswer` is an array such as `["ja|я", "profesia|професія"]`.

### `fill_blank`
Typical working fields:
- `question`;
- `options`;
- `correctAnswer`;
- `explanation`;
- `wordIds`;
- optional `fullSentence`.

### `dropdown_blank`
Typical working fields:
- `sentenceParts` containing text segments and a blank object such as:
```json
{"blankId":"b1","options":["si","som","je"],"correct":"si"}
```

### `sentence_builder`
Typical working fields:
- `tokens`;
- `correctSentence`.

### `sentence_order`
Typical working fields:
- `tokens`;
- `correctOrder`.

### `dialogue_choose_reply`
Typical working fields:
- `dialogue` array containing speaker and Slovak utterance;
- options with IDs, Slovak text and `correct` boolean.

### `correct_error`
Typical working fields:
- `sentence`;
- `acceptedAnswers`.

### `reading_comprehension`
Typical working fields:
- `text`;
- `questions`, whose options carry the correct answer according to the real working format.

### `meaning_in_context`
Typical working fields:
- `context`;
- `target`;
- options with IDs, Ukrainian `text`, and `correct` boolean.

### `natural_phrase`
Typical working fields:
- `situation`;
- options with IDs, Slovak `sk`, and `correct` boolean.

### `multiple_select`
Typical working fields:
- options with IDs, Slovak `sk`, and `correct` boolean;
- more than one option may be correct.

Never assume a type is valid merely because its name sounds reasonable. Inspect a working example first.

## 9. EXERCISE QUALITY
Exercises must test the lesson target, not merely repeat the same sentence.
A strong lesson should vary recognition, controlled use, contextual meaning, sentence construction, dialogue/reading and transfer when appropriate.

For every exercise check:
- the prompt is solvable from the supplied data;
- exactly the intended answer is correct unless the type explicitly supports multiple answers;
- `correctAnswer` matches `options` where the type requires it;
- every referenced `wordIds` exists;
- sentence-builder answers use exactly the supplied tokens;
- sentence-order answers use exactly the supplied tokens and correct order;
- accepted answers actually solve the sentence;
- distractors are plausible but wrong for a reason taught by the lesson;
- explanations are correct and in Ukrainian;
- no exercise tests knowledge that was never introduced.

Avoid repetitive blocks of the same exercise type unless repetition itself is pedagogically justified.

## 10. FINAL SITUATION / TRANSFER
The final situation is not another trivial multiple-choice translation.
It should demonstrate that the learner can use the lesson target in a realistic context.

Typical structure when the working contract uses it:
- `screenType: "final_life_situation"`;
- Ukrainian `title`;
- Ukrainian `scenario`;
- Ukrainian `question`;
- Slovak answer options;
- `correctAnswer` matching the actual option numbering convention;
- Ukrainian `translation` and `explanation`;
- `button`.

The final task should test transfer to a new or more integrated context, not simply repeat an earlier exercise word-for-word.

## 11. RESULT SCREEN
Keep the result structure compatible with the working importer.
`nextLesson` must point to a real next lesson when known. Use `null` when the next lesson is not yet defined rather than inventing a destination.

## 12. LESSON NUMBERING AND REFERENCES
For every lesson, these must agree:
- file name;
- `id`;
- section ID;
- `order`;
- exercise `lessonId` values;
- word IDs;
- `wordsScreen.items[*].wordId`;
- `finalSituation`/result identifiers when used;
- `nextLesson`.

Before generating a new file, inspect the repository to determine the actual next number. Never infer it from a sample file number.

## 13. REQUIRED PRODUCTION WORKFLOW
### A. Read first
Before changing anything:
1. Read repository instructions.
2. Read `README.md`, `MASTER.md`, `AGENT_PROTOCOL.md`.
3. Read relevant curriculum/knowledge/progress/audit files.
4. Inspect current `main` tree and recent commits.
5. Inspect the relevant existing section.
6. Inspect a known-working importer-compatible lesson example.
7. Determine exact section numbering.

### B. Design before generation
Define:
- CEFR outcomes;
- grammar/function targets;
- vocabulary/function set;
- prerequisites;
- ownership of new vocabulary;
- review/transfer needs;
- purpose of each lesson;
- mastery evidence;
- pedagogically justified lesson count.

### C. Build
Construct JSON from the real importer contract, not from memory or a generic lesson template.

### D. Pre-GitHub validation
Every file must pass all applicable checks before being written to GitHub:
- valid JSON syntax;
- complete file, not truncated;
- exactly the required top-level envelope;
- no duplicate keys;
- no accidental extra nesting;
- no Python list/dict serialization;
- braces/brackets/quotes correct;
- required fields present;
- correct field types;
- lesson ID and filename agree;
- section numbering correct;
- all internal references resolve;
- `wordIds` resolve;
- `correctAnswer` values are coherent with the exercise type;
- no malformed Unicode;
- no accidental Slovenian;
- learner-facing instructions in Ukrainian.

### E. Semantic QA
Check:
- Slovak grammar and naturalness;
- morphology and agreement;
- meaning;
- CEFR appropriateness;
- prerequisites;
- exercise logic;
- accepted answers;
- distractors;
- dialogues;
- reading/context;
- final transfer situation;
- localization completeness.

### F. Adversarial QA
Try to break each lesson:
- Can each exercise be solved from its own data?
- Does every marked answer actually answer the prompt?
- Are all `correct` flags correct?
- Does every `correctOrder` use exactly the supplied tokens?
- Are accepted answers valid?
- Is any Ukrainian field accidentally a serialized object/array?
- Is any Slovak sentence unnatural?
- Is the theory sufficient for the exercises?
- Is the lesson merely repetitive?
- Does the final situation prove transfer/mastery?

### G. Batch/section QA
Check the section as a whole:
- full target coverage;
- sensible progression;
- vocabulary ownership;
- meaningful repetition;
- no unnecessary overlap;
- no prerequisite violations;
- no redundant lessons;
- strong mastery evidence.

### H. Replace, do not duplicate
When rebuilding a section:
- replace obsolete section files;
- remove temporary/mistaken duplicate files;
- never leave two competing versions of the same lesson/section in `main`.

### I. GitHub verification
After writing files:
1. Read them back from `main`.
2. Verify the actual stored content, not only the outgoing payload.
3. Verify the section directory/tree contains exactly the intended sequence.
4. Verify old mistaken files are gone.
5. Verify recent commit(s) and branch state.
6. Update progress documentation only after durable state is correct.

## 14. IMPORT QA HONESTY
Do not say "passes import" unless the actual importer was run successfully.
These are different claims:
- JSON parses;
- structure matches the known working contract;
- semantic QA passed;
- the application importer accepted it.

Report only the checks actually completed.

If the importer cannot be run from the available environment, state that limitation explicitly.

## 15. CURRENT SECTION 02 REFERENCE
Section 02 is currently five denser lessons:
1. `a1-s02-l07` — Kto som?
2. `a1-s02-l08` — Ja, ty, on, ona, ono
3. `a1-s02-l09` — Zoznámime sa
4. `a1-s02-l10` — O mne
5. `a1-s02-l11` — Predstavím sa

These are the current accepted Section 02 lesson numbers. Their format follows the user's working importer example, while their numbering remains the Section 02 sequence.

## 16. GOLD STANDARD VS IMPORT CONTRACT
`curriculum/GOLD_STANDARD_LESSON.md` defines lesson-quality expectations: completeness, density, learner flow, varied practice, context, production and mastery evidence.

It is not a reason to invent a different importer schema.

Numeric examples such as "2 theory screens", "6 vocabulary items", or "16 exercises" are quality/reference guidance, not universal blind quotas. A richer lesson may legitimately contain more vocabulary or a different number of theory screens/exercises when pedagogically justified and compatible with the real importer contract.

When a user supplies a known-working importer example, preserve its actual field names and types. When in doubt, inspect the working file instead of guessing.

## 17. FAILURE PROTOCOL
If a hard defect is found:

**STOP. Do not continue producing dependent content.**

1. Identify the defect.
2. Repair it.
3. Parse again.
4. Re-run semantic and adversarial checks.
5. Commit the repair.
6. Re-read GitHub state.
7. Continue only when the repository is clean.

Never hide a defect by changing progress documentation.

## 18. USER CONTINUATION SIGNAL
The user's `+` means: execute the next repository-defined production task without asking what to do next, unless the repository contains a genuine blocker requiring user input.

## 19. ANTI-ERROR CHECKLIST — RUN BEFORE EVERY COMMIT
Ask explicitly:

- Am I copying the **FORMAT**, not the sample's numbering?
- What is the actual next lesson number in the target section?
- Is the target language **Slovak / slovenčina**, not Slovenian / slovenščina?
- Are learner-facing instructions **Ukrainian**?
- Am I using the **real importer contract**, not an invented schema?
- Did I preserve field names and value types from the working example?
- Did I increase vocabulary when useful rather than artificially limiting it?
- Is every new word purposeful and actually practiced?
- Are all `wordIds` and `lessonId` references valid?
- Does every exercise's answer logic work?
- Does the final situation demonstrate transfer?
- Did I replace old files rather than create duplicates?
- Did I re-read the actual files from GitHub after writing?
- Did I distinguish JSON/schema QA from actual importer QA?

If any answer is uncertain, stop and inspect the repository/example before committing.

## 20. CORE RULE
**Quality and repository truth beat speed. A smaller number of valid, meaningful lessons is better than a larger number of broken, thin, or duplicated lessons.**
