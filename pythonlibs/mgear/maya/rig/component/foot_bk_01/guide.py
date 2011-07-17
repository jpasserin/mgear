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

## @package mgear.maya.rig.component.foot_bk_01.guide
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
VERSION = [1,0,0]
TYPE = "foot_bk_01"
NAME = "foot"
DESCRIPTION = "Foot with reversed controlers to control foot roll."

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

    connectors = ["leg_2jnt_01", "leg_3jnt_01"]

    # =====================================================
    ##
    # @param self
    def postInit(self):
        self.pick_transform = ["root", "#_loc"]
        self.save_transform = ["root", "#_loc", "heel", "outpivot", "inpivot"]
        self.addMinMax("#_loc", 1, -1)

    # =====================================================
    ## Add more object to the object definition list.
    # @param self
    def addObjects(self):

        self.root = self.addRoot()
        self.locs = self.addLocMulti("#_loc", self.root)

        centers = [self.root]
        centers.extend(self.locs)
        self.dispcrv = self.addDispCurve("crv", centers)

        # Heel and pivots
        self.heel = self.addLoc("heel", self.root)
        self.outpivot = self.addLoc("outpivot", self.root)
        self.inpivot = self.addLoc("inpivot", self.root)

        self.dispcrv = self.addDispCurve("1", [self.root, self.heel, self.outpivot, self.heel, self.inpivot])

    # =====================================================
    ## Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        self.pRoll = self.addParam("roll", "r", "int", 0, 0, 1)


