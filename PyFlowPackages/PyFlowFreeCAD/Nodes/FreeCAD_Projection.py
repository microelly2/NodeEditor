'''
mapping objects onto faces
'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2


class FreeCAD_Parallelprojection(FreeCadNodeBase2):
    '''
    parallal projection of an edge onto a face
    '''

    def __init__(self, name="MyParallelProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"
        
        p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
        p.recomputeNode=True
        p.description="direction of the projection light"


    @staticmethod
    def description():
        return FreeCAD_Parallelprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Perspectiveprojection(FreeCadNodeBase2):
    '''
    perspective projection of an edge onto a face
    '''

    def __init__(self, name="MyPerspectiveProjection"):
        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"
        
        p=self.createInputPin('center', 'VectorPin',FreeCAD.Vector(0,0,1000))
        p.recomputeNode=True
        p.description="center of projection, position of the point light"


    @staticmethod
    def description():
        return FreeCAD_Perspectiveprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []


class FreeCAD_UVprojection(FreeCadNodeBase2):
    '''
    uv projection of an edge onto a face
    the curve is discretized,
    the points are mapped 
    and a interpolated curve is computed
    '''

    def __init__(self, name="MyUVProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"

        p=self.createInputPin('pointCount', 'Integer',20)
        p.description="number of points of the edge used for constructing the curve"

    # zum aufpolstern #+# trennen in zweite node!
        p=self.createInputPin('inverse', 'Boolean')
        p=self.createInputPin('Extrusion', 'Boolean')
        p=self.createInputPin('ExtrusionUp', 'Float',100)
        p=self.createInputPin('ExtrusionDown', 'Float',50)
        p.recomputeNode=True



    @staticmethod
    def description():
        return FreeCAD_UVprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []







def nodelist():
    return [
			FreeCAD_Parallelprojection,
			FreeCAD_Perspectiveprojection,
			FreeCAD_UVprojection,
			
		]
