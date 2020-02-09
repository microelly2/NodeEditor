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





def run_FreeCAD_Blinker(self):

    from blinker import signal
    try:
        sn=self.getData('signalName')
        ss= self.name +"@PyFlow"
    except:
        sn=self.Object.signalName
        ss=self.name +")@FreeCAD"

    from threading import Thread


    def sleeper(i):
        
        anz=0
        for j in range(1000):
            send_data = signal(sn)
            say("###",i,j,self.getData("sleep"),time.time())
            #say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            #say( "%r signal feedbacks:" %self.name)
            #for r in result:
            #    say(r[1])

        
            time.sleep(1+0.02*random.random())
            if self.getData("sleep") ==0:
                say("ENDE",i)
                return
        say("NDE ALL",i)

    def sleeper2(i):
            sleeper2a(i)



    def sleeper2a(i):
        a=time.time()
        say("start  outExec.call",i)
        say('##example set color')
        say("Ende call ",i,time.time()-a)


    def looper(j):
        try:
            j=self.getData("loops")
        except:
            return
        say("################# vSTART Looper",j)
        for i in range(j):
            if self.stopped:
                say("stopped")
                return
            send_data = signal(sn)
            say("###",i,j,self.getData("sleep"),time.time())
            say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            say( "%r signal feedbacks:" %self.name)
            for r in result:
                say(r[1])

            if self.getData("sleep") ==0:
                say("ENDE blinker calls at iteration",i)
                return
            t = Thread(target=sleeper2, args=(i,))
            t.start()
            time.sleep(self.getData("sleep")*0.1) 


        say("###             END Looper",j)

    a=time.time()
    self.stopped=False
    t2 = Thread(target=looper, args=(10,))
    t2.start()
    say("startf")
    #t2._stop();  say("stoppedAA")
    FreeCAD.t2=t2

    say("-----------------------------------Ende main",time.time()-a)

    def hu():
        for i in range(3):
            send_data = signal(sn)
            say()
            say("%r sends signal %r to receivers ..." %(ss,sn))
            result = send_data.send(self.name, message=self.getData("signalMessage"),obj=self.getData("signalObject"))
            say( "%r signal feedbacks:" %self.name)
            for r in result:
                say(r[1])
            tsleep=self.getData('sleep')
            if tsleep == 0:
                say("no loop")
                return
            else:
                say("sleep...",0.2)
                time.sleep(tsleep)
                say(i,"wake on!!")

def run_FreeCAD_Receiver(self):

    try:
        say("Data:",self.kw)
        say("Sender:",self.sender)
    except:
        say("no sender data and name avaiable")
    #self.setData("signalName",self.sender)
    #self.setData("senderMessage",self.kw['message'])
    self.setColor(b=0,a=0.4)
    




def myExecute_Receiver(proxy,fp):
    proxy.name=fp.Name
    run_FreeCAD_Receiver(proxy)

def myExecute_Blinker(proxy,fp):
    proxy.name=fp.Name
    run_FreeCAD_Blinker(proxy)

def f(x):
        return x*x


def run_FreeCAD_Async(self):
    #say(self.name)
    #sayl()
    #anz=0
    maxanz=15
    obj=self

    self.setData("message",self.name+" start")

    self.setData("message","")

    from threading import Thread

    def sleeper(i):
        
        anz=0
        for j in range(56):
            tt=random.randint(1,4)*2+1
     #       tt=2
            #print (self.name," %d loops for %f " % (j,tt))
            #print(obj)
            for zz in range(tt):
                anz += 1
                time.sleep(0.28)
                lll=0
                for k in range(100):
                    for kk in range(1000):
                        lll +=1
                #print (self.name,anz)
            
            #print ("thread %d woke up" % i)
            self.setData("message",self.name+"-----"+str(anz))
            obj.outExec.call()

            if anz>maxanz:
                break
            
        print ("-------------------Ende",self.name,anz,maxanz)
        self.setData("message",self.name+"  ENDE")
    

    for i in range(1):
        t = Thread(target=sleeper, args=(i,))
        t.start()
    

