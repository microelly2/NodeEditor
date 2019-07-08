PACKAGE_NAME = 'PyFlowFreeCAD'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PyFlowFreeCAD.Pins.VectorPin import VectorPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.RotationPin import RotationPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.PlacementPin import PlacementPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.ArrayPin import ArrayPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.FCobjPin import FCobjPin,ShapePin,EnumerationPin


# Function based nodes
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Vector import Vector
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Rotation import Rotation
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Placement import Placement

# Factories
from PyFlow.Packages.PyFlowFreeCAD.Factories.PinInputWidgetFactory import getInputWidget


#from PyFlow.Packages.PyFlowBase.Factories.UIPinFactory import createUIPin
from PyFlow.Packages.PyFlowFreeCAD.Factories.UINodeFactory import createUINode


from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Placement import FreeCAD_Placement
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import FreeCAD_Object,FreeCAD_Toy,FreeCAD_Foo,FreeCAD_Bar

_FOO_LIBS = {
    Vector.__name__: Vector(PACKAGE_NAME),
    Rotation.__name__: Rotation(PACKAGE_NAME),
    Placement.__name__: Placement(PACKAGE_NAME),
}

_NODES = {
	FreeCAD_Placement.__name__: FreeCAD_Placement,
	FreeCAD_Object.__name__: FreeCAD_Object,
	FreeCAD_Toy.__name__: FreeCAD_Toy,
	FreeCAD_Foo.__name__: FreeCAD_Foo,
	FreeCAD_Bar.__name__: FreeCAD_Bar,

}

_PINS = {
    VectorPin.__name__: VectorPin,
    RotationPin.__name__: RotationPin,
    PlacementPin.__name__: PlacementPin,
	ArrayPin.__name__: ArrayPin,
	FCobjPin.__name__: FCobjPin,
	ShapePin.__name__: ShapePin,
	EnumerationPin.__name__: EnumerationPin,
}


_TOOLS = OrderedDict()


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

