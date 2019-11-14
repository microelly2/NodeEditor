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

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase


import sys
if sys.version_info[0] !=2:
	from importlib import reload





class FreeCAD_Box( FreeCadNodeBase):
    '''
    erzeuge einer Part.Box
    '''

    def __init__(self, name="MyBox"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.randomize = self.createInputPin("randomize", 'BoolPin')


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
    erzeuge einer BSpline Flaeche degree 1
    by 4 points
    '''

    def __init__(self, name="MyQuadrangle"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

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

        self.setPinObject("Shape",shape)

        if self.shapeout.hasConnections():
            self.postCompute()

        if self.shapeOnly.getData():
            self.postCompute()
        else:
            cc=self.getObject()
            cc.Label=self.objname.getData()
            cc.Shape=shape
            self.postCompute(cc)

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



class FreeCAD_Polygon2(FreeCadNodeBase):
    '''
    erzeuge eines Streckenzugs
    input pin for a list of vectors
    '''

    def __init__(self, name="MyPolygon"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.points = self.createInputPin('points', 'VectorPin',[], structure=StructureType.Multi)
        self.points.setData([FreeCAD.Vector(0,0,0),FreeCAD.Vector(10,0,0)])


        self.Called=False
        self.count=2


    @timer
    def compute(self, *args, **kwargs):

        # recursion stopper
        if self.Called:
            return
        #sayl()
        # mit zeitstemple aktivieren
        #self.Called=True

        pts=self.points.getData()
        if len(pts)<2:
            sayW("zu wenig points")
        else:
            try:
                shape=Part.makePolygon(pts)
            except:
                return


            self.setPinObject("Shape",shape)

            if self.shapeout.hasConnections():
                self.postCompute()

            if self.shapeOnly.getData():
                cc=self.getObject()
                self.postCompute()
            else:
                cc=self.getObject()
                if cc  !=  None:
                    cc.Label=self.objname.getData()
                    cc.Shape=shape
                    self.postCompute(cc)

        if self._preview:
            self.preview()

        #self.Called=False

    @staticmethod
    def description():
        return FreeCAD_Polygon2.__doc__

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

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.part1 = self.createInputPin('Part_in1', 'FCobjPin')
        self.part2 = self.createInputPin('Part_in2', 'FCobjPin')

        self.shape1 = self.createInputPin('Shape_in1', 'ShapePin')
        self.shape2 = self.createInputPin('Shape_in2', 'ShapePin')

        self.mode = self.createInputPin('mode', 'EnumerationPin')
        self.mode.values=["fuse","cut","common"]
        self.mode.setData("fuse")

        self.volume = self.createOutputPin('Volume', 'FloatPin')

        self.objname.setData(name)

    @timer
    def compute(self, *args, **kwargs):

#       say ("in compute",self.getName(),"objname is",self.objname.getData())

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

        mode=self.mode.getData()
        if mode == 'common':
            shape=s1.common(s2)
        elif mode == 'cut':
            shape=s1.cut(s2)
        else:
            shape=s1.fuse(s2)


        if self.shapeOnly.getData():
            self.postCompute()
        else:
            cc=self.getObject()
            cc.Label=self.objname.getData()
            cc.Shape=shape
            self.postCompute(cc)

        self.setPinObject('Shape',shape)


        if self.part.hasConnections():
            say("send a Part")
            if cc == None:
                self.part.setData(None)
            else:
                self.part.setData(cc.Name)

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
    '''BSpline Surface'''

    @staticmethod
    def description():
        return '''create a default bspline surface from poles and degrees'''


    def __init__(self, name="MyBSplineSurface"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.arrayData.description="Array of poles vectors"
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createInputPin('maxDegreeU', 'IntPin', 3)
        self.createInputPin('maxDegreeV', 'IntPin', 3)

        self.shapeout = self.createOutputPin('Shape_out', 'FacePin')
        self.shapeout.description='BSpline Face'
#        self.createOutputPin('geometry', 'ShapePin').\
#        description='BSpline Surface geometry'

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
    '''BSpline Curve'''

    @staticmethod
    def description():
        return '''create a default bspline surface from poles and degrees'''


    def __init__(self, name="MyBSplineCurve"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.randomize = self.createInputPin("randomize", 'BoolPin')
        self.shapeout = self.createOutputPin('Shape_out', 'EdgePin')
        self.arrayData = self.createInputPin('poles', 'VectorPin', structure=StructureType.Array)
        self.createInputPin('maxDegree', 'IntPin', 3)

        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)


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
    '''Array of Vectors Surface'''

    def __init__(self, name="MyVectorArray"):

        super(self.__class__, self).__init__(name)

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.createInputPin("vecA", 'VectorPin',FreeCAD.Vector(20,0,0))
        self.createInputPin("vecB", 'VectorPin',FreeCAD.Vector(0,10,0))
        self.createInputPin("vecC", 'VectorPin')
        self.createInputPin("vecBase", 'VectorPin')
        self.createInputPin("countA", 'IntPin',5)
        self.createInputPin("countB", 'IntPin',8)
        self.createInputPin("countC", 'IntPin',1)
        self.createInputPin("randomX", 'FloatPin',5)
        self.createInputPin("randomY", 'FloatPin',5)
        self.createInputPin("randomZ", 'FloatPin',5)
        self.createInputPin("degreeA", 'IntPin',3)
        self.createInputPin("degreeB", 'IntPin',3)
        self.createOutputPin('vectors_out', 'VectorPin', structure=StructureType.Array)


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

    def __init__(self, name="MyObject"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

#        self.trace = self.createInputPin('trace', 'BoolPin')
#        self.randomize = self.createInputPin("randomize", 'BoolPin')

#        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData("Box")

#        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
#        self.shapeOnly.recomputeNode=True


        self.createInputPin('Reload_from_FC', 'ExecPin', None, self.reload)
        self.createInputPin('Store_to_FC', 'ExecPin', None, self.store,)
#        for i in range(7):
#            self.createOutputPin('dummy', 'ExecPin')



    def compute(self, *args, **kwargs):

        say("")
        say ("in compute",self.getName(),"objname is",self.objname.getData())
        nl=len(self.getName())
        pps=self.getOrderedPins()
        say(pps)
        for p in pps:
            try:
                print((str(p.getName()[nl+1:]),p.getData()))
            except:  pass
        obn=self.objname.getData()
        obj=FreeCAD.ActiveDocument.getObject(obn)
        self.fob=obj
        self.store()
        try:
            sh=obj.Shape
            self.setPinObject("Shape_out",sh)
        except:
            pass # no shape

        self.outExec.call()

        a=self.makebackref()
        if a != None:
            a.sources=[obj]


        if self._preview:
            self.preview()



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
    def __init__(self, name="Console"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.entity = self.createInputPin('entity', 'AnyPin',[], structure=StructureType.Multi)
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
    dummy for tests
    '''

    def __init__(self, name="MyPartExplorer"):

        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

#        self.trace = self.createInputPin('trace', 'BoolPin')
#        self.randomize = self.createInputPin("randomize", 'BoolPin')

#        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')

#        self.objname = self.createInputPin("objectname", 'StringPin')
#        self.objname.setData(name)

#        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
#        self.shapeOnly.recomputeNode=True

        self.part = self.createInputPin('Shape_in', 'ShapePin')
        self.outArray = self.createOutputPin('Points', 'VectorPin', structure=StructureType.Array)
        a=self.createOutputPin('Faces', 'ShapeListPin')
        b=self.createOutputPin('Edges', 'ShapeListPin')

        self.pinsk={
                'Volume':'FloatPin',
                'Area':'FloatPin',
                'Length':'FloatPin',
                'BoundBox': None,
                'CenterOfMass':'VectorPin',
#               #'Edges','Faces','Vertexes','Compounds','Wires','Shells',
#               #'PrincipalProperties','StaticMoments',
                'Mass':'FloatPin',
                'ShapeType':'StringPin',
#
        }

        say(self.pinsk)
        for p in list(self.pinsk.keys()):
            if self.pinsk[p]  !=  None:
                say(p,self.pinsk[p])
                self.createOutputPin(p, self.pinsk[p])

        self.part.recomputeNode=True




    def compute(self, *args, **kwargs):

        shape=self.getPinObject("Shape_in")
        self.setPinObject("Shape_out",shape)
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

        # testweise lesen
        if 0:
            edges=self.getPinObjects("Edges")
            Part.show(Part.Compound(edges[:-1]))

            edges=self.getPinObjects("Faces")
            Part.show(Part.Compound(edges[:4]))

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
    dummy for tests
    '''


    def __init__(self, name="MyShapeIndex"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        p=self.createInputPin('Shapes', 'AnyPin')
        p.recomputeNode=True
        p=self.createInputPin('index', 'IntPin')
        p.recomputeNode=True

        self.shapeout = self.createOutputPin('Shape', 'ShapePin')


    def compute(self, *args, **kwargs):

#       import nodeeditor.dev
#       reload (nodeeditor.dev)
#       nodeeditor.dev.run_ShapeIndex_compute(self,*args, **kwargs)
#   def run_ShapeIndex_compute(self,*args, **kwargs):

        sayl()
        subshapes=self.getPinObjects("Shapes")
        if len(subshapes) == 0:
            sayW("no subshapes")
            return

        try:
            shape=subshapes[self.getData('index')]
        except:
            shape=Part.Shape()
        say(subshapes)
        say(self.getData('index'))
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
    there can be a reference to a FreeCAD object by its name
    or a shapePin
    '''

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
    dummy for tests
    '''

    def __init__(self, name="MyParallelProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        p=self.createInputPin('face', 'AnyPin')
        p=self.createInputPin('edge', 'AnyPin')
        p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
        p.recomputeNode=True


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
    dummy for tests
    '''

    def __init__(self, name="MyPerspectiveProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        p=self.createInputPin('face', 'AnyPin')
        p=self.createInputPin('edge', 'AnyPin')
        p=self.createInputPin('center', 'VectorPin',FreeCAD.Vector(0,0,1000))
        p.recomputeNode=True


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
    dummy for tests
    '''

    def __init__(self, name="MyUVProjection"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        p=self.createInputPin('face', 'AnyPin')
        p=self.createInputPin('edge', 'AnyPin')
        #p=self.createInputPin('direction', 'VectorPin',FreeCAD.Vector(0,0,1))
        p=self.createInputPin('pointCount', 'IntPin',20)
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

    def __init__(self, name="MyCompound"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.shapeout = self.createOutputPin('Shape_out', 'ShapePin')


        #self.shapes=self.createInputPin('Shapes', 'AnyPin', None,  supportedPinDataTypes=["ShapePin", "FCobjPin"])
        self.shapes=self.createInputPin('Shapes', 'ShapePin', None)
        self.shapes.enableOptions(PinOptions.AllowMultipleConnections)
        self.shapes.disableOptions(PinOptions.SupportsOnlyArrays)

#        p=self.createInputPin('ShapeList', 'ShapeListPin', [])
#        p.enableOptions(PinOptions.AllowMultipleConnections)
#        p.disableOptions(PinOptions.SupportsOnlyArrays)
#        p.recomputeNode=True




    @staticmethod
    def description():
        return FreeCAD_Compound.__doc__

    @staticmethod
    def category():
        return 'Combination'

    @staticmethod
    def keywords():
        return ['Group:','Part']



class FreeCAD_Plot(NodeBase):
    '''
    dummy for tests
    '''

    def __init__(self, name="MyPlot"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')

        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin')

        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)

        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True

        self.xpin=self.createInputPin('x', 'FloatPin', structure=StructureType.Array)
        self.ypin=self.createInputPin('y', 'FloatPin', structure=StructureType.Array)

        self.xpin2=self.createInputPin('x2', 'FloatPin', structure=StructureType.Array)
        self.ypin2=self.createInputPin('y2', 'FloatPin', structure=StructureType.Array)

        self.f2=self.createInputPin('Figure2', 'BoolPin')
        self.f3=self.createInputPin('Figure3', 'BoolPin')

    def compute(self, *args, **kwargs):

        sayl()

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_Plot_compute(self,*args, **kwargs)

        self.outExec.call()

        if self._preview:
            self.preview()


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
    select a part or some subobjects oof the same object. than a node with pins for all
    these selected details is created
    '''

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

    dok = 2
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

    @timer
    def Xcompute(self, *args, **kwargs):

        name=self.getData('name')
        Shape=self.getPinObject('Shape_in')
        workspace=self.getData('Workspace')
        mode='1'
        wireframe=False
        transparency=50
        #+#todo make the parameters to pins

        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_view3d(self,name,Shape,workspace,mode,wireframe,transparency)

        self.outExec.call()

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


class FreeCAD_Blinker(FreeCadNodeBase):
    '''
    blinker sender
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


    @staticmethod
    def description():
        return FreeCAD_Blinker.__doc__

    @staticmethod
    def category():
        return 'Signal'

    @staticmethod
    def keywords():
        return ['Sender']


class FreeCAD_Receiver(FreeCadNodeBase):
    '''
    blinker receiver
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')


    @staticmethod
    def description():
        return FreeCAD_Receiver.__doc__

    @staticmethod
    def category():
        return 'Signale'

    @staticmethod
    def keywords():
        return ['Receiver']







def nodelist():
    return [
#                FreeCAD_Foo,
#                FreeCAD_Toy,
#               FreeCAD_Bar,
                FreeCAD_Object,
                FreeCAD_Box,
                FreeCAD_Cone,
                FreeCAD_Sphere,
                FreeCAD_Quadrangle,
#                FreeCAD_Polygon,
                FreeCAD_Polygon2,
#                FreeCAD_Array,
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
#                FreeCAD_Part,
                FreeCAD_Ref,
                FreeCAD_RefList,
                FreeCAD_LOD,
                FreeCAD_view3D,
                FreeCAD_Destruct_Shape,
                FreeCAD_bakery,
                FreeCAD_topo,
                FreeCAD_conny,
                FreeCAD_randomizePolygon,
                
                FreeCAD_Blinker,
                FreeCAD_Receiver,
                
        ]
