# tools zum zugriff auf pyFlow

import os
os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join([ "PyQt4"])
import Qt

from PyFlow.Core.Common import *
from nodeeditor.say import *
import FreeCAD


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


def deleteInstance():
	FreeCAD.PF.hide()
	#FreeCAD.PF.deleteLater() # geth nicht wegen logger
	#del(FreeCAD.PF)



def getInstance():

	try:
		return FreeCAD.PF
	except:
		pass
	try: INITIALIZE()
	except: pass

	from PyFlow.App import PyFlow
	instance = PyFlow.instance()

	t=instance.windowTitle()
	if not t.startswith("FreeCAD NodeEditor"):
		instance.setWindowTitle("FreeCAD NodeEditor v0.12 @ "+instance.windowTitle())
		instance.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	FreeCAD.PF=instance


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
	sayl("create instance")
	return instance

from PyFlow import(
		INITIALIZE,
		GET_PACKAGES
	)




def getGraphManager():
	return getInstance().graphManager.get()


def createFunction(packageName,libName,functionName):
	packages = GET_PACKAGES()
	lib = packages[packageName].GetFunctionLibraries()[libName]
	defFoos = lib.getFunctions()
	fun = NodeBase.initializeFromFunction(defFoos[functionName])
	return fun


def createNode(packageName,nodeClass,nodeName,**kvargs):
	packages = GET_PACKAGES()
	classNodes = packages[packageName].GetNodeClasses()
	node = classNodes[nodeClass](nodeName,**kvargs)
	return node

def getNodesClasses():
	packages = GET_PACKAGES()
	return packages
#	classNodes = packages[packageName].GetNodeClasses()
#	node = classNodes[nodeClass](nodeName,**kvargs)

def connect(nodeA,pinNameA,nodeB,pinNameB):
	return connectPins(nodeA[str(pinNameA)], nodeB[str(pinNameB)])

def chainExec(nodeA,nodeB):
	return connectPins(nodeA[str('outExec')], nodeB[str('inExec')])
