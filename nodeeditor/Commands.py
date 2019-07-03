# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- freecad wrapper for pyflow
#--
#-- microelly 2019 
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import os
os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join([ "PyQt4"])
import Qt
print (Qt)
print Qt.IsPyQt4

from PyFlow.Core.Common import *
from nodeeditor.say import *

import FreeCAD,FreeCADGui

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

import os
import sys
import subprocess
import json
from time import clock
import pkgutil
import uuid

import PyFlowGraph
reload (PyFlowGraph)
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

# the dummy methods for the workbench
def test_BB():
	FreeCAD.Console.PrintMessage("\ntest_B\n")

def test_AA():
	FreeCAD.Console.PrintMessage("\ntest_A\n")


def reset():
	try:
		FreeCAd.t.hide()
	except:
		pass

	if 10:
		import sys
		sms=sys.modules.keys()
		for m in sms:

			if m.startswith('PyFlow'):
				print(m)
				del(sys.modules[m])

	return


def T1():
	''' test Qt environment'''
	import Qt
	say(Qt)
	say(["PyQt4",Qt.IsPyQt4])
	say(["PySide",Qt.IsPySide])
	say(Qt)
	QtCore=Qt.QtCore
	say(QtCore)


def scene_A(instance):
	a=pfwrap.getGraphManager()

	gg=a.getAllGraphs()[0]

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

def scene_B(instance):
	clearGraph()
	a=pfwrap.getGraphManager()

	box=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	box2=FreeCAD.ActiveDocument.addObject("Part::Cone","Cone")
	sphere=FreeCAD.ActiveDocument.addObject("Part::Sphere","Sphere")

	gg=a.getAllGraphs()[0]

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
	connection = pfwrap.connect(fpo,'Object', fpo2,'ObjectA')
	connection = pfwrap.connect(fpo,'outExec', fpo2,'inExec')
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
	


def test_AA():

	instance=pfwrap.getInstance()
	say(instance)
	instance.show()

	a=pfwrap.getGraphManager()

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

	#scene_A(instance)
	scene_B(instance)

	#refresh gui ...
	a=pfwrap.getGraphManager()
	gg=a.getAllGraphs()[0]

	tempd=instance.getTempDirectory()
	fpath=tempd+'/_refreshguiswap.json'
	saveData = gg.serialize()

	with open(fpath, 'w') as f:
		json.dump(saveData, f, indent=4)

	with open(fpath, 'r') as f:
		data = json.load(f)
		instance.loadFromData(data, fpath)



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





def T2():
	# erzeugen PyFlow Fenster
	test_AA()
	# erzeuge eigenes Fesnter und uebernehme die Daten
	a=MyDockWidget(None, "objectname")
	a.show()
	FreeCAD.a=a

def save_and_laod_json_file_test():
	pfwrap.getInstance().load('/home/thomas/Schreibtisch/aa2.json')
	pfwrap.getInstance().save(False,'/home/thomas/Schreibtisch/aa2.json')


def T3():
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
	#showPyFlow()
	pfwrap.getInstance().hide()
	hidePyFlow()
	FreeCAD.open(u"/home/thomas/graph.FCStd")
	loadGraph()


def T2():
	instance=pfwrap.getInstance()
	t=instance.getTempDirectory()
	say(t)
