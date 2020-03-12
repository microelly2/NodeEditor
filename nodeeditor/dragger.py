
from nodeeditor.utils import *

import FreeCAD
import Part
import FreeCADGui as Gui
import sys,time
import random

from nodeeditor.say import *
from nodeeditor.Commands import clearReportView
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Object import timer

import PySide2
import Qt
from Qt import QtCore
from Qt import QtGui


class EventFilter(QtCore.QObject):
    '''Eventfilter for facedrawing'''

##\cond

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.on=False
        self.displayObjects=False
        self.t=[]
        self.z=0
        self.LMpress=False

    @timer
    def snapList(self,delta=0.04):
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
                    shape=getattr(obj.Shape, self.selcomponent)
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
        ''' 
        the eventfilter for the mouse sensor
        '''

        if e.type()== PySide2.QtCore.QEvent.Type.KeyPress:
                
                if e.key()== QtCore.Qt.Key_F2:
                    say("------------F2-- show mode and moddata---------------")
                    say(self.node)
                    #return False
                    return Qt.QtWidgets.QWidget.eventFilter(self, o, e)
                elif e.key()== QtCore.Qt.Key_Escape:
                    say("------------Escape = Stop-AA----------------")
                    self.t=[{'Object':"HUHU",'Component':"Face1"}]
                    self.snapList(0.002)
                    stop(self.node)

                elif e.key()== QtCore.Qt.Key_F3 :
                    if not self.on:
                        say("------------F3 on-----------------")
                        self.on=True
                    return Qt.QtWidgets.QWidget.eventFilter(self, o, e)
                elif e.key()== QtCore.Qt.Key_F4 :
                    if self.on:
                        say("------------F4 off-----------------")
                        self.on=False
                    return Qt.QtWidgets.QWidget.eventFilter(self, o, e)
                try:
                    if  e.key()== QtCore.Qt.Key_F5 :
                        if self.displayObjects<time.time()-0.1:
                            clearReportView(name="dragger")
                            say("------------F5 display objects under mouse-----------------")
                            if self.t != None:
                                for tt in self.t:
                                    say(tt)
                        self.displayObjects=time.time()    
                        return False
                    elif e.key() == QtCore.Qt.Key_Right :
                        cursor=QtGui.QCursor()
                        p = cursor.pos()
                        cursor.setPos(p.x()+1,p.y())
                        return True
                    elif e.key() == QtCore.Qt.Key_Left :
                        cursor=QtGui.QCursor()
                        p = cursor.pos()
                        cursor.setPos(p.x()-1,p.y())
                        return True
                    elif e.key() == QtCore.Qt.Key_Up :
                        cursor=QtGui.QCursor()
                        p = cursor.pos()
                        cursor.setPos(p.x(),p.y()-1)
                        return True
                    elif e.key() == QtCore.Qt.Key_Down :
                        cursor=QtGui.QCursor()
                        p = cursor.pos()
                        cursor.setPos(p.x(),p.y()+1)
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

        if 0 and e.type() == QtCore.QEvent.Wheel:
            numDegrees = e.delta() / 8
            numSteps = numDegrees / 15
            self.z -= numSteps
            self.snapList()
            return True

        if e.type() == QtCore.QEvent.MouseButtonPress:
            if str(e.button()) == 'PySide2.QtCore.Qt.MouseButton.LeftButton':
                self.LMpress=True

        if e.type() == QtCore.QEvent.MouseButtonRelease:
            self.LMpress=False

        if e.type() == QtCore.QEvent.MouseMove:
                (x,y)=Gui.ActiveDocument.ActiveView.getCursorPos()
                t=Gui.ActiveDocument.ActiveView.getObjectsInfo((x,y))
                if t  !=  None:
                    self.t=[]
                    for tt in t:
                        # ignore drawing objects=edges/vertexes - nur faces akzeptieren
                        if not tt['Object'].startswith('ID') and  tt['Component'].startswith("Face"):
                            self.t +=[tt]
                    if len(self.t)>0:
                        self.snapList(0.002)

                    cursor=QtGui.QCursor()
                    p = cursor.pos()
                    if self.on:
                        say("Mouse pos",p.x(),p.y(),"Cursor pos in window",x,y)
                        self.ax=p.x()
                        self.ay=p.y()
                        self.x=x
                        self.y=y
                        self.node.setData('positionApp',FreeCAD.Vector(self.ax,self.ay))
                        self.node.setData('positionWindow',FreeCAD.Vector(self.x,self.y))
                        self.node.outExec.call()
                    
                return Qt.QtWidgets.QWidget.eventFilter(self, o, e)

        return Qt.QtWidgets.QWidget.eventFilter(self, o, e)


def start(self,*args, **kwargs):
    ef=EventFilter()
#    ef.mouseWheel=0
    ef.node=self
    self.eventfilter=ef
    from PySide2 import QtGui
    QtGui.qApp.installEventFilter(ef)
    self.outExec.call()


def stop(self,*args, **kwargs):
    from PySide2 import QtGui
    ef=self.eventfilter
    QtGui.qApp.removeEventFilter(ef)
    self.outExec.call()


def compute(self,*args, **kwargs):
    self.outExec.call()
