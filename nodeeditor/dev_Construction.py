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

def run_FreeCAD_Reduce(self):

    flags=self.getData("selection")
    eids=self.getData("shapes")
    say(self.name)
    if eids is None:
        return
    shapes=[store.store().get(eid)  for eid in eids]
    reduced=[]
    for f,s in zip(shapes,flags):
        if s:
             reduced += [f]
    try:
        rc=Part.Compound(reduced)
    except:
       rc=Part.Shape()
    say("!!rc=",rc)
    self.setPinObject("Shape_out",rc)
    self.setColor(b=0,a=0.4)
    

    
def run_FreeCAD_Tube(self):
    #+# todo better normal for 3d curve
    floats=self.getData('parameter')
    radius=self.getData('radius')

    cc=self.getPinObject("backbone")
    if cc is None:
        say("no backbone curve abort")
        return
    say("expected parameter range", cc.ParameterRange)
    curve=cc.Curve
    pts=[]
    for f,r  in zip(floats,radius):
        f *= 0.1
        r *= 0.1
        p=curve.value(f)
        t=curve.tangent(f)[0]
        if 0:
            h=FreeCAD.Vector(0,0,1)
            n=t.cross(h)
        else:
            n=curve.normal(f)
            h=n.cross(t)
            
        pts += [[p-h*r,p+n*r,p+h*r,p-n*r]]
    
    # aufrichten normale
    z=pts[0]
    pts2 =[z]
    for i in range(len(pts)-1):
        a=z
        b=pts[i+1]
        sums=[]
        for j in range(4):
            sums +=[sum([(a[k-j]-b[k]).Length for k in range(4)])]
        say(sums.index(min(sums)))
        index=sums.index(min(sums))
        z=b[index:]+b[:index]
        pts2 += [z]
        
    self.setData("points",pts2)
    

