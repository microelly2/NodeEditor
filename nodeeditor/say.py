# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- (c) microelly 2017 v 0.4
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''package ausgabe von programmablaufinformationen, importieren der wichtigsten module'''

import Qt
from Qt import QtCore, QtGui,QtWidgets

import sys
import traceback
import inspect


try: # define the FreeCAD say methods

	import FreeCAD

	def log(s,logon=False):
		'''write to a logfile'''
		if logon:
			f = open('/tmp/log.txt', 'a')
			f.write(str(s) +'\n')
			f.close()

	def say(*args):
		'''print information to console''' 
		s='; '.join([str(a) for a in args])
#		log(str(s))
		FreeCAD.Console.PrintMessage(str(s)+"\n")

	def sayErr(*args):
		'''print information as error'''
		s='; '.join([str(a) for a in args])
		log(str(s))
		FreeCAD.Console.PrintError(str(s)+"\n")


	def sayW(*args):
		'''print information as warning'''
		s='; '.join([str(a) for a in args])
		log(str(s))
		FreeCAD.Console.PrintWarning(str(s)+"\n")

	def sayl(*args):
		''' print message with traceback''' 
		s='; '.join([str(a) for a in args])
		l=len(inspect.stack())
		FreeCAD.Console.PrintWarning(str(s)+" "+str(inspect.stack()[1][3]+" @ ..."+inspect.stack()[1][1][-68:]+" li: "+str(inspect.stack()[1][2]))+"\n")


except:

	print("cannot load FreeCAD methods")

	def say(*args):
		'''print information to console''' 
		s='; '.join([str(a) for a in args])
		print(str(s))

	def sayErr(*args):
		'''print information as error'''
		s="ERROR:"+'; '.join([str(a) for a in args])
		print(str(s))

	def sayW(*args):
		say(args)
		'''print information as warning'''
		s="WARNING:"+'; '.join([str(a) for a in args])
		print(str(s))

	def sayl(*args):
		''' print message with traceback''' 
		s='; '.join([str(a) for a in args])
		l=len(inspect.stack())
		print (str(s),inspect.stack()[1][3]," @ ",inspect.stack()[1][1]," line: ",inspect.stack()[1][2])


def errorDialog(msg):
	''' pop up an error QMessageBox'''
	diag = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,u"Error Message",msg )
	diag.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	diag.exec_()


def sayexc(mess=''):
	''' print message with traceback''' 
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

	l=len(inspect.stack())
	print (inspect.stack()[1][3]," @ ",inspect.stack()[1][1]," line: ",inspect.stack()[1][2])
	if l>3: print (inspect.stack()[2][3]," @ ",inspect.stack()[2][1]," line: ",inspect.stack()[2][2])
	if l>3 and inspect.stack()[3][3] != '<module>':        
		print (inspect.stack()[3][1]," line ",inspect.stack()[3][2])
		print (inspect.stack()[3][3])



def showdialog(title="Fehler",
			   text="Schau in den ReportView fuer mehr Details", detail=None):
	'''display a window with: title,text and detail'''

	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Warning)
	msg.setText(text)
	msg.setWindowTitle(title)
	if detail != None:
		msg.setDetailedText(detail)
	msg.exec_()


def sayexc2(title='Error', mess=''):
	'''display exception trace in Console
	and pop up a window with title, message'''

	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
	lls = eval(ttt)
	laa = len(lls)
	la2 = lls[(laa - 3):]
	sayErr(title)
	if mess!='':
		sayErr(mess)

	showdialog(title, text=mess, detail="--> ".join(la2))

	try:
		say(la2[-2])
		sayErr(la2[-1])
	except:
		pass

	l=len(inspect.stack())
	say(inspect.stack()[1][3]+" @ "+inspect.stack()[1][1]+" line: ",inspect.stack()[1][2])
	if l>3: say (inspect.stack()[2][3]+" @ "+inspect.stack()[2][1]+" line: ",inspect.stack()[2][2])
	if l>4 and inspect.stack()[3][3] != '<module>':
		say (inspect.stack()[3][1]," line ",inspect.stack()[2][2])
		say (inspect.stack()[3][3])

def sayk(*args):
	from time import gmtime, strftime
	aa=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	s="--"+'; '.join([str(a) for a in args])
	with open("/tmp/say_log.txt", "a") as myfile:
		myfile.write("\n"+aa+" "+ s+ "\n")
		myfile.write(inspect.stack()[1][3]+" @ "+inspect.stack()[1][1]+" line: "+str(inspect.stack()[1][2]))


'''
import inspect
print(inspect.stack()[1],"huhu")
'''
