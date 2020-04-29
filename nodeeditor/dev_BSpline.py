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
    
def patchgrid(self):

    shape=self.getPinObject("Face_in")
    es=shape.Edges
    sf=shape.Surface
    e=es[0]

    pts=e.discretize(200)

    pams=np.array([sf.parameter(p) for p in pts])
    pamsA=np.array([(u,v) for (v,u) in pams])

    pamms= pams[pams[:,0].argsort()]
    pammsA= pamsA[pamsA[:,0].argsort()]

    segs={}
    pamss2=[(round(k[0],1),k[1]) for k in pams]
    for p in pamss2:
        try:
            segs[p[0]]+=[p[1]]
        except:
            segs[p[0]]=[p[1]]

    col=[]
    for s in segs:
        mi=min(segs[s])
        ma=max(segs[s])
        if mi != ma:
            ss=sf.uIso(s)
            ss.segment(mi,ma)
            col += [ss.toShape()]

    us=col
    col=[]
    
        

    segsA={}
    pamss2A=[(round(k[0],1),k[1]) for k in pamsA]

    for p in pamss2A:
        try:
            segsA[p[0]]+=[p[1]]
        except:
            segsA[p[0]]=[p[1]]



    col=[]
    for s in segsA:
        mi=min(segsA[s])
        ma=max(segsA[s])
        if mi != ma:
            ss=sf.vIso(s)
            ss.segment(mi,ma)
            
            
            col += [ss.toShape()]


    vs=col
    return (us,vs)



def run_FreeCAD_BSplineSegment(self):
    
    sh=self.getPinObject("Shape")
    if sh is None:
        sayErr("no Shape -- abort ")
        return

    try:
        bs=sh.Surface.copy()
    except:
        bc=sh.Curve.copy()
        bs= None

    if bs is None:
        ustart=self.getData('uStart')*0.01
        uend=self.getData('uEnd')*0.01
        [ua,ue]=sh.ParameterRange
        bc.segment(ua+(ue-ua)*ustart,ua+(ue-ua)*uend)
        self.setPinObject('Shape_out',bc.toShape())
    else:
        ustart=self.getData('uStart')*0.01
        vstart=self.getData('vStart')*0.01
        uend=self.getData('uEnd')*0.01
        vend=self.getData('vEnd')*0.01
        [ua,ue,va,ve]=sh.ParameterRange
        bs.segment(ua+(ue-ua)*ustart,ua+(ue-ua)*uend,va+(ve-va)*vstart,va+(ve-va)*vend)
        self.setPinObject('Shape_out',bs.toShape())
     
    
    
     

#+# todo cleanup code reduceCurve 31.01.2020
def run_FreeCAD_ReduceCurve(self):
    

    try:
        if self.shape is None:
            1/0
        say(self.shape)
        sh=self.shape
    except:
        sh=self.getPinObject("Shape")
        if sh is None:
            sayErOb(self,"no Shape")    
            return

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



'''
    Replaces this B-Spline curve by approximating a set of points.
    The function accepts keywords as arguments.

    approximate2(Points = list_of_points)

    Optional arguments :

    DegMin = integer (3) : Minimum degree of the curve.
    DegMax = integer (8) : Maximum degree of the curve.
    Tolerance = float (1e-3) : approximating tolerance.
    Continuity = string ('C2') : Desired continuity of the curve.
    Possible values : 'C0','G1','C1','G2','C2','C3','CN'

    LengthWeight = float, CurvatureWeight = float, TorsionWeight = float
    If one of these arguments is not null, the functions approximates the
    points using variational smoothing algorithm, which tries to minimize
    additional criterium:
    LengthWeight*CurveLength + CurvatureWeight*Curvature + TorsionWeight*Torsion
    Continuity must be C0, C1 or C2, else defaults to C2.

    Parameters = list of floats : knot sequence of the approximated points.
    This argument is only used if the weights above are all null.

    ParamType = string ('Uniform','Centripetal' or 'ChordLength')
    Parameterization type. Only used if weights and Parameters above aren't specified.

    Note : Continuity of the spline defaults to C2. However, it may not be applied if
    it conflicts with other parameters ( especially DegMax ).
'''

def run_FreeCAD_ApproximateBSpline(self):
    shin=self.getPinObject("Shape_in")
    if shin is None:
        sayErOb(self,"no Shape_in")    
        return

    say(shin)
    points=self.getData("points")

    if shin is None: 
        sf=None
    
        pp=[points[0]]
        for i in range(1,len(points)):
            if ((points[i]-points[i-1]).Length)>0.01:
                pp += [points[i]]
    
        bs = Part.BSplineCurve()
        tol=max(self.getData("tolerance"),1.)
        bs.approximate(pp,Tolerance=tol*0.001)
        self.setPinObject("Shape_out",bs.toShape())
    else:
        shin=shin.toNurbs().Face1
        sf=shin.Surface

        uvs=[]
        pts2da=[sf.parameter(p) for p in points]
    
        pts2d=[]
        for i,p in enumerate(pts2da):
            pts2d += [FreeCAD.Base.Vector2d(p[0],p[1])]

        bs2d = Part.Geom2d.BSplineCurve2d()
        tol=max(self.getData("tolerance"),1.)
        bs2d.approximate(pts2d,Tolerance=tol*0.001)

        self.setPinObject("Shape_out",bs2d.toShape(sf))


'''
>>> print(bs2d.interpolate.__doc__)

    Replaces this B-Spline curve by interpolating a set of points.
    The function accepts keywords as arguments.

    interpolate(Points = list_of_points)

    Optional arguments :

    PeriodicFlag = bool (False) : Sets the curve closed or opened.
    Tolerance = float (1e-6) : interpolating tolerance

    Parameters : knot sequence of the interpolated points.
    If not supplied, the function defaults to chord-length parameterization.
    If PeriodicFlag == True, one extra parameter must be appended.

    EndPoint Tangent constraints :

    InitialTangent = vector, FinalTangent = vector
    specify tangent vectors for starting and ending points
    of the BSpline. Either none, or both must be specified.

    Full Tangent constraints :

    Tangents = list_of_vectors, TangentFlags = list_of_bools
    Both lists must have the same length as Points list.
    Tangents specifies the tangent vector of each point in Points list.
    TangentFlags (bool) activates or deactivates the corresponding tangent.
    These arguments will be ignored if EndPoint Tangents (above) are also defined.

    Note : Continuity of the spline defaults to C2. However, if periodic, or tangents
    are supplied, the continuity will drop to C1.

>>> 
'''
def run_FreeCAD_InterpolateBSpline(self):
    points=self.getData("points")
    say("interpolate for {} points".format(len(points)))
    if len(points)<2:return

    shin=self.getPinObject("Shape_in")
    if shin is None:
        bs2d = Part.BSplineCurve()
        tol=max(self.getData("tolerance"),1.)
        #+# todo: problem with tolerance parameter - how to use it ?

        bs2d.interpolate(points,PeriodicFlag=False)
        self.setPinObject("Shape_out",bs2d.toShape())
    
        return

    
    
    
    shin=shin.toNurbs().Face1
    sf=shin.Surface
    
    uvs=[]
    pts2da=[sf.parameter(p) for p in points]
    pts2d=[]
    for i,p in enumerate(pts2da):
        pts2d += [FreeCAD.Base.Vector2d(p[0],p[1])]

    bs2d = Part.Geom2d.BSplineCurve2d()

    tol=max(self.getData("tolerance"),1.)
    #+# todo: problem with tolerance parameter - how to use it ?

    bs2d.interpolate(pts2d,PeriodicFlag=False)
    self.setPinObject("Shape_out",bs2d.toShape(sf))





def run_FreeCAD_Destruct_BSpline(self,bake=False, **kwargs):
    shape=self.getPinObject("Shape_in")
    if shape is None: return
    c=shape.Curve
    say(c)
    self.setData("knots",c.getKnots())
    self.setData("mults",c.getMultiplicities())
    self.setData("degree",c.Degree)
    self.setData("poles",c.getPoles())
    #self.setData("periodic",False)
    say("done")



def run_FreeCAD_Destruct_BSplineSurface(self,bake=False, **kwargs):
    shape=self.getPinObject("Shape_in")
    if shape is None: return
    c=shape.Surface
    say(c)
    FreeCAD.c=c
    self.setData("uknots",c.getUKnots())
    self.setData("umults",c.getUMultiplicities())
    self.setData("udegree",c.UDegree)
    self.setData("uperiodic",c.isUPeriodic)
    self.setData("vknots",c.getVKnots())
    self.setData("vmults",c.getVMultiplicities())
    self.setData("vdegree",c.VDegree)
    self.setData("vperiodic",c.isVPeriodic)
    poles=c.getPoles()

    self.setData('poles',poles)

    say("done")



#-----------------------------
#    umrechnungsmethode

 
def maskit(poles,vv,t,ui,vi,ut=0.2,vt=0.3, ruA=0,rvA=0, ruB=0,rvB=0,sA=1,sB=1):

    uc,vc,_=poles.shape
    mask=np.array([vv.x,vv.y,vv.z]*(2+ruA+ruB)*(2+rvA+rvB)).reshape(2+ruA+ruB,2+rvA+rvB,3)

    mask[0] *= ut
    mask[-1] *= 1-ut

    mask[:,0] *= vt
    mask[:,-1] *= 1 - vt

    # begrenzungen
    su=max(0,ui-ruA)
    sv=max(0,vi-rvA)
    eu=min(uc,ui+ruB+2)
    ev=min(vc,vi+rvB+2)

    msu=max(0,-ui+ruA)
    msv=max(0,-vi+rvA)
    meu=min(2+ruA+ruB,uc-ui+1)
    mev=min(2+rvA+rvB,vc-vi+1)
    
    mm=mask[msu:meu,msv:mev]
    mm[1:-1]*= sA
    mm[:,1:-1]*= sB

    poles[su:eu,sv:ev] += mm*t
    return poles
    


def run_FreeCAD_Editor(self):
    try:
        say(self.shape)
        sh=self.shape
    except:
        sh=self.getPinObject("Shape")
    
    if sh is None:
        sayErOb(self,"no Shape")    
        return

    sf=sh.Surface

    # daten holen und neu aufbauen
    ud=sf.UDegree
    vd=sf.VDegree
    ap=np.array(sf.getPoles())
    uk=np.array(sf.getUKnots())
    vk=np.array(sf.getVKnots())
    mu=np.array(sf.getUMultiplicities())
    mv=np.array(sf.getVMultiplicities())
    
    def pamo(v):
        if v== -100:
            return 0
        else:
            return 10**(v/100-1)
    
    ut=pamo(self.getData("u"))
    vt=pamo(self.getData("v"))
    
    startu=self.getData("startU")*0.01
    startv=self.getData("startV")*0.01
    [umin,umax,vmin,vmax]=sf.toShape().ParameterRange
    startu=umin+(umax-umin)*(self.getData("startU")+100)/200
    startv=vmin+(vmax-vmin)*(self.getData("startV")+100)/200
    
    if self.getData('useStartPosition'):
        vv=self.getData('startPosition')
        startu,startv=sf.parameter(vv)
    else:
        vv=sf.value(startu,startv)
    
    say("startuv",startu,startv)
    say("----------------vv von position",vv)
    
    try:
        FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.start)
    except:
        pass
    
    
    if self.getData('displayStart'):
        say("display Start .............")
        
        trans = coin.SoTranslation()
        trans.translation.setValue(vv.x,vv.y,vv.z)
        cub = coin.SoSphere()
        cub.radius.setValue(3)

        col = coin.SoBaseColor()
        col.rgb=(1,0,0)
        
        myCustomNode = coin.SoSeparator()
        myCustomNode.addChild(col)
        myCustomNode.addChild(trans)
        myCustomNode.addChild(cub)
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        sg.addChild(myCustomNode)
        self.start=myCustomNode
    
    
    vvtt=self.getData('targetPosition')
    if self.getData('useStart'):
        ui,vi=startu,startv
    else:
        ui,vi=sf.parameter(vvtt) 
    say("reale ziel position ui,vi",ui,vi)
   
    
    try:
        FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.target)
    except:
        pass
    
    if self.getData('displayTarget'):
        
        trans = coin.SoTranslation()
        trans.translation.setValue(vvtt.x,vvtt.y,vvtt.z)
        cub = coin.SoSphere()
        cub.radius.setValue(3)

        col = coin.SoBaseColor()
        col.rgb=(0,1,0)
        
        myCustomNode = coin.SoSeparator()
        myCustomNode.addChild(col)
        myCustomNode.addChild(trans)
        myCustomNode.addChild(cub)
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        sg.addChild(myCustomNode)
        self.target=myCustomNode
    
    
    
    
    
    vv=vvtt
    
    vv0=vvtt-sf.value(ui,vi)
    # fur deg 1
    #uix=int(round(ui+0.5))-1
    #vix=int(round(vi+0.5))-1

    # deg 2
    uix=int(round(ui+0.5))
    vix=int(round(vi+0.5))

    [umin,umax,vmin,vmax]=sf.toShape().ParameterRange
    #say("borders",[umin,umax,vmin,vmax])
    #say("uix,vix",uix,vix)
    
    if self.getData('bordersFrozen'):
        if uix<1:
            uix=1
        if vix<1:
            vix=1
        if uix>umax-1:
            uix=int(umax)-1
        if vix>vmax-1:
            vix=int(vmax)-1

    if self.getData('tangentsFrozen'):
        if uix<2:
            uix=2
        if vix<2:
            vix=2
        if uix>umax-2:
            uix=int(umax)-2
        if vix>vmax-2:
            vix=int(vmax)-2
    
    st=self.getData('t')+101
    ut*= st
    vt*= st
    
    ruA=self.getData('offsetUA')
    ruB=self.getData('offsetUB')
    rvA=self.getData('offsetVA')
    rvB=self.getData('offsetVB')
    sA=(self.getData('scaleU')+150)/50
    sB=(self.getData('scaleV')+150)/50
    
    
    

    def dist(param):

        t=param[0]
        ap=maskit(np.array(sf.getPoles()),vv0,t,uix,vix,ut=ut,vt=vt, ruA=ruA,rvA=rvA,ruB=ruB,rvB=rvB,sA=sA,sB=sB)
        fa=Part.BSplineSurface()
        fa.buildFromPolesMultsKnots(ap,mu,mv,uk,vk,False,False,ud,vd)
        return fa.toShape().distToShape(Part.Vertex(vv))[0]
    
    from scipy import optimize
    
    allmethods=[ 
            'Nelder-Mead' ,
            'Powell' ,
            'CG' ,
            'BFGS' ,
            'L-BFGS-B', 
            'TNC',
            'COBYLA',
            'SLSQP',
        ]

    methods=[ 'Nelder-Mead' ]
    
    for method in methods:
        
        a=time.time()
        result = optimize.minimize(dist, x0=[0,],  method=method)
        r=result.x[0]

        say("quality",np.round(result.fun,5),np.round(result.x,2),result.message,method)
        say("run time for scipy.optimize.minimum",method,round(time.time()-a,3))

    fa=Part.BSplineSurface()
    ap=maskit(np.array(sf.getPoles()),vv0,r,uix,vix,ut=ut,vt=vt, ruA=ruA,rvA=rvA,ruB=ruB,rvB=rvB,sA=sA,sB=sB)
    fa.buildFromPolesMultsKnots(ap,mu,mv,uk,vk,False,False,ud,vd)
    
    #zeige nur aenderungen
    fb=fa.copy()
    fb.segment(max(uix-ruA-2,uk[0]),min(uix+2+ruB,uk[-1]),max(vix-rvA-2,vk[0]),min(vix+2+rvB,vk[-1]))
    col=[fb.uIso(k).toShape() for k in fb.getUKnots()]
    col += [fb.vIso(k).toShape() for k in fb.getVKnots()]
    
    shape=fa.toShape()
    
    self.setPinObject('Shape_out',shape)
    
    ui2,vi2=fa.parameter(vv)   
    #say("neue pos", ui2,vi2)12
    say("curvature",fa.curvature(ui2,vi2,'Max'))
      
    
    [umin,umax,vmin,vmax]=fa.toShape().ParameterRange
    aa=fa.uIso(ui2).toShape()
    bb=fa.vIso(vi2).toShape()
    
    if self.getData('displayIso'):
        #self.setPinObject('Shape_out',Part.Compound([shape,aa,bb]))
        self.setPinObject('Shape_out',Part.Compound(col+ [aa,bb]))
        
    self.setData('position_out',[vv,vv])

    say("Abstand", round(fa.toShape().distToShape(Part.Vertex(vv))[0],5))

    self.setData('u_out',(ui2-umin)/(umax-umin)*10)
    self.setData('v_out',(vi2-vmin)/(vmax-vmin)*10)



def run_FreeCAD_IronCurve(self):

    sh=self.getPinObject('Shape')
    
    if sh is None:
        sayErOb(self,"no Shape")    
        return

    pts=sh.Curve.getPoles()
    
    col=[]
    w=self.getData("weight")

    mode=self.getData("mode")
    def run(pts,k=1):

        l=len(pts)

        if mode == 'constant':
            pts2= [pts[0]] + [ (pts[i-1]+2*pts[i]+pts[i+1])/4 for i in range(1,l-1)] +[pts[-1]]
            pts2= [pts[0]] + [ (pts[i-1]+w*pts[i]+pts[i+1])/(2+w) for i in range(1,l-1)] +[pts[-1]]
        else:
            pts2=[pts[0]]
            for i in range(1,l-1):
                al=(pts[i-1]-pts[i]).Length
                el=(pts[i+1]-pts[i]).Length
                say(i,al,el)
                f=10.
                if al!=0:
                    al=min(1,1/al*(w+1))
                else:
                    al=1
                if el !=0:
                    el=min(1,1/el*(w+1))
                else:
                    el=1
                
                say(i,al,el)                
                
                pts2 += [(al*pts[i-1]+pts[i]+el*pts[i+1])/(1+al+el)]
                

            pts2 +=[pts[-1]]

        dd=[FreeCAD.Vector()]+[(pts[i]-pts2[i]).normalize()*k for i in range(1,l-1)]+[FreeCAD.Vector()]
        pts3=[p+q for p,q in zip(pts2,dd)]
        
        if 0:
            for i in range(1,l-3):
                
                if (pts3[i]-pts3[i+1]).Length>(pts3[i]-pts3[i+3]).Length:
                    pts3=pts3[:i+1] +[pts3[i+3],pts3[i+2],pts3[i+1]] + pts3[i+4:]

            for i in range(1,l-2):           
                if (pts3[i]-pts3[i+1]).Length>(pts3[i]-pts3[i+2]).Length:
                   pts3=pts3[:i+1] +[pts3[i+2],pts3[i+1]] + pts3[i+3:]
        
        c=Part.BSplineCurve(pts3)
        return pts3,c.toShape()

    loopsa=self.getData('loopsA')
    loopsb=self.getData('loopsB')

    k=self.getData('k')

    say(loopsa,loopsb)
    for i in range(loopsa):
        pts,c=run(pts)
        #pts,c=run(pts,k)
        col.append(c)

    for i in range(loopsb):
        pts,c=run(pts,k)
        col.append(c)


    '''
        Discretizes the curve and returns a list of points.
        The function accepts keywords as argument:
        discretize(Number=n) => gives a list of 'n' equidistant points
        discretize(QuasiNumber=n) => gives a list of 'n' quasi equidistant points (is faster than the method above)
        discretize(Distance=d) => gives a list of equidistant points with distance 'd'
        discretize(Deflection=d) => gives a list of points with a maximum deflection 'd' to the curve
        discretize(QuasiDeflection=d) => gives a list of points with a maximum deflection 'd' to the curve (faster)
        discretize(Angular=a,Curvature=c,[Minimum=m]) => gives a list of points with an angular deflection of 'a'
                                            and a curvature deflection of 'c'. Optionally a minimum number of points
                                            can be set which by default is set to 2.        
    '''

    k=self.getData('deflection')
    if k>0:
        ptsdd=c.discretize(QuasiDeflection=k*0.1)
        #ptsdd=c.discretize(Deflection=k*0.1)
        self.setPinObject('Shape_out',Part.makePolygon(ptsdd))    

        deflp=Part.makePolygon(ptsdd)
        defl=Part.BSplineCurve(ptsdd).toShape()
        say("deflection",len(ptsdd))
        self.setPinObject('Shape_out',defl)
        #self.setPinObject('Shape_out',Part.Compound([deflp,defl]))
        self.setData('points',ptsdd)
    else:
        #self.setPinObject('Shape_out',Part.Compound(col))
        self.setPinObject('Shape_out',col[-1])
        self.setData('points',pts)
    
    FreeCAD.ActiveDocument.recompute()



def run_FreeCAD_IronSurface(self):
    sh=self.getPinObject('Shape')
    if sh is None:
        sayErOb(self,"no Shape")    
        return

    ptsarr=sh.Surface.getPoles()
    
    col=[]
    w=self.getData("weight")

    def run(pts,k=1):

        l=len(pts)

        pts2= [pts[0]] + [ (pts[i-1]+2*pts[i]+pts[i+1])/4 for i in range(1,l-1)] +[pts[-1]]
        pts2= [pts[0]] + [ (pts[i-1]+w*pts[i]+pts[i+1])/(2+w) for i in range(1,l-1)] +[pts[-1]]

        dd=[FreeCAD.Vector()]+[FreeCAD.Vector((pts[i]-pts2[i])).normalize()*k for i in range(1,l-1)]+[FreeCAD.Vector()]
        pts3=[FreeCAD.Vector(p+q) for p,q in zip(pts2,dd)]
        
        
        #
        for i in range(1,l-3):
            
            if (pts3[i]-pts3[i+1]).Length>(pts3[i]-pts3[i+3]).Length:
                pts3=pts3[:i+1] +[pts3[i+3],pts3[i+2],pts3[i+1]] + pts3[i+4:]

        for i in range(1,l-2):           
            if (pts3[i]-pts3[i+1]).Length>(pts3[i]-pts3[i+2]).Length:
               pts3=pts3[:i+1] +[pts3[i+2],pts3[i+1]] + pts3[i+3:]
        
        c=Part.BSplineCurve(pts3)
        return pts3,c.toShape()

    loopsa=self.getData('loopsA')
    loopsb=self.getData('loopsB')
    k=self.getData('k')

    ptsarr2=[]
    for pts in ptsarr:

        for i in range(loopsa+1):
            pts,c=run(pts)
        for i in range(loopsb+1):
            pts,c=run(pts,k)
            
        ptsarr2 += [pts]
    
    ptsarr=np.array(ptsarr2).swapaxes(0,1)
    ptsarr2=[]

    for pts in ptsarr:

        for i in range(loopsa+1):
            pts,c=run(pts)
        for i in range(loopsb+1):
            pts,c=run(pts,k)
            
        ptsarr2 += [pts]
        col.append(c)
    
    ptsarr=np.array(ptsarr2).swapaxes(0,1)
    self.setPinObject('Shape_out',Part.Compound(col))
    self.setData('points',ptsarr.tolist())
    FreeCAD.ActiveDocument.recompute()




        




def run_FreeCAD_UIso(self,*args, **kwargs):

    f=self.getPinObject('Face_in')
    if f is None: return
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    u=self.getData("u")

    uu=umin+(umax-umin)*0.1*u
    c=sf.uIso(uu)
    self.setPinObject('Shape_out',c.toShape())

    #if self.getData('display'):
    #    obj=self.getObject()
    #    obj.Shape=c.toShape()




def run_FreeCAD_VIso(self,*args, **kwargs):

    f=self.getPinObject('Face_in')
    if f is None: return
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    v=self.getData("v")

    vv=vmin+(vmax-vmin)*0.1*v
    c=sf.vIso(vv)
    self.setPinObject('Shape_out',c.toShape())

    #if self.getData('display'):
    #    obj=self.getObject()
    #    obj.Shape=c.toShape()


def run_FreeCAD_UVGrid(self,*args, **kwargs):

    sayl()
    f=self.getPinObject('Face_in')
    if f is None: return
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    uc=self.getData("uCount")
    vc=self.getData("vCount")
    
    us=[]
    for u in range(uc+1):
        uu=umin+(umax-umin)*u/uc
        c=sf.uIso(uu).toShape()
        us += [c]

    vs=[]
    for v in range(vc+1):
        vv=vmin+(vmax-vmin)*v/vc
        c=sf.vIso(vv).toShape()
        vs += [c]

#

    #verfeinerung path
    sayl()
    if  f.Area != sf.toShape().Area:
        
        us,vs=patchgrid(self)
        
        '''
        # EXAKTE VERSION - ZU LANGSAM
        # patch
        anz=20
        us=[]
        for u in range(uc+1):
            uu=umin+(umax-umin)*u/uc
            c=sf.uIso(uu).toShape()
            cc=sf.uIso(uu)
            pts=c.discretize(anz)
            off=True
            suba=umin
            subb=umin
            for p in pts:
                if f.distToShape(Part.Vertex(p))[0]<1:
                    if off:
                        off=False
                        suba=cc.parameter(p)
                    else:
                        subb=cc.parameter(p)
            try:
                #say(suba,subb)
                cc.segment(suba,subb)
                c=cc.toShape()
                us += [c]
            except:
                pass

        vs=[]
        for v in range(vc+1):
            vv=vmin+(vmax-vmin)*v/vc
            cc=sf.vIso(vv)
            c=cc.toShape()
            pts=cc.toShape().discretize(anz)
            off=True
            suba=vmin
            subb=vmin
            for p in pts:
                if f.distToShape(Part.Vertex(p))[0]<1:
                    if off:
                        off=False
                        suba=cc.parameter(p)
                    else:
                        subb=cc.parameter(p)
            try:
                cc.segment(suba,subb)
                c=cc.toShape()
                vs += [c]
            except:
                pass
        '''
        
    

    self.setPinObjects('uEdges',us)
    self.setPinObjects('vEdges',vs)
    self.setPinObject('Shape_out',Part.Compound(us+vs+f.Edges))





def run_FreeCAD_FillEdge(self):
    sayW("Fill Edge not yet implemented")




def run_FreeCAD_CurveOffset(self):
    import Part
   

    edge=self.getPinObject("Shape_in")
    
    if edge is None:
        sayW("no shape edge")
        return

    Z=FreeCAD.Vector(0,0,1)
    col=[]

    lastdd=100

    edstart=edge
    ed=edstart

    loops=self.getData("loops")
    for i in range(loops):

        cs=ed.Curve

        size=300

        norms=[]
        
        if  i > 1:
            #step=self.getData("step")/10
            #size=int(round(edstart.Length/step))
            #tas=[]
            say("get distant points size ",size)
            points=cs.discretize(size+1)
        
        else:
            deflection=self.getData("deflection")
            points=cs.discretize(QuasiDeflection=deflection*0.001)
        
        for p in points:
            v=cs.parameter(p)
            t =cs.tangent(v)[0]
            norms += [t.cross(Z)]
        
        dd=self.getData("mindd")/100
        
        if self.getData('flip'):
            dd = -dd

        distA=self.getData("distA")

        pts=[]
        ptserr=[]

        if 1:
            for n,p in zip(norms,points):
                neup=p+n*dd
                zp=edstart.distToShape(Part.Vertex(*neup))[1][0][0]

                if (p-zp).Length >distA*0.01:
                    #say("ABweichung",(p-zp).Length)
                    #say("p",p)
                    #say("neup",neup)
                    #say("zp",zp)
                    #say(edstart.distToShape(Part.Vertex(*neup)))
                    if i == 0:
                        ptserr += [neup]
                    else:
                        pts +=[neup]
                else:
                    pts +=[neup]



        lp=len(pts)

        def checkcross(A,B,C,D):
            ''' schneiden sich die strecken AC und BD innen?'''

            a=C-A
            b=B-D
            c=B-A

            aa=np.array([[a.x,a.y],[b.x,b.y]])
            aa=np.array([[a.x,b.x],[a.y,b.y]])
            bb=np.array([c.x,c.y])
            x=np.linalg.solve(aa,bb)

            fa= 0<x[0] and x[0]<1
            fb= 0<x[1] and x[1]<1
            
            return fa and fb

        def cut(i,j):

                A=pts[i]
                B=pts[i+1]
                C=pts[j]
                D=pts[j+1]
                
                return checkcross(A,C,B,D)

        fehler=[0]
        for i in range(lp-2):
            for j in range(lp-2):
                if i >= j:
                    continue
                if cut(i,j):
                    fehler += [i,j]

        fehler += [-1]

        neupol=[]

        for l in range(int(len(fehler)/2)):
            neupol += pts[fehler[2*l]:fehler[2*l+1]]

        neupol += pts[fehler[-1]:]
        pts=neupol

        col= [Part.makePolygon(pts)]
        FreeCADGui.updateGui()

        bc=Part.BSplineCurve()
        
        bc.buildFromPoles(pts)
        ed=bc.toShape()

        if not self.getData('asPolygon'):
            col = [ed]

        self.setPinObject("Shape_out",Part.Compound(col))
        self.outExec.call()
  
    
    ptsn=bc.discretize(size+1)

    dists=[edstart.distToShape(Part.Vertex(*p))[0] for p in ptsn]
    say("distance expected min max",abs(dd),round(min(dists),2),round(max(dists),2))
    


def run_FreeCAD_BSplineOffset(self):
    sayl()

    sh=self.getPinObject("Shape") 
    if sh is None:
        sayErOb(self,"no Shape")    
        return
    
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
        #nus=FreeCAD.Vector(0,0,10)
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
    if 1:
        rs=[]
        for u in range(1,size):
            for v in range(1,size):                
                n=FreeCAD.Vector(norms[u,v])
                a=FreeCAD.Vector(*(points[u+1,v]-points[u,v]))
                aa=a.normalize()
                rs +=[0.5*a.Length/abs(aa.dot(n))]
                
        say("Q offset works for maximum height with out collisions", min(rs))


    newpts=points+ norms*h

    self.setData('Points_out',newpts.tolist())   

    ud=2
    vd=2
    bsa=noto.createBSplineSurface(newpts,udegree=ud,vdegree=vd)
    self.setPinObject('Shape_out',bsa.toShape())

    # test quality
    testpts=np.array([[bsa.value(ua+(ue-ua)*u/size,va+(ve-va)*v/size) for v in range(size+1)]  for u in range(size+1)])
    ptsn=testpts.reshape((size+1)**2,3)
    
    dists=[sh.distToShape(Part.Vertex(*p))[0] for p in ptsn]
    say("distance expected min max",round(abs(h),2),round(min(dists),2),round(max(dists),2))

    



from nodeeditor.tools import *

def run_FreeCAD_CloseFace(self):

    fac=self.getPinObject('Shape_in')
    if fac is None:
        sayW("no Shape_in")
        return
    swap=self.getData('swap')
    force=self.getData("tangentForce")*0.01

    sf=fac.Face1.Surface
    
    poles=sf.getPoles()
    ud=sf.UDegree   
    vd=sf.VDegree

    umults=sf.getUMultiplicities()
    vmults=sf.getVMultiplicities()

    if swap:
        ud,vd=vd,ud  
        umults,vmults=vmults,umults     
        poles=np.array(poles).swapaxes(0,1)

    a=[FreeCAD.Vector(p) for p in poles[0]]
    b=[FreeCAD.Vector(p) for p in poles[1]]
    d=[FreeCAD.Vector(p) for p in poles[-2]]
    c=[FreeCAD.Vector(p) for p in poles[-1]]
   


    ptsk=[]
    for ap,bp,cp,dp in zip(a,b,c,d):
        dist=(cp-ap).Length*force
        na=(ap-bp).normalize()
        nc=(cp-dp).normalize()
        #ptsk += [[ap,ap+na*dist,cp+nc*dist,cp]]
        ptsk += [[ap,ap+na*dist,(ap+na*dist+cp+nc*dist)*0.5,cp+nc*dist,cp]]

    bs=createBSplineSurface(ptsk,
                udegree=3,vdegree=3,
                uperiodic=False,vperiodic=False,
                uclosed=False,vclosed=False,weights=None)

    if swap:
        bs.increaseDegree(vd,ud)
    else:
        bs.increaseDegree(ud,vd)
    
        
    if swap:
        poles1=np.array(sf.getPoles()).swapaxes(0,1)[::-1]
        poles2=np.array(bs.getPoles()).swapaxes(0,1)
    else:
        poles1=np.array(sf.getPoles())[::-1]
        poles2=np.array(bs.getPoles()).swapaxes(0,1)#[::-1]
    
    pall=np.concatenate([poles1,poles2[1:-1]])
    pall2=np.concatenate([pall[-ud:],pall[:-ud]])

    kk=ud
    pall2=np.concatenate([pall[-kk:],pall[:-kk]])
    
    dd=pall2.shape[0]
    say("dd",dd)
    say(umults[1:-1],sum(umults[1:-1]))
    if sum(umults[1:-1])<=(dd-2*ud-1):
        say("FUEGE reste eine")
        umults2=[1,ud] +umults[1:-1]+[ud,1]
        kdd=dd-sum(umults2)
        say(kdd)
        umults2 +=[1]*(kdd+1)
        say(sum(umults2))
    else:
        umults2=[1,ud] +[1]*(dd-2*ud-1)+[ud,1]
    
    
    say("pall2 shape",pall2.shape)
    say("!u2!",umults2,ud,len(umults2),sum(umults2))
    say("!v!",vmults,vd,len(vmults),sum(vmults))
    
    bs2=Part.BSplineSurface()
    bs2.buildFromPolesMultsKnots(pall2,umults2,vmults,range(len(umults2)),range(len(vmults)),
            True,False,ud,vd)        

    self.setPinObject("Shape_out",bs2.toShape())




def run_FreeCAD_replacePoles(self):

    sh=self.getPinObject("Shape")
    if sh is None:
        sayErr("no Shape - abort")
        return
    
    sf=sh.Surface
    poles=np.array(sf.getPoles())
    points=np.array(self.getData('poles'))
    [uix,vix]=self.getData('polesIndex')
    #say(poles.shape)
    #say(points.shape)
    #say([uix,vix])
 
     # daten holen und neu aufbauen
    ud=sf.UDegree
    vd=sf.VDegree


    ap=np.array(sf.getPoles())

    uk=np.array(sf.getUKnots())
    vk=np.array(sf.getVKnots())
   
    
    mu=np.array(sf.getUMultiplicities())
    mv=np.array(sf.getVMultiplicities())
    start=ap[uix,vix]
    
    #ap[uix-1:uix+2,vix-1:vix+2] += (points-start)*0.8
    #ap[uix:uix+1,vix:vix+1] += (points-start)*0.2
    #ap[uix-1:uix+2,vix-1:vix+2] += (points)*0.8
    ap[uix:uix+1,vix:vix+1] += (points)*1

    fa=Part.BSplineSurface()
    fa.buildFromPolesMultsKnots(ap,mu,mv,uk,vk,False,False,ud,vd)
    self.setPinObject('Shape_out',fa.toShape())
    


def run_FreeCAD_Helmet3(self):


    dome=self.getData('dome')
    say(np.array(dome).shape)
    border=self.getData('border')
    say(np.array(border).shape)
    hh=self.getData("heightBorder")

    ptsa=np.array(border)
    assert dome.shape == (3,3,3)
    assert ptsa.shape= (16,3)

    poles=np.zeros((5,5,3))
    poles[0,0:-1]=ptsa[12:17][::-1]
    poles[4]=ptsa[4:9]
    poles=poles.swapaxes(0,1)
    poles[0]=ptsa[0:5]
    poles[4]=ptsa[8:13][::-1]

    poles[1,1:4]=dome[0]
    poles[2,1:4]=dome[1]
    poles[3,1:4]=dome[2]

    polesb=np.zeros((7,7,3))
    polesb[1:-1,1:-1]=poles
    polesb[0]=polesb[1]
    polesb[-1]=polesb[-2]
    polesb=polesb.swapaxes(0,1)
    polesb[0]=polesb[1]
    polesb[-1]=polesb[-2]
    polesb=polesb.swapaxes(0,1)

    polesb[1,1:-1,2] += hh
    polesb[-2,1:-1,2] += hh
    polesb[2:-2,1,2] += hh
    polesb[2:-2,-2,2] += hh

    polesb[0,0]=polesb[0,1]
    polesb[-1,-1]=polesb[-1,-2]
    polesb[0,-1]=polesb[0,-2]
    polesb[-1,0]=polesb[-1,1]

    ud=3
    vd=3
    mu=[4,1,1,1,4]
    mv=[4,1,1,1,4]

    uk=range(len(mu))
    vk=range(len(mv))

    sf=Part.BSplineSurface()
    sf.buildFromPolesMultsKnots(polesb,mu,mv,uk,vk,False,False,ud,vd)
    
    self.setPinObject("Shape_out",sf.toShape())
    









