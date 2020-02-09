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


