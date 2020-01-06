
# cp 110
import nodeeditor.pfwrap as pfwrap
instance=pfwrap.getInstance()
gg=pfwrap.getGraphManager().getAllGraphs()[0]
_FreeCAD_Expression=pfwrap.createNode('PyFlowFreeCAD','FreeCAD_Expression','FreeCAD_Expression')
_FreeCAD_Expression.setPosition(-11.0,-208.0)
gg.addNode(_FreeCAD_Expression)

_makeInt=pfwrap.createFunction('PyFlowBase','DefaultLib','makeInt')
_makeInt.setPosition(-201.0,-191.0)
gg.addNode(_makeInt)

_makeFloat=pfwrap.createFunction('PyFlowBase','DefaultLib','makeFloat')
_makeFloat.setPosition(-241.0,-129.0)
gg.addNode(_makeFloat)

_makeInt1=pfwrap.createFunction('PyFlowBase','DefaultLib','makeInt')
_makeInt1.setPosition(-238.0,-12.0)
gg.addNode(_makeInt1)


pfwrap.connect(_makeInt,'out',_FreeCAD_Expression,'a')
pfwrap.connect(_makeFloat,'out',_FreeCAD_Expression,'b')
pfwrap.connect(_makeFloat,'out',_FreeCAD_Expression,'c')
pfwrap.connect(_makeInt1,'out',_FreeCAD_Expression,'d')


_makeInt.setData('i',100)
_makeInt.setData('i',50)
_makeFloat.setData('f',10.10)

_FreeCAD_Expression.setData('modules','time')
_FreeCAD_Expression.setData('expression','time.time()*0+a+b*c+d')

_FreeCAD_Expression.compute()

assert _FreeCAD_Expression.getData('float_out') == 152.01

nodeeditor.Commands.refresh_gui()

