# implemenation of the compute methods for category 

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


print ("reloaded: "+ __file__)



from nodeeditor.cointools import *



def run_FreeCAD_FillEdge(self,produce=False, **kwargs):
   
    return #+# muss mparametriz werden
    wire=FreeCAD.ActiveDocument.BePlane.Shape.Wires[0]
    #_=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Shape004.Shape.Edge2, ]))
    _=Part.makeFilledFace(wire.Edges)
    Part.show(_)
    
