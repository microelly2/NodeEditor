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



def run_FreeCAD_Compound(self, *args, **kwargs):

        #+# todo ShapesList implementieren
#        try:
#            subshapes=self.getPinObjects("Shapes")
#        except:
#            subshapes=[]
#        try:
#            subshapes += self.getPinObjects("ShapeList")
#        except:
#            pass

        # get list of nodes
        outArray = []
        ySortedPins = sorted(self.shapes.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            outArray.append(i.owningNode().getPinObject(i.name))
        

#-----------------


        say("Compound Shapes:",outArray)
        shape=Part.Compound(outArray)

        self.setPinObject("Shape_out",shape)
    

    
    
def run_FreeCAD_RepeatPattern(self):

    b=self.getData("pattern")
    apts=self.getData("vectors")

    a=np.array(apts)

    # make the vectors array flat
    if len(np.array(a).shape)>1:
        ll=np.array(a).shape
        a=np.array(a).reshape(np.prod(ll[:-1]),3)

    a=[FreeCAD.Vector(v.tolist()) for v in a]
    c=[[av+bv for bv in b] for av in a]

    col=[]
    for pts in c:
        col +=[Part.makePolygon(pts)]

    cc=Part.Compound(col)

    self.setData("pattern_out",c)
    self.setPinObject("Shape_out",cc)
    self.setColor(a=0.7)
    


def run_FreeCAD_Reduce(self):

    flags=self.getData("selection")
    eids=self.getData("shapes")
    say(self.name)
    if eids is None:
        return
    shapes=[store.store().get(eid)  for eid in eids]
    reduced=[]
    for f,s in zip(shapes,flags):
        if s:
             reduced += [f]
    try:
        rc=Part.Compound(reduced)
    except:
       rc=Part.Shape()
    say("!!rc=",rc)
    self.setPinObject("Shape_out",rc)
    self.setColor(b=0,a=0.4)

def run_FreeCAD_Slice(self):
    sayW("not implemeted")
    sayl()
    

    

def run_FreeCAD_Loft(self):

    shapes=self.getPinObjectsA('shapes')
    if shapes is None or len(shapes)==0:
        sayErOb(self,"no shapes")
        return

    ws=[]

    for s in shapes:
        say(s,s.Wires,s.Edges)
        
        try:
            ws += [s.Wires[0]]
        except:
            ws += [s.Edges[0]]

    say(ws)
    
    loft=Part.makeLoft(ws,
        self.getData('solid'),self.getData('ruled'),
        self.getData('closed'),self.getData('maxDegree'))
    
    self.setPinObject('Shape_out',loft)
    



def run_FreeCAD_Sweep(self):


    profile=self.getPinObject('profile')
    profiles=self.getPinObjectsA('profiles')   
    if profile is None and profiles is None:
        sayErOb(self,"profile or profiles not defined")
        return


    if self.getPinObject('path') is None:
        sayErOb(self,"path not defined")
        return
        

    path=self.getPinObject('path').Edge1

    say(path)     # path sollte ein wire sein !!   
    
    if profile is not None:
        a=FreeCAD.ActiveDocument.addObject('Part::Feature','profile')
        a.Shape=profile
        pps=[a]

    else:
        pps=[]
        for p in profiles:
            pa=FreeCAD.ActiveDocument.addObject('Part::Feature','profile')
            pa.Shape=p
            pps += [pa]
    
    b=FreeCAD.ActiveDocument.addObject('Part::Feature','path')
    b.Shape=path
    FreeCAD.activeDocument().recompute(None,True,True)
    
    sw=FreeCAD.ActiveDocument.addObject('Part::Sweep','Sweep')   
    sw.Sections= pps
    sw.Spine=(b,['Edge1',])    
    sw.Solid=False
    sw.Frenet=False
    FreeCAD.activeDocument().recompute(None,True,True)
    
    self.setPinObject('Shape_out',sw.Shape)

    FreeCAD.activeDocument().removeObject(sw.Name)   
    FreeCAD.activeDocument().removeObject(b.Name)
    
    for p in pps:
        FreeCAD.activeDocument().removeObject(p.Name)
    






def run_FreeCAD_Seam(self):
    if  self.getPinObject("shapeA") is None:
        sayErOb(self,"no ShapeA")
        return
        
    fa=self.getPinObject("shapeA").Surface.copy()
    auflip=self.getData("flipUA")
    avflip=self.getData("flipVA")
    aswap=self.getData("swapA")
    ta=self.getData("tangentA")
    ta=(100+ta)/400
    
    fb=self.getPinObject("shapeB").Surface.copy()
    buflip=self.getData("flipUB")
    bvflip=self.getData("flipVB")
    bswap=self.getData("swapB")
    tb=self.getData("tangentB")
    tb=(100+tb)/400
    seamonly=self.getData("seamonly")
  

    # daten holen und neu aufbauen
    faud=fa.UDegree
    favd=fa.VDegree

    fbud=fb.UDegree
    fbvd=fb.VDegree

    ap=np.array(fa.getPoles())
    bp=np.array(fb.getPoles())
    favk=np.array(fa.getVKnots())
    fbvk=np.array(fb.getVKnots())
    fauk=np.array(fa.getUKnots())
    fbuk=np.array(fb.getUKnots())

    favk -= favk[0]
    fbvk -= fbvk[0]


    
    
    famu=np.array(fa.getUMultiplicities())
    fbmu=np.array(fb.getUMultiplicities())
    famv=np.array(fa.getVMultiplicities())
    fbmv=np.array(fb.getVMultiplicities())

    fa=Part.BSplineSurface()
    fa.buildFromPolesMultsKnots(ap,famu,famv,fauk,favk,False,False,faud,favd)
    fb=Part.BSplineSurface()
    fb.buildFromPolesMultsKnots(bp,fbmu,fbmv,fbuk,fbvk,False,False,fbud,fbvd)


    if auflip:
        famv=famv[::-1]
        ap=np.flipud(np.array(ap))
        fa=Part.BSplineSurface()
        fa.buildFromPolesMultsKnots(ap,famu,famv,fauk,favk,False,False,faud,favd)

    if avflip:
        famu=famu[::-1]
        ap=np.fliplr(np.array(ap))
        fa=Part.BSplineSurface()
        fa.buildFromPolesMultsKnots(ap,famu,famv,fauk,favk,False,False,faud,favd)

    if aswap:
        fa=Part.BSplineSurface()
        ap=ap.swapaxes(0,1)
        fa.buildFromPolesMultsKnots(ap,famv,famu,favk,fauk,False,False,favd,faud)

    if buflip:
        fbmv=fbmv[::-1]
        bp=np.flipud(np.array(bp))
        fb=Part.BSplineSurface()
        fb.buildFromPolesMultsKnots(bp,fbmu,fbmv,fbuk,fbvk,False,False,fbud,fbvd)

    if bvflip:
        fbmu=fbmu[::-1]
        bp=np.fliplr(np.array(bp))
        fb=Part.BSplineSurface()
        fb.buildFromPolesMultsKnots(bp,fbmu,fbmv,fbuk,fbvk,False,False,fbud,fbvd)

    if bswap:
        fb=Part.BSplineSurface()
        bp=bp.swapaxes(0,1)
        fb.buildFromPolesMultsKnots(bp,fbmv,fbmu,fbvk,fbuk,False,False,fbvd,fbud)

    ud=max(fa.UDegree,fb.UDegree,3)
    vd=max(fa.VDegree,fb.VDegree,3)

    fa.increaseDegree(ud,vd)
    fb.increaseDegree(ud,vd)

    favk=np.array(fa.getVKnots())
    fbvk=np.array(fb.getVKnots())

    say(favk)
    say(fbvk)
    sayl("############")
    
    assert favk[0]==fbvk[0]

    am=favk[-1]
    bm=fbvk[-1]

    famu=fa.getVMultiplicities()
    fbmu=fb.getVMultiplicities()

    for k,m in zip(favk,famu):
        fb.insertVKnot(k*bm/am,m,0)

    for k,m in zip(fbvk,fbmu):
        fa.insertVKnot(k*am/bm,m,0)

    pas=np.array(fa.getPoles())
    pbs=np.array(fb.getPoles())

    # nur seam
    poles=[pas[-1],
            pas[-1]*(1+ta)-pas[-2]*ta,pas[-1]*(1+2*ta)-pas[-2]*ta*2,
            pbs[0]*(1+2*tb)-pbs[1]*2*tb,pbs[0]*(1+tb)-pbs[1]*tb,pbs[0]]


    say(np.array(poles).shape)
    ae=[FreeCAD.Vector(*p) for p in pas[-1]]
    ap=[FreeCAD.Vector(*p) for p in pas[-2]]
    
    be=[FreeCAD.Vector(*p) for p in pbs[0]]
    bp=[FreeCAD.Vector(*p) for p in pbs[1]]
    
    lens=[(a-b).Length for a,b in zip(ae,be)]
    say("-----------")
    #say("lens",lens)
    tas=[(e-p).normalize() for e,p in zip(ae,ap)]
    tbs=[(e-p).normalize() for e,p in zip(be,bp)]
    
    #ta=0.3
    #tb=0.3
    say("ta tb",ta,tb)
    
    poles=[[a,a+tav*ta*l,a+tav*2*ta*l,b+tbv*2*tb*l,b+tbv*tb*l,b] for a,tav,tbv,b,l  in zip(ae,tas,tbs,be,lens)]
    poles=np.array(poles).swapaxes(0,1)
    say(np.array(poles).shape)



    say("----------------")
    poles=np.array(poles)
    say(poles[:,0])
    if FreeCAD.Vector(*poles[0,0])==FreeCAD.Vector(*poles[-1,0]):
        say("Enden gleich")
        poles[:,0]=poles[0,0]
    if FreeCAD.Vector(*poles[0,-1])==FreeCAD.Vector(*poles[-1,-1]):
        say("Enden gleich 2")
        poles[:,-1]=poles[0,-1]

    vknots=fa.getVKnots()
    vmults=fa.getVMultiplicities()

    uaknots=fa.getUKnots()
    uamults=fa.getUMultiplicities()

    ubknots=fb.getUKnots()
    ubmults=fb.getUMultiplicities()

    say("seamonly",seamonly)
    if seamonly:

        if ud<=3:
            um=[ud+1,1,1,ud+1]

        elif ud==4:
            um=[5,1,5]

        elif ud==5:
            um=[6,6]

    else:

        if ud<=3:
            um2=[ud,1,1,ud]

        elif ud==4:
            um2=[4,1,4]

        elif ud==5:
            um2=[5,5]

        poles=np.concatenate([pas[:-1],poles,pbs[1:]])
        um=uamults[:-1]+um2+ubmults[1:]

    ku=range(len(um))

    degA=ud
    degB=vd

    sf=Part.BSplineSurface()
    sf.buildFromPolesMultsKnots(poles,um,vmults,ku,vknots,False,False,degA,degB)
    shape=sf.toShape()
    say(shape)
    #Part.show(shape)
    self.setPinObject("Shape_out",shape)



def pinHasData(self,pinname):
    return len(self.getPinByName(pinname).affected_by) >0

def run_FreeCAD_ApplyPlacements(self):

    comp=[]
    s=Part.makeBox(200,1000,200)
    pms=self.getData("Placements")
    say(pms)
    #pms=self.getPinPlacements("Placements")
    
    if pinHasData(self,"Shape_in"):
        s=self.getPinObject("Shape_in")
    else:
        s=None
    
    say("got",pms)
    say("s",s)
    #s=Part.makeBox(2,100,2)

    if  s is not None:
        say(s)
        
        # say(pms)
        for p in pms:
            
            
            ss=s.copy()
            say("ss placement",ss.Placement)
            ss.Placement=p.copy()
            say("ss placement",ss.Placement)
            comp += [ss]
        
        #self.setPinObject("Shape_out",Part.Compound(comp))
        sayl()
        self.setPinObject("Shape_out",ss)
        say("ss",ss)
        #Part.show(ss)
        #Part.show
    
    
    else:
        if pinHasData(self,"Shapes"):
            ss=self.getPinObjectsA("Shapes")
        else:
            ss=[]
        say(ss)
        if len(ss)>0:
            shapes=[s.copy() for s in ss]
            for s,pm in zip(shapes,pms):
                s.Placement=pm
            self.setPinObject("Shape_out",Part.Compound(shapes))
        else:
            say("POINTS---------")
            points=self.getData('points')
            say(np.array(points).shape)
            if len(np.array(points).shape) == 2:
                points_out=[pm.multVec(FreeCAD.Vector(*p)) for (p,pm) in zip(points,pms)]

            elif len(np.array(points).shape) == 3:
                points_out=[[pm.multVec(FreeCAD.Vector(*p)) for p in ps] for ps,pm in zip(points,pms)]
            else:
                say("no points abbruch")
                return
            self.setData("points_out",points_out)


