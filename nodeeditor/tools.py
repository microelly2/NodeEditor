import numpy as np
import random
import time
import os.path
from os import path
import matplotlib.pyplot as plt
import scipy.interpolate

from nodeeditor.say import *


print ("reloaded: "+ __file__)

# tools for geometry ...


def data2vecs(data):
    '''convert data to vector or list of vectors or other more complex vectorstructure'''
    
    ndat=np.array(data).flatten()
    say(ndat)
    if ndat.shape==(3,):
        say("vector")
        return FreeCAD.Vector(*ndat)
    else:
        classes=set([x.__class__.__name__ for x in data])
        if not 'list' in classes    :
            say("simple values")
            _points=np.array(data).reshape(int(len(data)/3),3)
            points=[FreeCAD.Vector(*p) for p in _points]
            return points
        else:
            # list of vectorlists
            plist=[]
            for l in data:
                classes=set([x.__class__.__name__ for x in l])
                assert not 'list' in classes
                _points=np.array(l).reshape(int(len(l)/3),3)
                points=[FreeCAD.Vector(*p) for p in _points]
                plist.append(points)
            return plist
                
import Part        
def createBSplineSurface(poles=None,
            uknots=None,vknots=None,umults=None,vmults=None,
            udegree=3,vdegree=3,uperiodic=False,vperiodic=False,
            uclosed=False,vclosed=False,weights=None):
    
    if poles is None:
        poles=[[[0,0,0],[50,0,0],[100,0,0]],[[0,50,0],[50,50,200],[100,50,0]],[[0,100,0],[50,100,0],[100,100,0]]]
        
    (uc,vc,_)=np.array(poles).shape
    udegree=min(udegree,uc-1)
    vdegree=min(vdegree,uc-1)
        
    bs=Part.BSplineSurface()
    
    if umults is None:
        umults=[udegree+1]+[1]*(uc-1-udegree)+[udegree+1]
    if vmults is None:
        vmults=[vdegree+1]+[1]*(vc-1-vdegree)+[vdegree+1]
    
    if uknots is None:
        uknots=range(len(umults))
    if vknots is None:
        vknots=range(len(vmults))
    

    bsa=Part.BSplineSurface()
    if weights is None:
        bsa.buildFromPolesMultsKnots(poles,umults,vmults,uknots,vknots,uclosed,vclosed,udegree,vdegree)
    else:
        bsa.buildFromPolesMultsKnots(poles,umults,vmults,uknots,vknots,uclosed,vclosed,udegree,vdegree,weights)
    
    
    return bsa
    
        
        
        
        
    
    
