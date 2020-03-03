import FreeCAD
from FreeCAD import Vector as MVector

#from nodeeditor.wrapper import MVector # as Vector

import numpy as np
from nodeeditor.say import *
import nodeeditor.store as store

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
    def list2Vector( XYZ=('FloatPin', [],{"enabledOptions": PinOptions.ArraySupported })):
        ''' vector by coordinates X, Y, Z.'''
        v = MVector(*XYZ)
        return v

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
    def vecCreate( X=('Float', 0), Y=('Float', 0), Z=('Float', 0)):
        ''' vector by coordinates X, Y, Z.'''
        v = MVector(X,Y,Z)
        #say("create vector",v)
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
    @IMPLEMENT_NODE(returns=('VectorPin', MVector(1,2,3)), nodeType=NodeTypes.Pure, 
		meta={'Category': 'Vector', 'Keywords': ['Vector', '+']})
    def vecAdd(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''adds vector a and b'''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def vecSubstract(a=('VectorPin', MVector()), b=('VectorPin', MVector())):
        '''substracts vector a and b'''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def between(a=('VectorPin', MVector()), b=('VectorPin', MVector()),m=('Integer',5)):
        '''between vector a and b'''
        
        return a *0.1*(10-m)+b*m*0.1

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def betweenList(a=('AnyPin', [],{'constraint': '1', 
                "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
        b=('AnyPin', [],{'constraint': '1', 
                "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
        m=('Integer',5)):
        '''between list a and b'''
        rc=[av *0.1*(10-m)+bv*m*0.1 for av,bv in zip(a,b)]
        return rc


    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', [MVector()]),  meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    @IMPLEMENT_NODE(returns=('AnyPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector', '-']})
    def move(
				a=('AnyPin', [],{"enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), 
                v=('VectorPin', MVector()),
			):
        ''' add vector v to a list of vectors a'''
        

        rc=[MVector(av)+v for av in a]
        say(rc)
        return rc



    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', "workspace", ),  meta={'Category': 'Document', 'Keywords': []})
    def workspace(name=('String', "workspace"), temp=('BoolPin', True),):

        say("workspace called")
        return (name)

