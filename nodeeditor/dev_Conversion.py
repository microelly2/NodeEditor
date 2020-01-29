# implemenation of the compute methods for category Conversion

import numpy as np
import random
import time
import os.path
from os import path
import matplotlib.pyplot as plt
import scipy.interpolate

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.pfwrap as pfwrap

from pivy import coin

print ("reloaded: "+ __file__)


def run_FreeCAD_ListOfVectorlist(self):

	ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
	col=[]
	for i in ySortedPins:
		# hack to get current values #+# todo debug
		i.owningNode().compute()
		vv=i.owningNode().getData(i.name)
		col +=[vv]
	say("shape result",np.array(col).shape)
	self.setData('vectorarray',col)
    
