'''
Program flow
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2



    
class FreeCAD_Counter(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('reset', 'ExecPin', None, self.freset)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
    
        
        a=self.createOutputPin('count', 'IntPin',0)
        
    
    def freset(self,*args, **kwargs):
        self.setData("count",0)
        self.outExec.call()
        self.setColor()

        
class FreeCAD_Sleep(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        
        a=self.createInputPin('sleep', 'IntPin',0)



def nodelist():
    return [
                FreeCAD_Counter,##
                FreeCAD_Sleep,##
                
        ]
