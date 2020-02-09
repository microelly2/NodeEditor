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



def run_FreeCAD_Geom2DGeometry(self,*args, **kwargs):
    
    sayl()

    if os.path.exists('/tmp/lock'):
        say("Abbruch")
        return

    try:
        if time.time()-self.Lock <1.1:
            return
    except:
        say("noc lock")
    self.Lock=time.time()
    say("running--------")
    
    face=self.getPinObject("Shape")
    if face == None:
        return
    
    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    ua=self.getData("ua")*0.1
    va=self.getData("va")*0.1
    ub=self.getData("ub")*0.1
    vb=self.getData("vb")*0.1

    ua=umin+ua*(umax-umin)
    va=vmin+va*(vmax-vmin)
    ub=umin+ub*(umax-umin)
    vb=vmin+vb*(vmax-vmin)

    a=FreeCAD.Base.Vector2d(ua,va)
    b=FreeCAD.Base.Vector2d(ub,vb)

    line=Part.Geom2d.Line2dSegment(a,b)
    
    ee = line.toShape(sf)
    # Part.show(ee)
    #say(ee)
    say(ee.Length)
    
    self.setPinObject("geometry",line)
    self.setPinObject("Shape_out",ee)


    self.Lock=0


def run_FreeCAD_Geom2DCircle(self,*args, **kwargs):

    face=self.getPinObject("Shape")
    if face == None:
        return

    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    u=self.getData("u")*0.1
    v=self.getData("v")*0.1
    r=self.getData("radius")*0.1

    u=umin+u*(umax-umin)
    v=vmin+v*(vmax-vmin)
    r=r*(umax-umin)

    a=FreeCAD.Base.Vector2d(u,v)

    line=Part.Geom2d.Circle2d(a,r)
    say(line)
    
    ee = line.toShape(sf)
    
    self.setPinObject("geometry",line)
    self.setPinObject("Shape_out",ee)




def run_FreeCAD_Geom2DEllipse(self,*args, **kwargs):

    face=self.getPinObject("Shape")
    if face == None:
        return

    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    u=self.getData("uLocation")*0.1
    v=self.getData("vLocation")*0.1
    #r=self.getData("radius")*0.1
    r=4

    u=umin+u*(umax-umin)
    v=vmin+v*(vmax-vmin)
    r=r*(umax-umin)

    a=FreeCAD.Base.Vector2d(u,v)
    xax=FreeCAD.Base.Vector2d(np.sin(self.getData("direction")*np.pi/5),np.cos(self.getData("direction")*np.pi/5))
    #yax=FreeCAD.Base.Vector2d(self.getData("uYAxis"),self.getData("vYAxis"))
    fig=ine=Part.Geom2d.Ellipse2d()
    fig.MinorRadius=self.getData("MinorRadius")*0.1
    fig.MajorRadius=self.getData("MajorRadius")*0.1
    fig.Location=a
    fig.XAxis=xax
#   fig.YAxis=yax
    
    
    ee = fig.toShape(sf)
    
    self.setPinObject("geometry",fig)
    self.setPinObject("Shape_out",ee)




def run_FreeCAD_Geom2DArcOfEllipse(self,*args, **kwargs):

    face=self.getPinObject("Shape")
    if face == None:
        return

    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    u=self.getData("uLocation")*0.1
    v=self.getData("vLocation")*0.1
    #r=self.getData("radius")*0.1
    r=4

    u=umin+u*(umax-umin)
    v=vmin+v*(vmax-vmin)
    r=r*(umax-umin)

    a=FreeCAD.Base.Vector2d(u,v)
    xax=FreeCAD.Base.Vector2d(np.sin(self.getData("direction")*np.pi/5),np.cos(self.getData("direction")*np.pi/5))
    #yax=FreeCAD.Base.Vector2d(self.getData("uYAxis"),self.getData("vYAxis"))
    fig=Part.Geom2d.Ellipse2d()
    fig.MinorRadius=self.getData("MinorRadius")*0.1
    fig.MajorRadius=self.getData("MajorRadius")*0.1
    fig.Location=a
    fig.XAxis=xax
#   fig.YAxis=yax

    arca=self.getData("startAngle")
    arcb=self.getData("endAngle")*np.pi/5

    say(arca,arcb)
    fig=Part.Geom2d.ArcOfEllipse2d(fig,arca,arcb)

    ee = fig.toShape(sf)
    
    self.setPinObject("geometry",fig)
    self.setPinObject("Shape_out",ee)



def run_FreeCAD_Geom2DArcOfCircle(self,*args, **kwargs):

    sayl()
    face=self.getPinObject("Shape")
    if face == None:
        umin,umax,vmin,vmax=0,10,0,10
        sf=None
    else:
        umin,umax,vmin,vmax=face.ParameterRange
        sf=face.Surface

    u=self.getData("uLocation")*0.1
    v=self.getData("vLocation")*0.1
    #r=self.getData("radius")*0.1
    r=self.getData("radius")*0.1

    u=umin+u*(umax-umin)
    v=vmin+v*(vmax-vmin)
    r=r*(umax-umin)

    a=FreeCAD.Base.Vector2d(u,v)
#   xax=FreeCAD.Base.Vector2d(np.sin(self.getData("direction")*np.pi/5),np.cos(self.getData("direction")*np.pi/5))
#   #yax=FreeCAD.Base.Vector2d(self.getData("uYAxis"),self.getData("vYAxis"))
#   fig=Part.Geom2d.Ellipse2d()
#   fig.MinorRadius=self.getData("MinorRadius")*0.1
#   fig.MajorRadius=self.getData("MajorRadius")*0.1
#   fig.Location=a
#   fig.XAxis=xax
#   fig.YAxis=yax


    fig=Part.Geom2d.Circle2d(a,r)

    arca=self.getData("startAngle")
    arcb=self.getData("endAngle")*np.pi/5

    say(arca,arcb)
    fig=Part.Geom2d.ArcOfCircle2d(fig,arca,arcb)

    if sf== None:
        ee = fig.toShape()
    else:
        ee = fig.toShape(sf)
    
    self.setPinObject("geometry",fig)
    self.setPinObject("Shape_out",ee)



def run_FreeCAD_Geom2DArcOfParabola(self,*args, **kwargs):

    face=self.getPinObject("Shape")
    if face == None:
        return

    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    u=self.getData("uLocation")*0.1
    v=self.getData("vLocation")*0.1
    #r=self.getData("radius")*0.1
    r=4

    u=umin+u*(umax-umin)
    v=vmin+v*(vmax-vmin)
    r=r*(umax-umin)

    a=FreeCAD.Base.Vector2d(u,v)
    xax=FreeCAD.Base.Vector2d(np.sin(self.getData("direction")*np.pi/5),np.cos(self.getData("direction")*np.pi/5))
    #yax=FreeCAD.Base.Vector2d(self.getData("uYAxis"),self.getData("vYAxis"))
    fig=Part.Geom2d.Parabola2d()
    fig.Focal=self.getData("MinorRadius")*0.1
    #fig.MajorRadius=self.getData("MajorRadius")*0.1
    fig.Location=a
    fig.XAxis=xax
#   fig.YAxis=yax

    arca=self.getData("startAngle")*np.pi/5
    arcb=self.getData("endAngle")*np.pi/5

    say(arca,arcb)
    fig=Part.Geom2d.ArcOfParabola2d(fig,arca,arcb)

    if sf  !=  None:
        ee = fig.toShape(sf)
    else:
        ee = fig.toShape()
    
    self.setPinObject("geometry",fig)
    self.setPinObject("Shape_out",ee)


'''
para=Part.Parabola(App.Vector(-50.993458,78.566841,0),App.Vector(28.611713,68.414307,0),App.Vector(0,0,1))
Part.ArcOfParabola(para,11.605501,43.939412)



circ=Part.Circle(App.Vector(33.254650,124.267365,0),App.Vector(0,0,1),49.420288)
Part.ArcOfCircle(circ,3.110107,4.361358)
'''


 
