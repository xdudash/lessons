from __future__ import annotations

import localize_clean as base


def suffix_localize(obj, key, translations):
    value = obj.get(key)
    if not isinstance(value, str) or not base.CYR.search(value):
        return
    if key == "uk":
        obj["ru"] = translations["ru"][value]
        obj["en"] = translations["en"][value]
        return
    root = key[:-2] if key.endswith("Uk") else key
    obj[root + "Ru"] = translations["ru"][value]
    obj[root + "En"] = translations["en"][value]


_original_collect_sources = base.collect_sources
LEGACY_SUPPORT_KEYS = {"left", "right", "value", "sender", "body", "day", "hours", "correct"}


def collect_sources(value, out, key=None):
    _original_collect_sources(value, out, key)

    def walk(node):
        if isinstance(node, dict):
            for k, child in node.items():
                if k in LEGACY_SUPPORT_KEYS and isinstance(child, str) and base.CYR.search(child):
                    out.add(child)
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)


base.suffix_localize = suffix_localize
base.collect_sources = collect_sources

fixed_translation = base.fixed_translation
localize_lesson = base.localize_lesson
quality_audit = base.quality_audit
verify = base.verify
validate_schema = base.validate_schema

if __name__ == "__main__":
    base.main()
