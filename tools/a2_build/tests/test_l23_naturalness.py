import unittest
from tools.a2_build.generator import example_for

class L23NaturalnessTests(unittest.TestCase):
    def test_zajtra_namiesto_uses_natural_contrast(self):
        self.assertEqual(
            example_for('zajtra namiesto','завтра замість'),
            ('Prídem zajtra, nie dnes.','Я прийду завтра, не сьогодні.'),
        )

if __name__=='__main__':
    unittest.main()
