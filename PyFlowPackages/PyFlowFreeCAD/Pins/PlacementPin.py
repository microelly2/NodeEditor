from FreeCAD import Placement
from nodeeditor.say import *

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class PlacementEncoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Placement):
            return {Placement.__name__: []}
        json.JSONEncoder.default(self, vec3)


class PlacementDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(PlacementDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Placement()
        #return Placement(vec3Dict[Placement.__name__])


class PlacementPin(PinBase):
    """doc string for FloatPlacementPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(PlacementPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Placement())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('PlacementPin',)

    @staticmethod
    def color():
        return (170, 100, 200, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatPlacementPin', Placement()

    @staticmethod
    def jsonEncoderClass():
        return PlacementEncoder

    @staticmethod
    def jsonDecoderClass():
        return PlacementDecoder

    @staticmethod
    def internalDataStructure():
        return Placement

    @staticmethod
    def processData(data):
        return PlacementPin.internalDataStructure()(data)
