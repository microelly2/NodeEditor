'''
all still not categorized nodes
'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2



class FreeCAD_Tube(FreeCadNodeBase2):
    '''
    calculate the points for a parametric tube along a backbone curve
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('backbone', 'ShapePin')
        a.description="backbone curve for the tube"
        a=self.createInputPin('parameter', 'Float',structure=StructureType.Array)
        a.description="u parameter of the position of the ribs"
        a=self.createInputPin('radius', 'Float',structure=StructureType.Array)
        a.description="radius/size of the rib rings"
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="array of poles for the postprocessing bspline surface"

    @staticmethod
    def description():
        return FreeCAD_Tube.__doc__

    @staticmethod
    def category():
        return 'Object'



def nodelist():
    return [

                FreeCAD_Tube,
                
        ]


# hack wird irgendwo geladen warun #+#
# muss wieder raus, weil schon in information !!!
class FreeCAD_Object(FreeCadNodeBase2):
    def __init__(self, name="MyToy"):

            super(self.__class__, self).__init__(name)
            self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
            self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       
    
    
    pass
    
    
