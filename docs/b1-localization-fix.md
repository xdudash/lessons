# SlovakGo B1 Localization Fix

This patch adds the missing language configuration to SlovakGo B1 lesson JSON files:

```json
"localization": {
  "uiLanguages": ["ru", "uk", "en"],
  "targetLanguage": "sk",
  "fallbackUiLanguage": "en"
}
```

## Run

From the repository root:

```bash
python3 tools/add_b1_localization.py B1 --backup
```

Without backups:

```bash
python3 tools/add_b1_localization.py B1
```

The script only changes files detected as B1 lessons. Existing `localization` blocks are kept as-is unless you run:

```bash
python3 tools/add_b1_localization.py B1 --overwrite-existing
```
