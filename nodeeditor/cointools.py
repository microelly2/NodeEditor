# coin tools

import Part,FreeCADGui
from pivy import coin
from pivy.coin import *
from nodeeditor.say import *

def clearcoin(self):
    root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    try:
        root.removeChild(self._sg)
        del(self._sg)
    except:
        pass

def hidecoin(self):
    root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    sayl("WW",self._sg)
    root.removeChild(self._sg)
    say("Done")
    try:
        root.removeChild(self._sg)
        say("deleted")
        #clearcoin(self)

    except:
        pass

def showcoin(self):
    root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    sayl()
    try:
        root.addChild(self._sg)
    except:
        pass
        


def displaysphere(self,point,radius=5,color=(1,1,1)):
    
    try:
        sg=self._sg
    except:
        sg    = SoSeparator()
        self._sg= sg

        root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        root.addChild(sg)

    p=point
    #say(point,color,"##########")

    trans = coin.SoTranslation()
    trans.translation.setValue(p.x,p.y,p.z)
    cub = coin.SoSphere()
    cub.radius.setValue(radius)
    col = coin.SoBaseColor()
    col.rgb=color
    myCustomNode = coin.SoSeparator()
    myCustomNode.addChild(col)
    myCustomNode.addChild(trans)
    myCustomNode.addChild(cub)
    sg.addChild(myCustomNode)


def displayspheres(self,points,radius=5,color=(1,1,1)):
    for p in points:
        displaysphere(self,p,radius=radius,color=color)

def displayline(self,pts,color=(1,1,1),linewidth=4):
    
    try:
        sg=self._sg
    except:
        sg    = SoSeparator()
        self._sg= sg
        root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        root.addChild(sg)
        
        
    heart    = SoSeparator()
    coord = SoCoordinate3()
    coord.point.setValues(0,len(pts),pts)
    a=[i for i in range(len(pts))]+[-1]

    drawstyle = SoDrawStyle()
    drawstyle.style = SoDrawStyle.LINES
    drawstyle.lineWidth = 1
   

    lineSet = SoIndexedLineSet()
    lineSet.coordIndex.setValue(0)
    lineSet.coordIndex.setValues(0, len(a), a)

    myMaterial = SoMaterial()
    myBinding = SoMaterialBinding()
    myMaterial.diffuseColor.set1Value(0, SbColor(*color))
#   myMaterial.diffuseColor.set1Value(1, SbColor(0,1.,0))
#   myMaterial.diffuseColor.set1Value(2, SbColor(0,1.,1))
#   myMaterial.diffuseColor.set1Value(3, SbColor(1,0.,1))
#    myBinding.value = SoMaterialBinding.PER_PART

    heart.addChild(drawstyle)
    heart.addChild(myMaterial)
    heart.addChild(myBinding)


    heart.addChild(coord)
    heart.addChild(lineSet)
    sg.addChild(heart)
    #root.removeChild(heart)
    # self._sg=heart
   # displaytext(self,pts,color=(1,1,0))


def displaytext(self,pos,color=(1,1,1),text=["aaa","bbb"]):
    
    textpos = coin.SoTransform()
    p=pos
    textpos.translation.setValue(p.x+10,p.y+10,p.z+10)
    font = coin.SoFont()
    font.size = 20
    text2d = coin.SoText2()
    text3d = coin.SoAsciiText()
    
    text2d.string.setValues([l.encode("utf8") for l in text if l])
    text3d.string.setValues([l.encode("utf8") for l in text if l])

    myMaterial = SoMaterial()
    myMaterial.diffuseColor.set1Value(0, SbColor(*color))

    try:
        sg=self._sg
    except:
        sg    = SoSeparator()
        self._sg= sg
        root=FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        root.addChild(sg)
        
        
    node2d    = SoSeparator()


    node2d.addChild(textpos)
    node2d.addChild(myMaterial)
    node2d.addChild(font)
    node2d.addChild(text2d)
    #node2d.addChild(text3d)
    sg.addChild(node2d)

