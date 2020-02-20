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

def run_FreeCAD_Collect_Data(self, mode=None):

    if mode=="reset":
        self.points=[]
    
    else:

        maxSize=self.getData("maxSize")    
        point = self.getData("data")

        self.points += [point]
        if maxSize >0 and len(self.points)>maxSize:
                self.points = self.points[len(self.points)-maxSize:]   

    self.setData("collection",self.points)

    if not self.inRefresh.hasConnections():
        self.outExec.call()

def run_FreeCAD_ImportCSVFile(self):

    try:
        self.last
    except:
        self.last=time.time()
        
    filename=self.getData('filename')
    
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
    #say(os.stat(filename))

    if not self.getData('force') and self.last > mtime:
        sayErr("---------------not new")
        return
        
    self.last = time.time()

    f=open(filename,"r")
    contents =f.read()
    ls=contents.splitlines()
    rr=[]
    vs=[]
    seps=self.getData('separator')
    sepk={
        'tabulator':'\t',
        'space':' ',
        'semicolon':';',
        'comma':',',
    }    
        
    sep=sepk[seps]
    for l in ls:
        try:
            if l.startswith('#'):
                continue
            rr += [[float(a) for a in l.split(sep)]]
            ff=[float(a) for a in l.split(sep)]
        except:
            pass
        vs += [FreeCAD.Vector(*ff[:3])]
        
    self.setData('data',rr)
    self.setData('points',vs)
    say(vs)



    if 0: # tessellation tests temp
        tt=FreeCAD.ActiveDocument.BePlane.Shape.Face1
        ta=time.time()
        zz=tt.tessellate(0.1)
        say("Tessellate",len(str(zz)))
        
        say(time.time()-ta)
    

