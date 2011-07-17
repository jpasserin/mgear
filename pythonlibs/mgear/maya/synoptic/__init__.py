'''

    This file is part of MGEAR.

    MGEAR is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.

    Author:     Jeremie Passerin      geerem@hotmail.com
    Url:        http://www.jeremiepasserin.com
    Date:       2011 / 07 / 13

'''

## @package mgear.maya.synoptic
# @author Jeremie Passerin
#
##################################################
# GLOBAL
##################################################
import os
import sip

import maya.cmds as cmds
import maya.OpenMayaUI as mui
from pymel.core import *

from PyQt4 import QtGui, QtCore, uic

def getMayaWindow():
	'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

    
TAB_PATH = os.path.join(os.path.dirname(__file__), "tabs")
SYNOPTIC_WIDGET_NAME = "synoptic_view"

##################################################
# OPEN
##################################################
def open():

    global synoptic_window
    synoptic_window = Synoptic(getMayaWindow())
    synoptic_window.show()
    if (cmds.dockControl('synoptic_dock', q=1, ex=1)):
        cmds.deleteUI('synoptic_dock')
    allowedAreas = ['right', 'left']
    synoptic_dock = cmds.dockControl('synoptic_dock',aa=allowedAreas, a='left', content=SYNOPTIC_WIDGET_NAME, label='Synoptic View', w=350)
    
##################################################
# SYNOPTIC
##################################################
class Synoptic(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Synoptic, self).__init__(parent)
        self.create_widgets()

    def create_widgets(self):
    
        # Widgets
        self.model_list = QtGui.QComboBox()
        self.model_list.setObjectName("model_list")
        self.refresh_button = QtGui.QPushButton("Refresh")
        self.refresh_button.setObjectName("refresh_button")
        self.tabs = QtGui.QTabWidget()
        self.tabs.setObjectName("synoptic_tab")
        
        # Layout
        self.setObjectName(SYNOPTIC_WIDGET_NAME)
        # self.resize(350, 500)
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.hbox = QtGui.QHBoxLayout(self)
        
        self.vbox.addLayout(self.hbox)
        self.hbox.addWidget(self.model_list)
        self.hbox.addWidget(self.refresh_button)
        self.vbox.addWidget(self.tabs)
        
        # Connect Signal
        QtCore.QObject.connect(self.refresh_button, QtCore.SIGNAL("clicked()"), self.updateModelList)
        QtCore.QObject.connect(self.model_list, QtCore.SIGNAL("currentIndexChanged()"), self.updateTabs)
        
        # Initialise
        self.updateModelList()
        self.updateTabs()
        
    # Singal Methods =============================
    def updateModelList(self):
        rig_models = [item for item in ls(transforms=True) if item.getParent() is None and item.hasAttr("is_rig")]
        self.model_list.clear()
        for item in rig_models:
            self.model_list.addItem(item.name(), item.name()    )
            
    def updateTabs(self):
        
        self.tabs.clear()
        tab_names = ["biped_body", "biped_hands"]
        for i, tab_name in enumerate(tab_names):
            module_name = "mgear.maya.synoptic.tabs."+tab_name
            module = __import__(module_name, globals(), locals(), ["*"], -1)
            SynopticTab = getattr(module , "SynopticTab")

            tab = SynopticTab()
            self.tabs.insertTab(i, tab, tab_name)
        