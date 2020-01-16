
#####################################
import nodeeditor
import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]

_FreeCAD_ImportFile=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_ImportFile','FreeCAD_ImportFile')
_FreeCAD_ImportFile.setPosition(-463.0,-97.0)
gg.addNode(_FreeCAD_ImportFile)

_FreeCAD_Elevation=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Elevation','FreeCAD_Elevation')
_FreeCAD_Elevation.setPosition(-292.0,-209.0)
gg.addNode(_FreeCAD_Elevation)

_FreeCAD_BSplineSurface=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_BSplineSurface','FreeCAD_BSplineSurface')
_FreeCAD_BSplineSurface.setPosition(-77.0,-244.0)
gg.addNode(_FreeCAD_BSplineSurface)

_FreeCAD_Polygon=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Polygon','FreeCAD_Polygon')
_FreeCAD_Polygon.setPosition(-266.0,12.0)
gg.addNode(_FreeCAD_Polygon)


pfwrap.connect(_FreeCAD_ImportFile,'points',_FreeCAD_Polygon,'points')
pfwrap.connect(_FreeCAD_ImportFile,'points',_FreeCAD_Elevation,'points')
pfwrap.connect(_FreeCAD_Elevation,'outExec',_FreeCAD_BSplineSurface,'inExec')
pfwrap.connect(_FreeCAD_Elevation,'poles',_FreeCAD_BSplineSurface,'poles')
nodeeditor.Commands.refresh_gui()
