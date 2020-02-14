'''

'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2




class FreeCAD_Ref(FreeCadNodeBase2):
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

class FreeCAD_RefList(FreeCadNodeBase2):
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



class FreeCAD_LOD(FreeCadNodeBase2):
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



class FreeCAD_View3D(FreeCadNodeBase2):
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
        self.createInputPin('off','Boolean')


    @staticmethod
    def description():
        return FreeCAD_View3D.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']




class FreeCAD_bakery(FreeCadNodeBase2):
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



class FreeCAD_topo(FreeCadNodeBase2):
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




class FreeCAD_Conny(FreeCadNodeBase2):
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



def nodelist():
    return [
			FreeCAD_View3D,
			FreeCAD_bakery,
			FreeCAD_Ref,
			#FreeCAD_RefList,
			FreeCAD_LOD,
			
			
		]

