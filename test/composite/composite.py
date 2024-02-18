from edxia.utils.path import pattern_from_BSE
from edxia.composite import CompositeMap, CompositeChannels
from edxia.io.loader import PickleLoader
from edxia.core.experiment import MappingExperiment
import numpy as np

import unittest

class TestComposite(unittest.TestCase):
    def test_composite_loading(self):
        pattern = pattern_from_BSE("../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")
        loader = PickleLoader(exp)


        channels = CompositeChannels(["Si", "Al", "Ca"], [4, 4, 2])
        composite = loader.load_composite(channels)

        self.assertTrue(len(composite.map.shape) == 3)
        self.assertTrue(composite.map.shape[2] == 3)

        loader.remove_npy_files()

if __name__ == '__main__':
    unittest.main()

