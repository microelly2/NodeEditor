# store pointers to objects
from nodeeditor.say import *
import FreeCAD
class store():

	def add(self,key, obj):
		try:
			FreeCAD.STORE
		except:
			FreeCAD.STORE={}
		FreeCAD.STORE[str(key)]=obj

	def addid(self, obj):
		try:
			FreeCAD.STORE
		except:
			FreeCAD.STORE={}
		FreeCAD.STORE[str(id(obj))]=obj

	def get(self,key):
		try:
			return FreeCAD.STORE[str(key)]
		except:
			return None

	def list(self):
		try:
			FreeCAD.STORE
		except:
			FreeCAD.STORE={}
		say("store object list ...")
		for k in FreeCAD.STORE.keys():
			say(k,FreeCAD.STORE[k])

	def dela(self,key):
		try:
			FreeCAD.STORE
		except:
			FreeCAD.STORE={}
		self.list()
		say("delete",key)
		try:
			del(FreeCAD.STORE[str(key)])
		except:
			pass
