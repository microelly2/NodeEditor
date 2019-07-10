import FreeCAD,FreeCADGui
from PythonObjects import FeaturePython,ViewProvider
import pfwrap
from nodeeditor.say import *

def _PyFlowGraph(FeaturePython):

	def __init__(self,obj):
		FeaturePython.__init__(self, obj)
		obj.Proxy = self
		self.Type = self.__class__.__name__


class _PyFlowGraphViewProvider(ViewProvider):

	def recompute(self):
		obj=self.Object
		say("Recompute ",obj.Label)
		instance=pfwrap.getInstance()
		instance.graphManager.get().clear()
		a=PyFlowGraph()
		data=eval(a.graph)
		instance.loadFromData(data)
		pfwrap.getInstance().show()

	def setupContextMenu(self, obj, menu):

		action = menu.addAction("load and show Graph ...")
		action.triggered.connect(self.recompute)

		action = menu.addAction("show PyFlow ...")
		action.triggered.connect(self.showPyFlow)

		action = menu.addAction("hide PyFlow ...")
		action.triggered.connect(self.hidePyFlow)

		action = menu.addAction("clear Graph ...")
		action.triggered.connect(self.clearGraph)


	def hidePyFlow(self):
		pfwrap.deleteInstance()

	def showPyFlow(self):
		try:
			FreeCAD.PF.hide()
		except:
			pass
		pfwrap.getInstance().show()

	def clearGraph(self):
		instance=pfwrap.getInstance()
		instance.graphManager.get().clear()


	def setEdit(self,vobj,mode=0):
		say("set edit deactivated")
		self.recompute()
		return False

# anwendungsklassen 

def PyFlowGraph():

	name="PyFlowGraph"
	obj = FreeCAD.ActiveDocument.getObject(name)
	if obj == None:
		#obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
		obj=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
		obj.addProperty("App::PropertyString", "graph", "Data","serialized data of the flow graph")
		_PyFlowGraph(obj)
		_PyFlowGraphViewProvider(obj.ViewObject,'/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/icons/BB.svg')

	return obj

