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


def run_FreeCAD_Offset(self,produce=False, **kwargs):
    #sayl()
    count=self.getData("count")
    edge=self.getPinObject("Wire")
    say(edge)
    if edge is None: return
    pts=edge.discretize(count*10)
    # Part.show(Part.makePolygon(pts))
    face=self.getPinObject("Shape")
    sf=face.Surface
    r=self.getData("offset")*20
    pts2=[]
    pts3=[]
    pts4=[]
    pts5=[]
    #r2=self.getData("height")*20
    r2=100
    
    for i in range(len(pts)-1):
        p=pts[i]
        u,v=sf.parameter(p)
        say(u,v)
        t=(pts[i+1]-p).normalize()
        say(t)
        n=sf.normal(u,v)
        say(n)
        u,v=sf.parameter(p+n.cross(t)*r)
        pts2 += [sf.value(u,v)]
        u,v=sf.parameter(p-n.cross(t)*r)
        pts3 += [sf.value(u,v)]
        pts4 += [p+n*r2]
        pts5 += [p-n*r2]
    closed=True
    closed=False
    if closed:
        pol2=Part.makePolygon(pts2+[pts2[0]])
        pol3=Part.makePolygon(pts3+[pts3[0]])
        pol4=Part.makePolygon(pts4+[pts4[0]])
    else:
        pol2=Part.makePolygon(pts2)
        pol3=Part.makePolygon(pts3)
        pol4=Part.makePolygon(pts4)
    if produce:
            Part.show(pol2)
            Part.show(pol3)
            Part.show(pol4)

    sfa=Part.BSplineSurface()
    
    poles=np.array([pts2,pts4,pts3])

    countB=len(pts2)
    countA=3
    degA=2
    degB=3
    if closed==False:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multA=[degA]+[1]*(countA-degA)+[degA]
        
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,True,False,degA,degB)
    else:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multB=[degB]+[1]*(countB-degB)+[degB]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,True,degA,degB)

    if 10:
        poles=np.array([pts2,pts4,pts3,pts5])
        countA=4

        poles=np.array([pts2,pts2,pts4,pts3,pts3])
        countA=5
        
        multA=[degA]+[1]*(countA-degA)+[degA]
        multB=[degB]+[1]*(countB-degB)+[degB]
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,True,False,degA,degB)


    Part.show(sfa.toShape())



    self.setPinObject("Shape_out",Part.Compound([pol2,pol3,pol4]))

