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



class FreeCAD_ApplyPlacements(FreeCadNodeBase2):
    '''
    apply a list of placements to 
    a shape or a list of shapes 
    or a list of vectors(polygon)
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="a list of vectors which define a poylgon pattern"

        a=self.createInputPin('Shapes', 'ShapeListPin')   
        a.description="a list of shapes,  the n. shape will get the n. placement"

        a=self.createInputPin('Shape_in', 'ShapePin')   
        a.description="a single shape, there will be a copy of this shape for each placement"
        
        a=self.createInputPin('Placements', 'PlacementPin',structure=StructureType.Array)
        a.description="the list of placement which are applied to the shape, shapelist or points"

        a=self.createOutputPin('Shape_out', 'ShapePin')   

        a=self.createOutputPin('points_out', 'VectorPin',structure=StructureType.Array)
        a.description="the result if the input was the __points__ pin"

    @staticmethod
    def description():
        return FreeCAD_ApplyPlacements.__doc__



class FreeCAD_Repeat(FreeCadNodeBase2):
    '''
    list of the same element repeated
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('in', 'AnyPin',constraint='1')   
        a.description="element to repeat"
        a=self.createOutputPin('out', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description="count repetitions of elment in" 
        a=self.createInputPin('count', 'Integer',2) 
        a.description="how often to repeat element in"
          
        a=self.createOutputPin('Shapes', 'ShapeListPin')
        a.description="list of shapes if input element is a shape"
        
    @staticmethod
    def description():
        return FreeCAD_Repeat.__doc__



class FreeCAD_Index(FreeCadNodeBase2):
    '''
    returns item with a given index from a list
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('list', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description="a list"
        
        a=self.createInputPin('index', 'Integer',2)
        a.description='position of the item in the list starting with 0'
        a=self.createOutputPin('item', 'AnyPin',constraint='1')
        a.description="element of list at index position"
        

    @staticmethod
    def description():
        return FreeCAD_Index.__doc__


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




class FreeCAD_Elevation(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        #a=self.createInputPin('filename', 'String','/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/testdata.csv')
        
        a=self.createInputPin('force', 'Boolean',True)
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a=self.createOutputPin('poles', 'VectorPin',structure=StructureType.Array)

        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['linear', 'thin_plate', 'cubic', 'inverse', 'multiquadric', 'gaussian', 'quintic']
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("cubic")


        a=self.createInputPin('gridCount', 'Integer',10)
        a.annotationDescriptionDict={ "ValueRange":(3,30)}
        a.setInputWidgetVariant("Simple2")
        
        a=self.createInputPin('bound', 'Float',0)
        a.setInputWidgetVariant("Simple3")
       


        a=self.createInputPin('noise', 'Integer',1)
        a.annotationDescriptionDict={ "ValueRange":(0,4)}
        a.setInputWidgetVariant("Simple2")
        
        a=self.createInputPin('Rbf', 'Boolean',True)
    

    
class FreeCAD_Counter(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('reset', 'ExecPin', None, self.freset)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
    
        
        a=self.createOutputPin('count', 'IntPin',0)
        
    
    def freset(self,*args, **kwargs):
        self.setData("count",0)
        self.outExec.call()
        self.setColor()

        
class FreeCAD_Sleep(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        
        a=self.createInputPin('sleep', 'IntPin',0)
        

class FreeCAD_Expression(FreeCadNodeBase2):
    '''
    evaluate  an expressions with at most 4 variables
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('modules', 'StringPin','time')
        a.description="required module names separated by comma"
        a=self.createInputPin('expression', 'StringPin','time.time()+a')
        a.description="expression with at most 4 variables a, b, c, d"
        
        a=self.createInputPin('a', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a.description="first parameter"
        a=self.createInputPin('b', 'AnyPin')
        a.description="2nd parameter"
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('c', 'AnyPin')
        a.description="3. parameter"
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('d', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a.description="last parameter"
        
        a=self.createOutputPin('string_out', 'StringPin')
        a.description="result as string"
        a=self.createOutputPin('float_out', 'FloatPin', None)
        a.description="result as float"
        a=self.createOutputPin('int_out', 'IntPin', None)
        a.description="result as integer"
        a=self.createOutputPin('bool_out', 'BoolPin', None)
        a.description="result as boolean"
 
    @staticmethod
    def description():
        return FreeCAD_Expression.__doc__
 
   

def nodelist():
    return [
                FreeCAD_Toy,

    ]



def nodelist():
    return [
                FreeCAD_Toy,##
                FreeCAD_Object,##

                #FreeCAD_Console,
                FreeCAD_VectorArray,##
                #FreeCAD_Boolean,

                #FreeCAD_Plot,
                #FreeCAD_ShapeIndex,
                #FreeCAD_ShapeExplorer,
                #FreeCAD_Compound,
                #FreeCAD_Edge,
                #FreeCAD_Face, 

                #FreeCAD_Ref,
                
                #FreeCAD_LOD,
                #FreeCAD_View3D,
                #FreeCAD_Destruct_Shape,

                FreeCAD_ListOfVectors,##
                FreeCAD_ListOfVectorlist,##
                FreeCAD_MoveVectors,##
                FreeCAD_ScaleVectors,##
                #FreeCAD_RepeatPattern,
                #FreeCAD_Transformation,
                FreeCAD_Reduce,##
                #FreeCAD_IndexToList,
                #FreeCAD_DistToShape,
                #FreeCAD_CenterOfMass,
                #FreeCAD_ListOfShapes,
                #FreeCAD_ListOfPlacements,
                FreeCAD_ApplyPlacements,##
                FreeCAD_Repeat,##
                FreeCAD_Index,##
                #FreeCAD_Zip,#ok bis hier
                
                FreeCAD_Tube,##

                # noch zu dokumentieren ##############################
                #FreeCAD_bakery,
                #FreeCAD_topo,
                
                #FreeCAD_Conny,
                #FreeCAD_RandomizePolygon,
                

                # FreeCAD_RefList, muss noch programmiert werden
                #FreeCAD_ImportFile,
                FreeCAD_Elevation,##
                #FreeCAD_Camera,
                FreeCAD_Counter,##
                FreeCAD_Sleep,##
                #FreeCAD_Export,
                #FreeCAD_Import,
                FreeCAD_Expression,##
                #FreeCAD_Seam,
                #FreeCAD_Nurbs,
                #FreeCAD_Loft,
                
                #FreeCAD_Sweep,
                
                #FreeCAD_RuledSurface,
                #FreeCAD_Slice,

                
        ]


# hack wird irgendwo geladen warun #+#
# muss wieder raus, weil schon in information !!!
class FreeCAD_Object(FreeCadNodeBase2):
    pass
    
    
