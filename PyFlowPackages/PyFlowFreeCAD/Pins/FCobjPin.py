#import FreeCAD

from nodeeditor.say import *

#import json

from PyFlow.Core import PinBase
#from PyFlow.Core.Common import *

#import nodeeditor.store as store


'''
class FCobjEncoder(json.JSONEncoder):
    def default(self, vec3):
        say("fc decoder")
        if vec3==None:
            return {FCobj.__name__: None}
        else:
            store.store().addid(vec3.Name,vec3)
            return {FCobj.__name__: vec3.Name}
        json.JSONEncoder.default(self, vec3)


class FCobjDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        say("init fco decode")
        super(FCobjDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        say("fc obj hook-----------------")
        say(vec3Dict)
        if vec3Dict[FCobj.__name__] == None:
            return None
        else:
            return store.store().get(vec3Dict[FCobj.__name__])
            return FreeCAD.ActiveDocument.getObject(vec3Dict[FCobj.__name__])
'''

class FCobjPin(PinBase):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName())
        super(FCobjPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(None)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('FCobjPin',None)

    @staticmethod
    def color():
        return (150, 0, 0, 255)

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

class ShapeId():
    pass

class ShapePin(FCobjPin):
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
        return ('ShapePin',None)

    @staticmethod
    def color():
        return (150, 0, 0, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'ShapePin', None

    @staticmethod
    def internalDataStructure():
        return ShapeId

    @staticmethod
    def processData(data):
        #say("FCobj Pin Processing send data!:",data,data.__class__.__name__)
        #return FCobjPin.internalDataStructure()(data)
        return data

class EnumSelection():
    pass


class EnumerationPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        #say("create pin",name,parent.getName())
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
        #say("FCobj Pin Processing send data!:",data,data.__class__.__name__)
        #return FCobjPin.internalDataStructure()(data)
        return data


class Array():
    pass

import nodeeditor.store as store


class ArrayPin(FCobjPin):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
        say("create pin",name,parent.getName())
        super(ArrayPin, self).__init__(name, parent, direction, **kwargs)
#        self.values=["tic","tac","toe"]
 #       self.setDefaultValue([4,5,6,8])
  #      FreeCAD.pin=self




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
        #say("FCobj Pin Processing send data!:",data,data.__class__.__name__)
        #return FCobjPin.internalDataStructure()(data)
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
    return [EnumerationPin,ShapePin,FCobjPin,ArrayPin]
