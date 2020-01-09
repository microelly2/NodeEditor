
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2, FreeCadNodeBase


class FreeCAD_ShapePattern(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('hide','Boolean')
        a = self.createInputPin('mode', 'String')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["cone","sphere","cylinder","cube","line","tree","human"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("cone")
        a=self.createInputPin('height',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('width',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('randomize',"Integer")
        a.setInputWidgetVariant("Slider")

        
        a=self.createInputPin('points', 'VectorPin')
        a.setInputWidgetVariant("NO")
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('color', 'VectorPin')
        a.setInputWidgetVariant("NO")
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('radius', 'FloatPin',10)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

  
        self.createOutputPin('Points_out', 'VectorPin')


class FreeCAD_QuadMesh(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('hide','Boolean')
        
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)




class FreeCAD_Dragger(FreeCadNodeBase):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('start', 'ExecPin', None, self.start)
        
        
        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a=self.createOutputPin('Points_out', 'VectorPin',structure=StructureType.Array)
        
        self.inExec = self.createInputPin('reset', 'ExecPin', None, self.resetpoints)
        a=self.createInputPin("ticktime","Integer",-100)
        a.setInputWidgetVariant("Slider")

    def start(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_dragger(self)

    def resetpoints(self, *args, **kwargs):
        del(self.points)

    def stop(self, *args, **kwargs):
        try:
            FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
        except:
            pass



    def Tick(self, delta):     
        
        if self.getData("ticktime")==-100:
            return
        try:
           self._total += delta
        except:
            self._total= delta
           
        if self._total >= (self.getData("ticktime")+100)/1000:
                self.compute()
                self._total=0



def nodelist():
    return [
                FreeCAD_ShapePattern,
                FreeCAD_Dragger,
                FreeCAD_QuadMesh,

    ]
