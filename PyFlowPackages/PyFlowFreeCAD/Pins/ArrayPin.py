import numpy as np

class Array(object):
	def __init__(self,dat=[]):
		self.dat=np.array(dat)


from nodeeditor.say import *

import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class ArrayEncoder(json.JSONEncoder):
    def default(self, vec3):
        if isinstance(vec3, Array):
            return {Array.__name__: vec3.dat}
        json.JSONEncoder.default(self, vec3)


class ArrayDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(ArrayDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Array(vec3Dict[Array.__name__])


class ArrayPin(PinBase):
    """doc string for FloatArrayPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(ArrayPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(Array([1,2,3]))

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('ArrayPin',)

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'FloatArrayPin', Array()

    @staticmethod
    def jsonEncoderClass():
        return ArrayEncoder

    @staticmethod
    def jsonDecoderClass():
        return ArrayDecoder

    @staticmethod
    def internalDataStructure():
        return Array

    @staticmethod
    def processData(data):
        return ArrayPin.internalDataStructure()(data)
