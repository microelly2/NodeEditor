
#####################################
import nodeeditor
import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]

_FreeCAD_VectorArray=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_VectorArray','FreeCAD_VectorArray')
_FreeCAD_VectorArray.setPosition(-313.0,-304.0)
gg.addNode(_FreeCAD_VectorArray)

#FreeCAD_VectorArray.setData(pinname,value)

_FreeCAD_Tripod=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Tripod','FreeCAD_Tripod')
_FreeCAD_Tripod.setPosition(-99.13197657830375,-389.74195706022357)
gg.addNode(_FreeCAD_Tripod)

#FreeCAD_Tripod.setData(pinname,value)

_FreeCAD_ShapePattern=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_ShapePattern','FreeCAD_ShapePattern')
_FreeCAD_ShapePattern.setPosition(299.0,-401.0)
gg.addNode(_FreeCAD_ShapePattern)

#FreeCAD_ShapePattern.setData(pinname,value)

_FreeCAD_Dragger=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Dragger','FreeCAD_Dragger')
_FreeCAD_Dragger.setPosition(342.8726233010518,-195.9047950601577)
gg.addNode(_FreeCAD_Dragger)

#FreeCAD_Dragger.setData(pinname,value)

_sequence=pfwrap.createNode('PyFlowBase','sequence','sequence')
_sequence.setPosition(103.3020351325444,-430.13788679513476)
gg.addNode(_sequence)

#sequence.setData(pinname,value)

_FreeCAD_ShapePattern4=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_ShapePattern','FreeCAD_ShapePattern4')
_FreeCAD_ShapePattern4.setPosition(501.0,-134.0)
gg.addNode(_FreeCAD_ShapePattern4)

#FreeCAD_ShapePattern4.setData(pinname,value)


pfwrap.connect(_FreeCAD_VectorArray,'Shape_out',_FreeCAD_Tripod,'Shape')
pfwrap.connect(_FreeCAD_Tripod,'outExec',_sequence,'inExec')
pfwrap.connect(_FreeCAD_Tripod,'poles',_FreeCAD_ShapePattern,'points')
pfwrap.connect(_FreeCAD_Tripod,'poles',_FreeCAD_Dragger,'points')
pfwrap.connect(_FreeCAD_Dragger,'outExec',_FreeCAD_ShapePattern4,'inExec')
pfwrap.connect(_FreeCAD_Dragger,'Points_out',_FreeCAD_ShapePattern4,'points')
pfwrap.connect(_sequence,'1',_FreeCAD_ShapePattern,'inExec')
pfwrap.connect(_sequence,'2',_FreeCAD_Dragger,'reset')
pfwrap.connect(_sequence,'3',_FreeCAD_Dragger,'start')
nodeeditor.Commands.refresh_gui()
