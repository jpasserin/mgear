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

## @package mgear.maya.rig.component.control_01
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
# Maya
from pymel.core.general import *
from pymel.core.animation import *
from pymel.util import *
import pymel.core.datatypes as dt

import maya.OpenMaya as om

# mgear
from mgear.maya.rig.component import MainComponent

import mgear.maya.primitive as pri
import mgear.maya.transform as tra
import mgear.maya.attribute as att
import mgear.maya.node as nod
import mgear.maya.icon as ico

#############################################
# COMPONENT
#############################################
class Component(MainComponent):

    def addObjects(self):
    
        self.ctl = self.addCtl(self.root, "ctl", tra.getTransform(self.root), self.color_ik, "square")
        
        params = [ s for s in ["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz"] if self.settings["k_"+s] ]
        att.setKeyableAttributes(self.ctl, params)
        
    def addAttributes(self):
        return

    def addOperators(self):
        return

    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Set the relation beetween object from guide to rig.\n
    # @param self
    def setRelation(self):
        self.relatives["root"] = self.ctl 
