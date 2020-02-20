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



def run_FreeCAD_Index(self):
    vecs=self.getData("list")
    ix=self.getData('index')
    if ix<len(vecs):
        self.setData("item",vecs[ix])
    else:
        sayErr("index not valid")



def run_FreeCAD_Repeat(self):
    
    s=self.getData("in")
    #say(s)
    count=self.getData("count")
    #say('##')
    t=[s]*count
    #say(t)
    self.setData("out",t)
    #self.setData("Shapes",[s]*count)

    sayl()

  
  
