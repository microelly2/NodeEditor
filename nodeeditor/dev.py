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



def run_FreeCAD_VectorArray(self,*args, **kwargs):

    countA=self.getData("countA")
    countB=self.getData("countB")
    countC=self.getData("countC")
    vO=self.getData("vecBase")
    vA=self.getData("vecA")

    vB=self.getData("vecB")
    vC=self.getData("vecC")
    rx=self.getData("randomX")
    ry=self.getData("randomY")
    rz=self.getData("randomZ")


    degA=self.getData("degreeA")
    degB=self.getData("degreeB")
    if countA<degA+1:
        degA=countA-1
    if countB<degB+1:
        degB=countB-1

    points=[vO+vA*a+vB*b+vC*c+FreeCAD.Vector((0.5-random.random())*rx,(0.5-random.random())*ry,(0.5-random.random())*rz)
        for a in range(countA) for b in range(countB) for c in range(countC)]

    if countC != 1:
        sayexc("not implemented")
        return

    if degA==0 or degB==0:
        col = []
        poles=np.array(points).reshape(countA,countB,3)
        for ps in poles:
            ps=[FreeCAD.Vector(p) for p in ps]
            col += [Part.makePolygon(ps)]
        for ps in poles.swapaxes(0,1):
            ps=[FreeCAD.Vector(p) for p in ps]
            col += [Part.makePolygon(ps)]

        shape=Part.makeCompound(col)


    else:

        poles=np.array(points).reshape(countA,countB,3)

        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sf=Part.BSplineSurface()
        sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,False,degA,degB)
        shape=sf.toShape()


    self.setData('vectors_out',poles.tolist())

    #cc=self.getObject()
    #try:
    #    cc.Label=self.objname.getData()
    #except:
    #    pass
    #cc.Shape=shape
    self.setPinObject('Shape_out',shape)
    #Beispiel Nodename setzen
    #self.setNodename("HUHU")
    
    # Fehler setzen
    #self.setError("raise Exception")
    








def run_FreeCAD_Plot(self,*args, **kwargs):

    
    sayl()
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


    if len(y)  != 0:
        N=len(y)
        if len(x) != len(y):
            x = np.linspace(0, 10, N, endpoint=True)
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
    fig.canvas.flush_events()



def run_projection_compute(self,*args, **kwargs):

    sayl()
#   f=FreeCAD.ActiveDocument.BePlane.Shape.Face1
#   w=FreeCAD.ActiveDocument.Sketch.Shape.Edge1

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

def run_perspective_projection_compute(self,*args, **kwargs):

    sayl()
#   f=FreeCAD.ActiveDocument.BePlane.Shape.Face1
#   w=FreeCAD.ActiveDocument.Sketch.Shape.Edge1

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


def run_uv_projection_compute(self,*args, **kwargs):

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


def run_Bar_compute(self,*args, **kwargs):
    sayl()


def run_Foo_compute(self,*args, **kwargs):
    sayl()



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



def run_FreeCAD_UVGrid(self,*args, **kwargs):

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



def run_FreeCAD_Voronoi(self,*args, **kwargs):
    '''
    create voronoi and delaunay stuff using scipy, see
    https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.spatial.Voronoi.html
    '''

    from scipy.spatial import Voronoi, voronoi_plot_2d

    # get data from inpins or generate somthinfg for testing
    face=self.getPinObject("Face")
    ulist=self.getData("uList")
    vlist=self.getData("vList")

    if len(ulist) == len(vlist) and len(ulist)>0:
        say("use old")
        pointsa=zip(ulist,vlist)
    else:
        say("ewigene datan")
        n=30
        try: 
            pointsa=self.pointsa
            #1/0
        except:
            pointsa=np.random.random(2*n).reshape(n,2)*0.8 + [0.1,0.1]
            self.pointsa=pointsa

    # add the bounding box in normalized uvspace
    points = np.concatenate([pointsa,np.array([[0,0],[0,1],[1,0],[1,1]])])

    # core calculation
    vor = Voronoi(points)
    points=[FreeCAD.Vector(v[0],v[1]) for v in points]

    if 0:
        say("ridge points--")
        say(len(vor.ridge_points))
        say(vor.ridge_points)


    #
    # delaunay
    #
    edges=[]
    col=[]
    for r in  vor.ridge_points:
        pts=[points[v] for v in r if v  !=  -1]
        if len(pts)>1:
            for i in range(len(pts)-1):
                pa=pts[i]
                pb=pts[i+1]
                xa,ya=pa[0],pa[1]
                xb,yb=pb[0],pb[1]
                edges += [(xa,ya,xb,yb)]

    if self.getData("useLines"):
        shape=mapEdgesLines(edges,face)
    else:
        shape=mapEdgesCurves(edges,face)

    spoints=[v.Point for v in shape.Vertexes]
    self.setPinObject("delaunayTriangles",shape)

    #
    # voronoi 
    #
    vertexes=[FreeCAD.Vector(v[0],v[1]) for v in vor.vertices]

    if 0:
        say("regions")
        say(vor.regions)

        say("point region")
        say(vor.point_region)

        say("ridge_vertexes")
        say(vor.ridge_vertices)

    col=[]
    col2=[]
    uvedges=[]
    #for r in  vor.regions:
    say("ridge_vertices ..")
    pos=self.getData('indA')
    #
    # this code is buggy !!!
    #
    #for ix, r in  enumerate(vor.ridge_vertices):
    for ix, r in  enumerate(vor.regions):
        pts=[vertexes[v] for v in r if v  !=  -1]
        #say(ix,len(r),len(pts))
        #if ix  != pos:
        #   continue
        uvedgesA=[]
        if len(pts)>1:
            col += [Part.makePolygon(pts)]
            for i in range(len(pts)-1):
                pa=pts[i]
                pb=pts[i+1]
                xa,ya=pa[0],pa[1]
                xb,yb=pb[0],pb[1]
                
                if not check (xa,ya,xb,yb):
                    (xa,ya,xb,yb)=trim(xa,ya,xb,yb)
                if check (xa,ya,xb,yb):
                    pa=FreeCAD.Vector(xa,ya)
                    pb=FreeCAD.Vector(xb,yb)
                    #say()
                    uvedges += [(xa,ya,xb,yb)]
                    uvedgesA += [(xa,ya,xb,yb)]
                    #col2 += [Part.makePolygon([pa,pb])]
                if not check (xa,ya,xb,yb):
                    (xa,ya,xb,yb)=trim(xa,ya,xb,yb)
                    if check (xa,ya,xb,yb):
                        pa=FreeCAD.Vector(xa,ya)
                        pb=FreeCAD.Vector(xb,yb)
                        #say()
                        #uvedges += [(xa,ya,xb,yb)]
                        uvedgesA += [(xa,ya,xb,yb)]
                        #col2 += [Part.makePolygon([pa,pb])]
                    else:
                        say("Err",xa,ya,xb,yb)
        try:
            uuu=uvedgesA+[(uvedgesA[-1][2],uvedgesA[-1][3],uvedgesA[0][0],uvedgesA[0][1])]
            #say(uuu[0])
            #say(uuu[-1])
            #say("--")
        except:
            pass

    # create the output shape
    if self.getData("useLines"):
        shape=mapEdgesLines(uvedges,face)
    else:
        shape=mapEdgesCurves(uvedges,face)
    self.setPinObject("voronoiCells",shape)


#-------------------volle zellen

    #
    # regions filled 
    #
    #say("vor.regions",vor.regions)

    for ix, r in  enumerate(vor.regions):
        pts=[vertexes[v] for v in r if v  !=  -1]
        if ix==self.getData('indA'):
            #say(ix,r)
            if len(pts)<=2:
                say("zuwenig punkte")
            else:
                shapes=mapPoints(pts,face)
                if len(shapes)>0:
                    cc=FreeCAD.ActiveDocument.getObject("regionFilled")
                    if cc == None:
                        cc=FreeCAD.ActiveDocument.addObject("Part::Feature","regionFilled")
                    cc.Shape=shapes[0]
                    if self.getData('flipArea'):
                        #say(shapes)
                        cc.Shape=shapes[1]
            break


    from scipy.spatial import Delaunay

    tri = Delaunay(pointsa)
    #say(tri.simplices)
    points=[FreeCAD.Vector(p[0],p[1]) for p in points]

    #
    # simplexes
    #
    if 0:
        coll=[]
        if 0: # 3D Variante
            for s in tri.simplices:
                [a,b,c,d]=s
                a=points[a]
                b=poi[b]
                c=points[c]
                d=points[d]
                coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([a,d]),Part.makePolygon([b,c]),Part.makePolygon([b,d]),Part.makePolygon([c,d])]
        else: #2 D
            for s in tri.simplices:
                [a,b,c]=s
                a=points[a]
                b=points[b]
                c=points[c]
                coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([b,c])]

    #
    # convex hull
    #
#   coll=[]
    edges=[]
    for s in tri.convex_hull:
        [a,b]=s
        a=points[a]
        b=points[b]
#       coll += [Part.makePolygon([a,b])]
        xa,ya=a[0],a[1]
        xb,yb=b[0],b[1]
        edges += [(xa,ya,xb,yb)]

    if self.getData("useLines"):
        shape=mapEdgesLines(edges,face)
    else:
        shape=mapEdgesCurves(edges,face)
    self.setPinObject("convexHull",shape)

    #
    # punkte veranschaulichen
    #
    col=[]
    for p in spoints:
        col += [Part.makeSphere(50,p)]

    shape=Part.Compound(col)
    self.setPinObject("Points",shape)







def run_FreeCAD_Hull(self,*args, **kwargs):
    '''
    calculate voronoi delaunay  stuff for 3D point cloud
    '''

    from scipy.spatial import Delaunay

    # get the point cloud
    shape=self.getPinObject("Shape")
    if shape is None: return
    points=[v.Point for v in shape.Vertexes]

    # threshold parameter for alpha hull
    lmax=0.03*(self.getData('alpha')+0.1)

    #core calculation
    atime=time.time()
    tri = Delaunay(points)
    say("time to calculate delaunay:{}".format(time.time()-atime)) 

    # say(tri.simplices)

    #
    # simplexes and alpha hull
    #
    atime=time.time()
    coll=[]
    colf=[]

    for s in tri.simplices:
        aatime=time.time()
        [a,b,c,d]=s
        a=points[a]
        b=points[b]
        c=points[c]
        d=points[d]
        coll += [Part.makePolygon([a,b]),Part.makePolygon([a,c]),Part.makePolygon([a,d]),Part.makePolygon([b,c]),Part.makePolygon([b,d]),Part.makePolygon([c,d])]

        bbtime=time.time()
        tta=Part.makePolygon([a,b,c,a]).Edges
        ttb=Part.makePolygon([a,b,d,a]).Edges
        ttc=Part.makePolygon([a,c,d,a]).Edges
        ttd=Part.makePolygon([b,c,d,b]).Edges

        # create a alpha simplex if it is small enough 
        if max ([e.Length for e in tta+ttb+ttc+ttd])<lmax:
            bbtime=time.time()
            if 10:
                wire=Part.makePolygon([a,b,c,a])
                colf += [Part.Face(wire)]
                wire=Part.makePolygon([a,b,d,a])
                colf += [Part.Face(wire)]
                wire=Part.makePolygon([a,d,c,a])
                colf += [Part.Face(wire)]
                wire=Part.makePolygon([d,b,c,d])
                colf += [Part.Face(wire)]

            else:
                w=Part.BSplineSurface()
                w.buildFromPolesMultsKnots(np.array([[a,b],[a,c]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
                colf += [w.toShape()]
                w.buildFromPolesMultsKnots(np.array([[a,b],[a,d]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
                colf += [w.toShape()]
                w.buildFromPolesMultsKnots(np.array([[b,c],[b,d]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
                colf += [w.toShape()]
                w.buildFromPolesMultsKnots(np.array([[a,d],[a,c]]),[2,2],[2,2],[0,1],[0,1],False,False,1,1)
                colf += [w.toShape()]
            say("! time alpha:makefaces {}  simplex edges{}".format(time.time()-bbtime,bbtime-aatime)) 
    say("time to calculate alpha:{}".format(time.time()-atime)) 


    # restrict set if simplexes is flag simpleSimplex is set
    atime=time.time()
    if self.getData('singleSimplex'):
        index=self.getData('simplex')
        coll=coll[6*index:6*index+6]

    shape=Part.Compound(coll)
    self.setPinObject("delaunayTriangles",shape)

    try:
        shape=Part.Compound(colf)
    except:
        shape=Part.Shape()
    if len(colf)==0:
        shape=Part.makeSphere(0.0)

    self.setPinObject("alphaHull",shape)
    say("number of bordercells",len(colf)/3)

    #
    # convex hull
    #
    coll=[]
    for s in tri.convex_hull:
        [a,b,c]=s
        a=points[a]
        b=points[b]
        c=points[c]
        coll += [Part.makePolygon([a,b]),Part.makePolygon([b,c]),Part.makePolygon([c,a])]

    self.setPinObject("convexHull",Part.Compound(coll))

    # post process following nodes
    atime=time.time()

    say("time for call view3dNodes:{}".format(time.time()-atime)) 



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


def run_FreeCAD_2DGeometry(self,*args, **kwargs):
    
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


def run_FreeCAD_2DCircle(self,*args, **kwargs):

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




def run_FreeCAD_2DEllipse(self,*args, **kwargs):

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




def run_FreeCAD_2DArcOfEllipse(self,*args, **kwargs):

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



def run_FreeCAD_2DArcOfCircle(self,*args, **kwargs):

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



def run_FreeCAD_2DArcOfParabola(self,*args, **kwargs):

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

#--------------------------

import sys
if sys.version_info[0] !=2:
    from importlib import reload


def run_FreeCAD_Simplex(self,*args, **kwargs):

    k=self.getData("noise")
    say("kkk",k)

    def rav(v):
        '''add a random vector to a vector'''
        return v+FreeCAD.Vector(0.5-random.random(),0.5-random.random(),0.5-random.random())*k


    sayl()
    a=self.getData("pointA")
    b=self.getData("pointB")
    c=self.getData("pointC")
    d=self.getData("pointD")
    say(a,b,c,d)
    colf=[]
    wire=Part.makePolygon([a,rav(b),rav(c),a])
    colf += [Part.Face(wire)]
    
    wire=Part.makePolygon([a,rav(b),rav(d),a])
    colf += [Part.Face(wire)]

    wire=Part.makePolygon([a,rav(c),rav(d),a])
    colf += [Part.Face(wire)]

    wire=Part.makePolygon([c,rav(b),rav(d),c])
    colf += [Part.Face(wire)]

    #Part.show(Part.Compound(colf))
    self.setPinObject("Compound_out",Part.Compound(colf))

    for tol in range(100):
        colf2=[c.copy() for c in colf]
        try:
            # say ("try tolerance",tol)
            for f in colf2:
                f.Tolerance=tol
            sh=Part.Shell(colf2)
            sol=Part.Solid(sh)
            say (sol.isValid())
            if sol.isValid():
                say("solid created with tol",tol)
                #Part.show(sol)
                #cc=self.getObject();cc.Shape=sol
                
                self.setPinObject("Shape_out",sol)
                break
        except:
            pass





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



def run_FreeCAD_Discretize(self,*args, **kwargs):
    sayl()
    count=self.getData("count")
    edge=self.getPinObject("Wire")
    say(edge)
    if edge is None: return
    ptsa=edge.discretize(count)

    self.setPinObject("Shape_out",Part.makePolygon(ptsa))
    if 0:
        sc=Part.BSplineCurve()
        sc.buildFromPoles(ptsa)
        self.setPinObject("Shape_out",sc.toShape())
    

    return

    pts=edge.discretize(count*10)
    #Part.show(Part.makePolygon(pts))
    face=FreeCAD.ActiveDocument.BePlane.Shape.Face1
    sf=face.Surface
    r=200
    pts2=[]
    pts3=[]
    for i in range(len(pts)-1):
        p=pts[i]
        u,v=sf.parameter(p)
        say(u,v)
        t=(pts[i+1]-p).normalize()
        say(t)
        n=sf.normal(u,v)
        say(n)
        u,v=sf.parameter(p+n.cross(t)*r)
        pts2 += [sf.value(u,v)]
        u,v=sf.parameter(p-n.cross(t)*r)
        pts3 += [sf.value(u,v)]
    closed=True
    if 0:
        if closed:
            Part.show(Part.makePolygon(pts2+[pts2[0]]))
            Part.show(Part.makePolygon(pts3+[pts3[0]]))
        else:
            Part.show(Part.makePolygon(pts2))
            Part.show(Part.makePolygon(pts3))




def run_FreeCAD_Offset(self,produce=False, **kwargs):
    #sayl()
    count=self.getData("count")
    edge=self.getPinObject("Wire")
    say(edge)
    if edge is None: return
    pts=edge.discretize(count*10)
    # Part.show(Part.makePolygon(pts))
    face=self.getPinObject("Shape")
    sf=face.Surface
    r=self.getData("offset")*20
    pts2=[]
    pts3=[]
    pts4=[]
    pts5=[]
    #r2=self.getData("height")*20
    r2=100
    
    for i in range(len(pts)-1):
        p=pts[i]
        u,v=sf.parameter(p)
        say(u,v)
        t=(pts[i+1]-p).normalize()
        say(t)
        n=sf.normal(u,v)
        say(n)
        u,v=sf.parameter(p+n.cross(t)*r)
        pts2 += [sf.value(u,v)]
        u,v=sf.parameter(p-n.cross(t)*r)
        pts3 += [sf.value(u,v)]
        pts4 += [p+n*r2]
        pts5 += [p-n*r2]
    closed=True
    closed=False
    if closed:
        pol2=Part.makePolygon(pts2+[pts2[0]])
        pol3=Part.makePolygon(pts3+[pts3[0]])
        pol4=Part.makePolygon(pts4+[pts4[0]])
    else:
        pol2=Part.makePolygon(pts2)
        pol3=Part.makePolygon(pts3)
        pol4=Part.makePolygon(pts4)
    if produce:
            Part.show(pol2)
            Part.show(pol3)
            Part.show(pol4)

    sfa=Part.BSplineSurface()
    
    poles=np.array([pts2,pts4,pts3])

    countB=len(pts2)
    countA=3
    degA=2
    degB=3
    if closed==False:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multA=[degA]+[1]*(countA-degA)+[degA]
        
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,True,False,degA,degB)
    else:
        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        multB=[degB]+[1]*(countB-degB)+[degB]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,False,True,degA,degB)

    if 10:
        poles=np.array([pts2,pts4,pts3,pts5])
        countA=4

        poles=np.array([pts2,pts2,pts4,pts3,pts3])
        countA=5
        
        multA=[degA]+[1]*(countA-degA)+[degA]
        multB=[degB]+[1]*(countB-degB)+[degB]
        multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
        knotA=range(len(multA))
        knotB=range(len(multB))

        sfa=Part.BSplineSurface()
        sfa.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,True,False,degA,degB)


    Part.show(sfa.toShape())



    self.setPinObject("Shape_out",Part.Compound([pol2,pol3,pol4]))





def run_FreeCAD_FillEdge(self,produce=False, **kwargs):
   
    return #+# muss mparametriz werden
    wire=FreeCAD.ActiveDocument.BePlane.Shape.Wires[0]
    #_=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Shape004.Shape.Edge2, ]))
    _=Part.makeFilledFace(wire.Edges)
    Part.show(_)
    

def run_FreeCAD_Solid(self,bake=False, **kwargs):
    
    #shapes=self.getData("Shapes")
    #say(shapes)
    #return
    
    yPins = self.getPinByName("Shapes").affected_by
    
    outArray=[]
    for pin in yPins:
        k=str(pin.uid)
        d=store.store().get(k)
#       say(d)
        outArray.append(d)
    say(outArray)
    
    shapes=outArray
    say(shapes)

    colf=shapes

    

    for tol in range(1000):
        colf2=[c.copy() for c in colf]
        try:
            #say ("try tolerance",tol)
            for f in colf2:
                f.Tolerance=tol
            sh=Part.Shell(colf2)

            sol=Part.Solid(sh)
            say (sol.isValid())
            if sol.isValid():
                say("solid created with tol",tol)
                if bake:
                    Part.show(sol)
                #cc=self.getObject();cc.Shape=sol
                
                self.setPinObject("Shape_out",sol)
                break
        except:
            pass




# autumn 19
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



def run_FreeCAD_BSplineSurface(self, *args, **kwargs):

        
        data=self.getPinDataYsorted('poles')
        for d in data:
            say("!",np.array(d).shape)
        dat=np.concatenate(data)
        say(np.array(dat).shape)       
        
        if len(dat) == 0:
            sayW("no points for poles")
            return
        dat=np.array(dat)
        sf=Part.BSplineSurface()

        poles=np.array(dat)

        (countA,countB,_)=poles.shape
        degB=min(countB-1,3,self.getPinByName("maxDegreeU").getData())
        degA=min(countA-1,3,self.getPinByName("maxDegreeV").getData())
        
        periodicU=self.getData("periodicU")
        
        periodicV=self.getData("periodicV")
        if periodicU:
            multA=[1]*(countA+1)
            knotA=range(len(multA))
        else:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))

        if periodicV:
            multB=[1]*(countB+1)
            knotB=range(len(multB))
        else:
            multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]       
            knotB=range(len(multB))


        sf=Part.BSplineSurface()
        sf.buildFromPolesMultsKnots(poles,multA,multB,knotA,knotB,periodicU,periodicV,degA,degB)
        shape=sf.toShape()

        self.setPinObject("Shape_out",shape)
    



def run_FreeCAD_BSplineCurve(self, *args, **kwargs):

        dat=self.arrayData.getData()
        if len(dat)==0:             return
        dat=np.array(dat)
        sf=Part.BSplineCurve()

        poles=np.array(dat)

        (countA,_)=poles.shape
        degA=min(countA-1,13,self.getPinByName("maxDegree").getData())

        periodic=self.getData("periodic")
        #periodic=True
        if not periodic:
            multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
            knotA=range(len(multA))

        else:
            multA=[1]*(countA+1)
            knotA=range(len(multA))

            
        sf=Part.BSplineCurve()
        sf.buildFromPolesMultsKnots(poles,multA,knotA,periodic,degA)
        shape=sf.toShape()


        shape=sf.toShape()
        
        #cc=self.getObject()
        #cc.Label=self.objname.getData()
        #cc.Shape=shape

        self.setPinObject("Shape_out",shape)
    
    


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
    

def run_FreeCAD_Collect_Vectors(self, mode=None):
    #say("collect",mode)
    if mode=="reset":
        self.points=[]
        return


    maxSize=self.getData("maxSize")
    red=self.getData("reduce")
    point = self.getData("point")
    try:
        if (self.points[-1]-point).Length <0.01:
#           say("zu dicht")
            return
    except:
        pass

    # point.y *= -1.

    self.points += [point]
    #say(len(self.points))
    if maxSize >0 and len(self.points)>maxSize:
            self.points = self.points[len(self.points)-maxSize:]
    if len(self.points)>2 and red>2:
        pol=Part.makePolygon(self.points)
        pointsd=pol.discretize(red)
    else:
        pointsd=self.points
    self.setData("points",pointsd)
    #say(len(self.points),len(pointsd))
    if not self.inRefresh.hasConnections():
        self.outExec.call()
    



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




def run_FreeCAD_swept(self):
    ta=time.time()
    l=self.getData("steps")
    step=self.getData("step")

    # the border of the car
    trackpoints=self.getData("trackPoints")
#   say(trackpoints)
    path=self.getPinObject("Path")

    if path is None: return
    pts=path.discretize(l+1)
#   say(pts)
    centerAxis=self.getData("centerAxis")
#   return
    pols=[]
    pms=[]
    pts=FreeCAD.ActiveDocument.Sketch.Shape.Edge1.discretize(l+1)

    centers=[]
    a=pts[0]+centerAxis
    pols=[Part.makePolygon([a,pts[0]])]
    for i in range(l):
        b=pts[i]
        b2=pts[i+1]

        A=np.array([[b.x-a.x,b.y-a.y],[b.x-b2.x,b.y-b2.y]])
        B=np.array([(b-a).dot(a),(b-b2).dot((b+b2)*0.5)])
        x=np.linalg.solve(A,B)
        m=FreeCAD.Vector(x[0],x[1])
        centers += [m]
        r=FreeCAD.Rotation(b-m,b2-m)
        pm=FreeCAD.Placement(FreeCAD.Vector(),r,m)

        a2=pm.multVec(a)
        pols += [Part.makePolygon([a2,b2])]
        pms += [pm]

        a=a2

    # the axes flow of the car movement
    flows = Part.Compound(pols)
    self.setPinObject("flowAxes_out",flows)

    # calculate the list of transformations
    pm=FreeCAD.Placement()
    pms2=[pm]
    for p in pms:
        pm=p.multiply(pm)
        pms2 += [pm]

    # the tracks of the trackpoints
    tcols=[]
    for c0 in trackpoints:
        ptcs=[p.multVec(c0) for p in pms2]
        tcols+= [Part.makePolygon(ptcs)]
    shapea=Part.Compound(tcols)
    
    #shapea=Part.makePolygon(centers)
    
    self.setPinObject("tracks_out",shapea)

    # display the starting car
    car=trackpoints+[trackpoints[0]]
    # Part.show(Part.makePolygon(trackpoints+[trackpoints[0]]))

    # display the final car
    carend=[pms2[step].multVec(c) for c in car]
    shape=Part.makePolygon(carend)
    #say(shape)
    self.setPinObject("Car_out",shape)



    say(time.time()-ta)




def run_FreeCAD_handrail(self):

    anz=self.getData('steps')
    heightStep=self.getData('heightStair')/anz*4
    heightBorder=self.getData('heightBorder')
    path=self.getPinObject("Path")
    borderA=self.getPinObject("borderA")
    borderB=self.getPinObject("borderB")

    edge=path
    if edge is None: return
    curv=edge.Curve
    pts=edge.discretize(anz)
    allc=[]
    comps=[]
    borders= [ borderA, borderB, ] 

    for edge2 in borders:
        rail=[]
        up=FreeCAD.Vector(0,0,heightStep)
        g=FreeCAD.Vector(0,0,heightBorder)
        for i in range(anz):
            p=pts[i]
            tp=curv.parameter(p)
            n=curv.normal(tp)

            a=p+n*10
            b=p-n*10
            line=Part.makePolygon([a,b])
            cc=line.Edge1.Curve.intersectCC(edge2.Curve)

            if len(cc) != 0:
                pp=cc[0]
                c=FreeCAD.Vector(pp.X,pp.Y,pp.Z)
                line=Part.makePolygon([p+i*up,c+i*up])
                comps += [line]
                rail +=[c+i*up+g,c+i*up,c+i*up+g]
            else:
                pass
#               comps += [line]

        comps += [Part.makePolygon(rail)]

    shape=Part.Compound(comps)
    self.setPinObject("Shape_out",shape)



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



def run_FreeCAD_Bender(self):

    if FreeCAD.ActiveDocument.getObject("Shape") == None:
        createToy()
        #return

    a=self.getData('a')
    b=self.getData('b')
    c=self.getData('c')

    countA=11
    countB=11

    degA=3
    degB=3

    multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
    multB=[degB+1]+[1]*(countB-1-degB)+[degB+1]
    knotA=range(len(multA))
    knotB=range(len(multB))

    comps=[]

    poles=FreeCAD.ActiveDocument.Shape.Shape.Face1.Surface.getPoles()
    shapein=self.getPinObject("Shape_in")
    say(shapein)
    if shapein is None: return
    poles=shapein.Surface.getPoles()
    poles=np.array(poles)

    col=[]
    for ps in poles:
        ps=[FreeCAD.Vector(p) for p in ps]
        col += [Part.makePolygon(ps)]

    for ps in poles.swapaxes(0,1):
        ps=[FreeCAD.Vector(p) for p in ps]
        col += [Part.makePolygon(ps)]


    comps += [Part.Compound(col)]

    # trafo
    b=np.pi/360*b/100
    a *= 10
    c *= np.pi/360 *4

    from math import sin,cos

    #poles2=np.zeros(countA*countB*3).reshape(countA,countB,3)
    poles2=np.zeros([countA,countB,3])

    for u in range(countA):
        for v in range(countB):
            [x,y,z]=poles[u,v]
            poles2[u,v,0]=(a+x)*cos(b*y+c)
            poles2[u,v,1]=(a+x)*sin(b*y+c)
            poles2[u,v,2]=z


    col=[]
    for ps in poles2:
        ps=[FreeCAD.Vector(p) for p in ps]
        col += [Part.makePolygon(ps)]

    for ps in poles2.swapaxes(0,1):
        ps=[FreeCAD.Vector(p) for p in ps]
        col += [Part.makePolygon(ps)]


    # Part.show(Part.Compound(col))
    comps += [Part.Compound(col)]

    sf=Part.BSplineSurface()
    sf.buildFromPolesMultsKnots(poles2,multA,multB,knotA,knotB,False,False,degA,degB)
    shape=sf.toShape()
    #App.ActiveDocument.Shape003.Shape=shape

    comps  = [shape]

    shape=Part.Compound(comps)
    self.setPinObject("Shape_out",shape)



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




def run_FreeCAD_FlipSwapArray(self):
    say("flipswap")
    say(self.name)
    poles=np.array(self.getData('poles_in'))
    say("shape",poles.shape)
    if len(poles.shape)<2: return
    if self.getData('swap'):
        poles=poles.swapaxes(0,1)
    if self.getData('flipu'):
        poles=np.flipud(poles)
    if self.getData('flipv'):
        poles=np.flipud(poles)


    
    say("result",poles.shape)
    self.setData('poles_out',poles.tolist())



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





def run_FreeCAD_Blinker(self):

    from blinker import signal
    try:
        sn=self.getData('signalName')
        ss= self.name +"@PyFlow"
    except:
        sn=self.Object.signalName
        ss=self.name +")@FreeCAD"

    from threading import Thread


    def sleeper(i):
        
        anz=0
        for j in range(1000):
            send_data = signal(sn)
            say("###",i,j,self.getData("sleep"),time.time())
            #say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            #say( "%r signal feedbacks:" %self.name)
            #for r in result:
            #    say(r[1])

        
            time.sleep(1+0.02*random.random())
            if self.getData("sleep") ==0:
                say("ENDE",i)
                return
        say("NDE ALL",i)

    def sleeper2(i):
            sleeper2a(i)



    def sleeper2a(i):
        a=time.time()
        say("start  outExec.call",i)
        say('##example set color')
        say("Ende call ",i,time.time()-a)


    def looper(j):
        try:
            j=self.getData("loops")
        except:
            return
        say("################# vSTART Looper",j)
        for i in range(j):
            if self.stopped:
                say("stopped")
                return
            send_data = signal(sn)
            say("###",i,j,self.getData("sleep"),time.time())
            say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            say( "%r signal feedbacks:" %self.name)
            for r in result:
                say(r[1])

            if self.getData("sleep") ==0:
                say("ENDE blinker calls at iteration",i)
                return
            t = Thread(target=sleeper2, args=(i,))
            t.start()
            time.sleep(self.getData("sleep")*0.1) 


        say("###             END Looper",j)

    a=time.time()
    self.stopped=False
    t2 = Thread(target=looper, args=(10,))
    t2.start()
    say("startf")
    #t2._stop();  say("stoppedAA")
    FreeCAD.t2=t2

    say("-----------------------------------Ende main",time.time()-a)

    def hu():
        for i in range(3):
            send_data = signal(sn)
            say()
            say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            say( "%r signal feedbacks:" %self.name)
            for r in result:
                say(r[1])
            tsleep=self.getData('sleep')
            if tsleep == 0:
                say("no loop")
                return
            else:
                say("sleep...",0.2)
                time.sleep(tsleep)
                say(i,"wake on!!")

def run_FreeCAD_Receiver(self):

    try:
        say("Data:",self.kw)
        say("Sender:",self.sender)
    except:
        say("no sender data and name avaiable")
    #self.setData("signalName",self.sender)
    #self.setData("senderMessage",self.kw['message'])
    self.setColor(b=0,a=0.4)
    




def myExecute_Receiver(proxy,fp):
    proxy.name=fp.Name
    run_FreeCAD_Receiver(proxy)

def myExecute_Blinker(proxy,fp):
    proxy.name=fp.Name
    run_FreeCAD_Blinker(proxy)

def f(x):
        return x*x


def run_FreeCAD_Async(self):
    #say(self.name)
    #sayl()
    #anz=0
    maxanz=15
    obj=self

    self.setData("message",self.name+" start")

    self.setData("message","")

    from threading import Thread

    def sleeper(i):
        
        anz=0
        for j in range(56):
            tt=random.randint(1,4)*2+1
     #       tt=2
            #print (self.name," %d loops for %f " % (j,tt))
            #print(obj)
            for zz in range(tt):
                anz += 1
                time.sleep(0.28)
                lll=0
                for k in range(100):
                    for kk in range(1000):
                        lll +=1
                #print (self.name,anz)
            
            #print ("thread %d woke up" % i)
            self.setData("message",self.name+"-----"+str(anz))
            obj.outExec.call()

            if anz>maxanz:
                break
            
        print ("-------------------Ende",self.name,anz,maxanz)
        self.setData("message",self.name+"  ENDE")
    

    for i in range(1):
        t = Thread(target=sleeper, args=(i,))
        t.start()
    




def run_FreeCAD_FigureOnFace(self):

    ca=np.array(self.getData("pattern"))

    #todo reshape auf flach
    if ca.shape[0]==0: return
    if len(ca.shape)==2:
        ca=ca.reshape(1,ca.shape[0],3)

    c=ca[:,:,0:2]

    #+# todo affine trafo matrix multiplikation vollstaendig machen
    p=self.getPinByName("transformation")
    trafo=p.getTransformation()

    if trafo is not None:
        c[:,:,0] *= trafo[0,0]*0.01
        c[:,:,1] *= trafo[1,1]*0.01
        c[:,:,0] += trafo[3,0]
        c[:,:,1] += trafo[3,1]
    
    cutborder=self.getData("cutBorder")
    shape=self.getPinObject('Shape_in')
    sf=shape.Surface

    say(shape.ParameterRange)
    (umin,umax,vmin,vmax)=shape.ParameterRange
    cols=[]
    tf=self.getData("tangentForce")*0.005
    for cv in c: 
        pts=[]  
        uvs=[]  
        uvsA=[]     
        broken=False
        for ca in cv+[cv[0]]:
            (u,v)=ca.tolist()
            if cutborder:
                if u<umin or u>umax or v<vmin or v>vmax: 
                    broken=True
            
            p=sf.value(u,v)
            pts+= [p]
            uvs += [FreeCAD.Base.Vector2d(u,v)]
            uvsA += [FreeCAD.Base.Vector(u,v)]
        if broken:
            continue

        deg=self.getData("degree")

        if deg == 0: # polygon dirfekt      
            try:
                cols += [Part.makePolygon(pts+[pts[0]])]
            except:
                pass

        else:
            bs2d = Part.Geom2d.BSplineCurve2d()

            #bs2d.buildFromPolesMultsKnots(uvs,[1]*(len(uvs)+1),range(len(uvs)+1),True,1)
            #if deg >1:
            if 1:
                uvsA += [uvsA[0]]
                l=len(uvsA)
                uvs2=[]
                for i in range(l-1):
                    try:
                        pa=uvsA[i]
                        pb=uvsA[i+1]
                        ll=(pb.sub(pa)).Length
                        n=(pb.sub(pa)).normalize()
                        uvs2 += [pa,pa+n*tf*ll,pb-n*tf*ll]
                    except:
                        pass
                uvs2 += [pb]
                uvs=[FreeCAD.Base.Vector2d(v.x,v.y) for v in uvs2]
                
            bs = Part.BSplineCurve()
            uvs2=uvs2[:-1]
            uvs=uvs[:-1]
            bs.buildFromPolesMultsKnots(uvs2,[1]*(len(uvs2)+1),range(len(uvs2)+1),True,2)
            #Part.show(bs.toShape());            return
            
            bs2d.buildFromPolesMultsKnots(uvs,[1]*(len(uvs)+1),range(len(uvs)+1),True,deg)
            #bs2d.buildFromPolesMultsKnots(uvs,[1]*(len(uvs)+1),range(len(uvs)+1),False,deg)
            e1 = bs2d.toShape(sf)
            if deg <= 1:
                cols += [e1]
            #say(cols)

        
        if 1 and deg>1 and self.getData("createFaces"):    
            face=shape
            try:
                splita=[(e1,face)]
                r=Part.makeSplitShape(face, splita)
                cols += [r[0][0]]
                
            except:
                say("FEHLER XX")
                pass
        else:
                cols += [e1]

        if 0: 
            e2=e1.copy()
            say(e2)
            e2.Placement.Base.z=10
            loft=Part.makeLoft([e1,e2],False)
            cols += [loft]


    # say("---------",cols)
    self.setPinObject("Shape_out",Part.Compound(cols))
    self.setPinObjects("details",cols)


    
    
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
    


def run_FreeCAD_Polygon(self):
    
            # recursion stopper
        if self.Called:
            return
        #sayl()
        # mit zeitstemple aktivieren
        #self.Called=True

        pts=self.points.getData()
        #say(pts)
        if pts[0].__class__.__name__ == 'list':
            pts=pts[0]
        say("--")
        if len(pts)<2:
            sayW("zu wenig points")
        else:
            try:
                shape=Part.makePolygon(pts)
            except:
                return

        self.setPinObject("Shape_out",shape)

        if self._preview:
            self.preview()

        #self.Called=False


def run_FreeCAD_ListOfVectors(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        i.owningNode().compute()
        vv=i.owningNode().getData(i.name)
        #say(i.name,vv)
        #say(np.array(vv).shape)
        if len(np.array(vv).shape)>1:
            ll=np.array(vv).shape
            vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
            b += vv.tolist()
        else:
            b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    self.setData("vectors",b)
    self.setColor(a=0.7)
    

def run_FreeCAD_ListOfVectorList(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        i.owningNode().compute()
        vv=i.owningNode().getData(i.name)
        #say(i.name,vv)
        #say(np.array(vv).shape)
        if len(np.array(vv).shape)>1:
            ll=np.array(vv).shape
            vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
            b += vv.tolist()
        else:
            b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    self.setData("vectors",b)
    self.setColor(a=0.7)
    
    
def run_FreeCAD_MoveVectors(self):
    #+# todo anpassen 1 2 3 dimensionale arrays

    vv=self.getData("vectors")
    mv=self.getData("mover")
    say(np.array(vv).shape)
    if len(np.array(vv).shape)>2:
        b2=[]
        for av in vv:
            
            b3=[v+mv for v in av]
            b2 += [b3]
    else:
        b2=[v+mv for v in vv]

    self.setData("vectors_out",b2)
    self.setColor(g=0,a=0.4)
    

def run_FreeCAD_ScaleVectors(self):
    #+# todo anpassen 1 2 3 dimensionale arrays

    vv=self.getData("vectors")
    mv=self.getData("scaler")

    b=[]
    if len(np.array(vv).shape)>1:
        ll=np.array(vv).shape
        vv=np.array(vv).reshape(np.prod(ll[:-1]),3)
        b += vv.tolist()
    else:
        b += [vv]
    
    b=[FreeCAD.Vector(*v) for v in b]
    b2=[FreeCAD.Vector(v.x*mv.x,v.y*mv.y,v.z*mv.z) for v in b]

    self.setData("vectors_out",b2)
    self.setColor(b=0,a=0.4)
    

## ||
## \/ okay


def run_FreeCAD_Transformation(self):

    vx=self.getData("vectorX")
    vy=self.getData("vectorY") 
    vz=self.getData("vectorZ") 
    v0=self.getData("vector0") 
    dat=[vx.x,vx.y,vx.z,
        vy.x,vy.y,vy.z,
        vz.x,vz.y,vz.z,
        v0.x,v0.y,v0.z,
        ]
    
    dat=np.array(dat).reshape(4,3)

    vv2=self.getPinByName("transformation")
    vv2.setTransformation(dat)
    


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
    


def run_FreeCAD_IndexToList(self):

    outArray = []
    pins=self.getPinByName('index').affected_by
    for i in pins:
        outArray.append(i.owningNode().getData(i.name))
    arr=np.array(outArray).flatten()
    if len(arr)==0:return
    m=max(arr)
    flags=np.zeros(m+1)
    for p in arr:
        flags[p]=1
    self.setData("flags",flags.tolist())
    self.setColor(b=0,a=0.4)
    
    
    
    
## ab hier neu 02.12.

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
    


def run_FreeCAD_LessThan(self):
    values=self.getData("values")
    threshold=self.getData("threshold")
    rc=[]
    for v in values:
        say(v, v<threshold)
        rc += [v<threshold]
    self.setData("lessThan",rc)
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_MoreThan(self):
    values=self.getData("values")
    threshold=self.getData("treshold")
    rc=[]
    for v in values:
        say(v, v>threshold)
        rc += [v>threshold]
    self.setData("moreThan",rc)
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_Equal(self):
    values=self.getData("values")
    threshold=self.getData("value")
    rc=[]
    for v in values:
        say(v, v ==threshold)
        rc += [v == threshold]
    self.setData("equal",rc)
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_Nearly(self):
    values=self.getData("values")
    threshold=self.getData("value")
    tol=self.getData("tolerance")
    rc=[]
    for v in values:
        #say(v, v ==threshold)
        rc += [v >= threshold -tol and  v <= threshold + tol]
    self.setData("nearly",rc)
    self.setColor(b=0,a=0.4)
    


def run_FreeCAD_And(self):
    a=self.getData("a")
    b=self.getData("b")
    flags=[va and vb for va,vb in zip(a,b)]
    self.setData("and",flags)

    wr=self.getWrapper()
    wr.setHeaderHtml("AND: "+flagstring(flags))

    self.setColor(b=0,a=0.4)
    


def flagstring(flags,lenf=10):
    '''create string form boolean list'''
    fstring=""
    for f in flags[:lenf]:
        fstring += "L" if f else "O"
    if lenf<len(flags):
        fstring += "..."
    return fstring


def run_FreeCAD_BoolToy(self):
    self.setData("flags",[self.getData("flagA"),self.getData("flagB"),self.getData("flagC"),self.getData("flagD")])
    flags=[self.getData("flagA"),self.getData("flagB"),self.getData("flagC"),self.getData("flagD")]
    fstring="Flags:"
    for f in flags:
        fstring += "L" if f else "O"
    #set the label of the node
    wr=self.getWrapper()
    wr.setHeaderHtml(fstring)
 
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_Or(self):
    a=self.getData("a")
    b=self.getData("b")
    flags = [va or vb for va,vb in zip(a,b)]
    self.setData("or",flags)
    
    wr=self.getWrapper()
    wr.setHeaderHtml("OR: "+flagstring(flags))
 
    self.setColor(b=0,a=0.4)
    



def run_FreeCAD_Not(self):
    a=self.getData("a")
    flags=[not va for va in a]
    self.setData("not",flags)

    wr=self.getWrapper()
    wr.setHeaderHtml("NOT: "+flagstring(flags))

    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_True(self):
    self.setData("true",[True]*self.getData("count"))
    self.setColor(b=0,a=0.4)
    

def run_FreeCAD_False(self):
    self.setData("false",[False]*self.getData("count"))
    self.setColor(b=0,a=0.4)
    

##ab hier neu 03.12.

def run_FreeCAD_FloatToy(self):
    #+# todo add scale and start parameter proc
    floats=[]
    start=self.getData("start")
    scale=self.getData("scale")
    limit=self.getData("limit")
    for i in range(limit):
        if i==0:
            v=self.getData("float")
        else:
            v=self.getData("float"+str(i))
        floats += [v*scale+start]
    

    trailer=self.getData("trailer")
    say("trailer",trailer)
    floats += trailer
    say("len floats",len(floats))

    self.setData("floats",floats)
    self.setColor(b=0,a=0.4)
    
    
def run_FreeCAD_Tube(self):
    #+# todo better normal for 3d curve
    floats=self.getData('parameter')
    radius=self.getData('radius')

    cc=self.getPinObject("backbone")
    if cc is None:
        say("no backbone curve abort")
        return
    say("expected parameter range", cc.ParameterRange)
    curve=cc.Curve
    pts=[]
    for f,r  in zip(floats,radius):
        f *= 0.1
        r *= 0.1
        p=curve.value(f)
        t=curve.tangent(f)[0]
        if 0:
            h=FreeCAD.Vector(0,0,1)
            n=t.cross(h)
        else:
            n=curve.normal(f)
            h=n.cross(t)
            
        pts += [[p-h*r,p+n*r,p+h*r,p-n*r]]
    
    # aufrichten normale
    z=pts[0]
    pts2 =[z]
    for i in range(len(pts)-1):
        a=z
        b=pts[i+1]
        sums=[]
        for j in range(4):
            sums +=[sum([(a[k-j]-b[k]).Length for k in range(4)])]
        say(sums.index(min(sums)))
        index=sums.index(min(sums))
        z=b[index:]+b[:index]
        pts2 += [z]
        
    self.setData("points",pts2)
    



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
    



def run_FreeCAD_ListOfShapes(self):
    
    say()
    say("list of vectors dump ...")
    say("Hack recompute input nodes is active")
    ySortedPins = sorted(self.pas.affected_by, key=lambda pin: pin.owningNode().y)
    b=[]
    for i in ySortedPins:
        # hack to get current values #+# todo debug
        # i.owningNode().compute()
        vv=i.owningNode().getPinObject(i.name)
        say(i.name,vv)
        b += [vv]
    say(b)
    self.setPinObjects("ShapeList",b)
    self.setColor(a=0.7)
    


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


def run_FreeCAD_Object(self, *args, **kwargs):

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




   

def run_FreeCAD_ListOfPlacements(self):

    if len(self.getPinByName("axes").affected_by) >0:
        axes=self.getData("axes")
    else: axes=[]

    if len(self.getPinByName("centers").affected_by) >0:
        centers=self.getData("centers")
    else:centers=[]

    if len(self.getPinByName("moves").affected_by) >0:
        moves=self.getData("moves")
    else:
        moves=[]

    if len(self.getPinByName("angles").affected_by) >0:        
        angles=self.getData("angles")
    else:
        angles=[]
        
    ll=max(len(axes),len(centers),len(moves),len(angles))

    if 1:
        if ll>len(centers):
            centers += [FreeCAD.Vector(0,0,0)]*(ll-len(centers))

        if ll>len(axes):
            axes += [FreeCAD.Vector(0,0,1)]*(ll-len(axes))

        if ll>len(moves):
            moves += [FreeCAD.Vector(0,0,0)]*(ll-len(moves))

        if ll>len(angles):
            angles += [10]*(ll-len(angles))
    
    
    rots=[]
    for m,ax,an,ce in zip(moves,axes,angles,centers):
        rots += [FreeCAD.Placement(m,FreeCAD.Rotation(ax,an),ce)]
    
    self.setPinPlacements("Placements",rots)




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





def run_FreeCAD_Repeat(self):
    
    s=self.getData("in")
    #say(s)
    count=self.getData("count")
    #say('##')
    t=[s]*count
    #say(t)
    self.setData("out",t)
    #self.setData("Shapes",[s]*count)

    sayl()




def run_FreeCAD_Index(self):
    vecs=self.getData("list")
    self.setData("item",vecs[self.getData('index')])


    
    

def run_FreeCAD_Zip(self):
    x=self.getData("x")
    y=self.getData("y")
    z=self.getData("z")
    
    zz= [FreeCAD.Vector(x,y,z) for x,y,z in zip(x,y,z)]
    say("len",len(zz))
    self.setData("vectors_out",zz)




def run_FreeCAD_ImportFile(self):

    try:
        self.last
    except:
        self.last=time.time()
        
    filename=self.getData('filename')
    
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
    #say(os.stat(filename))

    if not self.getData('force') and self.last > mtime:
        sayErr("---------------not new")
        return
        
    self.last = time.time()

    f=open(filename,"r")
    contents =f.read()
    ls=contents.splitlines()
    rr=[]
    vs=[]
    seps=self.getData('separator')
    sepk={
        'tabulator':'\t',
        'space':' ',
        'semicolon':';',
        'comma':',',
    }    
        
    sep=sepk[seps]
    for l in ls:
        try:
            if l.startswith('#'):
                continue
            rr += [[float(a) for a in l.split(sep)]]
            ff=[float(a) for a in l.split(sep)]
        except:
            pass
        vs += [FreeCAD.Vector(*ff[:3])]
        
    self.setData('data',rr)
    self.setData('points',vs)
    say(vs)



    if 0: # tessellation tests temp
        tt=FreeCAD.ActiveDocument.BePlane.Shape.Face1
        ta=time.time()
        zz=tt.tessellate(0.1)
        say("Tessellate",len(str(zz)))
        
        say(time.time()-ta)
    
#----------------------------------------------------------------------------



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






def run_TEST(self,val):
    sayl("TTTTTTTTTTTTTTTTTTTTTTTT")
    say(val)
    say(self)
    FreeCAD.s=self
    


def run_FreeCAD_Camera(self):
    '''
    v=Gui.ActiveDocument.ActiveView
    cam=v.getCameraNode()


    cam.scaleHeight(23)

    cam.viewBoundingBox


    cam.pointAt
    # SoCamera::pointAt(SbVec3f const &)


     cam.position
     
    cam.position.get() -> string
    cam.orientation.get()


    cam.position.set("20 4 5")

    v.setCamera("SoPerspectiveCamera")

    cam.heightAngle.get()
    '''
  
    v=FreeCADGui.ActiveDocument.ActiveView
    
    #FreeCADGui.activeDocument().activeView().setCameraType("Perspective")
    
    cam=v.getCameraNode()
    say(cam.__class__.__name__)
    typ=cam.__class__.__name__
    
    if 0:
        dx=self.getData('directionX')
        dy=self.getData('directionY')
        dz=self.getData('directionZ')
        r=FreeCAD.Rotation(FreeCAD.Vector(0,0,-1),FreeCAD.Vector(dx,dy,dz))
        cdir="{} {} {} {}".format(r.Axis.x,r.Axis.y,r.Axis.z,r.Angle)
        cam.orientation.set(cdir)
        say("direction",cam.orientation.get())
    
    cam.orientation.set("0 0 1 0")
    
    pos=self.getPinByName('position')
    if 0 and len(pos.affected_by) == 0:
        x=self.getData('positionX')
        y=self.getData('positionY')
        z=self.getData('positionZ')
    else:
         (x,y,z)=self.getData("position")   
    


    pos="{} {} {}".format(x,y,-z)
    say("Position",pos)
    cam.position.set(pos)

    if typ != "SoPerspectiveCamera":
        cam.height.set(str(z))
    else:
        say("angle",cam.heightAngle.get())
        cam.heightAngle.set(str(self.getData("angle")/50))
        #cam.widthAngle.set(str(self.getData("angle")/50))
        say("angle",cam.heightAngle.get())
        # das hat keinen einflass..
        #say("aspect ratio",cam.aspectRatio.get())
        #cam.aspectRatio.set("0.2")
        
    
    

    
    
    

    if 1:# self.getData('usePointAt'):
        pos=self.getPinByName('pointAt')
        if 0 and len(pos.affected_by) == 0:
            vec=coin.SbVec3f(self.getData('pointAtX'),self.getData('pointAtY'),self.getData('pointAtZ'))
        else:
            vec=coin.SbVec3f(*self.getData("pointAt" ) ) 
        
        cam.pointAt(vec)
        roll=0
        cam.pointAt(vec,coin.SbVec3f(0,0.0+math.sin(math.pi*roll/180),0.0+math.cos(math.pi*roll/180)))
    

    say("-----------------")
    #cam.nearDistance.set('0')
    #say("ND",cam.nearDistance.get())
    cam.farDistance.set('10000')
    #say("FD",cam.farDistance.get())
    #say(v)
    
    if self.getData("trackimages"):
        
        fn=self.getData("trackName")
        dn="/tmp/{}".format(fn)
        dirname = os.path.dirname(dn) 
        if not path.exists(dirname):
            os.mkdir(dirname)
        if self.getData("timestamp"):
            tt=str(time.time())
        else:
            tt=''
            
        v.saveImage("/tmp/{}{}.png".format(fn,tt))
        self.setData("image","/tmp/{}{}.png".format(fn,tt))



  


def run_FreeCAD_Counter(self):
    self.setData("count", self.getData("count")+1)



     
def run_FreeCAD_Export(self):
        
    a=self.getPinObject("Shape")
    fn=self.getData("filename")
    mode=self.getData('mode')
    if mode=='BREP':
        a.exportBrep(fn)
    elif  mode=='STEP':
        a.exportStep("/tmp/a.step")
    elif  mode=='Inventor':
        fn="/tmp/a.iv"
        s=a.writeInventor()   
        f= open(fn,"w+")
        f.write(s)
        f.close()
    
    
def run_FreeCAD_Import(self):
    
    fn=self.getData("filename")
    a=Part.Shape()
    #a.importBrep(fn)
    
    mode=self.getData('mode')
    if mode=='BREP':
        a.importBrep(fn)
    elif  mode=='STEP':
        a.importStep(fn)


    self.setPinObject("Shape_out",a)
    
    
def run_FreeCAD_Expression(self):

    
    modules=self.getData('modules')
    modules=modules.split(',')
    for m in modules:
        if m=='': break
        exec("import "+m)

    expression=self.getData('expression')
    a=self.getData('a')
    b=self.getData('b')
    c=self.getData('c')
    d=self.getData('d')
    v=eval(expression)

    say("parameters a,b,c,d",a,b,c,d)
    say(expression,v,v.__class__)
    self.setData('string_out',str(v))
    try:
        self.setData('float_out',float(v))
        self.setData('int_out',int(round(v)))
    except: pass
    
    self.setData('bool_out',v)
    




def run_FreeCAD_Seam(self):
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
       

def run_FreeCAD_Nurbs(self):
    
    #shape=FreeCAD.ActiveDocument.Cone.Shape.Face1
    #shape=FreeCAD.ActiveDocument.Sphere.Shape.Face1
    shape=self.getPinObject("shape")
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
    
#def rgb2gray(rgb):
#    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

    
def run_FreeCAD_ShapePattern(self):

    ptsa=np.array(self.getData('points'))

    # todo 3 kinds of input: single vector, list of vectors, array of vectors
    
    try:
        (a,b,c)=ptsa.shape
        pts=ptsa.reshape(a*b,3)
    except:
        pts=ptsa
    
    if ptsa.shape==(3):
        say("single point")
        pts=np.array([FreeCAD.Vector(ptsa)]).reshape(1,3)
    
    
    ptsa=np.array(self.getData('forces'))

    try:
        (a,b,c)=ptsa.shape
        diffs=ptsa.reshape(a*b,3)
    except:
        diffs=ptsa
    
    try:
        if diffs.shape==pts.shape:
            diffs=[a-b for a,b in zip(diffs,pts)]
            say("diffs berechnet")
            say(diffs[:4])      
        else:
            diffs=[FreeCAD.Vector(0,0,10+3*random.random()) for p in pts]    
    except:
        diffs=[FreeCAD.Vector(0,0,10+3*random.random()) for p in pts]    
    
    # single value or list
    radius=self.getData('radius')
    if isinstance(radius, list):
        rr=radius[0]
    else:
        rr=radius

    w=self.getData('width')
    w=(w+101)/201

    h=self.getData('height')
    h=(h+101)/201*50
    
    rand=(self.getData('randomize')+100)/200

    colors=[(0.5+random.random()*0.3,0.6+random.random()*0.4,random.random()*0.3) for p in pts]
    radius=[ (rand*(0.5-random.random())+1)*rr*w for p in pts]
 

    try:
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        sg.removeChild(self.sg2)
    except:
        say("noch kein sdfgd")

    if self.getData('hide'):
        return
   
    

    a=time.time()
    sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    sg2= coin.SoSeparator()

    mode=self.getData('mode')

    for p,c,r,d in zip(pts,colors,radius,diffs):
            
            trans = coin.SoTranslation()
            p=FreeCAD.Vector(p)
            
            if mode =='sphere':
                trans.translation.setValue(p[0],p[1],p[2])
                cub = coin.SoSphere()
                cub.radius.setValue(2*r)
                col = coin.SoBaseColor()
                col.rgb=(c[2],c[0],c[1])
                myCustomNode = coin.SoSeparator()
                myCustomNode.addChild(col)
                myCustomNode.addChild(trans)
                myCustomNode.addChild(cub)

            elif mode =='line':
                p1=(p[0],p[1],p[2])
                p1=(p[0]+d[0],p[1]+d[1],p[2]+d[2]*h)
                p2=(p[0],p[1],p[2])
                dash = coin.SoSeparator()
                v = coin.SoVertexProperty()
                v.vertex.set1Value(0, p1)
                v.vertex.set1Value(1, p2)
                l = coin.SoLineSet()
                l.vertexProperty = v
                dash.addChild(l)
                drawstyle = coin.SoDrawStyle()
                drawstyle.lineWidth =2
                col = coin.SoBaseColor()
                myCustomNode = coin.SoSeparator()
                myCustomNode.addChild(col)
                myCustomNode.addChild(drawstyle)
                myCustomNode.addChild(trans)
                myCustomNode.addChild(dash)

            elif mode =='cube':
                trans.translation.setValue(p[0],p[1],p[2]+0.5*h)
                cub = coin.SoCube()
                cub.width.setValue(2*r)
                cub.height.setValue(2*r)
                cub.depth.setValue(h)
                col = coin.SoBaseColor()
                col.rgb=(c[2],c[0],c[1])                
                myCustomNode = coin.SoSeparator()
                myCustomNode.addChild(col)
                myCustomNode.addChild(trans)
                myCustomNode.addChild(cub)

            elif mode =='cone':
                trans.translation.setValue(p[0],p[1],p[2]+0.5*h)
                cub = coin.SoCone()
                cub.height.setValue(h)
                cub.bottomRadius.setValue(2*r)
                myRotation = coin.SoRotationXYZ()
                myRotation.angle = coin.M_PI/2
                myRotation.axis = coin.SoRotationXYZ.X
                col = coin.SoBaseColor()
                col.rgb=(c[2],c[0],c[1])
                myCustomNode = coin.SoSeparator()
                myCustomNode.addChild(col)
                myCustomNode.addChild(trans)
                myCustomNode.addChild(myRotation) 
                myCustomNode.addChild(cub)

            elif mode =='human':
                say('not yet implemented')
                #+# todo
                
            else: # mode == 'tree'
                trans.translation.setValue(p[0],p[1],p[2]+1*h)
                cub = coin.SoCone()
                cub.height.setValue(2*h)
                cub.bottomRadius.setValue(2*r)
                myRotation = coin.SoRotationXYZ()
                myRotation.angle = coin.M_PI/2
                myRotation.axis = coin.SoRotationXYZ.X
                col = coin.SoBaseColor()
                col.rgb=(c[2],c[0],c[1])
                trans2 = coin.SoTranslation()
                trans2.translation.setValue(0,0.6*h,0)
                cub2 = coin.SoCone()
                cub2.height.setValue(1*h)
                cub2.bottomRadius.setValue(1.4*r)
                myCustomNode = coin.SoSeparator()
                myCustomNode.addChild(col)
                myCustomNode.addChild(trans)
                myCustomNode.addChild(myRotation) 
                myCustomNode.addChild(cub)
                myCustomNode.addChild(trans2)
                myCustomNode.addChild(cub2)
            
            sg2.addChild(myCustomNode)

    sg.addChild(sg2)
    self.sg2=sg2

def run_FreeCAD_ImageT(self):

    from scipy import ndimage
    fn=self.getData('image')
    import matplotlib.image as mpimg    

    img=mpimg.imread(fn)
    (sa,sb,sc)=img.shape
    red=0.005*(self.getData("red")+100)
    green=0.005*(self.getData("green")+100)
    blue=0.005*(self.getData("blue")+100)
    #blue=0
    say("rgb",red,green,blue)
    
    
    # andere filtre
    #img = ndimage.sobel(img)
    #img = ndimage.laplace(img)
    
    im2=img[:,:,0]*red+img[:,:,1]*green+img[:,:,2]*blue
    im2=np.round(im2)
    
    if self.getData('invert'):
        im2 = 1- im2
    
    #im2 = ndimage.sobel(im2)

   
    ss=int((self.getData('maskSize')+100)/20)
    say("ss",ss)
    if ss != 0:
        mode=self.getData('mode')
        say("mode",mode)
        if mode=='closing':
            im2=ndimage.grey_closing(im2, size=(ss,ss))
        elif mode=='opening':
            im2=ndimage.grey_opening(im2, size=(ss,ss))    
        elif mode=='erosion':
            im2=ndimage.grey_erosion(im2, size=(ss,ss))
        elif mode=='dilitation':
            im2=ndimage.grey_dilation(im2, footprint=np.ones((ss,ss)))
        else:
            say("NO MODE")
       


    




    nonzes=np.where(im2 == 0)
    pts = [FreeCAD.Vector(sb+-x,sa-y) for y,x in np.array(nonzes).swapaxes(0,1)]
    
    h=10
    pts = [FreeCAD.Vector(sb+-x,sa-y,(red*img[y,x,0]+green*img[y,x,1]+blue*img[y,x,2])*h) for y,x in np.array(nonzes).swapaxes(0,1)]
    colors=[img[y,x] for y,x in np.array(nonzes).swapaxes(0,1)]
    say("len pts",len(pts))
    self.setData("Points_out",pts)
    #self._preview=True   
    
    



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
            say("restore matrix")
            
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

    

def run_FreeCAD_uv2xyz(self):
    sh=self.getPinObject("Shape")
    bs=sh.Surface
    uvs=self.getData('points')
    
    pts += [bs.value(uv[0],uv[1]) for uv in uvs]
    self.setData('Points_out',pts)
    




def run_FreeCAD_QuadMesh(self):

    try:
        FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
    except:
        pass

    if self.getData('hide'):
        return

    points=self.getData('points')
    vps=np.array(points)
    (a,b,c)=vps.shape
    tt=vps.reshape(a*b,3)

    result = coin.SoSeparator()

    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (.78, .57, .11)
    result.addChild(myMaterial)

    myCoords = coin.SoCoordinate3()
    myCoords.point.setValues(0, a*b, tt)
    result.addChild(myCoords)

    myQuadMesh = coin.SoQuadMesh()
    myQuadMesh.verticesPerRow = b
    myQuadMesh.verticesPerColumn = a

    result.addChild(myQuadMesh)

    sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    sg.addChild(result)
    self.gg=result
        



def run_FreeCAD_replacePoles(self):

    sh=self.getPinObject("Shape")
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



# glättenb

def run_FreeCAD_IronCurve(self):

    sh=self.getPinObject('Shape')
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


def run_FreeCAD_Sweep(self):

    profile=FreeCAD.ActiveDocument.Circle.Shape.Edge1
    path=FreeCAD.ActiveDocument.Sketch.Shape.Edge1.copy()
    #path.Curve.segment(1,5)
    say(path.Curve.getKnots())
    #path.reverse()
    #profile.reverse()
    
    #path=Part.makePolygon([FreeCAD.Vector(),FreeCAD.Vector(0,100,0)])
    
    sweep=Part.makeSweepSurface(path,profile,self.getData('f'))
    #sweep=Part.makeSweepSurface(path,profile,10)
    say("hh")
    self.setPinObject('Shape_out',sweep)

def run_FreeCAD_Loft(self):

    shapes=self.getPinObjectsA('shapes')

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
    
    
def run_FreeCAD_IfElse(self):
    self.setData('out',self.getData('flag'))
    self.outExec.call()
    if self.getData('flag'):
        self.ifExec.call()
    else:
        self.elseExec.call()
    



import nodeeditor
import nodeeditor.cointools
reload(nodeeditor.cointools)

from nodeeditor.cointools import *


        


# 19-22.01.2020
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
        
       



def run_commit(self):
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
    points=np.array([[bs.value(ua+(ue-ua)*u*0.01,va+(ve-va)*v*0.01) for v in range(101)]  for u in range(101)])
    
    nomrs=[]
    for u in range(101):
        nus=[]
        for v in range(101):
            try:
                nus += [bs.normal(ua+(ue-ua)*u*0.01,va+(ve-va)*v*0.01)]
            except:
                nus += [FreeCAD.Vector()]
        nomrs += [nus]
        
    norms=np.array(nomrs)
    #norms=np.array([[bs.normal(ua+(ue-ua)*u*0.01,va+(ve-va)*v*0.01) for v in range(101)]  for u in range(101)]) 

    newpts=points+ norms*h
    self.setData('Points_out',newpts.tolist())
    self.setPinObject('Shape_out',bs.toShape())
     
