'''
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
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2


class FreeCAD_Blinker(FreeCadNodeBase2):
    '''
    blinker sender
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.signal=self.createInputPin('signalName', 'StringPin', 'blink')
        self.data=self.createInputPin('signalMessage', 'StringPin')
        self.d3=self.createInputPin('signalObject', 'FCobjPin')
        a=self.createInputPin('sleep', 'FloatPin',10)
        a.annotationDescriptionDict={ "ValueRange":(0.,300.)}

        a=self.createInputPin('loops', 'IntPin',1)
        a.annotationDescriptionDict={ "ValueRange":(0.,100.)}


    @staticmethod
    def description():
        return FreeCAD_Blinker.__doc__

    @staticmethod
    def category():
        return 'Signal'

    @staticmethod
    def keywords():
        return ['Sender']
    
    def stop(self, *args, **kwargs):
        self.stopped=True


class FreeCAD_Receiver(FreeCadNodeBase2):
    '''
    blinker receiver
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inExec = self.createInputPin('subscribe', 'ExecPin', None, self.subscribe)
        self.inExec = self.createInputPin('unsubscribe', 'ExecPin', None, self.unsubscribe)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.signal=self.createInputPin('signalName', 'StringPin', 'blink')
        self.createOutputPin('senderName', 'StringPin')
        self.createOutputPin('senderMessage', 'StringPin')
        self.createOutputPin('senderObject', 'FCobjPin')
        self.signal=self.createInputPin('autoSubscribe', 'BoolPin', False)

        
    def subscribe(self, *args, **kwargs):
        sayl()
        from blinker import signal
        sn=self.getData('signalName')

        send_data = signal(sn)
        @send_data.connect
        def receive_data(sender, **kw):
            print("%r: caught signal from %r, data %r" % (self.name,sender, kw))
            print ("SENDER",sender)
            
            try:
                self.sender = sender
                self.kw = kw
            except:
                print("PROBLEME mit sendern")
                return
            
            self.setData("senderName",sender)
            self.setData("senderMessage",self.kw['message'])
            self.setData("senderObject",self.kw['obj'])
            self.setColor(b=0,a=0.4)
            self.outExec.call()
            
            return ("got return from  "+ self.name)
            
        self.r=receive_data
        
    def unsubscribe(self, *args, **kwargs):
        from blinker import signal
        sn=self.getData('signalName')
        send_data = signal(sn)
        send_data.disconnect(self.r)
        sayl()

        self.r=None
        self.sender = None
        self.kw = None


    def postCreate(self, jsonTemplate=None):
        super(self.__class__, self).postCreate(jsonTemplate=jsonTemplate)
        say("postcreate")
        if self.getData("autoSubscribe"):
            self.subscribe()



    @staticmethod
    def description():
        return FreeCAD_Receiver.__doc__

    @staticmethod
    def category():
        return 'Signal'

    @staticmethod
    def keywords():
        return ['Receiver']


class FreeCAD_Async(FreeCadNodeBase2):
    '''
    
    '''

    dok = 2
    def __init__(self, name="baked",**kvargs):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.signal=self.createInputPin('step', 'FloatPin', 2)
        self.signal=self.createOutputPin('message', 'StringPin')


    @staticmethod
    def description():
        return FreeCAD_Async.__doc__

    @staticmethod
    def category():
        return 'Signal'

    @staticmethod
    def keywords():
        return ['Receiver']





def nodelist():
    return [
                
                FreeCAD_Blinker,
                FreeCAD_Receiver,
                #FreeCAD_Async, #wozu??

        ]
