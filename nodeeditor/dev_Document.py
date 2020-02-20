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





def run_FreeCAD_Solid(self,bake=False, **kwargs):
    
    #shapes=self.getData("Shapes")
    #say(shapes)
    #return
    
    yPins = self.getPinByName("Shapes").affected_by
    
    outArray=[]
    for pin in yPins:
        k=str(pin.uid)
        d=store.store().get(k)
#       say(d)
        outArray.append(d)
    say(outArray)
    
    shapes=outArray
    say(shapes)

    colf=shapes

    

    for tol in range(1000):
        colf2=[c.copy() for c in colf]
        try:
            #say ("try tolerance",tol)
            for f in colf2:
                f.Tolerance=tol
            sh=Part.Shell(colf2)

            sol=Part.Solid(sh)
            say (sol.isValid())
            if sol.isValid():
                say("solid created with tol",tol)
                if bake:
                    Part.show(sol)
                #cc=self.getObject();cc.Shape=sol
                
                self.setPinObject("Shape_out",sol)
                break
        except:
            pass


