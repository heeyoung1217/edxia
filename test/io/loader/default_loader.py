from edxia.io.loader import DefaultLoader
from edxia.core.experiment import MappingExperiment

from edxia.utils.path import pattern_from_BSE

import unittest

class TestDefaultLoader(unittest.TestCase):
    def test_loading(self):
        pattern = pattern_from_BSE("../../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")

        loader = DefaultLoader(exp)

        ca_map = loader.load_edsmap("Ca")




if __name__ == '__main__':
    unittest.main()