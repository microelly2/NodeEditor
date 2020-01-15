
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2


#------------------------------------


class FreeCAD_Tripod(FreeCadNodeBase2):
    '''
    position on a surface or curve
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'String','view3d')
        a=self.createInputPin('u', 'Float',0)
        a=self.createInputPin('v', 'Float',0)
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('poles', 'VectorPin',structure=StructureType.Array)
        self.createOutputPin('polesIndex','IntPin',structure=StructureType.Array)
        self.createOutputPin('placement', 'PlacementPin' )
        self.createInputPin("display", 'Boolean', True)
        self.createInputPin("directionNormale", 'Boolean', False)
        self.createInputPin("curvatureMode", 'Boolean', True)
        


    @staticmethod
    def description():
        return FreeCAD_Tripod.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Surface','position','Point','uv']









class FreeCAD_UIso(FreeCadNodeBase2):
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
        a=self.createInputPin('u', 'Float',5)
        self.createOutputPin('Shape_out', 'EdgePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_UIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


import traceback
import inspect

class FreeCAD_VIso(FreeCadNodeBase2):
    '''
    vIso curve on a surface
    '''

    dok = 2
    def __init__(self, name="MyVIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('v', 'Float',5)
        self.createOutputPin('Shape_out', 'EdgePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_VIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_UVGrid(FreeCadNodeBase2):
    '''
    uIso and vIso curves grid
    '''

    def __init__(self, name="myUvGrid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('uCount', 'Integer',5)
        a=self.createInputPin('vCount', 'Integer',5)

        self.createOutputPin('uEdges', 'ShapeListPin').description="list of uIso curve edges"
        self.createOutputPin('vEdges', 'ShapeListPin').description="list of vIso curve edges"
        self.createOutputPin('Shape_out', 'ShapePin').description="all curves as compound"

    @staticmethod
    def description():
        return FreeCAD_UVGrid.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []   
        




class FreeCAD_Voronoi(FreeCadNodeBase2):
    '''
    voronoi cells, delaunay triangulation on a surface for a given set of uv points  on this surface
    '''

    def __init__(self, name="MyVoronoi"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face', 'ShapePin')
        self.createInputPin("useLines", 'Boolean', True)
        a=self.createInputPin("indA", 'Integer', True)

        a.setInputWidgetVariant("MyINPUTVARIANT")

        self.createInputPin("indB", 'Integer', True)
        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'Float', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'Float', structure=StructureType.Array,defaultValue=None)

        a=self.createInputPin("flipArea", 'Boolean', True)

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



class FreeCAD_Hull(FreeCadNodeBase2):
    '''
    delaynay triangulation, convex hull and alpha hull for a given set of points
    '''

    def __init__(self, name="MyHull"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')
        self.createInputPin("singleSimplex", 'Boolean', True)

        a=self.createInputPin("simplex", 'Integer', True)
        a.description="index of the displayed simplex if singleSimplex is set"

        a=self.createInputPin("showFaces", 'Boolean', True)
        a.description="display alpha and convex hull by faces" 

        a=self.createInputPin("alpha", 'Integer', True)

        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'Float', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'Float', structure=StructureType.Array,defaultValue=None)
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








class FreeCAD_Discretize(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyDiscretizeFusion"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
#        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'Integer', True)
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

class FreeCAD_Offset(FreeCadNodeBase2):
    '''
    create a curve around a wire on a face with some offset
    '''

    def __init__(self, name="MyOffset"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'Integer', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'Float', True)
        a=self.createInputPin("height", 'Float', True)

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






class FreeCAD_FillEdge(FreeCadNodeBase2):
    '''
    closed wire to face Part.makeFilledFace
    '''

    def __init__(self, name="MyFillEdge"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("Edges", 'ShapePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)

        a=self.createInputPin("Wire", 'ShapePin', True)
        a.description="closed wire to be filled"

        self.createOutputPin('Shape_out', 'ShapePin').description="filled face"


    @staticmethod
    def description():
        return FreeCAD_FillEdge.__doc__

    @staticmethod
    def category():
        return 'Surfaces'

    @staticmethod
    def keywords():
        return []




class FreeCAD_Solid(FreeCadNodeBase2):
    '''
    make solid of faces
    '''

    def __init__(self, name="MySolid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('bake', 'ExecPin', None, self.bake)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("Shapes", 'ShapePin',structure=StructureType.Array)
        a=self.createInputPin("Faces", 'FacePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Solid.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSpline(FreeCadNodeBase2):
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
        description="flag, whether the curve is periodic/closed or open"
        


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSplineSurface(FreeCadNodeBase2):
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
        description="flag, whether the face is periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


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

        self.pp=self.createInputPin('point', 'VectorPin')
        self.pp.description="list of collected vectors"
#        self.pp.enableOptions(PinOptions.AllowMultipleConnections)
#        self.pp.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createInputPin("maxSize",'Integer',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'Integer',0).\
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

class FreeCAD_ApproximateBSpline(FreeCadNodeBase2):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_ApproximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_InterpolateBSpline(FreeCadNodeBase2):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
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
        description="flag, whether the face is periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_InterpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']


class FreeCAD_Collect_Vectors(FreeCadNodeBase2):
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
        self.createInputPin("maxSize",'Integer',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'Integer',0).\
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

class FreeCAD_ApproximateBSpline(FreeCadNodeBase2):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_ApproximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_InterpolateBSpline(FreeCadNodeBase2):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_InterpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']



class FreeCAD_ConnectPoles(FreeCadNodeBase2):
    '''
    concatenate vectorarrays with the same 2nd axis together along the first axis
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.polesin=self.createInputPin("poles_in",'VectorPin', structure=StructureType.Array)
        self.polesin.enableOptions(PinOptions.AllowMultipleConnections)
        self.polesin.description="connection for multiple 2 dimensional vectorarrays which should be concatenated, they must have the same number of rows"


        a=self.createOutputPin('poles_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 dim array of vectors as base for a grid or bspline surface"
        
        self.createOutputPin('umults_out', 'FloatPin',structure=StructureType.Array).\
        description="list of the multiplicities in the first axis depends on overlay"

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description="a BSplineSurface degree 3 to visualize the poles array"

        a=self.createInputPin('tangentA', 'Float',0)
        a.description="force of the tangents of the first array" 
        
        a=self.createInputPin('tangentB', 'Float',0)
        a.description="force of the tangents of the 2nd array" 

        a=self.createInputPin('overlay', 'Integer',0)
        a.description="0 = concatenate, 1 = calculate mean of the last and first row of two arrays, 2 = add tangent support between the faces"
        #a.setInputWidgetVariant("SimpleSlider")

    @staticmethod
    def description():
        return FreeCAD_ConnectPoles.__doc__

    @staticmethod
    def category():
        return 'VectorArray dim 2'

    @staticmethod
    def keywords():
        return ['matrix','vector','concatenate']


class FreeCAD_FlipSwapArray(FreeCadNodeBase2):
    '''
    flip directions of the vector-array or swap its axes
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("poles_in",'VectorPin', structure=StructureType.Array)
        a.description="2 dim vector array" 

        a=self.createOutputPin('poles_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 dim vector array flipped or swapped poles_in" 
        
        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description="a BSplineSurface degree 3 to visualize the poles array"

        a=self.createInputPin('swap', 'Boolean',0)
        a.description="Flag for swap axes of the array"

        a=self.createInputPin('flipu', 'Boolean',0)
        a.description="Flag for invert u direction of the array"

        a=self.createInputPin('flipv', 'Boolean',0)
        a.description="Flag for invert v direction of the array"


    @staticmethod
    def description():
        return FreeCAD_FlipSwapArray.__doc__

    @staticmethod
    def category():
        return 'VectorArray dim 2'

    @staticmethod
    def keywords():
        return ['flip','swap','Vector']


class FreeCAD_uv2xyz(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("points",'VectorPin', structure=StructureType.Array)
        a=self.createInputPin("Shape",'ShapePin')
      
        a=self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)

class FreeCAD_xyz2uv(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("points",'VectorPin', structure=StructureType.Array)
        a=self.createInputPin("Shape",'ShapePin')
      
        a=self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)


class FreeCAD_replacePoles(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.createInputPin('Shape', 'ShapePin')
        self.createInputPin('poles', 'VectorPin',structure=StructureType.Array)
        self.createInputPin('polesIndex','IntPin',structure=StructureType.Array)
        self.createOutputPin('Shape_out', 'ShapePin')


class FreeCAD_Editor(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.inExec = self.createInputPin("commit", 'ExecPin', None, self.commit)
        self.inExec = self.createInputPin("rollback", 'ExecPin', None, self.rollback)
        
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        
        a=self.createInputPin("position",'VectorPin')

        a=self.createInputPin('u',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('v',"Integer")
        a.setInputWidgetVariant("Slider")
        
        
        self.createInputPin("displayIso", 'Boolean', False)
        
        self.createInputPin("useXYZT", 'Boolean', False)
        

        
        a=self.createInputPin('x',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('y',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('z',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('t',"Integer")
        a.setInputWidgetVariant("Slider")
        

        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position_out', 'VectorPin')
        self.createInputPin("directionNormale", 'Boolean', False)
        self.createOutputPin('u_out', 'FloatPin')
        self.createOutputPin('v_out', 'FloatPin')
        self.createOutputPin('Shape_out', 'ShapePin')

        
    def commit(self,*arg,**kwarg):
        self.shape=self.getPinObject("Shape_out")
        
    def rollback(self,*arg,**kwarg):
        try:
            del(self.shape)
        except:
            pass


class FreeCAD_Editor2(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.inExec = self.createInputPin("commit", 'ExecPin', None, self.commit)
        self.inExec = self.createInputPin("bake", 'ExecPin', None, self.bake)
        self.inExec = self.createInputPin("rollback", 'ExecPin', None, self.rollback)
        
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        
        
        self.createInputPin("useStart", 'Boolean', False)

        a=self.createInputPin('startU',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('startV',"Integer")
        a.setInputWidgetVariant("Slider")
        
        self.createInputPin("displayStart", 'Boolean', False)
        self.createInputPin("useStartPosition", 'Boolean', False)
        a=self.createInputPin("startPosition",'VectorPin')
        
        self.createInputPin("displayTarget", 'Boolean', False)
        a=self.createInputPin("targetPosition",'VectorPin')


		#feineinstellung
        a=self.createInputPin('u',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('v',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('t',"Integer")
        a.setInputWidgetVariant("Slider")
        
        #a=self.createInputPin('ku',"Integer")
        #a.setInputWidgetVariant("Slider")
        #a=self.createInputPin('kv',"Integer")
        #a.setInputWidgetVariant("Slider")
        
        
        self.createInputPin("bordersFrozen", 'Boolean', False)
        self.createInputPin("tangentsFrozen", 'Boolean', False)
        
        self.createInputPin("displayIso", 'Boolean', False)
        
        #self.createInputPin("useXYZT", 'Boolean', False)
        
        a=self.createInputPin('offsetUA', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetUB', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetVA', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetVB', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('scaleU',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('scaleV',"Integer")
        a.setInputWidgetVariant("Slider")
        
        

        
        

        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position_out', 'VectorPin')
        #self.createInputPin("directionNormale", 'Boolean', False)
        self.createOutputPin('u_out', 'FloatPin')
        self.createOutputPin('v_out', 'FloatPin')
        self.createOutputPin('Shape_out', 'ShapePin')

    def bake(self,*arg,**kwarg):
        say("nicht impl")
        

        
    def commit(self,*arg,**kwarg):
        self.shape=self.getPinObject("Shape_out")
        
    def rollback(self,*arg,**kwarg):
        try:
            del(self.shape)
        except:
            pass



def nodelist():
    return [
                FreeCAD_Tripod,

                FreeCAD_UIso, FreeCAD_VIso,
                FreeCAD_UVGrid,

                FreeCAD_Voronoi,
                FreeCAD_Hull,

                FreeCAD_Discretize,
                FreeCAD_Offset,
                FreeCAD_FillEdge,
                FreeCAD_Solid,
                
                FreeCAD_Destruct_BSpline,
                FreeCAD_Destruct_BSplineSurface,
                FreeCAD_Collect_Vectors,
                FreeCAD_ApproximateBSpline,
                FreeCAD_InterpolateBSpline,

                FreeCAD_ConnectPoles,
                FreeCAD_FlipSwapArray,
                
                FreeCAD_uv2xyz,
                FreeCAD_xyz2uv,
                FreeCAD_replacePoles,
                FreeCAD_Editor,
                FreeCAD_Editor2,
                

        ]
