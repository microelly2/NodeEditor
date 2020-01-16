import nodeeditor
import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]

_FreeCAD_VectorArray=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_VectorArray','FreeCAD_VectorArray')
_FreeCAD_VectorArray.setPosition(-228.6921223730601,-215.2858684530729)
gg.addNode(_FreeCAD_VectorArray)

#FreeCAD_VectorArray.setData(pinname,value)

_FreeCAD_QuadMesh=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_QuadMesh','FreeCAD_QuadMesh')
_FreeCAD_QuadMesh.setPosition(-88.19496953179734,-92.19081735231327)
gg.addNode(_FreeCAD_QuadMesh)

#FreeCAD_QuadMesh.setData(pinname,value)

_FreeCAD_View3D=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_View3D','FreeCAD_View3D')
_FreeCAD_View3D.setPosition(-76.51980075617351,-259.0598351580601)
gg.addNode(_FreeCAD_View3D)

#FreeCAD_View3D.setData(pinname,value)


pfwrap.connect(_FreeCAD_VectorArray,'Shape_out',_FreeCAD_View3D,'Shape_in')
pfwrap.connect(_FreeCAD_VectorArray,'vectors_out',_FreeCAD_QuadMesh,'points')
nodeeditor.Commands.refresh_gui()
