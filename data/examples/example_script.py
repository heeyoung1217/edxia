#!/usr/bin/env python3
#
# Copyright (c) 2021 Fabien Georget <fabien.georget@epfl.ch>, EPFL
# Copyright (c) 2021 Fabien Georget <georget@ibac.rwth-aachen.de>, EPFL
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os.path

import numpy as np

from skimage.filters.rank import maximum, minimum
from skimage.morphology import disk
from skimage import segmentation
from skimage.color import gray2rgb
from skimage.util import img_as_ubyte

from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

from edxia.composite import CompositeChannels
from edxia.composite.segmentation import SlicSegmenter
from edxia.io.loader import PickleLoader
from edxia.io.raw_io import aztec_ascii_map_format, aztec_ascii_bse_format,\
                            imagej_ascii_bse_format,\
                            esprit_ascii_bse_format, esprit_ascii_map_format
from edxia.core import Map
from edxia.core.experiment import MappingExperiment
from edxia.point_analysis.points import points_from_segmentation
from edxia.filters.denoise import DenoiseFilter


"""This module is a simple example of automated script using edxia.


How to use:
-----------

1) Change the data_path variable to point to the folder where your map is stored
2) Change the pattern to match thename of your hypermap
3) Change label and description
3) Change the bse_format and map_format if needed
4) Select DRAW_PLOT or START_GLUE OPTION
5) Adapt the script as needed
"""

DRAW_PLOT = True # True if in plotting mode, False to start Glue
START_GLUE = not DRAW_PLOT #True

# define the map
# --------------
data_path = "../example_map_1/"
pattern = os.path.join(data_path, "map_short_atom_{component}.txt")
exp = MappingExperiment(pattern, label="example",
                        description="An example",
                        bse_format=imagej_ascii_bse_format,
                        map_format=esprit_ascii_map_format
                        )
loader = PickleLoader(exp, filters=[DenoiseFilter(0.1),])


# Create the composite
# --------------------
channels = CompositeChannels(["Fe", "Si", "Ca"], [3, 4, 2])
composite = loader.load_composite(channels)
bse = loader.load_edsmap("BSE")
composite.mix_with_bse(bse, 0.6)
composite.map[bse.map<0.2,:] = 0
# segmentation_labels = SlicSegmenter(0.01, 20000).apply(composite)


# BSE and segmentation of the BSE
# -------------------------------
image = minimum(maximum(img_as_ubyte(bse.map), disk(3)), disk(3))
bse_filter = Map("BSE", image, exp)

segmentation_labels = SlicSegmenter(0.1, 6000, channel_axis=None).apply(bse_filter)



# Create map stack
# ----------------
extras = {}
stack = loader.load_stack()
# only activate the next two lines if map is in unit of mass
# extras["SOX"] = stack.sum_of_oxides_from_mass()
# stack.to_atomic(copy=False)

# load representative points
# --------------------------
pts = points_from_segmentation(stack, segmentation_labels, mask_img=composite.map, include_rc=False, include_yx=False)

# Decomposition
# -------------
decomp = PCA(5)
pca_point_res = decomp.fit_transform(pts.df)

flat = stack.flatten()
pca_stack_res = decomp.transform(flat)


# Clustering
# ----------
nc  = 15 # number of components
model = GaussianMixture(n_components=nc)
gm_point_labels = model.fit_predict(pca_point_res)
gm_stack_labels = model.predict(pca_stack_res)


# Plots
# -----
if DRAW_PLOT:
    import matplotlib.pyplot as plt

    # Example plots
    fig1, [[ax1, ax2,], [ax3, ax8]] = plt.subplots(2, 2, constrained_layout=True)
    fig2, [[ax4, ax5,], [ax6, ax7]] = plt.subplots(2, 2, constrained_layout=True)

    ax1.imshow(bse.map, cmap=plt.cm.gray)
    ax2.imshow(segmentation.mark_boundaries(image, segmentation_labels.labels))
    ax3.imshow(composite.map)


    colors = np.zeros((len(pts.df), 3))
    colors[:,0] = np.clip(pts.df["Fe"]*5, 0, 1)
    colors[:,1] = np.clip(pts.df["Si"]*5, 0, 1)
    colors[:,2] = np.clip(pts.df["Ca"]*3, 0, 1)


    ax5.scatter(pca_point_res[:,0], pca_point_res[:,1], s=1, c=colors)
    ax5.set_xlabel("PCA0")
    ax5.set_ylabel("PCA1")


    ax6.scatter(pca_point_res[:,0], pca_point_res[:,2], s=1, c=colors)
    ax6.set_xlabel("PCA0")
    ax6.set_ylabel("PCA2")


    ax4.scatter(pts.df["Fe"]/pts.df["Si"], pts.df["Si"]/pts.df["Ca"], s=1, c=colors)
    ax4.set_xlim([0, 1])
    ax4.set_ylim([0, 1])

    ax4.set_xlabel("Fe/Si")
    ax4.set_ylabel("Si/Ca")

    colors_gm = np.zeros((len(pts.df), 3))
    for i in range(nc):
        si = pts.df["Fe"][gm_point_labels == i].median()
        al = pts.df["Si"][gm_point_labels == i].median()
        ca = pts.df["Ca"][gm_point_labels == i].median()

        colors_gm[gm_point_labels == i, 0] = min(si*5, 1)
        colors_gm[gm_point_labels == i, 1] = min(al*5, 1)
        colors_gm[gm_point_labels == i, 2] = min(ca*3, 1)


    ax7.scatter(pca_point_res[:,0], pca_point_res[:,1], s=1, c=colors_gm)
    ax7.set_xlabel("PCA0")
    ax7.set_ylabel("PCA1")
    #

    images = np.zeros((bse.map.shape[0], bse.map.shape[1], 3))

    image_labels = stack.reshape(gm_stack_labels)

    for i in range(nc):
        si = pts.df["Fe"][gm_point_labels == i].median()
        al = pts.df["Si"][gm_point_labels == i].median()
        ca = pts.df["Ca"][gm_point_labels == i].median()

        images[image_labels == i, 0] = min(si*5, 1)
        images[image_labels == i, 1] = min(al*5, 1)
        images[image_labels == i, 2] = min(ca*3, 1)

    toshow = gray2rgb(bse.map)*0.3+images*0.7
    toshow[bse.map<0.2,:] = 0
    ax8.imshow(toshow)

    ax1.set_title("a) BSE")
    ax2.set_title("b) BSE segmentation")
    ax3.set_title("c) Composite")
    ax8.set_title("d) Colors from clustering")

    ax4.set_title("a) Ratio plot")
    ax5.set_title("b) PCA - point colors")
    ax6.set_title("c) PCA - point colors")
    ax7.set_title("d) PCA - cluster colors")

    fig1.savefig("bse_composite.png", dpi=300)
    fig2.savefig("points.png", dpi=300)

    plt.show()

if START_GLUE:
    from glue.app.qt.application import GlueApplication
    from glue.core import DataCollection
    from glue.core.subset import ElementSubsetState
    from glue.core.component_link import ComponentLink
    from edxia.glue import gluedata_from_points, gluedata_from_stack_and_composite
    from edxia.glue.qt.linker import component_linker

    from matplotlib.colors import to_hex


    for i in range(8):
        extras["PCA{0}".format(i)] = stack.reshape(pca_stack_res[:,i])

    # Start glue
    pts = points_from_segmentation(stack, segmentation_labels, mask_img=composite.map, extras=extras)

    pts_data = gluedata_from_points("points", pts)
    stack_data = gluedata_from_stack_and_composite("maps", stack, composite, extras=extras)
    dc = DataCollection([pts_data, stack_data])

    for i in range(nc):
        si = pts.df["Fe"][gm_point_labels == i].median()
        al = pts.df["Si"][gm_point_labels == i].median()
        ca = pts.df["Ca"][gm_point_labels == i].median()

        gm_point_state = ElementSubsetState(np.asarray(gm_point_labels == i), pts_data)
        sub = dc.new_subset_group("GM point subset {0}".format(i), gm_point_state)
        sub.style.color = to_hex((min(si, 1.0)*5, min(al, 1.0)*5, min(ca, 1.0)*3))

        image_label = stack.reshape(gm_stack_labels)
        image_label = np.flipud(image_label)

        gm_stack_state = ElementSubsetState(np.asarray(image_label.ravel() == i), stack_data)
        sub = dc.new_subset_group("GM stack subset {0}".format(i), gm_stack_state)
        sub.style.color = to_hex((min(si, 1.0)*5, min(al, 1.0)*5, min(ca, 1.0)*3))

    link_y = ComponentLink([pts_data.id['y'],], stack_data.id['Pixel Axis 0 [y]'])
    link_x = ComponentLink([pts_data.id['x'],], stack_data.id['Pixel Axis 1 [x]'])

    ga = GlueApplication(dc)
    component_linker(ga.session, ga.data_collection)
    dc.add_link([link_y, link_x])

    ga.start()


