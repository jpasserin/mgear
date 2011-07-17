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

## @package mgear.maya.rig.component.neck_ik_01.guide
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
TYPE = "neck_ik_01"
NAME = "neck"
DESCRIPTION = ""

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
        self.pick_transform = ["root", "neck", "head", "eff"]
        self.save_transform = ["root", "tan0", "tan1", "neck", "head", "eff"]
        self.save_blade = ["blade"]

    # =====================================================
    ## Add more object to the object definition list.
    # @param self
    def addObjects(self):

        self.root = self.addRoot()
        self.neck = self.addLoc("neck", self.root)
        self.head = self.addLoc("head", self.neck)
        self.eff = self.addLoc("eff", self.head)

        v0 = vec.linearlyInterpolate(self.root.Kinematics.Global.Transform.Translation, self.neck.Kinematics.Global.Transform.Translation, .333)
        self.tan0 = self.addLoc("tan0", self.root, v0)
        v1 = vec.linearlyInterpolate(self.root.Kinematics.Global.Transform.Translation, self.neck.Kinematics.Global.Transform.Translation, .666)
        self.tan1 = self.addLoc("tan1", self.neck, v1)

        self.blade = self.addBlade("blade", self.root, self.tan0)

        centers = [self.root, self.tan0, self.tan1, self.neck]
        self.dispcrv = self.addDispCurve("neck_crv", centers, 3)

        centers = [self.neck, self.head, self.eff]
        self.dispcrv = self.addDispCurve("head_crv", centers, 1)

    # =====================================================
    ## Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        # Ik
        self.pHeadRefArray  = self.addParam("headrefarray", "headrefarray", "string", "")
        self.pIkRefArray  = self.addParam("ikrefarray", "ikrefarray", "string", "")

        # Default values
        self.pMaxStretch = self.addParam("maxstretch", "mst", "double", 1.5, 1)
        self.pMaxSquash = self.addParam("maxsquash", "msq", "double", .5, 0, 1)
        self.pSoftness = self.addParam("softness", "msq", "double", 0, 0, 1)

        # Options
        self.pDivision = self.addParam("division", "div", "long", 5, 3)

        # FCurves
        self.pSt_profile = self.addFCurveParam("st_profile", "st", [[0,-.25],[.4,-1],[1,-1]])
        self.pSq_profile = self.addFCurveParam("sq_profile", "sq", [[0,.1],[.4,1],[1,1]])
