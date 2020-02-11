'''
import and export related to filesystem
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2


class FreeCAD_Export(FreeCadNodeBase2):
    '''
    export a shape into a file
    '''

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

    @staticmethod
    def description():
        return FreeCAD_Export.__doc__

    @staticmethod
    def category():
        return 'File'

    
class FreeCAD_Import(FreeCadNodeBase2):
    '''
    import a shape from a file
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('filename', 'StringPin')
        a.description="path to the shape file"       
        
        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["BREP"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("BREP")
        self.mode.description="format of the file"

        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_Import.__doc__

    @staticmethod
    def category():
        return 'File'



__all__= [
		FreeCAD_Import,
		FreeCAD_Export,
		
	]

def nodelist():
	return __all__
