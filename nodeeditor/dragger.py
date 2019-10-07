#dragger.py
import os
os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join([ "PyQt4"])
#import Qt
#from Qt import QtCore
#from Qt import QtGui
#from Qt.QtWidgets import *




from nurbswb.say import *

import FreeCAD
import sys,time
import random


from nodeeditor.say import *

from nodeeditor.Commands import clearReportView

from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import timer
from PySide import QtGui,QtCore

class EventFilter(QtCore.QObject):
    '''Eventfilter for facedrawing'''

##\cond

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.mouseWheel=0
        self.enterleave=False
        self.enterleave=True
        self.keyPressed2=False
        self.editmode=False
        self.key='x'
        self.posx=-1
        self.posy=-1
        self.lasttime=time.time()
        self.lastkey='#'
        self.colorA=0
        self.colors=[]
        self.pts=[]
        self.ptsm=[]
        self.mode='n'

        self.on=False
        self.displayObjects=False
        self.t=[]
        self.z=0
        self.LMpress=False

    @timer
    def snapList(self,delta=0.04):
            #say("snaplist")
#            if self.t == None:
#                return
            if not self.LMpress:
                return

            if self.displayObjects<time.time()-delta:
                
                #clearReportView(name="dragger")
                if self.t != None:
                    say(self.t[0])
                    t=self.t
                    try:
                        say("!!",self.selobject,self.selcomponent)
                    except:
                        self.node.selectedFaceChanged.call() 
                        self.selobject=t[0]['Object']
                        self.selcomponent=t[0]['Component']

                        obj=FreeCAD.ActiveDocument.getObject('self.selobject')
                        if obj == None: return
                        shape=getattr(obj, self.selcomponent)
                        say("Shape AA",shape)
                        self.node.setPinObject("selectedFace",shape)
                        say(self.selobject,self.selcomponent)

                    if  self.selobject != t[0]['Object'] or  self.selcomponent != t[0]['Component']:
                        say("Face changed")
                        self.node.selectedFaceChanged.call() 
                        say("old",self.selobject,self.selcomponent)
                        say("new",t[0])

                    self.selobject=t[0]['Object']
                    self.selcomponent=t[0]['Component']

                    obj=FreeCAD.ActiveDocument.getObject(self.selobject)
                    say(obj.Name)
                    shape=getattr(obj.Shape, self.selcomponent)
                    say("Shape BB",shape)
                    self.node.setPinObject("selectedFace",shape)

                    # send koord 1.sel
                    tt=t[0]
                    self.node.setData('positionSelection',FreeCAD.Vector(tt['x'],tt['y'],tt['z']))
                    self.node.selectionExec.call()
                    
                    return
                    #clearReportView(name="dragger")
                    say("------------display objects under mouse ----")

                    t=[]
                    for i,tt in enumerate(self.t):
                        if not tt['Object']=='View_FreeCAD_Sphere': t+=[tt]


                    l=len(t) 
                    zz=self.z % l
                    #say("len list",self.z,zz,l)
                    #say(t)
                    for i,tt in enumerate(t):

                        ss=tt['Object']+"."+tt['Component']
                        ss += ":     "+str(round(tt['x'],1))+" "+str(round(tt['y'],1))+" "+str(round(tt['z'],1))
                        if i ==zz:
                            say("----> {} <---".format(ss))
                            self.node.setData('positionSelection',FreeCAD.Vector(tt['x'],tt['y'],tt['z']))
                            
                        else:
                           say("       {}".format(ss))
                           pass
                    self.node.selectionExec.call()

            self.displayObjects=time.time()    





    def eventFilter(self, o, e):
        ''' the eventfilter for the facedraw server'''

        z=str(e.type())

        event=e

        if event.type() == QtCore.QEvent.ContextMenu : return True

        # not used events
        if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
                z == 'PySide.QtCore.QEvent.Type.ChildRemoved'or \
                z == 'PySide.QtCore.QEvent.Type.User'  or \
                z == 'PySide.QtCore.QEvent.Type.Paint' or \
                z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
                z == 'PySide.QtCore.QEvent.Type.UpdateRequest'  : 
            return QtGui.QWidget.eventFilter(self, o, e)


        if z == 'PySide.QtCore.QEvent.Type.KeyPress':
            # http://doc.qt.io/qt-4.8/qkeyevent.html

            if 1:


                if 1:
                    # only two function keys implemented, no modifieres
                    if e.key()== QtCore.Qt.Key_F2:
                        say("------------F2-- show mode and moddata---------------")
                        say(self.node)
                        return False
                    elif e.key()== QtCore.Qt.Key_Escape:
                        say("------------Escape = Stop-AA----------------")
                        #self.node.selectedFaceChanged.call() 
                        #self.node.selectionExec.call()
                        self.t=[{'Object':"HUHU",'Component':"Face1"}]
                        self.snapList(0.002)
                        stop(self.node)

                    elif e.key()== QtCore.Qt.Key_F3 :
                        if not self.on:
                            say("------------F3 on-----------------")
                            self.on=True
                        return QtGui.QWidget.eventFilter(self, o, e)
                        return True
                    elif e.key()== QtCore.Qt.Key_F4 :
                        if self.on:
                            say("------------F4 off-----------------")
                            self.on=False
                        return QtGui.QWidget.eventFilter(self, o, e)
                        return True
                try:

                    
                    if  e.key()== QtCore.Qt.Key_F5 :
                        if self.displayObjects<time.time()-0.1:
                            clearReportView(name="dragger")
                            say("------------F5 display objectszero-----------------")
                            
                            if self.t != None:
                                for tt in self.t:
                                    say(tt)
                        self.displayObjects=time.time()    

                        return False
                    elif e.key()== QtCore.Qt.Key_F6 :
                        say("------------F6 none-----------------")
                        return False
                    elif  e.key()== QtCore.Qt.Key_Return:
                       say("------------Enter-----------------")
                    elif e.key() == QtCore.Qt.Key_Right :
                        say("Go right")
                        return True
                    elif e.key() == QtCore.Qt.Key_Left :
                        say("Go Left")
                        return True
                    elif e.key() == QtCore.Qt.Key_Up :
                        say("go up")
                        return True
                    elif e.key() == QtCore.Qt.Key_Down :
                        print "Go Down"
                        return True
#                    elif e.key() == QtCore.Qt.Key_PageUp :
#                    elif e.key() == QtCore.Qt.Key_PageDown :

                    if e.key()== QtCore.Qt.Key_Enter or e.key()== QtCore.Qt.Key_Return:
                        say("Enter Action-----------------------------")
                        return True
                    else: # letter key pressed
                        ee=e.text()
                        if len(ee)>0: r=ee[0]
                        else: r="key:"+ str(e.key())
                        self.lastkey=e.text()

                        # zooming +-*
                        if r=='+':
                            Gui.activeDocument().ActiveView.zoomIn()
                            return True
                        if r=='-':
                            Gui.activeDocument().ActiveView.zoomOut()
                            return True
                        if r=='*':
                            Gui.activeDocument().ActiveView.fitAll()
                            return True

                except:
                    sayexc()

        if 0 and event.type() == QtCore.QEvent.Wheel:
            numDegrees = event.delta() / 8
            numSteps = numDegrees / 15
            self.z -= numSteps
            self.snapList()
            return True

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if str(event.button()) == 'PySide.QtCore.Qt.MouseButton.LeftButton':
                self.LMpress=True

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.LMpress=False

        if event.type() == QtCore.QEvent.MouseMove:
                (x,y)=Gui.ActiveDocument.ActiveView.getCursorPos()
                t=Gui.ActiveDocument.ActiveView.getObjectsInfo((x,y))
                #say(time.time())
                if t <> None:
                    self.t=[]
                    for tt in t:
                        if not tt['Object'].startswith('ID') and  tt['Component'].startswith("Face"):
                            self.t +=[tt]
                    if len(self.t)>0:
                        self.snapList(0.002)

                    cursor=QtGui.QCursor()
                    p = cursor.pos()
                    if self.on:
                        
                        #say("Mouse pos",p.x(),p.y(),"Cursor pos in window",x,y)
                        self.ax=p.x()
                        self.ay=p.y()
                        self.x=x
                        self.y=y
                        pts=[FreeCAD.Vector(self.ax,self.ay),FreeCAD.Vector(),FreeCAD.Vector(self.x,self.y)]
                        shape=Part.makePolygon(pts)
                        #self.node.setPinObject("Shape_out",shape)
                        self.node.setData('positionApp',pts[0])
                        self.node.setData('positionWindow',pts[2])
                        
                        

                        
                        self.node.outExec.call()
                    
                    #self.snapList(0.02)

                # details siehe sculpter.py
                
                #-----------------------------
                return QtGui.QWidget.eventFilter(self, o, e)
                return True

        # end of a single key pressed
        if 0:
            if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
                self.lasttime=time.time()
                say("released")
                self.keyPressed2=False


            if z == 'PySide.QtCore.QEvent.Type.Enter' :
                say("enter")
            elif z == 'PySide.QtCore.QEvent.Type.Leave' :
                say("leave")

            if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
                say("hover")

        return QtGui.QWidget.eventFilter(self, o, e)




def start(self,*args, **kwargs):
    sayl()
    ef=EventFilter()
    ef.mouseWheel=0
    ef.node=self
    self.eventfilter=ef
    from PySide import QtGui,QtCore
    mw=QtGui.qApp
    mw.installEventFilter(ef)


def stop(self,*args, **kwargs):
    sayl()
    mw=QtGui.qApp
    ef=self.eventfilter
    mw.removeEventFilter(ef)


def compute(self,*args, **kwargs):
    sayl()
