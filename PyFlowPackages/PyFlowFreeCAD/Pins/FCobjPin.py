#import FreeCAD

from nodeeditor.say import *

#import json

from PyFlow.Core import PinBase
#from PyFlow.Core.Common import *

import nodeeditor.store as store


class FCobjPin(PinBase):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(FCobjPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(None)

    def __repr__(self):
        return "[{0}:{1}: Data:{2}]".format(self.dataType, self.getName(),  self.currentData())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
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
        #say("FCobj Pin Processing send data!:",data,data.__class__.__name__)
        #return FCobjPin.internalDataStructure()(data)
        return data


    def getObject(self):
        arrin=self.getData()
        if arrin <> None:
            s=FreeCAD.ActiveDocument.getObject(arrin)
            return s
        else:
            return None



class ShapeId():
    pass

class ShapePin(FCobjPin):
#class ShapePin(PinBase):

    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        say("create pin",name,parent.getName())
        super(ShapePin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(None)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ShapePin',)

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



class ShapeListId():
    pass

class ShapeListPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        say("create pin",name,parent.getName())
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


class EnumSelection():
    pass


class EnumerationPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(EnumerationPin, self).__init__(name, parent, direction, **kwargs)
        self.values=["tic","tac","toe"]
        self.setDefaultValue(self.values[0])

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ShapePin',None)

    @staticmethod
    def color():
        return (150, 150, 0, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'EnumerationPin', None

    @staticmethod
    def internalDataStructure():
        return EnumSelection

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
        #say("getArray methode")
        arrin=self.getData()
        #say("got key:",arrin)
        if arrin <> None:
            s=store.store().get(arrin)
            return s
        else:
            return None

    def setArray(self,array):
        #if self.hasConnections():
        #say("to store ",array)
        #say("key",str(self.uid))
        store.store().add(str(self.uid),array)
        self.setData(str(self.uid))





def nodelist():
    return [EnumerationPin,ShapePin,ShapeListPin,FCobjPin,ArrayPin]
