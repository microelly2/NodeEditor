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




     
def run_FreeCAD_Export(self):
        
    a=self.getPinObject("Shape")
    if a is None:
        sayErOb(self,"no Shape")
        return
    fn=self.getData("filename")
    mode=self.getData('mode')
    if mode=='BREP':
        a.exportBrep(fn)
    elif  mode=='STEP':
        a.exportStep("/tmp/a.step")
    elif  mode=='Inventor':
        fn="/tmp/a.iv"
        s=a.writeInventor()   
        f= open(fn,"w+")
        f.write(s)
        f.close()
    
    
def run_FreeCAD_Import(self):
    
    fn=self.getData("filename")
    a=Part.Shape()
    #a.importBrep(fn)
    
    mode=self.getData('mode')
    if mode=='BREP':
        a.importBrep(fn)
    elif  mode=='STEP':
        a.importStep(fn)


    self.setPinObject("Shape_out",a)
    
   
