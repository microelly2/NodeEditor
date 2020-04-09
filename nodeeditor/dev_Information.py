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


def run_FreeCAD_CenterOfMass(self):
    #shape=self.getPinObject("Shape")
    if 0:
        t=self.getPinByName("Shape")

        outArray = []
        ySortedPins = sorted(t.affected_by, key=lambda pin: pin.owningNode().y)
        for i in ySortedPins:
            outArray.append(i.owningNode().getPinObject(i.name))

    else:
        outArray=self.getPinObjectsA("ShapeList")
    
    say(outArray)    
        
    pts=[f.CenterOfMass for f in outArray]
    self.setData("points",pts)
    


def run_FreeCAD_DistToShape(self):
    
    eids=self.getPinObjectsA("shapes")
    if len(eids)==0:
       points=self.getData('points')
       eids=[Part.Point(p).toShape() for p in points]
    
    target=self.getPinObject("target")
    dists=[]
    for s in eids:
        dists += [target.distToShape(s)[0]]

    self.setData("distance",dists)
    self.setColor(b=0,a=0.4)



def run_FreeCAD_Object2(self, *args, **kwargs):

        say("-------------------------------")
        say ("in compute",self.getName(),"objname is",self.objname.getData())
        nl=len(self.getName())
        pps=self.getOrderedPins()
        say(pps)
        say("lllllllllllll")
        for p in pps:
            try:
                print((str(p.getName()[nl+1:]),p.getData()))
            except:  pass
        obn=self.objname.getData()
        FreeCAD.ActiveDocument.recompute()
        obj=FreeCAD.ActiveDocument.getObject(obn)
        self.fob=obj
        sayl("vor store ")
        obj.purgeTouched()
        self.store()
        sayl("oioio")
        try:
            sh=obj.Shape
            self.setPinObject("Shape_out",sh)
        except:
            pass # no shape
        sayl("kk")
    

        say("vorbr")
        a=self.makebackref()
        say("nach backref")
        if a != None:
            a.sources=[obj]


        a.purgeTouched()
        say("Reference", a.Name)
        
        if self._preview:
            self.preview()





def run_FreeCAD_Plot(self,*args, **kwargs):

    
    sayl("huhuhu44")

    
    mode=self.getData("Figure")
    say("mode",mode)

    if mode=="Figure1":
        fig=plt.figure(1)

    elif mode=="Figure2":
        fig=plt.figure(2)

    elif mode=="Figure3":
        fig=plt.figure(3)

    else:
        fig=plt.figure(4)

    #plt.close()
    plt.clf()
    plt.title(self.getName())

    x=self.xpin.getData()
    y=self.ypin.getData()

    say(x)
    say(y)
    say(len(x),len(y))

    #x=[1,2,3]
    #y=[1,5,3]
    
    if len(y)  != 0:
        N=len(y)
        if len(x) != len(y):
            x = np.linspace(0, len(y), N, endpoint=True)
        else:
            x=np.array(x)

        y=np.array(y)

        if not  mode=="Figure3":
             plt.plot(x, y , 'b-')


    x2=self.xpin2.getData()
    y2=self.ypin2.getData()
    say (len(x2),len(y2))
    if x2  !=  None and y2  !=  None:
        x2=np.array(x2)
        y2=np.array(y2)
        if not mode=="Figure3":
            plt.plot(x2, y2 , 'r-')
        else:
            plt.plot(x2, y2, 'ro')


    plt.show()
    
    
    fig.canvas.draw()
    #fig.canvas.flush_events()



def run_FreeCAD_Plot2D(self):
        xs=self.getData('x')
        #print(xs)
        ys=self.getData('y')
        #ys=[0,12,-3,5,0,4,8]
        #print(ys)
        if len(xs) == 0:
            print("def xs",len(ys)) 
            xs=np.linspace(0,len(ys)-1,len(ys))*100
            print (xs)
            #xs=[0,1,2,3]
        #print(xs)
        pts=[FreeCAD.Vector(x,y) for x,y in zip(xs,ys)]
        #print(pts)
        pol=Part.makePolygon(pts)
        #Part.show(pol)
        self.setPinObject("Shape_out",pol)
