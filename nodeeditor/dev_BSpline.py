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
reload(noto)
    

def run_FreeCAD_BSplineSegment(self):
    
    sh=self.getPinObject("Shape")
    bs=sh.Surface.copy()

    ustart=self.getData('uStart')*0.01
    vstart=self.getData('vStart')*0.01
    uend=self.getData('uEnd')*0.01
    vend=self.getData('vEnd')*0.01
    [ua,ue,va,ve]=sh.ParameterRange
    bs.segment(ua+(ue-ua)*ustart,ua+(ue-ua)*uend,va+(ve-va)*vstart,va+(ve-va)*vend)
    self.setPinObject('Shape_out',bs.toShape())
     
def run_FreeCAD_BSplineOffset(self):

    sh=self.getPinObject("Shape") 
    h=self.getData("height")

    bs=sh.Surface
    [ua,ue,va,ve]=sh.ParameterRange
    
    size=self.getData('sizeU')
    sizeV=self.getData('sizeV')
    say(size)

    # point to offset
    points=np.array([[bs.value(ua+(ue-ua)*u/size,va+(ve-va)*v/size) for v in range(size+1)]  for u in range(size+1)])

    # find normals to expand
    nomrs=[]
    errors=[]
    for u in range(size+1):
        nus=[]
        for v in range(size+1):
            try:
                nus += [bs.normal(ua+(ue-ua)*u/size,va+(ve-va)*v/size)]
            except:
                say("Error normal for",u,v)
                errors +=[(u,v)]
                nus += [FreeCAD.Vector()]
        nomrs += [nus]       

    norms=np.array(nomrs)
    
    # reair invalid normals 
    for (u,v) in errors:
        say(size,u,v)
        du=1
        dv=1
        if u==size:
            du =-1
        if v==size:
            dv =-1
        say("new normal used",norms[u+du,v+dv])
        norms[u,v]=norms[u+du,v+dv]

    # calculate secure height without collsions
    # #+#todo: improve algorithm to handle collisions
    rs=[]
    for u in range(1,size):
        for v in range(1,size):                
            n=FreeCAD.Vector(norms[u,v])
            a=FreeCAD.Vector(*(points[u+1,v]-points[u,v]))
            aa=a.normalize()
            rs +=[0.5*a.Length/abs(aa.dot(n))]
            
    say("offset works for maximum height with out collisions", min(rs))


    newpts=points+ norms*h
    self.setData('Points_out',newpts.tolist())   

    bsa=noto.createBSplineSurface(newpts,udegree=1,vdegree=1)
    self.setPinObject('Shape_out',bsa.toShape())

    # test quality
    testpts=np.array([[bsa.value(ua+(ue-ua)*u/size,va+(ve-va)*v/size) for v in range(size+1)]  for u in range(size+1)])
    ptsn=testpts.reshape((size+1)**2,3)
    
    dists=[sh.distToShape(Part.Vertex(*p))[0] for p in ptsn]
    say("distance expected min max",round(abs(h),2),round(min(dists),2),round(max(dists),2))

    
    
    
     

#+# todo cleanup code reduceCurve 31.01.2020
def run_FreeCAD_ReduceCurve(self):
    
    try:
        if self.shape is None:
            1/0
        say(self.shape)
        sh=self.shape
    except:
        sh=self.getPinObject("Shape")
        self.shape=sh
    
    c=sh.Curve.copy()
   
    
    sfa=c.copy()
    sfb=c.copy()
    sfab=c.copy()    
    
    pts=c.getPoles()
    
    p=self.getData('start')+1
    l=self.getData('segments')
    kk=c.getKnots()
    
    
    
    clearcoin(self)
    if l == -1:
        self.setPinObject('Shape_out',sh)
        return

    if not self.getData('hide') and self.getData('useStartPosition'):
            displaysphere(self,c.value(kk[max(0,p-4)]),radius=4,color=(0,1,1))
    
    
    say("intervall",p,l)
    poles=pts[:p]+pts[p+l:]

    s=Part.makePolygon(poles)
    
       
    
    if self.getData('useStartPosition'):
        pp=self.getData('position')
    else:
        if l==0:
            pp=pts[p]
        else:
            pp=Part.makePolygon(pts[p:p+l+1]).CenterOfMass

    m1=self.getData('Move1')
    m2=self.getData('Move2')

    
    
    
    if l == 0:
        target=pts[p]
    else:
        if self.getData('usePositionAsAbsolute'):
            target=self.getData('position')    
        else:
            target=Part.makePolygon(pts[p:p+l+1]).CenterOfMass+self.getData('position')    
        
    if not self.getData('hide'):
        displaysphere(self,target,radius=8,color=(1,0,1))


    poles=pts[:p-1]+[pp]+pts[p+l:]
    countA=len(poles)
    degA=3
    periodic=False
    
    if not periodic:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        knotA=range(len(multA))
    else:
        multA=[1]*(countA+1)
        knotA=range(len(multA))

    polesA=[p+FreeCAD.Vector(0,0,10) for p in poles]  
    poles=polesA
    sf=Part.BSplineCurve()
    sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)
    

    strat=self.getData("Strategy")

    def dist(param):

        t=param[0]
        pap=FreeCAD.Vector(*param)
        poles=pts[:p-1]+[pap]+pts[p+l:]
        sf=Part.BSplineCurve()
        sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)


        
        dd=sf.toShape().distToShape(Part.Vertex(target))[0]        
        ll=sf.toShape().Length

        
        if strat=='Shortest':
            return ll
        else:
            return  dd




    
    from scipy import optimize
    
    if strat != 'Center of Mass':    
        method=self.getData('Method')
        a=time.time()
        start=target
        result = optimize.minimize(dist, x0=[start.x,start.y,start.z],  method=method)
        r=result.x[0]

        say("quality",np.round(result.fun,5),np.round(result.x,2),result.message,method)
        say("run time for scipy.optimize.minimum",method,round(time.time()-a,3))

        pp=FreeCAD.Vector(result.x)

    if  strat != 'Point':
        if l==0:
            tang=pts[p-1]-pts[p+1]
        else:
            tang=pts[p]-pts[p+l]
        
        norm=FreeCAD.Vector(-tang.y,tang.x)
        pp += -m1*tang/100 +m2*norm/100

    
    
    say("build poles---------------------")
    if l != 0:
        poles=pts[:p-1]+[pp]+pts[p+l:]
    else:
        poles=pts[:p]+[pp]+pts[p+1:]
    
    say("pts,poles,l",len(pts),len(poles),l)
    
    if p+l==len(pts):
        poles=pts[:p-1]+[pts[-1]]
    
    
    mpoints=pts[p:p+l]
    
    countA=len(poles)
    degA=3
    periodic=False
    
    if not periodic:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        knotA=range(len(multA))
    else:
        multA=[1]*(countA+1)
        knotA=range(len(multA))

    
    sf=Part.BSplineCurve()
    sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)


    tv=sf.parameter(target)
    tang=sf.tangent(tv)
    
    dird=FreeCAD.Vector(np.cos(m1/100.*np.pi),np.sin(m1/100.*np.pi))
    tdd=dird.dot(tang[0])

    say("lenght dist",sf.toShape().Length,sf.toShape().distToShape(Part.Vertex(target))[0])
    
    
    kks=sf.getKnots()   
    pointsAAA= [sf.value(t) for t in range(max(0,p-4),min(p+1,len(kks)))]
    if not self.getData('hide'):
        displaysphere(self,pointsAAA[0],radius=6,color=(0,1,0))
        displaysphere(self,pointsAAA[-1],radius=6,color=(0,1,0))
    if l ==0:
        pointsAAA += [c.value(kk[t]) for t in range(max(0,p-4),min(p+l+1,len(kk)))]
    else:    
        pointsAAA += [c.value(kk[t]) for t in range(max(0,p-4),min(p+l,len(kk)))]
    self.setData('points',pointsAAA)
    
    if not self.getData('hide'):
        displayspheres(self,pointsAAA,radius=4,color=(0,1,1))
    
    
    self.outExec.call()
    
    po=max(1,p-4)

    
    kk=c.getKnots()

    sfa=sf.copy()
    sfa.segment(po,po+4)
    ptsf =sfa.toShape().discretize(100)[::-1]
    if not self.getData('hide'):
        displayline(self,ptsf,(1,0,0))

    ca=c.copy()
    if l==0:
        ca.segment(kk[po-1+1],kk[min(po+l+2+2+1,len(kk)-1)])
    else:
        ca.segment(kk[po-1+1],kk[min(po+l+2+2,len(kk)-1)])
    ptsf = ca.toShape().discretize(100)
    if not self.getData('hide'):
        displayline(self,ptsf,(1,1,0))
    
    sf=Part.BSplineCurve()
    sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)
    
    # alte anzahl wiederhrstellen
    if self.getData("preservePolesCount"):  
        for i in range(l):
            sf.insertKnot(p-3+(2*i+1)/(l+1),1)

    self.setPinObject('Shape_out',sf.toShape())
        


