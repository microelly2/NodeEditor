
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2


class FreeCAD_ImageT(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        fn=self.createInputPin('image', 'StringPin','/home/thomas/Bilder/cp_069.png')
        a=self.createInputPin('red', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('green', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('blue', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        
       
        a=self.createInputPin('invert', 'Boolean',0)

        a = self.createInputPin('mode', 'String')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["raw","closing","opening","erosion","diletation"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("raw")

        a=self.createInputPin('maskSize', 'Integer',0, {
            PinSpecifires.INPUT_WIDGET_VARIANT : "Slider", 
            PinSpecifires.VALUE_RANGE: (0,20),})
        a.setInputWidgetVariant("Slider")

#        a=self.createInputPin('bubbles', 'Boolean',0)
#        a=self.createInputPin('bubbleSize', 'Integer',0)
#        a.setInputWidgetVariant("Slider")

   
        self.createOutputPin('Points_out', 'VectorPin')




def nodelist():
    return [
                FreeCAD_ImageT,

	]
