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

## @package mgear.maya.synoptic.widgets
# @author Jeremie Passerin
#
##################################################
# GLOBAL
##################################################
import sip
import maya.OpenMayaUI as mui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

import mgear.maya.synoptic.utils as syn_uti

import functools

##################################################
# PROMOTED WIDGETS
##################################################
# They must be declared first because they are used in the widget.ui
class QuickSelButton(QPushButton):

    def mousePressEvent(self, event):

        model = syn_uti.getModel(self)
        channel = self.property("channel").toString()
        mouse_button = event.button()

        syn_uti.quickSel(model, channel, mouse_button)

class SelectButton(QWidget):
    over = False
    color_over = QColor(255, 255, 255, 255)

    def enterEvent(self, event):
        self.over = True
        self.repaint()
        self.update()

    def leaveEvent(self, event):
        self.over = False
        self.repaint()
        self.update()

    def mousePressEvent(self, event):

        model = syn_uti.getModel(self)
        object = str(self.property("object").toString()).split(",")
        mouse_button = event.button()
        key_modifier = event.modifiers()

        syn_uti.selectObj(model, object, mouse_button, key_modifier)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.over:
            painter.setBrush(self.color_over)
        else:
            painter.setBrush(self.color)
        self.drawShape(painter)
        painter.end()
        
class SelectBtn_RFk(SelectButton):
    color = QColor(0, 0, 192, 255)
    
class SelectBtn_RIk(SelectButton):
    color = QColor(0, 128, 192, 255)
    
class SelectBtn_CFk(SelectButton):
    color = QColor(128, 0, 128, 255)
    
class SelectBtn_CIk(SelectButton):
    color = QColor(192, 64, 192, 255)
    
class SelectBtn_LFk(SelectButton):
    color = QColor(192, 0, 0, 255)
    
class SelectBtn_LIk(SelectButton):
    color = QColor(192, 128, 0, 255)
    
class SelectBtn_yellow(SelectButton):
    color = QColor(255, 192, 0, 255)
    
class SelectBtn_Box(SelectButton):
    def drawShape(self, painter):
        painter.drawRect(0, 0, self.width()-1, self.height()-1)
        
class SelectBtn_Circle(SelectButton):
    def drawShape(self, painter):
        painter.drawEllipse(0, 0, self.width()-1, self.height()-1)
    
# ------------------------------------------
class SelectBtn_RFkBox(SelectBtn_RFk, SelectBtn_Box):
    pass
class SelectBtn_RIkBox(SelectBtn_RIk, SelectBtn_Box):
    pass
class SelectBtn_CFkBox(SelectBtn_CFk, SelectBtn_Box):
    pass
class SelectBtn_CIkBox(SelectBtn_CIk, SelectBtn_Box):
    pass
class SelectBtn_LFkBox(SelectBtn_LFk, SelectBtn_Box):
    pass
class SelectBtn_LIkBox(SelectBtn_LIk, SelectBtn_Box):
    pass
class SelectBtn_yellowBox(SelectBtn_yellow, SelectBtn_Box):
    pass
    
class SelectBtn_RFkCircle(SelectBtn_RFk, SelectBtn_Circle):
    pass
class SelectBtn_RIkCircle(SelectBtn_RIk, SelectBtn_Circle):
    pass
class SelectBtn_CFkCircle(SelectBtn_CFk, SelectBtn_Circle):
    pass
class SelectBtn_CIkCircle(SelectBtn_CIk, SelectBtn_Circle):
    pass
class SelectBtn_LFkCircle(SelectBtn_LFk, SelectBtn_Circle):
    pass
class SelectBtn_LIkCircle(SelectBtn_LIk, SelectBtn_Circle):
    pass
