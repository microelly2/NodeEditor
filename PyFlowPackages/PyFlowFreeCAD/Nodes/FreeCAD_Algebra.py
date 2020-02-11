'''
expressions, equations, simple algebra
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2

        

class FreeCAD_Expression(FreeCadNodeBase2):
    '''
    evaluate an expression with at most 4 variables
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('modules', 'StringPin','time')
        a.description="required module names separated by comma"
        a=self.createInputPin('expression', 'StringPin','time.time()+a')
        a.description="expression with at most 4 variables a, b, c, d"
        
        a=self.createInputPin('a', 'AnyPin',0.0)
        a.enableOptions(PinOptions.AllowAny)
        a.description="first parameter"
        a=self.createInputPin('b', 'AnyPin')
        a.description="2nd parameter"
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('c', 'AnyPin')
        a.description="3. parameter"
        a.enableOptions(PinOptions.AllowAny)
        a=self.createInputPin('d', 'AnyPin')
        a.enableOptions(PinOptions.AllowAny)
        a.description="last parameter"
        
        a=self.createOutputPin('string_out', 'StringPin')
        a.description="result as string"
        a=self.createOutputPin('float_out', 'FloatPin', None)
        a.description="result as float"
        a=self.createOutputPin('int_out', 'IntPin', None)
        a.description="result as integer"
        a=self.createOutputPin('bool_out', 'BoolPin', None)
        a.description="result as boolean"
 
    @staticmethod
    def description():
        return FreeCAD_Expression.__doc__

    @staticmethod
    def category():
        return 'Algebra'

__all__= [
			FreeCAD_Expression,
                
        ]

 
def nodelist():
    return __all__
