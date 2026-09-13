import json, tempfile, unittest
from pathlib import Path
from tools.a2_build.ownership import normalize_sk, load_a1_owned, classify_targets
from tools.a2_build.model import PlanLesson, LessonCopy

class OwnershipTests(unittest.TestCase):
    def test_normalize_and_a1_inventory(self):
        self.assertEqual(normalize_sk('  Lekáreň. '),'lekáreň')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a1-s01-l01.json'; p.write_text(json.dumps({'lessons':[{'words':[{'sk':'Lekáreň'}]}]}),encoding='utf-8')
            self.assertIn('lekáreň',load_a1_owned(Path(td)))
    def test_classification_progression(self):
        p=PlanLesson(1,1,'a2-s01-l01','x','x',('lekáreň','nové'))
        c=LessonCopy('x','x',('аптека','нове'))
        got=classify_targets(p,c,{'lekáreň'},set())
        self.assertEqual([x.status for x in got],['REVIEW','NEW'])

if __name__=='__main__': unittest.main()
