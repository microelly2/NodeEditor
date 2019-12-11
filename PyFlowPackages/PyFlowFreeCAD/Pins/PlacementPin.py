from FreeCAD import Placement
from nodeeditor.say import *

class MPlacement(Placement):
    pass

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class PlacementEncoder(json.JSONEncoder):
    def default(self, vec3):
        
        if isinstance(vec3, Placement):
            return {Placement.__name__: list(vec3.toMatrix().A)}
        return {Placement.__name__: list(vec3.toMatrix().A)}
        json.JSONEncoder.default(self, vec3)


class PlacementDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(PlacementDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return vec3Dict[Placement.__name__]
        return Placement(*vec3Dict[Placement.__name__])


class PlacementPin(PinBase):
    """doc string for FloatPlacementPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(PlacementPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue([])

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
        return 'PlacementPin', []

    @staticmethod
    def jsonEncoderClass():
        return PlacementEncoder

    @staticmethod
    def jsonDecoderClass():
        return PlacementDecoder

    @staticmethod
    def internalDataStructure():
        return MPlacement

    @staticmethod
    def processData(data):
        return PlacementPin.internalDataStructure()(data)


    def getPlacement(self):
        #say("getTransformation method")
        arrin=self.getData()
        say("got key:",arrin)
        pm=FreeCAD.Placement(FreeCAD.Matrix(*arrin))
        say(pm)
        return(pm)
        
        if arrin  !=  None:
            s=store.store().get(arrin)
            return s
        else:
            return None

    def setPlacement(self,placement):
        #store.store().add(str(self.uid),Transformation)
        say("set --",placement)
        self.setData(list(str(placement.toMatrix().A)))

