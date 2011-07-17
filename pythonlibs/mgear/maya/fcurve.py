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

## @package mgear.maya.fcurve
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
import mgear

from pymel.core.general import *

#############################################
# FCURVE
#############################################
# Get FCurve Values ======================================
## Get X values evently spaced on the FCurve.
# @param fcv FCurve - The FCurve to evaluate.
# @param division Integer - The number of division you want to evaluate on the FCurve.
# @return List of Double - The values.
def getFCurveValues(fcv_node, division, factor=1):

    incr = 1 / (division-1.0)
    
    values = []
    for i in range(division):
        setAttr(fcv_node+".input", i*incr)
        values.append(getAttr(fcv_node+".output") * factor)
    
    return values