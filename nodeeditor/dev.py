import numpy as np
import random
import time

import FreeCAD
import FreeCADGui

import Part

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin

from nodeeditor.say import *
import nodeeditor.store as store
import nodeeditor.pfwrap as pfwrap


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
            say("probme seting",p)
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
    
    self.outExec.call()







def run_Plot_compute(self,*args, **kwargs):

    import matplotlib.pyplot as plt

    if self.f2.getData():
        plt.figure(2)

    elif self.f3.getData():
        plt.figure(3)
    else:
        plt.figure(1)

#   plt.close()
    plt.title(self.getName())

    x=self.xpin.getData()
    y=self.ypin.getData()

    #say(x)
    #say(y)
    say(len(x),len(y))


    if len(y)  != 0:
        N=len(y)
        if len(x) != len(y):
            x = np.linspace(0, 10, N, endpoint=True)
        else:
            x=np.array(x)

        y=np.array(y)

        if not self.f3.getData():
            plt.plot(x, y, 'bx')
        plt.plot(x, y , 'b-')


    x2=self.xpin2.getData()
    y2=self.ypin2.getData()
    say (len(x2),len(y2))
    if x2  !=  None and y2  !=  None:
        x2=np.array(x2)
        y2=np.array(y2)
        if self.f3.getData():
            plt.plot(x2, y2 , 'r-')
        else:
            plt.plot(x2, y2, 'ro')


    plt.show()



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
    cc=self.getObject()
    if cc  !=  None:
        cc.Label=self.objname.getData()
        cc.Shape=shape
        #cc.ViewObject.LineWidth=8
        cc.ViewObject.LineColor=(1.,1.,0.)

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
    shape=f.makeParallelProjection(e,d)
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
    closed=False

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

    cc=self.getObject()
    if cc  !=  None:
        cc.Label=self.objname.getData()

    if self.getPinByName('inverse').getData():
        cc.Shape=r2[0][0]
    else:
        cc.Shape=r[0][0]

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


def run_FreeCAD_view3D(self, *args, **kwargs):

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
    if s  !=  None:
        if s.Volume != 0:
            f.Shape=s
        else:  
            t=Part.makeBox(0.001,0.001,0.001)#.toShape()
            f.Shape=t

    f.recompute()
    f.purgeTouched()

    if 0:
        if not wireframe:
            f.ViewObject.DisplayMode = "Flat Lines"
            f.ViewObject.ShapeColor = (random.random(),random.random(),1.)
        else:
            f.ViewObject.DisplayMode = "Wireframe"
            f.ViewObject.LineColor = (random.random(),random.random(),1.)

    self.outExec.call()




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


    self.outExec.call()



def run_FreeCAD_uIso(self,*args, **kwargs):

    f=self.getPinObject('Face')
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    u=self.getData("u")

    uu=umin+(umax-umin)*0.1*u
    c=sf.uIso(uu)
    self.setPinObject('Edge',c.toShape())

    if self.getData('display'):
        obj=self.getObject()
        obj.Shape=c.toShape()

    self.outExec.call()


def run_FreeCAD_vIso(self,*args, **kwargs):

    f=self.getPinObject('Face')
    if f.__class__.__name__  == 'Shape':
        f=f.Face1
    sf=f.Surface

    [umin,umax,vmin,vmax]=f.ParameterRange
    v=self.getData("v")

    vv=vmin+(vmax-vmin)*0.1*v
    c=sf.vIso(vv)
    self.setPinObject('Edge',c.toShape())

    if self.getData('display'):
        obj=self.getObject()
        obj.Shape=c.toShape()

    self.outExec.call()

def run_FreeCAD_uvGrid(self,*args, **kwargs):

    f=self.getPinObject('Face_in')
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


    self.setPinObjects('uEdges',us)
    self.setPinObjects('vEdges',vs)
    self.setPinObject('Compound_out',Part.Compound(us+vs))
    self.outExec.call()



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
        say(ix,len(r),len(pts))
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
                    say()
                    uvedges += [(xa,ya,xb,yb)]
                    uvedgesA += [(xa,ya,xb,yb)]
                    #col2 += [Part.makePolygon([pa,pb])]
                if not check (xa,ya,xb,yb):
                    (xa,ya,xb,yb)=trim(xa,ya,xb,yb)
                    if check (xa,ya,xb,yb):
                        pa=FreeCAD.Vector(xa,ya)
                        pb=FreeCAD.Vector(xb,yb)
                        say()
                        #uvedges += [(xa,ya,xb,yb)]
                        uvedgesA += [(xa,ya,xb,yb)]
                        #col2 += [Part.makePolygon([pa,pb])]
                    else:
                        say("Err",xa,ya,xb,yb)
        try:
            uuu=uvedgesA+[(uvedgesA[-1][2],uvedgesA[-1][3],uvedgesA[0][0],uvedgesA[0][1])]
            say(uuu[0])
            say(uuu[-1])
            say("--")
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
    say("vor.regions",vor.regions)
    for ix, r in  enumerate(vor.regions):
        pts=[vertexes[v] for v in r if v  !=  -1]
        if ix==self.getData('indA'):
            say(ix,r)
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
                        say(shapes)
                        cc.Shape=shapes[1]
            break


    from scipy.spatial import Delaunay

    tri = Delaunay(pointsa)
    say(tri.simplices)
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


    self.outExec.call()




def run_FreeCAD_Hull(self,*args, **kwargs):
    '''
    calculate voronoi delaunay  stuff for 3D point cloud
    '''

    from scipy.spatial import Delaunay

    # get the point cloud
    shape=self.getPinObject("Shape")
    points=[v.Point for v in shape.Vertexes]

    # threshold parameter for alpha hull
    lmax=0.03*(self.getData('alpha')+0.1)

    #core calculation
    atime=time.time()
    tri = Delaunay(points)
    say("time to caculate delaunay:{}".format(time.time()-atime)) 

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
    say("time to caculate alpha:{}".format(time.time()-atime)) 


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
    self.outExec.call()
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
    #say(self.Lock)
    #self.Lock=0
    import os
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

    self.outExec.call()
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

    self.outExec.call()


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

    self.outExec.call()


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

    self.outExec.call()

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
    r=self.getData("MajorRadius")*0.1

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

    self.outExec.call()

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

    self.outExec.call()

 
 

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
            say ("try tolerance",tol)
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

    self.outExec.call()



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

    self.outExec.call()


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
    ptsa=edge.discretize(count)

    self.setPinObject("Shape_out",Part.makePolygon(ptsa))
    if 0:
        sc=Part.BSplineCurve()
        sc.buildFromPoles(ptsa)
        self.setPinObject("Shape_out",sc.toShape())
    
    self.outExec.call()
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

    self.outExec.call()



def run_FreeCAD_FillEdge(self,produce=False, **kwargs):
   

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
            say ("try tolerance",tol)
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

    self.outExec.call()


# autum 19
def run_FreeCAD_Destruct_BSpline(self,bake=False, **kwargs):
    shape=self.getPinObject("Shape_in")
    c=shape.Curve
    say(c)
    self.setData("knots",c.getKnots())
    self.setData("mults",c.getMultiplicities())
    self.setData("degree",c.Degree)
    self.setData("poles",c.getPoles())
    #self.setData("periodic",False)
    say("done")
    self.outExec.call()


def run_FreeCAD_Destruct_BSplineSurface(self,bake=False, **kwargs):
    shape=self.getPinObject("Shape_in")
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
    self.outExec.call()


def run_FreeCAD_BSplineSurface(self, *args, **kwargs):

        dat=self.arrayData.getData()
        #say("dat",dat)
        if len(dat) == 0:
            sayW("no points for poles")
            return
        dat=np.array(dat)
        sf=Part.BSplineSurface()

        poles=np.array(dat)
        #say(poles)

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
        self.outExec.call()



def run_FreeCAD_BSplineCurve(self, *args, **kwargs):

        dat=self.arrayData.getData()
        dat=np.array(dat)
        sf=Part.BSplineCurve()

        poles=np.array(dat)
        say(poles)
        (countA,_)=poles.shape
        degA=min(countA-1,3,self.getPinByName("maxDegree").getData())

        multA=[degA+1]+[1]*(countA-1-degA)+[degA+1]
        knotA=range(len(multA))

        sf=Part.BSplineCurve()
        sf.buildFromPolesMultsKnots(poles,multA,knotA,False,degA)
        shape=sf.toShape()

        shape=sf.toShape()
        
        #cc=self.getObject()
        #cc.Label=self.objname.getData()
        #cc.Shape=shape

        self.setPinObject("Shape_out",shape)
        self.outExec.call()
    


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
        self.outExec.call()

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
    self.outExec.call()
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
def run_FreeCAD_approximateBSpline(self):
    shin=self.getPinObject("Shape_in")
    shin=shin.toNurbs().Face1
    sf=shin.Surface
    points=self.getData("points")
    uvs=[]
    pts2da=[sf.parameter(p) for p in points]
    pts2d=[]
    for i,p in enumerate(pts2da):
        pts2d += [FreeCAD.Base.Vector2d(p[0],p[1])]

    bs2d = Part.Geom2d.BSplineCurve2d()
    tol=max(self.getData("tolerance"),1.)
    bs2d.approximate(pts2d,Tolerance=tol*0.001)
    self.setPinObject("Shape_out",bs2d.toShape(sf))
    self.outExec.call()

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
def run_FreeCAD_interpolateBSpline(self):
    shin=self.getPinObject("Shape_in")
    shin=shin.toNurbs().Face1
    sf=shin.Surface
    points=self.getData("points")
    say("interpolate for {} points".format(len(points)))
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
    self.outExec.call()



def run_FreeCAD_swept(self):
    ta=time.time()
    l=self.getData("steps")
    step=self.getData("step")

    # the border of the car
    trackpoints=self.getData("trackPoints")
#   say(trackpoints)
    path=self.getPinObject("Path")
#   say(path)
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
    self.outExec.call()


    say(time.time()-ta)




def run_FreeCAD_handrail(self):

    anz=self.getData('steps')
    heightStep=self.getData('heightStair')/anz*4
    heightBorder=self.getData('heightBorder')
    path=self.getPinObject("Path")
    borderA=self.getPinObject("borderA")
    borderB=self.getPinObject("borderB")

    edge=path
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
    self.outExec.call()


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
    self.outExec.call()


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
    self.outExec.call()
 
    say(self.getWrapper())
    FreeCAD.b=self.getWrapper().getHeaderText()
    say("end neue version")




def run_FreeCAD_FlipSwapArray(self):
    say("flipswap")
    say(self.name)
    polesA=np.array(self.getData('poles_in'))
    poles=polesA.swapaxes(0,1)
    self.setData('poles_out',poles.tolist())
    self.outExec.call()


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
    self.outExec.call()


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
    ee=neighbor[e][0]
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
    self.outExec.call()



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
    self.outExec.call()


def run_FreeCAD_randomizePolygon(self,*args, **kwargs):
#    return
#def u():
    sayl()
    edge=self.getPinObject("Shape_in")
    say(edge)
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
    self.outExec.call()
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

            self.outExec.call()
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
        self.setColor()

        self.outExec.call()
        say("Ende call ",i,time.time()-a)




    def looper(j):
        j=self.getData("loops")
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

    say("Data:",self.kw)
    say("Sender:",self.sender)
    #self.setData("signalName",self.sender)
    #self.setData("senderMessage",self.kw['message'])
    self.setColor(b=0,a=0.4)
    self.outExec.call()    




def myExecute_Receiver(proxy,fp):
#    sayl()
    proxy.name=fp.Name
    run_FreeCAD_Receiver(proxy)

def myExecute_Blinker(proxy,fp):
#    sayl()
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
    self.outExec.call()
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
        self.outExec.call()

    for i in range(1):
        t = Thread(target=sleeper, args=(i,))
        t.start()
    
    self.outExec.call()



def run_FreeCAD_figureOnFace(self):

    ca=np.array(self.getData("pattern"))

    #todo reshape auf flach
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

    self.setColor()
    self.outExec.call()    
    
def run_FreeCAD_repeatPattern(self):

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
    self.outExec.call()    


def run_FreeCAD_Polygon2(self):
    
            # recursion stopper
        if self.Called:
            return
        #sayl()
        # mit zeitstemple aktivieren
        #self.Called=True

        pts=self.points.getData()
        say(pts)
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

            say("shape",shape)
            self.setPinObject("Shape_out",shape)

            if self.shapeout.hasConnections():
                self.postCompute()

            if self.shapeOnly.getData():
                cc=self.getObject()
                self.postCompute()
            else:
                cc=self.getObject()
                if cc  !=  None:
                    cc.Label=self.objname.getData()
                    cc.Shape=shape
                    self.postCompute(cc)

        if self._preview:
            self.preview()

        #self.Called=False


def run_FreeCAD_listOfVectors(self):
    
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
    self.outExec.call()    
    
    
def run_FreeCAD_moveVectors(self):
    #+# todo anpassen 1 2 3 dimensionale arrays

    vv=self.getData("vectors")
    mv=self.getData("mover")

    if len(np.array(vv).shape)>1:
        b2=[]
        for av in vv:
            b3=[v+mv for v in av]
            b2 += [b3]
    else:
        b2=[v+mv for v in b]

    self.setData("vectors_out",b2)
    self.setColor(g=0,a=0.4)
    self.outExec.call()    

def run_FreeCAD_scaleVectors(self):
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
    self.outExec.call()    

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
    self.outExec.call()    


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
    self.outExec.call()    


def run_FreeCAD_IndexToList(self):

    outArray = []
    pins=self.getPinByName('index').affected_by
    for i in pins:
        outArray.append(i.owningNode().getData(i.name))
    arr=np.array(outArray).flatten()
    m=max(arr)
    flags=np.zeros(m+1)
    for p in arr:
        flags[p]=1
    self.setData("flags",flags.tolist())
    self.setColor(b=0,a=0.4)
    self.outExec.call()    
    
    
    
## ab hier neu 02.12.

def run_FreeCAD_distToShape(self):
    
    eids=self.getPinObjectsA("shapes")
    target=self.getPinObject("target")
    dists=[]
    for s in eids:
        dists += [target.distToShape(s)[0]]
    self.setData("distance",dists)
    self.setColor(b=0,a=0.4)
    self.outExec.call()    


def run_FreeCAD_lessThan(self):
    values=self.getData("values")
    threshold=self.getData("threshold")
    rc=[]
    for v in values:
        say(v, v<threshold)
        rc += [v<threshold]
    self.setData("lessThan",rc)
    self.setColor(b=0,a=0.4)
    self.outExec.call()    

def run_FreeCAD_and(self):
    a=self.getData("a")
    b=self.getData("b")
    flags=[va and vb for va,vb in zip(a,b)]
    self.setData("and",flags)

    wr=self.getWrapper()
    wr.setHeaderHtml("AND: "+flagstring(flags))

    self.setColor(b=0,a=0.4)
    self.outExec.call()    


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
    self.outExec.call()    

def run_FreeCAD_or(self):
    a=self.getData("a")
    b=self.getData("b")
    flags = [va or vb for va,vb in zip(a,b)]
    self.setData("or",flags)
    
    wr=self.getWrapper()
    wr.setHeaderHtml("OR: "+flagstring(flags))
 
    self.setColor(b=0,a=0.4)
    self.outExec.call()    

def run_FreeCAD_not(self):
    a=self.getData("a")
    flags=[not va for va in a]
    self.setData("not",flags)

    wr=self.getWrapper()
    wr.setHeaderHtml("NOT: "+flagstring(flags))

    self.setColor(b=0,a=0.4)
    self.outExec.call()    

def run_FreeCAD_true(self):
    self.setData("true",[True]*self.getData("count"))
    self.setColor(b=0,a=0.4)
    self.outExec.call()    

def run_FreeCAD_false(self):
    self.setData("false",[False]*self.getData("count"))
    self.setColor(b=0,a=0.4)
    self.outExec.call()    

##ab hier neu 03.12.

def run_FreeCAD_FloatToy(self):
    floats=[]
    for i in range(10):
        if i==0:
            v=self.getData("float")
        else:
            v=self.getData("float"+str(i))
        floats += [v]

    self.setData("floats",floats)
    self.setColor(b=0,a=0.4)
    self.outExec.call()    
    
def run_FreeCAD_Tube(self):
    floats=self.getData('parameter')
    radius=self.getData('radius')

    cc=self.getPinObject("backbone")
    say("expected parameter range", cc.ParameterRange)
    curve=cc.Curve
    pts=[]
    for f,r  in zip(floats,radius):
        f *= 0.1
        r *= 0.1
        p=curve.value(f)
        t=curve.tangent(f)[0]
        n=curve.normal(f)
        h=FreeCAD.Vector(0,0,1)
        n=t.cross(h)
        pts += [[p-h*r,p+n*r,p+h*r,p-n*r]]

    self.setData("points",pts)
    self.outExec.call()    
