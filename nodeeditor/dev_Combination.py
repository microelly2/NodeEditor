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



def run_FreeCAD_Compound(self, *args, **kwargs):

        #+# todo ShapesList implementieren
#        try:
#            subshapes=self.getPinObjects("Shapes")
#        except:
#            subshapes=[]
#        try:
#            subshapes += self.getPinObjects("ShapeList")
#        except:
#            pass

        # get list of nodes
        outArray = []
        ySortedPins = sorted(self.shapes.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            outArray.append(i.owningNode().getPinObject(i.name))
        

#-----------------


        say("Compound Shapes:",outArray)
        shape=Part.Compound(outArray)

        self.setPinObject("Shape_out",shape)
    

    
    
def run_FreeCAD_RepeatPattern(self):

    b=self.getData("pattern")
    apts=self.getData("vectors")

    a=np.array(apts)

    # make the vectors array flat
    if len(np.array(a).shape)>1:
        ll=np.array(a).shape
        a=np.array(a).reshape(np.prod(ll[:-1]),3)

    a=[FreeCAD.Vector(v.tolist()) for v in a]
    c=[[av+bv for bv in b] for av in a]

    col=[]
    for pts in c:
        col +=[Part.makePolygon(pts)]

    cc=Part.Compound(col)

    self.setData("pattern_out",c)
    self.setPinObject("Shape_out",cc)
    self.setColor(a=0.7)
    
