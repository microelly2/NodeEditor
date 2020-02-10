
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
        self.released=0
        self.count=0




    def eventFilter(self, o, e):
        ''' 
        the eventfilter for the keyboard
        '''

        if e.type()== PySide2.QtCore.QEvent.Type.KeyRelease:
            if time.time()- self.released >self.node.getData('timeout'):
                say()
                if self.count>0:
                    say("Key relesse",self.node.name,self.count,e.text(),time.time())
                    self.node.setData('key',e.text())
                    self.node.setData('count',self.count)
                    self.node.outExec.call()
                    self.node.setColor()

                self.released=time.time()
                self.count +=1
            if not self.node.getData('stopEvent'):
                return Qt.QtWidgets.QWidget.eventFilter(self, o, e)
            else:
                return True
        
        if e.type()== PySide2.QtCore.QEvent.Type.KeyPress:
            if time.time()- self.released  >self.node.getData('timeout'):
                self.count =0
                say()
                say("Key pressed",self.node.name,self.count,time.time())

                self.node.setData('key',e.text())
                self.node.setData('count',self.count)
                self.node.outExec.call()
                self.node.setColor()
            
                self.released=time.time()

            if not self.node.getData('stopEvent'):
                return Qt.QtWidgets.QWidget.eventFilter(self, o, e)
            else:
                return True

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
