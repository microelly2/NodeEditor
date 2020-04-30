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
        vv=i.owningNode().getData(i.name)
        col +=[vv]
    say("shape result",np.array(col).shape)
    self.setData('vectorarray',col)
    





def run_FreeCAD_ListOfShapes(self):
    
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        vv=i.owningNode().getPinObject(i.name)
        say(i.name,vv)
        b += [vv]
    say(b)
    self.setPinObjects("ShapeList",b)
    self.setColor(a=0.7)
    



def run_FreeCAD_ListOfVectors(self):
    
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        vv=i.owningNode().getData(i.name)
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
    
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        vv=i.owningNode().getData(i.name)
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




def run_FreeCAD_ListOfPlacements(self):

    if len(self.getPinByName("axes").affected_by) >0:
        axes=self.getData("axes")
    else: axes=[]

    if len(self.getPinByName("centers").affected_by) >0:
        centers=self.getData("centers")
    else:centers=[]

    if len(self.getPinByName("moves").affected_by) >0:
        moves=self.getData("moves")
    else:
        moves=[]

    if len(self.getPinByName("angles").affected_by) >0:        
        angles=self.getData("angles")
    else:
        angles=[]
        
    ll=max(len(axes),len(centers),len(moves),len(angles))

    if 1:
        if ll>len(centers):
            centers += [FreeCAD.Vector(0,0,0)]*(ll-len(centers))

        if ll>len(axes):
            axes += [FreeCAD.Vector(0,0,1)]*(ll-len(axes))

        if ll>len(moves):
            moves += [FreeCAD.Vector(0,0,0)]*(ll-len(moves))

        if ll>len(angles):
            angles += [10]*(ll-len(angles))
    
    
    rots=[]
    for m,ax,an,ce in zip(moves,axes,angles,centers):
        rots += [FreeCAD.Placement(m,FreeCAD.Rotation(ax,an),ce)]
    
    self.setPinPlacements("Placements",rots)


    

def run_FreeCAD_Zip(self):
    x=self.getData("x")
    y=self.getData("y")
    z=self.getData("z")
    
    zz= [FreeCAD.Vector(x,y,z) for x,y,z in zip(x,y,z)]
    say("len",len(zz))
    self.setData("vectors_out",zz)




def run_FreeCAD_IndexToList(self):

    outArray = []
    pins=self.getPinByName('index').affected_by
    for i in pins:
        outArray.append(i.owningNode().getData(i.name))
    arr=np.array(outArray).flatten()
    if len(arr)==0:return
    m=max(arr)
    flags=np.zeros(m+1)
    for p in arr:
        flags[p]=1
    self.setData("flags",flags.tolist())
    self.setColor(b=0,a=0.4)
    

    
def run_FreeCAD_MoveVectors(self):
    #+# todo anpassen 1 2 3 dimensionale arrays

    vv=self.getData("vectors")
    mv=self.getData("mover")
    say(np.array(vv).shape)
    if len(np.array(vv).shape)>2:
        b2=[]
        for av in vv:
            
            b3=[v+mv for v in av]
            b2 += [b3]
    else:
        b2=[v+mv for v in vv]

    self.setData("vectors_out",b2)
    self.setColor(g=0,a=0.4)
    
    

def run_FreeCAD_ScaleVectors(self):
    #+# todo anpassen 1 2 3 dimensionale arrays

    vv=self.getData("vectors")
    mv=self.getData("scaler")

    b=[]
    if len(np.array(vv).shape)>1:
        ll=np.array(vv).shape
        vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
        b += vv.tolist()
    else:
        b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    b2=[FreeCAD.Vector(v.x*mv.x,v.y*mv.y,v.z*mv.z) for v in b]

    self.setData("vectors_out",b2)
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_FlipSwapArray(self):
    say("flipswap")
    say(self.name)
    poles=np.array(self.getData('poles_in'))
    say("shape",poles.shape)
    if len(poles.shape)<2: return
    if self.getData('swap'):
        poles=poles.swapaxes(0,1)
    if self.getData('flipu'):
        poles=np.flipud(poles)
    if self.getData('flipv'):
        poles=np.flipud(poles)


    
    say("result",poles.shape)
    self.setData('poles_out',poles.tolist())



