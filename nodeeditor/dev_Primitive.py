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


print ("reloaded: "+ __file__)


import nodeeditor
import nodeeditor.cointools
#reload(nodeeditor.cointools)
from nodeeditor.cointools import *

from nodeeditor.utils import *
import nodeeditor.tools as noto
#reload(noto)
    


def run_FreeCAD_Simplex(self,*args, **kwargs):

    k=self.getData("noise")
    say("kkk",k)

    def rav(v):
        '''add a random vector to a vector'''
        return v+FreeCAD.Vector(0.5-random.random(),0.5-random.random(),0.5-random.random())*k


    sayl()
    a=self.getData("pointA")
    b=self.getData("pointB")
    c=self.getData("pointC")
    d=self.getData("pointD")
    say(a,b,c,d)
    colf=[]
    wire=Part.makePolygon([a,rav(b),rav(c),a])
    colf += [Part.Face(wire)]
    
    wire=Part.makePolygon([a,rav(b),rav(d),a])
    colf += [Part.Face(wire)]

    wire=Part.makePolygon([a,rav(c),rav(d),a])
    colf += [Part.Face(wire)]

    wire=Part.makePolygon([c,rav(b),rav(d),c])
    colf += [Part.Face(wire)]

    #Part.show(Part.Compound(colf))
    self.setPinObject("Compound_out",Part.Compound(colf))

    for tol in range(100):
        colf2=[c.copy() for c in colf]
        try:
            # say ("try tolerance",tol)
            for f in colf2:
                f.Tolerance=tol
            sh=Part.Shell(colf2)
            sol=Part.Solid(sh)
            say (sol.isValid())
            if sol.isValid():
                say("solid created with tol",tol)
                #Part.show(sol)
                #cc=self.getObject();cc.Shape=sol
                
                self.setPinObject("Shape_out",sol)
                break
        except:
            pass



def run_FreeCAD_BSplineSurface(self, *args, **kwargs):

        
        data=self.getPinDataYsorted('poles')
        if len(data)==0:
            sayErOb(self,"no poles given")
            return
           
        for d in data:
            say("!",np.array(d).shape)
        dat=np.concatenate(data)
        say(np.array(dat).shape)       
        
        if len(dat) == 0:
            sayW("no points for poles")
            return
        dat=np.array(dat)
        sf=Part.BSplineSurface()

        poles=np.array(dat)

        (countA,countB,_)=poles.shape
        degB=min(countB-1,3,self.getPinByName("maxDegreeU").getData())
        degA=min(countA-1,3,self.getPinByName("maxDegreeV").getData())
        
        periodicU=self.getData("periodicU")
        
        periodicV=self.getData("periodicV")
        if periodicU:
            multA=[1]*(countA+1)
            knotA=range(len(multA))
        else:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))

        if periodicV:
            multB=[1]*(countB+1)
            knotB=range(len(multB))
        else:
            multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]       
            knotB=range(len(multB))


        sf=Part.BSplineSurface()
        sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,periodicU,periodicV,degA,degB)
        shape=sf.toShape()

        self.setPinObject("Shape_out",shape)
    



def run_FreeCAD_BSplineCurve(self, *args, **kwargs):

        dat=self.arrayData.getData()
        if len(dat)==0:             return
        dat=np.array(dat)
        sf=Part.BSplineCurve()

        poles=np.array(dat)

        (countA,_)=poles.shape
        degA=min(countA-1,13,self.getPinByName("maxDegree").getData())

        periodic=self.getData("periodic")
        #periodic=True
        if not periodic:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))

        else:
            multA=[1]*(countA+1)
            knotA=range(len(multA))

            
        sf=Part.BSplineCurve()
        sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)
        shape=sf.toShape()


        shape=sf.toShape()
        
        #cc=self.getObject()
        #cc.Label=self.objname.getData()
        #cc.Shape=shape

        self.setPinObject("Shape_out",shape)
    
    

def run_FreeCAD_Polygon(self):
    
            # recursion stopper
        if self.Called:
            return
        #sayl()
        # mit zeitstemple aktivieren
        #self.Called=True

        pts=self.points.getData()
        #say(pts)
        if pts[0].__class__.__name__ == 'list':
            pts=pts[0]
        say("--")
        if len(pts)<2:
            sayW("zu wenig points")
        else:
            try:
                shape=Part.makePolygon(pts)
            except:
                return

        self.setPinObject("Shape_out",shape)

        if self._preview:
            self.preview()

        #self.Called=False
