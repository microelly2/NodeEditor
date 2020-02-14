'''
nodes to create pure coin objects in the 3d view
it is used only for visualization effects
basic routines are found in cointools.py
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import FreeCadNodeBase2, FreeCadNodeBase
from nodeeditor.cointools import *


class FreeCAD_ShapePattern(FreeCadNodeBase2):
    '''
    repeat 3D coin objects along a list of positions
    '''

    videos='https://youtu.be/PC6-fJGbFxg'
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

    @staticmethod
    def category():
        return 'Coin'

    @staticmethod
    def description():
        return FreeCAD_ShapePattern.__doc__


class FreeCAD_QuadMesh(FreeCadNodeBase2):
    '''
    create a coin quadmesh for fast visualization
    '''

    videos='https://youtu.be/B-d1-RsRhzw' 
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('hide','Boolean')
        a.description='hide the representation'
        
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description='array of points to build the grid' 

    @staticmethod
    def category():
        return 'Coin'

    @staticmethod
    def description():
        return FreeCAD_QuadMesh.__doc__



#+# dragger hand muss verbessert werden - eigen pin und kruemmung hinzunehmen

class FreeCAD_Dragger(FreeCadNodeBase):
    '''
    a coin tool to display a draggable placement or a list of such placements
    '''

    videos='https://youtu.be/W_i2X9FR9vY https://youtu.be/tX8y4BHj7BM https://youtu.be/EQ6_5EFUiI4 https://youtu.be/5vhxx2Mt9QI'
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        
        self.inExec = self.createInputPin('start', 'ExecPin', None, self.start)        
        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description='one or more starting position for dragger(s)'
        a=self.createOutputPin('Points_out', 'VectorPin',structure=StructureType.Array)
        a.description='the final positions of the draggers'
        
        a=self.createOutputPin('point_out', 'VectorPin')
        a.description='the final position of the first dragger'
     
        a=self.createOutputPin('hand', 'VectorPin',structure=StructureType.Array)
        a.description='data for the final placement of the first dragger (includes tangent and curvature information'

        a=self.createOutputPin('hands', 'PlacementPin',structure=StructureType.Array)
        a.description='data for the final placement of all draggers'
        
        a = self.createInputPin('reset', 'ExecPin', None, self.resetpoints)
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
        self.start()  

    def stop(self, *args, **kwargs):
        try:
            FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
        except:
            pass
        clearcoin(self)


    @staticmethod
    def category():
        return 'Coin'

    @staticmethod
    def description():
        return FreeCAD_Dragger.__doc__


class FreeCAD_Camera(FreeCadNodeBase2):
    '''

    '''
    videos='https://youtu.be/feBz9Gp2GFU'
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('position', 'VectorPin')
        
        if 0:
            a=self.createInputPin('directionX', 'Float',0)
            a=self.createInputPin('directionY', 'Float',0)
            a=self.createInputPin('directionZ', 'Float',0)
        
            a=self.createInputPin('usePointAt', 'Boolean',True)

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


    @staticmethod
    def category():
        return 'Coin'

    @staticmethod
    def description():
        return FreeCAD_Camera.__doc__



def nodelist():
    return [
                FreeCAD_ShapePattern,
                FreeCAD_Dragger,
                FreeCAD_QuadMesh,
                FreeCAD_Camera,

    ]
