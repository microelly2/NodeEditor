'''
shapes which are created on generic data, no shpas as inputs
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2







class FreeCAD_Box( FreeCadNodeBase2):
    '''
    erzeuge einer Part.Box
    '''

    dok=4
    def __init__(self, name="MyBox"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')



        self.length = self.createInputPin("length", 'Float')
        self.length.description="Lenght of the Box"
        self.length.setInputWidgetVariant("Slider")

    #    self.length2 = self.createInputPin("length", 'Float')
    #    self.length2.description="Lenght of the Box"
    #    self.length2.setInputWidgetVariant("Simple2")

        self.length.annotationDescriptionDict={ "A":23,"ValueRange":(10.,20.)}
    #    self.length2.annotationDescriptionDict={ "A":23,"Step":2. }

        self.width = self.createInputPin("width", 'Float')
        self.width.description="Width of the Box"
        self.height = self.createInputPin("height", 'Float')
        self.height.description = "Height of the Box"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description = "position of the Box"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the height of the Box" 

#        self.objname.setData(name)

        self.setDatalist("length width height position direction",
            [10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0)])


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

    @timer
    def compute(self, *args, **kwargs):

        shape=self.applyPins(Part.makeBox,"length width height position direction")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Box.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Box','Part']









class FreeCAD_Cone(FreeCadNodeBase2):
    '''erzeuge eines Part.Kegel'''
    
    dok=4
    def __init__(self, name="MyCone"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        self.radius1 = self.createInputPin("radius1", 'Float')
        self.radius1.description="Radius of the bottom circle"
        self.radius2 = self.createInputPin("radius2", 'Float')
        self.radius2.description="Radius of the top circle"
        self.height = self.createInputPin("height", 'Float')
        self.height.description="Height of the circle"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description="Position of the center of the bottom circle"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the axis"
        self.angle = self.createInputPin("angle", 'Float')
        self.angle.description="longitude of the sector"

        self.setDatalist("radius1 radius2 height position direction angle",
            [10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),360])


    def compute(self, *args, **kwargs):

        shape=self.applyPins(Part.makeCone,"radius1 radius2 height position direction angle")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()
        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Cone.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Sphere','Part']



class FreeCAD_Sphere(FreeCadNodeBase2):
    '''erzeuge einer Part.Kurgel'''

    dok=4
    def __init__(self, name="MySphere"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.radius = self.createInputPin("radius", 'Float')
        self.radius.description="Radius of the sphere"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description="position of the Sphere"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the south north axis"
        self.angle1 = self.createInputPin("angle1", 'Float')
        self.angle1.description="maximum north latitude"
        self.angle2 = self.createInputPin("angle2", 'Float')
        self.angle2.description="maximum south latitude"
        self.angle3 = self.createInputPin("angle3", 'Float')
        self.angle3.description="maximum longitude (start is always 0)"

        self.setDatalist("radius position direction angle1 angle2 angle3",
            [10,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90,90,360])

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

    @timer
    def compute(self, *args, **kwargs):
        shape=self.applyPins(Part.makeSphere,"radius position direction angle1 angle2 angle3")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()
        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Sphere.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Sphere','Part']



class FreeCAD_Quadrangle(FreeCadNodeBase2):
    '''
    create a Bspline Surface of degree 1
    by 4 points
    '''

    dok=4
    def __init__(self, name="MyQuadrangle"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.vA = self.createInputPin("vecA", 'VectorPin')
        self.vB = self.createInputPin("vecB", 'VectorPin')
        self.vC = self.createInputPin("vecC", 'VectorPin')
        self.vD = self.createInputPin("vecD", 'VectorPin')

        self.setDatalist("vecA vecB vecC vecD", [
                        FreeCAD.Vector(0,0,0),
                        FreeCAD.Vector(100,0,0),
                        FreeCAD.Vector(100,200,40),
                        FreeCAD.Vector(0,200,40),
                    ])

        self.Called=False


    def compute(self, *args, **kwargs):

        # recursion stopper
        if self.Called:
            return

        self.Called=True
        vA=self.vA.getData()
        vB=self.vB.getData()
        vC=self.vC.getData()
        vD=self.vD.getData()

        w=Part.BSplineSurface()
        w.buildFromPolesMultsKnots([[vA,vB],[vD,vC]],[2,2],[2,2],[0,1],[0,1],False,False,1,1)
        shape=w.toShape()

        self.setPinObject("Shape_out",shape)


        self.Called=False

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Quadrangle.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Surface','Part']



class FreeCAD_Polygon(FreeCadNodeBase2):
    '''
    erzeuge eines Streckenzugs
    input pin for a list of vectors
    '''

    dok=4
    
    def __init__(self, name="MyPolygon"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.points = self.createInputPin('points', 'VectorPin',[], structure=StructureType.Array)
        self.points.description="list of points as array"
        self.points.setData([FreeCAD.Vector(0,0,0),FreeCAD.Vector(10,0,0)])


        self.Called=False
        self.count=2


    @staticmethod
    def description():
        return FreeCAD_Polygon.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Pointlist','Polygon','Part']


class FreeCAD_BSplineSurface(FreeCadNodeBase2):
    '''
    BSpline Surface 
    create a default bspline surface from poles and degrees
    '''

    dok=4
    @staticmethod

    def description():
        return ''''''

    def __init__(self, name="MyBSplineSurface"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="Array of poles vectors"
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('maxDegreeU', 'Integer', 3)
        a.description="maximum degree for u"
        
        a=self.createInputPin('maxDegreeV', 'Integer', 3)
        a.description="maximum degree for v"
        
        a=self.createInputPin('periodicU', 'Boolean',)
        a.description="is surface periodic in u direction"
        
        a=self.createInputPin('periodicV', 'Boolean',)
        a.description="is surface periodic in v direction"

        self.shapeout = self.createOutputPin('Shape_out', 'FacePin')
        self.shapeout.description='BSpline Face'

    @staticmethod
    def description():
        return FreeCAD_BSplineSurface.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Surface','Part']


class FreeCAD_BSplineCurve(FreeCadNodeBase2):
    '''
    BSpline Curve
    create a default bspline surface from poles and degrees
    '''

    dok=4

    def __init__(self, name="MyBSplineCurve"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'EdgePin')
        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('maxDegree', 'Integer', 3)
        a.description="degree of the curve (default is 3)"
        a=self.createInputPin('periodic', 'Boolean',)
        a.description="is curve periodic"
  



    @staticmethod
    def description():
        return FreeCAD_BSplineCurve.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Curve','Part']

class FreeCAD_Simplex(FreeCadNodeBase2):
    '''
    Tetraeder ..
    '''

    def __init__(self, name="MySimplex"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin("noise", 'Float', True)

        a=self.createInputPin("pointA", 'VectorPin', True)
        a.setData(Vector(0,0,0))

        a=self.createInputPin("pointB", 'VectorPin', True)
        a.setData(Vector(10,0,0))
        a=self.createInputPin("pointC", 'VectorPin', True)
        a.setData(Vector(0,10,0))
        a=self.createInputPin("pointD", 'VectorPin', True)
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






def nodelist():
    return [
                FreeCAD_Box,
                FreeCAD_Cone,
                FreeCAD_Sphere,
                FreeCAD_Quadrangle,
                FreeCAD_Polygon,
                
                FreeCAD_BSplineSurface,
                FreeCAD_BSplineCurve,
                FreeCAD_Simplex,


        ]
