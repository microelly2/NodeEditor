
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
        a.description='hide or show pattern'
        
        a = self.createInputPin('mode', 'String')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["cone","sphere","cylinder","cube","line","tree","human"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("cone")
        a.description='predefined object to display'
        
        a=self.createInputPin('height',"Integer")
        a.setInputWidgetVariant("Slider")
        a.description='to scale the pattern in z direction'
        
        a=self.createInputPin('width',"Integer")
        a.setInputWidgetVariant("Slider")
        a.description='to scale the pattern in xy directions'
        a=self.createInputPin('randomize',"Integer")
        a.setInputWidgetVariant("Slider")
        a.description='use it to create the pattern in different sizes for example with tree for a forest'
        
        a=self.createInputPin('points', 'VectorPin')
        a.setInputWidgetVariant("NO")
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)
        a.description="list fo vectors where the pattern should accure"

        a=self.createInputPin('forces', 'VectorPin')
        a.setInputWidgetVariant("NO")
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)
        a.description='is used to display the line pattern: direction and length of the line'


        a=self.createInputPin('color', 'VectorPin')
        a.setInputWidgetVariant("NO")
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)
        a.description='list of vector to define the rgb color for each pattern'

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
	a coin tool to display a draggable placement or a list of such placements
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
        a=self.createOutputPin('point_out', 'VectorPin')
        
        self.inExec = self.createInputPin('reset', 'ExecPin', None, self.resetpoints)
#        a=self.createInputPin("tickOff","Boolean")
#        a=self.createInputPin("ticktime","Integer",-100)
        a.setInputWidgetVariant("Slider")

    def start(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_dragger(self)

    def resetpoints(self, *args, **kwargs):
        try:
            del(self.points)
        except:
            pass

    def stop(self, *args, **kwargs):
        try:
            FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
        except:
            pass

	# example implementation for automated running inside pyflow
    def XX_DEACTIVETED_Tick(self, delta):     
        
        if self.getData("ticktime")==-100 or self.getData('tickOff'):
            return
        try:
           self._total += delta
        except:
            self._total= delta
           
        if self._total >= (self.getData("ticktime")+100)/200:
                self.compute()
                self._total=0



def nodelist():
    return [
                FreeCAD_ShapePattern,
                FreeCAD_Dragger,
                FreeCAD_QuadMesh,

    ]
