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



from nodeeditor.cointools import *
    



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
            say("restore matrix - hack: deactivated ")
            
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





def run_FreeCAD_QuadMesh(self):

    try:
        FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.gg)
    except:
        pass

    if self.getData('hide'):
        return

    points=self.getData('points')
    vps=np.array(points)
    try:
        (a,b,c)=vps.shape
    except:
        sayErOb(self,"points have no grid structure")
        return
        
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




