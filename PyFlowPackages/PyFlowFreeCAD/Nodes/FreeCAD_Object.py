
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2

class FreeCAD_Boolean(FreeCadNodeBase):
    '''boolean ops of two parts example'''

    def __init__(self, name="Fusion"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
        self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

        self.shape1 = self.createInputPin('Shape_in1', 'ShapePin')
        self.shape2 = self.createInputPin('Shape_in2', 'ShapePin')

        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["fuse","cut","common","fragments"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("fuse")

        self.volume = self.createOutputPin('Volume', 'FloatPin')


    @timer
    def compute(self, *args, **kwargs):

        mode=self.mode.getData()
        self.setNodename("Boolean "+mode)
        self.setImage("freecad_"+mode)

        shape1=self.shape1.getData()
        shape2=self.shape2.getData()

        s1=store.store().get(shape1)
        s2=store.store().get(shape2)

        if s1  !=  None and s2  != None:
            # arbeite mit shapes
            pass

        else:
            part1=self.part1.getData()
            part2=self.part2.getData()
            if part1 == None or part2 == None:
                say("part12 is None, abort")
                return

            s1=store.store().get(part1)
            if not s1.__class__.__name__ =='Solid':
                part1=FreeCAD.ActiveDocument.getObject(part1)
                s1=part1.Shape

            s2=store.store().get(part2)
            if not s2.__class__.__name__ =='Solid':
                part2=FreeCAD.ActiveDocument.getObject(part2)
                s2=part2.Shape

        
        if mode == 'common':
            shape=s1.common(s2)
        elif mode == 'cut':
            shape=s1.cut(s2)
        else:
            shape=s1.fuse(s2)


        self.setPinObject('Shape_out',shape)

        '''
        if self.part.hasConnections():
            say("send a Part")
            if cc == None:
                self.part.setData(None)
            else:
                self.part.setData(cc.Name)
        '''
        say("Volume for {0}: {1:.2f}".format(self.getName(),shape.Volume))
        self.volume.setData(shape.Volume)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Boolean.__doc__

    @staticmethod
    def category():
        return 'Combination'

    @staticmethod
    def keywords():
        return ['Fusion','Cut','Common','Part']






class FreeCAD_VectorArray(FreeCadNodeBase):
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





class FreeCAD_Object(FreeCadNodeBase):
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
        return FreeCAD_Object.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Console(FreeCadNodeBase):
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



class FreeCAD_ShapeExplorer(FreeCadNodeBase):
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






class FreeCAD_ShapeIndex(FreeCadNodeBase):
    '''
    selection of a shape by its index in a list of shapes
    '''


    dok=3
    def __init__(self, name="MyShapeIndex"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

#        self.objname = self.createInputPin("objectname", 'String')
#        self.objname.setData(name)


        p=self.createInputPin('Shapes', 'ShapeListPin')
        p.description="list of shapes #+#"
        p=self.createInputPin('index', 'Integer')
        p.recomputeNode=True
        p.description ="index of the shape"

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


    def compute(self, *args, **kwargs):


        subshapes=self.getPinObjects("Shapes")
        if len(subshapes) == 0:
            sayW("no subshapes")
            return

        try:
            shape=subshapes[self.getData('index')]
        except:
            shape=Part.Shape()

#        say(subshapes)
#        say(self.getData('index'))
        self.setPinObject("Shape",subshapes[self.getData('index')])
        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_ShapeIndex.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape','Edge','Face','Part']




class FreeCAD_Face(FreeCadNodeBase):
    '''
    select a face of a shape by its number
    there can be a reference to a FreeCAD object by its name
    or a shapePin
    '''

    dok=4
    def __init__(self, name="MyFace"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'FacePin')

        a=self.createInputPin('sourceObject', 'String')
        a.description="name of the FreeCAD object from which the face should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with faces"
        p=self.createInputPin('index', 'Integer')
        p.description="number of the face, counting starts with 0"
        p.recomputeNode=True



    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            if shape is None: return
            edge=shape.Faces[self.getPinByName('index').getData()]
        else:
            face=obj.Shape.Edges[self.getPinByName('index').getData()]

        self.setPinObject("Shape_out",face)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Face.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape','Part']



class FreeCAD_Edge(FreeCadNodeBase):
    '''
    select a edge of a shape by its number
    there can be a reference to a FreeCAD object by its name
    or a shapePin
    '''

    dok=4
    
    def __init__(self, name="MyEdge"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'EdgePin')


        a=self.createInputPin('sourceObject', 'String')
        a.description="name of the FreeCAD object from which the edge should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with edges"
        p=self.createInputPin('index', 'Integer')
        p.description="number of the edge, counting starts with 0"
        p.recomputeNode=True


    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            if shape is None: return
            edge=shape.Edges[self.getPinByName('index').getData()]
        else:
            edge=obj.Shape.Edges[self.getPinByName('index').getData()]

        self.setPinObject("Shape_out",edge)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Edge.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape']


class FreeCAD_Destruct_Shape(FreeCadNodeBase):
    '''
    get the edges, faces and points of a shape
    there can be a reference to a FreeCAD object 
    by its name or a shapePin
    '''

    dok=4
    
    def __init__(self, name="MyDestruction"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.outArray = self.createOutputPin('Points', 'VectorPin', structure=StructureType.Array)
        self.outArray.description="a list of the vectors for the vertexes of the shape"
        a=self.createOutputPin('Faces', 'ShapeListPin')
        a.description="list of the faces of the shape"
        b=self.createOutputPin('Edges', 'ShapeListPin')
        a.description="list of the faces of the shape"


        a=self.createInputPin('sourceObject', 'String')
        a.description="name of the FreeCAD object with the shape"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape without part"


    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            
        else:
            shape=obj.Shape
        if shape is None: return
        edges=shape.Edges
        faces=shape.Faces

        points=[v.Point for v in getattr(shape,'Vertexes')]
        self.setData('Points',points)
        self.setPinObjects("Edges",edges)
        self.setPinObjects("Faces",faces)

        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_Edge.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape']




class FreeCAD_Compound(FreeCadNodeBase):
    '''
    compound of a list of shapes
    '''

    dok=4

    def __init__(self, name="MyCompound"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        self.shapes=self.createInputPin('Shapes', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)


    @staticmethod
    def description():
        return FreeCAD_Compound.__doc__

    @staticmethod
    def category():
        return 'Combination'

    @staticmethod
    def keywords():
        return ['Group:','Part']



class FreeCAD_Plot(FreeCadNodeBase):
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


class FreeCAD_Ref(FreeCadNodeBase):
    '''
    a reference to the shape or subobjects of a FreeCAD part
    select a part or some subobjects oof the same object. 
    Than a node with pins for all
    these selected details is created.
    '''

    dok=4
    def __init__(self, name="MyReference",**kvargs):
        try:
            s=FreeCADGui.Selection.getSelection()[0]
            name="REF_"+s.Name
        except:
            name="REF_None"


        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin('Reload Shapes', 'ExecPin', None, self.compute)
        self.inExec.description="force a reload of shape when the shape has changed inside FreeCAD"

        self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.refresh)
        self.inExec.description="set the reference to another subshape which must be selected in FreeCAD before adapt is called"

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.objname = self.createInputPin("objectname", 'String')
        self.objname.description="name of the part used for reference, this parameter is changed automatically by the adapt button."
        self.objname.setData(name)
        self.objname="name of the FreeCAD object"

        self._refpins = []

        try:
            self.refresh()
        except:
            pass


    def refresh(self, *args, **kwargs):
        '''reasign to a new gui selection: create new pins '''

        sels=FreeCADGui.Selection.getSelection()
        subsels=FreeCADGui.Selection.getSelectionEx()
        pins=self.getOrderedPins()

        newpinnames=[]
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                newpinnames += [pinname]

            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape_out"
                newpinnames += [pinname]


        #clean up
        say("newpinnmes",newpinnames)
        oldpinnames=[]
        for p in pins:
            say(p.name)
            if not p.isExec(): 
                if p.name not in newpinnames:
                    say("kill",p.name)
                    p.kill()
                else:
                    oldpinnames += [p.name]

        
        say("oldpinnames",oldpinnames)
        # pins for sub shapes
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                if pinname not in oldpinnames:
                    pintyp="ShapePin"
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                    try:
                        uiPin = self.getWrapper()._createUIPinWrapper(p2)
                        uiPin.setDisplayName("{}".format(p2.name))
                    except:
                        pass

                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape_out"
                pintyp="ShapePin"
                if pinname not in oldpinnames:
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)

                self.setPinObject(pinname,subob)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        self.objname = self.createInputPin("objectname", 'String')
        self.objname.setData(s.ObjectName)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.compute(args,kwargs)


    def createPins(self,objname,pinnames):
            
        # pins for sub shapes
        oldpinnames=[]
        for s in [1]:
            subscreated=False
            for name in pinnames:
                subscreated=True
                pinname=name
                
                if 1: # pinname not in oldpinnames:
                    pintyp="ShapePin"
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                    try:
                        uiPin = self.getWrapper()._createUIPinWrapper(p2)
                        uiPin.setDisplayName("{}".format(p2.name))
                    except:
                        pass

##                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                pinname="Shape_out"
                pintyp="ShapePin"
                if pinname not in oldpinnames:
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)

                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        #self.objname = self.createInputPin("objectname", 'String')
        self.objname.setData(objname)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.compute()
        



    def compute(self, *args, **kwargs):
        '''update shape-links'''

        pins=self.getOrderedPins()
        objname=self.getPinByName("objectname").getData()
        self._refpins=[]

        obj=FreeCAD.activeDocument().getObject(objname)
        for p in pins:
            if not p.isExec():
                if p.name == "Shape_out":
                    self.setPinObject(p.name,obj.Shape)
                elif p.name  !=  "objectname" :
                    try:
                        subob =getattr(obj.Shape,p.name)
                        self.setPinObject(p.name,subob)
                        self._refpins += [p.name]
                    except:
                        pass
        self.outExec.call()

        if self._preview:
            self.preview()
            
        a=self.makebackref()
        if a != None:
            a.sources=[obj]
        
        try:
            wr=self.getWrapper()
            wr.setHeaderHtml("Ref: "+obj.Label)
            self.setColor(b=0,a=0.4)
        except:
            pass


    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']

#--------------------------------


    def serialize(self):
        # eigentliches objekt serialisieren
        data = super(self.__class__, self).serialize()
        # extra data
        data['reflist'] = "extra data for reflisrt"
        data['_refpins'] = self._refpins
        say("serialize")
        say(data['_refpins'])
        return data

    
    def postCreate(self, jsonTemplate=None):
        super(self.__class__, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamic pins extra data
        say("postcreate")

        if jsonTemplate is not None and '_refpins' in jsonTemplate:
            say("process extra data:",jsonTemplate['_refpins'])
            objname=self.getPinByName("objectname").getData()
            pinnames=jsonTemplate['_refpins']
            say(objname)
            say(pinnames)
            self.createPins(objname,pinnames)
            say("done")
            

#--------------------------------

class FreeCAD_RefList(FreeCadNodeBase):
    '''
    a reference to a list of objects
    '''

    def __init__(self, name="MyReferenceList",**kvargs):
        try:
            s=FreeCADGui.Selection.getSelection()[0]
            name="REF_"+s.Name
        except:
            name="REF_None"

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.compute)
#       self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.refresh)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
#        self.objname = self.createInputPin("objectname", 'String')
#        self.objname = self.createInputPin("positions", 'VectorPin',structure=StructureType.Array)
#        self.objname = self.createInputPin("rotations", 'RotationPin',[],structure=StructureType.Array)
#        self.objname.setData(name)

        try:
            self.refresh()
        except:
            pass


    def refresh(self, *args, **kwargs):
        '''reasign to a new gui selection: create new pins '''

        sels=FreeCADGui.Selection.getSelection()
        subsels=FreeCADGui.Selection.getSelectionEx()
        pins=self.getOrderedPins()

        #clean up
        for p in pins:
#            if not p.isExec():
            if not p.isExec() and p.direction  !=  PinDirection.Input :
                p.kill()

        # pins for sub shapes
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                pintyp="ShapePin"
                p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{}".format(p2.name))
                except:
                    pass

                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape"
                pintyp="ShapePin"
                p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                self.setPinObject(pinname,subob)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        #self.objname = self.createInputPin("objectname", 'String')
        #self.objname.setData(s.ObjectName)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.outExec.call()


    def Xcompute(self, *args, **kwargs):
        '''update shape-links'''

        pins=self.getOrderedPins()
        objname=self.getPinByName("objectname").getData()

        obj=FreeCAD.activeDocument().getObject(objname)
        for p in pins:
            if not p.isExec():
                if p.name == "Shape":
                    self.setPinObject(p.name,obj.Shape)
                elif p.name  !=  "objectname":
                    subob =getattr(obj.Shape,p.name)
                    self.setPinObject(p.name,subob)

    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']



class FreeCAD_LOD(FreeCadNodeBase):
    '''
    Level of Detail switch
    '''

    dok=4
    def __init__(self, name="MyLOD",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.lod = self.createInputPin('LOD', 'Integer')
        self.lod.recomputeNode=True
        self.lod.description="Level of detail 1, 2, 3"
        self.createInputPin('ShapeLOD_1', 'ShapePin').description="shape for LOD 1"
        self.createInputPin('ShapeLOD_2', 'ShapePin').description="shape for LOD 2"
        self.createInputPin('ShapeLOD_3', 'ShapePin').description="shape for LOD 3"
        self.createOutputPin('Shape_out', 'ShapePin')


    def compute(self, *args, **kwargs):
        '''update shape-links'''
        lod=self.getData('LOD')
        if lod in [1,2,3]:
            self.setData('Shape_out',self.getData('ShapeLOD_'+str(lod)))
        else:
            say("lod out of range")
        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']



class FreeCAD_View3D(FreeCadNodeBase):
    '''
    create an instance in 3D space of FreeCAD, show the shape
    '''

    dok = 4
    def __init__(self, name="MyView3D",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'String','view3d').\
        description = "name of the object in 3D space"
        self.createInputPin('Workspace', 'String','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"


    @staticmethod
    def description():
        return FreeCAD_View3D.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']


class FreeCAD_bakery(FreeCadNodeBase):
    '''
    Part.show for a shape without parametric connection, the result is not overwritten but a new object is created 
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'String','view3d').\
        description = "name of the object in 3D space"

        self.createInputPin('label', 'String','view3d').\
        description = "label for the object in 3D space"
        #+# todo:add functionality for label

        self.createInputPin('Workspace', 'String','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"

    @staticmethod
    def description():
        return FreeCAD_bakery.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape',]


class FreeCAD_topo(FreeCadNodeBase):
    '''
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'String','view3d').\
        description = "name of the object in 3D space"

        self.createInputPin('label', 'String','view3d').\
        description = "label for the object in 3D space"
        #+# todo:add functionality for label

        self.createInputPin('Workspace', 'String','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"
        self.createOutputPin('Shape_out', 'ShapePin').description="filled face"
        self.createOutputPin('Shape_lost', 'ShapePin').description="filled face"
        self.createOutputPin('Shape_new', 'ShapePin').description="filled face"

    @staticmethod
    def description():
        return FreeCAD_topo.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape',]



class FreeCAD_Conny(FreeCadNodeBase):
    '''
    connect edges and close gaps, create a filled face 
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        '''
        a=self.createInputPin('degree', 'Integer',3)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a=self.createInputPin('rotateAxis', 'Integer',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a=self.createInputPin('simpleConnection', 'Boolean')
        a.recomputeNode=True
        
        '''

        a=self.createInputPin('ff', 'Boolean')
        a.recomputeNode=True
        a.description='a flag to change the ordering of the gap filler curves'

        a=self.createInputPin('tangentForce', 'Integer',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description=' how smooth the open ends of edges should be connected. 0 means no tangent support, this is a straight line from one end to the other'

        a=self.createInputPin('createFace', 'Boolean')
        a.recomputeNode=True
        a.description='''if this flag is set a filled face will be computed. Because the Part.filledFace is a miraclic method this call sometimes fails and other approaches are better'''

        
#        a=self.createInputPin('Shape_in', 'ShapePin')     
#        a.enableOptions(PinOptions.AllowMultipleConnections)
#        a.disableOptions(PinOptions.SupportsOnlyArrays)

        self.shapes=self.createInputPin('Shapes_in', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)
        self.shapes.description='multiple edges or wires which should be connected'


        self.createOutputPin('Shape_out', 'ShapePin').description="a filled face shape or the border (closed curve) of it"
        self.createOutputPin('gaps', 'ShapePin').description="edges created to get wire closed"
        self.createOutputPin('border', 'ShapePin').description="edges of the face only"

    @staticmethod
    def description():
        return FreeCAD_Conny.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Edge','FilledFace',]


class FreeCAD_RandomizePolygon(FreeCadNodeBase):
    '''
    add some randomness to a polygon
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('factorEnds', 'Integer',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description="factor for randomness on the endpoints of the polygon"

        a=self.createInputPin('factorInner', 'Integer',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description="factor for randomness for the inner points of the polygon"

        self.shapes=self.createInputPin('Shape_in', 'ShapePin', None)
        self.arrayData = self.createInputPin('points', 'VectorPin', structure=StructureType.Array)

        self.createOutputPin('Shape_out', 'ShapePin').description="modified points as wire"
        self.arrayData = self.createOutputPin('points_out', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="modified position of the vertexes as vectorlist"

    @staticmethod
    def description():
        return FreeCAD_RandomizePolygon.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Polygon','random','Vector']



class FreeCAD_Toy(FreeCadNodeBase):
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






class FreeCAD_ListOfVectors(FreeCadNodeBase):
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
        return FreeCAD_ListOfVectors.__doc__

    @staticmethod
    def category():
        return 'Conversion'




class FreeCAD_MoveVectors(FreeCadNodeBase):
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


class FreeCAD_ScaleVectors(FreeCadNodeBase):
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



class FreeCAD_RepeatPattern(FreeCadNodeBase):
    '''
    repeat a pattern along a vectors list 
    each vector of vectors is a start position 
    of a copy of the pattern vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('pattern', 'VectorPin', structure=StructureType.Array)
        a.description="list of vectors which define a figure"
        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        a.description="list of starting points  for the copies of the figure pattern"

        a=self.createOutputPin('pattern_out', 'VectorPin', structure=StructureType.Array)
        a.description="list of pattern lists"
        
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description ="Compound of the copied pattern polygons"


    @staticmethod
    def description():
        return FreeCAD_RepeatPattern.__doc__

    @staticmethod
    def category():
        return 'Combination'



class FreeCAD_Transformation(FreeCadNodeBase):
    '''
    affine transformation matrix
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('vectorX', 'VectorPin',FreeCAD.Vector(1,0,0))
        a.recomputeNode=True
        a.description="the result of the first base vector X=(1,0,0)"
        a=self.createInputPin('vectorY', 'VectorPin',FreeCAD.Vector(0,1,0))
        a.recomputeNode=True
        a.description="the result of the 2nd base vector Y=(0,1,0)"
        a=self.createInputPin('vectorZ', 'VectorPin',FreeCAD.Vector(0,0,1))
        a.recomputeNode=True
        a.description="the result of the 3rd base vector X=(0,0,1)"
        a=self.createInputPin('vector0', 'VectorPin',FreeCAD.Vector(0,0,0))
        a.recomputeNode=True
        a.description="movement vector after generic affine transformation"
        
        self.createOutputPin('transformation', 'TransformationPin' )

    @staticmethod
    def description():
        return FreeCAD_Transformation.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_Reduce(FreeCadNodeBase):
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


class FreeCAD_IndexToList(FreeCadNodeBase):
    '''
    create a flag list with 1 for the numbers 
    and 0 for the others
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('index', 'Integer')
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)
        a.description="numbers where the flag should be 1 (the others are 0)"
        a=self.createOutputPin('flags', 'BoolPin',structure=StructureType.Array)
        a.description="list of 0's and 1's"

    @staticmethod
    def description():
        return FreeCAD_IndexToList.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_DistToShape(FreeCadNodeBase):
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


class FreeCAD_CenterOfMass(FreeCadNodeBase):
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


class FreeCAD_ListOfShapes(FreeCadNodeBase):
    '''
    create a list of shapes from single shapes
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createOutputPin('ShapeList', 'ShapeListPin')
        a.description="the ordered list of the input shapes"

        self.pas=self.createInputPin('Shape', 'ShapePin')
        self.pas.description="the shapes are ordered by thy y coordinate of the nodes"
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)


    @staticmethod
    def description():
        return FreeCAD_ListOfShapes.__doc__

    @staticmethod
    def category():
        return 'Conversion'



class FreeCAD_ListOfPlacements(FreeCadNodeBase):
    '''
    create a list of placements from  lists of data
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('moves', 'VectorPin',structure=StructureType.Array)
        a.description="moving vectors/base vector property of the placements, default is (0,0,0) "
        
        a=self.createInputPin('axes', 'VectorPin',structure=StructureType.Array)
        a.description="rotation axes, default is (0,0,1)"
        
        a=self.createInputPin('angles', 'Float',structure=StructureType.Array)
        a.description="rotation angles in degree, default is 0"
        
        a=self.createInputPin('centers', 'VectorPin',structure=StructureType.Array)
        a.description="rotation centers, default is (0,0,0)"

        a=self.createOutputPin('Placements', 'PlacementPin',structure=StructureType.Array)
        a.description="list of placements created from given lists, the length is defined by the longest input list, the values for the other list are filled with default values"

    @staticmethod
    def description():
        return FreeCAD_ListOfPlacements.__doc__



class FreeCAD_ApplyPlacements(FreeCadNodeBase):
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



class FreeCAD_Repeat(FreeCadNodeBase):
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



class FreeCAD_Index(FreeCadNodeBase):
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


class FreeCAD_Zip(FreeCadNodeBase):
    '''
    create a list of vectors from the lists of coordinates
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('x', 'Float',structure=StructureType.Array)
        a.description='list of x coordinates'

        a=self.createInputPin('y', 'Float',structure=StructureType.Array)
        a.description='list of y coordinates'

        a=self.createInputPin('z', 'Float',structure=StructureType.Array)
        a.description='list of z coordinates'

        a=self.createOutputPin('vectors_out', 'VectorPin',structure=StructureType.Array)
        a.description='list of created vectors'

    @staticmethod
    def description():
        return FreeCAD_Zip.__doc__

class FreeCAD_Tube(FreeCadNodeBase):
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




class FreeCAD_Elevation(FreeCadNodeBase):
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
    

class FreeCAD_Camera(FreeCadNodeBase):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        #a=self.createInputPin('filename', 'String','/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/testdata.csv')
        
        #a=self.createInputPin('positionX', 'Float',0)
        #a=self.createInputPin('positionY', 'Float',0)
        #a=self.createInputPin('positionZ', 'Float',0)
        a=self.createInputPin('position', 'VectorPin')
        
        if 0:
            a=self.createInputPin('directionX', 'Float',0)
            a=self.createInputPin('directionY', 'Float',0)
            a=self.createInputPin('directionZ', 'Float',0)
        
            a=self.createInputPin('usePointAt', 'Boolean',True)
        #a=self.createInputPin('pointAtX', 'Float',0)
        #a=self.createInputPin('pointAtY', 'Float',0)
        a=self.createInputPin('angle', 'Float',0)
    
        a=self.createInputPin('pointAt', 'VectorPin')
        
        # geht nicht
        #a=self.createInputPin('nearDistance', 'Float',0)
        #a=self.createInputPin('farDistance', 'Float',1000)
       
        
        #a=self.createInputPin('perspective', 'Boolean',True)
        a=self.createInputPin('trackimages', 'BoolPin',False)
        a=self.createInputPin('timestamp', 'BoolPin',False)
        a=self.createInputPin('trackName', 'StringPin',"camera")
        a=self.createOutputPin('image', 'StringPin')
    
class FreeCAD_Counter(FreeCadNodeBase):
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

        
class FreeCAD_Sleep(FreeCadNodeBase):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        
        a=self.createInputPin('sleep', 'IntPin',0)
        
class FreeCAD_Export(FreeCadNodeBase2):
    '''
    export a shape into a file
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        
        a=self.createInputPin('Shape', 'ShapePin')
        a.description="shape to export"
        a=self.createInputPin('filename', 'StringPin')
        a.description="path to the shape file"
        
        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["BREP","Inventor"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("BREP")
        self.mode.description="format of the file"

    
class FreeCAD_Import(FreeCadNodeBase2):
    '''
    import a shape from a file
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        
        a=self.createInputPin('filename', 'StringPin')
        a.description="path to the shape file"
        
        
        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["BREP","Inventor"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("BREP")
        self.mode.description="format of the file"

        self.createOutputPin('Shape_out', 'ShapePin')
    
    
class FreeCAD_Expression(FreeCadNodeBase):
    '''
    evaluate  an expressions with at most 4 variables
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('modules', 'StringPin')
        a=self.createInputPin('expression', 'StringPin')
        
        a=self.createInputPin('a', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('b', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('c', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('d', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        
        a=self.createOutputPin('string_out', 'StringPin')
        a=self.createOutputPin('float_out', 'FloatPin', None)
        a=self.createOutputPin('int_out', 'IntPin', None)
        a=self.createOutputPin('bool_out', 'BoolPin', None)
   


def nodelist():
    return [
                FreeCAD_Toy,
                FreeCAD_Object,

                FreeCAD_Console,
                FreeCAD_VectorArray,
                FreeCAD_Boolean,

                FreeCAD_Plot,
                FreeCAD_ShapeIndex,
                FreeCAD_ShapeExplorer,
                FreeCAD_Compound,
                FreeCAD_Edge,
                FreeCAD_Face, 

                FreeCAD_Ref,
                
                FreeCAD_LOD,
                FreeCAD_View3D,
                FreeCAD_Destruct_Shape,

                FreeCAD_ListOfVectors,
                FreeCAD_MoveVectors,
                FreeCAD_ScaleVectors,
                FreeCAD_RepeatPattern,
                FreeCAD_Transformation,
                FreeCAD_Reduce,
                FreeCAD_IndexToList,
                FreeCAD_DistToShape,
                FreeCAD_CenterOfMass,
                FreeCAD_ListOfShapes,
                FreeCAD_ListOfPlacements,
                FreeCAD_ApplyPlacements,
                FreeCAD_Repeat,
                FreeCAD_Index,
                FreeCAD_Zip,#ok bis hier
                
                FreeCAD_Tube,

                # noch zu dokumentieren ##############################
                FreeCAD_bakery,
                FreeCAD_topo,
                
                FreeCAD_Conny,
                FreeCAD_RandomizePolygon,
                

                # FreeCAD_RefList, muss noch programmiert werden
                #FreeCAD_ImportFile,
                FreeCAD_Elevation,
                FreeCAD_Camera,
                FreeCAD_Counter,
                FreeCAD_Sleep,
                FreeCAD_Export,
                FreeCAD_Import,
                FreeCAD_Expression,

        ]
