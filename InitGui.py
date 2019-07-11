#***************************************************************************
#*																		*
#*   Copyright (c) 2019													 *  
#*   <microelly2@freecadbuch.de>										 * 
#*																		 *
#*   This program is free software; you can redistribute it and/or modify*
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	*
#*   the License, or (at your option) any later version.				*
#*   for detail see the LICENCE text file.								*
#*																		*
#*   This program is distributed in the hope that it will be useful,	*
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		*
#*   GNU Library General Public License for more details.				*
#*																		*
#*   You should have received a copy of the GNU Library General Public	*
#*   License along with this program; if not, write to the Free Software*
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#*   USA																*
#*																		*
#************************************************************************

__title__="FreeCAD PyFlow"

__url__ = "http://www.freecadbuch.de"
__vers__ ="0.01"

import nodeeditor


import os
import re
global __dir__
__dir__ = os.path.dirname(nodeeditor.__file__)

import sys

if sys.version_info[0] !=2:
	from importlib import reload


import FreeCAD, FreeCADGui

windowCreated = 0

try:
	import cv2
except:
	FreeCAD.Console.PrintWarning("PyFlow WB: Cannot import module named cv2\n")



FreeCAD.tcmdsPyFlow = []

def always():
	''' always'''
	return True

def ondocument():
	'''if a document is active'''
	return FreeCADGui.ActiveDocument is not None

def onselection():
	'''if at least one object is selected'''
	return len(FreeCADGui.Selection.getSelection())>0

def onselection1():
	'''if exactly one object is selected'''
	return len(FreeCADGui.Selection.getSelection())==1

def onselection2():
	'''if exactly two objects are selected'''
	return len(FreeCADGui.Selection.getSelection())==2

def onselection3():
	'''if exactly three objects are selected'''
	return len(FreeCADGui.Selection.getSelection())==3

def onselex():
	'''if at least one subobject is selected'''
	return len(FreeCADGui.Selection.getSelectionEx())!=0

def onselex1():
	'''if exactly one subobject is selected'''
	return len(FreeCADGui.Selection.getSelectionEx())==1


global _Command2

class _Command2():

	def __init__(self, lib=None, name=None, icon=None, command=None, modul='nodeeditor',tooltip='No Tooltip'):


		if lib == None:
			lmod = modul
		else:
			lmod = modul + '.' + lib
		if command == None:
			command = lmod + ".run()"
		else:
			command = lmod + "." + command

		self.lmod = lmod
		self.command = command
		self.modul = modul
		if icon != None:
			self.icon = __dir__ + icon
		else:
			self.icon = None

		if name == None:
			name = command
		self.name = name
		self.tooltip=tooltip

	def GetResources(self):
		if self.icon != None:
			return {'Pixmap': self.icon,
					'MenuText': self.name,
					'ToolTip': self.tooltip,
					'CmdType': "ForEdit"  # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
					}
		else:
			return {
				#'Pixmap' : self.icon,
				'MenuText': self.name,
				'ToolTip': self.name,
				'CmdType': "ForEdit"  # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
			}

	def IsActive(self):
		if Gui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):

		import re
		ta=False
		if ta:
			FreeCAD.ActiveDocument.openTransaction(self.name)
		if self.command != '':
			if self.modul != '':
				modul = self.modul
			else:
				modul = self.name
			Gui.doCommand("import " + modul)
			Gui.doCommand("import " + self.lmod)
			Gui.doCommand("reload(" + self.lmod+")")
			Gui.doCommand(self.command)
		if ta:
			FreeCAD.ActiveDocument.commitTransaction()
		if FreeCAD.ActiveDocument != None:
			FreeCAD.ActiveDocument.recompute()



def c3bI(menu, isactive, name, text, icon='None', cmd=None, tooltip='',*info):

	import re
	global _Command2
	if cmd == None:
		cmd = re.sub(r' ', '', text) + '()'
	if name == 0:
		name = re.sub(r' ', '', text)
	if icon=='None':
		pic=re.sub(r' ', '', text)
		icon='/../icons/'+pic+'.svg'

	if tooltip=='':
		tooltip=name
	t = _Command2(name, text, icon, cmd, tooltip=tooltip,*info)
	title = re.sub(r' ', '', text)
	name1 = "Micro_" + title
	t.IsActive = isactive
	Gui.addCommand(name1, t)
	FreeCAD.tcmdsPyFlow.append([menu, name1])
	return name1



if FreeCAD.GuiUp:

	tools=[]

	current=[]
	_current=[]

	current += [c3bI(["nodeeditor"], always, 'Commands', 'shutdown',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'test_AA',icon="/../icons/AA")]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'test_BB',icon="/../icons/BB")]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'test_CC',icon="/../icons/CC")]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'test_DD',icon="/../icons/DD")]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'reset',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'T1',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'T2',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'T3',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'hide PyFlow',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'show PyFlow',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'save Graph',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'load Graph',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'clear Graph',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'load File',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'unload modules',icon=None)]
	current += [c3bI(["nodeeditor"], always, 'Commands', 'PyFlowtoDockWidget',icon=None)]


	toolbars = [
				['Tools', tools],
				['My current Work', current]
			]





class PyFlow ( Workbench ):

	MenuText = "PyFlow"
	#ToolTip = "Openstreetmap data"

	def GetClassName(self):
		return "Gui::PythonWorkbench"

	def __init__(self, toolbars, version):

		self.toolbars = toolbars
		self.version = version


	def Initialize(self):

		# create menues
		menues = {}
		ml = []
		for _t in FreeCAD.tcmdsPyFlow:
			c = _t[0]
			a = _t[1]
			try:
				menues[tuple(c)].append(a)

			except:
				menues[tuple(c)] = [a]
				ml.append(tuple(c))

		for m in ml:
			self.appendMenu(list(m), menues[m])

		for t in self.toolbars:
				self.appendToolbar(t[0], t[1])


	Icon= '''
/* XPM */
static char * nurbs_xpm[] = {
"16 16 2 1",
".	c #FF0FFF",
"+	c #00FF00",
"................",
"....+...........",
".....+..........",
".....+..........",
".....+...+++++..",
"......+..+++++..",
".....+++++++++..",
".........+++++..",
"..+......+++++..",
"..++++...+++++..",
"................",
"................",
"..++++++++++++..",
"..+++++++++++...",
"..+++++++++.....",
"................"};'''



FreeCADGui.addWorkbench(PyFlow(toolbars, __vers__))

