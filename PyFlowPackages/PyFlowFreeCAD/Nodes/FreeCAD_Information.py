'''

'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2



class FreeCAD_CenterOfMass(FreeCadNodeBase2):
    '''
    center of mass for a list of shapes
    '''

    dok=4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapelist = self.createInputPin("ShapeList", 'ShapeListPin')
        self.shapelist.description="list of shapes to discover" 

        self.shapeout = self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        self.shapeout.description="the centers of mass for the shapes in __ShapeList__"


    @staticmethod
    def description():
        return FreeCAD_CenterOfMass.__doc__

    @staticmethod
    def category():
        return 'Information'





class FreeCAD_Object2(FreeCadNodeBase2):
    '''
    load and save objects in FreeCAD document
    '''

    dok=4
    def __init__(self, name="MyObject"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'String')
        self.objname.setData("Box")

        self.createInputPin('Reload_from_FC', 'ExecPin', None, self.reload)
        self.createInputPin('Store_to_FC', 'ExecPin', None, self.store,)




    def reload(self, *args, **kwargs):
        print ("reload from FreeCADobject and refresh data")
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.reload_obj(self)
        sayl()



    def store(self, *args, **kwargs):

        print ("store  data to  FreeCAD object and to the output pins" )

        data={}
        pps=self.getOrderedPins()
        for p in pps:
            dat=p.getData()
            print ("#+#+#",p.getName(),dat)
            data[str(p.name)+"_out"]=dat

        say("data")
        say(data)
        say("pps")
        say(pps)

        for p in pps:
            if p.group=='FOP':
                n=p.getName()
                if n.endswith('_out'):
                    p.setData(data[str(n)])
                    pn=n[:-4]
                    vn=data[str(n)]
                    say("set",n,pn,vn)
                    setattr(self.fob,pn,vn)
                    continue

                try:
                    pn=n.split('_')[1]
                    if pn=="Object": # hack for names FreeCAD_Object #+#
                        pn=n.split('_')[2]

                    vn=p.getData()

                    try:
                        v=self.fob.getPropertyByName(pn).Value
                    except:
                        v=self.fob.getPropertyByName(pn)
                    say("change value",n,pn,v,vn)
                    if v  !=  vn:  # value has changed
                        setattr(self.fob,pn,vn)
                except:
                    sayl("problem with store",n)
    
        FreeCAD.activeDocument().recompute()



    def createPins(self, *args, **kwargs):
        say('hack outsourced to nodeetitor.dev')
        import nodeeditor.dev
        reload (nodeeditor.dev)
        return  nodeeditor.dev.runraw(self)
        say("pins created")


    @staticmethod
    def description():
        return FreeCAD_Object2.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Console(FreeCadNodeBase2):
    '''
    write to FreeCAD.Console
    '''
    
    dok=4
    def __init__(self, name="Console"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.entity = self.createInputPin('entity', 'AnyPin',[], structure=StructureType.Multi)
        self.entity.description="data to print"
        self.entity.setData([FreeCAD.Vector(),FreeCAD.Vector()])



    def compute(self, *args, **kwargs):

        FreeCAD.Console.PrintMessage("%s: %s\n"%(self.name,self.entity.getData()))
        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Console.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []



class FreeCAD_ShapeExplorer(FreeCadNodeBase2):
    '''
    information about a shape
    '''

    dok=3
    def __init__(self, name="MyPartExplorer"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.part = self.createInputPin('Shape_in', 'ShapePin')

        self.outArray = self.createOutputPin('Points', 'VectorPin', structure=StructureType.Array)
        self.outArray.description="the coodinates of the vertexes as vectors"
        
        a=self.createOutputPin('Faces', 'ShapeListPin')
        a.description="the list of faces"
        b=self.createOutputPin('Edges', 'ShapeListPin')
        b.description="the list of edges"

        self.pinsk={
                'Volume':'Float',
                'Area':'Float',
                'Length':'Float',
                'BoundBox': None,
                'CenterOfMass':'VectorPin',
#               #'PrincipalProperties','StaticMoments',
                'Mass':'Float',
                'ShapeType':'String',
        }

        for p in list(self.pinsk.keys()):
            if self.pinsk[p]  !=  None:
                self.createOutputPin(p, self.pinsk[p])

        self.part.recomputeNode=True




    def compute(self, *args, **kwargs):

        shape=self.getPinObject("Shape_in")
        
        self.setPinObject("Shape_out",shape)
        if shape is None: return
        for n in list(self.pinsk.keys()):
            v=getattr(shape,n)
            if self.pinsk[n]  !=  None:
                self.setData(n,v)
        if 0:
            ls=shape.writeInventor().split('\n')
            for l in ls:say(l)

        points=[v.Point for v in getattr(shape,'Vertexes')]
        self.setData('Points',points)
        self.setPinObjects("Edges",shape.Edges)
        self.setPinObjects("Faces",shape.Faces)

        # output of the pins
        for t in self.getOrderedPins():
            if t.__class__.__name__ in ['ShapeListPin']:
                say("{} has {} items ({})".format(t.getName(),len(t.getData()),t.__class__.__name__))
            else:
                say("{} = {} ({})".format(t.getName(),t.getData(),t.__class__.__name__))

            if 0 and len(t.affects):
                for tt in t.affects:
                    if not tt.getName().startswith(self.getName()):
                        if tt.__class__.__name__ in ['AnyPin']:
                            say("----> {} (has {} items) ({})".format(tt.getName(),len(tt.getData()),tt.__class__.__name__))
                        else:
                            say("----> {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
                        FreeCAD.tt=tt
                        # say(tt.linkedTo[0])
                        a=FreeCAD.tt.linkedTo[0]['rhsNodeName']
                        say("call owning------------------",tt.owningNode().getName())

                        #start the follower node
                        #tt.owningNode().compute()

        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_ShapeExplorer.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []





class FreeCAD_Plot(FreeCadNodeBase2):
    '''
    display matplotlib windows with data
    '''

    dok= 4
    def __init__(self, name="MyPlot"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.xpin=self.createInputPin('x', 'Float', structure=StructureType.Array)
        self.ypin=self.createInputPin('y', 'Float', structure=StructureType.Array)

        self.xpin2=self.createInputPin('x2', 'Float', structure=StructureType.Array)
        self.ypin2=self.createInputPin('y2', 'Float', structure=StructureType.Array)

        self.xpin.description="x values for the first curve"
        self.ypin.description="y values for the first curve"
        self.xpin2.description="x values for the 2nd curve"
        self.ypin2.description="y values for the 2nd curve"
        

        self.mode = self.createInputPin('Figure', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["Figure1","Figure2","Figure3","Figure4"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("Figure1")
        self.mode.recomputeNode=True
        self.mode.description="Selector for the window name, there a re at most 4 diagram windows possible"
        

    @staticmethod
    def description():
        return FreeCAD_Plot.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []

#------------------------------------------------------------------


class FreeCAD_DistToShape(FreeCadNodeBase2):
    '''
    list of distances from  a list of shapes 
    to a target shape
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        a=self.createInputPin('shapes', 'ShapeListPin')
        a.description="list of shapes"
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="list of points"

        a=self.createInputPin('target', 'ShapePin')
        a.description="target shape"

        a=self.createOutputPin('distance', 'FloatPin',structure=StructureType.Array)
        a.description="distances"
        

    @staticmethod
    def description():
        return FreeCAD_DistToShape.__doc__

    @staticmethod
    def category():
        return 'Information'




__all__= [
		FreeCAD_CenterOfMass,
		FreeCAD_Console,
		FreeCAD_DistToShape,
		FreeCAD_Object2,
		FreeCAD_Plot,
		
		FreeCAD_ShapeExplorer,
		
	]

def nodelist():
	return __all__
