from edxia.utils import path

import unittest


class TestPath(unittest.TestCase):
    def test_pattern_from_BSE(self):
        self.assertEqual(path.pattern_from_BSE("../data/esprit_BSE.txt"), "../data/esprit_{component}.txt")
        self.assertEqual(path.pattern_from_BSE("../data/esprit_%x_BSE.txt"), "../data/esprit_%x_{component}.txt")
        self.assertEqual(path.pattern_from_BSE("../data/BSE_BSE.txt"), "../data/{component}_{component}.txt")

    def test_component_path(self):
        pattern = path.pattern_from_BSE("../data/esprit_BSE.txt")
        self.assertEqual(path.find_component_path(pattern, "Ca"), "../data/esprit_Ca.txt")

        with self.assertRaises(RuntimeError):
            ambiguous_pattern = "../data/esprit_*-{component}.txt"
            path.find_component_path(ambiguous_pattern, "Ca")

        with self.assertRaises(RuntimeError):
            wrong_pattern = "../data/esprit_platypus_{component}.txt"
            path.find_component_path(wrong_pattern, "Ca")

    def test_list_components(self):
        pattern = path.pattern_from_BSE("../data/esprit_BSE.txt")
        components = path.find_components(pattern)
        self.assertTrue("Ca" in components)
        self.assertTrue("BSE" in components)
        self.assertFalse("Ra" in components)


if __name__ == '__main__':
    unittest.main()