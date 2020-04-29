import numpy as np
import random
import time
import os.path
from os import path
import matplotlib.pyplot as plt
import scipy.interpolate


import FreeCAD
import FreeCADGui

import Part

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.pfwrap as pfwrap

from pivy import coin

import nodeeditor
import nodeeditor.cointools
#reload(nodeeditor.cointools)
from nodeeditor.cointools import *
      

       
import nodeeditor.tools as noto
#reload(noto)

def run_FreeCAD_Object(self):
    sayW("not implemented")

       

def run_FreeCAD_Nurbs(self):
    
    #shape=FreeCAD.ActiveDocument.Cone.Shape.Face1
    #shape=FreeCAD.ActiveDocument.Sphere.Shape.Face1
    shape=self.getPinObject("shape")
    if shape is None:
        sayErOb(self,"no shape")
        return

        return
    n=shape.toNurbs()
    say(n.Faces)
    say(n.Edges)
    sf=n.Face1.Surface
    ssff=Part.BSplineSurface()
    ssff.buildFromPolesMultsKnots(sf.getPoles(),
        sf.getUMultiplicities(), sf.getVMultiplicities(),
        sf.getUKnots(),sf.getVKnots(),False,False,sf.UDegree,sf.VDegree)
    
    ff=ssff.toShape()
    self.setPinObject("Shape_out",ff)
    



def runraw(self):
    sayl("#+")
    # called biy FreeCAD_Object createpins
    objname=self.objname.getData()
    fobj=FreeCAD.ActiveDocument.getObject(objname)

    if fobj == None:
        say("cannot create pins because no FreeCAD object for name {}".format(objname))
        return []
    ps=fobj.PropertiesList
    if 10:
        sayl('#')
        say("FreeCAD object Properties ---")
        for p in ps:
            say (p)


    pins=[]
    ipm=self.namePinInputsMap

    if 0:
        say("ipm.keys() for ",objname,fobj.Name,fobj.Label)
        for k in ipm.keys():
            say(k)

#---------------

    recomputepins=[]
    for p in ps:
        say("X",p)
        try:
            a=getattr(fobj,p)
        except:
            say ("ignore problem with prop",p," fix it later !!")
            continue

        if p in ["Placement","Shape",
                "MapMode",
                "MapReversed","MapPathParameter",
                "Attacher",
                "AttacherType",
                "AttachmentOffset","ExpressionEngine","Support"]:
            pass
            continue


        if p in ipm.keys():
            print("IGNORE '{}' - exists already".format(p))
            continue

        cn=a.__class__.__name__

        if p.startswith("aLink"):
            # zu tun
            continue
#       print("################",cn,p,a)
        if cn=="list" and p.endswith('List'):

            r2=p.replace('List','Pin')
            r=r2[1:]
#           say("--------------",p,r,r2)
            if r=="IntegerPin":
                r="IntPin"
            try:
                p1 = self.createInputPin(p, r ,[],structure=PinStructure.Array)
                p2 = self.createOutputPin(p+"_out", r ,[],structure=PinStructure.Array)
                pins += [p1,p2]
            except:
                say("cannot create list pin for",p,r2)

            continue



        if cn=="Quantity" or cn=="float":
            pintyp="FloatPin"
        elif  cn=="Vector":
            pintyp="VectorPin"
        elif  cn=="str" or cn=="unicode":
            pintyp="StringPin"
        elif  cn=="bool":
            pintyp="BoolPin"
        elif  cn=="int":
            pintyp="IntPin"
        elif  cn=="Placement":
            pintyp="PlacementPin"
        elif  cn=="Rotation":
            pintyp="RotationPin"


        elif cn=='list' or cn == 'dict' or cn=='tuple' or cn=='set':
            # zu tun
            continue
        elif cn=='Material'  or cn=='Shape' or cn=='Matrix' :           # zu tun
            continue
        elif cn=='NoneType' :
            # zu tun
            continue


        else:
            say(p,cn,a,"is not known")
            continue

        say("-----------------")

        pinname=p
        pinval=a

        say("create pin for ",pintyp,pinname,pinval)
        '''
        if pinname not in oldpinnames:
            pintyp="ShapePin"
            p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
            try:
                uiPin = self.getWrapper()._createUIPinWrapper(p2)
                uiPin.setDisplayName("{}".format(p2.name))
            except:
                pass

        self.setPinObject(pinname,subob)
        '''
        p1 = CreateRawPin(pinname,self, pintyp, PinDirection.Input)
        p2 = CreateRawPin(pinname+"_out",self, pintyp, PinDirection.Output)

        try:
            uiPin = self.getWrapper()._createUIPinWrapper(p2)
            uiPin.setDisplayName("{}".format(p2.name))
        except:
            pass

        try:
            uiPin = self.getWrapper()._createUIPinWrapper(p1)
            uiPin.setDisplayName("{}".format(p1.name))
        except:
            pass


        p1.enableOptions(PinOptions.Dynamic)
    #   p1.recomputeNode=True
        recomputepins += [p1]
        try:
            p1.setData(pinval)
            p2.setData(pinval)
        except:
            say("problem setting",p)
        say("created:",p1)

        pins  += [p1,p2]


    sayl()

    for p in recomputepins:
        p.recomputeNode=True

    for p in pins:
        p.group="FOP"
    sh=fobj.Shape
    self.setPinObject("Shape_out",sh)
    
    return pins


def run_enum(self):
    say("process the rawPin data ")
    say("rawPin is",self.pin._rawPin)
    say("values ...")
    for v in self.pin._rawPin.values:
        say(v)



def f4(self):
    say("FreeCAD Ui Node runs f4")
    say("nothing to do, done")


def run_FreeCAD_View3D(self, *args, **kwargs):

    name=self.getData('name')
    Shape=self.getPinObject('Shape_in')
    workspace=self.getData('Workspace')
    mode='1'
    wireframe=False
    transparency=50
    #+#todo make the parameters to pins
    timeA=time.time()
    shape=self.getPinObject('Shape_in')
    s=shape
    say("--------",s,s.Volume,s.Area)
    l=FreeCAD.listDocuments()
    if workspace=='' or workspace=='None':
        w=FreeCAD.ActiveDocument
        '''
        try:
            w=l['Unnamed']
        except:
            w=FreeCAD.newDocument("Unnamed")
            FreeCADGui.runCommand("Std_TileWindows")
        '''
    else:
        if workspace in l.keys():
            w=l[workspace]
        else:
            w=FreeCAD.newDocument(workspace)

            #Std_CascadeWindows
            FreeCADGui.runCommand("Std_ViewDimetric")
            FreeCADGui.runCommand("Std_ViewFitAll")
            FreeCADGui.runCommand("Std_TileWindows")


    f=w.getObject(name)
    if f == None:
        f = w.addObject('Part::Feature', name)

    say("off-------",self.getData('off'))
    if self.getData('off'):
        f.ViewObject.hide()
        return
    else:
        f.ViewObject.show()

    if s  !=  None:
        if 1 or s.Volume != 0:
            f.Shape=s
        else:  
            t=Part.makeBox(0.001,0.001,0.001)#.toShape()
            f.Shape=t

    f.recompute()
    f.purgeTouched()

    if 1:
        if not wireframe:
            f.ViewObject.DisplayMode = "Flat Lines"
            f.ViewObject.ShapeColor = (random.random(),random.random(),1.)
        else:
            f.ViewObject.DisplayMode = "Wireframe"
            f.ViewObject.LineColor = (random.random(),random.random(),1.)





from PyFlow.Packages.PyFlowBase.Factories.UINodeFactory import createUINode


def run_foo_compute(self,*args, **kwargs):
    pass


def run_visualize(self,*args, **kwargs):
    say(self._rawNode)
    say("create vid3d object in graph")
    gg=self.graph()
    x,y=-150,-100
    nodeClass='FreeCAD_view3D'
    #t3 = pfwrap.createNode('PyFlowFreeCAD',nodeClass,"MyPolygon")
    #t3.setPosition(x,y)
    #gg.addNode(t3)
    #uinode=createUINode(t3)
    #say(uinode)
    aa=self.canvasRef().spawnNode(nodeClass, x, y)
    say(aa.__class__)
    say("connect Shape withj vie3d.shape ...")
    FreeCAD.aa=aa
    FreeCAD.aa=self._rawNode['outExec']
    pfwrap.connect(self._rawNode,'Shape_out',aa._rawNode,'Shape_in')

    aa._rawNode.setData('name','View_'+self._rawNode.name)

    if self._rawNode["outExec"].hasConnections():
        for pin in self._rawNode["outExec"].affects:
            pfwrap.connect(self._rawNode,'outExec',aa._rawNode,'inExec')
            pfwrap.connect(aa._rawNode,'outExec',pin.owningNode(),pin.name)
    pfwrap.connect(self._rawNode,'outExec',aa._rawNode,'inExec')

    #refrehs view
    instance=pfwrap.getInstance()
    data = instance.graphManager.get().serialize()
    instance.graphManager.get().clear()
    instance.loadFromData(data)

    





def run_FreeCAD_Tripod(self,*args, **kwargs):
    sayl()
    f=self.getPinObject('Shape')
    if f is None: return
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    #if f.__class__.__name__  == 'Face':
    
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    say(umin,umax,vmin,vmax)
    u,v=self.getData("u"),self.getData("v")
    
    say(f)
    uu=umin+(umax-umin)*0.1*u
    vv=vmin+(vmax-vmin)*0.1*v

    # bechränkung auf innen
    uu=umin+(umax-umin)*0.005*(u+100)
    vv=vmin+(vmax-vmin)*0.005*(v+100)
    say(uu,vv)
    uks=sf.getUKnots()
    vks=sf.getVKnots()
    say(uks)
    say(vks)
    for i in range(len(uks)-1):
        if uks[i]<=uu and uu<uks[i+1]:
            say("u seg gefuden",i)
            break
    say("usgement",i)
    us=i
    for i in range(len(vks)-1):
        if vks[i]<=vv and vv<vks[i+1]:
            say("v seg gefuden",i)
            break
    say("vsgement",i)
    vs=i
    say("segment",us,vs)
    poles=sf.getPoles()
    say(np.array(poles).shape)
    arr=np.array(poles)[us:us+4,vs:vs+4]
    # nur ein punkt
    arr=np.array(poles)[us:us+1,vs:vs+1]
    arr=[sf.value(uu,vv)]
    
    #say(arr.shape)
    self.setData('poles',arr)
    self.setData('polesIndex',[us,vs])
    
    



    pos=sf.value(uu,vv)
    self.setData('position',pos)
    
    if self.getData('curvatureMode'): 
        # curvature
        t1,t2=sf.curvatureDirections(uu,vv)


    else: # tangents
        t1,t2=sf.tangent(uu,vv)
#       t1=t1.normalize()
#       t2=t2.normalize()

    if self.getData('directionNormale'): 
            n=t1.cross(t2).normalize()
    else: 
            n=t2.cross(t1).normalize()


    if self.getData('display'):
        obj=self.getObject()
        shape=Part.makePolygon([pos,pos+t1*10,pos+t2*5,pos,pos+n*5],
                        )
        obj.Shape=shape





def check(xa,ya,xb,yb):
    return (0<=xa and xa<=1) and (0<=ya and ya<=1) and (0<=xb and xb<=1) and (0<=yb and yb<=1)

def trim(xa,ya,xb,yb):
    if xa<0:
        t=-xb/(xa-xb)
        xa2=0
        ya2=t*ya+(1-t)*yb
        return (xa2,ya2,xb,yb)
    if xa>1:
        t=(1-xb)/(xa-xb)
        xa2=1
        ya2=t*ya+(1-t)*yb
        return (xa2,ya2,xb,yb)

    if ya<0:
        t=-yb/(ya-yb)
        ya2=0
        xa2=t*xa+(1-t)*xb
        return (xa2,ya2,xb,yb)
    if ya>1:
        t=(1-yb)/(ya-yb)
        ya2=1
        xa2=t*xa+(1-t)*xb
        return (xa2,ya2,xb,yb)

    if xb<0:
        t=-xa/(xb-xa)
        xb2=0
        yb2=t*yb+(1-t)*ya
        return (xa,ya,xb2,yb2)
    if xb>1:
        t=(1-xa)/(xb-xa)
        xb2=1
        yb2=t*yb+(1-t)*ya
        return (xa,ya,xb2,yb2)

    if yb<0:
        t=-ya/(yb-ya)
        yb2=0
        xb2=t*xb+(1-t)*xa
        return (xa,ya,xb2,yb2)
    if yb>1:
        t=(1-ya)/(yb-ya)
        yb2=1
        xb2=t*xb+(1-t)*xa
        return (xa,ya,xb2,yb2)


    return xa,ya,xb,yb



def mapEdgesLines( uvedges,face):

    if face == None:
        sayW("no face")
        return Part.Shape()
    col=[]
    say("face",face)
    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface
    for edge in uvedges:
        ua,va,ub,vb=edge
        ua=umin+ua*(umax-umin)
        va=vmin+va*(vmax-vmin)

        ub=umin+ub*(umax-umin)
        vb=vmin+vb*(vmax-vmin)
        
        pa=sf.value(ua,va)
        pb=sf.value(ub,vb)
        say(pa)
        col += [Part.makePolygon([pa,pb])]

    shape=Part.Compound(col)
    return shape

def mapEdgesCurves( edges,face):
    '''geschmiegte V<ariante'''

    col=[]
    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface
    for edge in edges:
        ua,va,ub,vb=edge
        ua=umin+ua*(umax-umin)
        va=vmin+va*(vmax-vmin)
        ub=umin+ub*(umax-umin)
        vb=vmin+vb*(vmax-vmin)

        a=FreeCAD.Base.Vector2d(ua,va)
        b=FreeCAD.Base.Vector2d(ub,vb)
        bs2d = Part.Geom2d.BSplineCurve2d()
        bs2d.buildFromPolesMultsKnots([a,b],[2,2],[0,1],False,1)
        ee = bs2d.toShape(sf)
        col += [ee]

    shape=Part.Compound(col)
    return shape

def mapPoints(pts,face):
    '''create subface patch boundet by pts on face'''

    if face == None:
        sayW("no face")
        return []

    umin,umax,vmin,vmax=face.ParameterRange
    sf=face.Surface

    say("DEBUG---------------") # hier ist noch verfeinerugn noetig
    if 0:
        ptsn=[]
        for p in pts:
            if p.x<0:
                p.x=0.00001
            if p.x>1:
                p.x=0.99999
            if p.y<0:
                p.y=0.00001
            if p.y>1:
                p.y=0.99999
                
            ptsn += [p]
        pts=ptsn

    col=[]
    for p in pts:
        ua,va = p[0],p[1]
        ua=umin+ua*(umax-umin)
        va=vmin+va*(vmax-vmin)
        a=FreeCAD.Base.Vector2d(ua,va)
        col += [a]
    col += [col[0]] # close curve

    bs2d = Part.Geom2d.BSplineCurve2d()
    ms=[2]+[1]*(len(col)-2)+[2]
    ks=range(len(ms))
    bs2d.buildFromPolesMultsKnots(col,ms,ks,False,1)
    eee = bs2d.toShape(sf)

    edge=eee.Edges[0]
    splita=[(edge,face)]
    r=Part.makeSplitShape(face, splita)

    edge.reverse()
    splitb=[(edge,face)]
    r2=Part.makeSplitShape(face, splitb)

    shapes=[]

    try:
        shapes += [r2[0][0]]
    except:
        pass
    try:
        shapes += [rc]
    except:
        pass

    shapes += [eee]

    return shapes



#---------------

def cylindricprojection(self,*args, **kwargs):

    s=App.activeDocument().ReflectLines001.Shape

    eds=[]
    for e in s.Edges:
        pts2=[]
        pts=e.discretize(100)
        for p in pts:
            h=p.y
            arc=np.arctan2(p.x,p.z)
            r=FreeCAD.Vector(p.x,p.z).Length
            R=150
            p2=FreeCAD.Vector(np.sin(arc)*R,h,np.cos(arc)*R)
            pts2 += [p2]

        Part.show(Part.makePolygon(pts2))

 


#--------------------------

import sys
if sys.version_info[0] !=2:
    from importlib import reload






def run_FreeCAD_Tread(self,produce=False, **kwargs):

    k=self.getData("noise")

    def rav(v):
        '''add a random vector to a vector'''
        return v+FreeCAD.Vector(0.5-random.random(),0.5-random.random(),(0.5-random.random())*1)*k


    pts=[self.getData("point_"+str(i)) for i in range(8)]
    pol=Part.makePolygon(pts+[pts[0]])
    f=Part.Face(pol)

    v=FreeCAD.Vector(0,0,120)
    pts2=[p+v for p in pts]
    pol2=Part.makePolygon(pts2+[pts2[0]])
    f2=Part.Face(pol2)
    colf=[f,f2]

    for i in range(8):
        pol=Part.makePolygon([pts[i-1],rav(pts[i]),rav(pts2[i]),rav(pts2[i-1]),pts[i-1]])
        f=Part.makeFilledFace(pol.Edges)
        colf += [f]

    comp=Part.Compound(colf)
    comp.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(1,0,0),90)
    self.setPinObject("Compound_out",comp)

    for tol in range(60,150):
        colf2=[c.copy() for c in colf]
        try:
            for f in colf2:
                f.Tolerance=tol
            sh=Part.Shell(colf2)
            sol=Part.Solid(sh)
            sol.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(1,0,0),90)
            if sol.isValid():
                say("solid created with tol",tol)
                if produce:
                    Part.show(sol)
                #cc=self.getObject();cc.Shape=sol
                self.setPinObject("Shape_out",sol)
                break
        except:
            pass




def run_FreeCAD_RefList(self,*args, **kwargs):

        if 0:
            pintyp="VectorPin"
            pinname="Base"
            p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Input)
            try:
                uiPin = self.getWrapper()._createUIPinWrapper(p2)
                uiPin.setDisplayName("{}".format(p2.name))
            except:
                pass


        #clean up
        pins=self.getOrderedPins()
        for p in pins:
            if not p.isExec() and p.direction  !=  PinDirection.Input :
                p.kill()

        name="objects"
        pinname=name
        pintyp="ShapeListPin"
        p2 = CreateRawPin(pinname,self, pintyp, PinDirection.Output)
        try:
            uiPin = self.getWrapper()._createUIPinWrapper(p2)
            uiPin.setDisplayName("{}".format(p2.name))
        except:
            pass

#       self.setPinObject(pinname,subob)

        ss=FreeCADGui.Selection.getSelection()
        
        self.setPinObjects(pinname,ss)
        
        # platzieren
        
#        positions=self.getData('positions')
#        rotations=self.getData('rotations')
#        for p,r in zip(positions,rotations)[:3]:
#            print p
#            print r
#            print
#        
#        
#        objs=self.getPinObjects(pinname)
#        for obj,pos,rot in zip(objs,positions,rotations):
#            obj.Placement=FreeCAD.Placement(pos,rot)






def run_genPart(fun,*args,**kwargs):

    return # daktiviert
    
    sayl("-create parrt for debugging by timer decorator---------------------")
    obj=args[0][0]
#   say(obj.name)
    name=obj.name
    cc=FreeCAD.ActiveDocument.getObject(name)
    if cc == None:
        cc=FreeCAD.ActiveDocument.addObject("Part::Feature",name)

    shape=None
    for shapename in ["Shape_out","Edge_out","Face_out","Compound_out","Shape"]:
        try:
            shape=obj.getPinObject(shapename)
            break
        except:
            say(shapename)
            pass

    if shape != None:
        cc.Shape=shape
        say("Shape gesetzt",name,shapename,shape)
    else:
        say("no shape pin found")


def run_FreeCAD_bakery(self):

    workspace=self.getData("Workspace")
    name=self.getData("name")
    shape=self.getPinObject('Shape_in')
    s=shape

    l=FreeCAD.listDocuments()
    if workspace=='' or workspace=='None':
        try:
            w=l['Unnamed']
        except:
            w=FreeCAD.newDocument("Unnamed")
            FreeCADGui.runCommand("Std_TileWindows")
    else:
        if workspace in l.keys():
            w=l[workspace]
        else:
            w=FreeCAD.newDocument(workspace)

            #Std_CascadeWindows
            FreeCADGui.runCommand("Std_ViewDimetric")
            FreeCADGui.runCommand("Std_ViewFitAll")
            FreeCADGui.runCommand("Std_TileWindows")

    #s=store.store().get(shape)

    f=w.getObject(name)
    #say("AB",time.time()-timeA)
    if 1 or f == None:
        f = w.addObject('Part::Feature', name)
    if s  !=  None:
    #    say("AC",time.time()-timeA)
        f.Shape=s
    #    say("AD",time.time()-timeA)
    #say("shape",s);say("name",name)
    #say("A",time.time()-timeA)
    w.recompute()
    #say("B",time.time()-timeA)
    if 1:
        color=(random.random(),random.random(),1.)
        f.ViewObject.ShapeColor = color
        f.ViewObject.LineColor = color
        f.ViewObject.PointColor = color

    #f.ViewObject.Transparency = transparency

    #say("E",time.time()-timeA)





def createToy():

    countA=11
    countB=11

    degA=3
    degB=3

    poles=np.zeros(countA*countB*3).reshape(countA,countB,3)
    for u in range(countA):
        for v in range(countB):
            poles[u,v,0]=10*u
            poles[u,v,1]=10*v

    poles[1:-1,:,2]=30
    poles[2:-2,:,2]=60
    
    poles[3:8,3:8,2]=180
    poles[4,4,2]=150
    poles[6,4,2]=220

    multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
    multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
    knotA=range(len(multA))
    knotB=range(len(multB))

    sf=Part.BSplineSurface()
    sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
    shape=sf.toShape()
    Part.show(shape)



def run_FreeCAD_ConnectPoles(self):

    ySortedPins = sorted(self.polesin.affected_by, key=lambda pin: pin.owningNode().y)
    #say("sortedPins",ySortedPins)
    ovl=self.getData('overlay')
    ws=[]
    for p in ySortedPins:
        #say(p)
        w=np.array(p.getData())
        ws += [w]
        say(w.shape)

    if ovl == 1:
        for i,w in enumerate(ws):
            if i == 0: 
                pl=[w[:-1]]
                last=w[-1]
            else:
                m=(last+w[0])*0.5
                pl += [[m],w[1:-1]]
            last=w[-1]
        pl += [[last]]
        poles=np.concatenate(pl)

    
    if ovl == 2:
        say("ovl tangent")
        a=ws[0][-2]
        b=ws[0][-1]
        c=ws[1][0]
        d=ws[1][1]
        fa=1+self.getData('tangentA')*0.01
        fb=1+self.getData('tangentB')*0.01
        
        a2=b+fa*(b-a)
        b2=c+fb*(c-d)

        pl = [ws[0],[a2,b2],ws[1]]
        poles=np.concatenate(pl)
        say(ws[0].shape[0])
        say(ws[1].shape[0])
        kns=(ws[0].shape[0],ws[1].shape[0])



    elif ovl == 0:
        if len(ws)==0: return
        poles=np.concatenate(ws)
    
    if 1:
        (countA,countB,_)=poles.shape
        degA=3
        degB=3

        if ovl == 2:
            multA = [degA+1]+[1]*(kns[0]-1-degA)+[degA]
            multA += [degA]+[1]*(kns[1]-1-degA)+[degA+1]
        else:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]

        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]

        knotA=range(len(multA))
        knotB=range(len(multB))

        sf=Part.BSplineSurface()
        sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
        shape=sf.toShape()
        self.setPinObject("Shape_out",shape)

    self.setData("umults_out",multA)
    say("connected")
    self.setData('poles_out',poles.tolist())

 
    say(self.getWrapper())
    FreeCAD.b=self.getWrapper().getHeaderText()
    say("end neue version")





def topokey(s):
    a=s.PrincipalProperties['Moments']
    f=a[2]
    return tuple([round(s.Area/f**2,1),round(s.Volume/f**3,1),round(a[0]/f,1),round(a[1]/f,1),round(a[2]/f,1)])
    return tuple([round(s.Area,1),round(s.Volume,1),round(a[0],1),round(a[1],1),round(a[2],1)])


def run_FreeCAD_topo(self):
    say("topo2")
    topomap={}
    topomap2={}
    sh=FreeCAD.ActiveDocument.Fusion.Shape
    sh=FreeCAD.ActiveDocument.Fusion001.Shape
    for i,s in enumerate(sh.Faces):
        #print (topokey(s))
        try:
            topomap[topokey(s)] += ["A.Face{}".format(i+1)]
            topomap2[topokey(s)] += [s]
        except:
            topomap[topokey(s)] = ["A.Face{}".format(i+1)]
            topomap2[topokey(s)] = [s]
    

    
    sh=FreeCAD.ActiveDocument.Fusion001.Shape
    sh=FreeCAD.ActiveDocument.Clone.Shape
    for i,s in enumerate(sh.Faces):
        #print (topokey(s))
        try:
            topomap[topokey(s)] += ["B.Face{}".format(i+1)]
            topomap2[topokey(s)] += [s]
        except:
            topomap2[topokey(s)] = [s]
            topomap[topokey(s)] = ["B.Face{}".format(i+1)]

    changed=[]
    lost=[]
    new=[]
    for k in topomap:
        print (k,topomap[k])
        if len(topomap[k]) == 1:
            
                changed += topomap2[k]
                if topomap[k][0].startswith("A"): 
                    lost +=  topomap2[k]
                else:
                    new +=  topomap2[k]
                    

    comp=Part.makeCompound(changed)
    #Part.show(comp)
    self.setPinObject("Shape_out",comp)
    self.setPinObject("Shape_lost",Part.makeCompound(lost))
    self.setPinObject("Shape_new",Part.makeCompound(new))
    
    mods=[]
    for fa in lost:
        for fb in new:
            tt={}
            anz=0
            lanz=(len(fa.Edges),len(fb.Edges))
            for e in fa.Edges:
                tt[topokey(e)]=1
            for e in fb.Edges:
                try:
                    if tt[topokey(e)]:
                        anz += 1
                except:
                    pass
            if anz != 0:
                say("uebereinstimmungen",anz,lanz)
                mods += [fa,fb]

    if 0:
        say("Edges...")
        topomapE={}
        topomapE2={}
        sh=FreeCAD.ActiveDocument.Fusion.Shape
        
        for i,s in enumerate(sh.Edges):
            #print (topokey(s))
            try:
                topomapE[topokey(s)] += ["A.Edge{}".format(i+1)]
                topomapE2[topokey(s)] += [s]
            except:
                topomapE[topokey(s)] = ["A.Edge{}".format(i+1)]
                topomapE2[topokey(s)] = [s]
        
        
        sh=FreeCAD.ActiveDocument.Fusion001.Shape
        for i,s in enumerate(sh.Edges):
            #print (topokey(s))
            try:
                topomapE[topokey(s)] += ["B.Edge{}".format(i+1)]
                topomapE2[topokey(s)] += [s]
            except:
                topomapE2[topokey(s)] = [s]
                topomapE[topokey(s)] = ["B.Edge{}".format(i+1)]



        
        for k in topomapE:
            print (k,topomapE[k])
            if len(topomapE[k]) == 1:
                changed += topomapE2[k]
            
    comp=Part.makeCompound(changed)
    comp=Part.makeCompound(mods)
    #Part.show(comp)
    self.setPinObject("Shape_out",comp)



def run_FreeCAD_conny(self):
 
    edges=self.getPinObjects(pinname='Shapes_in',sort=False)   
    sayl()
    neighbor=[]
    gaps=[]

    ec=len(edges)
#    say("len edges",ec)
#    say("edges")
    e2=[]
    for e in edges:
        #say(e,e.__class__)
        try: e2 += [e.Edge1]
        except:
            e2 += [e]
           
    e=e2
    #say(e)
    #return 
        
        
        
        
        
        
    for i in range(ec):
        sf=-1
        sflag=0
        sdist=10**8
        f=-1
        flag=0
        dist=10**8
        
        vs=edges[i].Vertexes[0].Point
        ve=edges[i].Vertexes[1].Point
        #say(vs,ve)
        for j in range(ec):
            if i == j:
                continue
            if (edges[j].Vertexes[0].Point-vs).Length <sdist:
                sf=j
                sdist=(edges[j].Vertexes[0].Point-vs).Length
                sflag=0
            if (edges[j].Vertexes[1].Point-vs).Length <sdist:
                sf=j
                sdist=(edges[j].Vertexes[1].Point-vs).Length
                sflag=1
            if (edges[j].Vertexes[0].Point-ve).Length <dist:
                f=j
                dist=(edges[j].Vertexes[0].Point-ve).Length
                flag=0
            if (edges[j].Vertexes[1].Point-ve).Length <dist:
                f=j
                dist=(edges[j].Vertexes[1].Point-ve).Length
                flag=1
        neighbor += [(sf,sflag,sdist,f,flag,dist)]
#        print (i,sf,sflag,sdist,f,flag,dist)

    # find neighbors chain of edges 
    e=0 # starting edge
    try:
        ee=neighbor[e][0]
    except:
        say("keine daten abbruch")
        return
    chain=[e,ee]
    for i in range(14):
        if neighbor[ee][0] not in chain:
            ee2=neighbor[ee][0]
            chain += [ee2]
            e=ee
            ee=ee2
        elif neighbor[ee][3] not in chain:
            ee2=neighbor[ee][3]
            chain += [ee2]
            e=ee
            ee=ee2

    print("chain",chain)



    # calculate gap filler for the chain
    pts=[]
    col=[]
  
    cc=len(chain)
    for i in range(cc):
        
        lmin=10**8
        ep=chain[i-1]
        e=chain[i]
        ff=-1
        # shortest gap between two edges of the chain
        for f in range(2):
            for fp in range(2):
                pa,pb=edges[e].Vertexes[f].Point,edges[ep].Vertexes[fp].Point
                
                l=(pa-pb).Length
                if l<lmin:
                    lmin=l
                    paa,pbb=pa,pb
                    polsa=edges[e].toNurbs().Edge1.Curve.getPoles()
                    polsb=edges[ep].toNurbs().Edge1.Curve.getPoles()

                    if ff == -1:
                        if (polsa[0]-polsb[0]).Length < (polsa[-1]-polsb[-1]).Length:
                            ff=0
                        else:
                            ff = 1
                    ff2= 1 - ff if  self.getData('ff') else 0




                    if f==ff2:
                        na=[polsa[0],polsa[1]]
                    else:
                        na=[polsa[-1],polsa[-2]]
                    if fp==ff2:
                        nb=[polsb[0],polsb[1]]
                    else:
                        nb=[polsb[-1],polsb[-2]]

        # create the gap filler
        if (na[0]-nb[0]).Length> 0.0001:

            #+# k should depend on size of gap (na[0]-nb[0]).Length
            k=self.getData("tangentForce")*0.05
            nn=[na[0],na[0]+(na[0]-na[1])*k,nb[0]+(nb[0]-nb[1])*k,nb[0]]
            
            ###simple line connection
            ##t=Part.makePolygon(nn)
            ##col += [Part.makePolygon([paa,pbb]).Edge1]

            t=Part.BSplineCurve()
            t.buildFromPolesMultsKnots(nn,[4,4],[0,1],False,3)
            gaps += [t.toShape().Edge1]
            col += [t.toShape().Edge1]

        col += [edges[ep].Edge1]

    # special case only two edges 
    if ec==2:
        col=[]
        gaps=[]

        polsa=edges[0].toNurbs().Edge1.Curve.getPoles()
        polsb=edges[1].toNurbs().Edge1.Curve.getPoles()
        
        ff= 1 if  self.getData('ff') else 0

        for [na,nb]  in  [
                    [[polsa[0],polsa[1]],[polsb[-1],polsb[-2]]],
                     [[polsa[-1],polsa[-2]],[polsb[0],polsb[1]]]
                     ]:
        
            if (na[0]-nb[0]).Length> 0.0001:
                
                k=self.getData("tangentForce")*0.05
                nn=[na[0],na[0]+(na[0]-na[1])*k,nb[0]+(nb[0]-nb[1])*k,nb[0]]
                
                t=Part.BSplineCurve()
                t.buildFromPolesMultsKnots(nn,[4,4],[0,1],False,3)
                gaps += [t.toShape().Edge1]
                col += [t.toShape().Edge1]

        col += [edges[1]]
        col += [edges[0]]

    #say(col)
    if self.getData("createFace"):
        ss=Part.sortEdges(col)
        sh=Part.makeFilledFace(ss[0])
    else:
        sh=Part.Compound(col)

    self.setPinObject("Shape_out",sh)
    #say("col",col)
    #say("gaps",gaps)
    self.setPinObject("gaps",Part.Compound(gaps))




def aa():    
    #-------------------- kann weg/reuse otherwhere
    if 1:
        pass
    else:
        
        ss=Part.sortEdges(col)
        poles=[]
        polesseg=[]
        for w in ss[0]:
            wn=w.toNurbs()
            pls=wn.Edge1.Curve.getPoles()
            if len(polesseg)>0:
                if (pls[0]- polesseg[-1][-1]).Length<0.001:
                    pass
                else:
                    pls.reverse()
            polesseg += [pls]
            poles += pls
        
        degA=self.getData("degree")   
        ls=int(len(polesseg)/2)
        poles=[]
        k=self.getData("tangentForce")
        
        pfak=degA
        pfak=0 # fuer weiche uebergaenge
        
        for i in range(ls):
            ll= (polesseg[2*i][0]-polesseg[2*i][1]).Length
            k *= 0.1*ll
            poles += [ polesseg[2*i][0]]*pfak
            try:
                poles += [
                    polesseg[2*i][0] + (polesseg[2*i][0]- polesseg[2*i-1][-2]).normalize()*k,
                    polesseg[2*i][1] + (polesseg[2*i][1] -polesseg[2*i+1][1]).normalize()*k,
                    ]
            except:
                say("no tangantes possible")
                poles += [
                    polesseg[2*i][0] + (polesseg[2*i][0]- polesseg[2*i-1][-2]),
                    polesseg[2*i][1] + (polesseg[2*i][1] -polesseg[2*i+1][1]),
                    ]

                pass
            poles += [polesseg[2*i][1]]*pfak
            
            poles +=polesseg[2*i+1]
        
        sh=Part.makePolygon(poles)
        sf=Part.BSplineCurve()

        poles=np.array(poles)
        (countA,_)=poles.shape

        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        knotA=range(len(multA))

        sf=Part.BSplineCurve()
        n=self.getData("rotateAxis")
        poles2=np.concatenate([poles[n:],poles[:n]]);poles=poles2
        
        sf.buildFromPolesMultsKnots(poles,multA,knotA,False,degA)

        sh=sf.toShape()

        if 0 and self.getData("createFace"):
            t=len(multA)//3-1
            sf1=sf.copy()
            sf2=sf.copy()
            sf3=sf.copy()
            sf2.segment(0,t)
            sf3.segment(t,2*t)
            sf1.segment(2*t,len(multA)-1)

            sh=Part.Compound([sf2.toShape(),sf3.toShape(),sf1.toShape()])
            Part.show(sh)
            tt=FreeCAD.ActiveDocument.ActiveObject
            surf=FreeCAD.ActiveDocument.addObject("Surface::GeomFillSurface","Surface")
            surf.BoundaryList=[(tt, ('Edge1', 'Edge2', 'Edge3'))]

            FreeCAD.ActiveDocument.recompute(None,True,True)


        if  self.getData("createFace"):
            t=len(multA)//2
            sf1=sf.copy()
            sf2=sf.copy()
            sf2.segment(0,t)          
            sf1.segment(t,len(multA)-1)
            sh=Part.Compound([sf2.toShape(),sf1.toShape()])
            e2=sf1.toShape().Edge1
            e2.reverse()
            sh=Part.makeRuledSurface(sf2.toShape().Edge1,e2)
      

         
            
    self.setPinObject("Shape_out",sh)


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


def run_FreeCAD_RandomizePolygon(self,*args, **kwargs):
#    return
#def u():
    sayl()
    edge=self.getPinObject("Shape_in")
    say(edge)
    if edge is None: return
    pts=[v.Point for v in edge.Vertexes]
    say(len(pts))
    ke=self.getData("factorEnds")
    ki=self.getData("factorInner")
    say(ki)
    a=pts[0]
    b=pts[-1]
    ptsa=[a+(b-a).normalize()*ke ]+[p+FreeCAD.Vector(random.random(),random.random(),random.random())*ki for p in pts[1:-1]]+[b+(a-b).normalize()*ke]

    self.setPinObject("Shape_out",Part.makePolygon(ptsa))
    self.setData("points_out",ptsa)

    sayl("fewrtig-- ")
    return







def myExecute_PyFlowRef(proy,fp):
    gm=FreeCAD.PF.graphManager.get()
    node=gm.findNode(fp.refname)
    if node != None:
        say("node to execute found",node)
        node.compute()


def reload_obj(self,*args, **kwargs):
    say("reload ",self)
    obn=self.objname.getData()
    obj=FreeCAD.ActiveDocument.getObject(obn)
    say(obn)
    say(obj)
    props=obj.PropertiesList
    for p in props:
        v=getattr(obj,p)
        say(p,v)
    self.createPins(self,*args, **kwargs)




def run_shelfToy(self):
    '''the implementation of the toy shelf tool'''
    
    nodes=FreeCAD.PF.graphManager.get().getAllNodes()
    nodes2 = sorted(nodes, key=lambda node: node.x)
    say("selected Nodes ...")
    for n in nodes2:
     if n.getWrapper().isSelected():
        say(n,n.x)

    mw=FreeCADGui.getMainWindow()
    say(mw)
    mw.hide()
    mw.show()
    say("!no action")



def run_PF_APP_WindowMinimized(app,event):
    '''triggered from PyFlow.App'''

    FreeCAD.savePFData = pfwrap.getInstance().graphManager.get().serialize()

    

def run_PF_APP_WindowNOMinimized(app,event):
    '''triggered from PyFlow.App'''


    pf=pfwrap.getInstance()
    for node in pfwrap.getInstance().graphManager.get().getAllNodes():
        node.kill()
    pfwrap.deleteInstance()
    del(FreeCAD.PF)
    try:
       pf.hide()
    except:
        pass

    pf=pfwrap.getInstance()
    pf.show()
    instance=pfwrap.getInstance()
    pf.graphManager.get().clear()
    pf.loadFromData(FreeCAD.savePFData)
    
    say("DONE")




def run_FreeCAD_Toy(self):
    self.setNodename("HU"+str(time.time()))
    self.setImage("freecad_cone")

    pml=[1,2,3,4,5,6,7,8,10,11,12,12,14,15,16,]
    tt=FreeCAD.Placement(FreeCAD.Matrix(*pml))
    pm2=self.getPinPlacement("PlacementPin_in")
    say("got",pm2)

    self.setPinPlacement("PlacementPin_out",tt.multiply(pm2))
    

def run_FreeCAD_Toy(self):
    rots=self.getPinRotations("RotationPin_in")
    say(rots)

    pms=self.getPinPlacements("PlacementPin_in")
    say(pms)

def run_FreeCAD_Toy(self):
    sh=self.getPinObject("ShapePin_in")
    self.setData("VectorPin_out",[sh.CenterOfMass])

def run_FreeCAD_Toy(self):
    sayl()


   






    




def interpolate(x,y,z, gridsize,mode='thin_plate',rbfmode=True,shape=None):

    mode=str(mode)
    grids=gridsize


    dx=np.max(x)-np.min(x)
    dy=np.max(y)-np.min(y)

    if dx>dy:
        gridx=grids
        gridy=int(round(dy/dx*grids))
    else:
        gridy=grids
        gridx=int(round(dx/dy*grids))

    if shape != None:
        (gridy,gridx)=shape

    xi, yi = np.linspace(np.min(x), np.max(x), gridx), np.linspace(np.min(y), np.max(y), gridy)
    xi, yi = np.meshgrid(xi, yi)


    if rbfmode:
        rbf = scipy.interpolate.Rbf(x, y, z, function=mode)
        rbf2 = scipy.interpolate.Rbf( y,x, z, function=mode)
    else:
        sayErr("interp2d nicht implementiert")
        x=np.array(x)
        y=np.array(y)
        z=np.array(z)
        xi, yi = np.linspace(np.min(x), np.max(x), gridx), np.linspace(np.min(y), np.max(y), gridy)

        rbf = scipy.interpolate.interp2d(x, y, z, kind=mode)
        rbf2 = scipy.interpolate.interp2d(y, x, z, kind=mode)

    zi=rbf2(yi,xi)
    return [rbf,xi,yi,zi]

def showFace(rbf,rbf2,x,y,gridsize,shapeColor,bound):

    grids=gridsize

    ws=[]

    pts2=[]
    xi, yi = np.linspace(np.min(x), np.max(x), grids), np.linspace(np.min(y), np.max(y), grids)

    for ix in xi:
        points=[]
        for iy in yi:
            iz=float(rbf(ix,iy))

#---------------------- special hacks #+#
            if bound>0:
                if iz > bound: iz = bound
                if iz < -bound: iz = -bound


            points.append(FreeCAD.Vector(ix,iy,iz))

        pts2.append(points)

    return pts2


    
def createElevationGrid(pts,mode='thin_plate',rbfmode=True,source=None,gridCount=20,zfactor=1,bound=10**5,matplot=False):
    
    modeColor={
    'linear' : ( 1.0, 0.3, 0.0),
    'thin_plate' : (0.0, 1.0, 0.0),
    'cubic' : (0.0, 1.0, 1.0),
    'inverse' : (1.0, 1.0, 0.0),
    'multiquadric' : (1.0, .0, 1.0),
    'gaussian' : (1.0, 1.0, 1.0),
    'quintic' :(0.5,1.0, 0.0)
    }


    k=0.0001
    k=0
    pts2=[p+FreeCAD.Vector(random.random(),random.random(),random.random())*k for p in pts]
    pts=pts2

    #say("points",pts)
    x=np.array(pts)[:,0]
    y=np.array(pts)[:,1]
    z=np.array(pts)[:,2]
    say(x)
    say(y)
    say(z)
    say("----------")
    
    #x=np.array(x)
    #y=np.array(y)
    #z=np.array(z)

    gridsize=gridCount

    rbf,xi,yi,zi1 = interpolate(x,y,z, gridsize,mode,rbfmode)
    
    # hilfsebene
    xe=[10,-10,10,-10]
    ye=[10,-9,10,-10]
    ze=[0,0,0,0]


    #rbf2,xi2,yi2,zi2 = interpolate(xe,ye,ze, gridsize,mode,rbfmode,zi1.shape)
    rbf2=0
    #zi=zi1-zi2
    zi=zi1

    try: color=modeColor[mode]
    except: color=(1.0,0.0,0.0)

    xmin=np.min(x)
    ymin=np.min(y)

    points=showFace(rbf,rbf2,x,y,gridsize,color,bound)
    say("XXXX points",points)

 
    return points
    #App.ActiveDocument.ActiveObject.Label=mode + " ZFaktor " + str(zfactor) + " #"
    #rc=App.ActiveDocument.ActiveObject


    #if matplot: showHeightMap(x,y,z,zi)
    #return rc

    # interpolation for image
    #gridsize=400
    #rbf,xi,yi,zi = interpolate(x,y,z, gridsize,mode,rbfmode)
    #rbf2,xi2,yi2,zi2 = interpolate(xe,ye,ze, gridsize,mode,rbfmode,zi.shape)
    #return [rbf,rbf2,x,y,z,zi,zi2]
    

def run_FreeCAD_Elevation(self):
    points=self.getData('points')
    say(points)
    sayl("##")
    nb=createElevationGrid(points)
    self.setData("poles",nb)

 

    
def createElevationGrid(pts,mode='thin_plate',rbfmode=True,gridCount=20,bound=0,noise=0.0001):
    
    modeColor={
    'linear' : ( 1.0, 0.3, 0.0),
    'thin_plate' : (0.0, 1.0, 0.0),
    'cubic' : (0.0, 1.0, 1.0),
    'inverse' : (1.0, 1.0, 0.0),
    'multiquadric' : (1.0, .0, 1.0),
    'gaussian' : (1.0, 1.0, 1.0),
    'quintic' :(0.5,1.0, 0.0)
    }

    # add some noise to avoid singualr matrixes
    if noise==0:
        noisefactor=0
    else:
        noisefactor=10**(-4+noise)
    
    if len(pts)==0:
        sayErr("no points for elevation grid")
        return []
    
    pts2=[p+FreeCAD.Vector(random.random(),random.random(),random.random())*noisefactor for p in pts]

    x=np.array(pts2)[:,0]
    y=np.array(pts2)[:,1]
    z=np.array(pts2)[:,2]

    if rbfmode:
        rbf = scipy.interpolate.Rbf(x, y, z, function=mode)
    else:
        rbf = scipy.interpolate.interp2d(x, y, z, kind=mode)

    # calculate output point grid
    xia, yia = np.linspace(np.min(x), np.max(x), gridCount), np.linspace(np.min(y), np.max(y), gridCount)

    pts3=[]
    for ix in xia:
        points=[]
        for iy in yia:
            iz=float(rbf(ix,iy))
            if bound>0:
                if iz > bound: iz = bound
                if iz < -bound: iz = -bound
            points.append(FreeCAD.Vector(ix,iy,iz))

        pts3.append(points)

    return pts3
    

def run_FreeCAD_Elevation(self):

    # get the data from the pyflow node
    points=self.getData('points')
    gridCount=self.getData('gridCount')
    
    bound=self.getData('bound')
    noise=self.getData('noise')
    rbfmode=self.getData('Rbf')
    mode=self.getData('mode')

    #say(points)
    #sayl("Abburch")
    #return
    # run the calculation
    poles=createElevationGrid(points,mode=mode,rbfmode=rbfmode,gridCount=gridCount,bound=bound,noise=noise)

        
    # store the ruesult to the outputpin and start postprocessing
    self.setData("poles",poles)


    
