'''

'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase, FreeCadNodeBase2







class FreeCAD_ShapeIndex(FreeCadNodeBase2):
    '''
    selection of a shape by its index in a list of shapes
    '''


    dok=3
    def __init__(self, name="MyShapeIndex"):
        super(self.__class__, self).__init__(name)


        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

#        self.objname = self.createInputPin("objectname", 'String')
#        self.objname.setData(name)


        p=self.createInputPin('Shapes', 'ShapeListPin')
        p.description="list of shapes #+#"
        p=self.createInputPin('index', 'Integer')
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




class FreeCAD_Face(FreeCadNodeBase2):
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

        a=self.createInputPin('sourceObject', 'String')
        a.description="name of the FreeCAD object from which the face should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with faces"
        p=self.createInputPin('index', 'Integer')
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



class FreeCAD_Edge(FreeCadNodeBase2):
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


        a=self.createInputPin('sourceObject', 'String')
        a.description="name of the FreeCAD object from which the edge should be selected"
        a=self.createInputPin('Shape_in', 'ShapePin')
        a.description="optional shape with edges"
        p=self.createInputPin('index', 'Integer')
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





class FreeCAD_Destruct_Shape(FreeCadNodeBase2):
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


        a=self.createInputPin('sourceObject', 'String')
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



