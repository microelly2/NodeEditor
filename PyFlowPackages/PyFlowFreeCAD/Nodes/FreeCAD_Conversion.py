'''
convert data to other types
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import FreeCadNodeBase2


class FreeCAD_Transformation(FreeCadNodeBase2):
    '''
    affine transformation matrix
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('vectorX', 'VectorPin',FreeCAD.Vector(1,0,0))
        a.recomputeNode=True
        a.description="the result of the first base vector X=(1,0,0)"

        a=self.createInputPin('vectorY', 'VectorPin',FreeCAD.Vector(0,1,0))
        a.recomputeNode=True
        a.description="the result of the 2nd base vector Y=(0,1,0)"

        a=self.createInputPin('vectorZ', 'VectorPin',FreeCAD.Vector(0,0,1))
        a.recomputeNode=True
        a.description="the result of the 3rd base vector X=(0,0,1)"

        a=self.createInputPin('vector0', 'VectorPin',FreeCAD.Vector(0,0,0))
        a.recomputeNode=True
        a.description="movement vector after generic affine transformation"
        
        a=self.createOutputPin('transformation', 'TransformationPin' )
        a.description="a transformation matrix"

    @staticmethod
    def description():
        return FreeCAD_Transformation.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_IndexToList(FreeCadNodeBase2):
    '''
    create a flag list with 1 for the numbers 
    and 0 for the others
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('index', 'Integer')
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)
        a.description="numbers where the flag should be 1 (the others are 0)"

        a=self.createOutputPin('flags', 'BoolPin',structure=StructureType.Array)
        a.description="list of 0's and 1's"

    @staticmethod
    def description():
        return FreeCAD_IndexToList.__doc__

    @staticmethod
    def category():
        return 'Conversion'

class FreeCAD_ListOfShapes(FreeCadNodeBase2):
    '''
    create a ordered list of shapes from single shapes
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createOutputPin('ShapeList', 'ShapeListPin')
        a.description="the ordered list of the input shapes"

        self.pas=self.createInputPin('Shape', 'ShapePin')
        self.pas.description="the shapes are ordered by thy y coordinate of the nodes"
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)


    @staticmethod
    def description():
        return FreeCAD_ListOfShapes.__doc__

    @staticmethod
    def category():
        return 'Conversion'




class FreeCAD_ListOfPlacements(FreeCadNodeBase2):
    '''
    create a orderd list of placements from  lists of data
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('moves', 'VectorPin',structure=StructureType.Array)
        a.description="moving vectors/base vector property of the placements, default is (0,0,0) "
        
        a=self.createInputPin('axes', 'VectorPin',structure=StructureType.Array)
        a.description="rotation axes, default is (0,0,1)"
        
        a=self.createInputPin('angles', 'Float',structure=StructureType.Array)
        a.description="rotation angles in degree, default is 0"
        
        a=self.createInputPin('centers', 'VectorPin',structure=StructureType.Array)
        a.description="rotation centers, default is (0,0,0)"

        a=self.createOutputPin('Placements', 'PlacementPin',structure=StructureType.Array)
        a.description="list of placements created from given lists, the length is defined by the longest input list, the values for the other list are filled with default values"

    @staticmethod
    def description():
        return FreeCAD_ListOfPlacements.__doc__


    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_Zip(FreeCadNodeBase2):
    '''
    create a list of vectors from the lists of coordinates
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('x', 'Float',structure=StructureType.Array)
        a.description='list of x coordinates'

        a=self.createInputPin('y', 'Float',structure=StructureType.Array)
        a.description='list of y coordinates'

        a=self.createInputPin('z', 'Float',structure=StructureType.Array)
        a.description='list of z coordinates'

        a=self.createOutputPin('vectors_out', 'VectorPin',structure=StructureType.Array)
        a.description='list of created vectors'

    @staticmethod
    def description():
        return FreeCAD_Zip.__doc__


    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_uv2xyz(FreeCadNodeBase2):
    '''
    calculate the wolrd xyz coordinates for a list of uv coordinates in relation to a surface
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("points",'VectorPin', structure=StructureType.Array)
        a.description='list of vectors with uv coodinates - used are vectors with x=u, y=v'

        a=self.createInputPin("Shape",'ShapePin')
        a.description='the reference bspline surface'
      
        a=self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)
        a.description='the list of 3D vectors'

    @staticmethod
    def description():
        return FreeCAD_uv2xyz.__doc__

    @staticmethod
    def category():
        return 'Conversion'



class FreeCAD_xyz2uv(FreeCadNodeBase2):
    '''
    calculate the uv coordinates for a set of xyz points on a bsline surface
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("points",'VectorPin', structure=StructureType.Array)
        a.description="a list of vectors"

        a=self.createInputPin("Shape",'ShapePin')
        a.description='a bspline surface'
      
        a=self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)
        a.description="the list of uv Vectors (3D Vectors are used but z is set to zero)"

    @staticmethod
    def description():
        return FreeCAD_xyz2uv.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_FlipSwapArray(FreeCadNodeBase2):
    '''
    flip directions of the vector-array or swap its axes
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("poles_in",'VectorPin', structure=StructureType.Array)
        a.description="2 dim vector array" 

        a=self.createOutputPin('poles_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 dim vector array flipped or swapped poles_in" 
        
        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description="a BSplineSurface degree 3 to visualize the poles array"

        a=self.createInputPin('swap', 'Boolean',0)
        a.description="Flag for swap axes of the array"

        a=self.createInputPin('flipu', 'Boolean',0)
        a.description="Flag for invert u direction of the array"

        a=self.createInputPin('flipv', 'Boolean',0)
        a.description="Flag for invert v direction of the array"


    @staticmethod
    def description():
        return FreeCAD_FlipSwapArray.__doc__

    @staticmethod
    def category():
        return 'Conversion'

    @staticmethod
    def keywords():
        return ['flip','swap','Vector']



class FreeCAD_ListOfVectors(FreeCadNodeBase2):
    '''
    create a ordered list of vectors from  single vectors
    the order of the vector is defined by
    the y coordinate of the vector nodes
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createOutputPin('vectors', 'VectorPin', structure=StructureType.Array)
        a.description='ordered vector list'

        self.pas=self.createInputPin('pattern', 'VectorPin')
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)
        self.pas.description='here multiple vectors can be connected to get them ordered'

    @staticmethod
    def description():
        return FreeCAD_ListOfVectorlist.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_ListOfVectorlist(FreeCadNodeBase2):
    '''
    create a list of vector lists,
    this can be a 2 dimensional array of vectors
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createOutputPin('vectorarray', 'VectorPin', structure=StructureType.Array)
        a.description="the list of list of vectors"
        

        self.pas=self.createInputPin('vectorlists', 'VectorPin', structure=StructureType.Array)
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)
        self.pas.description='here multiple lists vectors can be connected to get them ordered'


    @staticmethod
    def description():
        return FreeCAD_ListOfVectorlist.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_MoveVectors(FreeCadNodeBase2):
    '''
    move a list of vectors
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        a.description="list of vectors to move"
        
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)

        a=self.createInputPin('mover', 'VectorPin')
        a.description="__mover__ is added to all __vectors__"

        a.recomputeNode=True
        a.description ="mover vector"

    @staticmethod
    def description():
        return FreeCAD_MoveVectors.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_ScaleVectors(FreeCadNodeBase2):
    '''
    scale list of vectors
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        a.description="list of vectors to scale"
        
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)

        a=self.createInputPin('scaler', 'VectorPin',FreeCAD.Vector(1,1,1))    
        a.recomputeNode=True
        a.description ="factors to scale the three  ain axes"


    @staticmethod
    def description():
        return FreeCAD_ScaleVectors.__doc__

    @staticmethod
    def category():
        return 'Conversion'



__all__= [
        FreeCAD_FlipSwapArray,
        FreeCAD_IndexToList,
        FreeCAD_ListOfPlacements,
        FreeCAD_ListOfShapes,
        FreeCAD_Transformation,
        FreeCAD_Zip,
        
        FreeCAD_xyz2uv,
        FreeCAD_uv2xyz,
        
        FreeCAD_ListOfVectors,
        FreeCAD_ListOfVectorlist,
        FreeCAD_MoveVectors,
        FreeCAD_ScaleVectors,

        
    ]

def nodelist():
    return __all__
