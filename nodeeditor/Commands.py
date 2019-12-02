# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- freecad wrapper for pyflow
#--
#-- microelly 2019 
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import os
import sys
import json

os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join([ "PyQt4"])
import Qt

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin

from nodeeditor.say import *

import FreeCAD,FreeCADGui

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *


import nodeeditor.PyFlowGraph

from nodeeditor.PyFlowGraph import PyFlowGraph, Blinker, Receiver

from PyFlow import(
	INITIALIZE,
	GET_PACKAGES
)

from PyFlow.Core import(
	GraphBase,
	PinBase,
	NodeBase,
	GraphManager
)

import sys
if sys.version_info[0] !=2:
	from importlib import reload


import nodeeditor.pfwrap as pfwrap
reload (pfwrap)


def unloadmodules():
	''' prepare some modules for reload'''
	try:
		FreeCAd.t.hide()
	except:
		pass

	if 10:
		sms=sys.modules.keys()
		for m in sms:

			if m.startswith('PyFlow'):
				print(m)
				del(sys.modules[m])

	return


def QtEnvironment():
	''' test Qt environment'''
	say("Qt is " +str(Qt))
	say(["Flags in Qt: PyQt4",Qt.IsPyQt4,"PySide",Qt.IsPySide])


def refresh_gui():

	hidePyFlow()
#	tempd=pfwrap.getInstance().getTempDirectory()

	gg=pfwrap.getGraphManager().getAllGraphs()[0]
	saveData = gg.serialize()

	import tempfile
	f = tempfile.NamedTemporaryFile(delete=False)
	fpath= f.name
	json.dump(saveData, f, indent=4)
	f.close()
	say("fname",fpath)

	with open(fpath, 'r') as f:
		data = json.load(f)
		FreeCAD.data=data
		pfwrap.getInstance().loadFromData(data, fpath)

	pfwrap.getInstance().show()
	clearLogger()
	FreeCADGui.activeDocument().activeView().viewIsometric()
	FreeCADGui.SendMsgToActiveView("ViewFit")


def VectorRotationPlacement():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	makeInt=pfwrap.createFunction('PyFlowBase',"DefaultLib","makeInt")
	makeInt.setData('i', 5)

	addNode2 = pfwrap.createFunction('PyFlowBase',"MathAbstractLib","add")
	printNode = pfwrap.createNode('PyFlowBase',"consoleOutput","printer")

	gg.addNode(makeInt)
	gg.addNode(addNode2)
	gg.addNode(printNode)

	makeInt.setPosition(-200,-150)
	addNode2.setPosition(-150,-70)
	printNode.setPosition(200,-100)

	# freecad nodes erstellen

	fa=pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecAdd")
	gg.addNode(fa)
	fa.setPosition(100,0)
	fa.setData('a', FreeCAD.Vector(1,2,3))


	fb = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecAdd")
	gg.addNode(fb)
	fb.setPosition(-100,0)
	fb.setData('a', FreeCAD.Vector(1,2,3))
	fb.setData('b', FreeCAD.Vector(-3,-5,-6))

	connection = pfwrap.connect(fa,'out',printNode,'entity')
	connection = pfwrap.connect(fb,'out',fa,'b')

	ra=pfwrap.createFunction('PyFlowFreeCAD',"Rotation","rotMultiply")
	gg.addNode(ra)
	ra.setPosition(-300,100)

	pa=pfwrap.createFunction('PyFlowFreeCAD',"Placement","pmMultiply")
	pa.setPosition(-200,100)
	gg.addNode(pa)

	pc=pfwrap.createFunction('PyFlowFreeCAD',"Placement","pmCreate")
	pc.setPosition(-100,100)
	gg.addNode(pc)

	box=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	box2=FreeCAD.ActiveDocument.addObject("Part::Box","Box")

	fp = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Placement","Placer")
	fp.setData('objectname', 'Box')
	gg.addNode(fp)
	fp.setPosition(350,100)

	tim = pfwrap.createNode('PyFlowBase',"timer","MyTimer")
	tim.setPosition(200,-200)
	gg.addNode(tim)

	seq = pfwrap.createNode('PyFlowBase',"sequence","MySeq")
	gg.addNode(seq)
	seq.setPosition(-450,-50)

	connection = pfwrap.connect(tim,'OUT',fp,'inExec')
	connection = pfwrap.connect(fa,'out', fp,'Placement_Base')

def PlacerFreeCAD_ObjectandArraypins():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	box=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	box2=FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	sphere=FreeCAD.ActiveDocument.addObject("Part::Sphere","Sphere")


	printNode = pfwrap.createNode('PyFlowBase',"consoleOutput","printer")
	printNode.setPosition(500,-0)
	gg.addNode(printNode)

	fp = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Placement","Placer")
	fp.setData('objectname', 'Box')
	fp.setPosition(-100,-100)
	gg.addNode(fp)

	fpo = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Object","FCobj")
	fpo.setData('objectname', 'Box')
	fpo.setPosition(100,-100)
	gg.addNode(fpo)

	fpo2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Object","FCobj__________2")
	fpo2.setData('objectname', 'Box001')
	fpo2.setPosition(300,-100)
	gg.addNode(fpo2)
	#connection = pfwrap.connect(fpo,'Object', fpo2,'ObjectA')
	#connection = pfwrap.connect(fpo,'Shape_out', fpo2,'Shape_in')
	connection = pfwrap.connect(fpo,'outExec', fpo2,'inExec')
	connection = pfwrap.connect(fpo,'Array_out', fpo2,'Array_in')
	connection = pfwrap.connect(fpo2,'outExec', printNode,'inExec')
	connection = pfwrap.connect(fpo2,'Object', printNode,'entity')



	showPyFlow()
	a=pfwrap.getGraphManager()
	gg=a.getAllGraphs()[0]


	fb = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	gg.addNode(fb)
	fb.setPosition(-300,0)
	fb.setData('X', 1)
	fb.setData('Y', 2)


	ri = pfwrap.createFunction('PyFlowBase',"RandomLib","randint")
	gg.addNode(ri)

	tim = pfwrap.createNode('PyFlowBase',"timer","MyTimer")
	tim.setPosition(200,-200)
	gg.addNode(tim)

	connection = pfwrap.connect(ri,'Result', fb,'Z')
	connection = pfwrap.connect(fb,'out', fp,'Placement_Base')
	connection = pfwrap.connect(tim,'OUT', fp,'inExec')


def FusionoftwoToynodes():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Toy","Toy")
	t.setPosition(-200,-200)
	gg.addNode(t)

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Toy","Toy2")
	t2.setPosition(-200,00)
	gg.addNode(t2)

	tf = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Boolean","Boolean")
	tf.setPosition(100,-200)
	gg.addNode(tf)

	connection = pfwrap.connect(t,'Part', tf,'Part_in1')
	connection = pfwrap.connect(t2,'Part', tf,'Part_in2')

	connection = pfwrap.connect(t,'outExec', tf,'inExec')
	connection = pfwrap.connect(t2,'outExec', tf,'inExec')
	connection = pfwrap.chainExec(t,tf)

	tim = pfwrap.createNode('PyFlowBase',"timer","MyTimer")
	tim.setPosition(-500,-200)
	gg.addNode(tim)

	s = pfwrap.createNode('PyFlowBase',"sequence","MySequence")
	s.setPosition(-400,-00)
	gg.addNode(s)
	s.createOutputPin()
	s.createOutputPin()

	connection = pfwrap.connect(tim,'OUT', s,'inExec')
	connection = pfwrap.connect(s,'1', t,'inExec')
	#connection = pfwrap.connect(s,'2', t2,'inExec')


def ConeTorusBoxandImagenode():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	FreeCAD.ActiveDocument.addObject("Part::Torus","Torus")
	FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	
	t = pfwrap.createNode('PyFlowBase',"imageDisplay","ImageXX")
	t.setPosition(-100,-200)
	t.entity.setData('/home/thomas/Bilder/freeka.png')
	t.compute()
	#t.setData("shapeOnly",True)
	gg.addNode(t)

	refresh_gui()


def arrayofarrayforsurface():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	gg.addNode(v1)

	v2 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v2.setData('X', 10)
	v2.setData('Y', 0)
	gg.addNode(v2)

	v3 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v3.setData('X', 0)
	v3.setData('Y', 10)
	gg.addNode(v3)

	v4 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v4.setData('X', 10)
	v4.setData('Y', 10)
	gg.addNode(v4)

	ar = pfwrap.createNode('PyFlowBase',"makeArray","VecArray")
	gg.addNode(ar)
	connection = pfwrap.connect(v1,'out',ar,'data')
	connection = pfwrap.connect(v2,'out',ar,'data')

	ar2 = pfwrap.createNode('PyFlowBase',"makeArray","VecArray")
	gg.addNode(ar2)
	connection = pfwrap.connect(v3,'out',ar2,'data')
	connection = pfwrap.connect(v4,'out',ar2,'data')

	ar3 = pfwrap.createNode('PyFlowBase',"makeArray","VecArray")
	gg.addNode(ar3)
	ar3.setData('preserveLists',True)
	connection = pfwrap.connect(ar,'out',ar3,'data')
	connection = pfwrap.connect(ar2,'out',ar3,'data')

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_BSpline","aBSplineSurface")
	t2.setPosition(-300,-150)
	gg.addNode(t2)
	connection = pfwrap.connect(ar3,'out',t2,'poles')

	refresh_gui()

def createaVectorArraytoplay():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	ta = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_VectorArray","aVectorArray")
	ta.setPosition(-200,00)
	gg.addNode(ta)


	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(00,00)
	#t.setData("shapeOnly",True)
	gg.addNode(t)
	connection = pfwrap.connect(ta,'out',t,'entity')

	tim = pfwrap.createNode('PyFlowBase',"timer","MyTimer")
	tim.setPosition(-300,-100)
	gg.addNode(tim)
	connection = pfwrap.connect(tim,'OUT', ta,'inExec')

	refresh_gui()

def playwithFreeCAD_Array():
	'''test numpy array flow'''

	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Object","PPP")
	t2.setPosition(-00,-150)
	gg.addNode(t2)

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Array","AAA")
	t2.setPosition(-300,-150)
	gg.addNode(t2)

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Array","BBB")
	t3.setPosition(-100,0)
	gg.addNode(t3)

	t4 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Array","CCC")
	t4.setPosition(100,150)
	gg.addNode(t4)

	connection = pfwrap.connect(t2,'Array_out', t3,'Array_in')
	connection = pfwrap.chainExec(t2,t3)

	connection = pfwrap.connect(t3,'Array_out', t4,'Array_in')
	connection = pfwrap.chainExec(t3,t4)
	t2.compute()

	refresh_gui()

def PolygonandPolygon2():
	'''test point listnumpy array flow'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon","MyPolygon")
	t3.setPosition(-200,0)
	gg.addNode(t3)
	t3.compute()

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","MyPolygon2")
	gg.addNode(t3)
	t3.compute()

def PartExplorerSubshapeIndexandPlot():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Box","MyBox")
	t2.setPosition(-200,0)
	gg.addNode(t2)

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_PartExplorer","MyPartExplorer")
	t3.setPosition(00,0)
	gg.addNode(t3)
	t2.compute()
	t3.compute()
	connection = pfwrap.connect(t2,'Part', t3,'Part_in')

	t4 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_ShapeIndex","MyIndex")
	#t4.setData("shapeOnly",True)
	t4.setPosition(200,0)
	gg.addNode(t4)

	t4 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Plot","MyPlot")
	t4.setPosition(00,-200)
	#gg.addNode(t4)

	t2.compute()
	t3.compute()
	t4.compute()

	t5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Compound","MyCompound")
	t5.setPosition(-200,-200)
	gg.addNode(t5)

	refresh_gui()


def createPolygonFromCoordinateListswithnumpy():
	'''
	create Polygon from CoordinateLists	with numpy
	create 3 random lists
	zip them to a vector list
	create a polygon 
	'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	makeInt=pfwrap.createFunction('PyFlowBase',"DefaultLib","makeInt")
	makeInt.setData('i', 50)
	gg.addNode(makeInt)

	v = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","zip")
	gg.addNode(v)

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'x')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'y')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'z')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	gg.addNode(t)
#	connection = pfwrap.connect(v,'out', t,'entity')
	t.compute()

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Polygon")
	gg.addNode(t)
	connection = pfwrap.connect(v,'out', t,'points')

	refresh_gui()


def drawadoublesinuscurve():
	'''
	x=a*sin(b*z+c)
	y=a'*sin(b'*z+c')
	'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	makeInt=pfwrap.createFunction('PyFlowBase',"DefaultLib","makeInt")
	makeInt.setData('i', 50)
	gg.addNode(makeInt)

	v = pfwrap.createFunction('PyFlowFreeCAD',"Vector","zip")
	gg.addNode(v)

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","linSpace")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'z')
	connection = pfwrap.connect(makeInt,'out', v1,'num')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","linSpace")
	gg.addNode(v1)
#	connection = pfwrap.connect(v1,'out', v,'y')
	connection = pfwrap.connect(makeInt,'out', v1,'num')

	s = pfwrap.createFunction('PyFlowFreeCAD',"Vector","sin")
	gg.addNode(s)
	connection = pfwrap.connect(v1,'out', s,'data')
	connection = pfwrap.connect(s,'out', v,'y')
	s.setData("b",5)


	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","linSpace")
	gg.addNode(v1)
	#connection = pfwrap.connect(v1,'out', v,'x')
	connection = pfwrap.connect(makeInt,'out', v1,'num')

	s = pfwrap.createFunction('PyFlowFreeCAD',"Vector","sin")
	gg.addNode(s)
	connection = pfwrap.connect(v1,'out', s,'data')
	connection = pfwrap.connect(s,'out', v,'x')

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	gg.addNode(t)
	t.compute()

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Polygon")
	gg.addNode(t)
	connection = pfwrap.connect(v,'out', t,'points')

	refresh_gui()




def reset():
	'''file laden und graph anzeigen testcase'''

	if 'aa' not in FreeCAD.listDocuments().keys():
		FreeCAD.open(u"/home/thomas/aa.FCStd")
	FreeCAD.setActiveDocument("aa")
	
	try:
		pfwrap.deleteInstance()
		del(FreeCAD.PF)
	except:
		pass
	instance=pfwrap.getInstance()
	clearGraph()
	loadGraph()

class MyDockWidget(QDockWidget):

	def __init__(self, title_widget, objectname):

		QDockWidget.__init__(self)

		self.title_widget = title_widget
		self.setWindowTitle(objectname)
		self.setObjectName(objectname)

		if 1:
			self.setTitleBarWidget(None)
		else:
			self.setTitleBarWidget(self.title_widget)

		self.setMinimumSize(200, 185)

		self.centralWidget = QWidget(self)
		self.setWidget(self.centralWidget)

		l=QVBoxLayout()
		self.layout = l
		self.centralWidget.setLayout(l)

		#a=QGraphicsView()
		#l.addWidget(a)

		if 1:
			buttons=QWidget()
			bl = QHBoxLayout()
			buttons.setLayout(bl)

			pB = QPushButton(QtGui.QIcon('icons:freecad.svg'), 'load File A')
			bl.addWidget(pB)
#			pB.clicked.connect(self.loadA)

			pB = QPushButton(QtGui.QIcon('icons:freecad.svg'), 'refresh')
			bl.addWidget(pB)
#			pB.clicked.connect(self.refresh)
			for i in range(3):
				pB = QPushButton(QtGui.QIcon('icons:freecad.svg'), 'F'+str(i))
				bl.addWidget(pB)
#			pB.clicked.connect(self.save)

			pB = QPushButton(QtGui.QIcon('icons:freecad.svg'), 'load dialog')
			bl.addWidget(pB)
#			pB.clicked.connect(self.load)
			pB = QPushButton(QtGui.QIcon('icons:freecad.svg'), 'Properties Tool')
			bl.addWidget(pB)
#			pB.clicked.connect(createPropTool)

			l.addWidget(buttons)


		# geht nicht, weil FreeCAD PYside ist und es crash gibt
		#w = FreeCADGui.getMainWindow()

		w=pfwrap.getInstance()
		w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
		
		l.addWidget(pfwrap.getInstance().canvasWidget)


		a=QPushButton("Bottom Button 1")
		l.addWidget(a)

		d=QPushButton("Bottom Button 2")
		l.addWidget(d)





def PyFlowtoDockWidget():

	# erzeugen PyFlow Fenster
#	test_AA()
	# erzeuge eigenes Fesnter und uebernehme die Daten
	a=MyDockWidget(None, "objectname")
	a.show()
	FreeCAD.a=a

def save_and_load_json_file_test():
	pfwrap.getInstance().load('/home/thomas/Schreibtisch/aa2.json')
	pfwrap.getInstance().save(False,'/home/thomas/Schreibtisch/aa2.json')




def shutdown():
	'''fast stop of freecad test environ'''
	try:
		FreeCAD.closeDocument("Unnamed")
	except:
		pass
	try:
		FreeCAD.closeDocument("graph")
	except:
		pass

	FreeCADGui.runCommand("Std_Quit")


def hidePyFlow():
	pfwrap.deleteInstance()

def showPyFlow():
	try:
		pfwrap.getInstance().hide()
	except:
		pass
	pfwrap.getInstance().show()



def thinoutGraph():
	'''test clean up graph: delete half of the nodes'''
	instance=pfwrap.getInstance()
	gg=instance.graphManager.get().getAllGraphs()[0]
	for i,n in enumerate(gg.getNodes()):
		if i%2==0: n.kill()

def clearGraph():
	instance=pfwrap.getInstance()
	instance.graphManager.get().clear(keepRoot=False)

def clearGraph(): # bugfix clear geht nicht mit fc #+#
	for node in pfwrap.getInstance().graphManager.get().getAllNodes():
		node.kill()
	pfwrap.deleteInstance()
	del(FreeCAD.PF)

def loadGraph():
	showPyFlow()
	instance=pfwrap.getInstance()
	instance.graphManager.get().clear()
	a=PyFlowGraph()
#	a=FreeCAD.Gui.Selection.getSelection()[0]
	data=eval(a.graph)
	instance.loadFromData(data)


def saveGraph():
	instance=pfwrap.getInstance()
	saveData = instance.graphManager.get().serialize()
	a=PyFlowGraph()
	a.graph=str(saveData)


def loadFile():

	hidePyFlow()
	if 'graph' not in FreeCAD.listDocuments().keys():
		FreeCAD.open(u"/home/thomas/graph.FCStd")
	FreeCAD.setActiveDocument("graph")
	clearGraph()
	loadGraph()




def clearLogger():
	'''logger clear'''
	instance=pfwrap.getInstance()
	for t in instance._tools:
		if t.name() == 'Logger':
			say(t)
			t.clearView()
			t.hide()




class ViewProvider:
	def __init__(self, obj):
		obj.Proxy = self

def createObjectWithAllProperties(): 
	obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","allProps")
	for p in obj.supportedProperties():
		pn=str(p).replace('Part::Property','a')
		pn=str(p).replace('App::Property','a')
		obj.addProperty(p,pn)
		print ("obj.addProperty('{}','{}')".format(p,pn))

	ViewProvider(obj.ViewObject)

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Object","allProps")
	t.setPosition(-100,-200)
	#t.setData("shapeOnly",True)
	gg.addNode(t)


	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	#t.setData("shapeOnly",True)
	gg.addNode(t)


	fb = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	gg.addNode(fb)
	fb.setPosition(-300,0)
	fb.setData('X', 1)
	fb.setData('Y', 2)
	fb2 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	gg.addNode(fb2)

	arr = pfwrap.createNode('PyFlowBase',"makeArray","VecArray")

	gg.addNode(arr)

	connection = pfwrap.connect(fb,'out',arr,'data')
	connection = pfwrap.connect(fb2,'out',arr,'data')
	connection = pfwrap.connect(arr,'out',t,'entity')

	pol = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Polygon")
	gg.addNode(pol)

	refresh_gui()





def crossbeamexample():
	'''
	# see https://forum.freecadweb.org/viewtopic.php?f=8&t=37817
	'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	#t.setData("shapeOnly",True)
	gg.addNode(t)


	# 1.rib
	v = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v.setPosition(400,0)
	gg.addNode(v)

	v2= pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v2.setData('Y', 20)
	v2.setPosition(400,100*2)
	gg.addNode(v2)

	v3 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v3.setData('Y', 50)
	v3.setPosition(400,200*2)
	gg.addNode(v3)

	ar = pfwrap.createNode('PyFlowBase',"makeArray","VecArray_rib_1")
	gg.addNode(ar)
	connection = pfwrap.connect(v,'out',ar,'data')
	connection = pfwrap.connect(v2,'out',ar,'data')
	connection = pfwrap.connect(v3,'out',ar,'data')

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Rib_1")
	gg.addNode(t3)
	t3.setPosition(1700,-200)
	connection = pfwrap.connect(ar,'out',t3,'points')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(510,25*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(520,75*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(510,125*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(520,175*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	rib1=ar
	t3.compute()

	# 2.rib
	v = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v.setData('X', 20)
	v.setData('Z', 20)
	v.setPosition(600,0)
	gg.addNode(v)

	v2= pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v2.setData('X', 40)
	v2.setData('Y', 20)
	v2.setData('Z', 40)
	v2.setPosition(600,100*2)
	gg.addNode(v2)

	v3 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v3.setData('X', 40)
	v3.setData('Y', 50)
	v3.setData('Z', 40)
	v3.setPosition(600,200*2)
	gg.addNode(v3)

	ar = pfwrap.createNode('PyFlowBase',"makeArray","VecArray_rib_4")
	gg.addNode(ar)
	connection = pfwrap.connect(v,'out',ar,'data')
	connection = pfwrap.connect(v2,'out',ar,'data')
	connection = pfwrap.connect(v3,'out',ar,'data')

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Rib_4")
	gg.addNode(t3)
	t3.setPosition(1700,0)
	connection = pfwrap.connect(ar,'out',t3,'points')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(710,25*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(720,75*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(720,125*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(710,175*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	t3.compute()
	rib4=ar



	# 7.rib
	v = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v.setData('X', 140)
	v.setData('Z', 20)
	v.setPosition(800,0)
	gg.addNode(v)

	v2= pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v2.setData('X', 140)
	v2.setData('Y', 20)
	v2.setData('Z', 40)
	v2.setPosition(800,100*2)
	gg.addNode(v2)

	v3 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","vecCreate")
	v3.setData('X', 140)
	v3.setData('Y', 50)
	v3.setData('Z', 40)
	v3.setPosition(800,200*2)
	gg.addNode(v3)

	ar = pfwrap.createNode('PyFlowBase',"makeArray","VecArray_rib_7")
	gg.addNode(ar)

	connection = pfwrap.connect(v,'out',ar,'data')
	connection = pfwrap.connect(v2,'out',ar,'data')
	connection = pfwrap.connect(v3,'out',ar,'data')

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Rib_7")
	t3.setPosition(1700,400)
	gg.addNode(t3)
	connection = pfwrap.connect(ar,'out',t3,'points')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(920,25*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(910,75*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v,'out',j,'a')
	connection = pfwrap.connect(v2,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(920,125*2)
	j.setData('m',1)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	j = pfwrap.createFunction('PyFlowFreeCAD',"Vector","between")
	j.setPosition(910,175*2)
	j.setData('m',9)
	gg.addNode(j)
	connection = pfwrap.connect(v2,'out',j,'a')
	connection = pfwrap.connect(v3,'out',j,'b')
	connection = pfwrap.connect(j,'out',ar,'data')

	t3.compute()
	rib7=ar





	arf = pfwrap.createNode('PyFlowBase',"makeArray","RibArray")
	arf.setPosition(1800,250)
	arf.setData('preserveLists',True)
	gg.addNode(arf)
	rib1.setPosition(1200,10*5)
	rib4.setPosition(1200,40*5)
	rib7.setPosition(1200,70*5)
	connection = pfwrap.connect(rib1,'out',arf,'data')
	connection = pfwrap.connect(rib4,'out',arf,'data')
	connection = pfwrap.connect(rib7,'out',arf,'data')


	rib2 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","betweenList")
	rib2.setPosition(1400,20*5)
	rib2.setData('m',1)
	gg.addNode(rib2)
	connection = pfwrap.connect(rib1,'out',rib2,'a')
	connection = pfwrap.connect(rib4,'out',rib2,'b')
	connection = pfwrap.connect(rib2,'out',arf,'data')

	rib3 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","betweenList")
	rib3.setPosition(1500,30*5)
	rib3.setData('m',9)
	gg.addNode(rib3)
	connection = pfwrap.connect(rib1,'out',rib3,'a')
	connection = pfwrap.connect(rib4,'out',rib3,'b')
	connection = pfwrap.connect(rib3,'out',arf,'data')

	rib5 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","betweenList")
	rib5.setPosition(1400,50*5)
	rib5.setData('m',1)
	gg.addNode(rib5)
	connection = pfwrap.connect(rib4,'out',rib5,'a')
	connection = pfwrap.connect(rib7,'out',rib5,'b')
	connection = pfwrap.connect(rib5,'out',arf,'data')

	rib6 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","betweenList")
	rib6.setPosition(1500,60*5)
	rib6.setData('m',9)
	gg.addNode(rib6)
	connection = pfwrap.connect(rib4,'out',rib6,'a')
	connection = pfwrap.connect(rib7,'out',rib6,'b')
	connection = pfwrap.connect(rib6,'out',arf,'data')


	bs = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_BSpline","aBSplineSurface")
	gg.addNode(bs)
	bs.setPosition(2000,250)
	connection = pfwrap.connect(arf,'out',bs,'poles')
	bs.compute()

	refresh_gui()


#---------------------------------------------------
# the 4 main icons for new ideas




#--------------------------------------------------------

# some methods for fast testing T1,T2,T3

fn='bb'
fn='project'
fn='compb'

def loadAll():
	showPyFlow()
	try: 
		FreeCAD.getDocument(fn)
	except:
		FreeCAD.open(u"/home/thomas/{}.FCStd".format(fn))
	
	FreeCAD.setActiveDocument(fn)
	FreeCAD.ActiveDocument=FreeCAD.getDocument(fn)
	FreeCADGui.ActiveDocument=FreeCADGui.getDocument(fn)
	loadGraph()
	pass

def saveAll():
	saveGraph()
	FreeCAD.ActiveDocument.saveAs(u"/home/thomas/{}.FCStd".format(fn))
	pass


def view3DExample():
	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	tim = pfwrap.createNode('PyFlowBase',"timer","MyTimer")
	tim.setPosition(200,-200)
	gg.addNode(tim)


	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Box","MyBox")
	t2.setPosition(-200,-100)
	t2.setData("shapeOnly",True)
	t2.compute()
	gg.addNode(t2)


	rib = pfwrap.createFunction('PyFlowFreeCAD',"Vector","workspace")
	rib.setPosition(-100,0)
	gg.addNode(rib)
	
	rib5 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","view3D")
	rib5.setPosition(100,0)
	gg.addNode(rib5)
	connection = pfwrap.connect(t2,'Shape',rib5,'Shape')
	pfwrap.chainExec(t2,rib5)

	connection = pfwrap.connect(rib,'out',rib5,'Workspace')
	refresh_gui()
	pass




def createAllNodesforTests():

	FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	FreeCAD.ActiveDocument.addObject("Part::Box","Box")

	FreeCADGui.Selection.clearSelection()
	FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face1'])
	FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face2'])

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	# erzeuge für alle Nodes ein Objekt und lasse es laufen compute()

	from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import nodelist
	x=0
	y=0
	nodes={}
	for n in nodelist():
		say(n.__name__)
		name=n.__name__
		node=pfwrap.createNode('PyFlowFreeCAD',name,name)
		node.setPosition(x,y)
		gg.addNode(node)
		nodes[name] =node
		x+=200
		if x>7000:
			x=00
			y+= 600

	refresh_gui()
	
	return nodes


def runTestforAllNodes():
	#FreeCAD.nodes=createAllNodesforTest()

	instance=pfwrap.getInstance()
	FreeCAD.gg=pfwrap.getGraphManager().getAllGraphs()[0]
	nodes=FreeCAD.gg.getNodesList()
	errors=[]

	for node in nodes:
		try:
			say(node)
			node.compute()
		except:
			sayexc(str(node))
			errors += [str(node)]
	sayl("done")
	for e in errors:
		say(e)
	say("ERRORS:",len(errors))




def view3DRefandLOD():

	FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	FreeCAD.activeDocument().recompute()

	FreeCADGui.Selection.clearSelection()
	if 10:
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face1'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face2'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face3'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face4'])
	else:
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Cone,['Face1'])

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	rib5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_view3D","view3D")
	rib5.setPosition(100,0)
	gg.addNode(rib5)

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Ref","Ref_Box",b="das ist B")
	t2.compute()
	gg.addNode(t2)

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_LOD","myLOD")
	rib5.setPosition(100,200)
	t2.compute()
	gg.addNode(t2)

	#connection = pfwrap.connect(t2,'Shape',rib5,'Shape')
	refresh_gui()



def LODDemo():


	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	if 0:
		FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
		FreeCAD.ActiveDocument.addObject("Part::Box","Box")
		FreeCAD.ActiveDocument.addObject("Part::Sphere","Sphere")
		FreeCAD.activeDocument().recompute()

		FreeCADGui.Selection.clearSelection()
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face1'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face2'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face3'])
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Box,['Face4'])

		t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Ref","Ref")
		t2.compute()
		gg.addNode(t2)



	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Box","MyBox")
	t2.setPosition(-200,0)
	t2.setData("shapeOnly",True)
	gg.addNode(t2)


	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Sphere","MySphere")
	t2.setPosition(-200,0)
	t2.setData("shapeOnly",True)
	gg.addNode(t2)

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Cone","MyCone")
	t2.setPosition(-200,0)
	t2.setData("shapeOnly",True)
	gg.addNode(t2)
	
	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Toy","MyToy")
	t2.setPosition(-200,0)
	#t2.setData("shapeOnly",True)
	gg.addNode(t2)
	
	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Boolean","Bool")
	t2.setPosition(-200,0)
	#t2.setData("shapeOnly",True)
	gg.addNode(t2)

	rib5 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","view3D")
	rib5.setPosition(100,0)
	rib5.setData("Workspace","LOD_DEMO")
	gg.addNode(rib5)




	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_LOD","myLOD")
	t2.setPosition(100,200)
	
	t2.compute()
	gg.addNode(t2)

	connection = pfwrap.connect(t2,'Shape',rib5,'Shape')
	
	refresh_gui()





def voronoi():


	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Voronoi","myLOD")
	t2.setPosition(100,200)
	
	t2.compute()
	gg.addNode(t2)

	refresh_gui()




def VoronoiforPointcloud():
	'''
	create voroni data for a random list of points
	'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]



	makeInt=pfwrap.createFunction('PyFlowBase',"DefaultLib","makeInt")
	makeInt.setData('i', 50)
	gg.addNode(makeInt)

	v = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","zip")
	gg.addNode(v)

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'x')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'y')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Numpy","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'z')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	gg.addNode(t)
#	connection = pfwrap.connect(v,'out', t,'entity')
	t.compute()

	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Polygon")
	gg.addNode(t)
#	connection = pfwrap.connect(v,'out', t,'points')


	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Voronoi","myVoronoi")
	t2.setPosition(100,200)
	
	#t2.compute()
	#gg.addNode(t2)

	#t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Ref","Ref")
	#t2.compute()
	#gg.addNode(t2)


	refresh_gui()
	say("fertig")



def Geom2dNodes():
	'''
	draw a line Geom2d.LineSegment onto a surface
	and than a circke and an ellipse
	'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	# preprocessing load the environment scene ...
	createBePlane()

	#create a reference node for the face1 of the beplane
	FreeCADGui.Selection.clearSelection()
	FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.BePlane,['Face1'])

	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Ref","Ref_Box",b="das ist B")
	t2.compute()
	gg.addNode(t2)
	t2.setPosition(-200,0)

	# a linesegment on th beplane
	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_2DGeometry","linesegment")
	t.compute()
	gg.addNode(t)
	connection = pfwrap.connect(t2,'Face1', t,'Shape')

	rib5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_view3D","view")
	rib5.setPosition(200,0)
	rib5.setData("Workspace","aa")
	rib5.setData("name","linesegment")
	gg.addNode(rib5)
	connection = pfwrap.connect(t,'Shape_out',rib5,'Shape')
	pfwrap.chainExec(t,rib5)

	# a circle on the beplane
	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_2DCircle","circle")
	t.compute()
	gg.addNode(t)
	connection = pfwrap.connect(t2,'Face1', t,'Shape')

	rib5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_view3D","view")
	rib5.setPosition(200,0)
	rib5.setData("Workspace","aa")
	rib5.setData("name","circle")
	gg.addNode(rib5)
	connection = pfwrap.connect(t,'Shape_out',rib5,'Shape')
	pfwrap.chainExec(t,rib5)

	# an ellipse on the beplane
	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_2DEllipse","circle")
	t.setPosition(-300,-200)
	t.compute()
	gg.addNode(t)
	connection = pfwrap.connect(t2,'Face1', t,'Shape')

	rib5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_view3D","view")
	rib5.setPosition(200,-200)
	rib5.setData("Workspace","aa")
	rib5.setData("name","circle")
	gg.addNode(rib5)
	connection = pfwrap.connect(t,'Shape_out',rib5,'Shape')
	pfwrap.chainExec(t,rib5)


	# an arcof ellipse on the beplane
	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_2DArcOfEllipse","arc_of")
	t.setPosition(-300,-200)
	t.compute()
	gg.addNode(t)
	connection = pfwrap.connect(t2,'Face1', t,'Shape')

	rib5 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_view3D","view")
	rib5.setPosition(200,-200)
	rib5.setData("Workspace","aa")
	rib5.setData("name","arc_of")
	gg.addNode(rib5)
	connection = pfwrap.connect(t,'Shape_out',rib5,'Shape')
	pfwrap.chainExec(t,rib5)


	# todo: hyperbel, parabel  ...
	#+#

	refresh_gui()


def createBePlane():
	'''create an environment with a BePlane and a BeTube'''

	import nurbswb
	import nurbswb.berings
	rc=nurbswb.berings.createBePlane()
	rc.noise=4.
	rc=nurbswb.berings.createBeTube()
	rc.uSize=2000
	rc.vSize=500
	rc.vSegments=5
	rc.noise=500
	FreeCAD.activeDocument().recompute()


def createsomeparts():
	''' default box,cone and sphere for testing'''

	box=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	box2=FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	sphere=FreeCAD.ActiveDocument.addObject("Part::Sphere","Sphere")
	FreeCAD.activeDocument().recompute()


def T1():
	'''test method'''
	sayl("nix")

def T2():
	'''another test'''
	sayl("nix")

def T3():
	sayl("nix3")


def test_AA():

	PartExplorerSubshapeIndexandPlot()

def test_BB():

	refresh_gui()


def test_CC():

	refresh_gui()


def test_DD():
	crossbeamexample()

import FreeCADGui
def clearReportView(name="noname"):
	from PySide import QtGui
	mw=FreeCADGui.getMainWindow()
	r=mw.findChild(QtGui.QTextEdit, "Report view")
	r.clear()
	import time
	now = time.ctime(int(time.time()))
	#FreeCAD.Console.PrintWarning("Cleared Report view " +str(now)+" by " + name+"\n")

def getdescription(pin):
	if pin.description != 'NO Comments':
		return pin.description
	descriptions = {
		'u':'coordiate in uv space',
		'v':'2nd coordiate in uv space',
		'Shape_out': 'resulting shape',
		'Compound_out': 'resulting shape as compound',
		'Shape_in': 'reference shape',
		'Face_in': 'reference face',
		'Edge_in': 'reference edge',
		'display': 'option to create a resulting part',
		'uCount': 'number of u Iso curves',
		'vCount': 'number of v Iso curves',
		'randomize': 'add some random noise to the layout',
		
		}


	try:
		return descriptions[pin.name]
	except:
		return ''


def T3():
	clearReportView()
	packs=pfwrap.getNodesClasses()
	keys=list(packs.keys())
	keys.sort()
	for p in keys:
		if p == 'PyFlowBase':
			continue
		pack=packs[p]
		say("======"+p+"======")
		classNodes = pack.GetNodeClasses()
		cnks=list(classNodes.keys())
		cnks.sort()
		kats={}
		for c in cnks:
			if c[7:] in ['PinsTest']:
				continue 

			if c in [
			'FreeCAD_2DArcOfCircle', 
			'FreeCAD_2DArcOfEllipse', 'FreeCAD_2DArcOfParabola', 'FreeCAD_2DCircle', 'FreeCAD_2DEllipse', 'FreeCAD_2DGeometry', 
			'FreeCAD_Array', 
			'FreeCAD_BSplineCurve', 
			'FreeCAD_BSplineSurface', 
			'FreeCAD_Bar', 
			'FreeCAD_Boolean', 
			'FreeCAD_Box', 
			'FreeCAD_Compound', 
			'FreeCAD_Cone',
			'FreeCAD_Console', 
			'FreeCAD_Destruct_BSpline', 'FreeCAD_Destruct_BSplineSurface', 'FreeCAD_Destruct_Shape', 
			'FreeCAD_Discretize', 
			'FreeCAD_Edge', 'FreeCAD_Face', 
			'FreeCAD_FillEdge', 'FreeCAD_Foo', 
			'FreeCAD_Hull', 'FreeCAD_LOD', 'FreeCAD_Object', 'FreeCAD_Offset', 
			'FreeCAD_Parallelprojection', 'FreeCAD_Part', 'FreeCAD_PartExplorer', 
			'FreeCAD_Perspectiveprojection', 'FreeCAD_PinsTest', 'FreeCAD_Placement', 
			'FreeCAD_Plot', 'FreeCAD_Polygon', 'FreeCAD_Polygon2', 'FreeCAD_Quadrangle', 
			#'FreeCAD_Ref', 'FreeCAD_RefList', 
			'FreeCAD_ShapeIndex', 'FreeCAD_Simplex', 
			'FreeCAD_Solid', 
			'FreeCAD_Sphere', 
			'FreeCAD_Toy', 'FreeCAD_Tread', 
			'FreeCAD_Tripod', 'FreeCAD_UVprojection', 'FreeCAD_VectorArray', 
			'FreeCAD_Voronoi', 
			'FreeCAD_YYY', 
			'FreeCAD_uIso', 
			'FreeCAD_uvGrid', 
			'FreeCAD_vIso', 
			#'FreeCAD_view3D'
			]:
				pass
				#continue
			


			try:
				say("=====FC"+c[7:]+"=====")

				say("/*")
				node = classNodes[c]("nodeName")
				say("*/")
				
#				if node.dok != 2: continue

				# say(c,node)
				# say("-----") # horiz linie
				#say(node.__doc__)
				docs=node.__doc__
				for s in docs.split('\n'):
					say("  "+s.lstrip())
				
				say("[[nodes::{}|More ...]]\n\n".format(c[8:]))
				FreeCAD.n=node
				try:
					kats[node.category()] +=  [c]
				except:
					kats[node.category()] =  [c]

				say("===INPUT PINS===")
				for pin in node.getOrderedPins():
					if str(pin.direction) != 'PinDirection.Input':
						continue
					if pin.name in ['inExec','outExec']:
						continue
					say("**__"+pin.name+"__** ")
					#say(pin.direction)
					#say(pin.name)
					#say()
					say("[["+pin.__class__.__name__+"]]")
					des=getdescription(pin)
					if des !='':
						say(des)
					say()
				say("===OUTPUT PINS===")
				for pin in node.getOrderedPins():
					if str(pin.direction) != 'PinDirection.Output':
						continue

					if pin.name in ['inExec','outExec']:
						continue
					say("**__"+pin.name+"__** ")
					#say(pin.direction)
					#say(pin.name)
					say("[[" + pin.__class__.__name__ + "]]")
					des=getdescription(pin)
					if des  != '':
						say(des)

					say()
					FreeCAD.pin=pin
			except:
				sayErr("problem for ",c)
#	sayl("t3 done")
	say("======Nodes by category======")
	kl=list(kats.keys())
	kl.sort()
	for k in kl:
		say("====={}=====".format(k))
		for c in kats[k]:
			say("[[nodes::{}]]".format(c[8:]))
			say("[[start#fc_{}|/°/  ]]".format(c[8:]))


def reset():
	'''refrehs graph gui'''
	instance=pfwrap.getInstance()
	data = instance.graphManager.get().serialize()
	instance.graphManager.get().clear()
	instance.loadFromData(data)

from PyFlow.UI.Tool.Tool import ShelfTool, DockTool
from PyFlow.UI.Tool import GET_TOOLS
from PyFlow.UI.Tool import REGISTER_TOOL


def displayTools():
	''' tools for pyflow'''

	packageName="PyFlowBase"
	for toolName in ["Properties","NodeBox"]:
		FreeCAD.PF.invokeDockToolByName(packageName, toolName, settings=None)





def displayPreferencesWindow():
    a=pfwrap.getInstance()
    say(a)
    a.showPreferencesWindow()



def createSender():
    a=Blinker()

def createBlinker():
    a=Blinker()
    
def createReceiver():
    a=Receiver()


#------------ move_2 ------------------ 28.11.2019

def  test_AA():
    import FreeCAD
    import FreeCADGui
    App=FreeCAD
    Gui=FreeCADGui
    ### Begin command Std_RecentFiles
    try:
        App.closeDocument('Unnamed')
    except:
        pass
        App.setActiveDocument("")
        App.ActiveDocument=None
        Gui.ActiveDocument=None
    
    FreeCAD.open(u"/home/thomas/Schreibtisch/move_2.FCStd")
    App.setActiveDocument("move_2")
    App.ActiveDocument=App.getDocument("move_2")
    Gui.ActiveDocument=Gui.getDocument("move_2")
    ### End command Std_RecentFiles
    loadGraph()



def getNodebyName(name):
    ''' find a node by its name '''
    g=pfwrap.getGraphManager().getAllGraphs()[0]
    t=g.getNodesList()
    for n in t:
        print("!"+n.name+"!",name)
        say("hu")
        if name==n.name:
                 return n

def test_BB():
    n=getNodebyName("FreeCAD_VectorArray")
    n.compute()
    n=getNodebyName("FreeCAD_VectorArray8")
    n.compute()
     
     
     
