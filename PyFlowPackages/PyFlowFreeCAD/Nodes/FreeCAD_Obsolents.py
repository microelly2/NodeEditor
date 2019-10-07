# nodes, die nicht mehr gebraucht werden




class FreeCAD_Part(FreeCadNodeBase):
    '''
    Part.show(aShape) see node view3D
    '''

    @staticmethod
    def description():
        return '''creates a Part for a given shape: Part.show(shape)'''

    def __init__(self, name="Fusion"):
        super(FreeCAD_Part, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapein = self.createInputPin('Shape', 'ShapePin')
        self.shapein.recomputeNode=True
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)


    def compute(self, *args, **kwargs):

        shape=self.getPinObject("Shape")
        say(shape)
        if shape == None:
            sayW("no shape connected to pin Shape")
            return
        cc=self.getObject()
        say(cc)
        cc.Label=self.objname.getData()
        cc.Shape=shape
        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Plot.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Shape','3View3D']



class FreeCAD_YYY(FreeCadNodeBase):
    '''
    position on a surface or curve
    '''

    def __init__(self, name="LOD",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d')
        a=self.createInputPin('u', 'FloatPin',0)
        a.recomputeNode=True
        a=self.createInputPin('v', 'FloatPin',0)
        a.recomputeNode=True
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('placement', 'PlacementPin' )
        self.createInputPin("display", 'BoolPin', True)
        self.createInputPin("directionNormale", 'BoolPin', False)
        self.createInputPin("curvatureMode", 'BoolPin', True)
        


    @staticmethod
    def description():
        return FreeCAD_YYY.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Surface','position','Point','uv']


class FreeCAD_Bar(FreeCadNodeBase):
    '''
    dummy for tests
    '''

    def __init__(self, name="Fusion"):
       super(self.__class__, self).__init__(name)
#       self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.createOutputPin('positionApp', 'VectorPin')#.description="position of the mouse in the application window"
       self.createOutputPin('positionWindow', 'VectorPin')
       self.createOutputPin('Shape_out', 'ShapePin').description="Shape for illustration"
 

    @staticmethod
    def description():
        return FreeCAD_Bar.__doc__

    @staticmethod
    def category():
        return 'Development'

    @staticmethod
    def keywords():
        return []

