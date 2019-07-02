
'''python objects for freecad'''

# -*- coding: utf-8 -*-
#-- microelly 2017 v 0.1
#-- GNU Lesser General Public License (LGPL)


##\cond
import FreeCAD
import FreeCADGui
App = FreeCAD
Gui = FreeCADGui

import PySide

import Part
import numpy as np


class FeaturePython:
	''' basic defs'''

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj
		obj.addProperty("App::PropertyBool","_noExecute",'~aux')
		obj.addProperty("App::PropertyBool","_debug",'~aux')
		obj.addProperty("App::PropertyBool","_showaux",'~aux')


	def attach(self, vobj):
		print ("attached")
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None

	def showprops(self,obj,prop):
		if prop.startswith('_show'):
			mode= 0 if getattr(obj,prop) else 2
			for pn in obj.PropertiesList:
				if obj.getGroupOfProperty(pn).replace(' ','')==prop[5:] and pn<>prop:
					obj.setEditorMode(pn,mode)
				if obj.getGroupOfProperty(pn).startswith('~') and obj.getGroupOfProperty(pn).replace(' ','')[1:]==prop[5:] and pn<>prop:
					obj.setEditorMode(pn,mode)
			return

	def myOnChanged(self, fp, prop):
		pass

	def onChanged(self, fp, prop):
		try: a=fp._noExecute
		except: return
		if not fp._noExecute:
			self.myOnChanged(fp,prop)

	def onBeforeChange(self, fp, prop):
		pass

	def onDocumentRestored(self, fp):
		print ("Docu restored")
		for pn in fp.PropertiesList:
			if pn.startswith('_show'):
				self.onChanged(fp,pn)
		pass
		self.restored=True


	def myExecute(self,fp):
		pass

	def execute(self,fp):
		try: a=fp._noExecute
		except: return
		if not fp._noExecute:
			self.myExecute(fp)

	def run(self):
		print ("run test")

from nodeeditor.say import say

class ViewProvider:
	''' basic defs '''

	def __init__(self, obj,icon=None):
		obj.Proxy = self
		self.Object = obj.Object
		self.ViewObject = obj
		self.icon=icon
		if icon==None:
			icon= 'Nodeeditor/icons/BB.svg'
		if icon.startswith('/'): ic= self.icon
		else: ic= FreeCAD.ConfigGet("UserAppData") +'/Mod/' + icon 
		obj.addProperty("App::PropertyString",'icon').icon=ic
		say(ic)

#	def onDelete(self, obj, subelements):
#		return False

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None

	def attach(self, vobj):
		self.ViewObject = vobj
		self.Object = vobj.Object


	def getIcon(self):
		return self.Object.ViewObject.icon

	def claimChildren(self):
		s=self.Object
		rc=[]
		for prop in  s.PropertiesList:
			if s.getTypeIdOfProperty(prop) in ['App::PropertyLink']:
				v=s.getPropertyByName(prop)
				if v <>None:
					rc += [v]
			elif s.getTypeIdOfProperty(prop) in ['App::PropertyLinkList']:
				v=s.getPropertyByName(prop)
				if len(v) <> 0:
					rc += v
		return rc

	def recompute(self):
		obj=self.Object
		print "Recompute ",obj.Label
		obj.Proxy.myOnChanged(obj,"_recompute_")

	def setupContextMenu(self, obj, menu):
#		self.createDialog()

		action = menu.addAction("Recompute ...")
		action.triggered.connect(self.recompute)

#	def edit(self):
#		print "noimp"


	def setEdit(self,vobj,mode=0):
		#self.createDialog()
		print "huhu"
		try:
			self.edit()
#			print "ha 2"
		except:
			pass

		#FreeCAD.ActiveDocument.recompute()
#		print "hah"
#		print vobj
#		FreeCAD.v=vobj
		return True

	def run_later(self):
		self.ViewObject.show()

	def setEdit(self,vobj,mode=0):
		#self.createDialog()
		PySide.QtCore.QTimer.singleShot(100, self.run_later)
		raise Exception("Exception-Hack to start Editor")
#		return False
#		return True


##\endcond


