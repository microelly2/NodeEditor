'''
Data: List Array Tree
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2




class FreeCAD_Repeat(FreeCadNodeBase2):
    '''
    list of the same element repeated
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('in', 'AnyPin',constraint='1')   
        a.description="element to repeat"

        a=self.createOutputPin('out', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description="__count__ repetitions of element __in__" 

        a=self.createInputPin('count', 'Integer',2) 
        a.description="how often to repeat element __in__"
          
        a=self.createOutputPin('Shapes', 'ShapeListPin')
        a.description="list of shapes if input element __in__ is a shape"

        
    @staticmethod
    def description():
        return FreeCAD_Repeat.__doc__

    @staticmethod
    def category():
        return 'Data'



class FreeCAD_Index(FreeCadNodeBase2):
    '''
    returns item with a given index from a list
    '''

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

    @staticmethod
    def category():
        return 'Data'


def nodelist():
    return [

                FreeCAD_Index,
                FreeCAD_Repeat,
                
        ]
