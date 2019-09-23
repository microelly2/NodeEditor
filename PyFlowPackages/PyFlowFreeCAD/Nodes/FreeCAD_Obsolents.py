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


