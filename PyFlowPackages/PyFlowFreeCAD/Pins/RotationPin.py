from FreeCAD import Rotation
from nodeeditor.say import *
import FreeCAD

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *

class MRotation(Rotation):
    
    def __init__(self, *args,**kvargs):
        say("MRotation kv",kvargs)
        say("MRO args",args)
        super(MRotation, self).__init__(*args,**kvargs)
        say("MRotation ---------------- done")
    pass

class RotationEncoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Rotation):
            return {Rotation.__name__: vec3.toEuler()}
        json.JSONEncoder.default(self, vec3.toEuler())


class RotationDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(RotationDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Rotation(*vec3Dict[Rotation.__name__])


class RotationPin(PinBase):
    """doc string for FloatRotationPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(RotationPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue([0,0,0])

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('RotationPin',)

    @staticmethod
    def color():
        return (200, 50, 50, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'RotationPin', list(Rotation(0,0,0).toEuler())

    @staticmethod
    def jsonEncoderClass():
        return RotationEncoder

    @staticmethod
    def jsonDecoderClass():
        return RotationDecoder

    @staticmethod
    def internalDataStructure():
        return MRotation

    @staticmethod
    def processData(data):
        return RotationPin.internalDataStructure()(data)
