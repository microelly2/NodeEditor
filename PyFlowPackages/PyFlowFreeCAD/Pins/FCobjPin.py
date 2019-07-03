import FreeCAD

from nodeeditor.say import *

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *

class FCobj(object):
#    def getObject(self,*args):
 #       say("getobject")
  #      return self
    pass

class FCobjEncoder(json.JSONEncoder):
    def default(self, vec3):
        if vec3==None:
            return {FCobj.__name__: None}
        else:
            return {FCobj.__name__: vec3.Name}
        json.JSONEncoder.default(self, vec3)


class FCobjDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(FCobjDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        print "hook", vec3Dict
        if vec3Dict[FCobj.__name__] == None:
            return None
        else:
            return FreeCAD.ActiveDocument.getObject(vec3Dict[FCobj.__name__])


class FCobjPin(PinBase):
    """doc string for FloatFCobjPin"""
    def __init__(self, name, parent, direction, **kwargs):
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
    def jsonEncoderClass():
        return FCobjEncoder

    @staticmethod
    def jsonDecoderClass():
        return FCobjDecoder

    @staticmethod
    def internalDataStructure():
        return FCobj

    @staticmethod
    def processData(data):
        print ("FCobj Pin Processing send data:",data)
        return data
