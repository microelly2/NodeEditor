#import FreeCAD

from nodeeditor.say import *

#import json

from PyFlow.Core import PinBase
#from PyFlow.Core.Common import *

import nodeeditor.store as store


class FCobjPin(PinBase):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        #super(FCobjPin, self).__init__(name, parent, direction, **kwargs)
        super(FCobjPin, self).__init__(name, parent, direction,)
        self.setDefaultValue(None)

    def __repr__(self):

        return "[{0}:{1}: Data:{2}]".format(self.dataType, self.name,  self.currentData())

    def getName(self):
        return "self.name NIP"

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('FCobjPin','ShapePin','FacePin','EdgePin',None)
        return ('FCobjPin',None)

    @staticmethod
    def color():
        return (150, 150, 250, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FCobjPin', None

    @staticmethod
    def internalDataStructure():
        return object

    @staticmethod
    def processData(data):
        return data


    def getObject(self):
        arrin=self.getData()
        if arrin  !=  None:
            s=FreeCAD.ActiveDocument.getObject(arrin)
            return s
        else:
            return None

class FunctionId():
    pass

class FunctionPin(FCobjPin):

    """doc string for """

    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName(),direction)
        super(FunctionPin, self).__init__(name, parent, direction)
        self.setDefaultValue(None)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('FunctionPin','ShapePin')

    @staticmethod
    def color():
        return (90, 90, 250, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FunctionPin', None

    @staticmethod
    def internalDataStructure():
        return FunctionId

    @staticmethod
    def processData(data):
        return data





class ShapeId():
    pass

class ShapePin(FCobjPin):
#class ShapePin(PinBase):

    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName(),direction)
        super(ShapePin, self).__init__(name, parent, direction)
        self.setDefaultValue(None)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ShapePin','FacePin','EdgePin')

    @staticmethod
    def color():
        return (250, 50, 50, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'ShapePin', None

    @staticmethod
    def internalDataStructure():
        return ShapeId

    @staticmethod
    def processData(data):
        return data

class FaceId():
    pass

class FacePin(ShapePin):
    """doc string for FloatFCobjPin"""

    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName(),direction)
        super(FacePin, self).__init__(name, parent, direction)
        self.setDefaultValue(None)

    @staticmethod
    def supportedDataTypes():
        return ('FacePin',)

    @staticmethod
    def color():
        return (250, 150, 150, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FacePin', None

    @staticmethod
    def internalDataStructure():
        return FaceId


class EdgeId():
    pass

class EdgePin(ShapePin):
    """doc string for FloatFCobjPin"""

    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName(),direction)
        super(EdgePin, self).__init__(name, parent, direction)
        self.setDefaultValue(None)

    @staticmethod
    def supportedDataTypes():
        return ('EdgePin',)

    @staticmethod
    def color():
        return (250, 250, 150, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'EdgePin', None

    @staticmethod
    def internalDataStructure():
        return EdgeId



class ShapeListId():
    pass

class ShapeListPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName())
        super(ShapeListPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(None)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ShapeListPin',None)

    @staticmethod
    def color():
        return (100, 200, 100, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'ShapeListPin', None

    @staticmethod
    def internalDataStructure():
        return ShapeListId

    @staticmethod
    def processData(data):
        return data




class Array():
    pass


class ArrayPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(ArrayPin, self).__init__(name, parent, direction, **kwargs)


    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ArrayPin',None)

    @staticmethod
    def color():
        return (150, 150, 150, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'ArrayPin', None

    @staticmethod
    def internalDataStructure():
        return Array

    @staticmethod
    def processData(data):
        return data

    def getArray(self):
        #say("getArray method")
        arrin=self.getData()
        #say("got key:",arrin)
        if arrin  !=  None:
            s=store.store().get(arrin)
            return s
        else:
            return None

    def setArray(self,array):
        store.store().add(str(self.uid),array)
        self.setData(str(self.uid))





class Transformation():
    pass


class TransformationPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(TransformationPin, self).__init__(name, parent, direction, **kwargs)


    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('TransformationPin',None)

    @staticmethod
    def color():
        return (0, 250, 250, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'TransformationPin', None

    @staticmethod
    def internalDataStructure():
        return Transformation

    @staticmethod
    def processData(data):
        return data

    def getTransformation(self):
        #say("getTransformation method")
        arrin=self.getData()
        #say("got key:",arrin)
        if arrin  !=  None:
            s=store.store().get(arrin)
            return s
        else:
            return None

    def setTransformation(self,Transformation):
        store.store().add(str(self.uid),Transformation)
        self.setData(str(self.uid))





from PyFlow.Core import PinBase
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Pins.BoolPin import BoolPin
from PyFlow.Packages.PyFlowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyFlowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyFlowBase.Pins.StringPin import StringPin

class IntegerD(int):
    pass

class BooleanD():
    pass

class StringD(str):
    pass
class FloatD(float):
    pass

# generalised data setter
def setDataG(self,data):
    super(self.__class__, self).setData(data)
    try:
        if  self.direction == PinDirection.Input and not self.hasConnections():
            self.owningNode().compute()
    except:
        pass


class String(StringPin):
    """String pin with dialog autoupdate """

    @staticmethod
    def supportedDataTypes():
        return ('StringPin','String')

    @staticmethod
    def internalDataStructure():
        return StringD

    @staticmethod
    def processData(data):
        return StringD(data)

    def setData(self, data):
        setDataG(self, data)


class Boolean(BoolPin):
    """String pin with dialog autoupdate """

    @staticmethod
    def supportedDataTypes():
        return ('BoolPin', 'Boolean','IntPin','Integer')

    @staticmethod
    def internalDataStructure():
        return BooleanD

    @staticmethod
    def processData(data):
        return bool(data)

    def setData(self, data):
        setDataG(self, data)

class Integer(IntPin):
    """Integer pin with dialog autoupdate """

    @staticmethod
    def supportedDataTypes():
        return ('FloatPin', 'IntPin','Float','Integer')

    @staticmethod
    def internalDataStructure():
        return IntegerD

    @staticmethod
    def processData(data):
        return IntegerD(data)

    def setData(self, data):
        setDataG(self, data)


class Float(FloatPin):
    """Float pin with dialog autoupdate """

    @staticmethod
    def pinDataTypeHint():
        '''data type index and default value'''
        return 'FloatPin', 0.0

    @staticmethod
    def supportedDataTypes():
        return ('FloatPin', 'IntPin','Float','Integer')



    @staticmethod
    def internalDataStructure():
        return FloatD

    @staticmethod
    def processData(data):
        return FloatD(data)

    def setData(self, data):
        setDataG(self, data)

       



def nodelist():
    pins = [ShapePin,FacePin,EdgePin,ShapeListPin,FCobjPin,ArrayPin,TransformationPin ]
    pins += [Integer,Float,Boolean,String]
    pins += [FunctionPin]
    return pins
