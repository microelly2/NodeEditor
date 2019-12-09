import FreeCAD
#from FreeCAD import Rotation as MRotation
from FreeCAD import Vector


from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

from nodeeditor.say import *

class Rotation(FunctionLibraryBase):
    '''doc string for Rotation'''
    def __init__(self,packageName):
        super(Rotation, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', (0,0,0)), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreateEuler(Yaw=('FloatPin', 0), Pitch=('FloatPin', 0), Roll=('FloatPin', 0)):
        '''create Rotation from Euler angles'''
        say("rot create euler ",Yaw,Pitch,Roll)
        return [Yaw,Pitch,Roll]

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [0,0,0]), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreate(Axis=('VectorPin', Vector(0,0,1)), Angle=('FloatPin', 10)):
        '''create Rotation from axis and angle'''
        a=FreeCAD.Rotation(Axis,Angle)
        say("rot create",a.toEuler())
        return list(a.toEuler())

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [0,0,0]), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})

    def rotCreateBy2Vectors(From=('VectorPin', Vector(1,0,0)), To=('VectorPin', Vector(0,1,0))):
        '''create Rotation between vectors From and To'''
        return FreeCAD.Rotation(From,To).toEuler() 

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [0,0,0]), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotCreateBy3Vectors(X=('VectorPin', Vector(1,0,0)), Y=('VectorPin', Vector(0,1,0)),Z=('VectorPin', Vector(0,0,1)),mode=('StringPin','ZXY')):
        ''' three vectors that define rotated axes directions + an optional 3-characher string of capital letters 'X', 'Y', 'Z' that sets the order of importance of the axes (e.g., 'ZXY' means z direction is followed strictly, x is used but corrected if necessary, y is ignored) '''
        return list(FreeCAD.Rotation(X,Y,Z,mode).toEuler())


    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [0,0,0]), nodeType=NodeTypes.Pure, meta={'Category': 'Rotation', 'Keywords': ['Rotation', '+']})
    def rotMultiply(a=('RotationPin', [1,0,0]), b=('RotationPin', [0,1,0])):
        '''concatenate Rotation a and b'''
        say("rot mult a",a)
        say("rot mult b",b)
        return list(FreeCAD.Rotation(*a).multiply(FreeCAD.Rotation(*b)).toEuler())

