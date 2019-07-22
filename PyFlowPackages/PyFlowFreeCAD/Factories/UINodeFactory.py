
#import PyFlow.Packages.PyFlowFreeCAD.UI.UIFreeCAD_ObjectNode

from PyFlow.Packages.PyFlowFreeCAD.UI.UIFreeCAD_ObjectNode import UIFreeCAD_ObjectNode
from PyFlow.Packages.PyFlowFreeCAD.UI.UIFreeCAD_Polygon import UIFreeCAD_PolygonNode

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import FreeCAD_Object
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import FreeCAD_Polygon

from PyFlow.Packages.PyFlowFreeCAD.UI.UIFreeCAD_NodeBase import FreeCADUINodeBase

def createUINode(raw_instance):

    if isinstance(raw_instance, FreeCAD_Object):
        return UIFreeCAD_ObjectNode(raw_instance)

    if isinstance(raw_instance, FreeCAD_Polygon):
        return UIFreeCAD_PolygonNode(raw_instance)

    return  FreeCADUINodeBase(raw_instance)


