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


def flagstring(flags,lenf=10):
    '''create string form boolean list'''
    fstring=""
    for f in flags[:lenf]:
        fstring += "L" if f else "O"
    if lenf<len(flags):
        fstring += "..."
    return fstring

    
def run_FreeCAD_IfElse(self):
    self.setData('out',self.getData('flag'))
    self.outExec.call()
    if self.getData('flag'):
        self.ifExec.call()
    else:
        self.elseExec.call()
    


    


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
    threshold=self.getData("threshold")
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
    
