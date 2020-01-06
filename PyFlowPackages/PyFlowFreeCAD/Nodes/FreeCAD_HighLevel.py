
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2



class FreeCAD_swept(FreeCadNodeBase2):
    '''
    sweptpath step generator
    '''

    dok=2 

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('trackPoints', 'VectorPin', structure=StructureType.Array)
        self.createInputPin('centerAxis', 'VectorPin')

        self.createInputPin("Path",'ShapePin')

        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin('steps', 'Integer',200)
        a.setInputWidgetVariant("SimpleSlider")
        
        self.step=self.createInputPin('step', 'Integer',0)
        self.step.recomputeNode=True
        self.createOutputPin('Car_out', 'ShapePin')
        self.createOutputPin('tracks_out', 'ShapePin')
        self.createOutputPin('flowAxes_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_swept.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

    @staticmethod
    def keywords():
        return ["archi"]

class FreeCAD_handrail(FreeCadNodeBase2):
    '''
    staircase handrail
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin("Path",'ShapePin')
        self.createInputPin("borderA",'ShapePin')
        self.createInputPin("borderB",'ShapePin')

        self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin('steps', 'Integer',13)
        a.setInputWidgetVariant("SimpleSlider")
        
        a=self.createInputPin('heightStair', 'Float',250)
        a.setInputWidgetVariant("SimpleSlider")
        
        a=self.createInputPin('heightBorder', 'Float',70)
        a.setInputWidgetVariant("SimpleSlider")
      

    @staticmethod
    def description():
        return FreeCAD_handrail.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

    @staticmethod
    def keywords():
        return ['stair','rail','archi']


class FreeCAD_Bender(FreeCadNodeBase2):
    '''
    transforms the poles of a BSpline Surface **Shape_in** to the poles2 of the **Shape_out**
    
    for u in range(countA):

        for v in range(countB):

            [x,y,z]=poles[u,v]

            poles2[u,v,0]=(a+x)*cos(b*y+c)

            poles2[u,v,1]=(a+x)*sin(b*y+c)

            poles2[u,v,2]=z

    '''
    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin("Shape_in",'ShapePin')
        self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin('a', 'Integer',13)
        a.setInputWidgetVariant("SimpleSlider")

        a=self.createInputPin('b', 'Integer',13)
        a.setInputWidgetVariant("SimpleSlider")

        a=self.createInputPin('c', 'Integer',13)
        a.setInputWidgetVariant("SimpleSlider")
       
       

    @staticmethod
    def description():
        return FreeCAD_Bender.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

    @staticmethod
    def keywords():
        return ['transform','spline']

class FreeCAD_FigureOnFace(FreeCadNodeBase2):
    '''
    map figures pattens onto a surface
    '''

    dok = 4

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout = self.createOutputPin('details', 'ShapeListPin')

        self.createInputPin('pattern', 'VectorPin', structure=StructureType.Array)
        
        a=self.createInputPin("cutBorder", 'Boolean')
        a.recomputeNode=True
        
        self.createInputPin('transformation', 'TransformationPin')

        #beispiel fuer parametre range int
        a=self.createInputPin("degree", 'Integer',1)
        a.annotationDescriptionDict={ "ValueRange":(0.,3.)}     
        #a.recomputeNode=True
        a=self.createInputPin("createFaces", 'Boolean',False)
        #a.recomputeNode=True
        a=self.createInputPin("tangentForce", 'Float',10)
        a.annotationDescriptionDict={ "ValueRange":(0.,100.)}
        a.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_FigureOnFace.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

## ||
## \/ okay


class FreeCAD_Tread(FreeCadNodeBase2):
    '''
    Schindel oder Stufe
    '''

    def __init__(self, name="MyTread"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("noise", 'Float', 1)

        a=[1,2,3,4,5,6,7,8]
        for i in range(8):
            a[i]=self.createInputPin("point_"+str(i), 'VectorPin')
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
        return FreeCAD_Tread.__doc__

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





def nodelist():
    return [


                FreeCAD_Tread,
                FreeCAD_FigureOnFace,

                FreeCAD_swept,
                FreeCAD_handrail,
                FreeCAD_Bender,

        ]
