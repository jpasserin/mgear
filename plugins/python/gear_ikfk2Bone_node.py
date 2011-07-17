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
    along with this program.  If not, see <http:#www.gnu.org/licenses/lgpl.html>.

    Author:     Jeremie Passerin      geerem@hotmail.com
    Date:       2011 / 07 / 13

'''

## @package gear_ikfk2Bone_node.py
# @author Jeremie Passerin
#

#####################################################
# GLOBAL
#####################################################
import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import pymel.core.datatypes as dt


#####################################################
# INIT / UNINIT
#####################################################
# INIT ==============================================
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Jeremie Passerin', '1.0', 'Any')
    try:
        plugin.registerNode('gear_ikfk2Bone', gear_ikfk2Bone.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_ikfk2Bone.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_ikfk2Bone() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs Matrices -------------------------------
    gear_ikfk2Bone.root = addMatrixAttr("root", "r")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.root )
    gear_ikfk2Bone.ikref = addMatrixAttr("ikref", "ik")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.ikref )
    gear_ikfk2Bone.upv = addMatrixAttr("upv", "upv")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.upv )
    gear_ikfk2Bone.fk0 = addMatrixAttr("fk0", "fk0")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.fk0 )
    gear_ikfk2Bone.fk1 = addMatrixAttr("fk1", "fk1")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.fk1 )
    gear_ikfk2Bone.fk2 = addMatrixAttr("fk2", "fk2")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.fk2 )

    gear_ikfk2Bone.inAparent = addMatrixAttr("inAparent", "ina")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.inAparent )
    gear_ikfk2Bone.inBparent = addMatrixAttr("inBparent", "inb")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.inBparent )
    gear_ikfk2Bone.inCenterparent = addMatrixAttr("inCenterparent", "inc")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.inCenterparent )
    gear_ikfk2Bone.inEffparent = addMatrixAttr("inEffparent", "ine")
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.inEffparent )

    # Inputs Sliders --------------------------------

    gear_ikfk2Bone.lengthA = addNumericAttr("lengthA", "lA", OpenMaya.MFnNumericData.kFloat, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.lengthA )
    gear_ikfk2Bone.lengthB = addNumericAttr("lengthB", "lB", OpenMaya.MFnNumericData.kFloat, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.lengthB )
    gear_ikfk2Bone.negate = addNumericAttr("negate", "n", OpenMaya.MFnNumericData.kBoolean, False)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.negate )

    gear_ikfk2Bone.blend = addNumericAttr("blend", "b", OpenMaya.MFnNumericData.kFloat, 1, 0, 1 )
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.blend )
    gear_ikfk2Bone.roll = addNumericAttr("roll", "ro", OpenMaya.MFnNumericData.kFloat, 0, -180, 180 )
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.roll )
    gear_ikfk2Bone.scaleA = addNumericAttr("scaleA", "sA", OpenMaya.MFnNumericData.kFloat, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.scaleA )
    gear_ikfk2Bone.scaleB = addNumericAttr("scaleB", "sB", OpenMaya.MFnNumericData.kFloat, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.scaleB )
    gear_ikfk2Bone.maxstretch = addNumericAttr("maxstretch", "ms", OpenMaya.MFnNumericData.kFloat, 1.5, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.maxstretch )
    gear_ikfk2Bone.softness = addNumericAttr("softness", "so", OpenMaya.MFnNumericData.kFloat, 0, 0, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.softness )
    gear_ikfk2Bone.slide = addNumericAttr("slide", "sl", OpenMaya.MFnNumericData.kFloat, 0.5, 0, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.slide )
    gear_ikfk2Bone.reverse = addNumericAttr("reverse", "re", OpenMaya.MFnNumericData.kFloat, 0, 0, 1)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.reverse )

    # Outputs ---------------------------------------

    gear_ikfk2Bone.outA = addMatrixAttr("outA", "outa", True, False, True, False)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.outA )
    gear_ikfk2Bone.outB = addMatrixAttr("outB", "outb", False, False, True, False)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.outB )
    gear_ikfk2Bone.outCenter = addMatrixAttr("outCenter", "outc", False, False, True, False)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.outCenter )
    gear_ikfk2Bone.outEff = addMatrixAttr("outEff", "oute", False, False, True, False)
    gear_ikfk2Bone.addAttribute( gear_ikfk2Bone.outEff )

    # Connections -----------------------------------
    addAttrAffects(gear_ikfk2Bone, gear_ikfk2Bone.outA, [ gear_ikfk2Bone.root, gear_ikfk2Bone.ikref, gear_ikfk2Bone.upv, 
                                                gear_ikfk2Bone.fk0, gear_ikfk2Bone.fk1, gear_ikfk2Bone.fk2,
                                                gear_ikfk2Bone.inAparent, gear_ikfk2Bone.inBparent, gear_ikfk2Bone.inCenterparent, gear_ikfk2Bone.inEffparent,
                                                gear_ikfk2Bone.lengthA, gear_ikfk2Bone.lengthB, gear_ikfk2Bone.negate,
                                                gear_ikfk2Bone.blend, gear_ikfk2Bone.roll, gear_ikfk2Bone.scaleA, gear_ikfk2Bone.scaleB,
                                                gear_ikfk2Bone.maxstretch, gear_ikfk2Bone.softness, gear_ikfk2Bone.slide, gear_ikfk2Bone.reverse])

    addAttrAffects(gear_ikfk2Bone, gear_ikfk2Bone.outB, [ gear_ikfk2Bone.root, gear_ikfk2Bone.ikref, gear_ikfk2Bone.upv,
                                                gear_ikfk2Bone.fk0, gear_ikfk2Bone.fk1, gear_ikfk2Bone.fk2,
                                                gear_ikfk2Bone.inAparent, gear_ikfk2Bone.inBparent, gear_ikfk2Bone.inCenterparent, gear_ikfk2Bone.inEffparent,
                                                gear_ikfk2Bone.lengthA, gear_ikfk2Bone.lengthB, gear_ikfk2Bone.negate,
                                                gear_ikfk2Bone.blend, gear_ikfk2Bone.roll, gear_ikfk2Bone.scaleA, gear_ikfk2Bone.scaleB,
                                                gear_ikfk2Bone.maxstretch, gear_ikfk2Bone.softness, gear_ikfk2Bone.slide, gear_ikfk2Bone.reverse])

    addAttrAffects(gear_ikfk2Bone, gear_ikfk2Bone.outCenter, [ gear_ikfk2Bone.root, gear_ikfk2Bone.ikref, gear_ikfk2Bone.upv,
                                                gear_ikfk2Bone.fk0, gear_ikfk2Bone.fk1, gear_ikfk2Bone.fk2,
                                                gear_ikfk2Bone.inAparent, gear_ikfk2Bone.inBparent, gear_ikfk2Bone.inCenterparent, gear_ikfk2Bone.inEffparent,
                                                gear_ikfk2Bone.lengthA, gear_ikfk2Bone.lengthB, gear_ikfk2Bone.negate,
                                                gear_ikfk2Bone.blend, gear_ikfk2Bone.roll, gear_ikfk2Bone.scaleA, gear_ikfk2Bone.scaleB,
                                                gear_ikfk2Bone.maxstretch, gear_ikfk2Bone.softness, gear_ikfk2Bone.slide, gear_ikfk2Bone.reverse])

    addAttrAffects(gear_ikfk2Bone, gear_ikfk2Bone.outEff, [ gear_ikfk2Bone.root, gear_ikfk2Bone.ikref, gear_ikfk2Bone.upv,
                                                gear_ikfk2Bone.fk0, gear_ikfk2Bone.fk1, gear_ikfk2Bone.fk2,
                                                gear_ikfk2Bone.inAparent, gear_ikfk2Bone.inBparent, gear_ikfk2Bone.inCenterparent, gear_ikfk2Bone.inEffparent,
                                                gear_ikfk2Bone.lengthA, gear_ikfk2Bone.lengthB, gear_ikfk2Bone.negate,
                                                gear_ikfk2Bone.blend, gear_ikfk2Bone.roll, gear_ikfk2Bone.scaleA, gear_ikfk2Bone.scaleB,
                                                gear_ikfk2Bone.maxstretch, gear_ikfk2Bone.softness, gear_ikfk2Bone.slide, gear_ikfk2Bone.reverse])

# CLASS =============================================
class gear_ikfk2Bone(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000002)

    out = OpenMaya.MObject()

    root = OpenMaya.MObject()
    ikref = OpenMaya.MObject()
    upv = OpenMaya.MObject()
    fk0 = OpenMaya.MObject()
    fk1 = OpenMaya.MObject()
    fk2 = OpenMaya.MObject()

    inAparent = OpenMaya.MObject()
    inBparent = OpenMaya.MObject()
    inCenterparent = OpenMaya.MObject()
    inEffparent = OpenMaya.MObject()

    lengthA = OpenMaya.MObject()
    lengthB = OpenMaya.MObject()
    negate = OpenMaya.MObject()

    blend = OpenMaya.MObject()
    roll = OpenMaya.MObject()
    scaleA = OpenMaya.MObject()
    scaleB = OpenMaya.MObject()
    maxstretch = OpenMaya.MObject()
    softness = OpenMaya.MObject()
    slide = OpenMaya.MObject()
    reverse = OpenMaya.MObject()

    outA = OpenMaya.MObject()
    outB = OpenMaya.MObject()
    outCenter = OpenMaya.MObject()
    outEff = OpenMaya.MObject()

    def compute(self, plug, data):

        # Get inputs matrices ------------------------------
        root = data.inputValue( gear_ikfk2Bone.root ).asMatrix()
        tmRoot = OpenMaya.MTransformationMatrix(root)
        ikref = data.inputValue( gear_ikfk2Bone.ikref ).asMatrix()
        tmIkRef = OpenMaya.MTransformationMatrix(ikref)
        upv = data.inputValue( gear_ikfk2Bone.upv ).asMatrix()
        tmUpV = OpenMaya.MTransformationMatrix(upv)

        inAparent = data.inputValue( gear_ikfk2Bone.inAparent ).asMatrix()
        inBparent = data.inputValue( gear_ikfk2Bone.inBparent ).asMatrix()
        inCenterparent = data.inputValue( gear_ikfk2Bone.inCenterparent ).asMatrix()
        inEffparent = data.inputValue( gear_ikfk2Bone.inEffparent ).asMatrix()

        fk0 = data.inputValue( gear_ikfk2Bone.fk0 ).asMatrix()
        tmFK0 = OpenMaya.MTransformationMatrix(fk0)
        fk1 = data.inputValue( gear_ikfk2Bone.fk1 ).asMatrix()
        tmFK1 = OpenMaya.MTransformationMatrix(fk1)
        fk2 = data.inputValue( gear_ikfk2Bone.fk2 ).asMatrix()
        tmFK2 = OpenMaya.MTransformationMatrix(fk2)

        # Get inputs sliders -------------------------------
        lengthA = data.inputValue(gear_ikfk2Bone.lengthA).asFloat()
        lengthB = data.inputValue(gear_ikfk2Bone.lengthB).asFloat()
        negate = data.inputValue(gear_ikfk2Bone.negate).asBool()

        blend = data.inputValue(gear_ikfk2Bone.blend).asFloat()
        roll = dt.radians(data.inputValue(gear_ikfk2Bone.roll).asFloat())
        scaleA = data.inputValue(gear_ikfk2Bone.scaleA).asFloat()
        scaleB = data.inputValue(gear_ikfk2Bone.scaleB).asFloat()
        maxstretch = data.inputValue(gear_ikfk2Bone.maxstretch).asFloat()
        softness = data.inputValue(gear_ikfk2Bone.softness).asFloat()
        slide = data.inputValue(gear_ikfk2Bone.slide).asFloat()
        reverse = data.inputValue(gear_ikfk2Bone.reverse).asFloat()

        outName = plug.name().split(".")[-1]

        # IK Parameters Dictionary
        ik = {}
        ik["root"] = tmRoot
        ik["eff"] = tmIkRef
        ik["upv"] = tmUpV

        ik["lengthA"] = lengthA
        ik["lengthB"] = lengthB
        ik["negate"] = negate
        ik["roll"] = roll
        ik["scaleA"] = scaleA
        ik["scaleB"] = scaleB
        ik["maxstretch"] = maxstretch
        ik["softness"] = softness
        ik["slide"] = slide
        ik["reverse"] = reverse

        # FK Parameters Dictionary
        fk = {}

        fk["root"] = tmRoot
        fk["bone1"] = tmFK0
        fk["bone2"] = tmFK1
        fk["eff"] = tmFK2

        fk["lengthA"] = lengthA
        fk["lengthB"] = lengthB
        fk["negate"] = negate

        # Process
        # for optimization
        if blend == 0.0:
            result = self.getFKTransform(fk, outName)
        elif blend == 1.0:
            result = self.getIKTransform(ik, outName)
        else:
            # here is where the blending happens!
            ikbone1 = self.getIKTransform(ik, "outA")
            ikbone2 = self.getIKTransform(ik, "outB")
            ikeff = self.getIKTransform(ik, "outEff")

            fkbone1 = self.getFKTransform(fk, "outA")
            fkbone2 = self.getFKTransform(fk, "outB")
            fkeff = self.getFKTransform(fk, "outEff")
            
            # remove scale to avoid shearing issue
            # This is not necessary in Softimage because the scaling hierarchy is not computed the same way. 
            util = OpenMaya.MScriptUtil()
            util.createFromDouble(1,1,1)
            ikbone1.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            ikbone2.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            ikeff.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            fkbone1.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            fkbone2.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            fkeff.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            
            # map the secondary transforms from global to local
            ikeff = self.mapWorldPoseToObjectSpace(ikbone2, ikeff)
            fkeff = self.mapWorldPoseToObjectSpace(fkbone2, fkeff)
            ikbone2 = self.mapWorldPoseToObjectSpace(ikbone1, ikbone2)
            fkbone2 = self.mapWorldPoseToObjectSpace(fkbone1, fkbone2)

            # now blend them!
            fk["bone1"] = self.interpolateTransform(fkbone1, ikbone1, blend)
            fk["bone2"] = self.interpolateTransform(fkbone2, ikbone2, blend)
            fk["eff"] = self.interpolateTransform(fkeff, ikeff, blend)
            

            # now map the local transform back to global!
            fk["bone2"] = self.mapObjectPoseToWorldSpace(fk["bone1"], fk["bone2"])
            fk["eff"] = self.mapObjectPoseToWorldSpace(fk["bone2"], fk["eff"])

            # calculate the result based on that
            result = self.getFKTransform(fk, outName)

        # Output
        if plug == gear_ikfk2Bone.outA:
            h_outA = data.outputValue( gear_ikfk2Bone.outA )
            h_outA.setMMatrix( result.asMatrix() * inAparent.inverse() )

            data.setClean( plug )

        elif plug == gear_ikfk2Bone.outB:
            h_outB = data.outputValue( gear_ikfk2Bone.outB )
            h_outB.setMMatrix( result.asMatrix() *  inBparent.inverse() )

            data.setClean( plug )

        elif plug == gear_ikfk2Bone.outCenter:
            h_outC = data.outputValue( gear_ikfk2Bone.outCenter )
            h_outC.setMMatrix( result.asMatrix() * inCenterparent.inverse() )

            data.setClean( plug )

        elif plug == gear_ikfk2Bone.outEff:
            h_outE = data.outputValue( gear_ikfk2Bone.outEff )
            h_outE.setMMatrix( result.asMatrix() * inEffparent.inverse() )

            data.setClean( plug )
        else:
            return OpenMaya.MStatus.kUnknownParameter

        return OpenMaya.MStatus.kSuccess


    # IK ###################################################
    def getIKTransform(self, data, name):

        # prepare all variables
        result = OpenMaya.MTransformationMatrix()
        bonePos = OpenMaya.MVector()
        rootPos = OpenMaya.MVector()
        effPos = OpenMaya.MVector()
        upvPos = OpenMaya.MVector()
        rootEff = OpenMaya.MVector()
        xAxis = OpenMaya.MVector()
        yAxis = OpenMaya.MVector()
        zAxis = OpenMaya.MVector()
        rollAxis = OpenMaya.MVector()

        rootPos = data["root"].getTranslation(OpenMaya.MSpace.kWorld)
        effPos = data["eff"].getTranslation(OpenMaya.MSpace.kWorld)
        upvPos = data["upv"].getTranslation(OpenMaya.MSpace.kWorld)
        rootEff = effPos - rootPos
        rollAxis = rootEff.normal()

        rootEffDistance = rootEff.length()

        # init the scaling
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        data["root"].getScale(ptr, OpenMaya.MFnMatrixAttribute.kDouble)
        global_scale = util.getDoubleArrayItem(ptr, 0);
        
        util.createFromDouble(global_scale, global_scale, global_scale)
        result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)

        # Distance with MaxStretch ---------------------
        restLength = (data["lengthA"] * data["scaleA"] + data["lengthB"] * data["scaleB"]) * global_scale
        distance = rootEffDistance
        distance2 = distance
        if distance > (restLength * (data["maxstretch"])):
            distance = restLength * data["maxstretch"]

        # Adapt Softness value to chain length --------
        data["softness"] = data["softness"] * restLength * .1

        # Stretch and softness ------------------------
        # We use the real distance from root to controler to calculate the softness
        # This way we have softness working even when there is no stretch
        stretch = max(1, distance / restLength)
        da = restLength - data["softness"]
        if (data["softness"] > 0) and (distance2 > da):
            newlen = data["softness"]*(1.0 - math.exp(-(distance2 -da)/data["softness"])) + da
            stretch = distance / newlen;

        data["lengthA"] = data["lengthA"] * stretch * data["scaleA"] * global_scale
        data["lengthB"] = data["lengthB"] * stretch * data["scaleB"] * global_scale

        # Reverse -------------------------------------
        d = distance / (data["lengthA"] + data["lengthB"])

        if data["reverse"] < 0.5:
            reverse_scale = 1-(data["reverse"]*2 * (1-d))
        else:
            reverse_scale = 1-((1-data["reverse"])*2 * (1-d))

        data["lengthA"] *= reverse_scale
        data["lengthB"] *= reverse_scale

        invert = data["reverse"] > 0.5

        # Slide ---------------------------------------
        if data["slide"] < .5:
            slide_add = (data["lengthA"] * (data["slide"] * 2)) - (data["lengthA"])
        else:
            slide_add = (data["lengthB"] * (data["slide"] * 2)) - (data["lengthB"])

        data["lengthA"] += slide_add
        data["lengthB"] -= slide_add

        # calculate the angle inside the triangle!
        angleA = 0
        angleB = 0

        # check if the divider is not null otherwise the result is nan
        # and the output disapear from xsi, that breaks constraints
        if(rootEffDistance < data["lengthA"] + data["lengthB"]) and (rootEffDistance > math.fabs(data["lengthA"] - data["lengthB"]) + 1E-6):

            # use the law of cosine for lengthA
            a = data["lengthA"]
            b = rootEffDistance
            c = data["lengthB"]

            angleA = math.acos(min(1, (a * a + b * b - c * c ) / ( 2 * a * b)))

            # use the law of cosine for lengthB
            a = data["lengthB"]
            b = data["lengthA"]
            c = rootEffDistance
            angleB = math.acos(min(1, (a * a + b * b - c * c ) / ( 2 * a * b)))

            # invert the angles if need be
            if invert:
                angleA = -angleA
                angleB = -angleB

        # start with the X and Z axis
        xAxis = rootEff
        xAxis.normalize()
        yAxis = self.linearlyInterpolate(rootPos, effPos, .5)
        yAxis = upvPos - yAxis
        yAxis.normalize()
        yAxis = self.rotateVectorAlongAxis(yAxis, rollAxis, data["roll"])
        zAxis = xAxis ^ yAxis
        zAxis.normalize()
        yAxis = zAxis ^ xAxis
        yAxis.normalize()
        
        # switch depending on our mode
        if name == "outA":

            # check if we need to rotate the bone
            if angleA != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -angleA)

            if data["negate"]:
                xAxis *= -1
            # cross the yAxis and normalize
            yAxis = zAxis ^ xAxis
            yAxis.normalize()

            # output the rotation
            q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)

            # set the scaling + the position
            util = OpenMaya.MScriptUtil()
            util.createFromDouble(data["lengthA"], global_scale, global_scale)
            result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            result.setTranslation(rootPos, OpenMaya.MSpace.kWorld)

        elif name == "outB":

            # check if we need to rotate the bone
            if angleA != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -angleA)

            # calculate the position of the elbow!
            bonePos = xAxis * data["lengthA"]
            bonePos += rootPos

            # check if we need to rotate the bone
            if angleB != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -(angleB - math.pi))

            if data["negate"]:
                xAxis *= -1

            # cross the yAxis and normalize
            yAxis = zAxis ^ xAxis
            yAxis.normalize()

            # output the rotation
            q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)

            # set the scaling + the position
            util = OpenMaya.MScriptUtil()
            util.createFromDouble(data["lengthB"], global_scale, global_scale)
            result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
            result.setTranslation(bonePos, OpenMaya.MSpace.kWorld)

        elif name == "outCenter":

            # check if we need to rotate the bone
            if angleA != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -angleA)

            # calculate the position of the elbow!
            bonePos = xAxis * data["lengthA"]
            bonePos += rootPos

            # check if we need to rotate the bone
            if angleB != 0.0:
                if invert:
                    angleB += math.pi * 2

                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -(angleB *.5 - math.pi*.5))

            # cross the yAxis and normalize
            # yAxis.Sub(upvPos,bonePos); # this was flipping the centerN when the elbow/upv was aligned to root/eff
            zAxis = xAxis ^ yAxis
            zAxis.normalize()

            if data["negate"]:
                xAxis *= -1

            yAxis = zAxis ^ xAxis
            yAxis.normalize()

            # output the rotation
            q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)

            # set the scaling + the position
            # result.SetSclX(stretch * data["root.GetSclX());

            result.setTranslation(bonePos, OpenMaya.MSpace.kWorld)

        elif name == "outEff":

            # check if we need to rotate the bone
            effPos = rootPos
            if angleA != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -angleA)

            # calculate the position of the elbow!
            bonePos = xAxis * data["lengthA"]
            effPos += bonePos

            # check if we need to rotate the bone
            if angleB != 0.0:
                xAxis = self.rotateVectorAlongAxis(xAxis, zAxis, -(angleB - math.pi))

            # calculate the position of the effector!
            bonePos = xAxis * data["lengthB"]
            effPos += bonePos

            # output the rotation
            result = data["eff"]
            result.setTranslation(effPos, OpenMaya.MSpace.kWorld)

        return result

    # FK ####################################################################
    def getFKTransform(self, data, name):

        #prepare all variables
        result = OpenMaya.MTransformationMatrix()

        xAxis = OpenMaya.MVector()
        yAxis = OpenMaya.MVector()
        zAxis = OpenMaya.MVector()

        if name == "outA":
            result = data["bone1"]
            xAxis = data["bone2"].getTranslation(OpenMaya.MSpace.kWorld) - data["bone1"].getTranslation(OpenMaya.MSpace.kWorld)

            util = OpenMaya.MScriptUtil()
            util.createFromDouble(xAxis.length(), 1.0, 1.0)
            result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)

            if data["negate"]:
                xAxis *= -1

            # cross the yAxis and normalize
            xAxis.normalize()
            
            zAxis = OpenMaya.MVector(0,0,1)
            zAxis = zAxis.rotateBy(data["bone1"].rotation())
            yAxis = zAxis ^ xAxis

            # rotation
            q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)

        elif name == "outB":

            result = data["bone2"]
            xAxis = data["eff"].getTranslation(OpenMaya.MSpace.kWorld) - data["bone2"].getTranslation(OpenMaya.MSpace.kWorld)

            util = OpenMaya.MScriptUtil()
            util.createFromDouble(xAxis.length(), 1.0, 1.0)
            result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)

            if data["negate"]:
                xAxis *= -1

            # cross the yAxis and normalize
            xAxis.normalize()
            yAxis = OpenMaya.MVector(0,1,0)
            yAxis = yAxis.rotateBy(data["bone2"].rotation())
            zAxis = xAxis ^ yAxis
            zAxis.normalize()
            yAxis = zAxis ^ xAxis
            yAxis.normalize()

            # rotation
            q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)

        elif name == "outCenter":
        
        
            # Only +/-180 degree with this one but we don't get the shear issue anymore
            t = self.mapWorldPoseToObjectSpace(data["bone1"], data["bone2"])
            er = t.eulerRotation()
            er *= .5
            q = er.asQuaternion()
            t.setRotationQuaternion(q.x, q.y, q.z, q.w)
            t = self.mapObjectPoseToWorldSpace(data["bone1"], t)
            q = t.rotation()
        
            #q = self.slerp(data["bone1"].rotation(), data["bone2"].rotation(), .5)
            result.setRotationQuaternion(q.x, q.y, q.z, q.w)
            
            # rotation
            result.setTranslation(data["bone2"].getTranslation(OpenMaya.MSpace.kWorld), OpenMaya.MSpace.kWorld)


        elif name == "outEff":
            result = data["eff"]

        return result

    def rotateVectorAlongAxis(self, v, axis, a):

        # Angle as to be in radians

        sa = math.sin(a / 2.0)
        ca = math.cos(a / 2.0)

        q1 = OpenMaya.MQuaternion(v.x, v.y, v.z, 0)
        q2 = OpenMaya.MQuaternion(axis.x * sa, axis.y * sa, axis.z * sa, ca)
        q2n = OpenMaya.MQuaternion(-axis.x * sa, -axis.y * sa, -axis.z * sa, ca)
        q = q2 * q1
        q *= q2n

        out = OpenMaya.MVector(q.x, q.y, q.z)

        return out

    def linearlyInterpolate(self, v0, v1, blend=.5):

        vector = v1 - v0
        vector *= blend
        vector += v0

        return vector

    def interpolateTransform(self, xf1, xf2, blend):

        if blend == 1.0:
            return xf2
        elif blend == 0.0:
            return xf1

        # translate
        resultPos = self.linearlyInterpolate(xf1.getTranslation(OpenMaya.MSpace.kWorld), xf2.getTranslation(OpenMaya.MSpace.kWorld), blend)

        # scale
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        xf1.getScale(ptr, OpenMaya.MFnMatrixAttribute.kDouble)
        xf1_scl = OpenMaya.MVector(util.getDoubleArrayItem(ptr, 0), util.getDoubleArrayItem(ptr, 1), util.getDoubleArrayItem(ptr, 2))

        
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        xf2.getScale(ptr, OpenMaya.MFnMatrixAttribute.kDouble)
        xf2_scl = OpenMaya.MVector(util.getDoubleArrayItem(ptr, 0), util.getDoubleArrayItem(ptr, 1), util.getDoubleArrayItem(ptr, 2))

        resultScl = self.linearlyInterpolate(xf1_scl, xf2_scl, blend)
        
        # rotate
        resultQuat = self.slerp(xf1.rotation() ,xf2.rotation(), blend)
        
        # out
        result = OpenMaya.MTransformationMatrix()

        util = OpenMaya.MScriptUtil()
        util.createFromDouble(resultScl.x, resultScl.y, resultScl.z)
        result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)
        result.setRotationQuaternion(resultQuat.x,resultQuat.y,resultQuat.z,resultQuat.w)
        result.setTranslation(resultPos, OpenMaya.MSpace.kWorld)

        return result;

    def slerp(self, qa, qb, t):

        # Calculate angle between them.
        cosHalfTheta = qa.w * qb.w + qa.x * qb.x + qa.y * qb.y + qa.z * qb.z
        # if qa=qb or qa=-qb then theta = 0 and we can return qa
        if math.fabs(cosHalfTheta) >= 1.0:
            return qa

        # Calculate temporary values.
        halfTheta = math.acos(cosHalfTheta)
        sinHalfTheta = math.sqrt(1.0 - cosHalfTheta*cosHalfTheta)
        # if theta = 180 degrees then result is not fully defined
        # we could rotate around any axis normal to qa or qb
        if math.fabs(sinHalfTheta) < 0.001: # fabs is floating point absolute
            w = (qa.w * 0.5 + qb.w * 0.5)
            x = (qa.x * 0.5 + qb.x * 0.5)
            y = (qa.y * 0.5 + qb.y * 0.5)
            z = (qa.z * 0.5 + qb.z * 0.5)
            qm = OpenMaya.MQuaternion(x,y,z,w)
            return qm

        ratioA = math.sin((1 - t) * halfTheta) / sinHalfTheta;
        ratioB = math.sin(t * halfTheta) / sinHalfTheta;
        #calculate Quaternion.
        w = (qa.w * ratioA + qb.w * ratioB);
        x = (qa.x * ratioA + qb.x * ratioB);
        y = (qa.y * ratioA + qb.y * ratioB);
        z = (qa.z * ratioA + qb.z * ratioB);
        qm = OpenMaya.MQuaternion(x,y,z,w)
        return qm

    def getQuaternionFromAxes(self, vx, vy, vz):

        data = [round(vx.x,4), round(vx.y,4), round(vx.z,4), 0 ,
                round(vy.x,4), round(vy.y,4), round(vy.z,4), 0 ,
                round(vz.x,4), round(vz.y,4), round(vz.z,4), 0 ,
                0, 0, 0, 1]
    
        m = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( data , m)
        tm = OpenMaya.MTransformationMatrix(m)

        return tm.rotation()

    def mapWorldPoseToObjectSpace(self, objectSpace, pose):
        return OpenMaya.MTransformationMatrix(pose.asMatrix() * objectSpace.asMatrixInverse())

    def mapObjectPoseToWorldSpace(self, objectSpace, pose):
        return OpenMaya.MTransformationMatrix(pose.asMatrix() * objectSpace.asMatrix())

#####################################################
# ADD ATTRIBUTE METHODS
#####################################################
def addNumericAttr(name, short, data_type, default=0, min_value=None, max_value=None, writable=True, storable=True, readable=True, keyable=True):

    nAttr = OpenMaya.MFnNumericAttribute()

    attr = nAttr.create( name, short, data_type, default )
    nAttr.setWritable(writable)
    nAttr.setStorable(storable)
    nAttr.setReadable(readable)
    nAttr.setKeyable(keyable)
    if min_value is not None:
        nAttr.setMin(min_value)
    if max_value is not None:
        nAttr.setMax(max_value)

    return attr

def addMatrixAttr(name, short, writable=True, storable=True, readable=False, keyable=False):

    mAttr = OpenMaya.MFnMatrixAttribute()

    attr = mAttr.create( name, short, OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setWritable(writable)
    mAttr.setStorable(storable)
    mAttr.setReadable(readable)
    mAttr.setKeyable(keyable)
    mAttr.setConnectable(True)

    return attr

def addAttrAffects(node, outAttr, inAttr=[]):

    for attr in inAttr:
        node.attributeAffects ( attr, outAttr )
