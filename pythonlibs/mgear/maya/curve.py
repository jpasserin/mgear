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

## @package mgear.maya.curve
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
from pymel.core import *
import pymel.core.datatypes as dt

import mgear.maya.applyop as aop

#############################################
# CURVE
#############################################
# ========================================================
## Create a curve attached to given centers. One point per center.\n
# Do to so we use a cluster center operator per point. We could use an envelope (method to do so is in the code), but there was a reason I can't remember why it was better to use clustercenter.
# @param parent X3DObject - Parent object.
# @param name String - Name.
# @param centers List of X3DObject - Object that will drive the curve.
# @param close Boolean - True to close the fcurve.
# @param degree Integer - 1 for linear curve, 3 for Cubic.
# @return NurbCurve - The newly created curve.
def addCnsCurve(parent, name, centers, degree=1):

    if degree == 3:
        if len(centers) == 2:
            centers.insert(0, centers[0])
            centers.append(centers[-1])
        elif len(centers) == 3:
            centers.append(centers[-1])

    points = [dt.Vector() for center in centers ]

    node = addCurve(parent, name, points, False, degree)

    op = aop.gear_curvecns_op(node, centers)

    return node

# ========================================================
## Create a NurbsCurve with a single subcurve.
# @param parent X3DObject - Parent object.
# @param name String - Name.
# @param points List of Double - positions of the curve in a one dimension array [point0X, point0Y, point0Z, 1, point1X, point1Y, point1Z, 1, ...].
# @param close Boolean - True to close the curve.
# @param degree Integer - 1 for linear curve, 3 for Cubic.
# @param t SITransformation - Global transform.
# @return NurbCurve - The newly created curve.
def addCurve(parent, name, points, close=False, degree=3, m=dt.Matrix()):

    if close:
        points.extend(points[:degree])
        knots = range(len(points)+degree-1)
        node = curve(n=name, d=degree, p=points, per=close, k=knots)
    else:
        node = curve(n=name, d=degree, p=points)

    if m is not None:
        node.setTransformation(m)

    if parent is not None:
        parent.addChild(node)

    return node



