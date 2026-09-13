import os, unittest
from pathlib import Path
ROOT=Path(os.environ.get('SLOVAKGO_REPO_ROOT','.')).resolve()
@unittest.skipUnless((ROOT/'AGENTS.md').exists(),'repo docs unavailable in unit sandbox')
class RepoContractTests(unittest.TestCase):
    def test_root_docs_are_not_a1_only(self):
        agents=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
        master=(ROOT/'MASTER.md').read_text(encoding='utf-8')
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertIn('A1–C2',agents)
        self.assertIn('a2-sNN-lNN',agents)
        self.assertIn('interactive_scenario',agents)
        self.assertIn('A2/LESSON_PLAN.md',master)
        self.assertIn('lessons/a2/',readme)
