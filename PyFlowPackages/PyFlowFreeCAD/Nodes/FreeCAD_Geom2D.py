'''
This module contains nodes to create Geom2D objects like Circle, Ellipse, LineSegement.
The can be used to create Sketches or for uv-figures on faces
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2


class FreeCAD_Geom2DGeometry(FreeCadNodeBase2):
    '''
    2d Geometry object
    '''

    def __init__(self, name="Geo2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("ua", 'Float', True)
        a=self.createInputPin("va", 'Float', True)
        a=self.createInputPin("ub", 'Float', True)
        a=self.createInputPin("vb", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Geom2DGeometry.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Geom2DCircle(FreeCadNodeBase2):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyCircle2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("u", 'Float', True)
        a=self.createInputPin("v", 'Float', True)
        a=self.createInputPin("radius", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Geom2DCircle.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Geom2DEllipse(FreeCadNodeBase2):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'Float', True)
        a=self.createInputPin("vLocation", 'Float', True)

        a=self.createInputPin("direction", 'Float', True)

        a=self.createInputPin("MajorRadius", 'Float', True)
        a=self.createInputPin("MinorRadius", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Geom2DEllipse.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Geom2DArcOfEllipse(FreeCadNodeBase2):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfEllipse2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'Float', True)
        a=self.createInputPin("vLocation", 'Float', True)

        a=self.createInputPin("direction", 'Float', True)

        a=self.createInputPin("MajorRadius", 'Float', True)
        a=self.createInputPin("MinorRadius", 'Float', True)

        a=self.createInputPin("startAngle", 'Float', True)
        a=self.createInputPin("endAngle", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Geom2DArcOfEllipse.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Geom2DArcOfParabola(FreeCadNodeBase2):
    '''
    2d Geometry object
    '''

    def __init__(self, name="MyArcOfParabola2D"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Shape', 'ShapePin')

        a=self.createInputPin("uLocation", 'Float', True)
        a=self.createInputPin("vLocation", 'Float', True)

        a=self.createInputPin("direction", 'Float', True)

        a=self.createInputPin("MajorRadius", 'Float', True)
        a=self.createInputPin("MinorRadius", 'Float', True)

        a=self.createInputPin("startAngle", 'Float', True)
        a=self.createInputPin("endAngle", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('geometry', 'ShapePin') #.description='edges or faces compound of the alpha hull'


    @staticmethod
    def description():
        return FreeCAD_Geom2DArcOfParabola.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Geom2DArcOfCircle(FreeCadNodeBase2):
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

        a=self.createInputPin("uLocation", 'Float', True)
        a.description="first coordinate of the center"

        a=self.createInputPin("vLocation", 'Float', True)
        a.description="2nd coordinate of the center"

        a=self.createInputPin("radius", 'Float', True)
        a.description="radius of the circle"

        a=self.createInputPin("startAngle", 'Float', True)
        a.description="angle of the starting point of the arc"

        a=self.createInputPin("endAngle", 'Float', True)
        a.description="angle of the ending point of the arc"

        self.createOutputPin('Shape_out', 'ShapePin').\
            description="the projection of the geometry onto the Face1 of Shape_in"
        self.createOutputPin('geometry', 'ShapePin').\
            description='2D Arc of Circle geometry object'


    @staticmethod
    def description():
        return FreeCAD_Geom2DArcOfCircle.__doc__

    @staticmethod
    def category():
        return 'Geom2D'

    @staticmethod
    def keywords():
        return []



__all__= [
                FreeCAD_Geom2DGeometry,
                FreeCAD_Geom2DCircle,
                FreeCAD_Geom2DEllipse,
                FreeCAD_Geom2DArcOfEllipse,
                FreeCAD_Geom2DArcOfParabola,
                FreeCAD_Geom2DArcOfCircle,
        ]

def nodelist():
	return __all__

