'''
nodes which use function pins
'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2
sayl()


class FreeCAD_Function(FreeCadNodeBase2):
    '''
    example impementation of a node which uses a function pin and calculates 
    the value depending on the signature
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('function', 'FunctionPin')
        
        a=self.createInputPin('a', 'Float')
        a=self.createInputPin('b', 'Float')
        a=self.createInputPin('c', 'Float')
        
        
        self.createOutputPin('result', 'FloatPin')

    @staticmethod
    def description():
        return FreeCAD_Function.__doc__

    @staticmethod
    def category():
        return 'Lambda'


class FreeCAD_MinimizeFunction(FreeCadNodeBase2):
    '''
    #+# outdated
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('function', 'FunctionPin')
        
        #a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        self.createInputPin('start', 'VectorPin')
        
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('result', 'FloatPin')

    @staticmethod
    def description():
        return FreeCAD_Function.__doc__

    @staticmethod
    def category():
        return 'Lambda'

class FreeCAD_MinimizeFunction2(FreeCadNodeBase2):
    '''
    finds the local minimum parameter target_min of function(target) 
    using scipy.optimize.minimize
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('function', 'FunctionPin')
        
        #a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        self.createInputPin('start', 'FloatPin',structure=StructureType.Array)
        
        a=self.createInputPin("Method",'StringPin','BFGS')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP',]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("BFGS")
        a.description='''the scipy methods for optimize.
        
If the computation time is to long or not good results are calcuated a change of the method may help. 

see https://docs.scipy.org/doc/scipy/reference/optimize.html'''

        self.createOutputPin('result', 'FloatPin',structure=StructureType.Array)
        self.createOutputPin('minimum', 'FloatPin')

    @staticmethod
    def description():
        return FreeCAD_Function.__doc__

    @staticmethod
    def category():
        return 'Lambda'




class FreeCAD_Expression2Function(FreeCadNodeBase2):
    '''
    creates a function for an expression
    function_out=lambda a,b,c:expression
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createOutputPin('function_out', 'FunctionPin')       
        a=self.createInputPin('expression', 'StringPin','a+100*b+10000*c')


    @staticmethod
    def description():
        return FreeCAD_Expression2Function.__doc__

    @staticmethod
    def category():
        return 'Lambda'


class FreeCAD_SumDistances(FreeCadNodeBase2):
    '''
    defines a function which computes the
    sum of the distances of points from target
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createOutputPin('function_out', 'FunctionPin')       


    @staticmethod
    def description():
        return FreeCAD_SumDistances.__doc__

    @staticmethod
    def category():
        return 'Lambda'

class FreeCAD_SumForces(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createOutputPin('function_out', 'FunctionPin')       


    @staticmethod
    def description():
        return FreeCAD_SumDistances.__doc__

    @staticmethod
    def category():
        return 'Lambda'


class FreeCAD_DemoFunction(FreeCadNodeBase2):
    '''
    a node with some functions to test the function pin
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin("example",'StringPin','find_4_5')
   
        a=self.createOutputPin('function_out', 'FunctionPin')       


    @staticmethod
    def description():
        return FreeCAD_DemoFunction.__doc__

    @staticmethod
    def category():
        return 'Lambda'


class FreeCAD_ReduceFunction(FreeCadNodeBase2):
    '''
    reduces the parameters of a function by values
    examples:
    function_out = lambda a,b :function(a,b,c)
    function_out = lambda b :function(a,b,c)
    function_out = lambda:function(a,b,c)
    
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('function', 'FunctionPin')
        
        a=self.createInputPin('reduse_a', 'Boolean',True)
        a=self.createInputPin('reduse_b', 'Boolean',True)
        a=self.createInputPin('reduse_c', 'Boolean',True)

        a=self.createInputPin('a', 'Float')
        a=self.createInputPin('b', 'Float')
        a=self.createInputPin('c', 'Float')
   
        a=self.createOutputPin('function_out', 'FunctionPin')       
        a=self.createOutputPin('signature', 'StringPin')       

    @staticmethod
    def description():
        return FreeCAD_ReduceFunction.__doc__

    @staticmethod
    def category():
        return 'Lambda'


class FreeCAD_AssignPoints(FreeCadNodeBase2):
    '''
    assigns points to the related parametre of a function
    this node reduces the parameterlist of the function by one
    something like 
    lamda x,y ...: f(points,x,y, ...)
    '''

    videos='https://youtu.be/_2mogZicw_0'
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('function', 'FunctionPin')
        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
            
        a=self.createOutputPin('function_out', 'FunctionPin')       

    @staticmethod
    def description():
        return FreeCAD_AssignPoints.__doc__

    @staticmethod
    def category():
        return 'Lambda'




def nodelist():
    return [
                FreeCAD_AssignPoints,
                FreeCAD_DemoFunction,               
                FreeCAD_Expression2Function,
                FreeCAD_Function,
                #FreeCAD_MinimizeFunction,
                
                FreeCAD_MinimizeFunction2,             
                FreeCAD_ReduceFunction,                
                FreeCAD_SumDistances,
               #FreeCAD_SumForces,
                
        ]
