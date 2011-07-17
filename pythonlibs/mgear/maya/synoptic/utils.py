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

## @package mgear.maya.synoptic.utils
# @author Jeremie Passerin
#
##################################################
# GLOBAL
##################################################
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pymel.core import *

import mgear
import mgear.maya.dag as dag
from mgear.maya.synoptic import SYNOPTIC_WIDGET_NAME

CTRL_GRP_SUFFIX = "_controlers_grp"

##################################################
# 
##################################################
def getSynopticWidget(widget, max_iter=20):

    parent = widget.parentWidget()
    for i in range(max_iter):
        if parent.objectName() == SYNOPTIC_WIDGET_NAME:
            return parent
        parent = parent.parentWidget()
        
    return False
    
def getModel(widget):

    syn_widget = getSynopticWidget(widget, max_iter=20)
    model_name = syn_widget.model_list.currentText()
    model = PyNode(model_name)
    
    return model
    
def getControlers(model):

    ctl_set = PyNode(model.name()+CTRL_GRP_SUFFIX)
    members = ctl_set.members()
    
    return members
    
##################################################
# SELECT
##################################################      
# ================================================
def selectObj(model, object_names, mouse_button, key_modifier):

    if mouse_button == Qt.RightButton:
        return
        
    nodes = []
    for name in object_names:
        node = dag.findChild(model, name)
        if not node:
            mgear.log("Can't find object : %s.%s"%(model.name(), name), mgear.sev_error)
        nodes.append(node)
        
    if not nodes:
        return

    # Key pressed 
    if key_modifier is None:
        select(nodes)
    elif key_modifier == Qt.NoModifier:# No Key
        select(nodes)
    elif key_modifier == Qt.ControlModifier: # ctrl
        select(nodes, add=True)
    elif key_modifier == Qt.ShiftModifier: # shift
        select(nodes, toggle=True)
    elif int(key_modifier) == Qt.ControlModifier + Qt.ShiftModifier: # ctrl + shift
        select(nodes, deselect=True)
    elif key_modifier == Qt.AltModifier: # alt
        select(nodes)
    elif int(key_modifier) == Qt.ControlModifier + Qt.AltModifier: # ctrl + alt
        select(nodes, add=True)
    elif int(key_modifier) == Qt.ShiftModifier + Qt.AltModifier: # shift + alt
        select(nodes, toggle=True)
    elif int(key_modifier) == Qt.ControlModifier + Qt.AltModifier + Qt.ShiftModifier: # Ctrl + alt + shift
        select(nodes, deselect=True)
    else:
        select(nodes)

# ================================================
def quickSel(model, channel, mouse_button):

    qs_attr = model.attr("quicksel%s"%channel)

    if mouse_button == Qt.LeftButton: # Call Selection
        names = qs_attr.get().split(",")
        if not names:
            return
        select(clear=True)
        for name in names:
            ctl = dag.findChild(model, name)
            if ctl:
                ctl.select(add=True)
    elif mouse_button == Qt.MidButton: # Save Selection
        names = [ sel.name().split("|")[-1] for sel in ls(selection=True) if sel.name().endswith("_ctl") ]
        qs_attr.set(",".join(names))
        
    elif mouse_button == Qt.RightButton: # Key Selection
        names = qs_attr.get().split(",")
        if not names:
            return
            
# ================================================
def selAll(model):

    controlers = getControlers(model)
    select(controlers)
    
##################################################
# KEY
##################################################      
# ================================================
def keySel():
    setKeyframe()   
    
# ================================================
def keyObj(model, object_names):

    nodes = []
    for name in object_names:
        node = dag.findChild(model, name)
        if not node:
            mgear.log("Can't find object : %s.%s"%(model.name(), name), mgear.sev_error)
        nodes.append(node)
        
    if not nodes:
        return
    
    setKeyframe(*nodes)
    
# ================================================
def keyAll(model):

    controlers = getControlers(model)
    setKeyframe(controlers)
    
    
    
        
