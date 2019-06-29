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


def test_BB():
	'''einbetten in freecad'''

	try: INITIALIZE()
	except: pass

	#from PyFlow.App import PyFlow
	import PyFlow.App
	reload(PyFlow.App)
	from PyFlow.FCApp import PyFlow

	instance = PyFlow.instance()
	
	print("instance----------",instance)

	FreeCAD.PF=instance
	instance.show()



def T3():
	'''alternatives Fesnter moit graphics view'''
	from Qt import QtCore
	from Qt import QtGui
	from Qt import QtWidgets
	from Qt.QtWidgets import *

	a=QGraphicsView()


	b=QWidget()
	l=QVBoxLayout()
	b.setLayout(l)
	l.addWidget(a)

	a=QPushButton("HUHU")
	l.addWidget(a)

	d=QPushButton("odod")
	l.addWidget(d)

	b.show()
	FreeCAD.b=b


def test_AA():
	'''neuer start version 25.juni'''
	try: INITIALIZE()
	except: pass

	from PyFlow.App import PyFlow
	#from PyFlow.FCApp import PyFlow

	instance = PyFlow.instance()
	print("instance-----II-----",instance)

	instance.show()
	FreeCAD.PF=instance

	a=FreeCAD.PF.graphManager.get()


	#versuch gescripted afuzusetzen

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

	print "huhu"
	if 1:
		packages = GET_PACKAGES()
		gg=a.getAllGraphs()[0]
		if 0:
			fn=packages['PF_FreeCAD'].GetNodeClasses()["FreeCAD_Node"]
			f=fn('MyFreeCadNode')
			f.setPosition(50,-100)

			gg.addNode(f)

		defaultLibFoos = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"].getFunctions()
		randLibFoos = packages['PyFlowBase'].GetFunctionLibraries()["RandomLib"].getFunctions()

#		f = NodeBase.initializeFromFunction(defaultLibFoos["makeInt"])
#		say("makeInt node:",f)
#		gg.addNode(f)

		packages = GET_PACKAGES()
		lib = packages['PyFlowBase'].GetFunctionLibraries()["MathAbstractLib"]
		sayl("lib",lib)
		defaultLib = packages['PyFlowBase'].GetFunctionLibraries()["DefaultLib"]
		classNodes = packages['PyFlowBase'].GetNodeClasses()
		foos = lib.getFunctions()
		#say("foos",foos)
		defFoos = defaultLib.getFunctions()

		makeInt = NodeBase.initializeFromFunction(defFoos["makeInt"])
		addNode2 = NodeBase.initializeFromFunction(foos["add"])
		printNode = classNodes["consoleOutput"]("printer")
		say(makeInt)
		say("addnode2",addNode2)

		gg.addNode(makeInt)
		gg.addNode(addNode2)
		gg.addNode(printNode)
		makeInt.setPosition(-200,-150)
		addNode2.setPosition(-150,-70)
		printNode.setPosition(200,-100)

		makeInt.setData('i', 5)

		# freecad nodes erstellen -vector
		fclib = packages['PyFlowFreeCAD'].GetFunctionLibraries()["Vector"]
		fcfoos = fclib.getFunctions()
		fa = NodeBase.initializeFromFunction(fcfoos["vecAdd"])
		gg.addNode(fa)
		fa.setData('a', FreeCAD.Vector(1,2,3))
		connection = connectPins(fa[str('out')], printNode[str('entity')])

		fb = NodeBase.initializeFromFunction(fcfoos["vecAdd"])
		gg.addNode(fb)
		fb.setData('a', FreeCAD.Vector(1,2,3))
		fb.setData('b', FreeCAD.Vector(-3,-5,-6))
		connection = connectPins(fb[str('out')], fa[str('b')])

		fb.setPosition(-100,0)
		fa.setPosition(100,0)

		#rotation
		rotfoos = packages['PyFlowFreeCAD'].GetFunctionLibraries()["Rotation"].getFunctions()
		ra = NodeBase.initializeFromFunction(rotfoos["rotMultiply"])
		ra.setPosition(-300,100)
		gg.addNode(ra)

		#placement
		if 10:
			pmfoos = packages['PyFlowFreeCAD'].GetFunctionLibraries()["Placement"].getFunctions()
			print pmfoos
			pa = NodeBase.initializeFromFunction(pmfoos["pmMultiply"])
			pa.setPosition(-200,100)
			gg.addNode(pa)

			pa = NodeBase.initializeFromFunction(pmfoos["pmCreate"])
			pa.setPosition(-100,100)
			gg.addNode(pa)



	fpath='/home/thomas/Schreibtisch/ax.json'
	saveData = gg.serialize()
	#say( "saveData",saveData)
	say("------------------")
	#return
	with open(fpath, 'w') as f:
		json.dump(saveData, f, indent=4)

	with open(fpath, 'r') as f:
		data = json.load(f)
		#print "data",data
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

		w=FreeCAD.PF
		w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
		
		l.addWidget(FreeCAD.PF.canvasWidget)


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

def T3():
	FreeCAD.PF.load('/home/thomas/Schreibtisch/aa2.json')
	FreeCAD.PF.save(False,'/home/thomas/Schreibtisch/aa4.json')


def T3():
	FreeCADGui.runCommand("Std_Quit")
