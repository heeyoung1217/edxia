from edxia.core import MappingExperiment
from edxia.io.loader import PickleLoader
from edxia.io.raw_io import imagej_ascii_bse_format
from edxia.filters.denoise import DenoiseFilter

from edxia.composite import CompositeChannels
from edxia.composite.segmentation import SlicSegmenter

from edxia.point_analysis import points_from_segmentation

from skimage.color import label2rgb

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

"""
This script shows how to:
   - read the maps
   - create a composite map
   - segment the composite map
"""

# The pattern to the maps
pattern = "../example_map_1/map_short_atom_{component}.txt"

# The loaders
exp = MappingExperiment(pattern, "LC3-wc04-28d",
                        bse_format=imagej_ascii_bse_format)
loader = PickleLoader(exp, filters=[DenoiseFilter(0.1),])




# The composite
channels = CompositeChannels(["Fe","Si", "Ca"], factors=[4.0,4.0,2.0])
composite = loader.load_composite(channels)
bse = loader.load_edsmap("BSE")
composite.mix_with_bse(bse, 0.8)

# Define some new colormaps for the plots

empty = ((0.0,  0.0, 0.0),
         (1.0,  0.0, 0.0))
full = ((0.0,  0.0, 0.0),
        (1.0,  1.0, 1.0))

cdict_red = {'red':   full,
             'green': empty,
             'blue':  empty}

cdict_blue = {'red':  empty,
             'green': empty,
             'blue':  full}

cdict_green = {'red':   empty,
               'green': full,
               'blue':  empty}

# Plot individual maps

fig, ax = plt.subplots(2,2, sharex=True, sharey=True)

ax[0,0].set_aspect("equal")
ax[0,0].set_axis_off()
ax[0,0].set_title("BSE")
ax[0,0].xaxis.set_visible(False)
ax[0,0].yaxis.set_visible(False)
ax[0,0].imshow(bse.map, cmap=plt.cm.gray)


ax[0,1].set_aspect("equal")
ax[0,1].set_axis_off()
ax[0,1].set_title("Fe")
ax[0,1].xaxis.set_visible(False)
ax[0,1].yaxis.set_visible(False)
ax[0,1].imshow(loader.load_edsmap("Fe").map,
          cmap=LinearSegmentedColormap("red", cdict_red))

ax[1,0].set_aspect("equal")
ax[1,0].set_axis_off()
ax[1,0].set_title("Si")
ax[1,0].xaxis.set_visible(False)
ax[1,0].yaxis.set_visible(False)
ax[1,0].imshow(loader.load_edsmap("Si").map,
          cmap=LinearSegmentedColormap("green", cdict_green))

ax[1,1].set_aspect("equal")
ax[1,1].set_axis_off()
ax[1,1].set_title("Ca")
ax[1,1].xaxis.set_visible(False)
ax[1,1].yaxis.set_visible(False)
ax[1,1].imshow(loader.load_edsmap("Ca").map,
          cmap=LinearSegmentedColormap("blue", cdict_blue))
fig.tight_layout()
plt.savefig("components.png")

# Plot the composite
fig, ax = plt.subplots()

ax.set_aspect("equal")
ax.imshow(composite.map)
ax.set_axis_off()
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
fig.tight_layout()
plt.imsave('composite.png', composite.map)


# Segmentation
nb_points = 5000
compactness = 1.0
segmented = SlicSegmenter(compactness, nb_points).apply(composite)

# Plot segmentation
fig, ax = plt.subplots()
ax.set_axis_off()
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
segmcolors = label2rgb(segmented.labels, colors=segmented.get_color_labels())
ax.imshow(segmcolors)
fig.tight_layout()
plt.imsave('segmented.png', segmcolors)


# The points
stack = loader.load_stack(["Fe", "Si", "Ca"])
points = points_from_segmentation(stack, segmented)


fig, ax = plt.subplots()
ax.plot(points["Fe"]/points["Si"],points["Si"]/points["Ca"],".",color="#555555")
ax.set_xlim([0,1])
ax.set_ylim([0,0.8])
ax.set_xlabel("Fe/Si")
ax.set_ylabel("Si/Ca")
ax.minorticks_on()
ax.tick_params("x", which="both", bottom="True", top="True")
ax.tick_params("y", which="both", left="True", right="True")
plt.savefig("ratio_plots.png")