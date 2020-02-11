'''
nodes under development
nodes for debugging and test data 
some stuff to play and new prototypes in very alpha state
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2

from nodeeditor.cointools import *
reload (nodeeditor.cointools)


class FreeCAD_PinsTest(FreeCadNodeBase2):
    '''
    pins testcase: what is possible
    '''

    @staticmethod
    def description():
        return "creates different pins for testing connections"

    def __init__(self, name="Fusion"):
        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True


        for pn in  'Any Vector Rotation Shape ShapeList FCobj Array Float Int String Bool'.split(' '):
            say("create Pin for ",pn)
            
            p=self.createInputPin(pn+"_in", pn+'Pin')
            p=self.createOutputPin(pn+"_out", pn+'Pin')
            p=self.createInputPin(pn+"_in_array", pn+'Pin', structure=StructureType.Array)

            # gleiche pins einzeln oder als liste
            p.enableOptions(PinOptions.AllowMultipleConnections)
            p.disableOptions(PinOptions.SupportsOnlyArrays)

#           p=self.createInputPin(pn+"_in_dict", pn+'Pin', structure=PinStructure.Dict)
#           p=self.createInputPin(pn+"_in_mult", pn+'Pin', structure=PinStructure.Multi)
            p=self.createOutputPin(pn+"_out_array", pn+'Pin', structure=StructureType.Array)
#           p=self.createOutputPin(pn+"_out_dict", pn+'Pin', structure=PinStructure.Dict)

		#a pin for different types
        self.createInputPin("FloatOrInt","AnyPin", None,  supportedPinDataTypes=["FloatPin", "IntPin"])
        self.createInputPin("Shape_or_Rotation","AnyPin", None,  supportedPinDataTypes=["ShapePin", "RotationPin"])


    @staticmethod
    def description():
        return FreeCAD_PinsTest.__doc__

    @staticmethod
    def category():
        return 'Development'







class FreeCAD_Tape(FreeCadNodeBase2):
    '''
    create a list of points and tangents 
    to provide a tangent seam of a face
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description="the visualization of the tape"
        
        self.arrayData = self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="the position and tangent data for post processing"

        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.description="size of the tangent force"
        
        a=self.createInputPin('l',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.description="size of the normal force"
        
        a=self.createInputPin('hands', 'VectorPin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.description="the list of positions and directions to use as constraints" 

        #a=self.createInputPin('Shape', 'ShapePin')
        #a=self.createInputPin('scalesU', 'FloatPin',structure=StructureType.Array)
        #a=self.createInputPin('scalesV', 'FloatPin',structure=StructureType.Array)

        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Tape.__doc__

    @staticmethod
    def category():
        return 'Development'


class FreeCAD_Toy3(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.randomize = self.createInputPin("randomize", 'BoolPin')

        a=self.createInputPin('Shape', 'ShapePin')
        a=self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a=self.createInputPin('l',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a=self.createInputPin('uvs', 'VectorPin',structure=StructureType.Array)

        self.arrayData = self.createInputPin('data', 'AnyPin', structure=StructureType.Dict)
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.arrayData.disableOptions(PinOptions.ChangeTypeOnConnection | PinOptions.SupportsOnlyArrays)
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=StructureType.Dict)
        self.outArray.enableOptions(PinOptions.AllowAny)
        self.outArray.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.result = self.createOutputPin('result', 'BoolPin')
        #self.arrayData.onPinDisconnected.connect(self.inPinDisconnected)
        #self.arrayData.onPinConnected.connect(self.inPinConnected)
        #self.KeyType.typeChanged.connect(self.updateDicts)


    @staticmethod
    def category():
        return 'Development'


class FreeCAD_ReduceSurface(FreeCadNodeBase2):
    '''
  
    '''

    videos="https://youtu.be/iEHDOwz9S3Q https://youtu.be/vuQ4s3iYqOA"

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a = self.createInputPin("commit", 'ExecPin', None, self.commit)
        a.description='accept changes into working copy'
        a = self.createInputPin("bake", 'ExecPin', None, self.bake)
        a.description='store working copy as nonparametric Shape'
        a = self.createInputPin("rollback", 'ExecPin', None, self.rollback)
        a.description="cancel all changes and go back to the inputpin Shape curve"
        
        
        a=self.createInputPin('Move1', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description='interactive move the calculated new pole first direction'
        
        a=self.createInputPin('Move2', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description='interactive move the calculated new pole 2nd direction'

        a=self.createInputPin('Move3', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description='interactive move the calculated new pole 2nd direction'

        a=self.createInputPin("hide",'Boolean')
        a.description="do not display the controls in 3D after works is finished"
        
        a=self.createInputPin("position",'VectorPin')
        a.description='a position to use as new pole instead of the calculated pole'
        
        a=self.createInputPin("useStartPosition",'Boolean')
        a.description='use the pin position as new pole base' 
        
        a=self.createInputPin("usePositionAsAbsolute",'Boolean')
        a.description='use the pin position as absolute else it is added to the center of mass' 
        

        a=self.createInputPin('startU',"Integer")
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="knot number where modification starts"

        a=self.createInputPin('segmentsU',"Integer",-1)
        a.annotationDescriptionDict={ "ValueRange":(-1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="number of segments which are smoothed"

        a=self.createInputPin('startV',"Integer")
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="knot number where modification starts"

        a=self.createInputPin('segmentsV',"Integer",-1)
        a.annotationDescriptionDict={ "ValueRange":(-1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="number of segments which are smoothed"

        '''
        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('weight',"Integer",2)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        
        '''
        a=self.createInputPin("Strategy",'StringPin','Center of Mass')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["Center of Mass","Shortest","Point"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("Center of Mass")
        a.description='''how the curve should be simplified: 
  -''Center of Mass'' starts at the center fo the old poles
  -''Shortest'' calculates the shortest segement to fill the gap
  -''Point''  makes the curve fitting a point'''

        a=self.createInputPin("Method",'StringPin','BFGS')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP',]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("BFGS")
        a.description='''the scipy methods for optimize.
        
If the computation time is to long or not good results are calcuated a change of the method may help. 

see https://docs.scipy.org/doc/scipy/reference/optimize.html'''
        
        a=self.createInputPin('Shape', 'ShapePin')
        a.description='a bspline curve edge' 
        
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description='the list of knotes before and after change'

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description='the reduced bspline curve' 
        
        a=self.createInputPin("preservePolesCount",'Boolean')
        
        self.setExperimental()

        
    def commit(self,*arg,**kwarg):
        #import nodeeditor.dev
        #reload (nodeeditor.dev)
        #nodeeditor.dev.run_commit(self)
        #return

        self.shape=self.getPinObject("Shape_out")
        a=self.getData('start')
        b=self.getData('segments')
        ax=self._wrapper.UIinputs
        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='segments':
                p.setData(0)
            if p.name=='Move1':
                p.setData(0)

            if p.name=='Move2':
                p.setData(0)

        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='start':
                p.setData(a+4)
        self.compute()
        self.outExec.call()


        
    def rollback(self,*arg,**kwarg):
        try:
            del(self.shape)
        except:
            pass

    @staticmethod
    def description():
        return FreeCAD_ReduceSurface.__doc__



class FreeCAD_Topo2(FreeCadNodeBase2):
    '''
    dummy for tests
    '''

    @staticmethod
    def description():
        return "a dummy for tests"

    def __init__(self, name="Fusion"):
        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        a=self.createInputPin('ShapeA', 'ShapePin')
        a=self.createInputPin('ShapeB', 'ShapePin')
        
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description='the list of knotes before and after change'

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description='the reduced bspline curve' 


        a=self.createInputPin('vertexA',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(0,8)}
        a=self.createInputPin('vertexB',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(0,8)}
        
        a=self.createInputPin('selA',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(0,36)}
        
        #a=self.createInputPin('selB',"Integer",0)
        #a.annotationDescriptionDict={ "ValueRange":(0,8)}
        
        a=self.createInputPin("singleIndex",'Boolean')
        a=self.createInputPin("flagA",'Boolean')
        a=self.createInputPin("flagB",'Boolean')



    @staticmethod
    def category():
        return 'Development'



class FreeCAD_elastic(FreeCadNodeBase2):
    '''
    dummy for tests
    '''

    @staticmethod
    def description():
        return "a dummy for tests"

    def __init__(self, name="Fusion"):
        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute) 
        self.inExec = self.createInputPin("Hide", 'ExecPin', None, self.hide) 
        self.inExec = self.createInputPin("Show", 'ExecPin', None, self.show)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        a=self.createInputPin('a',"Integer",-100)
        a.setInputWidgetVariant("Slider")

        a=self.createInputPin('b',"Integer")
        a.setInputWidgetVariant("Slider")


        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a=self.createInputPin('fixpoints', 'VectorPin',structure=StructureType.Array)
        a=self.createInputPin('force', 'FunctionPin')
        
        a=self.createOutputPin('Points_out', 'VectorPin',structure=StructureType.Array)
        

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description='the reduced bspline curve' 


#        a=self.createInputPin('vertexA',"Integer",0)
#        a.annotationDescriptionDict={ "ValueRange":(0,8)}
#        a=self.createInputPin('vertexB',"Integer",0)
#        a.annotationDescriptionDict={ "ValueRange":(0,8)}
        
#        a=self.createInputPin('selA',"Integer",0)
#        a.annotationDescriptionDict={ "ValueRange":(0,36)}
        
        #a=self.createInputPin('selB',"Integer",0)
        #a.annotationDescriptionDict={ "ValueRange":(0,8)}
        
        #a=self.createInputPin("singleIndex",'Boolean')
        a=self.createInputPin("hide",'BoolPin')
        a=self.createInputPin("animate",'BoolPin')
        

    def show(self,*args, **kwargs):
        sayl()
        showcoin(self)
        sayl()

    def hide(self,*args, **kwargs):
        sayl()
        hidecoin(self)
        sayl()




    @staticmethod
    def category():
        return 'Development'



class FreeCAD_Forum(FreeCadNodeBase):
    '''
    poll the freecad forum for new posts
    '''

    def __init__(self, name="Fusion"):
        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('reset', 'ExecPin', None, self.reset) 
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createOutputPin('news', 'StringPin')

        self.process = self.createInputPin('process', 'Boolean')
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(1.0)
        self.delay.annotationDescriptionDict={ "ValueRange":(0.,10)}
        self._total=0

    def Tick(self, delta):
        if self.process.getData():
            #say(self._total,delta)
            self._total += delta
            if self._total >= self.delay.getData():
                self.compute()
                self._total=0

    def reset(self,*args, **kwargs):
        self.hash={}

    @staticmethod
    def description():
        return FreeCAD_Forum.__doc__

    @staticmethod
    def category():
        return 'Development'




class FreeCAD_ToyWidgets(FreeCadNodeBase2):
    '''
    methode zum spielen input widgets
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
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
        
        # alle pins erzeugen
        import  PyFlow.Packages.PyFlowFreeCAD
        pincs=PyFlow.Packages.PyFlowFreeCAD.PyFlowFreeCAD.GetPinClasses()  

        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))

        import  PyFlow.Packages.PyFlowBase
        pincs=PyFlow.Packages.PyFlowBase.PyFlowBase.GetPinClasses()   

        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))

    @staticmethod
    def description():
        return FreeCAD_ToyWidgets.__doc__

    @staticmethod
    def category():
        return 'Development'






def nodelist():
    return [
    
    FreeCAD_PinsTest,    
    FreeCAD_ToyWidgets,
    
    FreeCAD_Toy3,
    
    FreeCAD_Tape,

    FreeCAD_Topo2,   
    
    ##FreeCAD_ReduceSurface,
    FreeCAD_elastic,
    FreeCAD_Forum,
]
