import FreeCAD
from FreeCAD import Placement,Rotation,Vector

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

from nodeeditor.say import *

class Placement(FunctionLibraryBase):
    '''doc string for Placement'''
    def __init__(self,packageName):
        super(Placement, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('PlacementPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Placement', 'Keywords': ['Placement', '+']})
    def pmMultiply(a=('PlacementPin', [0]), b=('PlacementPin', [0])):
        '''multiply Placements a, b'''
        #say("a",a)
        #say("b",b)
        pma=FreeCAD.Placement(FreeCAD.Matrix(*a))
        pmb=FreeCAD.Placement(FreeCAD.Matrix(*b))
        #say("pma",pma)
        #say("pmb",pmb)
        pmc=pma.multiply(pmb)
        #say("pmc",pmc)
        
        return list(pmc.toMatrix().A)


    @staticmethod
    @IMPLEMENT_NODE(returns=('PlacementPin', []), nodeType=NodeTypes.Pure, meta={'Category': 'Placement', 'Keywords': ['Placement', '+']})
    def pmCreate(base=('VectorPin', Vector(1,2,3)), rotation=('RotationPin', [7,8,9])):
        '''create Placement from Base and Rotation '''
        #say("placementbase",base)
        #say("rot",rotation)
        #say("rotation",FreeCAD.Rotation(*rotation))
        rota=FreeCAD.Rotation(*rotation)
        #say(FreeCAD.Placement(base, rota))
        
        return list(FreeCAD.Placement(base, rota).toMatrix().A)

