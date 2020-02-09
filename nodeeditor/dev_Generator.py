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



def run_FreeCAD_VectorArray(self,*args, **kwargs):

    countA=self.getData("countA")
    countB=self.getData("countB")
    countC=self.getData("countC")
    vO=self.getData("vecBase")
    vA=self.getData("vecA")

    vB=self.getData("vecB")
    vC=self.getData("vecC")
    rx=self.getData("randomX")
    ry=self.getData("randomY")
    rz=self.getData("randomZ")


    degA=self.getData("degreeA")
    degB=self.getData("degreeB")
    if countA<degA+1:
        degA=countA-1
    if countB<degB+1:
        degB=countB-1

    points=[vO+vA*a+vB*b+vC*c+FreeCAD.Vector((0.5-random.random())*rx,(0.5-random.random())*ry,(0.5-random.random())*rz)
        for a in range(countA) for b in range(countB) for c in range(countC)]

    if countC != 1:
        sayexc("not implemented")
        return

    if degA==0 or degB==0:
        col = []
        poles=np.array(points).reshape(countA,countB,3)
        for ps in poles:
            ps=[FreeCAD.Vector(p) for p in ps]
            col += [Part.makePolygon(ps)]
        for ps in poles.swapaxes(0,1):
            ps=[FreeCAD.Vector(p) for p in ps]
            col += [Part.makePolygon(ps)]

        shape=Part.makeCompound(col)


    else:

        poles=np.array(points).reshape(countA,countB,3)

        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sf=Part.BSplineSurface()
        sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
        shape=sf.toShape()


    self.setData('vectors_out',poles.tolist())

    #cc=self.getObject()
    #try:
    #    cc.Label=self.objname.getData()
    #except:
    #    pass
    #cc.Shape=shape
    self.setPinObject('Shape_out',shape)
    #Beispiel Nodename setzen
    #self.setNodename("HUHU")
    
    # Fehler setzen
    #self.setError("raise Exception")
    


