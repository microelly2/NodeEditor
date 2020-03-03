## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera, microelly

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.



from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Core.Common import Direction

import FreeCADGui




from Qt import QtGui
from Qt.QtWidgets import QFileDialog

from nodeeditor.say import *

import sys
if sys.version_info[0] !=2:
    from importlib import reload

import os
RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/res/"

class ComputeTool(ShelfTool):
    """docstring for PreviewTool."""
    def __init__(self):
        super( ComputeTool, self).__init__()

    @staticmethod
    def toolTip():
        return "call compute method for selected nodes"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "compute.png")

    @staticmethod
    def name():
        return str("ComputeTool")

    def do(self):
         nodes=FreeCAD.PF.graphManager.get().getAllNodes()
         nodes2 = sorted(nodes, key=lambda node: node.x)
         say("selected Nodes ...")
         for n in nodes2:
             if n.getWrapper().isSelected():
                say(n,n.x)
                n.compute()


class DeleteTool(ShelfTool):
    """docstring for PreviewTool."""
    def __init__(self):
        super( DeleteTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Delete the selected nodes"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "delete.png")

    @staticmethod
    def name():
        return str("DeleteTool")

    def do(self):
         nodes=FreeCAD.PF.graphManager.get().getAllNodes()
         nodes2 = sorted(nodes, key=lambda node: node.x)
         say("selected Nodes ...")
         for n in nodes2:
             if n.getWrapper().isSelected():
                say(n,n.x)

                n.kill()

class ToyTool(ShelfTool):
    """docstring for PreviewTool."""
    def __init__(self):
        super( ToyTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Toy for Developer"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "toy.png")

    @staticmethod
    def name():
        return str("ToyTool")

    def do(self):
        import nodeeditor.dev
        reload (nodeeditor.dev)
        nodeeditor.dev.run_shelfToy(self)


class FreeCADTool(ShelfTool):
    """docstring for PreviewTool."""
    def __init__(self):
        super( FreeCADTool, self).__init__()

    @staticmethod
    def toolTip():
        return "FreeCAD mainWindow"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "freecad.png")

    @staticmethod
    def name():
        return str("FreeCADTool")

    def do(self):
        mw=FreeCADGui.getMainWindow()
        mw.hide()
        mw.show()



def toollist():
    return [
               ComputeTool,
               DeleteTool,
               
               FreeCADTool,
               ToyTool,
    ]
