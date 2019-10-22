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

from Qt import QtGui
from Qt.QtWidgets import QFileDialog

from nodeeditor.say import *

import os
RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/res/"

class PreviewTool(ShelfTool):
    """docstring for PreviewTool."""
    def __init__(self):
        super( PreviewTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Preview of a node on/off"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "preview.png")

    @staticmethod
    def name():
        return str("PreviewTool")

    def do(self):
         nodes=FreeCAD.PF.graphManager.get().getAllNodes()
         say("selected Nodes ...")
         for n in nodes:
             if n.getWrapper().isSelected():
                say(n)
                n._preview = not n._preview
                n.preview()
