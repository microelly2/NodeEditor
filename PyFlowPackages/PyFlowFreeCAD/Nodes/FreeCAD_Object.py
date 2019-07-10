from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

from nodeeditor.say import *

from FreeCAD import Vector
import FreeCAD
import Part

import nodeeditor.store as store



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
		store.store().list()

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



class FreeCAD_Bar(NodeBase):
	'''boolean ops of two parts example'''
	def __init__(self, name="Fusion"):

		super(FreeCAD_Bar, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
		self.part = self.createOutputPin('Part', 'FCobjPin')
		self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
		self.part2 = self.createInputPin('Part_in2', 'FCobjPin')
		self.objname = self.createInputPin("objectname", 'StringPin')

		self.mode = self.createInputPin('mode', 'EnumerationPin')
		self.mode.values=["fuse","cut","common"]
		self.mode.setData("fuse")

		self.volume = self.createOutputPin('Volume', 'FloatPin')

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

		say("getData:",self.part1.getData(),self.part1.getData().__class__)
		say("!",self.part1,self.part1.__class__)

		part1=self.part1.getData()
		if part1 <> None:
			part1=FreeCAD.ActiveDocument.getObject(part1)

		part2=self.part2.getData()
		if part2 <> None:
			part2=FreeCAD.ActiveDocument.getObject(part2)

		if part1 <> None and part2 <> None:
			say("parts 1 2")
			say(part1.Name)
			say(part2.Name)
			mode=self.mode.getData()
			if mode == 'common':
				shape=part1.Shape.common(part2.Shape)
			elif mode == 'cut':
				shape=part1.Shape.cut(part2.Shape)
			else:
				shape=part1.Shape.fuse(part2.Shape)
			cc.Shape=shape
		else:
			return

		if self.part.hasConnections():
			say("sende an Part")
			if cc == None:
				self.part.setData(None)
			else:
				self.part.setData(cc.Name)
		say("Volume",cc.Shape.Volume)
		self.volume.setData(cc.Shape.Volume)
		say ("data set to output object is done, exex...")
		self.outExec.call()
		say ("Ende exec for ---",self.getName())








class FreeCAD_Foo(NodeBase):
	pass


def nodelist():
	return [FreeCAD_Foo,FreeCAD_Toy,FreeCAD_Bar,FreeCAD_Object]
