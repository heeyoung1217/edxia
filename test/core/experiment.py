from edxia.core import experiment
from edxia.io.raw_io import esprit_ascii_map_format
from edxia.utils.path import pattern_from_BSE

import unittest

class TestMappingExperiment(unittest.TestCase):
    def test_mapping(self):
        pattern = pattern_from_BSE("../data/esprit_BSE.txt")
        label = "Test"

        exp = experiment.MappingExperiment(pattern, label=label,
                                     description="Long description")

        self.assertEqual(exp.label, label)
        self.assertEqual(exp.map_format, esprit_ascii_map_format)
        self.assertEqual(exp.get_path_map("Ca"), "../data/esprit_Ca.txt")

        with self.assertRaises(RuntimeError):
            exp.get_path_map("NotAComponent")

        raw_map = exp.load_raw_map("Ca")
        self.assertEqual(len(raw_map.shape), 2)


if __name__ == '__main__':
    unittest.main()