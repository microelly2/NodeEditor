import FreeCAD
from FreeCAD import Rotation # as MRotation
from FreeCAD import Vector


from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class Rotation(FunctionLibraryBase):
    '''doc string for Rotation'''
    def __init__(self,packageName):
        super(Rotation, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', Rotation()), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreateEuler(Yaw=('FloatPin', 0), Pitch=('FloatPin', 0), Roll=('FloatPin', 0)):
        '''create Rotation from Euler angles'''
        return Rotation(Yaw,Pitch,Roll) 

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', Rotation()), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreate(Axis=('VectorPin', Vector(0,0,1)), Angle=('FloatPin', 0)):
        '''create Rotation from axis and angle'''
        return Rotation(Axis,Angle) 

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', Rotation()), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})

    def rotCreateBy2Vectors(From=('VectorPin', Vector(1,0,0)), To=('VectorPin', Vector(0,1,0))):
        '''create Rotation between vectors From and To'''
        return Rotation(From,To) 

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', Rotation()), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreateBy3Vectors(X=('VectorPin', Vector(1,0,0)), Y=('VectorPin', Vector(0,1,0)),Z=('VectorPin', Vector(0,0,1)),mode=('StringPin','ZXY')):
        ''' three vectors that define rotated axes directions + an optional 3-characher string of capital letters 'X', 'Y', 'Z' that sets the order of importance of the axes (e.g., 'ZXY' means z direction is followed strictly, x is used but corrected if necessary, y is ignored) '''
        return Rotation(X,Y,Z,mode) 


    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', Rotation()), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotMultiply(a=('RotationPin', Rotation()), b=('RotationPin', Rotation())):
        '''concatenate Rotation a and b'''
        return a.multiply(b) 

