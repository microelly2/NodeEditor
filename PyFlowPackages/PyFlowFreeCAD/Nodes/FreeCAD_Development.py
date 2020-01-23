

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


class FreeCAD_Toy(FreeCadNodeBase2):
    '''erzeuge eine zufallsBox'''



    def __init__(self, name="MyToy"):

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
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')
        name="MyToy"
        self.objname.setData(name)

    def compute(self, *args, **kwargs):

        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        say(str(self.uid).replace('-','_'))

        cc=FreeCAD.ActiveDocument.getObject(yid)
        if cc == None:
            cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
            FreeCAD.activeDocument().recompute()
        cc.Label=self.objname.getData()


        f=30 if self.randomize.getData() else 0
        shape=Part.makeBox(10+f*random.random(),10+f*random.random(),10+f*random.random())
        cc.Shape=shape

        if self.part.hasConnections():
            say("send a Part")
            if cc == None:
                self.part.setData(None)
            else:
                self.part.setData(cc.Name)

        sayl()
        say(self.getPinByName("Shape"))
        say(shape)

        self.setPinObject("Shape",shape)
        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Toy.__doc__

    @staticmethod
    def category():
        return 'Development'

    @staticmethod
    def keywords():
        return ['Box','Part']










def nodelist():
	return [
	FreeCAD_PinsTest,
	FreeCAD_Foo,
	FreeCAD_StorePins,
	FreeCAD_Toy,
	
	]
