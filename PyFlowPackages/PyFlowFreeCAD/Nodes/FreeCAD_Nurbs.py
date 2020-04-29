'''
BSline Curves and Surfaces

'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2


#------------------------------------


class FreeCAD_Tripod(FreeCadNodeBase2):
    '''
    position on a surface or curve
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'String','view3d')
        a=self.createInputPin('u', 'Float',0)
        a=self.createInputPin('v', 'Float',0)
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position', 'VectorPin')
        self.createOutputPin('poles', 'VectorPin',structure=StructureType.Array)
        self.createOutputPin('polesIndex','IntPin',structure=StructureType.Array)
        self.createOutputPin('placement', 'PlacementPin' )
        self.createInputPin("display", 'Boolean', True)
        self.createInputPin("directionNormale", 'Boolean', False)
        self.createInputPin("curvatureMode", 'Boolean', True)
        


    @staticmethod
    def description():
        return FreeCAD_Tripod.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Surface','position','Point','uv']









class FreeCAD_UIso(FreeCadNodeBase2):
    '''
    uIso curve on a surface
    '''

    dok= 2
    def __init__(self, name="MyUIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin').\
        description="Face reference"
        a=self.createInputPin('u', 'Float',5)
        self.createOutputPin('Shape_out', 'EdgePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_UIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


import traceback
import inspect

class FreeCAD_VIso(FreeCadNodeBase2):
    '''
    vIso curve on a surface
    '''

    dok = 2
    def __init__(self, name="MyVIso"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('v', 'Float',5)
        self.createOutputPin('Shape_out', 'EdgePin').description="Shape for the curve"


    @staticmethod
    def description():
        return FreeCAD_VIso.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_UVGrid(FreeCadNodeBase2):
    '''
    uIso and vIso curves grid
    '''

    def __init__(self, name="myUvGrid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.createInputPin('Face_in', 'ShapePin')
        a=self.createInputPin('uCount', 'Integer',5)
        a=self.createInputPin('vCount', 'Integer',5)

        self.createOutputPin('uEdges', 'ShapeListPin').description="list of uIso curve edges"
        self.createOutputPin('vEdges', 'ShapeListPin').description="list of vIso curve edges"
        self.createOutputPin('Shape_out', 'ShapePin').description="all curves as compound"

    @staticmethod
    def description():
        return FreeCAD_UVGrid.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []   
        





class FreeCAD_Discretize(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyDiscretizeFusion"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
#        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'Integer', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        
        
        a=self.createInputPin('deflection',"Integer")
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        a.setInputWidgetVariant("Simple2")


        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Discretize.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Offset(FreeCadNodeBase2):
    '''
    create a curve around a wire on a face with some offset
    '''

    def __init__(self, name="MyOffset"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('produce', 'ExecPin', None, self.produce)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("count", 'Integer', True)
        a=self.createInputPin("Wire", 'ShapePin', True)
        a=self.createInputPin("Shape", 'ShapePin', True)
        a=self.createInputPin("offset", 'Float', True)
        a=self.createInputPin("height", 'Float', True)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Offset.__doc__

    @staticmethod
    def category():
        return 'Curves'

    @staticmethod
    def keywords():
        return []

#   def produce(self,**kvargs):
#       self.compute(produce=True)

    def produce(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Offset(self,produce=True)






class FreeCAD_FillEdge(FreeCadNodeBase2):
    '''
    closed wire to face Part.makeFilledFace
    '''

    def __init__(self, name="MyFillEdge"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("Edges", 'ShapePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)

        a=self.createInputPin("Wire", 'ShapePin', True)
        a.description="closed wire to be filled"

        self.createOutputPin('Shape_out', 'ShapePin').description="filled face"


    @staticmethod
    def description():
        return FreeCAD_FillEdge.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []




class FreeCAD_Solid(FreeCadNodeBase2):
    '''
    make solid of faces
    '''

    def __init__(self, name="MySolid"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('bake', 'ExecPin', None, self.bake)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin("Shapes", 'ShapePin',structure=StructureType.Array)
        a=self.createInputPin("Faces", 'FacePin',structure=StructureType.Array)
        a.enableOptions(PinOptions.AllowMultipleConnections)
        a.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createOutputPin('Shape_out', 'ShapePin')
        self.createOutputPin('Compound_out', 'ShapePin') # Faces compound without tolerance


    @staticmethod
    def description():
        return FreeCAD_Solid.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSpline(FreeCadNodeBase2):
    '''
    provides the parameters of a bspline edge object
    '''

    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout.description="Shape which has exactly one edge, this edge is explored"

        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="list of the poles vectors"
        self.createOutputPin('knots', 'FloatPin',structure=StructureType.Array).\
        description="list of the knots"
        self.createOutputPin('mults', 'IntPin',structure=StructureType.Array).\
        description="list of the multiplicities"
        self.createOutputPin('degree', 'IntPin').\
        description="degree of the curve"
        
        self.createOutputPin('periodic', 'BoolPin').\
        description="flag, whether the curve is periodic/closed or open"
        


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Destruct_BSplineSurface(FreeCadNodeBase2):
    '''
    provides the parameters of a bspline surface object
    '''

    dok=2 
    def __init__(self, name="MyDestruct"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout.description="Shape which has exactly one face, this edge is explored"


        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="array of the poles vectors"
        self.createOutputPin('uknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_Destruct_BSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return []





class XFreeCAD_ApproximateBSpline(FreeCadNodeBase2):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',300.)
        self.tolerance.annotationDescriptionDict={ "ValueRange":(0.,1000.)}
        # self.tolerance.setInputWidgetVariant("Simple2")

        
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_ApproximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_InterpolateBSpline(FreeCadNodeBase2):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True

        self.createOutputPin('poles', 'VectorPin', structure=StructureType.Array).\
        description="array of the poles vectors"
        self.createOutputPin('uknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the uknots"
        self.createOutputPin('umults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('udegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('uperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"
        
        self.createOutputPin('vknots', 'FloatPin',structure=StructureType.Array).\
        description="list of the vknots"
        self.createOutputPin('vmults', 'IntPin',structure=StructureType.Array).\
        description="list of the umultiplicities"
        self.createOutputPin('vdegree', 'IntPin').\
        description="udegree of the surface"
        
        self.createOutputPin('vperiodic', 'BoolPin').\
        description="flag, whether the face is periodic/closed or open in u direction"


    @staticmethod
    def description():
        return FreeCAD_InterpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']


class FreeCAD_Collect_Vectors(FreeCadNodeBase2):
    '''
    collect vectors to a list
    '''

    dok=2 

    def __init__(self, name="MyCollection"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inReset = self.createInputPin("reset", 'ExecPin', None, self.reset)
        self.inReset.description="clear the list of collected points"
        self.inRefresh = self.createInputPin("refresh", 'ExecPin', None, self.refresh)
        self.inRefresh.description="update the outpin **points**"
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('point', 'VectorPin').\
        description="list of collected vectors"
        self.createInputPin("maxSize",'Integer',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'Integer',0).\
        description="create only a discretized list of the polygon with this size"

        a=self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        a.description="list of collected vectors"
        
        self.points=[]

    @staticmethod
    def description():
        return FreeCAD_Collect_Vectors.__doc__

    @staticmethod
    def category():
        return 'Points'

    @staticmethod
    def keywords():
        return ['point','collect']

    def reset(self,*args, **kwargs):
        say("reset")
        self.compute(mode="reset")

    @timer
    def reset(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="reset")


    def refresh(self,*args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="refresh")
        self.outExec.call()

class FreeCAD_ApproximateBSpline(FreeCadNodeBase2):
    '''
    create an approximated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyApproximation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.annotationDescriptionDict={ "ValueRange":(0.,1000.)}
        # self.tolerance.setInputWidgetVariant("Simple2")

        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_ApproximateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Approximate','Curve','Nurbs','Projection']


class FreeCAD_InterpolateBSpline(FreeCadNodeBase2):
    '''
    create an interpolated BSpline for **points** on face **Shape_in**
    '''

    dok=2 

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
      
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('points', 'VectorPin', structure=StructureType.Array)
        self.tolerance=self.createInputPin("tolerance",'Float',100.)
        self.tolerance.description="relative value for to,.erance"
        self.createInputPin("Shape_in",'ShapePin')
        #+# todo: more parameters for approximate
        self.createOutputPin('Shape_out', 'ShapePin')
        self.tolerance.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_InterpolateBSpline.__doc__

    @staticmethod
    def category():
        return 'BSpline'

    @staticmethod
    def keywords():
        return ['Interpolate','Curve','Nurbs','Projection']



class FreeCAD_ConnectPoles(FreeCadNodeBase2):
    '''
    concatenate vectorarrays with the same 2nd axis together along the first axis
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.polesin=self.createInputPin("poles_in",'VectorPin', structure=StructureType.Array)
        self.polesin.enableOptions(PinOptions.AllowMultipleConnections)
        self.polesin.description="connection for multiple 2 dimensional vectorarrays which should be concatenated, they must have the same number of rows"


        a=self.createOutputPin('poles_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 dim array of vectors as base for a grid or bspline surface"
        
        self.createOutputPin('umults_out', 'FloatPin',structure=StructureType.Array).\
        description="list of the multiplicities in the first axis depends on overlay"

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description="a BSplineSurface degree 3 to visualize the poles array"

        a=self.createInputPin('tangentA', 'Float',0)
        a.description="force of the tangents of the first array" 
        
        a=self.createInputPin('tangentB', 'Float',0)
        a.description="force of the tangents of the 2nd array" 

        a=self.createInputPin('overlay', 'Integer',0)
        a.description="0 = concatenate, 1 = calculate mean of the last and first row of two arrays, 2 = add tangent support between the faces"
        #a.setInputWidgetVariant("SimpleSlider")

    @staticmethod
    def description():
        return FreeCAD_ConnectPoles.__doc__

    @staticmethod
    def category():
        return 'VectorArray dim 2'

    @staticmethod
    def keywords():
        return ['matrix','vector','concatenate']



#+#
class FreeCAD_replacePoles(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyInterpolation"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.createInputPin('Shape', 'ShapePin')
        self.createInputPin('poles', 'VectorPin',structure=StructureType.Array)
        self.createInputPin('polesIndex','IntPin',structure=StructureType.Array)
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def category():
        return 'BSpline'



#10-14.01.2020

class FreeCAD_Editor(FreeCadNodeBase2):
    '''
    A node to edit a bspine surface
    '''

    videos='https://youtu.be/5vhxx2Mt9QI https://youtu.be/wYJRXN-O618'
    
    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.inExec = self.createInputPin("commit", 'ExecPin', None, self.commit)
        self.inExec = self.createInputPin("bake", 'ExecPin', None, self.bake)
        self.inExec = self.createInputPin("rollback", 'ExecPin', None, self.rollback)
        
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        
        
        self.createInputPin("useStart", 'Boolean', False)

        a=self.createInputPin('startU',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('startV',"Integer")
        a.setInputWidgetVariant("Slider")
        
        self.createInputPin("displayStart", 'Boolean', False)
        self.createInputPin("useStartPosition", 'Boolean', False)
        a=self.createInputPin("startPosition",'VectorPin')
        
        self.createInputPin("displayTarget", 'Boolean', False)
        a=self.createInputPin("targetPosition",'VectorPin')


        #feineinstellung
        a=self.createInputPin('u',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('v',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('t',"Integer")
        a.setInputWidgetVariant("Slider")
        
        #a=self.createInputPin('ku',"Integer")
        #a.setInputWidgetVariant("Slider")
        #a=self.createInputPin('kv',"Integer")
        #a.setInputWidgetVariant("Slider")
        
        
        self.createInputPin("bordersFrozen", 'Boolean', False)
        self.createInputPin("tangentsFrozen", 'Boolean', False)
        
        self.createInputPin("displayIso", 'Boolean', False)
        
        #self.createInputPin("useXYZT", 'Boolean', False)
        
        a=self.createInputPin('offsetUA', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetUB', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetVA', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        a=self.createInputPin('offsetVB', 'Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('scaleU',"Integer")
        a.setInputWidgetVariant("Slider")
        a=self.createInputPin('scaleV',"Integer")
        a.setInputWidgetVariant("Slider")
        
        

        
        

        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('position_out', 'VectorPin')
        #self.createInputPin("directionNormale", 'Boolean', False)
        self.createOutputPin('u_out', 'FloatPin')
        self.createOutputPin('v_out', 'FloatPin')
        self.createOutputPin('Shape_out', 'ShapePin')

       

        
    def commit(self,*arg,**kwarg):
        self.shape=self.getPinObject("Shape_out")
        
    def rollback(self,*arg,**kwarg):
        try:
            del(self.shape)
        except:
            pass

    @staticmethod
    def description():
        return FreeCAD_Editor.__doc__

    @staticmethod
    def category():
        return 'BSpline'


# 15.01.2020
class FreeCAD_IronCurve(FreeCadNodeBase2):
    '''
    find a curve which is smoother than the starting curve with a lot of parameters to play
    '''

    videos='https://youtu.be/FlHtj-xWKDg'
    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('loopsA',"Integer")
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(1,10)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('loopsB',"Integer")
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(0,20)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('k',"Integer",0)
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('deflection',"Integer")
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        a.setInputWidgetVariant("Simple2")

        self.mode = self.createInputPin('mode', 'String','constant')
        self.mode.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["constant","distance"]
            }
            

        a=self.createInputPin('weight',"Integer",2)
        a.setInputWidgetVariant("Slider")
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_IronCurve.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_IronSurface(FreeCadNodeBase2):
    '''
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('loopsA',"Integer")
        a.annotationDescriptionDict={ "ValueRange":(1,10)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('loopsB',"Integer")
        a.annotationDescriptionDict={ "ValueRange":(0,20)}
        a.setInputWidgetVariant("Simple2")

        
        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('weight',"Integer",2)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        
        

        
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        self.createOutputPin('Shape_out', 'ShapePin')
        
        self.setExperimental()


    @staticmethod
    def description():
        return FreeCAD_IronCurve.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_ReduceCurve(FreeCadNodeBase2):
    '''
    interactive reduce poles from a curve to get it smoother 
    '''

    videos="https://youtu.be/iEHDOwz9S3Q https://youtu.be/vuQ4s3iYqOA"

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a = self.createInputPin("commit", 'ExecPin', None, self.commit)
        a.description='accept changes into working copy'
        a = self.createInputPin("bake", 'ExecPin', None, self.bake)
        a.description='store working copy as nonparametric Shape'
        a = self.createInputPin("rollback", 'ExecPin', None, self.rollback)
        a.description="cancel all changes and go back to the inputpin Shape curve"
        
        
        a=self.createInputPin('Move1', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description='interactive move the calculated new pole first direction'
        
        a=self.createInputPin('Move2', 'Integer',0)
        a.setInputWidgetVariant("Slider")
        a.description='interactive move the calculated new pole 2nd direction'

        a=self.createInputPin("hide",'Boolean')
        a.description="do not display the controls in 3D after works is finished"
        
        a=self.createInputPin("position",'VectorPin')
        a.description='a position to use as new pole instead of the calculated pole'
        
        a=self.createInputPin("useStartPosition",'Boolean')
        a.description='use the pin position as new pole base' 
        
        a=self.createInputPin("usePositionAsAbsolute",'Boolean')
        a.description='use the pin position as absolute else it is added to the center of mass' 
        

        a=self.createInputPin('start',"Integer")
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="knot number where modification starts"

        a=self.createInputPin('segments',"Integer",-1)
        a.annotationDescriptionDict={ "ValueRange":(-1,100)}
        a.setInputWidgetVariant("Simple2")
        a.description="number of segments which are smoothed"

        '''
        a=self.createInputPin('k',"Integer",0)
        a.annotationDescriptionDict={ "ValueRange":(-5,20)}
        a.setInputWidgetVariant("Simple2")

        a=self.createInputPin('weight',"Integer",2)
        a.annotationDescriptionDict={ "ValueRange":(0,10)}
        a.setInputWidgetVariant("Simple2")
        
        '''
        a=self.createInputPin("Strategy",'StringPin','Center of Mass')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["Center of Mass","Shortest","Point"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("Center of Mass")
        a.description='''how the curve should be simplified: 
  -''Center of Mass'' starts at the center fo the old poles
  -''Shortest'' calculates the shortest segement to fill the gap
  -''Point''  makes the curve fitting a point'''

        a=self.createInputPin("Method",'StringPin','BFGS')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP',]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("BFGS")
        a.description='''the scipy methods for optimize.
        
If the computation time is to long or not good results are calcuated a change of the method may help. 

see https://docs.scipy.org/doc/scipy/reference/optimize.html'''
        
        a=self.createInputPin('Shape', 'ShapePin')
        a.description='a bspline curve edge' 
        
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description='the list of knotes before and after change'

        a=self.createOutputPin('Shape_out', 'ShapePin')
        a.description='the reduced bspline curve' 
        
        a=self.createInputPin("preservePolesCount",'Boolean')
        
        self.setExperimental()

        
    def commit(self,*arg,**kwarg):

        self.shape=self.getPinObject("Shape_out")
        a=self.getData('start')
        b=self.getData('segments')
        ax=self._wrapper.UIinputs
        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='segments':
                p.setData(0)
            if p.name=='Move1':
                p.setData(0)

            if p.name=='Move2':
                p.setData(0)

        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='start':
                p.setData(a+4)
        self.compute()
        self.outExec.call()


        
    def rollback(self,*arg,**kwarg):
        try:
            del(self.shape)
        except:
            pass

    @staticmethod
    def description():
        return FreeCAD_ReduceCurve.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_BSplineSegment(FreeCadNodeBase2):
    '''
    segment of the BSpline 
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('uStart',"Float")
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        a=self.createInputPin('vStart',"Float",)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}

        a=self.createInputPin('uEnd',"Float",100)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}

        a=self.createInputPin('vEnd',"Float",100)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('Shape_out', 'ShapePin')
        
        self.setExperimental()


    @staticmethod
    def description():
        return FreeCAD_BSplineSegment.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_BSplineOffset(FreeCadNodeBase2):
    '''
    a poor man offset approx: create a grid of points moved in normal direction
    '''

    def __init__(self, name="MyTripod",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)  
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('height',"Float")
        a.annotationDescriptionDict={ "ValueRange":(-100,100)}
        
        self.createInputPin('Shape', 'ShapePin')
        self.createOutputPin('Shape_out', 'ShapePin')
        a=self.createOutputPin('Points_out', 'VectorPin', structure=StructureType.Array)
        
        a=self.createInputPin('sizeU',"Integer",10)
        a.annotationDescriptionDict={ "ValueRange":(10,100)}

        a=self.createInputPin('sizeV',"Integer",10)
        a.annotationDescriptionDict={ "ValueRange":(10,100)}

        
        
        self.setExperimental()

    @staticmethod
    def description():
        return FreeCAD_BSplineOffset.__doc__

    @staticmethod
    def category():
        return 'BSpline'

class FreeCAD_Nurbs(FreeCadNodeBase2):
    '''
    converts faces to nurbs
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('shape', 'ShapePin')
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_Nurbs.__doc__

    @staticmethod
    def category():
        return 'Nurbs'

class FreeCAD_CloseFace(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('Shape_in', 'ShapePin')
        a=self.createInputPin('swap', 'Boolean')
        a=self.createInputPin('tangentForce', 'Integer',50)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}

        
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_CloseFace.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_CurveOffset(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
   
        a=self.createInputPin('Shape_in', 'ShapePin')
        a=self.createInputPin('flip', 'Boolean')
        a=self.createInputPin('asPolygon', 'Boolean')
        a=self.createInputPin('loops', 'Integer',10)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}

        a=self.createInputPin('deflection', 'Integer',10)
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        
        a=self.createInputPin('mindd', 'Integer',10)
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        
        a=self.createInputPin('distA', 'Integer',10)
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        # Wegnehmen zu naher Punkte - Buchten entfernen
        
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_CloseFace.__doc__

    @staticmethod
    def category():
        return 'BSpline'


class FreeCAD_Helmet3(FreeCadNodeBase2):
    '''
    3rd version of a helmet: tangent border
    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
   
        a=self.createInputPin('border', 'VectorPin', structure=StructureType.Array)
        a=self.createInputPin('dome', 'VectorPin', structure=StructureType.Array)
   
   
        a=self.createInputPin('flip', 'Boolean')
        a=self.createInputPin('heightBorder', 'Float',1.0)
        a.annotationDescriptionDict={ "ValueRange":(0.01,100)}

        
        self.createOutputPin('Shape_out', 'ShapePin')

    @staticmethod
    def description():
        return FreeCAD_Helmet3.__doc__

    @staticmethod
    def category():
        return 'BSpline'





def nodelist():
    return [
                FreeCAD_ApproximateBSpline,
                FreeCAD_Tripod,

                FreeCAD_UIso, 
                FreeCAD_VIso,
                FreeCAD_UVGrid,

                
                FreeCAD_Discretize,
                FreeCAD_Offset,
                FreeCAD_FillEdge,
                FreeCAD_Solid,
                
                FreeCAD_Destruct_BSpline,
                FreeCAD_Destruct_BSplineSurface,
                
                FreeCAD_InterpolateBSpline,

                FreeCAD_ConnectPoles,
                
                FreeCAD_replacePoles,
                FreeCAD_Editor,

                FreeCAD_IronCurve,
                FreeCAD_IronSurface,
                FreeCAD_ReduceCurve,
                FreeCAD_BSplineSegment,
                FreeCAD_BSplineOffset,
                FreeCAD_Nurbs,
                
                FreeCAD_CloseFace,
                FreeCAD_CurveOffset,
                #FreeCAD_Placement3
                FreeCAD_Helmet3,
        ]
