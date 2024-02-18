import os

from qtpy import QtWidgets

from echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui

__all__ = ["RatioLayerMixtureStyleEditor"]


class RatioLayerMixtureStyleEditor(QtWidgets.QWidget):

    def __init__(self, layer, parent=None):

        super(RatioLayerMixtureStyleEditor, self).__init__(parent=parent)

        self.ui = load_ui('layer_style_editor_mixture.ui', self,
                          directory=os.path.dirname(__file__))

        connect_kwargs = {'alpha': dict(value_range=(0, 1)),}
        self._connections = autoconnect_callbacks_to_qt(layer.state, self.ui, connect_kwargs)