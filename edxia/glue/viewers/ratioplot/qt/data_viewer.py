from glue.utils import defer_draw, decorate_all_methods
from glue.viewers.matplotlib.qt.data_viewer import MatplotlibDataViewer
from glue.viewers.scatter.qt.layer_style_editor import ScatterLayerStyleEditor
from glue.viewers.scatter.layer_artist import ScatterLayerArtist
from glue.viewers.scatter.qt.options_widget import ScatterOptionsWidget
from glue.viewers.scatter.state import ScatterViewerState

from edxia.glue.viewers.ratioplot.viewer import MatplotlibRatioMixin
from edxia.glue.viewers.ratioplot.layer_artist import RatioMixtureLayerArtist
from edxia.glue.viewers.ratioplot.qt.layer_style_editor_mixture import RatioLayerMixtureStyleEditor



__all__ = ['RatioPlotViewer']

@decorate_all_methods(defer_draw)
class RatioPlotViewer(MatplotlibRatioMixin, MatplotlibDataViewer):

    LABEL = 'Ratios plot'
    _layer_style_widget_cls = {ScatterLayerArtist: ScatterLayerStyleEditor,
                               RatioMixtureLayerArtist: RatioLayerMixtureStyleEditor}
    _state_cls = ScatterViewerState
    _options_cls = ScatterOptionsWidget
    #_data_artist_cls = ScatterLayerArtist # not set
    # override _get_data_layer_atist instead
    _subset_artist_cls = ScatterLayerArtist

    allow_duplicate_data = True

    tools = ['select:rectangle', 'select:xrange',
            'select:yrange', 'select:circle',
            'select:polygon',
            'phases:select']

    def __init__(self, session, parent=None, state=None):
        MatplotlibDataViewer.__init__(self, session, parent=parent, state=state)
        MatplotlibRatioMixin.setup_callbacks(self)
