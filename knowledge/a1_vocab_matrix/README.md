# A1 complete vocabulary matrix

The complete baseline-derived item-level matrix is stored as `A1_COMPLETE.json.gz.b64` because the uncompressed matrix is too large for practical human editing.

## Contents
- 250 baseline lessons
- 1,500 vocabulary entries
- 1,272 unique expressions
- 187 repeated expressions
- 1,085 single-occurrence expressions
- For every unique expression: Russian translation, first owner lesson, all baseline occurrence lessons, and heuristic stage per occurrence.

## Decode
The file is base64 text containing a gzip-compressed UTF-8 JSON document. Decode base64, decompress gzip, then parse JSON.

Expected SHA-256 of the uncompressed compact JSON payload: `283c8ae1586d5dd9218fe13b02a302b8a39575c572ea5d4fd14e93f648b7aa0c`.

Stage policy: first occurrence = NEW; second = REVIEW; third = TRANSFER; fourth+ = MASTERY. Frequency is planning metadata, not proof of pedagogical mastery.

This artifact is the durable item-level corpus needed to resume A1 vocabulary ownership work without access to the original chat or uploaded ZIP.