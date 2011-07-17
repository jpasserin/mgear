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

## @package mgear.maya.vector
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
# Built-in
import math

# Maya
import maya.OpenMaya as om

# PyMel
import pymel.core.datatypes as dt
from pymel.core.general import *

#############################################
# NODE
#############################################
# ===========================================
def getDistance(v0, v1):

    v = v1 - v0

    return v.length()

# ===========================================
def getDistance2(obj0, obj1):

    v0 = getAttr(obj0+".translate")
    v1 = getAttr(obj1+".translate")

    v = v1 - v0

    return v.length()

# linearlyInterpolate ====================================
## Get a vector that is the interpolation of the two input vector.\n
# This method is not limitied to a 0-1
# @param v0 SIVector3 - First position.
# @param v1 SIVector3 - Second position.
# @param blend Double - Blend between the two vectors. (0 return the first vector, 1 return the second vector)
# @return SIVector3 - The interpolated vector.
def linearlyInterpolate(v0, v1, blend=.5):

    vector = v1 - v0
    vector *= blend
    vector += v0

    return vector

# getPlaneNormal ===================================
## Get the normal vector of a plane (Defined by 3 positions).
# @param v0 SIVector3 - First position on the plane.
# @param v1 SIVector3 - Second position on the plane.
# @param v2 SIVector3 - Third position on the plane.
# @return SIVector3 - The normal.
def getPlaneNormal(v0, v1, v2):

    vector0 = v1 - v0
    vector1 = v2 - v0
    vector0.normalize()
    vector1.normalize()

    normal = vector1 ^ vector0
    normal.normalize()

    return normal

# getPlaneBiNormal =================================
## Get the binormal vector of a plane (Defined by 3 positions).
# @param v0 SIVector3 - First position on the plane.
# @param v1 SIVector3 - Second position on the plane.
# @param v2 SIVector3 - Third position on the plane.
# @return SIVector3 - The binormal.
def getPlaneBiNormal(v0, v1, v2):

    normal = getPlaneNormal(v0, v1, v2)

    vector0 = v1 - v0

    binormal = normal ^ vector0
    binormal.normalize()

    return binormal

# ===========================================
def getTransposedVector(v, position0, position1, inverse=False):

    v0 = position0[1] - position0[0]
    v0.normalize()

    v1 = position1[1] - position1[0]
    v1.normalize()

    ra = v0.angle(v1)

    if inverse:
        ra = -ra

    axis = v0 ^ v1

    vector = rotateAlongAxis(v, axis, ra)

    # Check if the rotation has been set in the right order
    ra2 = (math.pi *.5 ) - v1.angle(vector)
    vector = rotateAlongAxis(v, axis, -ra2)

    return vector

# ===========================================
def rotateAlongAxis(v, axis, a):

    # Angle as to be in radians

    sa = math.sin(a / 2.0)
    ca = math.cos(a / 2.0)

    q1 = om.MQuaternion(v.x, v.y, v.z, 0)
    q2 = om.MQuaternion(axis.x * sa, axis.y * sa, axis.z * sa, ca)
    q2n = om.MQuaternion(-axis.x * sa, -axis.y * sa, -axis.z * sa, ca)
    q = q2 * q1
    q *= q2n

    out = om.MVector(q.x, q.y, q.z)

    return out



##########################################################
# CLASS
##########################################################
# ========================================================
class Blade(object):

    def __init__(self, t=dt.Matrix()):

        self.transform = t

        d = [t.data[j][i] for j in range(len(t.data)) for i in range(len(t.data[0])) ]

        m = om.MMatrix()
        om.MScriptUtil.createMatrixFromList(d, m)
        m = om.MTransformationMatrix(m)

        x = om.MVector(1,0,0).rotateBy(m.rotation())
        y = om.MVector(0,1,0).rotateBy(m.rotation())
        z = om.MVector(0,0,1).rotateBy(m.rotation())

        self.x = dt.Vector(x.x, x.y, x.z)
        self.y = dt.Vector(y.x, y.y, y.z)
        self.z = dt.Vector(z.x, z.y, z.z)

