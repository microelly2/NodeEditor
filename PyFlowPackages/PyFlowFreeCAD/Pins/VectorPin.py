#from pyrr import Vector
from FreeCAD import Vector

#from nodeeditor.wrapper import MVector as Vector

from nodeeditor.say import *

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class VectorEncoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Vector):
            return {Vector.__name__: [vec3.x,vec3.y,vec3.z]}
        json.JSONEncoder.default(self, vec3)


class VectorDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(VectorDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Vector(vec3Dict[Vector.__name__])


class VectorPin(PinBase):
    """doc string for FloatVectorPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(VectorPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Vector(7,2,3))

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('VectorPin',)

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatVectorPin', Vector()

    @staticmethod
    def jsonEncoderClass():
        return VectorEncoder

    @staticmethod
    def jsonDecoderClass():
        return VectorDecoder

    @staticmethod
    def internalDataStructure():
        return Vector

    @staticmethod
    def processData(data):
        return VectorPin.internalDataStructure()(data)
