import json
import tempfile
import unittest
from pathlib import Path

from tools.a2_build.generator import build_lesson
from tools.a2_build.model import LessonCopy, OwnedTarget, PlanLesson
from tools.a2_build.qa_a2 import check_file
from tools.a2_build.semantic_profiles import PROFILES


class SemanticFinalQATests(unittest.TestCase):
    def semantic_doc(self):
        plan = PlanLesson(
            1, 1, 'a2-s01-l01', 'Aký som človek?', 'x',
            ('milý','veselý','tichý','pokojný','aktívny','lenivý','pracovitý','zaujímavý'),
        )
        copy = LessonCopy(
            'Яка я людина?', 'Описуємо характер і звички.',
            ('милий','веселий','тихий','спокійний','активний','лінивий','працьовитий','цікавий'),
        )
        owned = [OwnedTarget(sk, uk, 'NEW') for sk, uk in zip(plan.mapped_targets, copy.target_uk)]
        doc = build_lesson(plan, copy, owned, 'a2-s01-l02')
        profile = PROFILES[1]
        steps = []
        models = [x[0] for x in profile.models]
        for i, (prompt, model) in enumerate(zip(profile.prompts_uk, models), 1):
            distractors = [x for x in models if x != model]
            steps.append({
                'id': f'f{i}',
                'prompt': {'uk': prompt},
                'options': [
                    {'sk': model, 'correct': True},
                    {'sk': distractors[0], 'correct': False},
                    {'sk': distractors[1], 'correct': False},
                ],
            })
        doc['lessons'][0]['finalSituation']['steps'] = steps
        return doc

    def check(self, doc):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'a2-s01-l01.json'
            p.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            return check_file(p, 'a2-s01-l01', 'a2-s01-l02')

    def test_semantic_profile_final_is_accepted(self):
        self.assertEqual(self.check(self.semantic_doc()), [])

    def test_wrong_semantic_prompt_is_rejected(self):
        doc = self.semantic_doc()
        doc['lessons'][0]['finalSituation']['steps'][0]['prompt']['uk'] = 'Інша ситуація, яка не належить цьому кроку.'
        errors = self.check(doc)
        self.assertTrue(any('semantic final prompt mismatch' in e for e in errors), errors)

    def test_swapped_semantic_answer_is_rejected(self):
        doc = self.semantic_doc()
        step = doc['lessons'][0]['finalSituation']['steps'][0]
        step['options'][0]['correct'] = False
        step['options'][1]['correct'] = True
        errors = self.check(doc)
        self.assertTrue(any('semantic final answer mismatch' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
