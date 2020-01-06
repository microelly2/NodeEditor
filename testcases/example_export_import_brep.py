
#cp_109

import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]
_FreeCAD_Export=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Export','FreeCAD_Export')
_FreeCAD_Export.setPosition(-132.0,-299.0)
gg.addNode(_FreeCAD_Export)

_FreeCAD_Import=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Import','FreeCAD_Import')
_FreeCAD_Import.setPosition(99.0,-299.0)
gg.addNode(_FreeCAD_Import)

_makeString=pfwrap.createFunction('PyFlowBase','DefaultLib','makeString')
_makeString.setPosition(-205.0,-146.0)
gg.addNode(_makeString)

_FreeCAD_VectorArray=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_VectorArray','FreeCAD_VectorArray')
_FreeCAD_VectorArray.setPosition(-365.0,-295.0)
gg.addNode(_FreeCAD_VectorArray)

_FreeCAD_View3D=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_View3D','FreeCAD_View3D')
_FreeCAD_View3D.setPosition(257.0,-299.0)
gg.addNode(_FreeCAD_View3D)

_makeString.setData('s','/tmp/aa.brep')
_FreeCAD_VectorArray.setData('countA',50)
_FreeCAD_VectorArray.setData('countB',50)
_FreeCAD_VectorArray.setData('randomZ',20)

pfwrap.connect(_FreeCAD_Export,'outExec',_FreeCAD_Import,'inExec')
pfwrap.connect(_FreeCAD_Import,'outExec',_FreeCAD_View3D,'inExec')
pfwrap.connect(_FreeCAD_Import,'Shape_out',_FreeCAD_View3D,'Shape_in')
pfwrap.connect(_makeString,'out',_FreeCAD_Import,'filename')
pfwrap.connect(_makeString,'out',_FreeCAD_Export,'filename')
pfwrap.connect(_FreeCAD_VectorArray,'outExec',_FreeCAD_Export,'inExec')
pfwrap.connect(_FreeCAD_VectorArray,'Shape_out',_FreeCAD_Export,'Shape')
nodeeditor.Commands.refresh_gui()
