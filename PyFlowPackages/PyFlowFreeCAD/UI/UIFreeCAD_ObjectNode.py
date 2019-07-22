from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo

from PyFlow.Packages.PyFlowFreeCAD.UI.UIFreeCAD_NodeBase import FreeCADUINodeBase

class UIFreeCAD_ObjectNode(FreeCADUINodeBase):
	def __init__(self, raw_node):
		super(UIFreeCAD_ObjectNode, self).__init__(raw_node)
		actionAddOut = self._menu.addAction("!! create Pins for Properties of the FreeCAD object")
#		actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
		actionAddOut.setToolTip("Adds property pins")
		actionAddOut.triggered.connect(self.onAddPins)


	def onAddPins(self):
		rawPins=self._rawNode.createPins(self)
		for rawPin in rawPins:
			uiPin = self._createUIPinWrapper(rawPin)
			uiPin.setDisplayName("{0}".format(rawPin.name))
		return 1



	@property
	def name(self):
		return self._rawNode.name 
