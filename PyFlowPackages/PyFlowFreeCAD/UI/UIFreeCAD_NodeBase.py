from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo

from nodeeditor.say import *

import os
RESOURCES_DIR=os.path.dirname(__file__)

class FreeCADUINodeBase(UINodeBase):


	def __init__(self,*args,**kargs):
		super(FreeCADUINodeBase, self).__init__(*args, **kargs)
		self.addActions()

	def addActions(self):
		say("add the FreeCAD special actions")

		say("!con",RESOURCES_DIR + "/pin.svg")
		
		actionAddOut2 = self._menu.addAction("show node")

		actionAddOut2.setData(NodeActionButtonInfo(RESOURCES_DIR + "/show.svg"))
		actionAddOut2.setToolTip("tipp for pins")
		actionAddOut2.triggered.connect(self.f2)

		actionAddOut3 = self._menu.addAction("compute node")
		actionAddOut3.setData(NodeActionButtonInfo(RESOURCES_DIR + "/compute.svg"))
		actionAddOut3.setToolTip("tipp for moda")
		actionAddOut3.triggered.connect(self.f3)

		actionAddOut4 = self._menu.addAction("f4")
		actionAddOut4.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
		actionAddOut4.triggered.connect(self.f4)

		actionAddOut4 = self._menu.addAction("visualize")
		#actionAddOut4.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
		actionAddOut4.triggered.connect(self.visualize)


	def f2(self):
		self._rawNode.show()

	def f3(self):
		self._rawNode.compute()

	def f4(self):
		sayl()
		self._rawNode.refresh()

	def visualize(self):
		sayl()
		import nodeeditor.dev
		reload (nodeeditor.dev)
		return  nodeeditor.dev.run_visualize(self)





class FreeCADUIFunctionBase(UINodeBase):


	def __init__(self,*args,**kargs):
		super(FreeCADUIFunctionBase, self).__init__(*args, **kargs)
		self.addActions()

	def addActions(self):
		say("add the FreeCAD special actions")

		say("!con",RESOURCES_DIR + "/pin.svg")

		actionAddOut2 = self._menu.addAction("show node")

		actionAddOut2.setData(NodeActionButtonInfo(RESOURCES_DIR + "/show.svg"))
		actionAddOut2.setToolTip("tipp for pins")
		actionAddOut2.triggered.connect(self.f2)


		actionAddOut3 = self._menu.addAction("compute node")
		actionAddOut3.setData(NodeActionButtonInfo(RESOURCES_DIR + "/compute.svg"))
		actionAddOut3.setToolTip("tipp for moda")
		actionAddOut3.triggered.connect(self.f3)




	def f3(self):
		self._rawNode.compute()

	def f2(self):
		sayl()
		say(self._rawNode)
