'''

'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2



class FreeCAD_Boolean(FreeCadNodeBase2):
    '''boolean ops of two parts example'''

    def __init__(self, name="Fusion"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
        self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

        self.shape1 = self.createInputPin('Shape_in1', 'ShapePin')
        self.shape2 = self.createInputPin('Shape_in2', 'ShapePin')

        self.mode = self.createInputPin('mode', 'String')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["fuse","cut","common","fragments"]
            }
        self.mode.setInputWidgetVariant("EnumWidget")
        self.mode.setData("fuse")

        self.volume = self.createOutputPin('Volume', 'FloatPin')


    @timer
    def compute(self, *args, **kwargs):

        mode=self.mode.getData()
        self.setNodename("Boolean "+mode)
        self.setImage("freecad_"+mode)

        shape1=self.shape1.getData()
        shape2=self.shape2.getData()

        s1=store.store().get(shape1)
        s2=store.store().get(shape2)

        if s1  !=  None and s2  != None:
            # arbeite mit shapes
            pass

        else:
            part1=self.part1.getData()
            part2=self.part2.getData()
            if part1 == None or part2 == None:
                say("part12 is None, abort")
                return

            s1=store.store().get(part1)
            if not s1.__class__.__name__ =='Solid':
                part1=FreeCAD.ActiveDocument.getObject(part1)
                s1=part1.Shape

            s2=store.store().get(part2)
            if not s2.__class__.__name__ =='Solid':
                part2=FreeCAD.ActiveDocument.getObject(part2)
                s2=part2.Shape

        
        if mode == 'common':
            shape=s1.common(s2)
        elif mode == 'cut':
            shape=s1.cut(s2)
        else:
            shape=s1.fuse(s2)


        self.setPinObject('Shape_out',shape)

        '''
        if self.part.hasConnections():
            say("send a Part")
            if cc == None:
                self.part.setData(None)
            else:
                self.part.setData(cc.Name)
        '''
        say("Volume for {0}: {1:.2f}".format(self.getName(),shape.Volume))
        self.volume.setData(shape.Volume)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Boolean.__doc__

    @staticmethod
    def category():
        return 'Combination'

    @staticmethod
    def keywords():
        return ['Fusion','Cut','Common','Part']



class FreeCAD_Compound(FreeCadNodeBase2):
    '''
    compound of a list of shapes
    '''

    dok=4

    def __init__(self, name="MyCompound"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        self.shapes=self.createInputPin('Shapes', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)


    @staticmethod
    def description():
        return FreeCAD_Compound.__doc__

    @staticmethod
    def category():
        return 'Combination'

    @staticmethod
    def keywords():
        return ['Group:','Part']


class FreeCAD_RepeatPattern(FreeCadNodeBase2):
    '''
    repeat a pattern along a vectors list 
    each vector of vectors is a start position 
    of a copy of the pattern vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('pattern', 'VectorPin', structure=StructureType.Array)
        a.description="list of vectors which define a figure"
        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        a.description="list of starting points  for the copies of the figure pattern"

        a=self.createOutputPin('pattern_out', 'VectorPin', structure=StructureType.Array)
        a.description="list of pattern lists"
        
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description ="Compound of the copied pattern polygons"


    @staticmethod
    def description():
        return FreeCAD_RepeatPattern.__doc__

    @staticmethod
    def category():
        return 'Combination'




class FreeCAD_Loft(FreeCadNodeBase2):
    '''
    'makeLoft(list of wires,[solid=False,ruled=False,closed=False,maxDegree=5]) -- Create a loft shape.'
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('shapes', 'ShapeListPin')
        a=self.createInputPin('solid', 'Boolean')
        a=self.createInputPin('ruled', 'Boolean')
        a=self.createInputPin('closed', 'Boolean')
        a=self.createInputPin('maxDegree', 'Integer',3)
        a.annotationDescriptionDict={ "ValueRange":(1,10)}
        a.setInputWidgetVariant("Simple2")

        
        self.createOutputPin('Shape_out', 'ShapePin')


    @staticmethod
    def description():
        return FreeCAD_Loft.__doc__

    @staticmethod
    def category():
        return 'Combination'

#+# probleme mit der methode in part
class FreeCAD_Sweep(FreeCadNodeBase2):
    '''
    'makeSweepSurface(edge(path),edge(profile),[float]) -- Create a profile along a path.'
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('path', 'ShapePin')
        a=self.createInputPin('profile', 'ShapePin')
        a=self.createInputPin('profiles', 'ShapeListPin')
        #a=self.createInputPin('f', 'Float')
        self.createOutputPin('Shape_out', 'ShapePin')


    @staticmethod
    def description():
        return FreeCAD_Sweep.__doc__

    @staticmethod
    def category():
        return 'Combination'



class FreeCAD_Slice(FreeCadNodeBase2):
    '''
    
>>> wires=list()
>>> shape=FreeCAD.ActiveDocument.Box.Shape
>>> 
>>> for i in shape.slice(Base.Vector(0,0,1),5):
>>>     wires.append(i)
>>> 
>>> comp=Part.Compound(wires)

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('shape', 'ShapePin')
        a=self.createInputPin('direction', 'VectorPin')
        a=self.createInputPin('distance', 'Float')
        
        self.createOutputPin('Shape_out', 'ShapePin')


    @staticmethod
    def description():
        return FreeCAD_Slice.__doc__

    @staticmethod
    def category():
        return 'Combination'


class FreeCAD_Seam(FreeCadNodeBase2):
    '''
    create a seam bspline face between two bspline surfaces with tangent constraint
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('shapeA', 'ShapePin')
        a.description="first bspline face"
        a=self.createInputPin('shapeB', 'ShapePin')
        a.description="2nd bspline face"
        
        a=self.createInputPin('flipUA', 'Boolean')
        a.description="invert u direction of 1st face"
        a=self.createInputPin('flipVA', 'Boolean')
        a.description="invert v direction of 2nd face"
        a=self.createInputPin('swapA', 'Boolean')
        a.description="swap u and v axes of 1st face"
        
        a=self.createInputPin('flipUB', 'Boolean')
        a.description="invert u direction of 2nd face"
        a=self.createInputPin('flipVB', 'Boolean')
        a.description="invert v direction of 2nd face"
        a=self.createInputPin('swapB', 'Boolean')
        a.description="swap u and v axes of 2nd face"
        
        a=self.createInputPin('seamonly', 'Boolean',True)
        a.description="if false the result is one bspline surface containing 1st 2nd face and the seam"

        a=self.createInputPin('tangentA', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description="force for the tangent from 1st face"
        
        a=self.createInputPin('tangentB', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description="force for the tangent from 2nd face"

        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_Seam.__doc__

    @staticmethod
    def category():
        return 'Combination'

__all__= [
		FreeCAD_Boolean,
		FreeCAD_Compound,
		FreeCAD_Loft,
		FreeCAD_RepeatPattern,
		FreeCAD_Seam,
		
		FreeCAD_Slice,
		FreeCAD_Sweep,
		
	]

def nodelist():
	return __all__



