from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'tools' / 'build_a1.py'
spec = importlib.util.spec_from_file_location('a1_builder', source)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

mod.LESSON_SECTIONS = [
    ('a1_s06', 31), ('a1_s07', 38), ('a1_s08', 44),
    ('a1_s09', 51), ('a1_s10', 57), ('a1_s11', 63),
    ('a1_s12', 68), ('a1_s13', 73), ('a1_s14', 77),
]
mod.main()
