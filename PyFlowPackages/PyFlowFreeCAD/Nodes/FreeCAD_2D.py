

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase


class FreeCAD_2DGeometry(FreeCadNodeBase):
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

        a=self.createInputPin("u", 'Float', True)
        a=self.createInputPin("v", 'Float', True)
        a=self.createInputPin("radius", 'Float', True)

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

        a=self.createInputPin("uLocation", 'Float', True)
        a=self.createInputPin("vLocation", 'Float', True)

        a=self.createInputPin("direction", 'Float', True)

        a=self.createInputPin("MajorRadius", 'Float', True)
        a=self.createInputPin("MinorRadius", 'Float', True)

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
        return FreeCAD_2DArcOfCircle.__doc__

    @staticmethod
    def category():
        return '2D'

    @staticmethod
    def keywords():
        return []






def nodelist():
    return [
                FreeCAD_2DGeometry,
                FreeCAD_2DCircle,
                FreeCAD_2DEllipse,
                FreeCAD_2DArcOfEllipse,
                FreeCAD_2DArcOfParabola,
                FreeCAD_2DArcOfCircle,


        ]
