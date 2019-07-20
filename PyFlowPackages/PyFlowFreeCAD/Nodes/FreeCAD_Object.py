from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

from nodeeditor.say import *

from FreeCAD import Vector
import FreeCAD
import Part

import nodeeditor.store as store
import numpy as np
import random



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


class FreeCAD_StorePins(NodeBase):
	'''
	testnode for store-pins
	'''

	def __init__(self, name):

		super(FreeCAD__StorePins, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.show = self.createInputPin('Show', 'ExecPin', None, self.show)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
		self.trace = self.createInputPin('trace', 'BoolPin')

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


	def show(self,*args, **kwargs):
		sayl("list all pins")
		

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
		#   say("sended obj",self.shapeout.uid,self.shapeout.getName(),self.getName())
		#   store.store().addid(c)
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


import functools
import time
import inspect

def timer(func):
	"""Print the runtime of the decorated function"""
	@functools.wraps(func)
	def wrapper_timer(*args, **kwargs):

		try :
				is_method   = inspect.getargspec(func)[0][0] == 'self'
		except :
				is_method   = False

		if is_method :
				name    = '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
		else :
				name    = '{}.{}'.format(fn.__module__, func.__name__)

		sayW("call '{}'".format(name))
		start_time = time.time()
		value = func(*args, **kwargs)
		end_time = time.time()
		run_time = end_time - start_time    # 3
		sayW("Finished method '{0}' in {1:.4f} secs".format(func.__name__,run_time))
		return value
	return wrapper_timer


class FreeCadNodeBase(NodeBase):
	'''common methods for FreeCAD integration'''

	def __init__(self, name="FreeCADNode"):

		super(FreeCadNodeBase, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
		self.Show = self.createInputPin('Show', 'ExecPin', None, self.show,group="debug")
		self.trace = self.createInputPin('trace', 'BoolPin',group="debug")

		self.part = self.createOutputPin('Part', 'FCobjPin')
		self.shapeout = self.createOutputPin('Shape', 'FCobjPin')

		self.objname = self.createInputPin("objectname", 'StringPin',group="config")

		self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin',group="config")
		self.randomize = self.createInputPin("randomize", 'BoolPin',group="config")
		self.shapeOnly.recomputeNode=True 
		self.objname.setData(name)

	@timer 
	def show(self,*args, **kwargs):
		sayl()
		#say("self:",self)
		say("Content of {}:".format(self.getName()))
		#say("list all pins !! siehe FreeCAD.ref")
		for t in self.getOrderedPins():
			say(t)
			n=t.__class__.__name__
			# spezialausgaben fuer objekte
			if n == 'ArrayPin':
				say(t.getArray())
			if n == 'FCobjPin':
				obj=t.getObject()
				if obj <> None :
					try:
						say("object: {} ({})".format(obj.Label,obj.Name))
					except:
						say(obj)
				
		FreeCAD.ref=self
		



	def getDatalist(self,pinnames):
		namelist=pinnames.split()
		ll=[self.getPinN(a).getData() for a in namelist]
		return ll

	def applyPins(self,ff,zz):
		zz2=self.getDatalist(zz)
		return ff(*zz2)

	def setDatalist(self,pinnames,values):
		namelist=pinnames.split()
		sayl("--set pinlist for {}".format(self.getName()))
		for a,v in zip(namelist,values):
			say(a,v)
			self.getPinN(a).setData(v)

	def getObject(self):
		'''get the FreeCAD object'''

		yid="ID_"+str(self.uid)
		yid=yid.replace('-','_')

		cc=FreeCAD.ActiveDocument.getObject(yid)

		if self.shapeOnly.getData():
			if cc:
				say("delete object")
				FreeCAD.ActiveDocument.removeObject(cc.Name)
			return None


		if cc == None:
			cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
			cc.ViewObject.Transparency=80
			cc.ViewObject.LineColor=(1.,0.,0.)
			cc.ViewObject.PointColor=(1.,1.,0.)
			cc.ViewObject.PointSize=10
			r=random.random()
			cc.ViewObject.ShapeColor=(0.,0.2+0.8*r,1.0-0.8*r)
		return cc

	def postCompute(self,fcobj=None):

		if self.part.hasConnections():
			say("sende an Part")
			if fcobj == None:
				self.part.setData(None)
			else:
				self.part.setData(fcobj.Name)
		self.outExec.call()
		if self.trace.getData():
			self.show()







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

	@timer
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
#       say("compute",self.getName())


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
	'''
	erzeuge einer BSpline Flaeche degree 1
	by 4 points
	'''

	def __init__(self, name="MyQuadrangle"):

		super(FreeCAD_Quadrangle, self).__init__(name)

		self.vA = self.createInputPin("vecA", 'VectorPin')
		self.vB = self.createInputPin("vecB", 'VectorPin')
		self.vC = self.createInputPin("vecC", 'VectorPin')
		self.vD = self.createInputPin("vecD", 'VectorPin')

		self.setDatalist("vecA vecB vecC vecD", [
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


from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class FreeCAD_Polygon(FreeCadNodeBase):
	'''
	erzeuge eines Streckenzugs
	for each point there is an input pin,
	input pins can be added frm context menue
	'''

	def __init__(self, name="MyQuadrangle"):

		super(FreeCAD_Polygon, self).__init__(name)

		self.vA = self.createInputPin("Vec1", 'VectorPin')
		self.vB = self.createInputPin("Vec2", 'VectorPin')

		self.setDatalist("Vec1 Vec2", [
						FreeCAD.Vector(-1,1,3),
						FreeCAD.Vector(1,-1,3),
					])

		self.vA.recomputeNode=True
		self.vB.recomputeNode=True

		self.Called=False
		self.count=2


	def createPin(self, *args, **kwargs):
		pps=self.getOrderedPins()
		last=pps[-1].getData()
		prev=pps[-2].getData()
		pinName = "Vec" + str(len(self.inputs) + -5)
		p = CreateRawPin(pinName, self, 'VectorPin', PinDirection.Input)
		p.enableOptions(PinOptions.Dynamic)
		p.recomputeNode=True
		p.setData(last+last-prev)
		self.count += 1
		pps=self.getOrderedPins()
		
		return p

	@timer 
	def compute(self, *args, **kwargs):

		# recursion stopper
		if self.Called:
			return

		self.Called=True
		
		pts=[]

		for t in self.getOrderedPins():
			n=t.__class__.__name__
			d=t.getData()
			if d.__class__.__name__ =='Vector':
				#if pts[-1] <> d:
					pts += [d]
	
		
		shape=Part.makePolygon(pts)

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


class FreeCAD_Polygon2(FreeCadNodeBase):
	'''
	erzeuge eines Streckenzugs
	input pin for a list of vectors
	'''

	def __init__(self, name="MyQuadrangle"):

		super(FreeCAD_Polygon2, self).__init__(name)

		self.points = self.createInputPin('points', 'VectorPin',[], structure=PinStructure.Multi)
		self.points.setData([FreeCAD.Vector(0,0,0),FreeCAD.Vector(10,0,0)])


		self.Called=False
		self.count=2


	@timer 
	def compute(self, *args, **kwargs):

		# recursion stopper
		if self.Called:
			return
		sayl()
		# mit zeitstemple aktivieren
		#self.Called=True
		
		pts=self.points.getData()
		if len(pts)<2:
			sayW("zu wenig points")
		else:
			shape=Part.makePolygon(pts)

			if self.shapeout.hasConnections():
				store.store().add(str(self.shapeout.uid),shape)
				self.shapeout.setData(str(self.shapeout.uid))
				self.postCompute()

			if self.shapeOnly.getData():
				cc=self.getObject()
				self.postCompute()
			else:
				cc=self.getObject()
				if cc <> None:
					cc.Label=self.objname.getData()
					cc.Shape=shape
					self.postCompute(cc)

		#self.Called=False


class FreeCAD_Boolean(FreeCadNodeBase):
	'''boolean ops of two parts example'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_Boolean, self).__init__(name)

		self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
		self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

		self.mode = self.createInputPin('mode', 'EnumerationPin')
		self.mode.values=["fuse","cut","common"]
		self.mode.setData("fuse")

		self.volume = self.createOutputPin('Volume', 'FloatPin')

		self.objname.setData(name)

	@timer
	def compute(self, *args, **kwargs):

#       say ("in compute",self.getName(),"objname is",self.objname.getData())


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
#       say ("data set to output object is done, exex...")
		self.outExec.call()
#       say ("Ende exec for ---",self.getName())








class FreeCAD_Array(FreeCadNodeBase):
	'''
	test node for large arrays
	
	
	'''
	def __init__(self, name="Fusion"):
		super(FreeCAD_Array, self).__init__(name)
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


class FreeCAD_BSpline(FreeCadNodeBase):
	'''Bspline Surface'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_BSpline, self).__init__(name)
		self.arrayData = self.createInputPin('poles', 'AnyPin', structure=PinStructure.Array, constraint="1")
		self.createInputPin('maxDegreeU', 'IntPin', 3)
		self.createInputPin('maxDegreeV', 'IntPin', 3)
		self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
		self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)



	@timer 
	def compute(self, *args, **kwargs):

		say("")
		say ("in compute",self.getName(),"objname is",self.objname.getData())
		dat=self.arrayData.getData()
		dat=np.array(dat)
		say("dat shape",dat.shape)

		import nodeeditor.dev
		reload (nodeeditor.dev)
		return  nodeeditor.dev.run_foo_compute(self,*args, **kwargs)


class FreeCAD_VectorArray(FreeCadNodeBase):
	'''Array of Vectors Surface'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_VectorArray, self).__init__(name)
#		self.arrayData = self.createInputPin('poles', 'AnyPin', structure=PinStructure.Array, constraint="1")
#		self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
#		self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

		self.createInputPin("vecA", 'VectorPin',FreeCAD.Vector(20,0,0))
		self.createInputPin("vecB", 'VectorPin',FreeCAD.Vector(0,10,0))
		self.createInputPin("vecC", 'VectorPin')
		self.createInputPin("vecBase", 'VectorPin')
		self.createInputPin("countA", 'IntPin',5)
		self.createInputPin("countB", 'IntPin',8)
		self.createInputPin("countC", 'IntPin',1)
		self.createInputPin("randomX", 'FloatPin',5)
		self.createInputPin("randomY", 'FloatPin',5)
		self.createInputPin("randomZ", 'FloatPin',5)
		self.createInputPin("degreeA", 'IntPin',3)
		self.createInputPin("degreeB", 'IntPin',3)

		self.outArray = self.createOutputPin('out', 'AnyPin', [[],[]], structure=PinStructure.Array)
		self.outArray.enableOptions(PinOptions.AllowAny)


		self.result = self.createOutputPin('result', 'BoolPin')

	@timer 
	def compute(self, *args, **kwargs):

		say ("in compute",self.getName(),"objname is",self.objname.getData())

		import nodeeditor.dev
		reload (nodeeditor.dev)
		return  nodeeditor.dev.run_VectorArray_compute(self,*args, **kwargs)







class FreeCAD_Object(FreeCadNodeBase):
	def __init__(self, name="Fusion"):
		super(FreeCAD_Object, self).__init__(name)
		self.Show = self.createInputPin('Reload_from_FC', 'ExecPin', None, self.reload,)
		self.Show = self.createInputPin('Store_to_FC', 'ExecPin', None, self.store,)
		for i in range(7):
			self.createOutputPin('dummy', 'ExecPin')
		


	def compute(self, *args, **kwargs):

		say("")
		say ("in compute",self.getName(),"objname is",self.objname.getData())
		nl=len(self.getName())
		pps=self.getOrderedPins()
		for p in pps:
			try:
				print (str(p.getName()[nl+1:]),p.getData())
			except:  pass
		obn=self.objname.getData()
		obj=FreeCAD.ActiveDocument.getObject(obn)
		self.fob=obj
		self.store()
		self.outExec.call()



	def reload(self, *args, **kwargs):
		print "reload from FreeCADobject and refresh data" 

	def store(self, *args, **kwargs):

		print ("store  data to  FreeCAD object and to the output pins" )
		
		data={}
		pps=self.getOrderedPins()
		for p in pps:
			dat=p.getData()
#			print ("#+#+#",p.getName(),dat)
			data[str(p.getName())+"_out"]=dat


		for p in pps:
			if p.group=='FOP':
				n=p.getName()
				if n.endswith('_out'):
					p.setData(data[str(n)])
					continue

				pn=n.split('_')[1]
				if pn=="Object": # hack for names FreeCAD_Object #+#
					pn=n.split('_')[2]
				
				vn=p.getData()

				try:
					v=self.fob.getPropertyByName(pn).Value
				except:
					v=self.fob.getPropertyByName(pn)

				if v <> vn:  # value has changed
					setattr(self.fob,pn,vn)

		FreeCAD.activeDocument().recompute()



	def createPins(self, *args, **kwargs):
		say('hack outsourced to nodeetitor.dev')
		import nodeeditor.dev
		reload (nodeeditor.dev)
		return  nodeeditor.dev.runraw(self)
		say("pins created")


class FreeCAD_Console(NodeBase):
	'''
	write to FreeCAD.Console
	'''
	def __init__(self, name="Fusion"):
		super(FreeCAD_Console, self).__init__(name)

		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.entity = self.createInputPin('entity', 'AnyPin',[], structure=PinStructure.Multi)
		self.entity.setData([FreeCAD.Vector(),FreeCAD.Vector()])



	def compute(self, *args, **kwargs):

		FreeCAD.Console.PrintMessage("%s: %s\n"%(self.name,self.entity.getData()))
		self.outExec.call()

class FreeCAD_PartExplorer(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_PartExplorer, self).__init__(name)
		self.part = self.createInputPin('Part_in', 'FCobjPin')
		self.outArray = self.createOutputPin('Points', 'VectorPin', structure=PinStructure.Array)
		self.createOutputPin('Faces', 'ShapeListPin')
		self.createOutputPin('Edges', 'ShapeListPin')

		self.pinsk={
				'Volume':'FloatPin',
				'Area':'FloatPin',
				'Length':'FloatPin',
				'BoundBox': None,
				'CenterOfMass':'VectorPin',
#				#'Edges','Faces','Vertexes','Compounds','Wires','Shells',
#				#'PrincipalProperties','StaticMoments',
				'Mass':'FloatPin',
				'ShapeType':'StringPin',
#				
		}

		say(self.pinsk)
		for p in self.pinsk.keys():
			if self.pinsk[p] <> None:
				say(p,self.pinsk[p])
				self.createOutputPin(p, self.pinsk[p])



	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_PartExplorer_compute(self,*args, **kwargs)

		self.outExec.call()




class FreeCAD_ShapeIndex(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_ShapeIndex, self).__init__(name)
		p=self.createInputPin('Shapes', 'AnyPin')
		p=self.createInputPin('index', 'IntPin')
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_ShapeIndex_compute(self,*args, **kwargs)

		self.outExec.call()



class FreeCAD_Face(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Face, self).__init__(name)
		p=self.createInputPin('sourceObject', 'StringPin')
		p=self.createInputPin('index', 'IntPin')
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Face_compute(self,*args, **kwargs)

		self.outExec.call()

class FreeCAD_Edge(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Edge, self).__init__(name)
		p=self.createInputPin('sourceObject', 'StringPin')
		p=self.createInputPin('index', 'IntPin')
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Edge_compute(self,*args, **kwargs)

		self.outExec.call()


class FreeCAD_Parallelprojection(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Parallelprojection, self).__init__(name)
		p=self.createInputPin('face', 'AnyPin')
		p=self.createInputPin('edge', 'AnyPin')
		p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_projection_compute(self,*args, **kwargs)

		self.outExec.call()

class FreeCAD_UVprojection(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_UVprojection, self).__init__(name)
		p=self.createInputPin('face', 'AnyPin')
		p=self.createInputPin('edge', 'AnyPin')
		#p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
		p=self.createInputPin('pointCount', 'IntPin',20)
		p=self.createInputPin('inverse', 'BoolPin')
		p=self.createInputPin('Extrusion', 'BoolPin')
		p=self.createInputPin('ExtrusionUp', 'FloatPin',100)
		p=self.createInputPin('ExtrusionDown', 'FloatPin',50)
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_uv_projection_compute(self,*args, **kwargs)

		self.outExec.call()



class FreeCAD_Compound(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Compound, self).__init__(name)
		p=self.createInputPin('Shapes', 'AnyPin', structure=PinStructure.Array)
		p=self.createInputPin('XXindex', 'IntPin')
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Compound_compute(self,*args, **kwargs)

		self.outExec.call()






#################


class FreeCAD_Bar(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):

		super(FreeCAD_Bar, self).__init__(name)
		self.part = self.createInputPin('Part_in', 'FCobjPin')
		self.outArray = self.createOutputPin('Points', 'VectorPin', structure=PinStructure.Array)
		self.createOutputPin('Faces', 'ShapeListPin')
		self.createOutputPin('Edges', 'ShapeListPin')

		self.pinsk={
				'Volume':'FloatPin',
				'Area':'FloatPin',
				'Length':'FloatPin',
				'BoundBox': None,
				'CenterOfMass':'VectorPin',
#				#'Edges','Faces','Vertexes','Compounds','Wires','Shells',
#				#'PrincipalProperties','StaticMoments',
				'Mass':'FloatPin',
				'ShapeType':'StringPin',
#				
		}

		say(self.pinsk)
		for p in self.pinsk.keys():
			if self.pinsk[p] <> None:
				say(p,self.pinsk[p])
				self.createOutputPin(p, self.pinsk[p])



	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Bar_compute(self,*args, **kwargs)

		self.outExec.call()


class FreeCAD_Foo(FreeCadNodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Foo, self).__init__(name)
		p=self.createInputPin('Shapes', 'ShapeListPin')
		p=self.createInputPin('index', 'IntPin')
		p.recomputeNode=True


	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Foo_compute(self,*args, **kwargs)

		self.outExec.call()


class FreeCAD_Plot(NodeBase):
	'''
	dummy for tests
	'''

	def __init__(self, name="Fusion"):
		super(FreeCAD_Plot, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
		self.xpin=self.createInputPin('x', 'FloatPin', structure=PinStructure.Array)
		self.ypin=self.createInputPin('y', 'FloatPin', structure=PinStructure.Array)

		self.xpin2=self.createInputPin('x2', 'FloatPin', structure=PinStructure.Array)
		self.ypin2=self.createInputPin('y2', 'FloatPin', structure=PinStructure.Array)
		self.f2=self.createInputPin('Figure2', 'BoolPin')
		self.f3=self.createInputPin('Figure3', 'BoolPin')

	def compute(self, *args, **kwargs):

		sayl()

		import nodeeditor.dev
		reload (nodeeditor.dev)
		nodeeditor.dev.run_Plot_compute(self,*args, **kwargs)

		self.outExec.call()






def nodelist():
	return [
				FreeCAD_Foo,
				FreeCAD_Toy,
				FreeCAD_Bar,
				FreeCAD_Object,
				FreeCAD_Box,
				FreeCAD_Cone,
				FreeCAD_Sphere,
				FreeCAD_Quadrangle,
				FreeCAD_Polygon,
				FreeCAD_Polygon2,
				FreeCAD_Array,
				FreeCAD_Console,
				FreeCAD_VectorArray,
				FreeCAD_Boolean,
				FreeCAD_BSpline,
				FreeCAD_Plot,
				FreeCAD_ShapeIndex,
				FreeCAD_PartExplorer,
				FreeCAD_Compound,
				FreeCAD_Edge,
				FreeCAD_Face,
				FreeCAD_Parallelprojection,
				FreeCAD_UVprojection,
		]
