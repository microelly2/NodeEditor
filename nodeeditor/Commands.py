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
from nodeeditor.say import *

import FreeCAD,FreeCADGui

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *


import PyFlowGraph

from PyFlowGraph import PyFlowGraph

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

import pfwrap
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


def T1():
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

	with open(fpath, 'r') as f:
		data = json.load(f)
		FreeCAD.data=data
		pfwrap.getInstance().loadFromData(data, fpath)

	pfwrap.getInstance().show()
	clearLogger()
	FreeCADGui.activeDocument().activeView().viewIsometric()
	FreeCADGui.SendMsgToActiveView("ViewFit")


def scene_A():

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

def scene_B():

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


def scene_C():

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


def scene_D():

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]

	FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	FreeCAD.ActiveDocument.addObject("Part::Torus","Torus")
	FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	
	say("huhu")
	t = pfwrap.createNode('PyFlowBase',"imageDisplay","ImageXX")
	t.setPosition(-100,-200)
	t.entity.setData('/home/thomas/Bilder/freeka.png')
	t.compute()
	#t.setData("shapeOnly",True)
	gg.addNode(t)



def scene_D():

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


def scene_Da():

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



def scene_E(instance):
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

def scene_A():
	'''test point listnumpy array flow'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon","MyPolygon")
	t3.setPosition(-100,0)
	gg.addNode(t3)
	t3.compute()

def scene_A():
	'''test point listnumpy array flow'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	t2 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Box","MyBox")
	t2.setPosition(-100,0)
	gg.addNode(t2)

	t3 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Bar","MyPartExplorer")
	t3.setPosition(100,0)
	gg.addNode(t3)
	connection = pfwrap.connect(t2,'Part', t3,'Part_in')

	t4 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Foo","MyIndex")
	t4.setData("shapeOnly",True)
	t4.setPosition(0,-200)
	gg.addNode(t4)

	t4 = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Plot","MyPlot")
	t4.setPosition(100,-200)
	gg.addNode(t4)


	t2.compute()
	t3.compute()
	t4.compute()

def scene_A():
	'''test point listnumpy array flow'''

	instance=pfwrap.getInstance()
	clearGraph()
	gg=pfwrap.getGraphManager().getAllGraphs()[0]


	makeInt=pfwrap.createFunction('PyFlowBase',"DefaultLib","makeInt")
	makeInt.setData('i', 50)
	gg.addNode(makeInt)

	v = pfwrap.createFunction('PyFlowFreeCAD',"Vector","zip")
	gg.addNode(v)
	

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'x')
	connection = pfwrap.connect(makeInt,'out', v1,'size')

	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'y')
	connection = pfwrap.connect(makeInt,'out', v1,'size')


	v1 = pfwrap.createFunction('PyFlowFreeCAD',"Vector","randomList")
	gg.addNode(v1)
	connection = pfwrap.connect(v1,'out', v,'z')
	connection = pfwrap.connect(makeInt,'out', v1,'size')


	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Console","Console")
	t.setPosition(-200,200)
	#t.setData("shapeOnly",True)
	gg.addNode(t)
	connection = pfwrap.connect(v,'out', t,'entity')

	t.compute()
	
	
	t = pfwrap.createNode('PyFlowFreeCAD',"FreeCAD_Polygon2","Polygon")
	#t.setPosition(-200,200)
	gg.addNode(t)
	connection = pfwrap.connect(v,'out', t,'points')
	


def test_AA():

	scene_A()
	refresh_gui()

def test_BB():

	scene_B()
	refresh_gui()


def test_CC():

	scene_C()
	refresh_gui()


def test_DD():

	scene_D()
	refresh_gui()



def reset():
	'''file laden und graph anzeigen testcase'''

	if 'aa' not in FreeCAD.listDocuments().keys():
		FreeCAD.open(u"/home/thomas/aa.FCStd")
	FreeCAD.setActiveDocument("aa")

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
	test_AA()
	# erzeuge eigenes Fesnter und uebernehme die Daten
	a=MyDockWidget(None, "objectname")
	a.show()
	FreeCAD.a=a

def save_and_load_json_file_test():
	pfwrap.getInstance().load('/home/thomas/Schreibtisch/aa2.json')
	pfwrap.getInstance().save(False,'/home/thomas/Schreibtisch/aa2.json')

def T2():
	#FreeCAD.PF.hide()
	#FreeCAD.PF.deleteLater() # geth nicht wegen logger
	#del(FreeCAD.PF)
	pfwrap.getInstance().hide()
	pfwrap.getInstance().show()



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
	'''test clean up graph: delet half of the nodes'''
	instance=pfwrap.getInstance()
	gg=instance.graphManager.get().getAllGraphs()[0]
	for i,n in enumerate(gg.getNodes()):
		if i%2==0: n.kill()

def clearGraph():
	instance=pfwrap.getInstance()
	instance.graphManager.get().clear()

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


def T3():
	box2=FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")


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


