import os, unittest
from pathlib import Path
from tools.a2_build.content import COPY
from tools.a2_build.ownership import parse_a2_plan, load_a1_owned, classify_targets
ROOT=Path(os.environ.get('SLOVAKGO_REPO_ROOT','.')).resolve()
@unittest.skipUnless((ROOT/'A2'/'LESSON_PLAN.md').exists() and (ROOT/'lessons'/'a1').exists(),'full repo unavailable')
class IntegrationTests(unittest.TestCase):
    def test_full_a2_map_and_copy_alignment(self):
        plan=parse_a2_plan(ROOT/'A2'/'LESSON_PLAN.md')
        self.assertEqual(len(plan),90); self.assertEqual(set(COPY),set(range(1,91)))
        for p in plan:
            self.assertEqual(len(p.mapped_targets),len(COPY[p.order].target_uk),p.lesson_id)
    def test_a1_inventory_is_real(self):
        a1=load_a1_owned(ROOT/'lessons'/'a1')
        self.assertGreater(len(a1),100)
        self.assertIn('lekáreň',a1)
