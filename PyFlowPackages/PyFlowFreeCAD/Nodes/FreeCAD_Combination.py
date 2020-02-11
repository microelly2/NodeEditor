'''
nodes which combine one or more shapes to a new shape or new shapes
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

    def __init__(self, name="MyCompound"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description="the Part.Compound of all shapes connected tp the Shapes pin"


        self.shapes=self.createInputPin('Shapes', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)
        self.shapes.description="these pin can be connected to multiple shapes"


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
        a.description="a list of shapes which define the ribs of the loft"
        a=self.createInputPin('solid', 'Boolean')
        a.description="make a solid - that means that a front and back face is added"
        a=self.createInputPin('ruled', 'Boolean')
        a.description="make the faces between the ribs ruled that is of degree 1 or linear"
        a=self.createInputPin('closed', 'Boolean')
        a.description="close from the last rib to the first to get a ring like object"
        a=self.createInputPin('maxDegree', 'Integer',3)
        a.description="maximum degree of the meridian curves"
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
        a.description="a wire where the sweep flows along"
        
        a=self.createInputPin('profile', 'ShapePin')
        a.description="use this if only one wire is sweeped along the path"
        
        a=self.createInputPin('profiles', 'ShapeListPin')
        a.description="the sweep flows trough the profile ribs"
        
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
        a.description='the shape to slice'
        
        a=self.createInputPin('direction', 'VectorPin')
        a.description='the normal direction of the cutting plane'
        
        a=self.createInputPin('distance', 'Float')
        a.description="the distance of the cutting plane to the world origin" 
        
        a=self.createOutputPin('Shape_out', 'ShapePin')


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



class FreeCAD_ApplyPlacements(FreeCadNodeBase2):
    '''
    apply a list of placements to 
    a shape or a list of shapes 
    or a list of vectors(polygon)
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="a list of vectors which define a poylgon pattern"

        a=self.createInputPin('Shapes', 'ShapeListPin')   
        a.description="a list of shapes,  the n. shape will get the n. placement"

        a=self.createInputPin('Shape_in', 'ShapePin')   
        a.description="a single shape, there will be a copy of this shape for each placement"
        
        a=self.createInputPin('Placements', 'PlacementPin',structure=StructureType.Array)
        a.description="the list of placement which are applied to the shape, shapelist or points"

        a=self.createOutputPin('Shape_out', 'ShapePin')   

        a=self.createOutputPin('points_out', 'VectorPin',structure=StructureType.Array)
        a.description="the result if the input was the __points__ pin"

    @staticmethod
    def description():
        return FreeCAD_ApplyPlacements.__doc__

    @staticmethod
    def category():
        return 'Combination'


class FreeCAD_Reduce(FreeCadNodeBase2):
    '''
    select a sublist fo a list of shapes on  flag list selection
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('shapes', 'ShapeListPin')
        a.description="list of shapes"

        a=self.createInputPin('selection', 'Boolean',structure=StructureType.Array)
        a.description="list of flags which shapes should be in the resulting list"

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description = "compound of the filtered shapes" 

    @staticmethod
    def description():
        return FreeCAD_Reduce.__doc__

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
		FreeCAD_ApplyPlacements,
		FreeCAD_Reduce
		
	]

def nodelist():
	return __all__



