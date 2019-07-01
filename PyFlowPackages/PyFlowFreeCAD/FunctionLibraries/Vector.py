import FreeCAD
from FreeCAD import Vector as MVector

#from nodeeditor.wrapper import MVector # as Vector

import numpy as np

class Array(object):
	def __init__(self,dat=[]):
		self.dat=np.array(dat)

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

class Vector(FunctionLibraryBase):
    '''doc string for Vector'''
    def __init__(self,packageName):
        super(Vector, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecCreate( X=('FloatPin', 0), Y=('FloatPin', 0), Z=('FloatPin', 0)):
        ''' vector by coordinates X, Y, Z.'''
        v = MVector(X,Y,Z)
        return v

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecArray ( X=('ArrayPin', Array())):
        ''' vector by coordinates X, Y, Z.'''
        v = MVector()
        return v

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecX( Vector=('VectorPin', MVector())):
        ''' vector coordinate x'''
        return Vector.x

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecY( Vector=('VectorPin', MVector())):
        ''' vector coordinate y'''
        return Vector.y

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecZ( Vector=('VectorPin', MVector())):
        ''' vector coordinate z'''
        return Vector.z

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", 0.0), meta={'Category': 'Vector', 'Keywords': ['vector', '|', 'dot', 'product']})
    def vecDotProduct(a=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "VectorPin", "QuatPin"]}),
                   b=("AnyPin", None, {"constraint": "1", "supportedDataTypes": ["FloatVector4Pin", "VectorPin", "QuatPin"]})):
        '''Dot product'''
        return a.dot(b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector(1,2,3)), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '+']})
    def vecAdd(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''adds vector a and b'''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def vecSubstract(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''substracts vector a and b'''
        return a - b

