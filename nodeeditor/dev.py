import FreeCAD 
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin
from nodeeditor.say import *




def runraw(self):
	# called biy FreeCAD_Object createpins
	objname=self.objname.getData()
	fobj=FreeCAD.ActiveDocument.getObject(objname)

	if fobj == None:
		print "cannot create pins because no FreeCAD object for name {}".format(objname)
		return []
	ps=fobj.PropertiesList
	if 0:
		sayl('#')
		print "FreeCAD object Properties ---"
		for p in ps:
			print p

	
	pins=[]
	ipm=self.namePinInputsMap

	if 0:
		print("ipm.keys() for ",objname,fobj.Name,fobj.Label)
		for k in ipm.keys():
			print k

#---------------

	recomputepins=[]
	for p in ps:
		try:
			a=getattr(fobj,p)
		except:
			print ("ignore problem with prop",p," fix it later !!")
			continue

		if p in ["Placement","Shape",
				"MapMode",
				"MapReversed","MapPathParameter",
				"Attacher",
				"AttacherType",
				"AttachmentOffset","ExpressionEngine","Support"]:
			pass
			#continue


		if p in ipm.keys():
			#print "IGNORE '{}' - exists aready".format(p)
			continue

		cn=a.__class__.__name__

		if p.startswith("aLink"):
			# zu tun
			continue
#		print("################",cn,p,a)
		if cn=="list" and p.endswith('List'):
			
			r2=p.replace('List','Pin')
			r=r2[1:]
#			say("--------------",p,r,r2)
			if r=="IntegerPin":
				r="IntPin"
			try:
				p1 = self.createInputPin(p, r ,[],structure=PinStructure.Array)
				p2 = self.createOutputPin(p+"_out", r ,[],structure=PinStructure.Array)
				pins += [p1,p2]
			except:
				say("cannot create list pin for",p,r2)

			continue



		if cn=="Quantity" or cn=="float":
			pintyp="FloatPin"
		elif  cn=="Vector":
			pintyp="VectorPin"
		elif  cn=="str" or cn=="unicode":
			pintyp="StringPin"
		elif  cn=="bool":
			pintyp="BoolPin"
		elif  cn=="int":
			pintyp="IntPin"
		elif  cn=="Placement":
			pintyp="PlacementPin"
		elif  cn=="Roation":
			pintyp="RotationPin"
		

		elif cn=='list' or cn == 'dict' or cn=='tuple' or cn=='set':
			# zu tun 
			continue
		elif cn=='Material'  or cn=='Shape' or cn=='Matrix' :
			# zu tun 
			continue
		elif cn=='NoneType' :
			# zu tun 
			continue


		else:
			say(p,cn,a,"is not known")
			continue



		pinname=p
		pinval=a
		
#		say("create pin for ",pintyp,pinname,pinval)
		p1 = CreateRawPin(pinname,self, pintyp, PinDirection.Input)
		p2 = CreateRawPin(pinname+"_out",self, pintyp, PinDirection.Output)
		p1.enableOptions(PinOptions.Dynamic)
	#	p1.recomputeNode=True
		recomputepins += [p1]
		p1.setData(pinval)
		p2.setData(pinval)
		say("created:",p1)
  
		pins  += [p1,p2]


	sayl()

	for p in recomputepins:
		p.recomputeNode=True

	for p in pins:
		p.group="FOP"

	return pins


import numpy as np
import Part

def run_foo_compute(self,*args, **kwargs):
	# compute fuer FreeCAD_Foo.compute
	dat=self.arrayData.getData()
	dat=np.array(dat)
	say(dat)
	sf=Part.BSplineSurface()
	sf.buildFromPolesMultsKnots(dat,[2,2],[2,2],[0,1],[0,1],False,False,1,1)
	shape=sf.toShape()
	cc=self.getObject()
	cc.Label=self.objname.getData()
	cc.Shape=shape


import random


def run_VectorArray_compute(self,*args, **kwargs):
	
	countA=self.getData("countA")
	countB=self.getData("countB")
	countC=self.getData("countC")
	vO=self.getData("vecBase")
	vA=self.getData("vecA")
	
	vB=self.getData("vecB")
	vC=self.getData("vecC")
	rx=self.getData("randomX")
	ry=self.getData("randomY")
	rz=self.getData("randomZ")
	
	
	degA=self.getData("degreeA")
	degB=self.getData("degreeB")
	if countA<degA+1:
		degA=countA-1
	if countB<degB+1:
		degB=countB-1

	points=[vO+vA*a+vB*b+vC*c+FreeCAD.Vector((0.5-random.random())*rx,(0.5-random.random())*ry,(0.5-random.random())*rz) 
		for a in range(countA) for b in range(countB) for c in range(countC)]

	if countC != 1:
		sayexc("not implemented")
		return

	if degA==0 or degB==0:
		col = []
		poles=np.array(points).reshape(countA,countB,3)
		for ps in poles:
			ps=[FreeCAD.Vector(p) for p in ps]
			col += [Part.makePolygon(ps)]
		for ps in poles.swapaxes(0,1):
			ps=[FreeCAD.Vector(p) for p in ps]
			col += [Part.makePolygon(ps)]

		shape=Part.makeCompound(col)


	else:

		poles=np.array(points).reshape(countA,countB,3)

		multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
		multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
		knotA=range(len(multA))
		knotB=range(len(multB))

		sf=Part.BSplineSurface()
		sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
		shape=sf.toShape()


	self.setData('out',poles)

	cc=self.getObject()
	cc.Label=self.objname.getData()
	cc.Shape=shape
	self.outExec.call()


