PACKAGE_NAME = 'PyFlowFreeCAD'


from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

from nodeeditor.utils import *

# Factories
from PyFlow.Packages.PyFlowFreeCAD.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.PyFlowFreeCAD.Factories.UINodeFactory import createUINode
#-#



# Pins
#from PyFlow.Packages.PyFlowFreeCAD.Pins.VectorPin import VectorPin

_PINS = {
    #VectorPin.__name__: VectorPin,
}

#from PyFlow.Packages.PyFlowCypher.Pins.CypherPin import nodelist 
#for n in nodelist():
#    _PINS[ n.__name__]=n


# Function based nodes
#from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Vector import Vector

_FOO_LIBS = {
    #Vector.__name__: Vector(PACKAGE_NAME),
}


_NODES = {}

nodelistcol=[]


#from PyFlow.Packages.PyFlowCypher.Nodes.Cypher_Nodes import nodelist
#nodelistcol += nodelist()


if devmode():
	from PyFlow.Packages.PyFlowCypher.Nodes.Cypher_Development import nodelist
	nodelistcol += nodelist()


for n in nodelistcol:
	_NODES[ n.__name__]=n


# tools
_TOOLS = OrderedDict()

#from PyFlow.Packages.PyFlowFreeCAD.Tools.PreviewTool import PreviewTool
#_TOOLS[PreviewTool.__name__] = PreviewTool







#from PyFlow.Packages.PyFlowFreeCAD.Factories.UINodeFactory import createUINode


class PyFlowCypher(IPackage):
    def __init__(self):
        super(PyFlowCypher, self).__init__()
    
    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS
    
    @staticmethod
    def GetNodeClasses():
        return _NODES
    
    @staticmethod
    def GetPinClasses():
        return _PINS
    
    @staticmethod
    def GetToolClasses():
        return _TOOLS
    
    @staticmethod
    def PinsInputWidgetFactory():
        return getInputWidget


#    @staticmethod
 #   def UIPinsFactory():
  #      return createUIPin


    @staticmethod
    def UINodesFactory():
        return createUINode


