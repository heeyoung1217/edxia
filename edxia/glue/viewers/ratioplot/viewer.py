from glue.viewers.scatter.viewer import MatplotlibScatterMixin
from glue.viewers.scatter.layer_artist import ScatterLayerArtist

from edxia.glue.viewers.ratioplot.layer_artist import RatioMixtureLayerArtist
class MatplotlibRatioMixin(MatplotlibScatterMixin):

    def get_data_layer_artist(self, layer=None, layer_state=None):
        if hasattr(layer, "meta") and layer.meta.get("is_phase_data", False):
            cls = RatioMixtureLayerArtist
        else:
            cls = ScatterLayerArtist
        return self.get_layer_artist(cls, layer=layer, layer_state=layer_state)

