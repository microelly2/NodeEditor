'''
import numpy as np
import random
import functools
import time
import inspect

from FreeCAD import Vector
import FreeCAD
import FreeCADGui
import Part

from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

import nodeeditor.store as store
from nodeeditor.say import *

'''
from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase






class FreeCAD_Box( FreeCadNodeBase):
    '''
    erzeuge einer Part.Box
    '''

    dok=4
    def __init__(self, name="MyBox"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')



        self.length = self.createInputPin("length", 'FloatPin')
        self.length.description="Lenght of the Box"
        self.length.setInputWidgetVariant("Slider")

        self.length2 = self.createInputPin("length", 'FloatPin')
        self.length2.description="Lenght of the Box"
        self.length2.setInputWidgetVariant("Simple2")

        self.length.annotationDescriptionDict={ "A":23,"ValueRange":(10.,20.)}
        self.length2.annotationDescriptionDict={ "A":23,"Step":2. }

        self.width = self.createInputPin("width", 'FloatPin')
        self.width.description="Width of the Box"
        self.height = self.createInputPin("height", 'FloatPin')
        self.height.description = "Height of the Box"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description = "position of the Box"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the height of the Box" 

#        self.objname.setData(name)

        self.setDatalist("length width height position direction",
            [10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0)])

        self.length.recomputeNode=True
        self.width.recomputeNode=True
        self.height.recomputeNode=True

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

    @timer
    def compute(self, *args, **kwargs):

        shape=self.applyPins(Part.makeBox,"length width height position direction")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Box.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Box','Part']









class FreeCAD_Cone(FreeCadNodeBase):
    '''erzeuge eines Part.Kegel'''
    
    dok=4
    def __init__(self, name="MyCone"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        self.radius1 = self.createInputPin("radius1", 'FloatPin')
        self.radius1.description="Radius of the bottom circle"
        self.radius2 = self.createInputPin("radius2", 'FloatPin')
        self.radius2.description="Radius of the top circle"
        self.height = self.createInputPin("height", 'FloatPin')
        self.height.description="Height of the circle"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description="Position of the center of the bottom circle"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the axis"
        self.angle = self.createInputPin("angle", 'FloatPin')
        self.angle.description="longitude of the sector"

        self.setDatalist("radius1 radius2 height position direction angle",
            [10,20,30,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),360])

        self.radius1.recomputeNode=True
        self.radius2.recomputeNode=True
        self.height.recomputeNode=True

    def compute(self, *args, **kwargs):

        shape=self.applyPins(Part.makeCone,"radius1 radius2 height position direction angle")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()
        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Cone.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Sphere','Part']



class FreeCAD_Sphere(FreeCadNodeBase):
    '''erzeuge einer Part.Kurgel'''

    dok=4
    def __init__(self, name="MySphere"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.radius = self.createInputPin("radius", 'FloatPin')
        self.radius.description="Radius of the sphere"
        self.position = self.createInputPin("position", 'VectorPin')
        self.position.description="position of the Sphere"
        self.direction = self.createInputPin("direction", 'VectorPin')
        self.direction.description="direction of the south north axis"
        self.angle1 = self.createInputPin("angle1", 'FloatPin')
        self.angle1.description="maximum north latitude"
        self.angle2 = self.createInputPin("angle2", 'FloatPin')
        self.angle2.description="maximum south latitude"
        self.angle3 = self.createInputPin("angle3", 'FloatPin')
        self.angle3.description="maximum longitude (start is always 0)"

        self.setDatalist("radius position direction angle1 angle2 angle3",
            [10,FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),-90,90,360])

        self.radius.recomputeNode=True
        self.angle1.recomputeNode=True
        self.angle2.recomputeNode=True
        self.angle3.recomputeNode=True

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

    @timer
    def compute(self, *args, **kwargs):
        shape=self.applyPins(Part.makeSphere,"radius position direction angle1 angle2 angle3")
        self.setPinObject("Shape_out",shape)
        self.outExec.call()
        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Sphere.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Sphere','Part']



class FreeCAD_Quadrangle(FreeCadNodeBase):
    '''
    create a Bspline Surface of degree 1
    by 4 points
    '''

    dok=4
    def __init__(self, name="MyQuadrangle"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.vA = self.createInputPin("vecA", 'VectorPin')
        self.vB = self.createInputPin("vecB", 'VectorPin')
        self.vC = self.createInputPin("vecC", 'VectorPin')
        self.vD = self.createInputPin("vecD", 'VectorPin')

        self.setDatalist("vecA vecB vecC vecD", [
                        FreeCAD.Vector(0,0,0),
                        FreeCAD.Vector(100,0,0),
                        FreeCAD.Vector(100,200,40),
                        FreeCAD.Vector(0,200,40),
                    ])

        self.vA.recomputeNode=True
        self.vB.recomputeNode=True
        self.vC.recomputeNode=True
        self.vD.recomputeNode=True

        self.Called=False


    def compute(self, *args, **kwargs):


        # recursion stopper
        if self.Called:
            return

        self.Called=True
        vA=self.vA.getData()
        vB=self.vB.getData()
        vC=self.vC.getData()
        vD=self.vD.getData()

        w=Part.BSplineSurface()
        w.buildFromPolesMultsKnots([[vA,vB],[vD,vC]],[2,2],[2,2],[0,1],[0,1],False,False,1,1)
        shape=w.toShape()

        self.setPinObject("Shape_out",shape)


        self.Called=False

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Quadrangle.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Surface','Part']



class FreeCAD_Polygon(FreeCadNodeBase):
    '''
    erzeuge eines Streckenzugs
    input pin for a list of vectors
    '''

    dok=4
    
    def __init__(self, name="MyPolygon"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.points = self.createInputPin('points', 'VectorPin',[], structure=StructureType.Array)
        self.points.description="list of points as array"
        self.points.setData([FreeCAD.Vector(0,0,0),FreeCAD.Vector(10,0,0)])


        self.Called=False
        self.count=2


    @staticmethod
    def description():
        return FreeCAD_Polygon.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['Pointlist','Polygon','Part']



class FreeCAD_Boolean(FreeCadNodeBase):
    '''boolean ops of two parts example'''

    def __init__(self, name="Fusion"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

#        self.objname = self.createInputPin("objectname", 'StringPin')
#        self.objname.setData(name)

#        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
#        self.shapeOnly.recomputeNode=True

        self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
        self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

        self.shape1 = self.createInputPin('Shape_in1', 'ShapePin')
        self.shape2 = self.createInputPin('Shape_in2', 'ShapePin')

        self.mode = self.createInputPin('mode', 'EnumerationPin')
        self.mode.values=["fuse","cut","common","fragments"]
        self.mode.setData("fuse")
        self.mode.recomputeNode=True

        self.volume = self.createOutputPin('Volume', 'FloatPin')


    @timer
    def compute(self, *args, **kwargs):

#       say ("in compute",self.getName(),"objname is",self.objname.getData())

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





class FreeCAD_BSplineSurface(FreeCadNodeBase):
    '''
    BSpline Surface 
    create a default bspline surface from poles and degrees
    '''

    dok=4
    @staticmethod

    def description():
        return ''''''

    def __init__(self, name="MyBSplineSurface"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="Array of poles vectors"
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('maxDegreeU', 'IntPin', 3)
        a.description="maximum degree for u"
        
        a=self.createInputPin('maxDegreeV', 'IntPin', 3)
        a.description="maximum degree for v"
        
        a=self.createInputPin('periodicU', 'BoolPin',)
        a.description="is surface periodic in u direction"
        
        a=self.createInputPin('periodicV', 'BoolPin',)
        a.description="is surface periodic in v direction"

        self.shapeout = self.createOutputPin('Shape_out', 'FacePin')
        self.shapeout.description='BSpline Face'

    @staticmethod
    def description():
        return FreeCAD_BSplineSurface.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Surface','Part']


class FreeCAD_BSplineCurve(FreeCadNodeBase):
    '''
    BSpline Curve
    create a default bspline surface from poles and degrees
    '''

    dok=4

    def __init__(self, name="MyBSplineCurve"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'EdgePin')
        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        a=self.createInputPin('maxDegree', 'IntPin', 3)
        a.description="degree of the curve (default is 3)"
        a=self.createInputPin('periodic', 'BoolPin',)
        a.description="is curve periodic"
    



    @staticmethod
    def description():
        return FreeCAD_BSplineCurve.__doc__

    @staticmethod
    def category():
        return 'Primitive'

    @staticmethod
    def keywords():
        return ['BSpline','Curve','Part']



class FreeCAD_VectorArray(FreeCadNodeBase):
    '''
    Array of Vectors 
    and a generated default BSplineSurface
    '''

    dok=4
    def __init__(self, name="MyVectorArray"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        a=self.createInputPin("vecA", 'VectorPin',FreeCAD.Vector(20,0,0))
        a.description="step vector for the first dimension"
        
        a=self.createInputPin("vecB", 'VectorPin',FreeCAD.Vector(0,10,0))
        a.description="step vector for the 2nd dimension"
        
        a=self.createInputPin("vecC", 'VectorPin')
        a.description="step vector for the 3rd dimension"
        
        a=self.createInputPin("vecBase", 'VectorPin')
        a.description="starting point of the array"
        
        a=self.createInputPin("countA", 'IntPin',5)
        a.description="number of elements in the first direction"
        
        a=self.createInputPin("countB", 'IntPin',8)
        a.description="number of elements in the 2nd direction"
        
        a=self.createInputPin("countC", 'IntPin',1)
        a.description="if c>1 a 3 dimensional arry of vector is created"
        
        a=self.createInputPin("randomX", 'FloatPin',5)
        a.description="adds some randomness onto the x coordinates of the points"
        
        a=self.createInputPin("randomY", 'FloatPin',5)
        a.description="adds some randomness onto the y coordinates of the points"
        
        a=self.createInputPin("randomZ", 'FloatPin',5)
        a.description="adds some randomness onto the z coordinates of the points"
        

        a=self.createInputPin("degreeA", 'IntPin',3)
        a.description="degree of the generated surface in u direction, degreeA = 0 means wire model"
        
        a=self.createInputPin("degreeB", 'IntPin',3)
        a.description="degree of the generated surface in u direction, degreeB = 0 means wire model"
        
        a=self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)
        a.description="2 or 3 dimensional array of vectors"
        


    @staticmethod
    def description():
        return FreeCAD_VectorArray.__doc__

    @staticmethod
    def category():
        return 'Generator'

    @staticmethod
    def keywords():
        return ['BSpline','Array','Surface','Grid','Part']





class FreeCAD_Object(FreeCadNodeBase):
    '''
    load and save objects in FreeCAD document
    '''

    dok=4
    def __init__(self, name="MyObject"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData("Box")


        self.createInputPin('Reload_from_FC', 'ExecPin', None, self.reload)
        self.createInputPin('Store_to_FC', 'ExecPin', None, self.store,)




    def reload(self, *args, **kwargs):
        print ("reload from FreeCADobject and refresh data")
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.reload_obj(self)
        sayl()



    def store(self, *args, **kwargs):

        print ("store  data to  FreeCAD object and to the output pins" )

        data={}
        pps=self.getOrderedPins()
        for p in pps:
            dat=p.getData()
            print ("#+#+#",p.getName(),dat)
            data[str(p.name)+"_out"]=dat

        say("data")
        say(data)
        say("pps")
        say(pps)

        for p in pps:
            if p.group=='FOP':
                n=p.getName()
                if n.endswith('_out'):
                    p.setData(data[str(n)])
                    pn=n[:-4]
                    vn=data[str(n)]
                    say("set",n,pn,vn)
                    setattr(self.fob,pn,vn)
                    continue

                try:
                    pn=n.split('_')[1]
                    if pn=="Object": # hack for names FreeCAD_Object #+#
                        pn=n.split('_')[2]

                    vn=p.getData()

                    try:
                        v=self.fob.getPropertyByName(pn).Value
                    except:
                        v=self.fob.getPropertyByName(pn)
                    say("change value",n,pn,v,vn)
                    if v  !=  vn:  # value has changed
                        setattr(self.fob,pn,vn)
                except:
                    sayl("problem with store",n)
    
        FreeCAD.activeDocument().recompute()



    def createPins(self, *args, **kwargs):
        say('hack outsourced to nodeetitor.dev')
        import nodeeditor.dev
        reload (nodeeditor.dev)
        return  nodeeditor.dev.runraw(self)
        say("pins created")


    @staticmethod
    def description():
        return FreeCAD_Object.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Console(FreeCadNodeBase):
    '''
    write to FreeCAD.Console
    '''
    
    dok=4
    def __init__(self, name="Console"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.entity = self.createInputPin('entity', 'AnyPin',[], structure=StructureType.Multi)
        self.entity.description="data to print"
        self.entity.setData([FreeCAD.Vector(),FreeCAD.Vector()])



    def compute(self, *args, **kwargs):

        FreeCAD.Console.PrintMessage("%s: %s\n"%(self.name,self.entity.getData()))
        self.outExec.call()

    @staticmethod
    def description():
        return FreeCAD_Console.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []



class FreeCAD_ShapeExplorer(FreeCadNodeBase):
    '''
    information about a shape
    '''

    dok=3
    def __init__(self, name="MyPartExplorer"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.part = self.createInputPin('Shape_in', 'ShapePin')

        self.outArray = self.createOutputPin('Points', 'VectorPin', structure=StructureType.Array)
        self.outArray.description="the coodinates of the vertexes as vectors"
        
        a=self.createOutputPin('Faces', 'ShapeListPin')
        a.description="the list of faces"
        b=self.createOutputPin('Edges', 'ShapeListPin')
        b.description="the list of edges"

        self.pinsk={
                'Volume':'FloatPin',
                'Area':'FloatPin',
                'Length':'FloatPin',
                'BoundBox': None,
                'CenterOfMass':'VectorPin',
#               #'PrincipalProperties','StaticMoments',
                'Mass':'FloatPin',
                'ShapeType':'StringPin',
        }

        for p in list(self.pinsk.keys()):
            if self.pinsk[p]  !=  None:
                self.createOutputPin(p, self.pinsk[p])

        self.part.recomputeNode=True




    def compute(self, *args, **kwargs):

        shape=self.getPinObject("Shape_in")
        
        self.setPinObject("Shape_out",shape)
        if shape is None: return
        for n in list(self.pinsk.keys()):
            v=getattr(shape,n)
            if self.pinsk[n]  !=  None:
                self.setData(n,v)
        if 0:
            ls=shape.writeInventor().split('\n')
            for l in ls:say(l)

        points=[v.Point for v in getattr(shape,'Vertexes')]
        self.setData('Points',points)
        self.setPinObjects("Edges",shape.Edges)
        self.setPinObjects("Faces",shape.Faces)

        # output of the pins
        for t in self.getOrderedPins():
            if t.__class__.__name__ in ['ShapeListPin']:
                say("{} has {} items ({})".format(t.getName(),len(t.getData()),t.__class__.__name__))
            else:
                say("{} = {} ({})".format(t.getName(),t.getData(),t.__class__.__name__))

            if 0 and len(t.affects):
                for tt in t.affects:
                    if not tt.getName().startswith(self.getName()):
                        if tt.__class__.__name__ in ['AnyPin']:
                            say("----> {} (has {} items) ({})".format(tt.getName(),len(tt.getData()),tt.__class__.__name__))
                        else:
                            say("----> {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
                        FreeCAD.tt=tt
                        # say(tt.linkedTo[0])
                        a=FreeCAD.tt.linkedTo[0]['rhsNodeName']
                        say("call owning------------------",tt.owningNode().getName())

                        #start the follower node
                        #tt.owningNode().compute()

        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_ShapeExplorer.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []






class FreeCAD_ShapeIndex(FreeCadNodeBase):
    '''
    selection of a shape by its index in a list of shapes
    '''


    dok=3
    def __init__(self, name="MyShapeIndex"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

#        self.objname = self.createInputPin("objectname", 'StringPin')
#        self.objname.setData(name)


        p=self.createInputPin('Shapes', 'ShapeListPin')
        p.description="list of shapes #+#"
        p=self.createInputPin('index', 'IntPin')
        p.recomputeNode=True
        p.description ="index of the shape"

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


    def compute(self, *args, **kwargs):


        subshapes=self.getPinObjects("Shapes")
        if len(subshapes) == 0:
            sayW("no subshapes")
            return

        try:
            shape=subshapes[self.getData('index')]
        except:
            shape=Part.Shape()

#        say(subshapes)
#        say(self.getData('index'))
        self.setPinObject("Shape",subshapes[self.getData('index')])
        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_ShapeIndex.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape','Edge','Face','Part']




class FreeCAD_Face(FreeCadNodeBase):
    '''
    select a face of a shape by its number
    there can be a reference to a FreeCAD object by its name
    or a shapePin
    '''

    dok=4
    def __init__(self, name="MyFace"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'FacePin')

        a=self.createInputPin('sourceObject', 'StringPin')
        a.description="name of the FreeCAD object from which the face should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with faces"
        p=self.createInputPin('index', 'IntPin')
        p.description="number of the face, counting starts with 0"
        p.recomputeNode=True



    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            if shape is None: return
            edge=shape.Faces[self.getPinByName('index').getData()]
        else:
            face=obj.Shape.Edges[self.getPinByName('index').getData()]

        self.setPinObject("Shape_out",face)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Face.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape','Part']



class FreeCAD_Edge(FreeCadNodeBase):
    '''
    select a edge of a shape by its number
    there can be a reference to a FreeCAD object by its name
    or a shapePin
    '''

    dok=4
    
    def __init__(self, name="MyEdge"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'EdgePin')


        a=self.createInputPin('sourceObject', 'StringPin')
        a.description="name of the FreeCAD object from which the edge should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with edges"
        p=self.createInputPin('index', 'IntPin')
        p.description="number of the edge, counting starts with 0"
        p.recomputeNode=True


    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            if shape is None: return
            edge=shape.Edges[self.getPinByName('index').getData()]
        else:
            edge=obj.Shape.Edges[self.getPinByName('index').getData()]

        self.setPinObject("Shape_out",edge)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Edge.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape']


class FreeCAD_Destruct_Shape(FreeCadNodeBase):
    '''
    get the edges, faces and points of a shape
    there can be a reference to a FreeCAD object 
    by its name or a shapePin
    '''

    dok=4
    
    def __init__(self, name="MyDestruction"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.outArray = self.createOutputPin('Points', 'VectorPin', structure=StructureType.Array)
        self.outArray.description="a list of the vectors for the vertexes of the shape"
        a=self.createOutputPin('Faces', 'ShapeListPin')
        a.description="list of the faces of the shape"
        b=self.createOutputPin('Edges', 'ShapeListPin')
        a.description="list of the faces of the shape"


        a=self.createInputPin('sourceObject', 'StringPin')
        a.description="name of the FreeCAD object with the shape"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape without part"


    def compute(self, *args, **kwargs):

        objn=self.getPinByName('sourceObject').getData()
        obj=FreeCAD.ActiveDocument.getObject(objn)
        if obj == None:
            sayW("no object found with name {}, use Shape_in instead".format(objn))
            shape=self.getPinObject("Shape_in")
            
        else:
            shape=obj.Shape
        if shape is None: return
        edges=shape.Edges
        faces=shape.Faces

        points=[v.Point for v in getattr(shape,'Vertexes')]
        self.setData('Points',points)
        self.setPinObjects("Edges",edges)
        self.setPinObjects("Faces",faces)

        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_Edge.__doc__

    @staticmethod
    def category():
        return 'Details'

    @staticmethod
    def keywords():
        return ['Shape']



class FreeCAD_Parallelprojection(FreeCadNodeBase):
    '''
    parallal projection of an edge onto a face
    '''

    dok=4
    def __init__(self, name="MyParallelProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"
        
        p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
        p.recomputeNode=True
        p.description="direction of the projection light"


    def compute(self, *args, **kwargs):

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_projection_compute(self,*args, **kwargs)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_Parallelprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []


class FreeCAD_Perspectiveprojection(FreeCadNodeBase):
    '''
    perspective projection of an edge onto a face
    '''

    dok=4
    def __init__(self, name="MyPerspectiveProjection"):
        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"
        
        p=self.createInputPin('center', 'VectorPin',FreeCAD.Vector(0,0,1000))
        p.recomputeNode=True
        p.description="center of projection, position of the point light"


    def compute(self, *args, **kwargs):

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_perspective_projection_compute(self,*args, **kwargs)
        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_Perspectiveprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []


class FreeCAD_UVprojection(FreeCadNodeBase):
    '''
    uv projection of an edge onto a face
    the curve is discretized,
    the points are mapped 
    and a interpolated curve is computed
    '''

    dok=4
    def __init__(self, name="MyUVProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        p=self.createInputPin('face', 'ShapePin')
        p.description="the target face for projection"
        
        p=self.createInputPin('edge', 'ShapePin')
        p.description="the edge which is projected"

        p=self.createInputPin('pointCount', 'IntPin',20)
        p.description="number of points of the edge used for constructing the curve"

    # zum aufpolstern #+# trennen in zweite node!
        p=self.createInputPin('inverse', 'BoolPin')
        p=self.createInputPin('Extrusion', 'BoolPin')
        p=self.createInputPin('ExtrusionUp', 'FloatPin',100)
        p=self.createInputPin('ExtrusionDown', 'FloatPin',50)
        p.recomputeNode=True


    def compute(self, *args, **kwargs):

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_uv_projection_compute(self,*args, **kwargs)
        self.outExec.call()

        if self._preview:
            self.preview()


    @staticmethod
    def description():
        return FreeCAD_UVprojection.__doc__

    @staticmethod
    def category():
        return 'Projection'

    @staticmethod
    def keywords():
        return []



class FreeCAD_Compound(FreeCadNodeBase):
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



class FreeCAD_Plot(FreeCadNodeBase):
    '''
    display matplotlib windows with data
    '''

    dok= 4
    def __init__(self, name="MyPlot"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        self.xpin=self.createInputPin('x', 'FloatPin', structure=StructureType.Array)
        self.ypin=self.createInputPin('y', 'FloatPin', structure=StructureType.Array)

        self.xpin2=self.createInputPin('x2', 'FloatPin', structure=StructureType.Array)
        self.ypin2=self.createInputPin('y2', 'FloatPin', structure=StructureType.Array)

        self.xpin.description="x values for the first curve"
        self.ypin.description="y values for the first curve"
        self.xpin2.description="x values for the 2nd curve"
        self.ypin2.description="y values for the 2nd curve"
        

        self.mode = self.createInputPin('Figure', 'EnumerationPin')
        self.mode.values=["Figure1","Figure2","Figure3","Figure4"]
        self.mode.setData("Figure1")
        self.mode.recomputeNode=True
        self.mode.description="Selector for the window name, there a re at most 4 diagram windows possible"
        

    @staticmethod
    def description():
        return FreeCAD_Plot.__doc__

    @staticmethod
    def category():
        return 'Information'

    @staticmethod
    def keywords():
        return []

#------------------------------------------------------------------


class FreeCAD_Ref(FreeCadNodeBase):
    '''
    a reference to the shape or subobjects of a FreeCAD part
    select a part or some subobjects oof the same object. 
    Than a node with pins for all
    these selected details is created.
    '''

    dok=4
    def __init__(self, name="MyReference",**kvargs):
        try:
            s=FreeCADGui.Selection.getSelection()[0]
            name="REF_"+s.Name
        except:
            name="REF_None"


        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin('Reload Shapes', 'ExecPin', None, self.compute)
        self.inExec.description="force a reload of shape when the shape has chanched  inside FreeCAD"

        self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.refresh)
        self.inExec.description="set the reference to another subshape which must be selected in FreeCAD before adapt is called"

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.description="name of the part used for reference, this parameter is changed automaticly by the adapt button."
        self.objname.setData(name)
        self.objname="name of the FreeCAD object"

        self._refpins = []

        try:
            self.refresh()
        except:
            pass


    def refresh(self, *args, **kwargs):
        '''reasign to a new gui selection: create new pins '''

        sels=FreeCADGui.Selection.getSelection()
        subsels=FreeCADGui.Selection.getSelectionEx()
        pins=self.getOrderedPins()

        newpinnames=[]
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                newpinnames += [pinname]

            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape_out"
                newpinnames += [pinname]


        #clean up
        say("newpinnmes",newpinnames)
        oldpinnames=[]
        for p in pins:
            say(p.name)
            if not p.isExec(): 
                if p.name not in newpinnames:
                    say("kill",p.name)
                    p.kill()
                else:
                    oldpinnames += [p.name]

        
        say("oldpinnames",oldpinnames)
        # pins for sub shapes
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                if pinname not in oldpinnames:
                    pintyp="ShapePin"
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                    try:
                        uiPin = self.getWrapper()._createUIPinWrapper(p2)
                        uiPin.setDisplayName("{}".format(p2.name))
                    except:
                        pass

                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape_out"
                pintyp="ShapePin"
                if pinname not in oldpinnames:
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)

                self.setPinObject(pinname,subob)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(s.ObjectName)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.compute(args,kwargs)


    def createPins(self,objname,pinnames):
            
        # pins for sub shapes
        oldpinnames=[]
        for s in [1]:
            subscreated=False
            for name in pinnames:
                subscreated=True
                pinname=name
                
                if 1: # pinname not in oldpinnames:
                    pintyp="ShapePin"
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                    try:
                        uiPin = self.getWrapper()._createUIPinWrapper(p2)
                        uiPin.setDisplayName("{}".format(p2.name))
                    except:
                        pass

##                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                pinname="Shape_out"
                pintyp="ShapePin"
                if pinname not in oldpinnames:
                    p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)

                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        #self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(objname)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.compute()
        



    def compute(self, *args, **kwargs):
        '''update shape-links'''

        pins=self.getOrderedPins()
        objname=self.getPinByName("objectname").getData()
        self._refpins=[]

        obj=FreeCAD.activeDocument().getObject(objname)
        for p in pins:
            if not p.isExec():
                if p.name == "Shape_out":
                    self.setPinObject(p.name,obj.Shape)
                elif p.name  !=  "objectname" :
                    try:
                        subob =getattr(obj.Shape,p.name)
                        self.setPinObject(p.name,subob)
                        self._refpins += [p.name]
                    except:
                        pass
        self.outExec.call()

        if self._preview:
            self.preview()
            
        a=self.makebackref()
        if a != None:
            a.sources=[obj]
        
        try:
            wr=self.getWrapper()
            wr.setHeaderHtml("Ref: "+obj.Label)
            self.setColor(b=0,a=0.4)
        except:
            pass


    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']

#--------------------------------


    def serialize(self):
        # eigentliches objekt serialisieren
        data = super(self.__class__, self).serialize()
        # extra data
        data['reflist'] = "extra data for reflisrt"
        data['_refpins'] = self._refpins
        say("serialize")
        say(data['_refpins'])
        return data

    
    def postCreate(self, jsonTemplate=None):
        super(self.__class__, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamic pins extra data
        say("postcreate")

        if jsonTemplate is not None and '_refpins' in jsonTemplate:
            say("process extra data:",jsonTemplate['_refpins'])
            objname=self.getPinByName("objectname").getData()
            pinnames=jsonTemplate['_refpins']
            say(objname)
            say(pinnames)
            self.createPins(objname,pinnames)
            say("done")
            

#--------------------------------

class FreeCAD_RefList(FreeCadNodeBase):
    '''
    a reference to a list of objects
    '''

    def __init__(self, name="MyReferenceList",**kvargs):
        try:
            s=FreeCADGui.Selection.getSelection()[0]
            name="REF_"+s.Name
        except:
            name="REF_None"

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.compute)
#       self.inExec = self.createInputPin('Adapt Selection', 'ExecPin', None, self.refresh)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
#        self.objname = self.createInputPin("objectname", 'StringPin')
#        self.objname = self.createInputPin("positions", 'VectorPin',structure=StructureType.Array)
#        self.objname = self.createInputPin("rotations", 'RotationPin',[],structure=StructureType.Array)
#        self.objname.setData(name)

        try:
            self.refresh()
        except:
            pass


    def refresh(self, *args, **kwargs):
        '''reasign to a new gui selection: create new pins '''

        sels=FreeCADGui.Selection.getSelection()
        subsels=FreeCADGui.Selection.getSelectionEx()
        pins=self.getOrderedPins()

        #clean up
        for p in pins:
#            if not p.isExec():
            if not p.isExec() and p.direction  !=  PinDirection.Input :
                p.kill()

        # pins for sub shapes
        for s in subsels:
            subscreated=False
            objname=s.ObjectName
            for name,subob in zip(s.SubElementNames,s.SubObjects):
                subscreated=True
                pinname=name
                pintyp="ShapePin"
                p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{}".format(p2.name))
                except:
                    pass

                self.setPinObject(pinname,subob)

            # if no subshapes selected, create shape pin
            if not subscreated:
                subob=sels[0].Shape
                pinname="Shape"
                pintyp="ShapePin"
                p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
                self.setPinObject(pinname,subob)
                try:
                    uiPin = self.getWrapper()._createUIPinWrapper(p2)
                    uiPin.setDisplayName("{0}".format(p2.name))
                except:
                    pass

        # remember objectname
        #self.objname = self.createInputPin("objectname", 'StringPin')
        #self.objname.setData(s.ObjectName)

        try:
            wr=self.getWrapper()
            newName = wr.canvasRef().graphManager.getUniqNodeName("Ref_"+objname)
            wr.setHeaderHtml(newName)
            uiPin = self.getWrapper()._createUIPinWrapper(self.objname)
            uiPin.setDisplayName("{}".format(self.objname.name))
        except:
            pass

        self.outExec.call()


    def Xcompute(self, *args, **kwargs):
        '''update shape-links'''

        pins=self.getOrderedPins()
        objname=self.getPinByName("objectname").getData()

        obj=FreeCAD.activeDocument().getObject(objname)
        for p in pins:
            if not p.isExec():
                if p.name == "Shape":
                    self.setPinObject(p.name,obj.Shape)
                elif p.name  !=  "objectname":
                    subob =getattr(obj.Shape,p.name)
                    self.setPinObject(p.name,subob)

    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']



class FreeCAD_LOD(FreeCadNodeBase):
    '''
    Level of Detail switch
    '''

    dok=4
    def __init__(self, name="MyLOD",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.lod = self.createInputPin('LOD', 'IntPin')
        self.lod.recomputeNode=True
        self.lod.description="Level of detail 1, 2, 3"
        self.createInputPin('ShapeLOD_1', 'ShapePin').description="shape for LOD 1"
        self.createInputPin('ShapeLOD_2', 'ShapePin').description="shape for LOD 2"
        self.createInputPin('ShapeLOD_3', 'ShapePin').description="shape for LOD 3"
        self.createOutputPin('Shape_out', 'ShapePin')


    def compute(self, *args, **kwargs):
        '''update shape-links'''
        lod=self.getData('LOD')
        if lod in [1,2,3]:
            self.setData('Shape_out',self.getData('ShapeLOD_'+str(lod)))
        else:
            say("lod out of range")
        self.outExec.call()

        if self._preview:
            self.preview()

    @staticmethod
    def description():
        return FreeCAD_Ref.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']



class FreeCAD_view3D(FreeCadNodeBase):
    '''
    create an instance in 3D space of FreeCAD, show the shape
    '''

    dok = 4
    def __init__(self, name="MyView3D",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d').\
        description = "name of the object in 3D space"
        self.createInputPin('Workspace', 'StringPin','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"


    @staticmethod
    def description():
        return FreeCAD_view3D.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape','Edge','Selection']


class FreeCAD_bakery(FreeCadNodeBase):
    '''
    Part.show for a shape without parametric connection, the result is not overwritten but a new object is created 
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d').\
        description = "name of the object in 3D space"

        self.createInputPin('label', 'StringPin','view3d').\
        description = "label for the object in 3D space"
        #+# todo:add functionality for label

        self.createInputPin('Workspace', 'StringPin','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"

    @staticmethod
    def description():
        return FreeCAD_bakery.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape',]


class FreeCAD_topo(FreeCadNodeBase):
    '''
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('name', 'StringPin','view3d').\
        description = "name of the object in 3D space"

        self.createInputPin('label', 'StringPin','view3d').\
        description = "label for the object in 3D space"
        #+# todo:add functionality for label

        self.createInputPin('Workspace', 'StringPin','').\
        description = " name of the workspace where the view is displayed, if empty  the active document is used" 
        self.createInputPin('Shape_in', 'ShapePin').\
        description= "shape to display"
        self.createOutputPin('Shape_out', 'ShapePin').description="filled face"
        self.createOutputPin('Shape_lost', 'ShapePin').description="filled face"
        self.createOutputPin('Shape_new', 'ShapePin').description="filled face"

    @staticmethod
    def description():
        return FreeCAD_topo.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Part','Shape',]



class FreeCAD_conny(FreeCadNodeBase):
    '''
    connect edges and close gaps, create a filled face 
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        '''
        a=self.createInputPin('degree', 'IntPin',3)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a=self.createInputPin('rotateAxis', 'IntPin',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a=self.createInputPin('simpleConnection', 'BoolPin')
        a.recomputeNode=True
        
        '''

        a=self.createInputPin('ff', 'BoolPin')
        a.recomputeNode=True
        a.description='a flag to change the ordering of the gap filler curves'

        a=self.createInputPin('tangentForce', 'IntPin',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description=' how smooth the open ends of edges should be connected. 0 means no tangent support, this is a straight line from one end to the other'

        a=self.createInputPin('createFace', 'BoolPin')
        a.recomputeNode=True
        a.description='''if this flag is set a filled face will be computed. Because the Part.filledFace is a miraclic method this call sometimes fails and other approaches are better'''

        
#        a=self.createInputPin('Shape_in', 'ShapePin')     
#        a.enableOptions(PinOptions.AllowMultipleConnections)
#        a.disableOptions(PinOptions.SupportsOnlyArrays)

        self.shapes=self.createInputPin('Shapes_in', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)
        self.shapes.description='multiple edges or wires which should be connected'


        self.createOutputPin('Shape_out', 'ShapePin').description="a filled face shape or the border (closed curve) of it"
        self.createOutputPin('gaps', 'ShapePin').description="edges created to get wire closed"
        self.createOutputPin('border', 'ShapePin').description="edges of the face only"

    @staticmethod
    def description():
        return FreeCAD_conny.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Edge','FilledFace',]


class FreeCAD_randomizePolygon(FreeCadNodeBase):
    '''
    add some randomness to a polygon
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('factorEnds', 'IntPin',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description="factor for randomness on the endpoints of the polygon"

        a=self.createInputPin('factorInner', 'IntPin',2)
        a.recomputeNode=True
        a.setInputWidgetVariant("Simple")
        a.description="factor for randomness for the inner points of the polygon"

        self.shapes=self.createInputPin('Shape_in', 'ShapePin', None)
        self.arrayData = self.createInputPin('points', 'VectorPin', structure=StructureType.Array)

        self.createOutputPin('Shape_out', 'ShapePin').description="modified points as wire"
        self.arrayData = self.createOutputPin('points_out', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="modified position of the vertexes as vectorlist"

    @staticmethod
    def description():
        return FreeCAD_randomizePolygon.__doc__

    @staticmethod
    def category():
        return 'Document'

    @staticmethod
    def keywords():
        return ['Polygon','random','Vector']



class FreeCAD_Toy(FreeCadNodeBase):
    '''
    methode zum spielen
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        '''
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)

        self.trace = self.createInputPin('flag', 'BoolPin')
        self.shapelist = self.createInputPin("ShapeList", 'ShapeListPin')
        t = self.createInputPin("Shape", 'ShapePin')
        t.enableOptions(PinOptions.AllowMultipleConnections)
        t.disableOptions(PinOptions.SupportsOnlyArrays)

        t = self.createInputPin("ROT", 'RotationPin',(8,9,0))
        t = self.createOutputPin("ROT_out", 'RotationPin',(3,4,5))
        t = self.createInputPin("PM", 'PlacementPin',(8,9,0))
        t = self.createOutputPin("PM_out", 'PlacementPin',(3,4,5))


        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout = self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.objname = self.createInputPin("objectname", 'StringPin')

        name="MyToy"
        self.objname.setData(name)
        '''
        
        import  PyFlow.Packages.PyFlowFreeCAD
        pincs=PyFlow.Packages.PyFlowFreeCAD.PyFlowFreeCAD.GetPinClasses()
    

        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))

        import  PyFlow.Packages.PyFlowBase
        pincs=PyFlow.Packages.PyFlowBase.PyFlowBase.GetPinClasses()
    

        #return
        for p in pincs:
            say("!",p)
            if p in ["AnyPin","ArrayPin"]:continue
            self.createInputPin(str(p)+"_in",str(p))
            self.createOutputPin(str(p)+"_out",str(p))


    @staticmethod
    def description():
        return FreeCAD_Toy.__doc__

    @staticmethod
    def category():
        return 'Development'




class FreeCAD_figureOnFace(FreeCadNodeBase):
    '''
    map figures pattens onto a surface
    '''

    dok = 4

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.shapeout = self.createInputPin('Shape_in', 'ShapePin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout = self.createOutputPin('details', 'ShapeListPin')

        self.createInputPin('pattern', 'VectorPin', structure=StructureType.Array)
        
        a=self.createInputPin("cutBorder", 'BoolPin')
        a.recomputeNode=True
        
        self.createInputPin('transformation', 'TransformationPin')

        #beispiel fuer parametre range int
        a=self.createInputPin("degree", 'IntPin',1)
        a.annotationDescriptionDict={ "ValueRange":(0.,3.)}     
        #a.recomputeNode=True
        a=self.createInputPin("createFaces", 'BoolPin',False)
        #a.recomputeNode=True
        a=self.createInputPin("tangentForce", 'FloatPin',10)
        a.annotationDescriptionDict={ "ValueRange":(0.,100.)}
        a.recomputeNode=True


    @staticmethod
    def description():
        return FreeCAD_figureOnFace.__doc__

    @staticmethod
    def category():
        return 'HighLevel'

## ||
## \/ okay


class FreeCAD_listOfVectors(FreeCadNodeBase):
    '''
    create a list of vectors from  single vectors
    the order of the vector is defined by
    the y coordiante of the vector nodes
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createOutputPin('vectors', 'VectorPin', structure=StructureType.Array)

        self.pas=self.createInputPin('pattern', 'VectorPin')
        self.pas.enableOptions(PinOptions.AllowMultipleConnections)
        self.pas.disableOptions(PinOptions.SupportsOnlyArrays)



    @staticmethod
    def description():
        return FreeCAD_listOfVectors.__doc__

    @staticmethod
    def category():
        return 'Conversion'




class FreeCAD_moveVectors(FreeCadNodeBase):
    '''
    move a list of vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)
        a.description="__mover__ is added to all __vectors__"

        a=self.createInputPin('mover', 'VectorPin')
        a.recomputeNode=True
        a.description ="mover vector"

    @staticmethod
    def description():
        return FreeCAD_moveVectors.__doc__

    @staticmethod
    def category():
        return 'Projection'


class FreeCAD_scaleVectors(FreeCadNodeBase):
    '''
    scale list of vectors
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.createInputPin('vectors', 'VectorPin', structure=StructureType.Array)
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)

        a=self.createInputPin('scaler', 'VectorPin')    
        a.recomputeNode=True
        a.description ="factors to scale the three  ain axes"


    @staticmethod
    def description():
        return FreeCAD_scaleVectors.__doc__

    @staticmethod
    def category():
        return 'Projection'



class FreeCAD_repeatPattern(FreeCadNodeBase):
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
        return FreeCAD_repeatPattern.__doc__

    @staticmethod
    def category():
        return 'Combination'



class FreeCAD_Transformation(FreeCadNodeBase):
    '''
    affine transformation matrix
    '''

    dok = 4
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
        
        self.createOutputPin('transformation', 'TransformationPin' )

    @staticmethod
    def description():
        return FreeCAD_Transformation.__doc__

    @staticmethod
    def category():
        return 'Conversion'


class FreeCAD_Reduce(FreeCadNodeBase):
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
        a=self.createInputPin('selection', 'BoolPin',structure=StructureType.Array)
        a.description="list of flags which shapes should be in the resulting list"

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')
        self.shapeout.description = "compound of the filtered shapes" 

    @staticmethod
    def description():
        return FreeCAD_Reduce.__doc__

    @staticmethod
    def category():
        return 'Construction'


class FreeCAD_IndexToList(FreeCadNodeBase):
    '''
    create a flag list with 1 for the numbers 
    and 0 for the others
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('index', 'IntPin')
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


class FreeCAD_distToShape(FreeCadNodeBase):
    '''
    list of distances from  a list of shapes 
    to a target shape
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


        a=self.createInputPin('shapes', 'ShapeListPin')
        a.description="list of shapes"
        a=self.createInputPin('target', 'ShapePin')
        a.description="target shape"

        a=self.createOutputPin('distance', 'FloatPin',structure=StructureType.Array)
        a.description="distances"

    @staticmethod
    def description():
        return FreeCAD_distToShape.__doc__

    @staticmethod
    def category():
        return 'Information'


class FreeCAD_centerOfMass(FreeCadNodeBase):
    '''
    center of mass for a list of shapes
    '''

    dok=4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapelist = self.createInputPin("ShapeList", 'ShapeListPin')
        self.shapelist.description="list of shapes to discover" 

        self.shapeout = self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        self.shapeout.description="the centers of mass for the shapes in __ShapeList__"


    @staticmethod
    def description():
        return FreeCAD_centerOfMass.__doc__

    @staticmethod
    def category():
        return 'Information'


class FreeCAD_listOfShapes(FreeCadNodeBase):
    '''
    create a list of shapes from single shapes
    '''

    dok = 4
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
        return FreeCAD_listOfShapes.__doc__

    @staticmethod
    def category():
        return 'Conversion'



class FreeCAD_listOfPlacements(FreeCadNodeBase):
    '''
    create a list of placements from  lists of data
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('moves', 'VectorPin',structure=StructureType.Array)
        a.description="moving vectors/base vector property of the placements, default is (0,0,0) "
        
        a=self.createInputPin('axes', 'VectorPin',structure=StructureType.Array)
        a.description="rotation axes, default is (0,0,1)"
        
        a=self.createInputPin('angles', 'FloatPin',structure=StructureType.Array)
        a.description="rotation angles in degree, default is 0"
        
        
        a=self.createInputPin('centers', 'VectorPin',structure=StructureType.Array)
        a.description="rotation centers, default is (0,0,0)"

        a=self.createOutputPin('Placements', 'PlacementPin',structure=StructureType.Array)
        a.description="list of placements created from given lists, the length is defined by the longest input list, the values for the other list are filled with default values"

    @staticmethod
    def description():
        return FreeCAD_listOfPlacements.__doc__



class FreeCAD_applyPlacements(FreeCadNodeBase):
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
        return FreeCAD_applyPlacements.__doc__



class FreeCAD_repeat(FreeCadNodeBase):
    '''
    list of the same element repeated
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('in', 'AnyPin',constraint='1')   
        a.description="element to repeat"
        a=self.createOutputPin('out', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description="count repetitions of elment in" 
        a=self.createInputPin('count', 'IntPin',2) 
        a.description="how often to repeat element in"
          
        a=self.createOutputPin('Shapes', 'ShapeListPin')
        a.description="list of shapes if input element is a shape"
        
    @staticmethod
    def description():
        return FreeCAD_repeat.__doc__



class FreeCAD_Index(FreeCadNodeBase):
    '''
    returns item with a given index from a list
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('list', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description="a list"
        
        a=self.createInputPin('index', 'IntPin',2)
        a.recomputeNode=True
        a.description='position of the item in the list starting with 0'
        a=self.createOutputPin('item', 'AnyPin',constraint='1')
        a.description="element of list at index position"
        

    @staticmethod
    def description():
        return FreeCAD_Index.__doc__


#------------------------


class FreeCAD_Zip(FreeCadNodeBase):
    '''
    create a list of vectors from the lists of coordinates
    '''

    dok = 4
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('x', 'FloatPin',structure=StructureType.Array)
        a.description='list of x coordinates'

        a=self.createInputPin('y', 'FloatPin',structure=StructureType.Array)
        a.description='list of y coordinates'

        a=self.createInputPin('z', 'FloatPin',structure=StructureType.Array)
        a.description='list of z coordinates'

        a=self.createOutputPin('vectors_out', 'VectorPin',structure=StructureType.Array)
        a.description='list of created vectors'

    @staticmethod
    def description():
        return FreeCAD_Zip.__doc__

class FreeCAD_Tube(FreeCadNodeBase):
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
        a=self.createInputPin('parameter', 'FloatPin',structure=StructureType.Array)
        a.description="u parameter of the position of the ribs"
        a=self.createInputPin('radius', 'FloatPin',structure=StructureType.Array)
        a.description="radius/size of the rib rings"
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)
        a.description="array of poles for the postprocessing bspline surface"

    @staticmethod
    def description():
        return FreeCAD_Tube.__doc__

    @staticmethod
    def category():
        return 'Construction'



def nodelist():
    return [
                FreeCAD_Toy,
                FreeCAD_Object,
                FreeCAD_Box,
                FreeCAD_Cone,
                FreeCAD_Sphere,
                FreeCAD_Quadrangle,

                FreeCAD_Polygon,
                FreeCAD_Console,
                FreeCAD_VectorArray,
                FreeCAD_Boolean,
                FreeCAD_BSplineSurface,
                FreeCAD_BSplineCurve,

                FreeCAD_Plot,
                FreeCAD_ShapeIndex,
                FreeCAD_ShapeExplorer,
                FreeCAD_Compound,
                FreeCAD_Edge,
                FreeCAD_Face, 

                FreeCAD_Parallelprojection,
                FreeCAD_Perspectiveprojection,
                FreeCAD_UVprojection,
                FreeCAD_Ref,
                
                FreeCAD_LOD,
                FreeCAD_view3D,
                FreeCAD_Destruct_Shape,

                FreeCAD_listOfVectors,
                FreeCAD_moveVectors,
                FreeCAD_scaleVectors,
                FreeCAD_repeatPattern,
                FreeCAD_Transformation,
                FreeCAD_Reduce,
                FreeCAD_IndexToList,
                FreeCAD_distToShape,
                FreeCAD_centerOfMass,
                FreeCAD_listOfShapes,
                FreeCAD_listOfPlacements,
                FreeCAD_applyPlacements,
                FreeCAD_repeat,
                FreeCAD_Index,
                FreeCAD_Zip,#ok bis hier
                
                FreeCAD_Tube,

                # noch zu dokumentieren ##############################
                FreeCAD_bakery,
                FreeCAD_topo,
                FreeCAD_conny,
                FreeCAD_randomizePolygon,
                FreeCAD_figureOnFace,

                # FreeCAD_RefList, muss noch programmiert werden
        ]
