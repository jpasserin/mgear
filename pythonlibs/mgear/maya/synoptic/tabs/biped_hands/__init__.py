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

## @package mgear.maya.synoptic.tabs.biped_hands
# @author Jeremie Passerin
#
##################################################
# GLOBAL
##################################################
import os

import sip
import maya.OpenMayaUI as mui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

import mgear.maya.synoptic.utils as syn_uti

import functools

UI_PATH = os.path.join(os.path.dirname(__file__), "widget.ui")
BG_PATH = os.path.join(os.path.dirname(__file__), "background.bmp")

##################################################
# SYNOPTIC TAB WIDGET
##################################################
#where UI_PATH is the path to our designer .ui file
form_class, base_class = uic.loadUiType(UI_PATH)

class SynopticTab(base_class, form_class):

    # ============================================
    # INIT
    def __init__(self, parent=None):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        # Retarget background Image to absolute path
        self.img_background.setPixmap(QPixmap(BG_PATH))

        # Connect signal
        self.b_selRight.clicked.connect(self.selRight_clicked)
        self.b_selLeft.clicked.connect(self.selLeft_clicked)
        self.b_keyRight.clicked.connect(self.keyRight_clicked)
        self.b_keyLeft.clicked.connect(self.keyLeft_clicked)
        self.b_keySel.clicked.connect(self.keySel_clicked)

    def mousePressEvent(self, event):
        print event.button()

    # ============================================
    # BUTTONS
    def selRight_clicked(self):
        model = syn_uti.getModel(self)
        # i : num of fingers, j : finger length
        object_names = ["finger_R%s_fk%s_ctl"%(i,j) for i in range(4) for j in range(3)]
        thumb_names = ["thumb_R0_fk%s_ctl"%j for j in range(3)]
        object_names.extend(thumb_names)
        syn_uti.selectObj(model, object_names, None, None)

    def selLeft_clicked(self):
        model = syn_uti.getModel(self)
        # i : num of fingers, j : finger length
        object_names = ["finger_L%s_fk%s_ctl"%(i,j) for i in range(4) for j in range(3)]
        thumb_names = ["thumb_L0_fk%s_ctl"%j for j in range(3)]
        object_names.extend(thumb_names)
        syn_uti.selectObj(model, object_names, None, None)

    def keyRight_clicked(self):
        model = syn_uti.getModel(self)
        # i : num of fingers, j : finger length
        object_names = ["finger_R%s_fk%s_ctl"%(i,j) for i in range(4) for j in range(3)]
        thumb_names = ["thumb_R0_fk%s_ctl"%j for j in range(3)]
        object_names.extend(thumb_names)
        syn_uti.keyObj(model, object_names)

    def keyLeft_clicked(self):
        model = syn_uti.getModel(self)
        # i : num of fingers, j : finger length
        object_names = ["finger_L%s_fk%s_ctl"%(i,j) for i in range(4) for j in range(3)]
        thumb_names = ["thumb_L0_fk%s_ctl"%j for j in range(3)]
        object_names.extend(thumb_names)
        syn_uti.keyObj(model, object_names)

    def keySel_clicked(self):
        syn_uti.keySel()
