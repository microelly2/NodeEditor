import nodeeditor
import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]

_strftime=pfwrap.createFunction('PyFlowFreeCAD','Datetime','strftime')
_strftime.setPosition(-32.0,-251.0)
gg.addNode(_strftime)

_time=pfwrap.createFunction('PyFlowFreeCAD','Datetime','time')
_time.setPosition(-264.0,-326.0)
gg.addNode(_time)

_now=pfwrap.createFunction('PyFlowFreeCAD','Datetime','now')
_now.setPosition(-328.0,-205.0)
gg.addNode(_now)


pfwrap.connect(_now,'out',_strftime,'timestamp')
nodeeditor.Commands.refresh_gui()
