import weakref
import FreeCAD


from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Widgets.InputWidgets import *

from PyFlow.UI.Widgets.QtSliders import pyf_Slider

from Qt import QtWidgets
from Qt import QtCore
from Qt.QtWidgets import *


FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 5


import numpy as np
from nodeeditor.say import *

from PyFlow.Packages.PyFlowFreeCAD.Nodes import *


class Array(object):
    def __init__(self,dat=[]):
        self.dat=np.array(dat)

class VectorInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(VectorInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return FreeCAD.Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.x)
        self.dsbY.setValue(val.y)
        self.dsbZ.setValue(val.z)

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(VectorInputWidget, self).resizeEvent(event)


class RotationInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(RotationInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.dsbA = pyf_Slider(self, "float", style=0, name="angle")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)
        self.layout().addWidget(self.dsbA)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
         return FreeCAD.Rotation()
#        return FreeCAD.Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        self.dsbX.setValue(val.Axis.x)
        self.dsbY.setValue(val.Axis.y)
        self.dsbZ.setValue(val.Axis.z)


    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(RotationInputWidget, self).resizeEvent(event)


class PlacementInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(PlacementInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        return
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return FreeCAD.Placement()
        #Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        #self.dsbX.setValue(val.x)
        #self.dsbY.setValue(val.y)
        #self.dsbZ.setValue(val.z)
        pass

    def resizeEvent(self, event):
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(PlacementInputWidget, self).resizeEvent(event)


class ArrayInputWidget(InputWidgetRaw):
    """Vector3 data input widget"""

    def __init__(self, **kwds):
        super(ArrayInputWidget, self).__init__(**kwds)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(1)
        return
        self.dsbX = pyf_Slider(self, "float", style=0, name="x")
        self.dsbY = pyf_Slider(self, "float", style=0, name="y")
        self.dsbZ = pyf_Slider(self, "float", style=0, name="z")
        self.layout().addWidget(self.dsbX)
        self.layout().addWidget(self.dsbY)
        self.layout().addWidget(self.dsbZ)

        self._configSpinBoxes()
        self.dsbX.valueChanged.connect(self._onDataChangedX)
        self.dsbY.valueChanged.connect(self._onDataChangedY)
        self.dsbZ.valueChanged.connect(self._onDataChangedZ)

    def blockWidgetSignals(self, bLocked):
        try:
            for w in [self.dsbX, self.dsbY, self.dsbZ]:
                w.blockSignals(bLocked)
        except:
            pass

    def asDataTypeClass(self):
        return Array()
        #Vector([self.dsbX.value(), self.dsbY.value(), self.dsbZ.value()])

    def _configSpinBoxes(self):
        for x in [self.dsbX, self.dsbY, self.dsbZ]:
            x.setDecimals(FLOAT_DECIMALS)
            x.setRange(FLOAT_RANGE_MIN, FLOAT_RANGE_MAX)
            x.setSingleStep(FLOAT_SINGLE_STEP)
            x.setDisplayMinimun(0)
            x.setDisplayMaximum(10)

    def _onDataChangedX(self, val):
        v = self.asDataTypeClass()
        v.x = val
        self.dataSetCallback(v)

    def _onDataChangedY(self, val):
        v = self.asDataTypeClass()
        v.y = val
        self.dataSetCallback(v)

    def _onDataChangedZ(self, val):
        v = self.asDataTypeClass()
        v.z = val
        self.dataSetCallback(v)

    def setWidgetValue(self, val):
        #self.dsbX.setValue(val.x)
        #self.dsbY.setValue(val.y)
        #self.dsbZ.setValue(val.z)
        pass

    def XresizeEvent(self, event):
        
        if self.width() < 260:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.hideSlider()
                x.hideLabel()
        else:
            for x in [self.dsbX, self.dsbY, self.dsbZ]:
                x.showSlider()
                x.showLabel()
        super(ArrayInputWidget, self).resizeEvent(event)

    def resizeEvent(self, event):
        super(ArrayInputWidget, self).resizeEvent(event)


class MyInputWidget(InputWidgetSingle):
    """
    String data input widget
    """

    def __init__(self, parent=None, **kwds):
        super(MyInputWidget, self).__init__(parent=parent, **kwds)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))
        self.le.setEnabled(False)

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val))


# alter slider funtionalitaet
class FloatInputWidgetSimpleSlider(InputWidgetSingle):
    """
    Floating point data input widget
    """

    def __init__(self, parent=None, **kwds):
        super(FloatInputWidgetSimpleSlider, self).__init__(parent=parent, **kwds)

        self.sb = pyf_Slider(self, "float", style=0)
        self.setWidget(self.sb)
        # when spin box updated call setter function
        self.sb.valueChanged.connect(lambda val: self.dataSetCallback(val))


    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(float(val))

    def setMaximum(self, max):
        self.sb.setMaximum(max)

    def setMinimum(self, min):
        self.sb.setMinimum(min)





class IntInputWidgetSimpleSlider(InputWidgetSingle):
    """
    Decimal number input widget
    """

    def __init__(self, parent=None, **kwds):
        super(IntInputWidgetSimpleSlider, self).__init__(parent=parent, **kwds)
        valueRange = (INT_RANGE_MIN, INT_RANGE_MAX)
        self.sb = pyf_Slider(self, "int", style=1)
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))



from PyFlow.Packages.PyFlowBase.Factories.PinInputWidgetFactory import *


class MyNoWidget(InputWidgetSingle):
    """
    """

    def __init__(self, parent=None, **kwds):
        super(self.__class__, self).__init__(parent=parent, **kwds)
        #self.le = QLineEdit(self)
        self.le = QLabel(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        #self.le.textChanged.connect(lambda val: self.dataSetCallback(val))
        self.le.setEnabled(False)

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val)[:40])



class IntInputWidgetSlider2(InputWidgetSingle):
    """
    Decimal number slider input widget
    """

    def __init__(self, parent=None, **kwds):
        super(self.__class__, self).__init__(parent=parent, **kwds)
        valueRange = [-100,100]
        draggerSteps=INT_SLIDER_DRAG_STEPS

        if "pinAnnotations" in kwds and kwds["pinAnnotations"] is not None:
            say("!X!", kwds["pinAnnotations"])
            if "ValueRange" in kwds["pinAnnotations"]:
                valueRange = kwds["pinAnnotations"]["ValueRange"]
            if "DraggerSteps" in kwds["pinAnnotations"]:
                draggerSteps= kwds["pinAnnotations"]["DraggerSteps"]
                
        say(valueRange)
        say(draggerSteps)
        # def __init__(self, parent=None, draggerSteps=draggerSteps, sliderRange=[-100, 100], *args, **kwargs):                
        self.sb = slider(self,draggerSteps=draggerSteps,sliderRange=valueRange) 
        self.setWidget(self.sb)
        self.sb.valueChanged.connect(self.dataSetCallback)

    def blockWidgetSignals(self, bLocked):
        self.sb.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.sb.setValue(int(val))



def getInputWidget(dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT,  **kwds):
    '''
    factory method
    '''
    #say("widgetvariant",widgetVariant,dataType)
    if widgetVariant == "NO":
        return MyNoWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    
    if dataType == 'StringPin' or dataType=='String':
        if widgetVariant == DEFAULT_WIDGET_VARIANT:
            return StringInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "PathWidget":
            return PathInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "EnumWidget":
            return EnumInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        elif widgetVariant == "ObjectPathWIdget":
            return ObjectPathWIdget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'BoolPin' or dataType=='Boolean':
        return BoolInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

     
    
    if dataType == 'FloatPin' or dataType == 'Float':
        say("FreeCAD -- float pin", widgetVariant)

        if widgetVariant == "Simple2":
            return FloatInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if widgetVariant == "Slider":
            return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if widgetVariant == "Simple":
            return FloatInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if kwds is not None and "pinAnnotations" in kwds:
            if kwds["pinAnnotations"] is not None and "ValueRange" in kwds["pinAnnotations"]:
                return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        
        return FloatInputWidgetSimpleSlider(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)


    if dataType == 'IntPin' or dataType == 'Integer':
        sayl('integer pin in FreeCAD')
        say("widgetvariant",widgetVariant,dataType)
        
        
        if widgetVariant == "Slider":
            return IntInputWidgetSlider2(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
        if widgetVariant == "Simple":
            return IntInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if kwds is not None and "pinAnnotations" in kwds:
            if kwds["pinAnnotations"] is not None and "ValueRange" in kwds["pinAnnotations"]:
                return IntInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

#        if widgetVariant == "EnumWidget":
#            return MyInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        return IntInputWidgetSimpleSlider(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

    if dataType == 'VectorPin':
        
        return VectorInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'RotationPin':
        return None
        #+# todo
        #return RotationInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'PlacementPin':
        return None
        #+# todo
        #return PlacementInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'ArrayPin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    #if dataType == 'FCobjPin':
    #    return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    #if dataType == 'ShapePin':
    #    return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    return None
