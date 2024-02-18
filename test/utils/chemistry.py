import edxia.utils.chemistry as chemistry

import unittest

class TestSegmentation(unittest.TestCase):
    def test_molar_masses(self):
        self.assertEqual(chemistry.molar_masses["H"], 1.0079)

        with self.assertRaises(KeyError):
            chemistry.molar_masses["Plop"]

        self.assertEqual(chemistry.oxides["Ca"][0], "CaO")
        self.assertEqual(chemistry.oxides["Ca"][1], 1)

        with self.assertRaises(KeyError):
            chemistry.oxides["Plop"]

    def test_formula(self):
        self.assertEqual(chemistry.formula_to_composition("CaO"), {"Ca":1.0, "O": 1.0})
        self.assertEqual(chemistry.formula_to_composition("Na2O"), {"Na":2.0, "O": 1.0})
        self.assertEqual(chemistry.formula_to_composition("Ca(OH)2"), {"Ca":1.0, "O": 2.0, "H": 2.0})

if __name__ == '__main__':
    unittest.main()

