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

from pivy import coin

print ("reloaded: "+ __file__)


def run_FreeCAD_ListOfVectorlist(self):

    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    col=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        i.owningNode().compute()
        vv=i.owningNode().getData(i.name)
        col +=[vv]
    say("shape result",np.array(col).shape)
    self.setData('vectorarray',col)
    



def run_FreeCAD_ListOfShapes(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        # i.owningNode().compute()
        vv=i.owningNode().getPinObject(i.name)
        say(i.name,vv)
        b += [vv]
    say(b)
    self.setPinObjects("ShapeList",b)
    self.setColor(a=0.7)
    



def run_FreeCAD_ListOfVectors(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        i.owningNode().compute()
        vv=i.owningNode().getData(i.name)
        #say(i.name,vv)
        #say(np.array(vv).shape)
        if len(np.array(vv).shape)>1:
            ll=np.array(vv).shape
            vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
            b += vv.tolist()
        else:
            b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    self.setData("vectors",b)
    self.setColor(a=0.7)
    

def run_FreeCAD_ListOfVectorList(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        i.owningNode().compute()
        vv=i.owningNode().getData(i.name)
        #say(i.name,vv)
        #say(np.array(vv).shape)
        if len(np.array(vv).shape)>1:
            ll=np.array(vv).shape
            vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
            b += vv.tolist()
        else:
            b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    self.setData("vectors",b)
    self.setColor(a=0.7)
    



def run_FreeCAD_Transformation(self):

    vx=self.getData("vectorX")
    vy=self.getData("vectorY") 
    vz=self.getData("vectorZ") 
    v0=self.getData("vector0") 
    dat=[vx.x,vx.y,vx.z,
        vy.x,vy.y,vy.z,
        vz.x,vz.y,vz.z,
        v0.x,v0.y,v0.z,
        ]
    
    dat=np.array(dat).reshape(4,3)

    vv2=self.getPinByName("transformation")
    vv2.setTransformation(dat)
    



def run_FreeCAD_uv2xyz(self):
    sh=self.getPinObject("Shape")
    if sh is None:
        sayErOb(self,"no Shape")
        return
        
    bs=sh.Surface
    uvs=self.getData('points')
    
    pts += [bs.value(uv[0],uv[1]) for uv in uvs]
    self.setData('Points_out',pts)
    

def run_FreeCAD_xyz2uv(self):
	sayW("not implemetned")
	sayl()
