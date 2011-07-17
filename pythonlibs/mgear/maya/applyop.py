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

## @package mgear.maya.applyop
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
from pymel.core import *
from pymel.util import *
import pymel.core.datatypes as dt

#############################################
# BUILT IN NODES
#############################################
# PathCns ================================================
## Apply a path constraint or curve constraint.
# @param obj X3DObject - Constrained object.
# @param curve Nurbcurve - Constraining Curve.
# @param cnsType Integer - 0 for Path Constraint ; 1 for Curve Constraint (Parametric).
# @param u Double - Position of the object on the curve (from 0 to 100 for path constraint, from 0 to 1 for Curve cns).
# @param tangent Boolean - Active tangent.
# @param upv X3DObject - Object that act as up vector.
# @param comp Boolean - Active constraint compensation.
# @return the newly created constraint.
def pathCns(obj, curve, cnsType=False, u=0, tangent=False):
    
    node = PyNode(createNode("motionPath"))
    node.setAttr("uValue", u)
    node.setAttr("fractionMode", not cnsType)
    node.setAttr("follow", tangent)
    
    connectAttr(curve.attr("worldSpace"), node.attr("geometryPath"))
    connectAttr(node.attr("allCoordinates"), obj.attr("translate"))
    connectAttr(node.attr("rotate"), obj.attr("rotate"))
    connectAttr(node.attr("rotateOrder"), obj.attr("rotateOrder"))
    connectAttr(node.attr("message"), obj.attr("specifiedManipLocation"))

    return node

# ========================================================
## Apply a direction constraint
# @param obj X3DObject - Constrained object.
# @param master X3DObject - Constraining Object.
# @param upv X3DObject - None of you don't want to use up vector
# @param comp Boolean - Active constraint compensation.
# @param axis String - Define pointing axis and upvector axis
# @return the newly created constraint.
def aimCns(obj, master, axis="xy", wupType=4, wupVector=[0,1,0], wupObject=None, maintainOffset=False):

    node = aimConstraint(master, obj, worldUpType=wupType, worldUpVector=wupVector, worldUpObject=wupObject, maintainOffset=maintainOffset)

    if axis == "xy": a = [1,0,0,0,1,0]
    elif axis == "xz": a = [1,0,0,0,0,1]
    elif axis == "yx": a = [0,1,0,1,0,0]
    elif axis == "yz": a = [0,1,0,0,0,1]
    elif axis == "zx": a = [0,0,1,1,0,0]
    elif axis == "zy": a = [0,0,1,0,1,0]

    elif axis == "-xy": a = [-1,0,0,0,1,0]
    elif axis == "-xz": a = [-1,0,0,0,0,1]
    elif axis == "-yx": a = [0,-1,0,1,0,0]
    elif axis == "-yz": a = [0,-1,0,0,0,1]
    elif axis == "-zx": a = [0,0,-1,1,0,0]
    elif axis == "-zy": a = [0,0,-1,0,1,0]

    elif axis == "x-y": a = [1,0,0,0,-1,0]
    elif axis == "x-z": a = [1,0,0,0,0,-1]
    elif axis == "y-x": a = [0,1,0,-1,0,0]
    elif axis == "y-z": a = [0,1,0,0,0,-1]
    elif axis == "z-x": a = [0,0,1,-1,0,0]
    elif axis == "z-y": a = [0,0,1,0,-1,0]

    elif axis == "-x-y": a = [-1,0,0,0,-1,0]
    elif axis == "-x-z": a = [-1,0,0,0,0,-1]
    elif axis == "-y-x": a = [0,-1,0,-1,0,0]
    elif axis == "-y-z": a = [0,-1,0,0,0,-1]
    elif axis == "-z-x": a = [0,0,-1,-1,0,0]
    elif axis == "-z-y": a = [0,0,-1,0,-1,0]

    for i, name in enumerate(["aimVectorX", "aimVectorY", "aimVectorZ", "upVectorX", "upVectorY", "upVectorZ"]):
        setAttr(node+"."+name, a[i])

    return node

#############################################
# CUSTOM NODES
#############################################
def gear_mulmatrix_op(mA, mB):

    node = createNode("gear_mulMatrix")

    connectAttr(mA, node+".matrixA")
    connectAttr(mB, node+".matrixB")

    return node

def gear_curvecns_op(crv, inputs=[]):

    select(crv)
    node = deformer(type="gear_curveCns")[0]

    for i, item in enumerate(inputs):
        connectAttr(item+".worldMatrix", node+".inputs[%s]"%i)

    return node

# gear_curveslide2_op =====================================
## Apply a sn_curveslide2_op operator
# @param outcrv NurbeCurve - Out Curve.
# @param incrv NurbeCurve - In Curve.
# @param position Double - Default position value (from 0 to 1).
# @param maxstretch Double - Default maxstretch value (from 1 to infinite).
# @param maxsquash Double - Default maxsquash value (from 0 to 1).
# @param softness Double - Default softness value (from 0 to 1).
# @return the newly created operator.
def gear_curveslide2_op(outcrv, incrv, position=0, maxstretch=1, maxsquash=1, softness=0):

    select(outcrv)
    node = deformer(type="gear_slideCurve2")[0]

    connectAttr(incrv+".local", node+".master_crv")
    connectAttr(incrv+".worldMatrix", node+".master_mat")

    setAttr(node+".master_length", arclen(incrv))
    setAttr(node+".slave_length", arclen(incrv))
    setAttr(node+".position", 0)
    setAttr(node+".maxstretch", 1)
    setAttr(node+".maxsquash", 1)
    setAttr(node+".softness", 0)

    return node

# Spine Point At ========================================
## Apply a SpinePointAt operator
# @param cns Constraint - The constraint to apply the operator on (must be a curve, path or direction constraint)
# @param startobj X3DObject - Start Reference.
# @param endobj X3DObject -End Reference.
# @param blend Double - Blend influence value from 0 to 1.
# @return the newly created operator.
def gear_spinePointAtOp(cns, startobj, endobj, blend=.5, axis="-Z"):

    node = createNode("gear_spinePointAt")

    # Inputs
    setAttr(node+".blend", blend)
    setAttr(node+".axe", ["X", "Y", "Z", "-X", "-Y", "-Z"].index(axis))

    connectAttr(startobj+".rotate", node+".rotA")
    connectAttr(endobj+".rotate", node+".rotB")

    # Outputs
    setAttr(cns+".worldUpType", 3)

    connectAttr(node+".pointAt", cns+".worldUpVector")

    return node

# ========================================================
## Apply a sn_ikfk2bone_op operator
# @param out List of X3DObject - The constrained outputs order must be respected (BoneA, BoneB,  Center, CenterN, Eff), set it to None if you don't want one of the output.
# @param root X3DObject - Object that will act as the root of the chain.
# @param eff X3DObject - Object that will act as the eff controler of the chain.
# @param upv X3DObject - Object that will act as the up vector of the chain.
# @param fk0 X3DObject - Object that will act as the first fk controler of the chain.
# @param fk1 X3DObject - Object that will act as the second fk controler of the chain.
# @param fk2 X3DObject - Object that will act as the fk effector controler of the chain.
# @param lengthA Double - Length of first bone.
# @param lengthB Double - Length of second bone.
# @param negate Boolean - Use with negative Scale.
# @param blend Double - Default blend value (0 for full ik, 1 for full fk).
# @return the newly created operator.
def gear_ikfk2bone_op(out=[], root=None, eff=None, upv=None, fk0=None, fk1=None, fk2=None, lengthA=5, lengthB=3, negate=False, blend=0):

    node = createNode("gear_ikfk2Bone")

    # Inputs
    setAttr(node+".lengthA", lengthA)
    setAttr(node+".lengthB", lengthB)
    setAttr(node+".negate", negate)
    setAttr(node+".blend", blend)

    connectAttr(root+".worldMatrix", node+".root")
    connectAttr(eff+".worldMatrix", node+".ikref")
    connectAttr(upv+".worldMatrix", node+".upv")
    connectAttr(fk0+".worldMatrix", node+".fk0")
    connectAttr(fk1+".worldMatrix", node+".fk1")
    connectAttr(fk2+".worldMatrix", node+".fk2")


    # Outputs
    if out[0] is not None:
        connectAttr(out[0]+".parentMatrix", node+".inAparent")

        dm_node = createNode("decomposeMatrix")
        connectAttr(node+".outA", dm_node+".inputMatrix")
        connectAttr(dm_node+".outputTranslate", out[0]+".translate")
        connectAttr(dm_node+".outputRotate", out[0]+".rotate")
        connectAttr(dm_node+".outputScale", out[0]+".scale")

    if out[1] is not None:
        connectAttr(out[1]+".parentMatrix", node+".inBparent")

        dm_node = createNode("decomposeMatrix")
        connectAttr(node+".outB", dm_node+".inputMatrix")
        connectAttr(dm_node+".outputTranslate", out[1]+".translate")
        connectAttr(dm_node+".outputRotate", out[1]+".rotate")
        connectAttr(dm_node+".outputScale", out[1]+".scale")

    if out[2] is not None:
        connectAttr(out[2]+".parentMatrix", node+".inCenterparent")

        dm_node = createNode("decomposeMatrix")
        connectAttr(node+".outCenter", dm_node+".inputMatrix")
        connectAttr(dm_node+".outputTranslate", out[2]+".translate")
        connectAttr(dm_node+".outputRotate", out[2]+".rotate")
        connectAttr(dm_node+".outputScale", out[2]+".scale")

    if out[3] is not None:
        connectAttr(out[3]+".parentMatrix", node+".inEffparent")

        dm_node = createNode("decomposeMatrix")
        connectAttr(node+".outEff", dm_node+".inputMatrix")
        connectAttr(dm_node+".outputTranslate", out[3]+".translate")
        connectAttr(dm_node+".outputRotate", out[3]+".rotate")
        connectAttr(dm_node+".outputScale", out[3]+".scale")

    return node


# sn_rollsplinekine_op ==================================
## Apply a sn_rollsplinekine_op operator
# @param out X3DObject - constrained Object.
# @param ctrl List of X3DObject - Objects that will act as controler of the bezier curve. Objects must have a parent that will be used as an input for the operator.
# @param u Double - Position of the object on the bezier curve (from 0 to 1).
# @return the newly created operator.
def gear_rollsplinekine_op(out, controlers=[], u=.5):

    node = createNode("gear_rollSplineKine")

    # Inputs
    setAttr(node+".u", u)

    dm_node = createNode("decomposeMatrix")

    connectAttr(node+".output", dm_node+".inputMatrix")
    connectAttr(dm_node+".outputTranslate", out+".translate")
    connectAttr(dm_node+".outputRotate", out+".rotate")
    # connectAttr(dm_node+".outputScale", out+".scale")

    connectAttr(out+".parentMatrix", node+".outputParent")

    for i, obj in enumerate(controlers):
        connectAttr(obj+".parentMatrix", node+".ctlParent[%s]"%i)

        connectAttr(obj+".worldMatrix", node+".inputs[%s]"%i)
        connectAttr(obj+".rx", node+".inputsRoll[%s]"%i)

    return node

# gear_squashstretch2_op ==================================
## Apply a sn_squashstretch2_op operator
# @param out X3DObject - Constrained object.
# @param sclref X3DObject - Global scaling reference object.
# @param length Double - Rest Length of the S&S.
# @param axis String - 'x' for scale all except x axis...
# @return the newly created operator.
def gear_squashstretch2_op(out, sclref=None, length=5, axis="x"):

    node = createNode("gear_squashStretch2")

    setAttr(node+".global_scaleX", 1)
    setAttr(node+".global_scaleY", 1)
    setAttr(node+".global_scaleZ", 1)
    setAttr(node+".driver_ctr", length)
    setAttr(node+".driver_max", length * 2)
    setAttr(node+".axis", "xyz".index(axis))

    connectAttr(node+".output", out+".scale")
    
    if sclref is not None:
        dm_node = createNode("decomposeMatrix")
        connectAttr(sclref+".worldMatrix", dm_node+".inputMatrix")
        connectAttr(dm_node+".outputScale", node+".global_scale")

    return node

# gear_inverseRotorder_op =====================================
## Apply a sn_inverseRotorder_op operator
# @return the newly created operator.
def gear_inverseRotorder_op(out_obj, in_obj):

    node = createNode("gear_inverseRotOrder")

    connectAttr(in_obj+".ro", node+".ro")
    connectAttr(node+".output", out_obj+".ro")

    return node
