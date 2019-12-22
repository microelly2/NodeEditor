
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase


#------------------------------------


class FreeCAD_Tripod(FreeCadNodeBase):
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









class FreeCAD_UIso(FreeCadNodeBase):
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

class FreeCAD_VIso(FreeCadNodeBase):
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


class FreeCAD_UVGrid(FreeCadNodeBase):
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
        




class FreeCAD_Voronoi(FreeCadNodeBase):
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



class FreeCAD_Hull(FreeCadNodeBase):
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
        a.description="index of the displayd simplex if singleSimplex is set"

        a=self.createInputPin("showFaces", 'Boolean', True)
        a.description="display alpha and convex hull by faces" 

        a=self.createInputPin("alpha", 'Integer', True)

        self.createOutputPin('uEdges', 'ShapeListPin')
        self.createOutputPin('vEdges', 'ShapeListPin')
        self.createInputPin('uList', 'Float', structure=StructureType.Array,defaultValue=None)
        self.createInputPin('vList', 'Float', structure=StructureType.Array,defaultValue=None)
        #self.createOutputPin('edges', 'Float', structure=StructureType.Array,defaultValue=None)
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








class FreeCAD_Discretize(FreeCadNodeBase):
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

class FreeCAD_Offset(FreeCadNodeBase):
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






class FreeCAD_FillEdge(FreeCadNodeBase):
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




class FreeCAD_Solid(FreeCadNodeBase):
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
        self.createOutputPin('knots', 'Float',structure=StructureType.Array).\
        description="list of the knots"
        self.createOutputPin('mults', 'Integer',structure=StructureType.Array).\
        description="list of the multiplicities"
        self.createOutputPin('degree', 'Integer').\
        description="degree of the curve"
        
        self.createOutputPin('periodic', 'Boolean').\
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
        self.createOutputPin('uknots', 'Float',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'Integer',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'Integer').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'Boolean').\
        description="flag, wheter the faceis periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'Float',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'Integer',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'Integer').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'Boolean').\
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

class FreeCAD_ApproximateBSpline(FreeCadNodeBase):
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


class FreeCAD_InterpolateBSpline(FreeCadNodeBase):
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
        self.createOutputPin('uknots', 'Float',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'Integer',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'Integer').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'Boolean').\
        description="flag, wheter the faceis periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'Float',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'Integer',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'Integer').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'Boolean').\
        description="flag, wheter the faceis periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_InterpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']


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

class FreeCAD_ApproximateBSpline(FreeCadNodeBase):
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


class FreeCAD_InterpolateBSpline(FreeCadNodeBase):
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



class FreeCAD_ConnectPoles(FreeCadNodeBase):
    '''
    concatenate vectorarrays with the same 2nd axis together along the first axis
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.polesin=self.createInputPin("poles_in",'VectorPin', structure=StructureType.Array)
        self.polesin.enableOptions(PinOptions.AllowMultipleConnections)
        self.polesin.description="connection for multiple 2 dimensional vectorarrays which sould be concatenated, they must have the same numver of rows"


        a=self.createOutputPin('poles_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 dim array of vectors as base for a grid or bspline surface"
        
        self.createOutputPin('umults_out', 'Float',structure=StructureType.Array).\
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


class FreeCAD_FlipSwapArray(FreeCadNodeBase):
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

        ]
