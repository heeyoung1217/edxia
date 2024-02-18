from glue.utils import defer_draw

from glue.viewers.matplotlib.layer_artist import MatplotlibLayerArtist
from edxia.glue.viewers.ratioplot.state import RatioPlotMixtureLayerState

import numpy as np

__all__ = ["RatioMixtureLayerArtist"]

class RatioMixtureLayerArtist(MatplotlibLayerArtist):
    _layer_state_cls = RatioPlotMixtureLayerState


    def __init__(self, axes, viewer_state, layer_state=None, layer=None):

        super(RatioMixtureLayerArtist, self).__init__(axes, viewer_state,
                                                 layer_state=layer_state, layer=layer)

        self.plot_artist = self.axes.plot([], [], solid_capstyle="round",
                                          linestyle="-",
                                          marker="o",
                                          linewidth=self.state.linewidth,
                                          markersize=self.state.markersize,
                                          alpha=self.state.alpha
                                          )[0]

        self.mpl_artists = [self.plot_artist, ]

        self._viewer_state.add_global_callback(self._update_scatter)
        self.state.add_global_callback(self._update_scatter)

    @defer_draw
    def _update_data(self):
        if self.state.visible:
            # find data
            x_att = self._viewer_state.x_att
            y_att = self._viewer_state.y_att

            index_1 = np.where(self.layer["phase"] == self.state.phase1)[0][0]
            index_2 = np.where(self.layer["phase"] == self.state.phase2)[0][0]

            xdata = [self.layer[x_att][index_1], self.layer[x_att][index_2]]
            ydata = [self.layer[y_att][index_1], self.layer[y_att][index_2]]

            self.plot_artist.set_data(xdata, ydata)

        else:
            self.plot_artist.set_data([], [])

    @defer_draw
    def _update_visual_attributes(self):
        self.plot_artist.set_linewidth(self.state.linewidth)
        self.plot_artist.set_color(self.state.color)
        self.plot_artist.set_markersize(self.state.markersize)
        self.plot_artist.set_alpha(self.state.alpha)

    @defer_draw
    def _update_scatter(self, **kwargs):

        if (self._viewer_state.x_att is None or
            self._viewer_state.y_att is None or
                self.state.layer is None):
            return

        self._update_data()
        self._update_visual_attributes()

    @defer_draw
    def update(self):
        self._update_scatter(force=True)
        self.redraw()

    def get_handle_legend(self):
        return None, None, None
