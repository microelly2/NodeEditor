'''
nodes for input devices like mouse, filesystem, network
'''

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *
from PyFlow.Packages.PyFlowFreeCAD.Nodes.FreeCAD_Base import timer, FreeCadNodeBase2, FreeCadNodeBase



class FreeCAD_Mouse(FreeCadNodeBase2):
    '''
    a Mouse Sensor
    '''


    def __init__(self, name="MouseSensor"):
       super(self.__class__, self).__init__(name)
#       self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.selectionExec = self.createOutputPin("SelectionChanged", 'ExecPin')
       self.createOutputPin('positionApp', 'VectorPin').description="position of the mouse in the Application window"
       self.createOutputPin('positionWindow', 'VectorPin').description="position of the mouse in the ActiveDocument window"
       #self.createOutputPin('Shape_out', 'ShapePin').description="Shape for illustration"
       self.createOutputPin('positionSelection', 'VectorPin').description="position on a selected component"
       
       self.createOutputPin('selectedFace', 'ShapePin')
       self.selectedFaceChanged = self.createOutputPin("selectedFaceChanged", 'ExecPin')
       self.createInputPin("zIndex", 'Integer')
       
       


    def start(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.start(self,*args, **kwargs)


    def stop(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.stop(self,*args, **kwargs)


    def compute(self, *args, **kwargs):

        import nodeeditor.dragger
        reload (nodeeditor.dragger)
        nodeeditor.dragger.compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Mouse.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['Mouse', 'Keyboard','Position' ]





class FreeCAD_Keyboard(FreeCadNodeBase2):
    '''
    a Keyboard Sensor
    '''


    def __init__(self, name="MouseSensor"):
       super(self.__class__, self).__init__(name)
       
       self.inExec = self.createInputPin("start", 'ExecPin', None, self.start)
       self.inExec = self.createInputPin("stop", 'ExecPin', None, self.stop)
       self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
       self.createOutputPin('key', 'StringPin')
       self.createOutputPin('count', 'IntPin')

       a=self.createInputPin("timeout", 'FloatPin',.2)
       a.annotationDescriptionDict={ "ValueRange":(0.01,2.)}
       
       self.createInputPin('stopEvent','BoolPin',False)
    
       


    def start(self, *args, **kwargs):

        import nodeeditor.keyboard
        reload (nodeeditor.keyboard)
        nodeeditor.keyboard.start(self,*args, **kwargs)


    def stop(self, *args, **kwargs):

        import nodeeditor.keyboard
        reload (nodeeditor.keyboard)
        nodeeditor.keyboard.stop(self,*args, **kwargs)


    def compute(self, *args, **kwargs):

        import nodeeditor.keyboard
        reload (nodeeditor.keyboard)
        nodeeditor.keyboard.compute(self,*args, **kwargs)

    @staticmethod
    def description():
        return FreeCAD_Keyboard.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['Mouse', 'Keyboard','Position' ]


class FreeCAD_ImportCSVFile(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('filename', 'String','/home/thomas/.FreeCAD/Mod.PyFlow/NodeEditor/testdata.csv')
        
        a=self.createInputPin('force', 'Boolean',True)
        a=self.createInputPin('separator', 'String',True)
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["space","tabulator","comma","semicolon"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("tabulator")

        
        
        a=self.createOutputPin('data', 'Float',structure=StructureType.Array)
        a=self.createOutputPin('points', 'VectorPin',structure=StructureType.Array)

    @staticmethod
    def category():
        return 'Sensor'
        
class FreeCAD_ImportAnyCSVFile(FreeCadNodeBase2):
    '''

    '''

    dok = 0
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('filename', 'String','/home/thomas/CORONA/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        
        a=self.createInputPin('force', 'Boolean',True)
        a=self.createInputPin('separator', 'String',True)
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":["space","tabulator","comma","semicolon"]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("comma")

        
        
        a=self.createOutputPin('data', 'StringPin',structure=StructureType.Array)

    @staticmethod
    def category():
        return 'Sensor'


class FreeCAD_Collect_Vectors(FreeCadNodeBase):
    '''
    collect vectors to a list
    '''

    dok=2 
    def __init__(self, name="MyCollection"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inReset = self.createInputPin("reset", 'ExecPin', None, self.reset)
        self.inReset.description="clear the list of collected points"
        self.inRefresh = self.createInputPin("refresh", 'ExecPin', None, self.refresh)
        self.inRefresh.description="update the outpin **points**"
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.pp=self.createInputPin('point', 'VectorPin')
        self.pp.description="list of collected vectors"
#        self.pp.enableOptions(PinOptions.AllowMultipleConnections)
#        self.pp.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createInputPin("maxSize",'Integer',100).\
        description="maximum length of the points list, if more points are gotten older points are dropped"
        self.createInputPin("reduce",'Integer',0).\
        description="create only a discretized list of the polygon with this size"

        a=self.createOutputPin('points', 'VectorPin', structure=StructureType.Array)
        a.description="list of collected vectors"
        
        self.points=[]

    @staticmethod
    def description():
        return FreeCAD_Collect_Vectors.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['point','collect']

    def reset(self,*args, **kwargs):
        say("reset")
        self.compute(mode="reset")

    @timer
    def reset(self, *args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="reset")


    def refresh(self,*args, **kwargs):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_FreeCAD_Collect_Vectors(self,mode="refresh")
        self.outExec.call()


class FreeCAD_Collect_Data(FreeCadNodeBase):
    '''
    collect data to a list
    '''

    dok=2 
    def __init__(self, name="MyCollection"):
        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inReset = self.createInputPin("reset", 'ExecPin', None, self.reset)
        self.inReset.description="clear the list "
        self.inRefresh = self.createInputPin("refresh", 'ExecPin', None, self.refresh)
        self.inRefresh.description="update the outpin **points**"
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        self.pp=self.createInputPin('data', 'AnyPin', constraint="1")
        self.pp.description="list of collected vectors"
#        self.pp.enableOptions(PinOptions.AllowMultipleConnections)
#        self.pp.disableOptions(PinOptions.SupportsOnlyArrays)

        self.createInputPin("maxSize",'Integer',100).\
        description="maximum length of the list, if more points are gotten older points are dropped"

        #a=self.createOutputPin('collection', 'StringPin', structure=StructureType.Array)
        a=self.createOutputPin('collection', 'AnyPin', structure=StructureType.Array,constraint="1")
        a.description="list of collected "
        
        self.points=[]

    @staticmethod
    def description():
        return FreeCAD_Collect_Data.__doc__

    @staticmethod
    def category():
        return 'Sensor'

    @staticmethod
    def keywords():
        return ['collect']


    def compute(self, *args, **kwargs):
        import nodeeditor.dev_all
        reload (nodeeditor.dev_all)
        nodeeditor.dev_all.run_FreeCAD_Collect_Data(self)

    def reset(self, *args, **kwargs):
        import nodeeditor.dev_all
        reload (nodeeditor.dev_all)
        nodeeditor.dev_all.run_FreeCAD_Collect_Data(self,mode="reset")


    def refresh(self,*args, **kwargs):
        import nodeeditor.dev_all
        reload (nodeeditor.dev_all)
        nodeeditor.dev_all.run_FreeCAD_Collect_Data(self,mode="refresh")
        self.outExec.call()





def nodelist():
    return [
                FreeCAD_Mouse,
                FreeCAD_Keyboard,
                
                FreeCAD_ImportCSVFile,
                FreeCAD_ImportAnyCSVFile,
                
                FreeCAD_Collect_Vectors,
                FreeCAD_Collect_Data,

    ]
