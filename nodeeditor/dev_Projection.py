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
    



def run_FreeCAD_Parallelprojection(self,*args, **kwargs):

    f=store.store().get(self.getPinByName('face').getData())
    say("Face",f)
    e=store.store().get(self.getPinByName('edge').getData())
    say("Edge",e)
    if f== None or e == None:
        sayW("no face or no edge connected")
        return

    store.store().list()
    d=self.getPinByName('direction').getData()
    say("direction",d)
    shape=f.makeParallelProjection(e,d)
    self.setPinObject('Shape_out',shape)

def run_FreeCAD_Perspectiveprojection(self,*args, **kwargs):


    f=store.store().get(self.getPinByName('face').getData())
    say("Face",f)
    e=store.store().get(self.getPinByName('edge').getData())
    say("Edge",e)
    if f== None or e == None:
        sayW("no face or no edge connected")
        return

    store.store().list()
    d=self.getPinByName('direction').getData()
    say("direction",d)
    shape=f.makePerspectiveProjection(e,d)
    cc=self.getObject()
    if cc  !=  None:
        cc.Label=self.objname.getData()
        cc.Shape=shape
        #cc.ViewObject.LineWidth=8
        cc.ViewObject.LineColor=(1.,1.,0.)


def run_FreeCAD_UVprojection(self,*args, **kwargs):

    f=store.store().get(self.getPinByName('face').getData())
    w=store.store().get(self.getPinByName('edge').getData())
    closed=True
    #closed=False

    if f==None:
        sayW("no face connected")
        return

    sf=f.Surface

    pointcount=max(self.getPinByName('pointCount').getData(),4)
    pts=w.discretize(pointcount)


    bs2d = Part.Geom2d.BSplineCurve2d()
    if closed:
        pts2da=[sf.parameter(p) for p in pts[1:]]
    else:
        pts2da=[sf.parameter(p) for p in pts]

    pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da]
    pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da[:-1]]
    if closed:
        bs2d.buildFromPolesMultsKnots(pts2d,[1]*(len(pts2d)+1),range(len(pts2d)+1),True,1)
    else:
        mults=[2]+[1]*(len(pts2d)-2)+[2]
        knots=range(len(mults))
        bs2d.buildFromPolesMultsKnots(pts2d,mults,knots,False,1)
        
    e1 = bs2d.toShape(sf)

    sp=FreeCAD.ActiveDocument.getObject("_Spline")
    if sp==None:
        sp=FreeCAD.ActiveDocument.addObject("Part::Spline","_Spline")
    sp.Shape=e1

    face=f
    edges=e1.Edges
    ee=edges[0]
    splita=[(ee,face)]
    r=Part.makeSplitShape(face, splita)

    ee.reverse()
    splitb=[(ee,face)]
    r2=Part.makeSplitShape(face, splitb)

    try:
        rc=r2[0][0]
        rc=r[0][0]
    except: return

    '''
    cc=self.getObject()
    if cc  !=  None:
        cc.Label=self.objname.getData()

    if self.getPinByName('inverse').getData():
        cc.Shape=r2[0][0]
    else:
        cc.Shape=r[0][0]
    '''
    if self.getData('inverse'):
        self.setPinObject("Shape_out",r2[0][0])
    else:
        self.setPinObject("Shape_out",r[0][0])
    return
    
    if self.getPinByName('Extrusion').getData():
        f = FreeCAD.getDocument('project').getObject('MyExtrude')
        if f == None:
            f = FreeCAD.getDocument('project').addObject('Part::Extrusion', 'MyExtrude')

        f.Base = sp
        f.DirMode = "Custom"
        f.Dir = FreeCAD.Vector(0.000000000000000, 0.000000000000000, 1.000000000000000)
        f.LengthFwd = self.getPinByName('ExtrusionUp').getData()
        f.LengthRev = self.getPinByName('ExtrusionDown').getData()
        f.Solid = True
        FreeCAD.activeDocument().recompute()

    #see without extra part >>> s.Face1.extrude(FreeCAD.Vector(0,1,1))
    #<Solid object at 0x660e520>

