'''

'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2






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





__all__=   [
			FreeCAD_Hull,
			FreeCAD_Voronoi,
            ]


def nodelist():
    return __all__
