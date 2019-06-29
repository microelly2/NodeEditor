PACKAGE_NAME = 'PyFlowFreeCAD'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PyFlowFreeCAD.Pins.VectorPin import VectorPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.RotationPin import RotationPin
from PyFlow.Packages.PyFlowFreeCAD.Pins.PlacementPin import PlacementPin

# Function based nodes
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Vector import Vector
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Rotation import Rotation
from PyFlow.Packages.PyFlowFreeCAD.FunctionLibraries.Placement import Placement

# Factories
from PyFlow.Packages.PyFlowFreeCAD.Factories.PinInputWidgetFactory import getInputWidget


_FOO_LIBS = {
    Vector.__name__: Vector(PACKAGE_NAME),
    Rotation.__name__: Rotation(PACKAGE_NAME),
    Placement.__name__: Placement(PACKAGE_NAME),
}

_NODES = {

}

_PINS = {
    VectorPin.__name__: VectorPin,
    RotationPin.__name__: RotationPin,
    PlacementPin.__name__: PlacementPin,
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
