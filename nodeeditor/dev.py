import numpy as np
import random

import FreeCAD
import nodeeditor.store
import Part

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.store
import nodeeditor.pfwrap as pfwrap


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
			#print "IGNORE '{}' - exists already".format(p)
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
		elif  cn=="Rotation":
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
	try:
		cc.Label=self.objname.getData()
	except:
		pass
	cc.Shape=shape
	self.setPinObject('Shape',shape)
	self.outExec.call()







def run_Plot_compute(self,*args, **kwargs):

	import matplotlib.pyplot as plt

	if self.f2.getData():
		plt.figure(2)

	elif self.f3.getData():
		plt.figure(3)
	else:
		plt.figure(1)

#	plt.close()
	plt.title(self.getName())

	x=self.xpin.getData()
	y=self.ypin.getData()

	#say(x)
	#say(y)
	say(len(x),len(y))


	if len(y) <>0:
		N=len(y)
		if len(x)<>len(y):
			x = np.linspace(0, 10, N, endpoint=True)
		else:
			x=np.array(x)

		y=np.array(y)

		if not self.f3.getData():
			plt.plot(x, y, 'bx')
		plt.plot(x, y , 'b-')


	x2=self.xpin2.getData()
	y2=self.ypin2.getData()
	say (len(x2),len(y2))
	if x2 <> None and y2 <> None:
		x2=np.array(x2)
		y2=np.array(y2)
		if self.f3.getData():
			plt.plot(x2, y2 , 'r-')
		else:
			plt.plot(x2, y2, 'ro')


	plt.show()



def run_projection_compute(self,*args, **kwargs):

	sayl()
	f=FreeCAD.ActiveDocument.BePlane.Shape.Face1
	w=FreeCAD.ActiveDocument.Sketch.Shape.Edge1
	f=store.store().get(self.getPinN('face').getData())
	say("Face",f)
	e=store.store().get(self.getPinN('edge').getData())
	say("Edge",e)

	store.store().list()
	d=self.getPinN('direction').getData()
	say("direction",d)
	shape=f.makeParallelProjection(e,d)
	cc=self.getObject()
	if cc <> None:
		cc.Label=self.objname.getData()
		cc.Shape=shape
		#cc.ViewObject.LineWidth=8
		cc.ViewObject.LineColor=(1.,1.,0.)


def run_uv_projection_compute(self,*args, **kwargs):

	f=store.store().get(self.getPinN('face').getData())
	w=store.store().get(self.getPinN('edge').getData())
	closed=True

	sf=f.Surface

	pointcount=max(self.getPinN('pointCount').getData(),4)
	pts=w.discretize(pointcount)


	bs2d = Part.Geom2d.BSplineCurve2d()
	if closed:
		pts2da=[sf.parameter(p) for p in pts[1:]]
	else:
		pts2da=[sf.parameter(p) for p in pts]

	pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da]
	bs2d.buildFromPolesMultsKnots(pts2d,[1]*(len(pts2d)+1),range(len(pts2d)+1),True,1)
	e1 = bs2d.toShape(sf)

	sp=FreeCAD.ActiveDocument.getObject("_Spline")
	if sp==None:
		sp=FreeCAD.ActiveDocument.addObject("Part::Spline","_Spline")
	sp.Shape=e1

	face=f
	edges=e1.Edges
	ee=edges[0]
	splita=[(ee,face)]
	r=Part.makeSplitShape(face, splita)

	ee.reverse()
	splitb=[(ee,face)]
	r2=Part.makeSplitShape(face, splitb)

	try:
		rc=r2[0][0]
		rc=r[0][0]
	except: return

	cc=self.getObject()
	if cc <> None:
		cc.Label=self.objname.getData()

	if self.getPinN('inverse').getData():
		cc.Shape=r2[0][0]
	else:
		cc.Shape=r[0][0]

	if self.getPinN('Extrusion').getData():
		f = FreeCAD.getDocument('project').getObject('MyExtrude')
		if f == None:
			f = FreeCAD.getDocument('project').addObject('Part::Extrusion', 'MyExtrude')

		f.Base = sp
		f.DirMode = "Custom"
		f.Dir = FreeCAD.Vector(0.000000000000000, 0.000000000000000, 1.000000000000000)
		f.LengthFwd = self.getPinN('ExtrusionUp').getData()
		f.LengthRev = self.getPinN('ExtrusionDown').getData()
		f.Solid = True
		FreeCAD.activeDocument().recompute()

	#see without extra part >>> s.Face1.extrude(FreeCAD.Vector(0,1,1))
	#<Solid object at 0x660e520>


def run_Bar_compute(self,*args, **kwargs):
	sayl()


def run_Foo_compute(self,*args, **kwargs):
	sayl()



def run_enum(self):
	say("process the rawPin data ")
	say("rawPin is",self.pin._rawPin)
	say("values ...")
	for v in self.pin._rawPin.values:
		say(v)



def f4(self):
	say("FreeCAD Ui Node runs f4")
	say("nothing to do, done")

import FreeCADGui

def run_view3d(self,name,shape,workspace,mode,wireframe,transparency):
	sayl()
	
	shape=self.getPinObject('Shape')
	s=shape
	l=FreeCAD.listDocuments()
	if workspace=='' or workspace=='None':
		w=l['Unnamed']
	else:
		if workspace in l.keys():
			w=l[workspace]
		else:
			w=FreeCAD.newDocument(workspace)

			#Std_CascadeWindows
			FreeCADGui.runCommand("Std_ViewDimetric")
			FreeCADGui.runCommand("Std_ViewFitAll")
			FreeCADGui.runCommand("Std_TileWindows")

	#s=store.store().get(shape)

	f=w.getObject(name)
	if f == None:
		f = w.addObject('Part::Feature', name)
	if s <> None:
		f.Shape=s
	say("shape",s)

	w.recompute()

	if not wireframe:
		f.ViewObject.DisplayMode = "Flat Lines"
		f.ViewObject.ShapeColor = (random.random(),random.random(),1.)
	else:
		f.ViewObject.DisplayMode = "Wireframe"
		f.ViewObject.LineColor = (random.random(),random.random(),1.)

	f.ViewObject.Transparency = transparency




from PyFlow.Packages.PyFlowBase.Factories.UINodeFactory import createUINode


def run_foo_compute(self,*args, **kwargs):
	pass


def run_visualize(self,*args, **kwargs):
	say(self._rawNode)
	say("create vid3d object in graph")
	gg=self.graph()
	x,y=-150,-100
	nodeClass='FreeCAD_view3D'
	#t3 = pfwrap.createNode('PyFlowFreeCAD',nodeClass,"MyPolygon")
	#t3.setPosition(x,y)
	#gg.addNode(t3)
	#uinode=createUINode(t3)
	#say(uinode)
	aa=self.canvasRef().spawnNode(nodeClass, x, y)
	say(aa.__class__)
	say("connect Shape withj vie3d.shape ...")
	FreeCAD.aa=aa
	pfwrap.connect(self._rawNode,'Shape',aa._rawNode,'Shape')
	sayl()

	pfwrap.connect(self._rawNode,'outExec',aa._rawNode,'inExec')
	aa._rawNode.setData('name','View_'+self._rawNode.name)




def run_FreeCAD_Tripod(self,*args, **kwargs):
	sayl()
	f=self.getPinObject('Shape')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	#if f.__class__.__name__  == 'Face':
	
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	say(umin,umax,vmin,vmax)
	u,v=self.getData("u"),self.getData("v")
	
	say(f)
	uu=umin+(umax-umin)*0.1*u
	vv=vmin+(vmax-vmin)*0.1*v
	pos=sf.value(uu,vv)
	self.setData('position',pos)
	
	if self.getData('curvatureMode'): 
		# curvature
		t1,t2=sf.curvatureDirections(uu,vv)


	else: # tangents
		t1,t2=sf.tangent(uu,vv)
#		t1=t1.normalize()
#		t2=t2.normalize()

	if self.getData('directionNormale'): 
			n=t1.cross(t2).normalize()
	else: 
			n=t2.cross(t1).normalize()

	
	if self.getData('display'):
		obj=self.getObject()
		shape=Part.makePolygon([pos,pos+t1*10,pos+t2*5,pos,pos+n*5],
						)
		obj.Shape=shape


	self.outExec.call()



def run_FreeCAD_uIso(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	u=self.getData("u")

	uu=umin+(umax-umin)*0.1*u
	c=sf.uIso(uu)
	self.setPinObject('Edge',c.toShape())

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=c.toShape()

	self.outExec.call()


def run_FreeCAD_vIso(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	v=self.getData("v")

	vv=vmin+(vmax-vmin)*0.1*v
	c=sf.vIso(vv)
	self.setPinObject('Edge',c.toShape())

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=c.toShape()

	self.outExec.call()

def run_FreeCAD_uvGrid(self,*args, **kwargs):

	f=self.getPinObject('Face')
	if f.__class__.__name__  == 'Shape':
		f=f.Face1
	sf=f.Surface

	[umin,umax,vmin,vmax]=f.ParameterRange
	uc=self.getData("uCount")
	vc=self.getData("vCount")
	
	us=[]
	for u in range(uc+1):
		uu=umin+(umax-umin)*u/uc
		c=sf.uIso(uu).toShape()
		us += [c]

	vs=[]
	for v in range(vc+1):
		vv=vmin+(vmax-vmin)*v/vc
		c=sf.vIso(vv).toShape()
		vs += [c]

	if self.getData('display'):
		obj=self.getObject()
		obj.Shape=Part.Compound(us+vs)

	self.setPinObjects('uEdges',us)
	self.setPinObjects('vEdges',vs)

