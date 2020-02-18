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


# is in dragger.py !!

def run_FreeCAD_Collect_Vectors(self, mode=None):
    #say("collect",mode)
    if mode=="reset":
        self.points=[]
        return


    maxSize=self.getData("maxSize")
    red=self.getData("reduce")
    point = self.getData("point")
    try:
        if (self.points[-1]-point).Length <0.01:
#           say("zu dicht")
            return
    except:
        pass

    # point.y *= -1.

    self.points += [point]
    #say(len(self.points))
    if maxSize >0 and len(self.points)>maxSize:
            self.points = self.points[len(self.points)-maxSize:]
    if len(self.points)>2 and red>2:
        pol=Part.makePolygon(self.points)
        pointsd=pol.discretize(red)
    else:
        pointsd=self.points
    self.setData("points",pointsd)
    #say(len(self.points),len(pointsd))
    if not self.inRefresh.hasConnections():
        self.outExec.call()

