from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *



from FreeCAD import Vector
import FreeCAD
import Part



# example shape
def createShape(a):

	pa=FreeCAD.Vector(0,0,0)
	pb=FreeCAD.Vector(a*50,0,0)
	pc=FreeCAD.Vector(0,50,0)
	shape=Part.makePolygon([pa,pb,pc,pa])
	return shape


def updatePart(name,shape):

	FreeCAD.Console.PrintError("update Shape for "+name+"\n")
	a=FreeCAD.ActiveDocument.getObject(name)
	if a== None:
		a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
	a.Shape=shape



def onBeforeChange_example(self,newData,*args, **kwargs):
	FreeCAD.Console.PrintError("before:"+str(self)+"\n")
	FreeCAD.Console.PrintError("data before:"+str(self.getData())+"-- > will change to:"+str(newData) +"\n")
	# do something like backup or checks before change here

def onChanged_example(self,*args, **kwargs):
	FreeCAD.Console.PrintError("Changed data to:"+str(self.getData()) +"\n")
	self.owningNode().reshape()


class FreeCAD_Placement(NodeBase):

	def __init__(self, name):

		super(FreeCAD_Placement, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.pa = self.createInputPin('Placement_Base', 'VectorPin')
		self.pb = self.createInputPin('Rotation_Axis', 'VectorPin')
		self.pc = self.createInputPin('Rotation_Angle', 'FloatPin')

		self.pc.onChanged=onChanged_example
		self.pc.onBeforeChange=onBeforeChange_example

		self.vobjname = self.createInputPin("objectname", 'StringPin')
		self.vobjname.setData(name)

		self.Shape="DAS IST SHAPE"
		self.pa.recomputeNode=True
		self.pb.recomputeNode=True
		self.pc.recomputeNode=True


	def reshape(self, *args, **kwargs):
		FreeCAD.Console.PrintError("try reshape ..\n")
		self.Shape=createShape(self.pc.getData())
		updatePart(self.getName(),self.Shape)
		FreeCAD.Console.PrintError("reshaped "+self.getName()+"\n")



	@staticmethod
	def pinTypeHints():
		return {'inputs': ['FloatPin','FloatPin','FloatPin','FloatPin','StringPin'], 'outputs': []}


	@staticmethod
	def category():
		return 'Placement'

	@staticmethod
	def keywords():
		return ['freecad']

	@staticmethod
	def description():
		return "change Placement of the FreeCAD object"

	def compute(self, *args, **kwargs):

		# change the placement of Box example
		c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())
		c.Placement.Base=10*self.pa.getData()
		c.Placement.Rotation.Angle=100*self.pc.getData()
		self.outExec.call()
