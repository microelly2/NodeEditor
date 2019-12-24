'''
import numpy as np
import random
import functools
import time
import inspect

from FreeCAD import Vector
import FreeCAD
import FreeCADGui
import Part

from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

import nodeeditor.store as store
from nodeeditor.say import *




import sys
if sys.version_info[0] !=2:
    from importlib import reload
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase
sayl()




class FreeCAD_LessThan(FreeCadNodeBase):
    '''
    compare a list of floats with a threshold
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('values', 'Float',structure=StructureType.Array)
        a=self.createInputPin('threshold', 'Float')

        a=self.createOutputPin('lessThan', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_LessThan.__doc__

    @staticmethod
    def category():
        return 'Logic'

class FreeCAD_MoreThan(FreeCadNodeBase):
    '''
    compare a list of floats with a treshold
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('values', 'Float',structure=StructureType.Array)
        a=self.createInputPin('treshold', 'Float')

        a=self.createOutputPin('moreThan', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_MoreThan.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_Equal(FreeCadNodeBase):
    '''
    compare a list of floats with a treshold
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('values', 'Float',structure=StructureType.Array)
        a=self.createInputPin('value', 'Float')

        a=self.createOutputPin('equal', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_Equal.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_Nearly(FreeCadNodeBase):
    '''
    compare a list of floats with a threshold
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('values', 'Float',structure=StructureType.Array)
        a=self.createInputPin('value', 'Float')
        a=self.createInputPin('tolerance', 'Float',0.1)

        a=self.createOutputPin('nearly', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_Nearly.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_And(FreeCadNodeBase):
    '''
    booloan and of two boolean lists
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('a', 'Boolean',structure=StructureType.Array)
        a=self.createInputPin('b', 'Boolean',structure=StructureType.Array)
        a=self.createOutputPin('and', 'BoolPin',structure=StructureType.Array)
        
        a.description="elementwisewise a and b "

    @staticmethod
    def description():
        return FreeCAD_And.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_Or(FreeCadNodeBase):
    '''
    booloan or of two boolean lists
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('a', 'Boolean',structure=StructureType.Array)
        a=self.createInputPin('b', 'Boolean',structure=StructureType.Array)
        a=self.createOutputPin('or', 'BoolPin',structure=StructureType.Array)
        
        a.description="elementwisewise a or b "

    @staticmethod
    def description():
        return FreeCAD_Or.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_Not(FreeCadNodeBase):
    '''
    boolean not of a boolean list
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('a', 'Boolean',structure=StructureType.Array)
        a=self.createOutputPin('not', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_Not.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_True(FreeCadNodeBase):
    '''
    boolean true  lists
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('count', 'Integer',3)
        a=self.createOutputPin('true', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_True.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_False(FreeCadNodeBase):
    '''
    boolean false lists
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('count', 'Integer',3)
        a=self.createOutputPin('false', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_False.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_BoolToy(FreeCadNodeBase):
    '''
    boolean toy - make a flag list of 4 values
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('flagA', 'Boolean')
        a=self.createInputPin('flagB', 'Boolean')
        a=self.createInputPin('flagC', 'Boolean')
        a=self.createInputPin('flagD', 'Boolean')
        a=self.createOutputPin('flags', 'BoolPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_BoolToy.__doc__

    @staticmethod
    def category():
        return 'Logic'


class FreeCAD_FloatToy(FreeCadNodeBase):
    '''
    float toy - make a list of 10 floats
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        for i in range(11):
            a=self.createInputPin('float', 'Float',i)

        a=self.createInputPin('scale', 'Float',1)
        a.description="all floats are multiplied with this parameter"

        a=self.createInputPin('start', 'Float',0)
        a.description="this parameter is added to the floats"

        a=self.createInputPin('limit', 'Integer',10)
        a.description="maximum count of floats in use "

        a=self.createInputPin('trailer', 'Float',structure=StructureType.Array)
        a.description="these floats are appended to get larger arrays" 

        a=self.createOutputPin('floats', 'FloatPin',structure=StructureType.Array)
        

    @staticmethod
    def description():
        return FreeCAD_BoolToy.__doc__

    @staticmethod
    def category():
        return 'Logic'







def nodelist():
    return [
                FreeCAD_LessThan,
                FreeCAD_MoreThan,
                FreeCAD_Equal,
                FreeCAD_Nearly,

                FreeCAD_And,
                FreeCAD_Or,
                FreeCAD_Not,
                FreeCAD_True,
                FreeCAD_False,

                FreeCAD_BoolToy,
                FreeCAD_FloatToy,
                
        ]



