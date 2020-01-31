

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2



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


        for pn in  'Any Vector Rotation Enumeration Shape ShapeList FCobj Array Float Int String Bool'.split(' '):
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

        self.createInputPin("yyy","AnyPin", None,  supportedPinDataTypes=["FloatPin", "IntPin"])

        self.createInputPin("Shape_or_Rotation","AnyPin", None,  supportedPinDataTypes=["ShapePin", "RotationPin"])




    def compute(self, *args, **kwargs):

        sayl()

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_Foo_compute(self,*args, **kwargs)

        self.outExec.call()


    @staticmethod
    def description():
        return FreeCAD_PinsTest.__doc__

    @staticmethod
    def category():
        return 'Development'

    @staticmethod
    def keywords():
        return []






class FreeCAD_Foo(FreeCadNodeBase2):
    '''
    dummy for tests
    '''

    @staticmethod
    def description():
        return "a dummy for tests"

    def __init__(self, name="Fusion"):
        super(self.__class__, self).__init__(name)



    def compute(self, *args, **kwargs):

        sayl()
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_foo_compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Foo.__doc__

    @staticmethod
    def category():
        return 'Development'

    @staticmethod
    def keywords():
        return []



class FreeCAD_StorePins(NodeBase):
    '''
    testnode for store-pins
    '''

    def __init__(self, name):

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

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.show = self.createInputPin('Show', 'ExecPin', None, self.show)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.trace = self.createInputPin('trace', 'BoolPin')

        self.obj = self.createOutputPin('Object', 'FCobjPin')
        self.obja = self.createInputPin('ObjectA', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape_out', 'FCobjPin')
        self.shapein = self.createInputPin('Shape_in', 'FCobjPin')

        if 0:
            self.arrout = self.createOutputPin('Array_out', 'FCobjPin')
            self.arrin = self.createInputPin('Array_in', 'FCobjPin')
        else:
            self.arrout = self.createOutputPin('Array_out', 'ArrayPin')
            self.arrin = self.createInputPin('Array_in', 'ArrayPin')

        self.vobjname = self.createInputPin("objectname", 'StringPin')
        self.vobjname.setData(name)


    def show(self,*args, **kwargs):
        sayl("list all pins")


    def getObject(self,*args):
        say("getobject")
        return self
    pass


    @staticmethod
    def pinTypeHints():
        return {'inputs': ['FloatPin','FloatPin','FloatPin','FloatPin','StringPin'], 'outputs': []}


    @staticmethod
    def category():
        return 'DefaultLib'

    @staticmethod
    def keywords():
        return ['freecad']

    @staticmethod
    def description():
        return "change Placement of the FreeCAD object"

    def compute(self, *args, **kwargs):
        # muss ueberarbeitet werden #+#

        say ("in compute",self.getName(),"objname is",self.vobjname.getData())
        say("#----------------------------------------############################")
        say("#----------------------------------------############################")

        ss=self.arrin.getArray()
        say("getArray",ss)

        # array erzeugen und  senden
        say("connected?",self.arrout.hasConnections())
        if 1 or self.arrout.hasConnections():

                varr=np.round(np.random.random((3,4)),2)
                say("store ",varr)
                store.store().add(str(self.arrout.uid),varr)
                self.arrout.setData(str(self.arrout.uid))
        say ("array done ok")
        say("#----------------------------------------############################")
        say("#----------------------------------------############################")


        say ("get shapein")
        shapein=self.shapein.getData()

        if shapein  !=  None:
            say("shapein",shapein)
            s=store.store().get(shapein)

            #
            say("s:::::::",s)
            if s  !=   None:
                say("!!!!!!!!!!!!!!!!!!!!show")
                #Part.show(s)

            #store.store().dela(shapein)
            store.store().list()


        try:
            say ("try get object")
            c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())
            say ("ok",c,c.Name)
        except:
            say ("nothing found")
            c=None

        # use the input object
        if self.obja.getData() == None:
            say( "no input object")
            c = None
        else:
            c=FreeCAD.ActiveDocument.getObject(self.obja.getData())



        # if this is not possible fall back to the given name for the obj
        if c== None:
            c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())


        say("!!",self.uid)
        say(str(self.uid))
        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        say(str(self.uid).replace('-','_'))

        if 1 or c==None:
            cc=FreeCAD.ActiveDocument.getObject(yid)

        if cc == None:
            cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
        say("created",cc.Name,yid)


        print("input object from pin",self.obja,"getData ..",self.obja.getData())

        if shapein  !=  None:
            say("shapein",shapein)
            s=store.store().get(shapein)

            #
            say("s:::::::",s)
            if s  !=   None:
                say("!!!!!!!!!!!!!!!!!!!!show")
                #Part.show(s)

            #store.store().dela(shapein)
            store.store().list()

            if s  !=  None:
                    say("!!!!!!!!!!!!!!!!!!!!show")
                    cc.Shape=s


        if c == None:
            self.obj.setData(None)
        else:
            s=c
            self.obj.setData(c.Name)
            say("[send key{0} from {1}@{2}]".format(self.shapeout.uid,self.shapeout.getName(),self.getName()))
        #   say("sended obj",self.shapeout.uid,self.shapeout.getName(),self.getName())
        #   store.store().addid(c)
            say("add to store shape",s,self.shapeout.uid)
            say("connected?",self.shapeout.hasConnections())
            if self.shapeout.hasConnections():
                store.store().add(str(self.shapeout.uid),s.Shape)
                self.shapeout.setData(self.shapeout.uid)

        say ("data set to output object is done, exec...")
        self.outExec.call()
        say ("End exec for ---",self.getName())


class FreeCAD_Toy2(FreeCadNodeBase2):
    ''''''



    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')
        name="MyToy"
        self.objname.setData(name)

        a=self.createInputPin('Shape', 'ShapePin')


        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a=self.createInputPin('l',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a=self.createInputPin('uvs', 'VectorPin',structure=StructureType.Array)



        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Toy2.__doc__

    @staticmethod
    def category():
        return 'Development'



class FreeCAD_Tape(FreeCadNodeBase2):
    ''''''



    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.arrayData = self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)
        
      



        a=self.createInputPin('Shape', 'ShapePin')


        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a=self.createInputPin('l',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        
        a=self.createInputPin('hands', 'VectorPin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        #a.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('scalesU', 'FloatPin',structure=StructureType.Array)
        a=self.createInputPin('scalesV', 'FloatPin',structure=StructureType.Array)


        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Toy2.__doc__

    @staticmethod
    def category():
        return 'Development'











class FreeCAD_Toy3(FreeCadNodeBase2):
    ''''''



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




def nodelist():
    return [
    FreeCAD_PinsTest,
    FreeCAD_Foo,
    FreeCAD_StorePins,
    #FreeCAD_Toy,
    FreeCAD_Toy2,
    FreeCAD_Toy3,
    
    FreeCAD_Tape,
    #FreeCAD_ReduceSurface,

]
