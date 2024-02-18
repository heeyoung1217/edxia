from edxia.utils.path import pattern_from_BSE
from edxia.composite import CompositeChannels
from edxia.composite.segmentation import SlicSegmenter
from edxia.io.loader import PickleLoader
from edxia.core.experiment import MappingExperiment

import matplotlib.pyplot as plt
from skimage.color import label2rgb

from edxia.filters.denoise import UniformFilter

import unittest

class TestSegmentation(unittest.TestCase):
    def test_segmentation(self):
        pattern = pattern_from_BSE("../data/esprit_BSE.txt")
        exp = MappingExperiment(pattern, description="Test experiment: default loader")
        loader = PickleLoader(exp, filters=[UniformFilter(3),])

        channels = CompositeChannels(["Si", "Al", "Ca"], [4, 4, 2])
        composite = loader.load_composite(channels)

        labels = SlicSegmenter(5, 5000).apply(composite)

        colors = labels.get_color_labels()
        plt.imshow(label2rgb(labels.labels, colors=colors))

        loader.remove_npy_files()

if __name__ == '__main__':
    unittest.main()

