from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo


class UIFreeCAD_ObjectNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIFreeCAD_ObjectNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Node Action X34")
#        actionAddOut.setData(NodeActionButtonInfo('../icons/EE.svg'))
        actionAddOut.setToolTip("Adds output execution pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onAddOutPin(self):
        print ("Action done")


    @property
    def name(self):
        return self._rawNode.name +"@FreeCAD"
