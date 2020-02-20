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


#    poles=FreeCAD.ActiveDocument.Shape.Shape.Face1.Surface.getPoles()
    
    shapein=self.getPinObject("Shape_in")
    say(shapein)
    if shapein is None: 
        sayErOb(self,"no Shape_in")
        return

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




