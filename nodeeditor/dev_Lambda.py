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

from pivy import coin

print ("reloaded: "+ __file__)


from inspect import signature

def run_FreeCAD_Function(self):
    f=self.getPinObject('function')
    a=self.getData('a')
    b=self.getData('b')
    c=self.getData('c')
    
    from inspect import signature
    if f is not None:
        sig = str(signature(f))      
        args=eval(sig)

        if isinstance(args, tuple):
            rc=f(*args)   
        else:
            rc=f(args)   
           
        self.setData('result',rc)
    

    
    
def run_FreeCAD_Expression2Function(self):

    s=self.getData('expression')
    if s != '':
        cmd="lambda a,b,c:{}".format(s)
        say(cmd)
        cmd2=eval(cmd)
        self.setPinObject('function_out',cmd2)
    
    
def run_FreeCAD_ReduceFunction(self):
    f=self.getPinObject('function')

    a=self.getData('a')
    b=self.getData('b')
    c=self.getData('c')
    
    
    if f is not None:
        sig = str(signature(f))
        say(sig[1:-1].split(','))      
        
        say(f)
        say(sig)

        usa= self.getData('reduse_a')
        usb= self.getData('reduse_b')
        usc= self.getData('reduse_c')
        
        if usa:
            if usb:
                if usc:
                    ff4=lambda :f(a,b,c)
                else:
                    ff4=lambda b,c:f(a,b,c)
            else:
                if usc:
                    ff4=lambda b:f(a,b,c)
                else:
                    ff4=lambda b,c:f(a,b,c)
        else:
            if usb:
                if usc:
                    ff4=lambda a:f(a,b,c)
                else:
                    ff4=lambda a,c:f(a,b,c)
            else:
                if usc:
                    ff4=lambda a,b:f(a,b,c)
                else:
                    ff4=lambda a, b, c:f(a,b,c)

        
        self.setPinObject('function_out',ff4)
        self.setData('signature',signature(ff4))

    

    
    
def run_FreeCAD_Expression2Function(self):

    s=self.getData('expression')
    if s != '':
        cmd="lambda a,b,c:{}".format(s)
        say(cmd)
        cmd2=eval(cmd)
        self.setPinObject('function_out',cmd2)
    
    
def run_FreeCAD_SumDistances(self):
    
    def sumdist(target,points):
        target=FreeCAD.Vector(*target)
        return sum([(target-p).Length for p in points]) #/len(points)
        
    self.setPinObject('function_out',sumdist)







def run_FreeCAD_MinimizeFunction(self):
    
    f=self.getPinObject('function')
    
    
    from scipy import optimize
    
    def dist(x):
        target=FreeCAD.Vector(*x)
        return f(target)
        
    methods=[ 
            'Nelder-Mead' ,
            'Powell' ,
            'CG' ,
            'BFGS' ,
            'L-BFGS-B', 
            'TNC',
            'COBYLA',
            'SLSQP',
        ]

    methods=[ 'Nelder-Mead' ]
    #methods=['Powell']
    
    for method in methods:
        
        a=time.time()
        result = optimize.minimize(dist, x0=[0,0,0],  method=method)
        r=result.x[0]

        say("quality",np.round(result.fun,5),np.round(result.x,2),result.message,method)
        say("run time for scipy.optimize.minimum",method,round(time.time()-a,3))

    self.setData('position',FreeCAD.Vector(*result.x))
    self.setData('result',result.fun)




def run_FreeCAD_DemoFunction(self):
    
    def find_4_5(target):
        return (target[0]-4)**2+(target[1]-5)**2

    def find_root_of_2(target):
        x=target[0]
        return abs(x**2-2)

    example=self.getData('example')        
    ff=eval(example)
    
    self.setPinObject('function_out',ff)


from scipy import optimize
def run_FreeCAD_MinimizeFunction2(self):
    
    f=self.getPinObject('function')
    start=self.getData('start')
    method=self.getData('Method')
    say("start value(s)",start)
    if len(start)==0:
        start=[0]
        
    a=time.time()
    result = optimize.minimize(f, x0=start,  method=method)

    say("quality",np.round(result.fun,5),np.round(result.x,2),result.message,method)
    say("run time for scipy.optimize.minimum",method,round(time.time()-a,3))
    say(result.x)
    self.setData('result',np.round(result.x,7).tolist())
    self.setData('minimum',result.fun)




    
    
def run_FreeCAD_AssignPoints(self):
    
    points=self.getData('points')
    f=self.getPinObject('function')
#    say(signature(f))
    assert '(target, points)' == str(signature(f))
    FreeCAD.t=signature(f)
     
    
    red=lambda target: f(target,points)
    self.setPinObject('function_out',red)
