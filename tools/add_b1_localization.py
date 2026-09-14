#!/usr/bin/env python3
"""
Add the SlovakGo localization block to B1 lesson JSON files.

The script is intentionally conservative:
- only files whose lesson level is B1 are changed;
- existing localization blocks are left intact by default;
- JSON is parsed and written back with stable UTF-8 formatting.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


LOCALIZATION = {
    "uiLanguages": ["ru", "uk", "en"],
    "targetLanguage": "sk",
    "fallbackUiLanguage": "en",
}


def iter_json_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".json" else []
    return sorted(root.rglob("*.json"))


def get_lessons(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("lessons"), list):
        return [item for item in data["lessons"] if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def is_b1_lesson(lesson: dict[str, Any]) -> bool:
    level = str(lesson.get("level", "")).upper()
    lesson_id = str(lesson.get("id", "")).lower()
    section_id = str(lesson.get("sectionId", "")).lower()
    return level == "B1" or "-b1" in lesson_id or lesson_id.startswith("b1") or section_id.startswith("b1")


def patch_file(path: Path, *, overwrite_existing: bool, make_backup: bool) -> tuple[bool, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"invalid JSON: {exc}"

    lessons = get_lessons(data)
    if not lessons:
        return False, "no lesson object found"

    b1_lessons = [lesson for lesson in lessons if is_b1_lesson(lesson)]
    if not b1_lessons:
        return False, "not B1"

    changed = False
    for lesson in b1_lessons:
        if "localization" not in lesson or overwrite_existing:
            lesson["localization"] = dict(LOCALIZATION)
            changed = True

    if not changed:
        return False, "already has localization"

    if make_backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return True, "localization added"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add localization.uiLanguages/targetLanguage/fallbackUiLanguage to SlovakGo B1 JSON files."
    )
    parser.add_argument("path", type=Path, help="B1 JSON file or directory with B1 JSON files")
    parser.add_argument("--overwrite-existing", action="store_true", help="replace existing localization blocks")
    parser.add_argument("--backup", action="store_true", help="create .bak files before writing changes")
    args = parser.parse_args()

    files = iter_json_files(args.path)
    changed = 0
    skipped = 0
    failed = 0

    for file_path in files:
        ok, reason = patch_file(
            file_path,
            overwrite_existing=args.overwrite_existing,
            make_backup=args.backup,
        )
        if ok:
            changed += 1
            print(f"UPDATED  {file_path}")
        else:
            skipped += 1
            if reason.startswith("invalid JSON"):
                failed += 1
                print(f"FAILED   {file_path} - {reason}")

    print()
    print(f"Scanned: {len(files)}")
    print(f"Updated: {changed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
