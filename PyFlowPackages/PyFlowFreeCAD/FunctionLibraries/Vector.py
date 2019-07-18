import FreeCAD
from FreeCAD import Vector as MVector

#from nodeeditor.wrapper import MVector # as Vector

import numpy as np
from nodeeditor.say import *

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

#    @staticmethod
#    @IMPLEMENT_NODE(returns=('VectorPin', MVector()), nodeType=NodeTypes.Pure, meta={'Category': 'Vector', 'Keywords': ['Vector']})
#    def vecArray ( X=('ArrayPin', Array())):
#        ''' vector by coordinates X, Y, Z.'''
#        v = MVector()
#        return v

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

#-------------numpy lib starts here -------------------------

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {'constraint': '1'}), meta={'Category': 'numpy', 'Keywords': ['list','interval']})
    def linSpace(start=('FloatPin',0.),stop=('FloatPin',10), num=('IntPin', 50)):
        """create a linear Space"""

        x1 = np.linspace(start, stop, num, endpoint=True)
        return list(x1)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [2.],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','random']})
    def randomList(size=('IntPin', 10)):
        """create a random list"""
        
        x1 = np.random.random(size)
        return list(x1)


    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','random']})
    def zip(x=('AnyPin', [0]),y=('AnyPin', [1]),z=('AnyPin', [2])) :
        """combine """
        
        res=np.array([x,y,z]).swapaxes(0,1)
        points=[FreeCAD.Vector(list(a)) for a in res]    
        return points

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def scale(data=('AnyPin', [0]),factor=('FloatPin', 1.)) :
        """multiply datalist with factor """
        
        return list(np.array(data)*factor)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def linearTrafo(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 0.)) :
        """a*x + b """
        
        return list(np.array(data)*a +b)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy', 'Keywords': ['list','scale','multiply']})
    def sin(data=('AnyPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 1.)) :
        """a*sin(b*x+c)"""
        
        return list(a*np.sin(np.array(data)*b +c))

