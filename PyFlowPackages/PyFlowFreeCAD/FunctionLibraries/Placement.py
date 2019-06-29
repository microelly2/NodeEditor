import FreeCAD
from FreeCAD import Placement,Rotation,Vector

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

class Placement(FunctionLibraryBase):
    '''doc string for Placement'''
    def __init__(self,packageName):
        super(Placement, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('PlacementPin', Placement()), nodeType=NodeTypes.Pure, meta={'Category': 'Placement', 'Keywords': ['Placement', '+']})
    def pmMultiply(a=('PlacementPin', Placement()), b=('PlacementPin', Placement())):
        '''multiply Placements a, b'''
        return a #.multiply(b) 


    @staticmethod
    @IMPLEMENT_NODE(returns=('PlacementPin', Placement()), nodeType=NodeTypes.Pure, meta={'Category': 'Placement', 'Keywords': ['Placement', '+']})
    def pmCreate(Base=('VectorPin', Vector()), Rotation=('RotationPin', Rotation())):
        '''create Placement from Base and Rotation '''
        return Placement(Base, Rotation)

