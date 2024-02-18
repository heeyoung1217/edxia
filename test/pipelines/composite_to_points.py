from glue import qglue

from edxia.utils.path import pattern_from_BSE
from edxia.composite import CompositeChannels
from edxia.composite.segmentation import SlicSegmenter
from edxia.io.loader import PickleLoader
from edxia.core.experiment import MappingExperiment

from edxia.point_analysis.points import points_from_segmentation

import matplotlib.pyplot as plt
from skimage.color import label2rgb

from edxia.filters.denoise import UniformFilter

from edxia.glue import gluedata_from_points, gluedata_from_stack_and_composite
from edxia.glue.arithmetic_data import define_ratio
from edxia.glue.link_data import link_stack_pts
from edxia.glue.map_coordinates import MapCoordinates

from glue.app.qt.application import GlueApplication
from glue.core import DataCollection

pattern = pattern_from_BSE("../data/esprit_BSE.txt")
exp = MappingExperiment(pattern, description="Test experiment: default loader")
loader = PickleLoader(exp, filters=[UniformFilter(3),])

channels = CompositeChannels(["Si", "Al", "Ca"], [4, 4, 2])
composite = loader.load_composite(channels)

filter_bse = loader.load_edsmap("BSE")
composite.mix_with_bse(filter_bse, 0.6)
composite.map[filter_bse.map<0.3,:] = 0
composite.map[filter_bse.map>0.54,:] = 0
#filter_bse.map[filter_bse.map<0.2] = 0

plt.imshow(composite.map)

labels = SlicSegmenter(5, 10000).apply(composite)

colors = labels.get_color_labels()
plt.figure()
plt.imshow(label2rgb(labels.labels, colors=colors))

stack = loader.load_stack()
stack.to_atomic(copy=False)

pts = points_from_segmentation(stack, labels, mask_img=composite.map)
#pts.to_atomic(copy=False)

plt.figure()
plt.plot(pts["Si/Ca"], pts["Al/Ca"], ".")
plt.xlim([0,0.6])
plt.ylim([0,0.5])

plt.figure()
plt.plot(pts["Al/Ca"], pts["S/Ca"], ".")
plt.xlim([0,0.5])
plt.ylim([0,0.5])

loader.remove_npy_files()

pts_data = gluedata_from_points("points", pts)


coords = MapCoordinates(scale=0.5, col_trans=-200, labels = (r"y ($\mathrm{\mu}$m)", r"x ($\mathrm{\mu}$m)"))

stack_data = gluedata_from_stack_and_composite(exp.label+"maps", stack, composite, coords=coords, extras=extras)

dc = DataCollection([pts_data, stack_data])

ga = GlueApplication(dc)

define_ratio("AlCa", pts_data, "Al", "Ca")
define_ratio("SiCa", pts_data, "Si", "Ca")
define_ratio("SCa", pts_data, "S", "Ca")

link_stack_pts(dc, stack.components, stack_data, pts_data)

ga.start()