from FreeCAD import Rotation
from nodeeditor.say import *
import FreeCAD

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class RotationEncoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Rotation):
            return {Rotation.__name__: []}
        json.JSONEncoder.default(self, vec3)


class RotationDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(RotationDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Rotation()
        #return Rotation(vec3Dict[Rotation.__name__])


class RotationPin(PinBase):
    """doc string for FloatRotationPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(RotationPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(FreeCAD.Rotation())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('RotationPin',)

    @staticmethod
    def color():
        return (170, 100, 200, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'RotationPin', Rotation()

    @staticmethod
    def jsonEncoderClass():
        return RotationEncoder

    @staticmethod
    def jsonDecoderClass():
        return RotationDecoder

    @staticmethod
    def internalDataStructure():
        return Rotation

    @staticmethod
    def processData(data):
        return RotationPin.internalDataStructure()(data)
