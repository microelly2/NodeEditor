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



from nodeeditor.cointools import *
    



def run_dragger(self,**kv):
    
    tns=[]

    def handler(arg):
        say("dragger moved")
        self.compute()

    def handler2(arg):
        say("dragger started")
    
    
    pointsa=self.getData('Points_out')
    self.startpositions=pointsa
    
    if len(pointsa)==0:
        pointsa=[FreeCAD.Vector()]
    
        
    try:
            self.points
    except:
        say("hoel daten - self. points nicht da ")
        points=self.getData("points")
        if len(points) == 0 :
            say("keine Dat points points - nehme zielpunkte")
            
            pointsa=[FreeCAD.Vector(0,0,0)]
            points=pointsa
    
        self.points=points
    
    #self.points=pointsa
    
    points=self.points
    
    par=np.array(points)

    if len(par.shape)==3:
        a,b,c=par.shape
        points=par.reshape(a*b,3)
    else:
        points=par
    
    self.points=points

    try:
        FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
    except:
        pass

    self.gg= coin.SoSeparator()
    FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().addChild(self.gg)

    pmas=[]
    for p in points:
        say("setze dragger position auf",p)

        t=coin.SoType.fromName("SoFCCSysDragger")
        dragger=t.createInstance()
        #dragger.setStartingPoint(coin.SbVec3f(0,0,0))
        try:
            #1/0
            say("restore matrix - hack: deactivated ")
            
            self.startmatrix=np.array([[0,0,1,0],[0.7,0.71,0,0],[-0.71,0.7,0,0],[40,-20,30,1]])
            self.startmatrix=np.array([[1,0,0,0],[0,1,0,0],[0.,0,1,0],[0,0,0,1]])
            say(self.startmatrix)
            mm=FreeCAD.Matrix(*self.startmatrix.flatten())
            mm.transpose()           
            pma=FreeCAD.Placement(mm)
            #pma.Base += pointsa[0]
            pma.Base += self.startpositions[0]
            
            
            pmas += [pma]
            
            #FreeCAD.ActiveDocument.Cone.Placement=pma
            
            dragger.getMotionMatrix().setValue(self.startmatrix)
        except:
            dragger.setStartingPoint(coin.SbVec3f(0,0,0))
        

        
        view = FreeCADGui.ActiveDocument.ActiveView
        view.addDraggerCallback(dragger, "addFinishCallback", handler)
        view.addDraggerCallback(dragger, "addStartCallback", handler2)

        g = coin.SoSeparator()
        tt = coin.SoTransform()

        tt.translation = p.tolist()  
        
        g.addChild(tt)
        g.addChild(dragger)
        self.gg.addChild(g)
        tns += [dragger]

    self.setData("hands",pmas)

    for n in tns:   
        pass
        #print (n)
        #print(n.getLocalStartingPoint().getValue())
        #print(n.getMotionMatrix().getValue())

    self.tns=tns


def run_FreeCAD_Dragger(self,**k):
   
    
    try:
        self.tns
    except:
        run_dragger(self)
    
    points=self.getData("points")
    par=np.array(points)
    pdiffs=[]
    
    #say("tns",self.tns)

    n=self.tns[0]
    pos=FreeCAD.Vector(n.getLocalStartingPoint().getValue())
    m=n.getMotionMatrix().getValue()
    m=FreeCAD.Matrix(*np.array(m).flatten())
    mm=m
    
    pma=FreeCAD.Placement(m).inverse()

    target=pma.multVec(-pos)
    tu=pma.multVec(FreeCAD.Vector(1,0,0))
    tv=pma.multVec(FreeCAD.Vector(0,1,0))
    self.setData('point_out',target)
    self.setData('hand',[target,tu,tv])
    

    mm.transpose()           
    pma=FreeCAD.Placement(mm)
    #pma.Base += self.startpositions[0]  
    self.setData('hands',[pma])
    
    apos=pma.inverse().multVec(target)
    
    clearcoin(self)

    ptsl=[FreeCAD.Vector(),target]
    displayline(self,ptsl,color=(1,1,1))
    displaytext(self,target,color=(1,1,0),text=[self.name])

    m=np.round(n.getMotionMatrix().getValue(),2)
    
    store=True
    if store:
        self.startmatrix=m
        
    m=n.getMotionMatrix().getValue()
    
    
    m=FreeCAD.Matrix(*np.array(m).flatten())
    pma=FreeCAD.Placement(m).inverse()
    t=np.round(np.array(pma.inverse().toMatrix().A).reshape(4,4),2)
    
    

    for n in self.tns:  
        pdiffs += [-FreeCAD.Vector(n.getLocalStartingPoint().getValue())]

    if len(par.shape)==3:
        a,b,c=par.shape
        
        # has something changed?     
        points=par.reshape(a*b,3)
        lls=[(a-FreeCAD.Vector(b)).Length for a,b in zip(pdiffs,points)]
        if max(lls)< 0.1:
            say("zu wenig aenderung abbruch")
            return
        
        pdiffs=np.array(pdiffs).reshape(a,b,3).tolist()
    
    self.setData("Points_out",pdiffs)    
    self.setData("point_out",pdiffs[0])
    
    self.points=pdiffs
       
    self.outExec.call()
    self.setColor()

    if self._preview:
        say("create preview")
        self.preview()

