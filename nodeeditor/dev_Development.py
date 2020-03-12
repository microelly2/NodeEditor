
import FreeCAD
import Part 

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


# print ("reloaded: "+ __file__)

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

    pts=[]
    ptsa=[]


    for i,h in  enumerate(ySortedPins):

        [p,tu,tv]=h.getData()

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
    
    sayl()
    
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


def run_FreeCAD_Toy3(self):
		sayl()
		dat=self.getData("data")
		say(dat)
		




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





def run_FreeCAD_Forum(self):
    import time
    sayl()
    say(time.time())
    url='http://forum.freecadweb.org/search.php?search_id=active_topics'
    


    import urllib.request
    import re,time


    try:
        _=self.hash
    except:
        self.hash={}
        self.last=time.time()

    response = urllib.request.urlopen(url)
    ans=response.read()
    for i,l in enumerate(ans.splitlines()):     
        if  'class="topictitle">' in str(l):
            #print(l)
            #print ("")
            m = re.search('topictitle">(.*)</a>', str(l))
            title = m.group(1)
            #print("--",title)
            
        elif  'username">' in str(l) or 'username-coloured">' in str(l):
            #say(l)
            if  'username">' in str(l):
                m = re.search('username">(.+?)</a> &raquo;(.+?)&raquo;', str(l))
                if m is None: 
                    pass
                    #print("----------",m) 
                else:
                    name = m.group(1)

                    date = m.group(2)
                    
                    #print(name,date)
            
            else:
            
                m = re.search('username-coloured">(.+?)</a> &raquo;(.+?)&raquo;', str(l))
                if m is None: 
                    pass
                    #print("----------",m) 
                else:
                    name = m.group(1)

                    date = m.group(2)
                    
                    #print("!!",name,date)
            
            
            
            
            
            try:
                _=self.hash[(title+name+date)]
#               say()
                
            except:
                if 0:
                    sayW(title)
                    say("by {}  ({})".format(name,date))
                self.setData("news",str((title,name,date)))
                self.outExec.call()
                self.hash[(title+name+date)]=time.time()
                self.last=time.time()

    self.setColor()


def NON(a):
    return None

def STRING(a):
    return a
     
def INT(a):
    return int(a);

def REFLIST(a):
    return [v for v in a]   

def INTLIST(a):
    return [int(v) for v in a]  

def FLOATLIST(a):
    return [float(v) for v in a]  


class Config(object):
    config = None

    def __init__(self):
        self.config = {}

    def __setattr__(self, key, value):
        if self.config is None:
            super(Config, self).__setattr__(key, value)
            return
        self.config[key] = value

    def __getattr__(self, key):
       return self.config[key]

    def __setitem__(self, key, value):
            self.config[key] = value

    def __getitem__(self, key):
            return self.config[key]

def params2obj(idd,data):

    vals=Config()
    pclass= None # data[0]
    
    params=data[1]
    
   
    if data[0]=='B_SPLINE_CURVE_WITH_KNOTS':
        
            pclass=data[0].lower()
            
            dat={
            "descript":STRING,
            "deg":INT,
            "poles":REFLIST,
            '_3':NON,
            '_4':NON,
            '_5':NON,
            "mults":INTLIST,
            "knots":FLOATLIST,
            }
            
            for i,k in enumerate(dat):
                vals[k]=dat[k](params[i])
                # poles=[pol for pol in params[2]]
            
            for k in dat:
                say(k,vals[k])

            say(vals.descript)

    return pclass,vals
    



def run_FreeCAD_StepData(self,*args,**kvals):
    
    sayl()

    #------------------------


    # Copyright (c) 2011, Thomas Paviot (tpaviot@gmail.com)
    # All rights reserved.

    # This file is part of the StepClassLibrary (SCL).
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions are met:
    #
    #   Redistributions of source code must retain the above copyright notice,
    #   this list of conditions and the following disclaimer.
    #
    #   Redistributions in binary form must reproduce the above copyright notice,
    #   this list of conditions and the following disclaimer in the documentation
    #   and/or other materials provided with the distribution.
    #
    #   Neither the name of the <ORGANIZATION> nor the names of its contributors may
    #   be used to endorse or promote products derived from this software without
    #   specific prior written permission.

    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    # AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    # ARE DISCLAIMED.
    # IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
    # DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    # THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    def process_nested_parent_strV1(attr_str,idx=0):
        '''
        The first letter should be a parenthesis
        input string: "(1,4,(5,6),7)"
        output: ['1','4',['5','6'],'7']
        '''
        say("**",attr_str)
        ma=re.match("([^\(]*)\((.*)\)([^\(]*)$",attr_str)
        if 0 and ma is not None:
            say("match pattern")
            say(ma.group(1))
            say(ma.group(2))
            say(ma.group(3))
        
        params = []
        current_param = ''
        k = 0
        while (k<len(attr_str)):
            ch = attr_str[k]
            k += 1
            if ch==',':
                params.append(current_param)
                current_param = ''
            elif ch=='(':
                nv = attr_str[k:]
                current_param2, progress = process_nested_parent_str(nv)
                say("got from inner call",current_param2)
                params.append(current_param2)
                say("params --",params)
                current_param = ''
                k += progress+1
            elif ch==')':
                params.append(current_param)
                say("k",k)
                return params,k
            else:
                current_param += ch
        params.append(current_param)
        say("done")
        return params,k

    def process_nested_parent_str(attr_str,idx=0):
        '''
        The first letter should be a parenthesis
        input string: "(1,4,(5,6),7)"
        output: ['1','4',['5','6'],'7']
        '''
        #say("**",idx,"---",attr_str)
        ma=re.match("([^\(]*)\((.*)\)([^\(]*)$",attr_str)
        if 0 and ma is not None:
            say("match pattern")
            say(ma.group(1))
            say(ma.group(2))
            say(ma.group(3))
        
        
        params = []
        current_param = ''
        k = 0
        new_str=['"']
        while (k<len(attr_str)):
            ch = attr_str[k]
            k += 1
            if ch==',':
                if new_str[-1] ==']' or new_str[-1] =='"' :
                    new_str += [',','"']
                  
                else:
                    new_str += ['"',',','"']
            elif ch=='(':
                new_str[-1]=' ' 
                new_str += ['[',' ','"']
            elif ch==')':
                if new_str[-1] ==']':
                    new_str += [']']
                else:
                    new_str +=  ['"',']']
            else:
                new_str  += [ch]
        if new_str[-1] !=']':
            new_str += '"'
        new_str="".join(new_str)
        
        #say("done",new_str)
        try:
            hh=eval(new_str)
            say(hh)
        except:
            hh=[]
        #say(len(hh))
        return hh,len(hh)



    #---------------------------
    import re
    # from . import Utils
    import time


    INSTANCE_DEFINITION_RE = re.compile("#(\d+)[^\S\n]?=[^\S\n]?(.*?)\((.*)\)[^\S\n]?;[\\r]?$")

    def map_string_to_num(stri):
        """ Take a string, check whether it is an integer, a float or not
        """
        if ('.' in stri) or ('E' in stri): #it's definitely a float
            return REAL(stri)
        else:
            return INTEGER(stri)

    class Model:
        """
        A model contains a list of instances
        """
        def __init__(self,name):
            self._name = name
            # a dict of instances
            # each time an instance is added to the model, count is incremented
            self._instances = {}
            self._number_of_instances = 0

        def add_instance(self, instance):
            '''
            Adds an instance to the model
            '''
            self._number_of_instances += 1
            self._instances[self._number_of_instances-1] = instance

        def print_instances(self):
            '''
            Dump instances to stdout
            '''
            for idx in range(self._number_of_instances):
                "=========="
                print("Instance #%i"%(idx+1))
                print(self._instances[idx])

    class Part21EntityInstance:
        """
        A class to represent a Part21 instance as defined in one Part21 file
        A Part21EntityInstance is defined by the following arguments:
        entity_name: a string
        entity_attributes: a list of strings to represent an attribute.
        For instance, the following expression:
        #4 = PRODUCT_DEFINITION_SHAPE('$','$',#5);
        will result in :
        entity : <class 'config_control_design.product_definition_shape'>
        entity_instance_attributes: ['$','$','#5']
        """
        def __init__(self,entity_name,attributes):
            self._entity
            self._attributes_definition = attributes
            print(self._entity_name)
            print(self._attributes_definition)


    class Part21Parser:
        """
        Loads all instances definition of a Part21 file into memory.
        Two dicts are created:
        self._instance_definition : stores attributes, key is the instance integer id
        self._number_of_ancestors : stores the number of ancestors of entity id. This enables
        to define the order of instances creation.
        """
        def __init__(self, filename):
            self._filename = filename
            # the schema
            self._schema_name = ""
            # the dict self._instances contain instance definition
            self._instances_definition = {}
            # this dict contains lists of 0 ancestors, 1 ancestor, etc.
            # initializes this dict
            #self._number_of_ancestors = {} # this kind of sorting don't work on non-trivial files
            #for i in range(2000):
            #    self._number_of_ancestors[i]=[]
            self.parse_file()
            # reduce number_of_ancestors dict
            #for item in self._number_of_ancestors.keys():
            #    if len(self._number_of_ancestors[item])==0:
            #        del self._number_of_ancestors[item]

        def get_schema_name(self):
            return self._schema_name
            print(schema_name)

        def get_number_of_instances(self):
            return len(list(self._instances_definition.keys()))

        def parse_file(self):
            init_time = time.time()
            print("Parsing file %s..."%self._filename)
            fp = open(self._filename)
            while True:
                line = fp.readline()
                if not line:
                    break
                # there may be a multiline definition. In this case, we read lines until we found
                # a ;
                while (line.find(';') == -1): #it's a multiline
                    line = line.replace("\n","").replace("\r","") + fp.readline()
                
                for i in range(20): #hack !! g/ //
                    line=line.replace(" ","")

                # parse line
                match_instance_definition = INSTANCE_DEFINITION_RE.search(line)  # id,name,attrs
                if match_instance_definition:
                    instance_id, entity_name, entity_attrs = match_instance_definition.groups()
                    instance_int_id = int(instance_id)
                    # find number of ancestors
                    #number_of_ancestors = entity_attrs.count('#')
                    # fill number of ancestors dict
                    #self._number_of_ancestors[number_of_ancestors].append(instance_int_id) # this kind of sorting don't work on non-trivial files
                    # parse attributes string
                    #say(entity_name)
                    #say("!! in ",entity_attrs)
                    
                    entity_attrs_list, str_len = process_nested_parent_str(entity_attrs)
                    #say("!! rc ",entity_attrs_list)
                    #if entity_name.startswith("B_SPLINE_S"):
                    #    return
                        
                    # then finally append this instance to the disct instance
                    self._instances_definition[instance_int_id] = (entity_name,entity_attrs_list)
                else: #does not match with entity instance definition, parse the header
                    if line.startswith('FILE_SCHEMA'):
                        #identify the schema name
                        self._schema_name = line.split("'")[1].split("'")[0].split(" ")[0].lower()
            fp.close()
            print('done in %fs.'%(time.time()-init_time))
            print('schema: - %s entities %i'%(self._schema_name,len(list(self._instances_definition.keys()))))

    class EntityInstancesFactory(object):
        '''
        This class creates entity instances from the str definition
        For instance, the definition:
        20: ('CARTESIAN_POINT', ["''", '(5.,125.,20.)'])
        will result in:
        p = ARRAY(1,3,REAL)
        p.[1] = REAL(5)
        p.[2] = REAL(125)
        p.[3] = REAL(20)
        new_instance = cartesian_point(STRING(''),p)
        '''
        def __init__(self, schema_name, instance_definition):
            # First try to import the schema module
            pass

    class Part21Population(object):
        def __init__(self, part21_loader):
            """ Take a part21_loader a tries to create entities
            """
            self._part21_loader = part21_loader
            self._aggregate_scope = []
            self._aggr_scope = False
            self.create_entity_instances()

        def create_entity_instances(self):
            """ Starts entity instances creation
            """
            for number_of_ancestor in list(self._part21_loader._number_of_ancestors.keys()):
                for entity_definition_id in self._part21_loader._number_of_ancestors[number_of_ancestor]:
                    self.create_entity_instance(entity_definition_id)

        def create_entity_instance(self, instance_id):
            instance_definition = self._part21_loader._instances_definition[instance_id]
            print("Instance definition to process",instance_definition)
            # first find class name
            class_name = instance_definition[0].lower()
            print("Class name:%s"%class_name)
            object_ = globals()[class_name]
            # then attributes
            #print object_.__doc__
            instance_attributes = instance_definition[1]
            print("instance_attributes:",instance_attributes)
            a = object_(*instance_attributes)

    if self.getData("process"):
    
        pts=[]
        vals={}
        col=[]
        
        for idd in  self.p21loader._instances_definition:
            pclass,pval=params2obj(idd,self.p21loader._instances_definition[idd])
            if pclass is not None:
                say(idd,"got",pclass,pval)
            continue
            
            
            
        '''    
            t=self.p21loader._instances_definition[idd]
            if t[0]=='CARTESIAN_POINT':
                pp=t[1][1]
                coords=[float(a) for a in pp]
                #say(coords)
                pts += [FreeCAD.Vector(*coords)]
                vals["#{}".format(idd)]=FreeCAD.Vector(*coords)

        
        for idd in  self.p21loader._instances_definition:
            t=self.p21loader._instances_definition[idd]
            if t[0]=='B_SPLINE_CURVE_WITH_KNOTS':
                deg=int(t[1][1])
                    
                poles=[vals[pol] for pol in t[1][2]]
                mults=[int(i) for i in t[1][6]]
                knots=[float(i) for i in t[1][7]]
                bc=Part.BSplineCurve()
                bc.buildFromPolesMultsKnots(poles,mults,knots,False,deg)
                col+=[bc.toShape()]
            elif t[0]=='B_SPLINE_SURFACE_WITH_KNOTS':
                udeg=int(t[1][1])
                vdeg=int(t[1][2])
                poles=t[1][3]
                ptsa=[]
                ptsa +=[[vals[pol] for pol in poles[0]]]
                ptsa +=[[vals[pol] for pol in poles[1]]]

                umults=[int(i) for i in poles[7]]
                vmults=[int(i) for i in poles[8]]
                uknots=[float(i) for i in poles[9]]
                vknots=[float(i) for i in poles[10]]
                
                bc=Part.BSplineSurface()                
                bc.buildFromPolesMultsKnots(ptsa,umults,vmults,uknots,vknots,False,False,udeg,vdeg)
                col+=[bc.toShape()]
            
                
            elif t[0]=='SPHERICAL_SURFACE':
                ref=t[1][1]
                radius=float(t[1][2])
                say("shere radius",radius,ref)
                
            #33 ('CONICAL_SURFACE', ["''", '#34', '2.', '0.19739555985'])
            #34 ('AXIS2_PLACEMENT_3D', ["''", '#35', '#36', '#37'])
            #35 ('CARTESIAN_POINT', ["''", ['0.', '0.', '0.'], ''])
            #36 ('DIRECTION', ["''", ['0.', '0.', '1.'], ''])
            #37 ('DIRECTION', ["''", ['1.', '0.', '-0.'], ''])

            
            ''' 
                

        self.setData("Points_out",pts)
        self.setPinObject("Shape_out",Part.Compound(col))


    #---------------------------    
    else:
    
        import time
        import sys
        #fn="/media/thomas/Intenso1/stel-stlfc/product.step"
        fn=self.getData("filename")
        fn="/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/bsplinesurface.step"
        self.p21loader = Part21Parser(fn)
        print("Creating instances")
        # p21population = Part21Population(p21loader)
        
#       for idd in  p21loader._instances_definition:
#           print(p21loader._instances_definition[idd])

        sayl("Abbruch")
        #return

        
        for idd in  self.p21loader._instances_definition:
                print(idd,self.p21loader._instances_definition[idd])
    
    
    
        import step2
        reload(step2)
        sayl("step2 loaded !!")
        import step
        reload(step)

        entities,types = step2.main()
    
    
        driver=step.getDriver()
        with driver.session() as session:
            session.write_transaction(step.clear)

        say("-----------------------------------")

    
    
        def sref(s):
            return "R-->"+s[1:]
        
        
        def makelist(v):
            vs=[]
            for p in v:
                if isinstance(p,list):
                    vs += [makelist(p)]
                elif p.startswith("#"):
                    vs += [ sref(p) ]
                elif p=='':
                    vs += ['']
                else:
                    try:
                        rc=int(p)
                    except:
                        try:
                            rc=float(p)
                        except:
                            rc=p
                    vs += [rc]
            return vs
            
        errors=[]   
        for idd in  self.p21loader._instances_definition:
                dat=self.p21loader._instances_definition[idd]
                enti=dat[0].lower()
                if dat[0]=='':
                    #sayW("ignore")
                    continue

                    
                if not enti.startswith('b_spline'):   

                    continue

                #say("#----------------------------",idd)
                say()
                print(idd,self.p21loader._instances_definition[idd])
                dbparams={
                    'project':'myFilename',
                    'stepid':idd
                }
                


                try:
                    _=entities[enti]
                    
                    #step2.displayEntity(entities, types,name=enti)
                    
                    #say(entities[enti])
                    #say("________________")
                    #say("dart 1",dat[1])
                    #say(len(entities[enti]),len(dat[1]))
                    if len(entities[enti]) < len(dat[1]):
                            #say("ignore first param")
                            params=dat[1][1:]
                    else:
                        params=dat[1]
                    
                    #say("!! params",params)
                    #step2.displayEntity(entities, types,name=enti)
                    for p,v in zip(entities[enti],params):
                        #say("LINE-----------",p,v)
                        if isinstance(v,list):
                            say(p[0],makelist(v))
                            dbparams[p[0]]=makelist(v)
                        elif v.startswith('#'):
                            say(p[0],sref(v))
                            dbparams[p[0]]=sref(v)
                        elif re.match("\[.*\]",v):
                            say(p[0],makelist(v))
                            dbparams[p[0]]=makelist(v)
                        elif p[1]=='REAL':
                            say(p[0],float(v))
                            dbparams[p[0]]=float(v)
                        elif p[1]=='INTEGER':
                            say(p[0],int(v))
                            dbparams[p[0]]=int(v)

                        else:
                            say(p[0],v)
                            dbparams[p[0]]=v
                            
            
                        
                except Exception as ex:
                    sayW(ex)
                    sayW("no entitiy for ",enti)
                    errors +=[enti]
                    if enti=='b_spline_surface_with_knots':
                        return
            
                if enti.startswith('b_spline'):   

                    FreeCAD.dbparams=dbparams                         
                    say(enti)
        
        
        

                    import json

                    params={}
                    for p in FreeCAD.dbparams:
                        if isinstance(FreeCAD.dbparams[p],list):
                            params[p]=json.dumps(FreeCAD.dbparams[p])
                        else:
                            params[p]=FreeCAD.dbparams[p]
                    
                    say(enti,idd,params)
                    typ=enti
                    kid=idd
                    #params={'a':23,'b':56}

                    with driver.session() as session:
                        rc=session.write_transaction(step.createNode2, kid,typ,params)
                        say("RC",rc)
                        for k in rc.keys():
                            print (rc.data())
                        FreeCAD.rc=rc
        
        
        
        say('errors...')
        for e in errors:
            say(e)
          
        FreeCAD.ents=entities


