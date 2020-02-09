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
    


def run_FreeCAD_Discretize(self,*args, **kwargs):
    sayl()
    count=self.getData("count")
    edge=self.getPinObject("Wire")
    say(edge)
    if edge is None: return
    ptsa=edge.discretize(count)

    self.setPinObject("Shape_out",Part.makePolygon(ptsa))
    if 0:
        sc=Part.BSplineCurve()
        sc.buildFromPoles(ptsa)
        self.setPinObject("Shape_out",sc.toShape())
    

    return

    pts=edge.discretize(count*10)
    #Part.show(Part.makePolygon(pts))
    face=FreeCAD.ActiveDocument.BePlane.Shape.Face1
    sf=face.Surface
    r=200
    pts2=[]
    pts3=[]
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
    closed=True
    if 0:
        if closed:
            Part.show(Part.makePolygon(pts2+[pts2[0]]))
            Part.show(Part.makePolygon(pts3+[pts3[0]]))
        else:
            Part.show(Part.makePolygon(pts2))
            Part.show(Part.makePolygon(pts3))




