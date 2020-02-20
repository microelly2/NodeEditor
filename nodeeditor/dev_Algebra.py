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

    
def run_FreeCAD_Expression(self):

    
    modules=self.getData('modules')
    modules=modules.split(',')
    for m in modules:
        if m=='': break
        exec("import "+m)

    expression=self.getData('expression')
    a=self.getData('a')
    b=self.getData('b')
    c=self.getData('c')
    d=self.getData('d')
    say(expression)
    if a is None:
        a=0.
    
    v=eval(expression)

    say("parameters a,b,c,d",a,b,c,d)
    say(expression,v,v.__class__)
    self.setData('string_out',str(v))
    try:
        self.setData('float_out',float(v))
        self.setData('int_out',int(round(v)))
    except: pass
    
    self.setData('bool_out',v)
    

