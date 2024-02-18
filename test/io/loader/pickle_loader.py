from edxia.io.loader import PickleLoader
from edxia.core.experiment import MappingExperiment

from edxia.utils.path import pattern_from_BSE

import os.path

import unittest

class TestPickleLoader(unittest.TestCase):
    def test_loading(self):
        pattern = pattern_from_BSE("../../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")

        loader = PickleLoader(exp)

        ca_map = loader.load_edsmap("Ca")
        ca_pickle_path = loader.get_path_picklemap("Ca")

        self.assertTrue(os.path.exists(ca_pickle_path))


        ca_map2 = loader.load_edsmap("Ca")

        self.assertTrue(((ca_map.map - ca_map2.map) < 1e-14).all())

        loader.remove_npy_files()
        self.assertFalse(os.path.exists(ca_pickle_path))

    def test_complex_loading(self):
        pattern = pattern_from_BSE("../../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")

        loader = PickleLoader(exp)

        comp_map = loader.load_edsmap("Ca+Si")
        ca_pickle_path = loader.get_path_picklemap("Ca")
        si_pickle_path = loader.get_path_picklemap("Si")

        self.assertTrue(os.path.exists(ca_pickle_path))
        self.assertTrue(os.path.exists(si_pickle_path))


    def test_stack_loading(self):
        pattern = pattern_from_BSE("../../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")

        loader = PickleLoader(exp)

        stack = loader.load_stack()

        self.assertEqual(stack.components, exp.list_components)

        loader.remove_npy_files()

if __name__ == '__main__':
    unittest.main()

