import unittest

class SemanticProfileTests(unittest.TestCase):
    def profiles(self):
        from tools.a2_build.semantic_profiles import PROFILES
        return PROFILES

    def test_all_90_lessons_have_explicit_semantic_profiles(self):
        profiles=self.profiles()
        self.assertEqual(set(profiles),set(range(1,91)))
        for order,p in profiles.items():
            self.assertEqual(len(p.models),3,order)
            self.assertEqual(len(p.prompts_uk),3,order)
            for sk,uk in p.models:
                self.assertGreaterEqual(len(sk.split()),2,(order,sk))
                self.assertTrue(sk.endswith(('.', '?', '!')),(order,sk))
                self.assertTrue(uk,(order,sk))
            for prompt in p.prompts_uk:
                self.assertNotIn('скажи:',prompt.lower(),(order,prompt))
                self.assertGreaterEqual(len(prompt.split()),5,(order,prompt))

    def test_models_avoid_known_unnatural_patterns(self):
        forbidden=(
            'Včera to zvládnem.',
            'Ráno som.',
            'To je aktívny.',
            'Chcem budem',
            'To je pôjdem.',
            'To je prídem.',
            'To je zavolám.',
            'Chcem skúsenosť.',
            'namiesto dnes',
            'urobte prestup',
            'potom tadiaľ cez',
            'pokojne večerať s rodinou',
            'zľava a akcia',
            'vybavenie hotové',
            'Nabudúce môžeme sa',
            'neschopný práce',
            'skôr lepšia rýchlejšia',
            'zlý nápad bez plánu',
            'Podľa mňa by som radšej',
        )
        for order,p in self.profiles().items():
            joined=' '.join(x[0] for x in p.models)
            for bad in forbidden:
                self.assertNotIn(bad,joined,(order,bad,joined))

    def test_doctor_profile_practises_symptom_and_duration(self):
        p=self.profiles()[75]
        sk=' '.join(x[0] for x in p.models)
        self.assertTrue(('kašeľ' in sk or 'bolí' in sk) and ('trvá' in sk or 'dni' in sk),sk)
        self.assertTrue(any('лікар' in x.lower() or 'симптом' in x.lower() for x in p.prompts_uk))

    def test_choice_profile_has_real_choice_language(self):
        p=self.profiles()[82]
        sk=' '.join(x[0] for x in p.models)
        low=sk.lower()
        for bad in ('To je radšej.','To je skôr.','To je namiesto.'):
            self.assertNotIn(bad,sk)
        self.assertTrue('radšej' in low and ('keby' in low or 'záleží' in low),sk)

    def test_a2_final_profile_integrates_past_future_problem_and_opinion(self):
        p=self.profiles()[90]
        sk=' '.join(x[0].lower() for x in p.models)
        self.assertTrue(any(x in sk for x in ('včera','minul','stalo','bol som')),sk)
        self.assertTrue(any(x in sk for x in ('zajtra','budem','môžeme','stretneme')),sk)
        self.assertTrue(any(x in sk for x in ('problém','riešen','pretože','podľa mňa')),sk)
        self.assertTrue(any('проблем' in x.lower() for x in p.prompts_uk))
        self.assertTrue(any('план' in x.lower() or 'завтра' in x.lower() for x in p.prompts_uk))

if __name__=='__main__':
    unittest.main()
