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

## @package mgear.maya.primitive
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
# Maya
from pymel.core import *
import pymel.core.datatypes as dt

# mgear
import mgear.maya.transform as tra
import mgear.maya.icon as ico
import mgear.maya.vector as vec

#############################################
# PRIMITIVE
#############################################
# ===========================================
# TRANSFORM
def addTransform(parent, name, m=dt.Matrix()):

    node = PyNode(createNode("transform", n=name))
    node.setTransformation(m)
    
    if parent is not None:
        parent.addChild(node)

    return node

def addTransformFromPos(parent, name, pos=dt.Vector(0,0,0)):

    node = PyNode(createNode("transform", n=name))
    node.setTranslation(pos, space="world")
    
    if parent is not None:
        parent.addChild(node)

    return node

# ===========================================
# LOCATOR
def addLocator(parent, name, m=dt.Matrix(), size=1):

    node = PyNode(createNode("locator")).getParent()
    node.rename(name)
    node.setTransformation(m)
    node.setAttr("localScale", size, size, size)
    
    if parent is not None:
        parent.addChild(node)

    return node

def addLocatorFromPos(parent, name, pos=dt.Vector(0,0,0), size=1):

    node = PyNode(createNode("locator")).getParent()
    node.rename(name)
    node.setTranslation(pos, space="world")
    node.setAttr("localScale", size, size, size)
    
    if parent is not None:
        parent.addChild(node)

    return node

# ===========================================
# JOINT
def addJoint(parent, name, m=dt.Matrix()):

    # I'm not using the joint() comand because this is parenting 
    # the newly created joint to current selection which might not be desired
    node = PyNode(createNode("joint", n=name))
    node.setTransformation(m)
    
    if parent is not None:
        parent.addChild(node)

    return node

def addJointFromPos(parent, name, pos=dt.Vector(0,0,0)):

    # I'm not using the joint() comand because this is parenting 
    # the newly created joint to current selection which might not be desired
    node = PyNode(createNode("joint", n=name))
    node.setTranslation(pos, space="world")
    
    if parent is not None:
        parent.addChild(node)

    return node

def add2DChain(parent, name, positions, normal, negate=False):
    
    if not "%s" in name:
        name += "%s"
    
    transforms = tra.getChainTransform(positions, normal, negate=False)
    t = tra.setMatrixPosition(transforms[-1], positions[-1])
    transforms.append(t)
    
    chain = []
    for i, t in enumerate(transforms): 
        node = addJoint(parent, name%i, t)
        chain.append(node)
        parent = node
    
    # moving rotation value to joint orient
    for i, jnt in enumerate(chain):
        
        if i == 0:
            jnt.setAttr("jointOrient", jnt.getAttr("rotate"))
        elif i == len(chain)-1:
            jnt.setAttr("jointOrient", 0, 0, 0)
        else:
            # This will fail if chain is not always oriented the same way (like Z chain)
            v0 = positions[i] - positions[i-1]
            v1 = positions[i+1] - positions[i]
            
            jnt.setAttr("jointOrient", 0, 0, dt.degrees(v0.angle(v1)))
            
        jnt.setAttr("rotate", 0, 0, 0)
            
    return chain
    
# ===========================================
# IK HANDLE
def addIkHandle(parent, name, chn, solver="ikRPsolver"):

    node = ikHandle(n=name, sj=chn[0], ee=chn[-1], solver=solver)[0]
    
    if parent is not None:
        parent.addChild(node)

    return node

    
    
    