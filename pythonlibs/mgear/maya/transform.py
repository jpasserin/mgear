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

## @package mgear.maya.transform
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
from pymel.core.general import *
from pymel.util import *
import pymel.core.datatypes as dt

import mgear.maya.vector as vec

#############################################
# TRANSFORM
#############################################
def getTranslation(node, worldSpace=True):
    return node.getTranslation(space="world")

def getTransform(node, worldSpace=True):
    return node.getMatrix(worldSpace=True)

def getTransformLookingAt(pos, lookat, normal, axis="xy", negate=False):

    normal.normalize()

    if negate:
        a = pos - lookat
        # normal *= -1
    else:
        a = lookat - pos

    a.normalize()
    c = cross(a, normal)
    c.normalize()
    b = cross(c, a)
    b.normalize()

    if axis == "xy":
        X = a
        Y = b
        Z = c
    elif axis == "xz":
        X = a
        Z = b
        Y = -c
    elif axis == "yx":
        Y = a
        X = b
        Z = -c
    elif axis == "yz":
        Y = a
        Z = b
        X = c
    elif axis == "zx":
        Z = a
        X = b
        Y = c
    elif axis == "zy":
        Z = a
        Y = b
        X = -c

    m = dt.Matrix()
    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m

# ===========================================================
def getChainTransform(positions, normal, negate=False):

    # Draw
    transforms = []
    for i in range(len(positions)-1):
        v0 = positions[i-1]
        v1 = positions[i]
        v2 = positions[i+1]

        # Normal Offset
        if i > 0:
            normal = vec.getTransposedVector(normal, [v0, v1], [v1, v2])

        t = getTransformLookingAt(v1, v2, normal, "xz", negate)
        transforms.append(t)

    return transforms

def getTransformFromPos(pos):

    m = dt.Matrix()
    m[0] = [1.0, 0, 0, 0.0]
    m[1] = [0, 1.0, 0, 0.0]
    m[2] = [0, 0, 1.0, 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m

def setMatrixPosition(in_m, pos):
    
    m = dt.Matrix()
    m[0] = in_m[0]
    m[1] = in_m[1]
    m[2] = in_m[2]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m

def setMatrixRotation(m, rot):

    # for v in rot:
        # v.normalize()

    X = rot[0]
    Y = rot[1]
    Z = rot[2]

    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]

    return m

# filterTransform ==========================================
## Retrieve a transformation filtered.
# @param t SITransformation - Reference transformation.
# @param translation Boolean - True to match translation.
# @param rotation Boolean - True to match rotation.
# @param scaling Boolean - True to match scaling.
# @return SITransformation - The filtered transformation
def getFilteredTransform(m, translation=True, rotation=True, scaling=True):

    t = dt.Vector(m[3][0],m[3][1],m[3][2])
    x = dt.Vector(m[0][0],m[0][1],m[0][2])
    y = dt.Vector(m[1][0],m[1][1],m[1][2])
    z = dt.Vector(m[2][0],m[2][1],m[2][2])

    out = dt.Matrix()
    
    if translation:
        out = setMatrixPosition(out, t)
        
    if rotation and scaling:
        out = setMatrixRotation(out, [x,y,z])
    elif rotation and not scaling:
        out = setMatrixRotation(out, [x.normal(), y.normal(), z.normal()])
    elif not rotation and scaling:
        out = setMatrixRotation(out, [dt.Vector(1,0,0) * x.length(), dt.Vector(0,1,0) * y.length(), dt.Vector(0,0,1) * z.length()])

    return out

##########################################################
# ROTATION
##########################################################

# setRefPose =============================================
def getRotationFromAxis(in_a, in_b, axis="xy", negate=False):

    a = dt.Vector(in_a.x, in_a.y, in_a.z)
    b = dt.Vector(in_b.x, in_b.y, in_b.z)
    c = dt.Vector()

    if negate:
        a *= -1

    a.normalize()
    c = a ^ b
    c.normalize()
    b = c ^ a
    b.normalize()

    if axis == "xy":
      x = a
      y = b
      z = c
    elif axis == "xz":
      x = a
      z = b
      y = -c
    elif axis == "yx":
      y = a
      x = b
      z = -c
    elif axis == "yz":
      y = a
      z = b
      x = c
    elif axis == "zx":
      z = a
      x = b
      y = c
    elif axis == "zy":
      z = a
      y = b
      x = -c

    m = dt.Matrix()
    setMatrixRotation(m, [x,y,z])

    return m
