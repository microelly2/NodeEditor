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


class EnumerationInputWidget(InputWidgetSingle):
    """
    String list selection input widget
    """

    def __init__(self, parent=None, **kwds):
        super(EnumerationInputWidget, self).__init__(parent=parent, **kwds)

        self.le = QComboBox(self)
        self.setWidget(self.le)
        self.le.currentIndexChanged.connect(lambda:self.dataSetCallback(self.le.currentText()))


    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        try:
            ix=self.pin._rawPin.values.index(val)
        except:
            ix=0
        self.le.setCurrentIndex(ix)

    def runpin(self):
        '''set data from sel.pin._rawPin'''
        d=self.pin._rawPin._data
        for i,item in enumerate(self.pin._rawPin.values):
            self.le.addItem(item)
        try:
            ix=self.pin._rawPin.values.index(d)
        except:
            ix=0
        self.le.setCurrentIndex(ix)
        sayl("call dev.run_enum")
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_enum(self)



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


from PyFlow.Packages.PyFlowBase.Factories.PinInputWidgetFactory import *


def getInputWidget(dataType, dataSetter, defaultValue, widgetVariant=DEFAULT_WIDGET_VARIANT,  **kwds):
    '''
    factory method
    '''
    say("widgetvariant",widgetVariant,dataType)
    if dataType == 'FloatPin':
        say("float pin")
        if widgetVariant == "Simple2":
            say("simple2 gefunden")
            return FloatInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if widgetVariant == "Slider":
            return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if widgetVariant == "Simple":
            return FloatInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        if kwds is not None and "pinAnnotations" in kwds:
            if kwds["pinAnnotations"] is not None and "ValueRange" in kwds["pinAnnotations"]:
                return FloatInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        return FloatInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)






    if dataType == 'IntPin':

        if kwds is not None and "pinAnnotations" in kwds:
            if kwds["pinAnnotations"] is not None and "ValueRange" in kwds["pinAnnotations"]:
                return IntInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)

        return IntInputWidgetSimple(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)


    if dataType == 'IntPin':
        say("input variant for freecad int pin ",widgetVariant)
        if widgetVariant == "HUHU":
            return MyInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue, **kwds)
    if dataType == 'VectorPin':
        return VectorInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'RotationPin':
        return RotationInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'PlacementPin':
        return PlacementInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'ArrayPin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'FCobjPin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'ShapePin':
        return ArrayInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    if dataType == 'EnumerationPin':
        return EnumerationInputWidget(dataSetCallback=dataSetter, defaultValue=defaultValue,  **kwds)
    return None
