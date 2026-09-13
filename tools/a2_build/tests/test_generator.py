import json, tempfile, unittest
from pathlib import Path
from tools.a2_build.model import PlanLesson, LessonCopy, OwnedTarget
from tools.a2_build.generator import build_lesson
from tools.a2_build.qa_a2 import check_file

class GeneratorTests(unittest.TestCase):
    def sample(self):
        p=PlanLesson(1,1,'a2-s01-l01','Aký som človek?','x',('milý','veselý','tichý','pokojný','aktívny','lenivý','pracovitý','zaujímavý'))
        c=LessonCopy('Яка я людина?','Описуємо характер і звички.',('милий','веселий','тихий','спокійний','активний','лінивий','працьовитий','цікавий'))
        o=[OwnedTarget(sk,uk,'NEW') for sk,uk in zip(p.mapped_targets,c.target_uk)]
        return p,c,o
    def test_runtime_shape_and_adversarial_qa(self):
        p,c,o=self.sample(); doc=build_lesson(p,c,o,'a2-s01-l02'); l=doc['lessons'][0]
        self.assertEqual(l['level'],'A2'); self.assertEqual(len(l['theoryScreens']),3); self.assertEqual(len(l['exercises']),14); self.assertEqual(len(l['finalSituation']['steps']),3); self.assertEqual(l['resultScreen']['nextLesson']['id'],'a2-s01-l02')
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'a2-s01-l01.json'; f.write_text(json.dumps(doc,ensure_ascii=False),encoding='utf-8')
            self.assertEqual(check_file(f,'a2-s01-l01','a2-s01-l02'),[])
    def test_duplicate_final_option_is_rejected(self):
        p,c,o=self.sample(); doc=build_lesson(p,c,o,'a2-s01-l02')
        st=doc['lessons'][0]['finalSituation']['steps'][0]; st['options'][1]['sk']=st['options'][0]['sk']
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'a2-s01-l01.json'; f.write_text(json.dumps(doc,ensure_ascii=False),encoding='utf-8')
            errs=check_file(f,'a2-s01-l01','a2-s01-l02'); self.assertTrue(any('duplicate labels' in e for e in errs))
    def test_terminal_omits_nextlesson(self):
        p,c,o=self.sample(); p=PlanLesson(15,90,'a2-s15-l90','A2 v praxi','x',p.mapped_targets); doc=build_lesson(p,c,o,None)
        self.assertNotIn('nextLesson',doc['lessons'][0]['resultScreen'])

if __name__=='__main__': unittest.main()
