import numpy as np
import random
import functools
import time
import inspect

from FreeCAD import Vector
import FreeCAD
import FreeCADGui
import Part


from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

import nodeeditor.store as store
from nodeeditor.utils import *
from nodeeditor.say import *

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase




class FreeCAD_Tripod(FreeCadNodeBase):
    '''
    position on a surface or curve
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d')
        a=self.createInputPin('u', 'FloatPin',0)
        a.recomputeNode=True
        a=self.createInputPin('v', 'FloatPin',0)
        a.recomputeNode=True
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('placement', 'PlacementPin' )
        self.createInputPin("display", 'BoolPin', True)
        self.createInputPin("directionNormale", 'BoolPin', False)
        self.createInputPin("curvatureMode", 'BoolPin', True)
        


    @staticmethod
    def description():
        return FreeCAD_Tripod.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Surface','position','Point','uv']






class FreeCAD_Mouse(FreeCadNodeBase):
    '''
    a Mouse Sensor
    '''


    def __init__(self, name="MouseSensor"):
       super(self.__class__, self).__init__(name)
#       self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.selectionExec = self.createOutputPin("SelectionChanged", 'ExecPin')
       self.createOutputPin('positionApp', 'VectorPin').description="position of the mouse in the Application window"
       self.createOutputPin('positionWindow', 'VectorPin').description="position of the mouse in the ActiveDocument window"
       #self.createOutputPin('Shape_out', 'ShapePin').description="Shape for illustration"
       self.createOutputPin('positionSelection', 'VectorPin').description="position on a selected component"
       
       self.createOutputPin('selectedFace', 'ShapePin')
       self.selectedFaceChanged = self.createOutputPin("selectedFaceChanged", 'ExecPin')
       self.createInputPin("zIndex", 'IntPin')
       
       


    def start(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.start(self,*args, **kwargs)


    def stop(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.stop(self,*args, **kwargs)


    def compute(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Mouse.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['Mouse', 'Keyboard','Position' ]






class FreeCAD_uIso(FreeCadNodeBase):
    '''
    uIso curve on a surface
    '''

    dok= 2
    def __init__(self, name="MyUIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin').\
        description="Face reference"
        a=self.createInputPin('u', 'FloatPin',5)
        a.recomputeNode=True
        self.createInputPin("display", 'BoolPin', True).description="option for display edge as part"
        self.createOutputPin('Edge_out', 'ShapePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_uIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


import traceback
import inspect

class FreeCAD_vIso(FreeCadNodeBase):
    '''
    vIso curve on a surface
    '''

    dok = 2
    def __init__(self, name="MyVIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('v', 'FloatPin',5)
        a.recomputeNode=True
        self.createInputPin("display", 'BoolPin', True).description="option for display edge as part"
        self.createOutputPin('Edge_out', 'ShapePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_vIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_uvGrid(FreeCadNodeBase):
    '''
    uIso and vIso curves grid
    '''

    def __init__(self, name="myUvGrid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('uCount', 'IntPin',5)
        a.recomputeNode=True
        a=self.createInputPin('vCount', 'IntPin',5)
        a.recomputeNode=True
#        self.createInputPin("display", 'BoolPin', True)
        self.createOutputPin('uEdges', 'ShapeListPin').description="list of uIso curve edges"
        self.createOutputPin('vEdges', 'ShapeListPin').description="list of vIso curve edges"
        self.createOutputPin('Compound_out', 'ShapePin').description="all curves as compound"

    @staticmethod
    def description():
        return FreeCAD_uvGrid.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Voronoi(FreeCadNodeBase):
    '''
    voronoi cells, delaunay triangulation on a surface for a given set of uv points  on this surface
    '''

    def __init__(self, name="MyVoronoi"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face', 'ShapePin')
#       a=self.createInputPin('uCount', 'IntPin',5)
#       a.recomputeNode=True
#       a=self.createInputPin('vCount', 'IntPin',5)
#       a.recomputeNode=True
        self.createInputPin("useLines", 'BoolPin', True)
        a=self.createInputPin("indA", 'IntPin', True)
        a.recomputeNode=True
        a.setInputWidgetVariant("MyINPUTVARIANT")

        a=self.createInputPin("flipArea", 'BoolPin', True)
        a.recomputeNode=True
        self.createInputPin("indB", 'IntPin', True)
        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'FloatPin', structure=StructureType.Array,defaultValue=None)

        self.createOutputPin('Points', 'ShapePin')
        self.createOutputPin('convexHull', 'ShapePin')
        self.createOutputPin('delaunayTriangles', 'ShapePin')
        self.createOutputPin('voronoiCells', 'ShapePin')


    @staticmethod
    def description():
        return FreeCAD_Voronoi.__doc__

    @staticmethod
    def category():
        return 'Voronoi'

    @staticmethod
    def keywords():
        return ['convex','Hull','Delaunay','Cell']



class FreeCAD_Hull(FreeCadNodeBase):
    '''
    delaynay triangulation, convex hull and alpha hull for a given set of points
    '''

    def __init__(self, name="MyHull"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')
        self.createInputPin("singleSimplex", 'BoolPin', True)

        a=self.createInputPin("simplex", 'IntPin', True)
        a.recomputeNode=True
        a.description="index of the displayd simplex if singleSimplex is set"
#       a.setInputWidgetVariant("MyINPUTVARIANT")

        a=self.createInputPin("showFaces", 'BoolPin', True)
        a.recomputeNode=True
        a.description="display alpha and convex hull by faces" 

        a=self.createInputPin("alpha", 'IntPin', True)
        a.recomputeNode=True

        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        #self.createOutputPin('edges', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createOutputPin('Points', 'ShapePin')
        self.createOutputPin('convexHull', 'ShapePin')
        self.createOutputPin('delaunayTriangles', 'ShapePin')
        self.createOutputPin('alphaHull', 'ShapePin').description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Hull.__doc__

    @staticmethod
    def category():
        return 'Voronoi'

    @staticmethod
    def keywords():
        return ['Convex','delaunay','alpha hull']




class FreeCAD_2DGeometry(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="Geo2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("ua", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("va", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("ub", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vb", 'FloatPin', True)
        a.recomputeNode=True

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DGeometry.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []



class FreeCAD_2DCircle(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyCircle2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("u", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("v", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("radius", 'FloatPin', True)
        a.recomputeNode=True

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DCircle.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DEllipse(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfEllipse(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfEllipse.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfParabola(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfParabola2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfParabola.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfCircle(FreeCadNodeBase):
    '''
    2d Geometry object - arc of a circle

    an arc is created in uv space and 
    mapped to a reference face
    '''

    dok = 2

    def __init__(self, name="MyArcOfCircle2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin').\
        description="Face1 of this shape defines the uv space for the arc representation, default is the xy plane"

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a.description="first coordinate of the center"
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True
        a.description="2nd coordinate of the center"

        a=self.createInputPin("radius", 'FloatPin', True)
        a.recomputeNode=True
        a.description="radius of the circle"

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a.description="angle of the starting point of the arc"
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        a.description="angle of the ending point of the arc"
        

        self.createOutputPin('Shape_out', 'ShapePin').\
            description="the projection of the geometry onto the Face1 of Shape_in"
        self.createOutputPin('geometry', 'ShapePin').\
            description='2D Arc of Circle geometry object'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfCircle.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []




class FreeCAD_Simplex(FreeCadNodeBase):
    '''
    Tetraeder
    '''

    def __init__(self, name="MySimplex"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin("noise", 'FloatPin', True)

        a=self.createInputPin("pointA", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,0,0))

        a=self.createInputPin("pointB", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(10,0,0))
        a=self.createInputPin("pointC", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,10,0))
        a=self.createInputPin("pointD", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,0,10))

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Simplex.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Tread(FreeCadNodeBase):
    '''
    Schindel oder Stufe
    '''

    def __init__(self, name="MyTread"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("noise", 'FloatPin', True)

        a=range(8)
        for i in range(8):
            a[i]=self.createInputPin("point_"+str(i), 'VectorPin', True)
            a[i].recomputeNode=True

        v=[
            Vector(0,20),
            Vector(30,20),
            Vector(30,0),
            Vector(80,0),
            
            Vector(80,10),
            Vector(40,10),
            Vector(40,30),
            Vector(0,30),
        ]
        for i in range(8):
            a[i].setData(v[i])

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Tread(self,produce=True)


class FreeCAD_Discretize(FreeCadNodeBase):
    '''
    '''

    def __init__(self, name="MyDiscretizeFusion"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
#        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Discretize.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def XXproduce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Tread(self,produce=True)

class FreeCAD_Offset(FreeCadNodeBase):
    '''
    create a curve around a wire on a face with some offset
    '''

    def __init__(self, name="MyOffset"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'FloatPin', True)
        a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Offset.__doc__

    @staticmethod
    def category():
        return 'Curves'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)






class FreeCAD_FillEdge(FreeCadNodeBase):
    '''
    closed edge to face
    '''

    def __init__(self, name="MyFillEdge"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'FloatPin', True)
        a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'Surfaces'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)



class FreeCAD_Solid(FreeCadNodeBase):
    '''
    make solid of faces
    '''

    def __init__(self, name="MySolid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('bake', 'ExecPin', None, self.bake)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        #a=self.createInputPin("count", 'IntPin', True)
        #a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shapes", 'ShapePin',structure=StructureType.Array)
        a=self.createInputPin("Faces", 'FacePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        #a=self.createInputPin("offset", 'FloatPin', True)
        #a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def Xproduce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)

# autum 2019 ...

class FreeCAD_Destruct_BSpline(FreeCadNodeBase):
    '''
    provides the parameters of a bspline edge object
    '''
    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout.description="Shape which has exactly one edge, this edge is explored"

        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="list of the poles vectors"
        self.createOutputPin('knots', 'FloatPin',structure=StructureType.Array).\
        description="list of the knots"
        self.createOutputPin('mults', 'IntPin',structure=StructureType.Array).\
        description="list of the multiplicities"
        self.createOutputPin('degree', 'IntPin').\
        description="degree of the curve"
        
        self.createOutputPin('periodic', 'BoolPin').\
        description="flag, wheter the curve is periodic/closed or open"
        


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSplineSurface(FreeCadNodeBase):
    '''
    provides the parameters of a bspline surface object
    '''
    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')




class FreeCAD_Tripod(FreeCadNodeBase):
    '''
    position on a surface or curve
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d')
        a=self.createInputPin('u', 'FloatPin',0)
        a.recomputeNode=True
        a=self.createInputPin('v', 'FloatPin',0)
        a.recomputeNode=True
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('placement', 'PlacementPin' )
        self.createInputPin("display", 'BoolPin', True)
        self.createInputPin("directionNormale", 'BoolPin', False)
        self.createInputPin("curvatureMode", 'BoolPin', True)
        


    @staticmethod
    def description():
        return FreeCAD_Tripod.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Surface','position','Point','uv']






class FreeCAD_Mouse(FreeCadNodeBase):
    '''
    a Mouse Sensor
    '''


    def __init__(self, name="MouseSensor"):
       super(self.__class__, self).__init__(name)
#       self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.selectionExec = self.createOutputPin("SelectionChanged", 'ExecPin')
       self.createOutputPin('positionApp', 'VectorPin').description="position of the mouse in the Application window"
       self.createOutputPin('positionWindow', 'VectorPin').description="position of the mouse in the ActiveDocument window"
       #self.createOutputPin('Shape_out', 'ShapePin').description="Shape for illustration"
       self.createOutputPin('positionSelection', 'VectorPin').description="position on a selected component"
       
       self.createOutputPin('selectedFace', 'ShapePin')
       self.selectedFaceChanged = self.createOutputPin("selectedFaceChanged", 'ExecPin')
       self.createInputPin("zIndex", 'IntPin')
       
       


    def start(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.start(self,*args, **kwargs)


    def stop(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.stop(self,*args, **kwargs)


    def compute(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Mouse.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['Mouse', 'Keyboard','Position' ]






class FreeCAD_uIso(FreeCadNodeBase):
    '''
    uIso curve on a surface
    '''

    dok= 2
    def __init__(self, name="MyUIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin').\
        description="Face reference"
        a=self.createInputPin('u', 'FloatPin',5)
        a.recomputeNode=True
        self.createInputPin("display", 'BoolPin', True).description="option for display edge as part"
        self.createOutputPin('Edge_out', 'ShapePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_uIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


import traceback
import inspect

class FreeCAD_vIso(FreeCadNodeBase):
    '''
    vIso curve on a surface
    '''

    dok = 2
    def __init__(self, name="MyVIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('v', 'FloatPin',5)
        a.recomputeNode=True
        self.createInputPin("display", 'BoolPin', True).description="option for display edge as part"
        self.createOutputPin('Edge_out', 'ShapePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_vIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_uvGrid(FreeCadNodeBase):
    '''
    uIso and vIso curves grid
    '''

    def __init__(self, name="myUvGrid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('uCount', 'IntPin',5)
        a.recomputeNode=True
        a=self.createInputPin('vCount', 'IntPin',5)
        a.recomputeNode=True
#        self.createInputPin("display", 'BoolPin', True)
        self.createOutputPin('uEdges', 'ShapeListPin').description="list of uIso curve edges"
        self.createOutputPin('vEdges', 'ShapeListPin').description="list of vIso curve edges"
        self.createOutputPin('Compound_out', 'ShapePin').description="all curves as compound"

    @staticmethod
    def description():
        return FreeCAD_uvGrid.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []	
        




class FreeCAD_Voronoi(FreeCadNodeBase):
    '''
    voronoi cells, delaunay triangulation on a surface for a given set of uv points  on this surface
    '''

    def __init__(self, name="MyVoronoi"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face', 'ShapePin')
#       a=self.createInputPin('uCount', 'IntPin',5)
#       a.recomputeNode=True
#       a=self.createInputPin('vCount', 'IntPin',5)
#       a.recomputeNode=True
        self.createInputPin("useLines", 'BoolPin', True)
        a=self.createInputPin("indA", 'IntPin', True)
        a.recomputeNode=True
        a.setInputWidgetVariant("MyINPUTVARIANT")

        a=self.createInputPin("flipArea", 'BoolPin', True)
        a.recomputeNode=True
        self.createInputPin("indB", 'IntPin', True)
        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'FloatPin', structure=StructureType.Array,defaultValue=None)

        self.createOutputPin('Points', 'ShapePin')
        self.createOutputPin('convexHull', 'ShapePin')
        self.createOutputPin('delaunayTriangles', 'ShapePin')
        self.createOutputPin('voronoiCells', 'ShapePin')


    @staticmethod
    def description():
        return FreeCAD_Voronoi.__doc__

    @staticmethod
    def category():
        return 'Voronoi'

    @staticmethod
    def keywords():
        return ['convex','Hull','Delaunay','Cell']



class FreeCAD_Hull(FreeCadNodeBase):
    '''
    delaynay triangulation, convex hull and alpha hull for a given set of points
    '''

    def __init__(self, name="MyHull"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')
        self.createInputPin("singleSimplex", 'BoolPin', True)

        a=self.createInputPin("simplex", 'IntPin', True)
        a.recomputeNode=True
        a.description="index of the displayd simplex if singleSimplex is set"
#       a.setInputWidgetVariant("MyINPUTVARIANT")

        a=self.createInputPin("showFaces", 'BoolPin', True)
        a.recomputeNode=True
        a.description="display alpha and convex hull by faces" 

        a=self.createInputPin("alpha", 'IntPin', True)
        a.recomputeNode=True

        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        #self.createOutputPin('edges', 'FloatPin', structure=StructureType.Array,defaultValue=None)
        self.createOutputPin('Points', 'ShapePin')
        self.createOutputPin('convexHull', 'ShapePin')
        self.createOutputPin('delaunayTriangles', 'ShapePin')
        self.createOutputPin('alphaHull', 'ShapePin').description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Hull.__doc__

    @staticmethod
    def category():
        return 'Voronoi'

    @staticmethod
    def keywords():
        return ['Convex','delaunay','alpha hull']




class FreeCAD_2DGeometry(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="Geo2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("ua", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("va", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("ub", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vb", 'FloatPin', True)
        a.recomputeNode=True

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DGeometry.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []



class FreeCAD_2DCircle(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyCircle2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("u", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("v", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("radius", 'FloatPin', True)
        a.recomputeNode=True

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DCircle.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DEllipse(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfEllipse(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfEllipse.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfParabola(FreeCadNodeBase):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfParabola2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("direction", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("MajorRadius", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("MinorRadius", 'FloatPin', True)
        a.recomputeNode=True

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfParabola.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_2DArcOfCircle(FreeCadNodeBase):
    '''
    2d Geometry object - arc of a circle

    an arc is created in uv space and 
    mapped to a reference face
    '''

    dok = 2

    def __init__(self, name="MyArcOfCircle2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin').\
        description="Face1 of this shape defines the uv space for the arc representation, default is the xy plane"

        a=self.createInputPin("uLocation", 'FloatPin', True)
        a.recomputeNode=True
        a.description="first coordinate of the center"
        a=self.createInputPin("vLocation", 'FloatPin', True)
        a.recomputeNode=True
        a.description="2nd coordinate of the center"

        a=self.createInputPin("radius", 'FloatPin', True)
        a.recomputeNode=True
        a.description="radius of the circle"

        a=self.createInputPin("startAngle", 'FloatPin', True)
        a.recomputeNode=True
        a.description="angle of the starting point of the arc"
        a=self.createInputPin("endAngle", 'FloatPin', True)
        a.recomputeNode=True
        a.description="angle of the ending point of the arc"
        

        self.createOutputPin('Shape_out', 'ShapePin').\
            description="the projection of the geometry onto the Face1 of Shape_in"
        self.createOutputPin('geometry', 'ShapePin').\
            description='2D Arc of Circle geometry object'


    @staticmethod
    def description():
        return FreeCAD_2DArcOfCircle.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []




class FreeCAD_Simplex(FreeCadNodeBase):
    '''
    Tetraeder
    '''

    def __init__(self, name="MySimplex"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin("noise", 'FloatPin', True)

        a=self.createInputPin("pointA", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,0,0))

        a=self.createInputPin("pointB", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(10,0,0))
        a=self.createInputPin("pointC", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,10,0))
        a=self.createInputPin("pointD", 'VectorPin', True)
        a.recomputeNode=True
        a.setData(Vector(0,0,10))

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Simplex.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Tread(FreeCadNodeBase):
    '''
    Schindel oder Stufe
    '''

    def __init__(self, name="MyTread"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("noise", 'FloatPin', True)

        a=range(8)
        for i in range(8):
            a[i]=self.createInputPin("point_"+str(i), 'VectorPin', True)
            a[i].recomputeNode=True

        v=[
            Vector(0,20),
            Vector(30,20),
            Vector(30,0),
            Vector(80,0),
            
            Vector(80,10),
            Vector(40,10),
            Vector(40,30),
            Vector(0,30),
        ]
        for i in range(8):
            a[i].setData(v[i])

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Tread(self,produce=True)


class FreeCAD_Discretize(FreeCadNodeBase):
    '''
    '''

    def __init__(self, name="MyDiscretizeFusion"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
#        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Discretize.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def XXproduce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Tread(self,produce=True)

class FreeCAD_Offset(FreeCadNodeBase):
    '''
    create a curve around a wire on a face with some offset
    '''

    def __init__(self, name="MyOffset"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'FloatPin', True)
        a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Offset.__doc__

    @staticmethod
    def category():
        return 'Curves'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)






class FreeCAD_FillEdge(FreeCadNodeBase):
    '''
    closed edge to face
    '''

    def __init__(self, name="MyFillEdge"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'IntPin', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'FloatPin', True)
        a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'Surfaces'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)



class FreeCAD_Solid(FreeCadNodeBase):
    '''
    make solid of faces
    '''

    def __init__(self, name="MySolid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('bake', 'ExecPin', None, self.bake)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        #a=self.createInputPin("count", 'IntPin', True)
        #a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shapes", 'ShapePin',structure=StructureType.Array)
        a=self.createInputPin("Faces", 'FacePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        #a=self.createInputPin("offset", 'FloatPin', True)
        #a=self.createInputPin("height", 'FloatPin', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_2DEllipse.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def Xproduce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)

# autum 2019 ...

class FreeCAD_Destruct_BSpline(FreeCadNodeBase):
    '''
    provides the parameters of a bspline edge object
    '''
    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout.description="Shape which has exactly one edge, this edge is explored"

        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="list of the poles vectors"
        self.createOutputPin('knots', 'FloatPin',structure=StructureType.Array).\
        description="list of the knots"
        self.createOutputPin('mults', 'IntPin',structure=StructureType.Array).\
        description="list of the multiplicities"
        self.createOutputPin('degree', 'IntPin').\
        description="degree of the curve"
        
        self.createOutputPin('periodic', 'BoolPin').\
        description="flag, wheter the curve is periodic/closed or open"
        


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSplineSurface(FreeCadNodeBase):
    '''
    provides the parameters of a bspline surface object
    '''
    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout.description="Shape which has exactly one face, this edge is explored"


        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="array of the poles vectors"
        self.createOutputPin('uknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'BoolPin').\
        description="flag, wheter the faceis periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, wheter the faceis periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []




# ---------
#


class FreeCAD_Collect_Vectors(FreeCadNodeBase):
    '''
    collect vectors to a list
    '''
    dok=2 
    def __init__(self, name="MyCollection"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inReset = self.createInputPin("reset", 'ExecPin', None, self.reset)
        self.inReset.description="clear the list of collected points"
        self.inRefresh = self.createInputPin("refresh", 'ExecPin', None, self.refresh)
        self.inRefresh.description="update the outpin **points**"
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('point', 'VectorPin').\
        description="list of collected vectors"
        self.createInputPin("maxSize",'IntPin',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'IntPin',0).\
        description="create only a discretized list of the polygon with this size"

        a=self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        a.description="list of collected vectors"
        
        self.points=[]

    @staticmethod
    def description():
        return FreeCAD_Collect_Vectors.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return ['point','collect']

    def reset(self,*args, **kwargs):
        say("reset")
        self.compute(mode="reset")

    @timer
    def reset(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="reset")


    def refresh(self,*args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="refresh")
        self.outExec.call()

class FreeCAD_approximateBSpline(FreeCadNodeBase):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''
    dok=2 
    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'FloatPin',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_approximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_interpolateBSpline(FreeCadNodeBase):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''
    dok=2 
    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'FloatPin',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True






        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="array of the poles vectors"
        self.createOutputPin('uknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'BoolPin').\
        description="flag, wheter the faceis periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, wheter the faceis periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_interpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']



# ---------
#


class FreeCAD_Collect_Vectors(FreeCadNodeBase):
    '''
    collect vectors to a list
    '''
    dok=2 
    def __init__(self, name="MyCollection"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inReset = self.createInputPin("reset", 'ExecPin', None, self.reset)
        self.inReset.description="clear the list of collected points"
        self.inRefresh = self.createInputPin("refresh", 'ExecPin', None, self.refresh)
        self.inRefresh.description="update the outpin **points**"
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('point', 'VectorPin').\
        description="list of collected vectors"
        self.createInputPin("maxSize",'IntPin',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'IntPin',0).\
        description="create only a discretized list of the polygon with this size"

        a=self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        a.description="list of collected vectors"
        
        self.points=[]

    @staticmethod
    def description():
        return FreeCAD_Collect_Vectors.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return ['point','collect']

    def reset(self,*args, **kwargs):
        say("reset")
        self.compute(mode="reset")

    @timer
    def reset(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="reset")


    def refresh(self,*args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="refresh")
        self.outExec.call()

class FreeCAD_approximateBSpline(FreeCadNodeBase):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''
    dok=2 
    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'FloatPin',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_approximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_interpolateBSpline(FreeCadNodeBase):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''
    dok=2 
    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'FloatPin',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_interpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']



def nodelist():
    return [
#                FreeCAD_Bar,
                FreeCAD_Mouse,
                FreeCAD_Tripod,
#                FreeCAD_YYY,
                FreeCAD_uIso, FreeCAD_vIso,
                FreeCAD_uvGrid,
                FreeCAD_Voronoi,
                FreeCAD_Hull,

                FreeCAD_2DGeometry,
                FreeCAD_2DCircle,
                FreeCAD_2DEllipse,
                FreeCAD_2DArcOfEllipse,
                FreeCAD_2DArcOfParabola,
                FreeCAD_2DArcOfCircle,

                FreeCAD_Simplex,
                FreeCAD_Tread,
                FreeCAD_Discretize,
                FreeCAD_Offset,
                FreeCAD_FillEdge,
                FreeCAD_Solid,
                
                FreeCAD_Destruct_BSpline,
                FreeCAD_Destruct_BSplineSurface,
                FreeCAD_Collect_Vectors,
                FreeCAD_approximateBSpline,
                FreeCAD_interpolateBSpline,

        ]
