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

## @package mgear.maya.rig.component.leg_2jnt_01.guide
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
TYPE = "leg_2jnt_01"
NAME = "leg"
DESCRIPTION = "2 bones leg with stretch, roundess, ik/fk..."

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
        self.pick_transform = ["root", "knee", "ankle", "eff"]
        self.save_transform = ["root", "knee", "ankle", "eff"]

    # =====================================================
    ## Add more object to the object definition list.
    # @param self
    def addObjects(self):

        self.root = self.addRoot()
        self.knee = self.addLoc("knee", self.root)
        self.ankle = self.addLoc("ankle", self.knee)
        self.eff = self.addLoc("eff", self.ankle)

        centers = [self.root, self.knee, self.ankle, self.eff]
        self.dispcrv = self.addDispCurve("crv", centers)

    # =====================================================
    ## Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        # Default Values
        self.pBlend       = self.addParam("blend", "b", "long", 1, 0, 1)
        self.pIkRefArray  = self.addParam("ikrefarray", "ikref", "string", "")
        self.pUpvRefArray = self.addParam("upvrefarray", "upvref", "string", "")
        self.pMaxStretch  = self.addParam("maxstretch", "ms", "double", 1.5 , 1, None)

        # Divisions
        self.pDiv0 = self.addParam("div0", "d0", "long", 2, 1, None)
        self.pDiv1 = self.addParam("div1", "d1", "long", 2, 1, None)
        
        # FCurves
        self.pSt_profile = self.addFCurveParam("st_profile", "st", [[0,-.25],[.4,-1],[1,-1]])
        self.pSq_profile = self.addFCurveParam("sq_profile", "sq", [[0,.1],[.4,1],[1,1]])

