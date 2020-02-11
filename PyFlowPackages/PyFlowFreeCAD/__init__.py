PACKAGE_NAME = 'PyFlowFreeCAD'


from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

from nodeeditor.utils import *

# Factories
from PyFlow.Packages.PyFlowFreeCAD.Factories.PinInputWidgetFactory import getInputWidget
#from PyFlow.Packages.PyFlowFreeCAD.Factories.UINodeFactory import createUINode
#-#



# Pins
from PyFlow.Packages.PyFlowFreeCAD.Pins.VectorPin import VectorPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.RotationPin import RotationPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.PlacementPin import PlacementPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.ArrayPin import ArrayPin
#from PyFlow.Packages.PyFlowFreeCAD.Pins.TransformationPin import TransformationPin

_PINS = {
    VectorPin.__name__: VectorPin,
    RotationPin.__name__: RotationPin,
    PlacementPin.__name__: PlacementPin,
    ArrayPin.__name__: ArrayPin,
#    TransformationPin.__name__:TransformationPin,
}

from PyFlow.Packages.PyFlowFreeCAD.Pins.FCobjPin import nodelist 
for n in nodelist():
    _PINS[ n.__name__]=n


# Function based nodes
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Vector import Vector
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Rotation import Rotation
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Placement import Placement
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Numpy import Numpy

from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Datetime import Datetime

_FOO_LIBS = {
    Vector.__name__: Vector(PACKAGE_NAME),
    Rotation.__name__: Rotation(PACKAGE_NAME),
    Placement.__name__: Placement(PACKAGE_NAME),
    Numpy.__name__: Numpy(PACKAGE_NAME),
    Datetime.__name__: Datetime(PACKAGE_NAME),
}


_NODES = {}

nodelistcol=[]


from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Algebra import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Coin import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Combination import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Conversion import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Data import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_File import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Flow import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Geom2D import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_HighLevel import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Image import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Information import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Lambda import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Logic import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Nurbs import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Placement import nodelist
nodelistcol += nodelist()
	
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Primitive import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Projection import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Sensor import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Signal import nodelist
nodelistcol += nodelist()

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Voronoi import nodelist
nodelistcol += nodelist()


if devmode():
	from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Development import nodelist
	nodelistcol += nodelist()


for n in nodelistcol:
	_NODES[ n.__name__]=n


# tools
_TOOLS = OrderedDict()

from PyFlow.Packages.PyFlowFreeCAD.Tools.PreviewTool import PreviewTool
_TOOLS[PreviewTool.__name__] = PreviewTool

from PyFlow.Packages.PyFlowFreeCAD.Tools.ComputeTool import toollist
for t in toollist():
	_TOOLS[t.__name__] = t






from PyFlow.Packages.PyFlowFreeCAD.Factories.UINodeFactory import createUINode


class PyFlowFreeCAD(IPackage):
    def __init__(self):
        super(PyFlowFreeCAD, self).__init__()
    
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


