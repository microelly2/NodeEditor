from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

from nodeeditor.say import *

from FreeCAD import Vector
import FreeCAD
import Part

import nodeeditor.store as store
import numpy as np



# exmaple shape
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


class FreeCAD_Object(NodeBase):

	def __init__(self, name):

		super(FreeCAD_Object, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.obj = self.createOutputPin('Object', 'FCobjPin')
		self.obja = self.createInputPin('ObjectA', 'FCobjPin')
		self.shapeout = self.createOutputPin('Shape_out', 'FCobjPin')
		self.shapein = self.createInputPin('Shape_in', 'FCobjPin')

		if 0:
			self.arrout = self.createOutputPin('Array_out', 'FCobjPin')
			self.arrin = self.createInputPin('Array_in', 'FCobjPin')
		else:
			self.arrout = self.createOutputPin('Array_out', 'ArrayPin')
			self.arrin = self.createInputPin('Array_in', 'ArrayPin')

		self.vobjname = self.createInputPin("objectname", 'StringPin')
		self.vobjname.setData(name)

	def getObject(self,*args):
		say("getobject")
		return self
	pass


	@staticmethod
	def pinTypeHints():
		return {'inputs': ['FloatPin','FloatPin','FloatPin','FloatPin','StringPin'], 'outputs': []}


	@staticmethod
	def category():
		return 'DefaultLib'

	@staticmethod
	def keywords():
		return ['freecad']

	@staticmethod
	def description():
		return "change Placement of the FreeCAD object"

	def compute(self, *args, **kwargs):

		say ("in compute",self.getName(),"objname is",self.vobjname.getData())
		say("#----------------------------------------############################")
		say("#----------------------------------------############################")

		ss=self.arrin.getArray()
		say("getArray",ss)

		# array erzeugen und  senden
		say("connected?",self.arrout.hasConnections())
		if 1 or self.arrout.hasConnections():

				varr=np.round(np.random.random((3,4)),2)
				say("store ",varr)
				store.store().add(str(self.arrout.uid),varr)
				self.arrout.setData(str(self.arrout.uid))
		say ("array done ok")
		say("#----------------------------------------############################")
		say("#----------------------------------------############################")


		say ("get shapein")
		shapein=self.shapein.getData()
		
		if shapein <> None:
			say("shapein",shapein)
			s=store.store().get(shapein)
			
			#
			say("s:::::::",s)
			if s <>  None:
				say("!!!!!!!!!!!!!!!!!!!!show")
				#Part.show(s)

			#store.store().dela(shapein)
			store.store().list()


		try:
			say ("try get object")
			c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())
			say ("ok",c,c.Name)
		except:
			say ("nothing found")
			c=None

		# use the input object
		if self.obja.getData() == None:
			say( "no input object")
			c = None
		else:
			c=FreeCAD.ActiveDocument.getObject(self.obja.getData())
			


		# if this is not possible fall back to the given name for the obj
		if c== None:
			c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())


		say("!!",self.uid)
		say(str(self.uid))
		yid="ID_"+str(self.uid)
		yid=yid.replace('-','_')
		say(str(self.uid).replace('-','_'))

		if 1 or c==None:
			cc=FreeCAD.ActiveDocument.getObject(yid)

		if cc == None:
			cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
		say("created",cc.Name,yid)


		print("input object from pin",self.obja,"getData ..",self.obja.getData())

		if shapein <> None:
			say("shapein",shapein)
			s=store.store().get(shapein)
			
			#
			say("s:::::::",s)
			if s <>  None:
				say("!!!!!!!!!!!!!!!!!!!!show")
				#Part.show(s)

			#store.store().dela(shapein)
			store.store().list()

			if s <> None:
					say("!!!!!!!!!!!!!!!!!!!!show")
					cc.Shape=s


		if c == None:
			self.obj.setData(None)
		else:
			s=c
			self.obj.setData(c.Name)
			say("[send key{0} from {1}@{2}]".format(self.shapeout.uid,self.shapeout.getName(),self.getName()))
		#	say("sended obj",self.shapeout.uid,self.shapeout.getName(),self.getName())
		#	store.store().addid(c)
			say("add to store shape",s,self.shapeout.uid)
			say("connected?",self.shapeout.hasConnections())
			if self.shapeout.hasConnections():
				store.store().add(str(self.shapeout.uid),s.Shape)
				self.shapeout.setData(self.shapeout.uid)

		say ("data set to output object is done, exex...")
		self.outExec.call()
		say ("Ende exec for ---",self.getName())




class FreeCAD_Toy(NodeBase):
	'''erzeuge eine zufallsBox'''

	def __init__(self, name="MyToy"):

		super(FreeCAD_Toy, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
		self.part = self.createOutputPin('Part', 'FCobjPin')
		self.objname = self.createInputPin("objectname", 'StringPin')
		self.randomize = self.createInputPin("randomize", 'BoolPin')
		name="MyToy"
		self.objname.setData(name)

	def compute(self, *args, **kwargs):

		say ("in compute",self.getName(),"objname is",self.objname.getData())

		yid="ID_"+str(self.uid)
		yid=yid.replace('-','_')
		say(str(self.uid).replace('-','_'))

		cc=FreeCAD.ActiveDocument.getObject(yid)

		if cc == None:
			cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)

			say("created",cc.Name,yid)

		cc.Label=self.objname.getData()

		import Part
		import random
		
		f=30 if self.randomize.getData() else 0
		shape=Part.makeBox(10+f*random.random(),10+f*random.random(),10+f*random.random())
		cc.Shape=shape

		if self.part.hasConnections():
			say("sende an Part")
			if cc == None:
				self.part.setData(None)
			else:
				self.part.setData(cc.Name)
		say ("data set to output object is done, exex...")
		self.outExec.call()
		say ("Ende exec for ---",self.getName())



	
class FreeCadNodeBase(NodeBase):
	'''common methods for FreeCAD integration'''

	def __init__(self, name="FreeCADNode"):

		super(FreeCadNodeBase, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.part = self.createOutputPin('Part', 'FCobjPin')
		self.shapeout = self.createOutputPin('Shape', 'FCobjPin')

		self.objname = self.createInputPin("objectname", 'StringPin')

		self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin')
		self.randomize = self.createInputPin("randomize", 'BoolPin')

		self.objname.setData(name)



	def getDatalist(self,pinnames):
		namelist=pinnames.split()
		ll=[self.getPinN(a).getData() for a in namelist]
		return ll

	def applyPins(self,ff,zz):
		zz2=self.getDatalist(zz)
		return ff(*zz2)

	def setDatalist(self,pinnames,values):
		namelist=pinnames.split()
		say("set pinlist")
		for a,v in zip(namelist,values):
			say(a,v)
			self.getPinN(a).setData(v)

	def getObject(self):
		'''get the FreeCAD object'''

		yid="ID_"+str(self.uid)
		yid=yid.replace('-','_')

		cc=FreeCAD.ActiveDocument.getObject(yid)
		if cc == None:
			cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
		return cc

	def postCompute(self,fcobj=None):

		if self.part.hasConnections():
			say("sende an Part")
			if fcobj == None:
				self.part.setData(None)
			else:
				self.part.setData(fcobj.Name)
		self.outExec.call()
#		import FreeCADGui
#		FreeCADGui.SendMsgToActiveView("ViewFit")







class FreeCAD_Box( FreeCadNodeBase):
	'''erzeuge einer Part.Box'''

	def __init__(self, name="MyBox"):

		super(FreeCAD_Box, self).__init__(name)

		self.length = self.createInputPin("length", 'FloatPin')
		self.width = self.createInputPin("width", 'FloatPin')
		self.height = self.createInputPin("height", 'FloatPin')
		self.position = self.createInputPin("position", 'VectorPin')
		self.direction = self.createInputPin("direction", 'VectorPin')

		self.objname.setData(name)

		self.setDatalist("length width height position direction",
			[10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0)])

		self.length.recomputeNode=True
		self.width.recomputeNode=True
		self.height.recomputeNode=True

	def compute(self, *args, **kwargs):

		shape=self.applyPins(Part.makeBox,"length width height position direction")

		if self.shapeout.hasConnections():
			store.store().add(str(self.shapeout.uid),shape)
			self.shapeout.setData(str(self.shapeout.uid))

		if self.shapeOnly.getData():
			self.postCompute()
		else:
			cc=self.getObject()
			cc.Label=self.objname.getData()
			cc.Shape=shape
			self.postCompute(cc)










class FreeCAD_Cone(FreeCadNodeBase):
	'''erzeuge einer Part.Kegel'''

	def __init__(self, name="MyCone"):

		super(FreeCAD_Cone, self).__init__(name)

		self.radius1 = self.createInputPin("radius1", 'FloatPin')
		self.radius2 = self.createInputPin("radius2", 'FloatPin')
		self.height = self.createInputPin("height", 'FloatPin')
		self.position = self.createInputPin("position", 'VectorPin')
		self.direction = self.createInputPin("direction", 'VectorPin')
		self.angle = self.createInputPin("angle", 'FloatPin')


		say("call init",self)
		self.setDatalist("radius1 radius2 height position direction angle",
			[10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),360])

		self.radius1.recomputeNode=True
		self.radius2.recomputeNode=True
		self.height.recomputeNode=True

	def compute(self, *args, **kwargs):

		shape=self.applyPins(Part.makeCone,"radius1 radius2 height position direction angle")
#		say("compute",self.getName())


		if self.shapeout.hasConnections():
			#say("add to store shape",shape,self.shapeout.uid)
			store.store().add(str(self.shapeout.uid),shape)
			self.shapeout.setData(str(self.shapeout.uid))
			self.postCompute()

		if self.shapeOnly.getData():
			self.postCompute()
		else:
			cc=self.getObject()
			cc.Label=self.objname.getData()
			cc.Shape=shape
			self.postCompute(cc)


class FreeCAD_Sphere(FreeCadNodeBase):
	'''erzeuge einer Part.Kurgel'''

	def __init__(self, name="MySphere"):

		super(FreeCAD_Sphere, self).__init__(name)

		self.radius = self.createInputPin("radius", 'FloatPin')
		self.position = self.createInputPin("position", 'VectorPin')
		self.direction = self.createInputPin("direction", 'VectorPin')
		self.angle1 = self.createInputPin("angle1", 'FloatPin')
		self.angle2 = self.createInputPin("angle2", 'FloatPin')
		self.angle3 = self.createInputPin("angle3", 'FloatPin')

		self.setDatalist("radius position direction angle1 angle2 angle3",
			[10,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90,90,360])

		self.radius.recomputeNode=True
		self.angle1.recomputeNode=True
		self.angle2.recomputeNode=True
		self.angle3.recomputeNode=True

	def compute(self, *args, **kwargs):

		shape=self.applyPins(Part.makeSphere,"radius position direction angle1 angle2 angle3")

		if self.shapeout.hasConnections():
			store.store().add(str(self.shapeout.uid),shape)
			self.shapeout.setData(str(self.shapeout.uid))
			self.postCompute()

		if self.shapeOnly.getData():
			self.postCompute()
		else:
			cc=self.getObject()
			cc.Label=self.objname.getData()
			cc.Shape=shape
			self.postCompute(cc)


class FreeCAD_Quadrangle(FreeCadNodeBase):
	'''erzeuge einer BSpline Flaeche'''

	def __init__(self, name="MyQuadrangle"):

		super(FreeCAD_Quadrangle, self).__init__(name)

		self.vA = self.createInputPin("vecA", 'VectorPin')
		self.vB = self.createInputPin("vecB", 'VectorPin')
		self.vC = self.createInputPin("vecC", 'VectorPin')
		self.vD = self.createInputPin("vecD", 'VectorPin')

		self.setDatalist("vecA vecB vecC vecD",	[
						FreeCAD.Vector(0,0,0),
						FreeCAD.Vector(100,0,0),
						FreeCAD.Vector(100,200,40),
						FreeCAD.Vector(0,200,40),
					])

		self.vA.recomputeNode=True
		self.vB.recomputeNode=True
		self.vC.recomputeNode=True
		self.vD.recomputeNode=True

		self.Called=False


	def compute(self, *args, **kwargs):


		# recursion stopper
		if self.Called:
			return

		self.Called=True
		vA=self.vA.getData()
		vB=self.vB.getData()
		vC=self.vC.getData()
		vD=self.vD.getData()
		
		w=Part.BSplineSurface()
		w.buildFromPolesMultsKnots([[vA,vB],[vD,vC]],[2,2],[2,2],[0,1],[0,1],False,False,1,1)
		shape=w.toShape()

		if self.shapeout.hasConnections():
			store.store().add(str(self.shapeout.uid),shape)
			self.shapeout.setData(str(self.shapeout.uid))
			self.postCompute()

		if self.shapeOnly.getData():
			self.postCompute()
		else:
			cc=self.getObject()
			cc.Label=self.objname.getData()
			cc.Shape=shape
			self.postCompute(cc)

		self.Called=False








class FreeCAD_Bar(FreeCadNodeBase):
	'''boolean ops of two parts example'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_Bar, self).__init__(name)

		self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
		self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

		self.mode = self.createInputPin('mode', 'EnumerationPin')
		self.mode.values=["fuse","cut","common"]
		self.mode.setData("fuse")

		self.volume = self.createOutputPin('Volume', 'FloatPin')

		self.objname.setData(name)

	def compute(self, *args, **kwargs):

#		say ("in compute",self.getName(),"objname is",self.objname.getData())


		part1=self.part1.getData()
		part2=self.part2.getData()
		if part1 == None or part2 == None: 
			say("part12 is None, abort")
			return


		s1=store.store().get(part1)
		if not s1.__class__.__name__ =='Solid':
			part1=FreeCAD.ActiveDocument.getObject(part1)
			s1=part1.Shape

		s2=store.store().get(part2)
		if not s2.__class__.__name__ =='Solid':
			part2=FreeCAD.ActiveDocument.getObject(part2)
			s2=part2.Shape

		mode=self.mode.getData()
		if mode == 'common':
			shape=s1.common(s2)
		elif mode == 'cut':
			shape=s1.cut(s2)
		else:
			shape=s1.fuse(s2)


		if self.shapeOnly.getData():
			self.postCompute()
		else:
			cc=self.getObject()
			cc.Label=self.objname.getData()
			cc.Shape=shape
			self.postCompute(cc)



		if self.part.hasConnections():
			say("sende an Part")
			if cc == None:
				self.part.setData(None)
			else:
				self.part.setData(cc.Name)

		say("Volume for {0}: {1:.2f}".format(self.getName(),shape.Volume))
		self.volume.setData(shape.Volume)
#		say ("data set to output object is done, exex...")
		self.outExec.call()
#		say ("Ende exec for ---",self.getName())








class FreeCAD_Foo(FreeCadNodeBase):
	def __init__(self, name="Fusion"):
		super(FreeCAD_Foo, self).__init__(name)
		self.Arr_in = self.createInputPin('Array_in', 'ArrayPin')
		self.Arr_out = self.createOutputPin('Array_out', 'ArrayPin')


	def compute(self, *args, **kwargs):

		say("")
		say ("in compute",self.getName(),"objname is",self.objname.getData())

		ss=self.Arr_in.getArray()
		say("got Array",ss)


		varr=np.round(np.random.random((3,4)),2)
		say("store Array",varr)
		self.Arr_out.setArray(varr)

		self.postCompute()




def nodelist():
	return [FreeCAD_Foo,FreeCAD_Toy,FreeCAD_Bar,FreeCAD_Object,
		FreeCAD_Box,
		FreeCAD_Cone,
		FreeCAD_Sphere,
		FreeCAD_Quadrangle,

		]
