import qtpy.QtWidgets as qtw
from qtpy.QtCore import Qt

from glue.config import viewer_tool
from glue.viewers.common.tool import CheckableTool

__all__ = ["FindPhaseCoord",]

def display_coordinates(xatt, yatt, x, y):
    qmb = qtw.QMessageBox()
    qmb.setWindowTitle("Coordinates")
    qmb.setText("Selected point: {0}={1:.2f} - {2}={3:.2f}".format(xatt,x,yatt,y))
    qmb.setDetailedText("{0}={1}\n{2}={3}".format(xatt,x,yatt,y))
    qmb.setTextInteractionFlags(Qt.TextSelectableByMouse)
    qmb.resize(400, qmb.size().height())
    qmb.exec_()


@viewer_tool
class FindPhaseCoord(CheckableTool):

    icon = 'glue_crosshair'
    tool_id = 'phases:select'
    action_text = 'Read coordinates from the graph'
    tool_tip = 'Read coordinates from the graph'
    status_tip = 'Select a point on the graph to see the coordinates.'
    shortcut = 'E'

    def __init__(self, viewer):
        super(FindPhaseCoord, self).__init__(viewer)

        self.viewer = viewer
        self.canvas = self.viewer.figure.canvas
        self.cid = None

    def get_handler(self):
        def on_click(event):
            x, y = event.xdata, event.ydata
            xatt, yatt = self.viewer.state.x_att, self.viewer.state.y_att
            display_coordinates(xatt.label, yatt.label, x, y)
        return on_click

    def activate(self):
        self.cid = self.canvas.mpl_connect('button_press_event', self.get_handler())

    def deactivate(self):
        self.canvas.mpl_disconnect(self.cid)

    def close(self):
        pass

