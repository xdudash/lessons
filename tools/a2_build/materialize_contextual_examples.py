from __future__ import annotations

import ast
from pathlib import Path
from pprint import pformat

ROOT = Path(__file__).resolve().parents[2]
TEST = ROOT / 'tools' / 'a2_build' / 'tests' / 'test_contextual_word_examples.py'
OUT = ROOT / 'tools' / 'a2_build' / 'contextual_examples.py'
GEN = ROOT / 'tools' / 'a2_build' / 'generator.py'


def load_cases():
    tree = ast.parse(TEST.read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CASES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError('CASES not found')


def main():
    cases = load_cases()
    mapping = {(sk.lower().strip(), uk): tuple(expected) for sk, uk, expected in cases}
    OUT.write_text(
        "from __future__ import annotations\n\n"
        "# Context-sensitive examples keyed by Slovak target + its Ukrainian meaning.\n"
        "# Generated from the regression corpus; edit the corpus first, then rematerialize.\n"
        f"CONTEXTUAL_EXAMPLES = {pformat(mapping, width=120, sort_dicts=True)}\n",
        encoding='utf-8',
    )

    src = GEN.read_text(encoding='utf-8')
    import_line = 'from .contextual_examples import CONTEXTUAL_EXAMPLES\n'
    if import_line not in src:
        src = src.replace('from .natural_examples import EXAMPLES\n', 'from .natural_examples import EXAMPLES\n' + import_line, 1)
    old = "    low=sk.lower().strip()\n    if low in EXAMPLES: return EXAMPLES[low]\n"
    new = "    low=sk.lower().strip()\n    contextual=CONTEXTUAL_EXAMPLES.get((low, uk))\n    if contextual is not None: return contextual\n    if low in EXAMPLES: return EXAMPLES[low]\n"
    if old not in src and new not in src:
        raise RuntimeError('example_for insertion point not found')
    src = src.replace(old, new, 1)
    GEN.write_text(src, encoding='utf-8')
    print(f'Materialized {len(mapping)} contextual examples and patched generator.')


if __name__ == '__main__':
    main()
