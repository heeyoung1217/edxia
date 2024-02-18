from glue.viewers.matplotlib.state import (MatplotlibDataViewerState,
                                           MatplotlibLayerState,
                                           DeferredDrawCallbackProperty as DDCProperty,
                                           DeferredDrawSelectionCallbackProperty as DDSCProperty)

__all__ = ["RatioPlotMixtureLayerState"]

class RatioPlotMixtureLayerState(MatplotlibLayerState):

    phase1 = DDSCProperty(docstring="The first phase of the mixture line")
    phase2 = DDSCProperty(docstring="The second phase of the mixture line")

    linewidth = DDCProperty(1, docstring="The line width")
    markersize = DDCProperty(3, docstring="The marker size")
    alpha = DDCProperty(1.0, docstring="The transparency of the layer")

    def __init__(self, viewer_state=None, layer=None):
        if layer is None:
            raise ValueError("phase dict need to be defined")

        self.set_phase_choices(layer)

        super().__init__(viewer_state=viewer_state, layer=layer)


        self._sync_color.disable_syncing()
        self._sync_alpha.disable_syncing()


        self.linewidth = layer.style.markersize
        self.markersize = layer.style.markersize+1
        self.alpha = 1.0


    def set_phase_choices(self, phase_dict):
        phases = phase_dict["phase"]
        phase_list = [phases[i] for i in range(phase_dict.size) if phases[i]]
        RatioPlotMixtureLayerState.phase1.set_choices(self, phase_list)
        RatioPlotMixtureLayerState.phase2.set_choices(self, phase_list)
