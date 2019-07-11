from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo


class UIFreeCAD_PolygonNode(UINodeBase):
	def __init__(self, raw_node):
		super(UIFreeCAD_PolygonNode, self).__init__(raw_node)
		actionAddOut = self._menu.addAction("Add out pin")
		actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
		actionAddOut.setToolTip("Adds input vector pin")
		actionAddOut.triggered.connect(self.onAddOutPin)

	def onPinWasKilled(self, uiPin):
		pass
		index = 1
		uiPin.OnPinDeleted.disconnect(self.onPinWasKilled)
		pins = list(self.UIoutputs.values())
		pins.sort(key=lambda x: int(x._rawPin.name))
		for outPin in pins:
			outPin.setName(str(index), True)
			outPin.setDisplayName("Then {0}".format(index))
			index += 1

	def postCreate(self, jsonTemplate=None):
		super(UIFreeCAD_PolygonNode, self).postCreate(jsonTemplate)
		for outPin in self.UIinputs.values():
			outPin.setDisplayName("{0}".format(outPin._rawPin.name))
			outPin.OnPinDeleted.connect(self.onPinWasKilled)

	def onAddOutPin(self):
		rawPin = self._rawNode.createPin()
		uiPin = self._createUIPinWrapper(rawPin)
		uiPin.OnPinDeleted.connect(self.onPinWasKilled)
		uiPin.setDisplayName("{0}".format(rawPin.name))
		return uiPin
