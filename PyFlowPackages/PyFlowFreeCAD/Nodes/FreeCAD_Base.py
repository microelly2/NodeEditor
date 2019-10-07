# Base classes and methods for freecad nodes

import numpy as np
import random
import functools
import time
import inspect

from FreeCAD import Vector
import FreeCAD
import FreeCADGui
import Part


from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

import nodeeditor.store as store
from nodeeditor.say import *


import sys
if sys.version_info[0] !=2:
	from importlib import reload


# method only for get runtime
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        log=False
        try :
                is_method   = inspect.getargspec(func)[0][0] == 'self'
        except :
                is_method   = False
        if is_method :
                name    = '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else :
                name    = '{}.{}'.format(fn.__module__, func.__name__)
        if log: sayW("call '{}'".format(name))
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time    # 3
        if log: sayW("Finished method '{0}' in {1:.4f} secs".format(func.__name__,run_time))
        return value
    return wrapper_timer


def Xtimer(func):
    """print runtime of the function and create part for shape"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        try :
                is_method   = inspect.getargspec(func)[0][0] == 'self'
        except :
                is_method   = False
        
        if is_method :
                name    = '{}.{}.{}'.format(func.__module__, args[0].__class__.__name__, func.__name__)
        else :
                name    = '{}.{}'.format(fn.__module__, func.__name__)
        
        sayW("call with genPart'{}'".format(name))
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time    # 3
        
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_genPart(func,args,kwargs)
        
        sayW("Finished method '{0}' in {1:.4f} secs".format(func.__name__,run_time))
        return value
    return wrapper




class FreeCadNodeBase(NodeBase):
    '''common methods for FreeCAD integration'''
    
    dok = 0
    
    def __init__(self, name="FreeCADNode",**kvargs):
        
        super(FreeCadNodeBase, self).__init__(name)
        self._debug = False
    
    @timer
#    @genPart
    def compute(self, *args, **kwargs):
        if self._debug:
            say("debug on for ",self)
        import nodeeditor.dev
        reload (nodeeditor.dev)
        a=eval("nodeeditor.dev.run_{}(self)".format(self.__class__.__name__))
    
    
    def bake(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        a=eval("nodeeditor.dev.run_{}(self,bake=True)".format(self.__class__.__name__))
    
    def refresh(self, *args, **kwargs):
        self.compute(*args, **kwargs)
        
        
    def initpins(self,name):

        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Show = self.createInputPin('Show', 'ExecPin', None, self.show)
        
        self.trace = self.createInputPin('trace', 'BoolPin')
        self.randomize = self.createInputPin("randomize", 'BoolPin')
        
        self.part = self.createOutputPin('Part', 'FCobjPin')
        self.shapeout = self.createOutputPin('Shape', 'ShapePin','True')
        
        self.objname = self.createInputPin("objectname", 'StringPin')
        self.objname.setData(name)
        
        self.shapeOnly = self.createInputPin("shapeOnly", 'BoolPin', True)
        self.shapeOnly.recomputeNode=True
    
    
    @timer
#    @genPart
    def show(self,*args, **kwargs):
        sayl()
        #say("self:",self)
        say("Content of {}:".format(self.getName()))
        #say("list all pins !! siehe FreeCAD.ref")
        FreeCAD.tt=self
        ll=len(self.getName())
        #say("self.getOrderedPins()")
        #say( self.getOrderedPins())
        
        k=self.orderedInputs.values()
        say("INPINS")
        for t in k:
            say(t)
            say(t.getFullName(),t.getData())
        sayl()
        k=self.orderedOutputs.values()
        say("OUTPINS")
        for t in k:
            say(t)
            say(t.getFullName(),t.getData())
        sayl()
        
        FreeCAD.ref=self
        return
        
        for t in self.getOrderedPins():
            say("{} = {} ({})".format(t.getName()[ll+1:],t.getData(),t.__class__.__name__))
            if len(t.affected_by):
                for tt in t.affected_by:
                    if not tt.getName().startswith(self.getName()):
                        say("<---- {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
            
            if len(t.affects):
                for tt in t.affects:
                    if not tt.getName().startswith(self.getName()):
                        say("----> {} = {} ({})".format(tt.getName(),tt.getData(),tt.__class__.__name__))
            
            
            n=t.__class__.__name__
            # spezialausgaben fuer objekte
            if n == 'ArrayPin':
                say(t.getArray())
            if n == 'FCobjPin':
                obj=t.getObject()
                if obj  !=  None :
                    try:
                        say("object: {} ({})".format(obj.Label,obj.Name))
                    except:
                        say(obj)
        
        FreeCAD.ref=self
        
        
        
        
    def getDatalist(self,pinnames):
        namelist=pinnames.split()
        ll=[self.getPinN(a).getData() for a in namelist]
        return ll
        
    def applyPins(self,ff,zz):
        zz2=self.getDatalist(zz)
        return ff(*zz2)
        
    def setDatalist(self,pinnames,values):
        namelist=pinnames.split()
        sayl("--set pinlist for {}".format(self.getName()))
        for a,v in zip(namelist,values):
            say(a,v)
            self.getPinN(a).setData(v)
        
    def getObject(self):
        '''get the FreeCAD object'''
        
        
        yid="ID_"+str(self.uid)
        yid=yid.replace('-','_')
        
        cc=FreeCAD.ActiveDocument.getObject(yid)
        
        try:
            if self.shapeOnly.getData():
                if cc:
                    say("delete object")
                    FreeCAD.ActiveDocument.removeObject(cc.Name)
                return None
        except: pass
        
        if cc == None:
            cc=FreeCAD.ActiveDocument.addObject("Part::Feature",yid)
            cc.ViewObject.Transparency=80
            cc.ViewObject.LineColor=(1.,0.,0.)
            cc.ViewObject.PointColor=(1.,1.,0.)
            cc.ViewObject.PointSize=10
            r=random.random()
            cc.ViewObject.ShapeColor=(0.,0.2+0.8*r,1.0-0.8*r)
        return cc
        
    def postCompute(self,fcobj=None):
        
        if self.part.hasConnections():
            say("send a Part")
            if fcobj == None:
                self.part.setData(None)
            else:
                self.part.setData(fcobj.Name)
        self.outExec.call()
        try:
            if self.trace.getData():
                self.show()
        except:
            pass
        
    #method to write/read the objectpins
    def getPinObject(self,pinName):
        return store.store().get(self.getData(pinName))
        
        
    def getPinObjects(self,pinName):
        eids=self.getData(pinName)
        if eids == None:
            sayW("no data on pin",pinName)
            return []
        return [store.store().get(eid) for eid in eids]
        
    def setPinObjects(self,pinName,objects):
        pin=self.getPinN(pinName)
        ekeys=[]
        for i,e in enumerate(objects):
            k=str(pin.uid)+"__"+str(i)
            store.store().add(k,e)
            ekeys += [k]
        self.setData(pinName,ekeys)
        
    def setPinObject(self,pinName,obj):
        pin=self.getPinN(pinName)
        k=str(pin.uid)
        store.store().add(k,obj)
        pin.setData(k)
        
    def reset(self,*args, **kwargs):
        pass
        
    def refresh(self,*args, **kwargs):
        pass
        
    def funA(self,*args, **kwargs):
        sayl("function funA called")
        pass
        
    def funB(self,*args, **kwargs):
        sayl("function funB called")
        pass
        
    def funC(self,*args, **kwargs):
        sayl("function funC called")
        pass
        


# example shape
def createShape(a):
    
    pa=FreeCAD.Vector(0,0,0)
    pb=FreeCAD.Vector(a*50,0,0)
    pc=FreeCAD.Vector(0,50,0)
    shape=Part.makePolygon([pa,pb,pc,pa])
    return shape


def updatePart(name,shape):

    FreeCAD.Console.PrintError("update Shape for "+name+"\n")
    a=FreeCAD.ActiveDocument.getObject(name)
    if a== None:
        a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
    a.Shape=shape



def onBeforeChange_example(self,newData,*args, **kwargs):
    FreeCAD.Console.PrintError("before:"+str(self)+"\n")
    FreeCAD.Console.PrintError("data before:"+str(self.getData())+"-- > will change to:"+str(newData) +"\n")
    # do something like backup or checks before change here

def onChanged_example(self,*args, **kwargs):
    FreeCAD.Console.PrintError("Changed data to:"+str(self.getData()) +"\n")
    self.owningNode().reshape()




def nodelist():
    return [
#                FreeCAD_Bar,
#                FreeCAD_YYY,
    ]
