import json, tempfile, unittest
from pathlib import Path
from tools.a2_build.model import PlanLesson, LessonCopy, OwnedTarget
from tools.a2_build.generator import build_lesson, example_for
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

    def test_build_lesson_uses_explicit_semantic_profiles(self):
        from tools.a2_build.semantic_profiles import PROFILES
        cases=(
            (3,13,'a2-s03-l13','Čo som robil včera?',('včera','ráno som','potom som','večer som','bol som','mal som','robil som','prišiel som','išiel som')),
            (4,19,'a2-s04-l19','Čo budem robiť zajtra?',('zajtra','budem pracovať','budem študovať','pôjdem','prídem','zavolám','napíšem','večer budem')),
            (15,90,'a2-s15-l90','A2 v praxi',('problém','riešenie','zajtra','včera','plán','podľa mňa','pretože','dohodnúť sa')),
        )
        for section,order,lid,title,targets in cases:
            with self.subTest(order=order):
                copy=LessonCopy(f'Урок {order}',f'Семантичний намір {order}.',tuple(f'значення {i}' for i in range(len(targets))))
                plan=PlanLesson(section,order,lid,title,'x',targets)
                owned=[OwnedTarget(sk,uk,'NEW') for sk,uk in zip(targets,copy.target_uk)]
                doc=build_lesson(plan,copy,owned,None if order==90 else f'next-{order}')['lessons'][0]
                profile=PROFILES[order]
                theory_models=[screen['examples'][0]['sk'] for screen in doc['theoryScreens']]
                self.assertEqual(theory_models,[model[0] for model in profile.models])
                prompts=[step['prompt']['uk'] for step in doc['finalSituation']['steps']]
                self.assertEqual(prompts,list(profile.prompts_uk))
                correct=[next(opt['sk'] for opt in step['options'] if opt['correct']) for step in doc['finalSituation']['steps']]
                self.assertEqual(correct,[model[0] for model in profile.models])
                self.assertFalse(any('скажи:' in prompt.lower() for prompt in prompts))

    def test_temporal_adverb_uses_matching_past_context(self):
        self.assertEqual(example_for('včera','учора'), ('Včera som bol doma.','Учора я був удома.'))

    def test_future_chunk_is_not_prefixed_with_chcem(self):
        self.assertEqual(example_for('budem pracovať','я буду працювати'), ('Budem pracovať.','Я буду працювати.'))

    def test_past_reflexive_chunk_keeps_its_tense(self):
        self.assertEqual(example_for('stretli sme sa','ми зустрілися'), ('Stretli sme sa.','Ми зустрілися.'))

    def test_unaccented_masculine_adjective_gets_copula(self):
        self.assertEqual(example_for('aktívny','активний'), ('Je aktívny.','Він активний.'))

    def test_incomplete_past_prefix_gets_a_real_completion(self):
        self.assertEqual(example_for('ráno som','вранці я…'), ('Ráno som bol doma.','Вранці я був удома.'))

    def test_temporal_noun_phrase_is_used_in_a_sentence(self):
        self.assertEqual(example_for('minulý víkend','минулі вихідні'), ('Minulý víkend som bol doma.','Минулі вихідні я був удома.'))

    def test_ost_noun_is_not_mistaken_for_an_infinitive(self):
        self.assertEqual(example_for('skúsenosť','досвід'), ('To je skúsenosť.','Це досвід.'))

    def test_single_finite_future_verb_is_a_sentence(self):
        self.assertEqual(example_for('pôjdem','я піду / поїду'), ('Pôjdem zajtra.','Я піду / поїду завтра.'))

    def test_spatial_prepositional_chunk_gets_context(self):
        self.assertEqual(example_for('na rohu','на розі'), ('Stretneme sa na rohu.','Зустрінемося на розі.'))

    def test_frequency_adverb_gets_natural_context(self):
        self.assertEqual(example_for('často','часто'), ('Často chodím pešo.','Я часто ходжу пішки.'))

    def test_direction_adverb_gets_location_context(self):
        self.assertEqual(example_for('vpravo','праворуч'), ('Obchod je vpravo.','Магазин праворуч.'))

if __name__=='__main__': unittest.main()
