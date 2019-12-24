
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase



class FreeCAD_Mouse(FreeCadNodeBase):
    '''
    a Mouse Sensor
    '''


    def __init__(self, name="MouseSensor"):
       super(self.__class__, self).__init__(name)
#       self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.selectionExec = self.createOutputPin("SelectionChanged", 'ExecPin')
       self.createOutputPin('positionApp', 'VectorPin').description="position of the mouse in the Application window"
       self.createOutputPin('positionWindow', 'VectorPin').description="position of the mouse in the ActiveDocument window"
       #self.createOutputPin('Shape_out', 'ShapePin').description="Shape for illustration"
       self.createOutputPin('positionSelection', 'VectorPin').description="position on a selected component"
       
       self.createOutputPin('selectedFace', 'ShapePin')
       self.selectedFaceChanged = self.createOutputPin("selectedFaceChanged", 'ExecPin')
       self.createInputPin("zIndex", 'Integer')
       
       


    def start(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.start(self,*args, **kwargs)


    def stop(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.stop(self,*args, **kwargs)


    def compute(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Mouse.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['Mouse', 'Keyboard','Position' ]


class FreeCAD_ImportFile(FreeCadNodeBase):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('filename', 'String','/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/testdata.csv')
        
        a=self.createInputPin('force', 'Boolean',True)
        a=self.createOutputPin('data', 'FloatPin',structure=StructureType.Array)
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)


def nodelist():
    return [
                FreeCAD_Mouse,
                FreeCAD_ImportFile,
	]
