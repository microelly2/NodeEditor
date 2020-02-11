'''
Placement of a FreeCAD object
'''

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *



from FreeCAD import Vector
import FreeCAD
import Part

from nodeeditor.say import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2


# example shape
def createShape(a):

    pa=FreeCAD.Vector(0,0,0)
    pb=FreeCAD.Vector(a*50,0,0)
    pc=FreeCAD.Vector(0,50,0)
    shape=Part.makePolygon([pa,pb,pc,pa])
    return shape


def updatePart(name,shape):

    FreeCAD.Console.PrintError("update Shape for "+name+"\n")
    a=FreeCAD.ActiveDocument.getObject(name)
    if a== None:
        a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
    a.Shape=shape



def onBeforeChange_example(self,newData,*args, **kwargs):
    FreeCAD.Console.PrintError("before:"+str(self)+"\n")
    FreeCAD.Console.PrintError("data before:"+str(self.getData())+"-- > will change to:"+str(newData) +"\n")
    # do something like backup or checks before change here

def onChanged_example(self,*args, **kwargs):
    FreeCAD.Console.PrintError("Changed data to:"+str(self.getData()) +"\n")
    self.owningNode().reshape()




class FreeCAD_Placement(FreeCadNodeBase2):
    '''
    Placement xyz
    '''

    def __init__(self, name='huhu'):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.pa = self.createInputPin('Placement_Base', 'VectorPin',FreeCAD.Vector())
        self.pb = self.createInputPin('Rotation_Axis', 'VectorPin',FreeCAD.Vector(0,0,1))
        self.pc = self.createInputPin('Rotation_Angle', 'FloatPin',0.0)

        #self.pc.onChanged=onChanged_example
        #self.pc.onBeforeChange=onBeforeChange_example

        self.vobjname = self.createInputPin("objectname", 'StringPin')
        self.vobjname.setData(name)

        self.Shape="DAS IST SHAPE"
        self.pa.recomputeNode=True
        self.pb.recomputeNode=True
        self.pc.recomputeNode=True


    @staticmethod
    def xcategory():
        return 'Placement'


    @staticmethod
    def description():
        return "change Placement of the FreeCAD object"

    def compute(self, *args, **kwargs):

        # change the placement of Box example
        c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())
        if c is not None:
            c.Placement.Base=10*self.pa.getData()
            c.Placement.Rotation.Angle=100*self.pc.getData()
            self.outExec.call()
        else:
            sayW("no object found",self.vobjname.getData())

    @staticmethod
    def category():
        return 'Placement'







def nodelist():
    return [
            FreeCAD_Placement,
                
        ]
