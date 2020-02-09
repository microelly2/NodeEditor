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
from nodeeditor.utils import *
from nodeeditor.cointools import *
reload (nodeeditor.cointools)


def run_FreeCAD_Toy2(self):
    
    sayl()
    clearcoin(self)

    shape=self.getPinObject("Shape")
    if shape is None:
        sayErOb(self,"no Shape")
        return
    sf=shape.Face1.Surface
    say(sf)
    
    
    u=3.4
    v=4.2
    c=sf.uIso(u)
    #say("curve poles",c.getPoles())
    
    
    
    pol=sf.value(u,v)
    say("alter wert uv",pol)
    #displaysphere(self,pol,radius=4,color=(1,1,0))
    
    
    sf2=sf.copy
    target=pol+FreeCAD.Vector(self.getData('l'),0,self.getData('k')*10)
    start=target
    displaysphere(self,target,radius=4,color=(1,0,0))
    
    dirtt=(target-pol).normalize()
    
    say("target",target)
    say(sf.parameter(target))
    
    # daten holen und neu aufbauen
    ud=sf.UDegree
    vd=sf.VDegree
    ap=np.array(sf.getPoles())
    uk=np.array(sf.getUKnots())
    vk=np.array(sf.getVKnots())
    mu=np.array(sf.getUMultiplicities())
    mv=np.array(sf.getVMultiplicities())

    sppoles=ap[3:7,4:8].copy()
    #sppoles=ap[4:6,5:7].copy()
    
    
    def dist(x):
        t=x[0]
        
        sfa=Part.BSplineSurface()
        ap[3:7,4:8] = sppoles + dirtt*t
        sfa.buildFromPolesMultsKnots(ap,mu,mv,uk,vk,False,False,ud,vd)

        return sfa.toShape().distToShape(Part.Vertex(target))[0] 
    
    
    from scipy import optimize
    
    if 10:
        method='Powell'
        a=time.time()
        start=target
        result = optimize.minimize(dist, x0=[60],  method=method)
        

        say("quality",np.round(result.fun,5),np.round(result.x,2),result.message,method)
        say("run time for scipy.optimize.minimum",method,round(time.time()-a,3))

        tz=float(result.x) #[0]

    
    sfa=Part.BSplineSurface()
    ap=np.array(sf.getPoles())
    ap[3:7,4:8] = sppoles + dirtt*tz
    
    sfa.buildFromPolesMultsKnots(ap,mu,mv,uk,vk,False,False,ud,vd)
    dd=sfa.toShape().distToShape(Part.Vertex(target))[0] 
    say("Distance",dd)
    self.setPinObject('Shape_out',sfa.toShape())



def run_FreeCAD_Tape(self):
    
    hands=self.getPinByName('hands')
    
    outArray = []
    ySortedPins = sorted(hands.affected_by, key=lambda pin: pin.owningNode().y)

    l=self.getData('l')
    k=self.getData('k')*4
    #l=0.1
    pts=[]
    ptsa=[]
    #say(ySortedPins)
    say('#############')
    for i,h in  enumerate(ySortedPins):
        #say(h.getData())
        [p,tu,tv]=h.getData()
        if i==0:
            say(i,p)
            say(tu)
            say(tv)
            say()
        '''
        if i ==0:
            pts +=  [[p,p+k*tu,p+2*k*tu],[p+l*tv,p+l*tv+k*tu,p+l*tv+2*k*tu]]
        else:
            pts +=  [[p-l*tv,p-l*tv+k*tu,p-l*tv+2*k*tu],[p,p+k*tu,p+2*k*tu],[p+l*tv,p+l*tv+k*tu,p+l*tv+2*k*tu]]
        '''

        '''
        if i ==0:
            pts +=  [[p,p+k*tu,p+2*k*tu],[p+l*tv,p+l*tv+k*tu,p+l*tv+2*k*tu]]
        else:
            pts +=  [[p-l*tv,p-l*tv+k*tu,p-l*tv+2*k*tu],[p,p+k*tu,p+2*k*tu],[p+l*tv,p-l*tv+k*tu,p+l*tv+2*k*tu]]

        '''
        
        pts +=  [[p-l*tv,p-l*tv+k*tu],[p,p+k*tu],[p+l*tv,p+l*tv+k*tu]]
        
        ptsa=pts[1:]+[pts[0]]
        ptsa=pts
    
    say(np.array(pts).shape)
    self.setData('Points_out',ptsa)





# 19-22.01.2020
def run_FreeCAD_ReduceSurface(self):
    
    try:
        1/0
        if self.shape is None:
            1/0
        say(self.shape)
        sh=self.shape
    except:
        sh=self.getPinObject("Shape")
        self.shape=sh
    
    c=sh.Surface.copy()
   
    
    sfa=c.copy()
    sfb=c.copy()
    sfab=c.copy()    
    
    pts=np.array(c.getPoles())
    say("shape",np.array(pts).shape)
    
    pU=self.getData('startU')+1
    lU=self.getData('segmentsU')
    kkU=c.getUKnots()
    
    pV=self.getData('startV')+1
    lV=self.getData('segmentsV')
    kkV=c.getUKnots()
    
    
    pts=np.array(c.getPoles())
    A=pts[pU,pV].copy()
    B=pts[pU+lU+1,pV].copy()
    C=pts[pU,pV+lV+1].copy()
    D=pts[pU+lU+1,pV+lV+1].copy()
    
    VAB=np.array([0,0,20])
    VCD=np.array([0,0,20])
    VA=np.array([0,60,80])
    for u in range(0,lU+2):
        for v in range(0,lV+2):
            pts[pU+u,pV+v] = ( (A*(lU+1-u)+B*u)*(lV+1-v)+ (C*(lU+1-u)+D*u)*v)  /(lU+1)/(lV+1) 
            #pts[pU+u,pV+v] +=  (lU+1-u)*u/(lU+1)*(lV+1-v)*v/(lV+1)*VAB # center  
            pts[pU+u,pV+v] +=  (lU+1-u)*u/(lU+1)*VCD # innnelang
            pts[pU+u,pV+v] +=  u/(lU+1)*v/(lV+1)*VA # corner
    
    #pts[pU:pU+lU+1,pV:pV+lV+1]=newpoles[pU:pU+lU+1,pV:pV+lV+1]
    #pts[rpU:rpU+lU+1,rpV:rpV+lV+1]=newpoles[rpU:rpU+lU+1,rpV:rpV+lV+1]
    (countA,countB,_)=pts.shape
    degA=degB=3

    multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
    multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
    knotA=range(len(multA))
    knotB=range(len(multB))

    sfq=Part.BSplineSurface()
    sfq.buildFromPolesMultsKnots(pts,multA,multB,knotA,knotB,False,False,degA,degB)
    shapeAAA=sfq.toShape()
    self.setPinObject("Shape_out",shapeAAA)
    self.setData('points',pts.tolist())
    return

    
    
    

    
    
    
    #--------------------------------
    
    clearcoin(self)

    #lU=1;    lV=1;    sayW("hack set lUlV 1")
    
    if lU == -1 or lV==-1:
        self.setPinObject('Shape_out',sh)
        return
    sayl()
    if not self.getData('hide') and self.getData('useStartPosition'):
            say("2 shepres")
            displaysphere(self,c.value(kkU[max(0,pU-4)],kkV[max(0,pV-4)]),radius=4,color=(0,1,1))
    
    
    say("intervall",pU,lU,pV,lV)
    pa=np.concatenate([pts[:pU],pts[pU+lU:]]).swapaxes(0,1)
    poles=np.concatenate([pa[:pV],pa[pV+lV:]]).swapaxes(0,1)
    say("ploes neu",poles.shape)
    


    #s=Part.makePolygon(poles)
    
       
    
    '''
    #deaktivert vorest
    if self.getData('useStartPosition'):
        pp=self.getData('position')
    else:
        if l==0:
            pp=pts[p]
        else:
            pp=Part.makePolygon(pts[p:p+l+1]).CenterOfMass
    '''
    
    m1=self.getData('Move1')
    m2=self.getData('Move2')
    m3=self.getData('Move3')

    
    rpU=max(0,pU-4)
    rpV=max(0,pV-4)
    
    if lU == 0 and lV ==0:
        target=pts[pU,pV]
    else:
        if self.getData('usePositionAsAbsolute'):
            target=self.getData('position')    
        else:
            #target=Part.makePolygon(pts[p:p+l+1]).CenterOfMass+self.getData('position') 
            ptsa=pts.swapaxes(0,1)
            
            target=np.array([[
            np.sum(pts[rpU:rpU+lU+1,k,0]),
            np.sum(pts[rpU:rpU+lU+1,k,1]),
            np.sum(pts[rpU:rpU+lU+1,k,2])] for k in range(0,pts.shape[1])])
            target=np.array([[
            np.sum(pts[rpU+1:rpU+lU+2,k,0]),
            np.sum(pts[rpU+1:rpU+lU+2,k,1]),
            np.sum(pts[rpU+1:rpU+lU+2,k,2])] for k in range(0,pts.shape[1])])
            
            
            target /= (lU+2)
    
    
    
    target+=FreeCAD.Vector(m1,m2,m3)

    self.setPinObject("Shape_out",Part.makePolygon([FreeCAD.Vector(tt) for tt in target]))
    #return
    
    # die segemente anreichern
    col=[]
    newpoles=[]
    for k in range(0,pts.shape[1]):
        
        polesA=np.concatenate([pts[:rpU,k],[target[k]],pts[rpU+lU+1:,k]])
        
        countA=len(polesA)
        degA=3
        periodic=False
        
        if not periodic:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))
        else:
            multA=[1]*(countA+1)
            knotA=range(len(multA))

        #polesA=[p+FreeCAD.Vector(0,0,10) for p in poles]  
        #poles=polesA
        
        
        bc=Part.BSplineCurve()
        
        bc.buildFromPolesMultsKnots(polesA,multA,knotA,periodic,degA)
        for i in range(lU):
            bc.insertKnot(rpU-2+(2*i+1)/(lU+1),1)
            pass

        newpoles += [bc.getPoles()]
        say(len(bc.getPoles()))
        col += [bc.toShape()]
        
    say("shape", np.array(newpoles).shape)
    newpoles=np.array(newpoles).swapaxes(0,1)
    self.setPinObject("Shape_out",Part.makeCompound(col))
    #return
    
    
    
    pts=np.array(c.getPoles())
    #pts[pU:pU+lU+1,pV:pV+lV+1]=newpoles[pU:pU+lU+1,pV:pV+lV+1]
    pts[rpU:rpU+lU+1,rpV:rpV+lV+1]=newpoles[rpU:rpU+lU+1,rpV:rpV+lV+1]
    (countA,countB,_)=pts.shape
    degA=degB=3

    multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
    multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
    knotA=range(len(multA))
    knotB=range(len(multB))

    sfq=Part.BSplineSurface()
    sfq.buildFromPolesMultsKnots(pts,multA,multB,knotA,knotB,False,False,degA,degB)
    shapeAAA=sfq.toShape()
    self.setPinObject("Shape_out",shapeAAA)
    self.setData('points',pts.tolist())
    return

    # andere richtung ------------------------------
    target=np.array([[
    np.sum(pts[k,rpV+1:rpV+lV+2,0]),
    np.sum(pts[k,rpV+1:rpV+lV+2,1]),
    np.sum(pts[k,rpV+1:rpV+lV+2,2])] for k in range(0,pts.shape[0])])

    target /= (lV+1)
    say(pts.shape)
    say(rpV,lV)
    say("!sd!",target.shape)
    self.setPinObject("Shape_out",Part.makePolygon([FreeCAD.Vector(tt) for tt in target]))
    #return

    pts=pts.swapaxes(0,1)
    

    # die segemente anreichern
    col=[]
    newpoles=[]
    for k in range(0,pts.shape[0]):
        
        polesA=np.concatenate([pts[:rpV,k],[target[k]],pts[rpV+lV+1:,k]])
        #polesA=np.concatenate([pts[:rpV,k],pts[rpV+lV+1:,k]])
        
        countA=len(polesA)
        degA=3
        periodic=False
        
        if not periodic:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))
        else:
            multA=[1]*(countA+1)
            knotA=range(len(multA))

        #polesA=[p+FreeCAD.Vector(0,0,10) for p in poles]  
        #poles=polesA
        
        
        bc=Part.BSplineCurve()
        
        bc.buildFromPolesMultsKnots(polesA,multA,knotA,periodic,degA)
        #say("iserts",bc.getKnots())
        #say(rpV,lV)
        #say(rpV-2+(2*i+1)/(lV+1))
        for i in range(lV):
            bc.insertKnot(rpV-2+(2*i+1)/(lV+1),1)
            pass

        newpoles += [bc.getPoles()]
        say(len(bc.getPoles()))
        col += [bc.toShape()]
        
    say("shape", np.array(newpoles).shape)
    #newpoles=np.array(newpoles).swapaxes(0,1)
    newpoles=np.array(newpoles)
    self.setPinObject("Shape_out",Part.makeCompound(col))
    #return
    
    
    say("newpoles shape",newpoles.shape)
    pts=np.array(c.getPoles())
    #pts[pU:pU+lU+1,pV:pV+lV+1]=newpoles[pU:pU+lU+1,pV:pV+lV+1]
    pts[rpU:rpU+lU+1,rpV:rpV+lV+1]=newpoles[rpU:rpU+lU+1,rpV:rpV+lV+1]
    (countA,countB,_)=pts.shape
    degA=degB=3

    multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
    multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
    knotA=range(len(multA))
    knotB=range(len(multB))

    sfq=Part.BSplineSurface()
    sfq.buildFromPolesMultsKnots(pts,multA,multB,knotA,knotB,False,False,degA,degB)
    shape=sfq.toShape()
    self.setPinObject("Shape_out",shape)
    return

    
    






    
    
    

    strat=self.getData("Strategy")
    strat = 'Center of Mass' # hack
    
    ptsA=poles[rpU]
    ptsB=poles.swapaxes(0,1)[rpV]

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

    '''
    if  strat != 'Point':
        if lU==0:
            tang=pts[p-1]-pts[p+1]
        else:
            tang=pts[p]-pts[p+l]
        
        norm=FreeCAD.Vector(-tang.y,tang.x)
        pp += -m1*tang/100 +m2*norm/100
    '''
    
    pp=FreeCAD.Vector(m1,m2,m3)
    
    say("build poles---------------------")
    if lU != 0:
        polesA=np.concatenate([ptsA[:pU-1],[pp],ptsA[pU+lU:]])
    else:
        polesA=ptsA[:pU]+[pp]+ptsA[pU+1:]
    
    say("pts,poles,l",len(ptsA),len(polesA),lU)
    
    if pU+lU==len(ptsA):
        polesA=ptsA[:pU-1]+[ptsA[-1]]
    
    
    #mpoints=pts[p:p+l]
    
    countA=len(polesA)
    degA=3
    periodic=False
    
    if not periodic:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        knotA=range(len(multA))
    else:
        multA=[1]*(countA+1)
        knotA=range(len(multA))

    
    sf=Part.BSplineCurve()
    sf.buildFromPolesMultsKnots(polesA,multA,knotA,periodic,degA)

    say(target)
    say("-----------------",sf)
    self.setPinObject('Shape_out',sf.toShape())
    return
    
    #tv=sf.parameter(target)
    #tang=sf.tangent(tv)
    
    #dird=FreeCAD.Vector(np.cos(m1/100.*np.pi),np.sin(m1/100.*np.pi))
    #tdd=dird.dot(tang[0])

    #say("lenght dist",sf.toShape().Length,sf.toShape().distToShape(Part.Vertex(target))[0])
    
    
    kks=sf.getKnots()   
    pointsAAA= [sf.value(t) for t in range(max(0,pU-4),min(pU+1,len(kks)))]
    if not self.getData('hide'):
        displaysphere(self,pointsAAA[0],radius=6,color=(0,1,0))
        displaysphere(self,pointsAAA[-1],radius=6,color=(0,1,0))
    if lU ==0:
        pointsAAA += [c.value(kkU[t],rpU) for t in range(max(0,pU-4),min(pU+lU+1,len(kkU)))]
    else:    
        pointsAAA += [c.value(kkU[t],rpU) for t in range(max(0,pU-4),min(pU+lU,len(kkU)))]
    self.setData('points',[pointsAAA,pointsAAA])
    
    if not self.getData('hide'):
        displayspheres(self,pointsAAA,radius=4,color=(0,1,1))
    
    
    self.setPinObject("Shape_out",Part.makePolygon(pointsAAA))
    sayW("abbruch");return    
    
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
        
       



def run_commitFF(self):
        self.shape=self.getPinObject("Shape_out")
        say("nicht --------------------- impl")
        a=self.getData('start')
        b=self.getData('segments')
        ax=self._wrapper.UIinputs
        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='segments':
                say("AA")
                p.setData(0)
            if p.name=='Move1':
                say("BB")
                p.setData(0)

            if p.name=='Move2':
                say("CC")
                p.setData(0)
        for i,j in enumerate(ax):
            p=ax[j]
            if p.name=='start':
                say("DD")
                p.setData(a+4)
        #self.setPinObject('Shape_out',self.shape)
        say("vor compute--------------------")
        self.compute()
        say("nach compute--------------------")
        self.outExec.call()


    
    


from inspect import signature
def run_FreeCAD_Toy3(self):
    dit=self.getData('data')
    say(dit)
    
    def myf(einezahl,anderezahl,a,b=3):
        say("MYF einz",einezahl)
        say("andnz",anderezahl)
        return einezahl +anderezahl
    
    _f=myf
    
    for k in dit:
        say(k)
        say(dit[k])
        say()
        exec(k+"=dit['"+k+"']")
        say(k,"--",eval(k))
    
    say("!!",eval(k),k)
    exec("uu=12")
    say(uu)
    return
    
    sig = str(signature(_f))
    zz="myf"   +sig
    zz="lambda x: _f"   +sig
    say(zz)
    rc=eval(zz)
    say(einezahl)
    say(_f)
    #say("rc--",rc)
    #rc(45)
    return
    
    say("sig",sig)
    #einezahl=dit['einezahl']
    t=dit['einezahl']
    say("t",t)
    exec("xx=5")
    say(xx)
    say('lllllll')
    say("einezahl",einezahl)
    
    ff=lambda x: myf(x,dit['anderezahl'])
    x2=dit['anderezahl']
    ff=lambda x1: myf(x1,x2)
    say("ff(8)",ff(8))
    






def run_FreeCAD_Toy3(self):
    say(noto)
    d=[[1,2,3],[4,5,6,6,7,8]]
    #d=[1,2,3,4,5,6]
    #d=[1,2,3]
    rc=noto.data2vecs(d)
    say(rc)
    bs=noto.createBSplineSurface()
    self.setPinObject("Shape1", bs.toShape())
    

def run_FreeCAD_Toy3(self):
    # testdaten fuer toponaming

    pts=[
    [0,0,0],[10,0,0],[10,5,0],[0,5,0],
    [0,0,15],[10,0,15],[10,5,15],[0,5,10]
    ]

    if 1:
        [A,B,C,D,E,F,G,H]=[FreeCAD.Vector(p) for p in pts]
        col=[Part.makePolygon(l) for l in [[A,B],[B,C],[C,D],[D,A],
                [E,F],[F,G],[G,H],[H,E],
                [A,E],[B,F],[C,G],[D,H]]]
        
        Part.show(Part.Compound(col))




#---------------------------
#---------------------------
from nodeeditor.say import *
import FreeCAD
import Part 
import numpy as np


class TopVertex(object):
    
    def __init__(self):
        sayl()
        self.vs={}
        self.ehs={}
        self.igel={}
        
    def pkey(self,p):
        return tuple((round(p.x,2),round(p.y,2),round(p.z,2)))

    def addVertex(self,v):
        self.vs[self.pkey(v.Point)]=v
        self.ehs[self.pkey(v.Point)]=[]
        self.igel[self.pkey(v.Point)]=[]

    def addEdge(self,e):
        p1k=self.pkey(e.Vertexes[0].Point)
        p2k=self.pkey(e.Vertexes[1].Point)
        [start,ende]=e.ParameterRange
        t1=e.tangentAt(start)
        t2=e.tangentAt(ende)
        dirchange=t1.dot(t2)
        val=[tuple((round((e.Vertexes[0].Point-e.Vertexes[1].Point).Length,2),round(dirchange,2)))]
        self.ehs[p1k] += val
        self.ehs[p2k] += val
        if (e.Vertexes[0].Point+t1-e.Vertexes[1].Point).Length<(e.Vertexes[0].Point-e.Vertexes[1].Point).Length:
            self.igel[p1k] += [t1]
        else:
            self.igel[p1k] += [-t1]

        if (e.Vertexes[0].Point-t1-e.Vertexes[1].Point).Length<(e.Vertexes[0].Point-e.Vertexes[1].Point).Length:
            self.igel[p2k] += [t2]
        else:
            self.igel[p2k] += [-t2]
        
        # self.igel[p2k] += [t2]
        
    def getEdgekeys(self):
        kks=[]
        

        
        for k in self.ehs:
            R=np.array(self.ehs[k]).swapaxes(0,1)
            aa=np.lexsort((R[1],R[0]))
            R2=np.array([(R[0,i],R[1,i]) for i in aa]).tolist()
            R2=[tuple(r) for r in R2]

            kks += [tuple(R2)]
        return kks
            
    def run(self):
        say("run igels ")

        for v in self.vs:
            say(v,self.igel[v])
        
        say("run done")
    
    
def run_FreeCAD_Topo2(self):
    sayl()
    
    
    tv=TopVertex()
    
    shape=FreeCAD.ActiveDocument.Box.Shape
    for v in shape.Vertexes:
        tv.addVertex(v)

    for e in shape.Edges:
        FreeCAD.e=e
        tv.addEdge(e)



    
    tv2=TopVertex()
    shape2=FreeCAD.ActiveDocument.Shape.Shape
    for v in shape2.Vertexes:
        tv2.addVertex(v)

    for e in shape2.Edges:
        FreeCAD.e=e
        tv2.addEdge(e)

    
    
    say("Asuwertung edgehash auftreten - welceh verschiedenen ecken gibt es")
    say("teil 1")
    eks={}
    ks=tv.getEdgekeys()
    for k in ks:
        try:
            eks[k] += 1
        except:
            eks[k] = 1
        
    for k in eks:
        say(k,eks[k])

        
    say("teil 2")
    eks={}
    ks=tv2.getEdgekeys()
    
    for k in ks:
        try:
            eks[k] += 1
        except:
            eks[k] = 1
        
    for k in eks:
        say(k,eks[k])
    
    
    
    
    akeys=[k for k in tv.igel.keys()]
    bkeys=[k for k in tv2.igel.keys()]

    aix=self.getData('vertexA')%len(akeys)
    bix=self.getData('vertexB')%len(bkeys)

    pA=akeys[aix]
    pB=bkeys[bix]

    
    vlA=[]
    for v in tv.igel[pA]:
        if v not in vlA:
            vlA += [v]

    vlB=[]
    for v in tv2.igel[pB]:
        if v not in vlB:
            vlB += [v]




    perms=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]] 
    
    selA=self.getData('selA')
    
    selAs=[selA]
    selAs=range(36)
    
    
    bests=[]
    besterr=1000

    clearcoin(self)
        
    def runsel(selA,lang=True):
        
        ata=time.time()
        
        iA=selA%6
        iB=selA//6

        [i0,i1]=perms[iA]   
        aa,bb = vlA[i0],vlA[i1]
        cc=aa.cross(bb)
        bb=cc.cross(aa)
        aaA,bbA,ccA=aa,bb,cc
        vvA=FreeCAD.Matrix(aa.x,aa.y,aa.z,0,  bb.x,bb.y,bb.z,0 , cc.x,cc.y,cc.z,0, 0,0,0,1)


        [i0,i1]=perms[iB]
        aa,bb = vlB[i0],vlB[i1]
        cc=aa.cross(bb)
        bb=cc.cross(aa)
        aaB,bbB,ccB=aa,bb,cc
        
        vvB=FreeCAD.Matrix(aa.x,aa.y,aa.z,0,  bb.x,bb.y,bb.z,0 , cc.x,cc.y,cc.z,0, 0,0,0,1)

        vv=vvB.inverse()*vvA
        

        if not lang:
            clearcoin(self)
            say("display")
            target=FreeCAD.Vector(pA)
            displaysphere(self,target,radius=0.5,color=(1,0,0))
            displayline(self,[target,target+aaA*4],(1,1,0))
            displayline(self,[target,target+bbA*4],(0,1,0))
            displayline(self,[target,target+ccA*4],(1,0,0))
            
            target=FreeCAD.Vector(pB)
            displaysphere(self,target,radius=0.5,color=(0,0,1))
            displayline(self,[target,target+aaB*4],(1,1,0))
            displayline(self,[target,target+bbB*4],(0,1,0))
            displayline(self,[target,target+ccB*4],(1,0,1))


        #verschiebung
        t4=FreeCAD.Matrix(1,0,0,pB[0],  0,1,0,pB[1],  0,0,1,pB[2], 0,0,0,1)
        t2=FreeCAD.Matrix(1,0,0,-pA[0],  0,1,0,-pA[1],  0,0,1,-pA[2], 0,0,0,1)

        
        shape=FreeCAD.ActiveDocument.Box.Shape.copy()

        pm=FreeCAD.ActiveDocument.Box.Placement
        
        pmm=pm.toMatrix()
        
        st4=shape.transformGeometry(t4*vv*t2)
        st5=st4.transformGeometry(pmm)
        #st5=shape.transformGeometry(pmm*t4*vv*t2)
        #say("st5 pm",st5.Placement)
        
        
        if not lang:
            
            '''
            a=FreeCAD.ActiveDocument.getObject("huhu")
            if a is None:
                a=FreeCAD.ActiveDocument.addObject("Part::Feature","huhu")
        
            a.Shape=st4
            #a.Placement=FreeCAD.Placement()
            '''
            self.setPinObject('Shape_out',st5)
        
        errs=0
        
        for v in st4.Vertexes:
            #print (v.Point)
            pk=tv2.pkey(v.Point)
            try:
                tv2.vs[pk]
            except:
                if not lang:
                    say("nicht gefundener Ecke ",pk)
                errs += 1
        #say("Abweichungen",selA,errs)
        
        return errs
            
    single=self.getData('singleIndex')
    
    if not single:
        for selA in selAs:
            a=time.time()
            errs=runsel(selA,True)
            if errs == besterr:
                bests += [selA]
            elif errs<besterr:
                besterr=errs
                bests = [selA]
        
        say(len(selAs))
        say("Transformationen ...")
        say("BESTE Abweichung",besterr,"fuer index:",bests)
        
        runsel(bests[0],False)

    else:
        runsel(self.getData('selA'),False)
    
    
    
    
    
def run_FreeCAD_elastic(self):  
    
    
    
    try:
        if time.time() - self._lastrun <1:
            sayErr("laueft noch")
            return
    except:
        self._lastrun=time.time()
    
    self._lastrun=time.time()
    say(self._lastrun,'##########################')
    
    

    eng=30
    bfak=30
    fofaktor=1/(1+(self.getData('b')+100)/10)
    #fofaktor=1
    
    
    b=500
    a=20
    a=20

    def force(point,pts):
        
        p=pts[0]
        rc=FreeCAD.Vector()
        for p in pts:
            dd=(point-p)
            l=dd.Length
            if l==0:
                continue
            #if l <0.00001:
            #   continue
            #b=500
            #a=20
            c=0.05
            c=0.005
            eng=25
            #eng=10
            
            eng=40
            if l<eng:
                f=l*0.05
                #say("eng",l)
                f=4
            else:
                f=c*(a/l-b)
                #f=c*(a/l**2.01-b)
#           say("f--",abs(f))
            if abs(f)<2: f=0
            
            rc += dd.normalize()*f
            l=rc.Length
            #if l>bfak:
            #   #say("reducen",l,bfak)
            #   rc *= bfak/l
        return rc
        
        
        

    a=self.getData('a')+101
    say('a',a)
    
    

    sayl()
    clearcoin(self)
    
    pts=self.getData('fixpoints')
    say(pts)
    if len(pts)==0:
        pts=[
            FreeCAD.Vector(200,0,-0),
            FreeCAD.Vector(100,200,-100),
            FreeCAD.Vector(50,200),
            FreeCAD.Vector(100,-50,100)
            ]
    
    
    pts2=self.getData('points')
    if len(pts2) == 0:
        
        pts2=[FreeCAD.Vector(0,0,100),
            FreeCAD.Vector(100,-100),FreeCAD.Vector(0,30),
            FreeCAD.Vector(-100,100),
            ]

        pts2=[-FreeCAD.Vector(250,250,250)
            +FreeCAD.Vector(random.random(),random.random(),random.random())*500 for i in range(5)]
    try:
        (sa,sb,sc)=np.array(pts2).shape
        pts2=[FreeCAD.Vector(a) for a in np.array(pts2).reshape(sa*sb,3)]
    except:
        pass
    #return
    
    
    
    ptsm=pts2
    #displayline(self,pts)
    #displayline(self,pts2)
    
    
    for p in pts:
        displaysphere(self,p,radius=4.5,color=(1,0,1))
    point=FreeCAD.Vector()
    
    tracks=[pts2]
    
    for j in range(a):
        if 0 and j%50==0:
            #clearcoin(self)
            for p in pts:
                displaysphere(self,p,radius=.5,color=(1,0,1))

        
        
        if self.getData('animate'):
            FreeCADGui.updateGui()
            time.sleep(0.01)
        pts3=[]
        #say("j",j)
        for i,point in enumerate(pts2):
            f =force(point,pts+pts2[:i]+pts2[i+1:])
            
            
            point += f * fofaktor
            
            pts3 += [point]

        #say("aenderungne")
        pts3n=[]
        mods=False
        
        for p2,p3 in zip(ptsm,pts3):
            if (p2-p3).Length>8*fofaktor:
                pts3n += [p3]
                mods=True
            else:
                pts3n += [p2]

        pts3=pts3n
        for p2,p3 in zip(pts2,pts3):
            #say([p2,p3])
            displayline(self,[p2,p3],color=(1,0,0))
            displaysphere(self,p2,radius=0.3,color=(1,0,0))
        #say()
        ptsm=[(pm+p2+p3)/3 for pm,p2,p3 in zip(ptsm,pts2,pts3)]
        pts2=pts3
        #say("MOFD",mods,j)
        tracks +=[pts2]
        if not mods:
            break
        
    say("Ende")

    for point in pts2:
        # abstand kraft 0 25 --> hilfs huelle 12.5
        r=min(0.5*b/a,5)
        
        displaysphere(self,point,radius=r,color=(0,0,1))
    
    say("tracks",np.array(tracks).shape)
    FreeCAD.Tracks=tracks
    self.setData("Points_out",pts2)
        

    if 0:
        pts=[t[6] for t in tracks]
        bs=Part.BSplineCurve()
        uc=len(pts)
        say("uc",uc)
        udegree=25
        umults=[udegree+1]+[1]*(uc-1-udegree)+[udegree+1]   
        uknots=range(len(umults))
        bs.buildFromPolesMultsKnots(pts,umults,uknots,False,udegree)
                
        Part.show(bs.toShape())

    if self.getData('hide'):
        clearcoin(self)
    self._lastrun=0
