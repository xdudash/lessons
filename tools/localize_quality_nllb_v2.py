from __future__ import annotations

import gc

import localize_quality_nllb as q
from quality_overrides import LEXICAL, OVERRIDES
from translation_fixes import LEXICAL as UK_LEXICAL, fixed_translation, normalize_translation


def build_tables(sources: set[str], preferred: dict[str, str]) -> dict[tuple[str, str], str]:
    engine = q.NLLB()
    table: dict[tuple[str, str], str] = {}

    for source in sources:
        for target in ("ru", "en"):
            if source in OVERRIDES:
                table[(target, source)] = OVERRIDES[source][target]
                continue
            fixed = fixed_translation(target, source)
            if fixed is not None:
                table[(target, source)] = fixed
                continue
            if source in UK_LEXICAL:
                table[(target, source)] = UK_LEXICAL[source][target]
                continue
            sk = preferred.get(source)
            if sk in LEXICAL:
                table[(target, source)] = LEXICAL[sk][target]

    for target in ("ru", "en"):
        unresolved = [s for s in sorted(sources) if (target, s) not in table]
        raw = engine.translate_batch(unresolved, "uk", target)
        retry: list[str] = []
        for source in unresolved:
            value = normalize_translation(target, source, raw[source])
            lost = any(tok not in value for tok in q.meaningful_latin_tokens(source))
            if q.invalid(target, value) or lost:
                retry.append(source)
            else:
                table[(target, source)] = value

        if retry:
            segmented = {source: q.split_keep_latin(source) for source in retry}
            chunks = sorted({piece.strip() for parts in segmented.values() for flag, piece in parts if flag and piece.strip()})
            translated_chunks = engine.translate_batch(chunks, "uk", target, batch_size=32)
            for source in retry:
                built: list[str] = []
                for flag, piece in segmented[source]:
                    if flag and piece.strip():
                        prefix = piece[:len(piece) - len(piece.lstrip())]
                        suffix = piece[len(piece.rstrip()):]
                        built.append(prefix + translated_chunks[piece.strip()] + suffix)
                    else:
                        built.append(piece)
                value = normalize_translation(target, source, "".join(built))
                if q.invalid(target, value) or any(tok not in value for tok in q.meaningful_latin_tokens(source)):
                    raise RuntimeError(f"quality check failed {target}: {source!r} -> {value!r}")
                table[(target, source)] = value

    del engine
    gc.collect()
    return table


q.build_tables = build_tables
q.main()
