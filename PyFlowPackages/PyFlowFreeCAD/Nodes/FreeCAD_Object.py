'''
all still not categorized nodes
'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2




class FreeCAD_VectorArray(FreeCadNodeBase2):
    '''
    Array of Vectors 
    and a generated default BSplineSurface
    '''

    dok=4
    def __init__(self, name="MyVectorArray"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin("vecA", 'VectorPin',FreeCAD.Vector(20,0,0))
        a.description="step vector for the first dimension"
        
        a=self.createInputPin("vecB", 'VectorPin',FreeCAD.Vector(0,10,0))
        a.description="step vector for the 2nd dimension"
        
        a=self.createInputPin("vecC", 'VectorPin')
        a.description="step vector for the 3rd dimension"
        
        a=self.createInputPin("vecBase", 'VectorPin')
        a.description="starting point of the array"
        
        a=self.createInputPin("countA", 'Integer',5)
        a.description="number of elements in the first direction"
        
        a=self.createInputPin("countB", 'Integer',8)
        a.description="number of elements in the 2nd direction"
        
        a=self.createInputPin("countC", 'Integer',1)
        a.description="if c>1 a 3 dimensional arry of vector is created"
        
        a=self.createInputPin("randomX", 'Float',5)
        a.description="adds some randomness onto the x coordinates of the points"
        
        a=self.createInputPin("randomY", 'Float',5)
        a.description="adds some randomness onto the y coordinates of the points"
        
        a=self.createInputPin("randomZ", 'Float',5)
        a.description="adds some randomness onto the z coordinates of the points"
        

        a=self.createInputPin("degreeA", 'Integer',3)
        a.description="degree of the generated surface in u direction, degreeA = 0 means wire model"
        
        a=self.createInputPin("degreeB", 'Integer',3)
        a.description="degree of the generated surface in u direction, degreeB = 0 means wire model"
        
        a=self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 or 3 dimensional array of vectors"
        


    @staticmethod
    def description():
        return FreeCAD_VectorArray.__doc__

    @staticmethod
    def category():
        return 'Generator'

    @staticmethod
    def keywords():
        return ['BSpline','Array','Surface','Grid','Part']



class FreeCAD_Toy(FreeCadNodeBase2):
    '''
    methode zum spielen
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        '''
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)

        self.trace = self.createInputPin('flag', 'Boolean')
        self.shapelist = self.createInputPin("ShapeList", 'ShapeListPin')
        t = self.createInputPin("Shape", 'ShapePin')
        t.enableOptions(PinOptions.AllowMultipleConnections)
        t.disableOptions(PinOptions.SupportsOnlyArrays)

        t = self.createInputPin("ROT", 'RotationPin',(8,9,0))
        t = self.createOutputPin("ROT_out", 'RotationPin',(3,4,5))
        t = self.createInputPin("PM", 'PlacementPin',(8,9,0))
        t = self.createOutputPin("PM_out", 'PlacementPin',(3,4,5))


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout = self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)

        self.objname = self.createInputPin("objectname", 'String')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'Boolean', True)
        self.shapeOnly.recomputeNode=True

        self.objname = self.createInputPin("objectname", 'String')

        name="MyToy"
        self.objname.setData(name)
        '''
        
        a = self.createInputPin("Slider", 'IntPin')
        a.setInputWidgetVariant("Slider")

        a = self.createInputPin("Simple", 'IntPin')
        a.setInputWidgetVariant("Simple") # unbeschraenkt

        a = self.createInputPin("Default", 'IntPin')
        
        a = self.createInputPin("Slider", 'FloatPin')
        a.setInputWidgetVariant("Slider")

        a = self.createInputPin("Simple", 'FloatPin')
        a.setInputWidgetVariant("Simple") # unbeschraenkt

        a = self.createInputPin("Default", 'FloatPin')
        
        return
        
        
        import  PyFlow.Packages.PyFlowFreeCAD
        pincs=PyFlow.Packages.PyFlowFreeCAD.PyFlowFreeCAD.GetPinClasses()
    

        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))

        import  PyFlow.Packages.PyFlowBase
        pincs=PyFlow.Packages.PyFlowBase.PyFlowBase.GetPinClasses()
    

        #return
        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))





    @staticmethod
    def description():
        return FreeCAD_Toy.__doc__

    @staticmethod
    def category():
        return 'Development'






class FreeCAD_ListOfVectors(FreeCadNodeBase2):
    '''
    create a list of vectors from  single vectors
    the order of the vector is defined by
    the y coordiante of the vector nodes
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createOutputPin('vectors', 'VectorPin', structure=StructureType.Array)

        self.pas=self.createInputPin('pattern', 'VectorPin')
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)



    @staticmethod
    def description():
        return FreeCAD_ListOfVectorlist.__doc__

    @staticmethod
    def category():
        return 'Conversion'

class FreeCAD_ListOfVectorlist(FreeCadNodeBase2):
    '''
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createOutputPin('vectorarray', 'VectorPin', structure=StructureType.Array)

        self.pas=self.createInputPin('vectorlists', 'VectorPin', structure=StructureType.Array)
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)



    @staticmethod
    def description():
        return FreeCAD_ListOfVectorlist.__doc__

    @staticmethod
    def category():
        return 'Conversion'




class FreeCAD_MoveVectors(FreeCadNodeBase2):
    '''
    move a list of vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)

        a=self.createInputPin('mover', 'VectorPin')
        a.description="__mover__ is added to all __vectors__"

        a.recomputeNode=True
        a.description ="mover vector"

    @staticmethod
    def description():
        return FreeCAD_MoveVectors.__doc__

    @staticmethod
    def category():
        return 'Projection'


class FreeCAD_ScaleVectors(FreeCadNodeBase2):
    '''
    scale list of vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)

        a=self.createInputPin('scaler', 'VectorPin')    
        a.recomputeNode=True
        a.description ="factors to scale the three  ain axes"


    @staticmethod
    def description():
        return FreeCAD_ScaleVectors.__doc__

    @staticmethod
    def category():
        return 'Projection'


class FreeCAD_Reduce(FreeCadNodeBase2):
    '''
    select a sublist fo a list of shapes on  flag list selection
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('shapes', 'ShapeListPin')
        a.description="list of shapes"
        a=self.createInputPin('selection', 'Boolean',structure=StructureType.Array)
        a.description="list of flags which shapes should be in the resulting list"

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description = "compound of the filtered shapes" 

    @staticmethod
    def description():
        return FreeCAD_Reduce.__doc__

    @staticmethod
    def category():
        return 'Construction'


#------------------------



class FreeCAD_Tube(FreeCadNodeBase2):
    '''
    calculate the points for a parametric tube along a backbone curve
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('backbone', 'ShapePin')
        a.description="backbone curve for the tube"
        a=self.createInputPin('parameter', 'Float',structure=StructureType.Array)
        a.description="u parameter of the position of the ribs"
        a=self.createInputPin('radius', 'Float',structure=StructureType.Array)
        a.description="radius/size of the rib rings"
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="array of poles for the postprocessing bspline surface"

    @staticmethod
    def description():
        return FreeCAD_Tube.__doc__

    @staticmethod
    def category():
        return 'Construction'







def nodelist():
    return [
                FreeCAD_Toy,##
                FreeCAD_Object,##

                FreeCAD_VectorArray,##

                FreeCAD_ListOfVectors,##
                FreeCAD_ListOfVectorlist,##
                FreeCAD_MoveVectors,##
                FreeCAD_ScaleVectors,##

                #FreeCAD_RepeatPattern,
                #FreeCAD_Transformation,

                FreeCAD_Reduce,##
                
                FreeCAD_Tube,##

                #FreeCAD_Export,
                #FreeCAD_Import,


                
        ]


# hack wird irgendwo geladen warun #+#
# muss wieder raus, weil schon in information !!!
class FreeCAD_Object(FreeCadNodeBase2):
    def __init__(self, name="MyToy"):

            super(self.__class__, self).__init__(name)
            self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
            self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       
    
    
    pass
    
    
