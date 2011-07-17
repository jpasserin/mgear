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

## @package mgear.maya.rig.component.control_01.guide
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
# Maya
from pymel.core.general import *
from pymel.util import *
import pymel.core.datatypes as dt

# mgear
from mgear.maya.rig.component.guide import ComponentGuide

# guide info
AUTHOR = "Jeremie Passerin"
URL = "http://www.jeremiepasserin.com"
EMAIL = "geerem@hotmail.com"
VERSION = [1,0,1]
TYPE = "control_01"
NAME = "control"
DESCRIPTION = "Simple controler"

##########################################################
# CLASS
##########################################################
class Guide(ComponentGuide):

    compType = TYPE
    compName = NAME
    description = DESCRIPTION

    author = AUTHOR
    url = URL
    email = EMAIL
    version = VERSION

    # =====================================================
    ##
    # @param self
    def postInit(self):
        self.pick_transform = ["root"]
        # self.save_transform = ["root", "icon"]
        self.save_transform = ["root"]
        self.save_primitive = ["icon"]

    # =====================================================
    ## Add more object to the object definition list.
    # @param self
    def addObjects(self):

        self.root = self.addRoot()
        self.icon = self.addLoc("icon", self.root, self.root.Kinematics.Global.Transform.Translation)

        self.addToGroup(self.root, "hidden")

    # =====================================================
    ## Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        # self.pIcon = self.addParam("icon", c.siString, "null", None, None)
        
        # self.pIkRefArray  = self.addParam("ikrefarray", "ikref", "string", "")
        # self.pUpvRefArray = self.addParam("upvrefarray", "upvref", "string", "")
        
        # self.pColor = self.addParam("color", "c", "long", 0, 0, 1)
        
        # self.pShadow = self.addParam("shadow", "shd", "bool", False)
        
        for s in ["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz"]:
            self.addParam("k_"+s, "k_"+s, "bool", True)

        # self.pDefault_RotOrder = self.addParam("default_rotorder", "droto", "long", 0, 0, 5)
        return

