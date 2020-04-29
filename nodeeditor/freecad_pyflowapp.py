import os
import sys
import subprocess
import json
#from time import clock
import pkgutil
import uuid
import shutil
from string import ascii_letters
import random

from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import *

from PyFlow import GET_PACKAGES
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.Core.version import *
from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.ConfigManager import ConfigManager
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Widgets.BlueprintCanvas import BlueprintCanvasWidget
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Tool.Tool import ShelfTool, DockTool
from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.UI.Tool import GET_TOOLS
from PyFlow.UI.Tool import REGISTER_TOOL
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.UI.ContextMenuGenerator import ContextMenuGenerator
from PyFlow.UI.Widgets.PreferencesWindow import PreferencesWindow
try:
    from PyFlow.Packages.PyFlowBase.Tools.PropertiesTool import PropertiesTool
except:
    pass
from PyFlow.Wizards.PackageWizard import PackageWizard
from PyFlow import INITIALIZE
from PyFlow.Input import InputAction, InputActionType
from PyFlow.Input import InputManager
from PyFlow.ConfigManager import ConfigManager

import PyFlow.UI.resources

EDITOR_TARGET_FPS = 60


from PyFlow.App import PyFlow, getOrCreateMenu, generateRandomString,  winTitle
from nodeeditor.say import *
from PyFlow.Core.Common import currentProcessorTime


class FreeCADPyFlow(PyFlow):
    

    @staticmethod
    def instance(parent=None, software=""):
        assert(software != ""), "Invalid arguments. Please pass you software name as second argument!"
        settings = ConfigManager().getSettings("APP_STATE")

        instance = FreeCADPyFlow(parent)
        instance.currentSoftware = software
        SessionDescriptor().software = instance.currentSoftware

        if software == "standalone":
            editableStyleSheet(instance)

        try:
            extraPackagePaths = []
            extraPathsString = ConfigManager().getPrefsValue("PREFS", "General/ExtraPackageDirs")
            if extraPathsString is not None:
                extraPathsString = extraPathsString.rstrip(";")
                extraPathsRaw = extraPathsString.split(";")
                for rawPath in extraPathsRaw:
                    if os.path.exists(rawPath):
                        extraPackagePaths.append(os.path.normpath(rawPath))
            INITIALIZE(additionalPackageLocations=extraPackagePaths, software=software)
        except Exception as e:
            QMessageBox.critical(None, "Fatal error", str(e))
            return

        instance.startMainLoop()

        # populate tools
        canvas = instance.getCanvas()
        toolbar = instance.getToolbar()

        # populate menus
        instance.populateMenu()

        geo = settings.value('Editor/geometry')
        if geo is not None:
            instance.restoreGeometry(geo)
        state = settings.value('Editor/state')
        if state is not None:
            instance.restoreState(state)
        settings.beginGroup("Tools")
        for packageName, registeredToolSet in GET_TOOLS().items():
            for ToolClass in registeredToolSet:
                if issubclass(ToolClass, ShelfTool):
                    ToolInstance = ToolClass()
                    # prevent to be garbage collected
                    instance.registerToolInstance(ToolInstance)
                    ToolInstance.setAppInstance(instance)
                    action = QAction(instance)
                    action.setIcon(ToolInstance.getIcon())
                    action.setText(ToolInstance.name())
                    action.setToolTip(ToolInstance.toolTip())
                    action.setObjectName(ToolInstance.name())
                    action.triggered.connect(ToolInstance.do)
                    # check if context menu data available
                    menuBuilder = ToolInstance.contextMenuBuilder()
                    if menuBuilder:
                        menuGenerator = ContextMenuGenerator(menuBuilder)
                        menu = menuGenerator.generate()
                        action.setMenu(menu)
                    toolbar.addAction(action)

                    # step to ShelfTools/ToolName group and pass settings inside
                    settings.beginGroup("ShelfTools")
                    settings.beginGroup(ToolClass.name())
                    ToolInstance.restoreState(settings)
                    settings.endGroup()
                    settings.endGroup()

                if issubclass(ToolClass, DockTool):
                    menus = instance.menuBar.findChildren(QMenu)
                    pluginsMenuAction = [m for m in menus if m.title() == "Plugins"][0].menuAction()
                    toolsMenu = getOrCreateMenu(instance.menuBar, "Tools")
                    instance.menuBar.insertMenu(pluginsMenuAction, toolsMenu)
                    packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
                    toolsMenu.addMenu(packageSubMenu)
                    showToolAction = packageSubMenu.addAction(ToolClass.name())
                    icon = ToolClass.getIcon()
                    if icon:
                        showToolAction.setIcon(icon)
                    showToolAction.triggered.connect(lambda pkgName=packageName, toolName=ToolClass.name(): instance.invokeDockToolByName(pkgName, toolName))

                    settings.beginGroup("DockTools")
                    childGroups = settings.childGroups()
                    for dockToolGroupName in childGroups:
                        # This dock tool data been saved on last shutdown
                        settings.beginGroup(dockToolGroupName)
                        if dockToolGroupName in [t.uniqueName() for t in instance._tools]:
                            continue
                        toolName = dockToolGroupName.split("::")[0]
                        instance.invokeDockToolByName(packageName, toolName, settings)
                        settings.endGroup()
                    settings.endGroup()

        PyFlow.appInstance = instance
        EditorHistory().saveState("New file")

        for name, package in GET_PACKAGES().items():
            prefsWidgets = package.PrefsWidgets()
            if prefsWidgets is not None:
                for categoryName, widgetClass in prefsWidgets.items():
                    PreferencesWindow().addCategory(categoryName, widgetClass())
                PreferencesWindow().selectByName("General")
        return instance

    # hack - save and restore data when pyflow main window is minimized and comes back
    def changeEvent(self, event):
        
        #sayl()
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                import nodeeditor.dev
                nodeeditor.dev.run_PF_APP_WindowMinimized(self,event)
            elif event.oldState() & QtCore.Qt.WindowMinimized:
                import nodeeditor.dev
                nodeeditor.dev.run_PF_APP_WindowNOMinimized(self,event)
        QWidget.changeEvent(self, event)
    # hack end


    def mainLoop(self):
        deltaTime = currentProcessorTime() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)

        # Tick all graphs
        # each graph will tick owning raw nodes
        # each raw node will tick it's ui wrapper if it exists
        self.graphManager.get().Tick(deltaTime)

        # Tick canvas. Update ui only stuff such animation etc.
        self.canvasWidget.Tick(deltaTime)

        self._lastClock = currentProcessorTime()


    def XmainLoop(self):
        
        deltaTime = clock() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)

        #+hack++
        if self.graphManager.get() == None:
            print("no graphManager found - aborting ...")
            return
        #-hack end--
        # Tick all graphs
        # each graph will tick owning raw nodes
        # each raw node will tick it's ui wrapper if it exists
        self.graphManager.get().Tick(deltaTime)

        # Tick canvas. Update ui only stuff such animation etc.
        self.canvasWidget.Tick(deltaTime)

        self._lastClock = clock()


    def closeEvent(self, event):

        '''
        #+hack deactivate saving
        if False: # mkae this configurabel somewhere?
            shouldSave = self.shouldSave()
        else:
            shouldSave = QMessageBox.No
        #-hack end
        if shouldSave == QMessageBox.Yes:
            if not self.save():
                event.ignore()
                return
        elif shouldSave == QMessageBox.Discard:
            event.ignore()
            return
        '''

        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()
        EditorHistory().shutdown()

        self.canvasWidget.shoutDown()
        # save editor config
        settings = ConfigManager().getSettings("APP_STATE")

        # clear file each time to capture opened dock tools
        settings.clear()
        settings.sync()

        settings.beginGroup('Editor')
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.endGroup()

        # save tools state
        settings.beginGroup('Tools')
        for tool in self._tools:
            if isinstance(tool, ShelfTool):
                settings.beginGroup("ShelfTools")
                settings.beginGroup(tool.name())
                tool.saveState(settings)
                settings.endGroup()
                settings.endGroup()
            if isinstance(tool, DockTool):
                settings.beginGroup("DockTools")
                settings.beginGroup(tool.uniqueName())
                tool.saveState(settings)
                settings.endGroup()
                settings.endGroup()
            tool.onDestroy()
        settings.endGroup()
        settings.sync()

        # remove temp directory if exists
        if os.path.exists(self.currentTempDir):
            shutil.rmtree(self.currentTempDir)

        SingletonDecorator.destroyAll()

        PyFlow.appInstance = None

        #+hack cleanup  pfwrapper
        import nodeeditor.pfwrap as pfwrap
        pfwrap.deleteInstance()
        del(FreeCAD.PF)
        #-hack end
        QMainWindow.closeEvent(self, event)

