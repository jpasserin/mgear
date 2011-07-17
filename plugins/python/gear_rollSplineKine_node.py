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

## @package gear_rollSplineKine_node.py
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
        plugin.registerNode('gear_rollSplineKine', gear_rollSplineKine.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_rollSplineKine.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_rollSplineKine() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs Matrices -------------------------------
    gear_rollSplineKine.ctlParent = mAttr.create( "ctlParent", "ctlp", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setStorable(True)
    mAttr.setReadable(False)
    mAttr.setIndexMatters(False)
    mAttr.setArray(True)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.ctlParent )

    gear_rollSplineKine.inputs = mAttr.create( "inputs", "in", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setStorable(True)
    mAttr.setReadable(False)
    mAttr.setIndexMatters(False)
    mAttr.setArray(True)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.inputs )

    gear_rollSplineKine.inputsRoll = nAttr.create ( "inputsRoll", "inr", OpenMaya.MFnNumericData.kFloat, 0.0 )
    nAttr.setArray(True)
    nAttr.setStorable(True)
    gear_rollSplineKine.addAttribute ( gear_rollSplineKine.inputsRoll )

    gear_rollSplineKine.outputParent = addMatrixAttr("outputParent", "outp")
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.outputParent )

    # Inputs Sliders --------------------------------

    gear_rollSplineKine.u = addNumericAttr("u", "u", OpenMaya.MFnNumericData.kFloat, .5, 0, 1)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.u )
    gear_rollSplineKine.resample = addNumericAttr("resample", "re", OpenMaya.MFnNumericData.kBoolean, False)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.resample )
    gear_rollSplineKine.subdiv = addNumericAttr("subdiv", "sd", OpenMaya.MFnNumericData.kLong, 10, 3 )
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.subdiv )
    gear_rollSplineKine.absolute = addNumericAttr("absolute", "abs", OpenMaya.MFnNumericData.kBoolean, False)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.absolute )

    # Outputs ---------------------------------------
    gear_rollSplineKine.output = addMatrixAttr("output", "out", True, False, True, False)
    gear_rollSplineKine.addAttribute( gear_rollSplineKine.output )

    # Connections -----------------------------------
    addAttrAffects(gear_rollSplineKine, gear_rollSplineKine.output, [ gear_rollSplineKine.ctlParent, gear_rollSplineKine.inputs, gear_rollSplineKine.inputsRoll, gear_rollSplineKine.outputParent,
                                                            gear_rollSplineKine.u, gear_rollSplineKine.resample, gear_rollSplineKine.subdiv, gear_rollSplineKine.absolute ])

# CLASS =============================================
class gear_rollSplineKine(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000003)

    ctlParent = OpenMaya.MObject()
    outputParent = OpenMaya.MObject()

    u = OpenMaya.MObject()
    resample = OpenMaya.MObject()
    subdiv = OpenMaya.MObject()
    absolute = OpenMaya.MObject()

    output = OpenMaya.MObject()

    def compute(self, plug, data):


        # Get inputs matrices ------------------------------
        # Inputs Parent
        dh_inputP = data.inputArrayValue( gear_rollSplineKine.ctlParent )
        inputsP = []
        for i in range(dh_inputP.elementCount()):
                dh_inputP.jumpToElement(i)
                inputsP.append(dh_inputP.inputValue().asMatrix())
        tmInP = [OpenMaya.MTransformationMatrix(m) for m in inputsP ]

        # Inputs
        dh_inputs = data.inputArrayValue( gear_rollSplineKine.inputs )
        inputs = []
        for i in range(dh_inputs.elementCount()):
                dh_inputs.jumpToElement(i)
                inputs.append(dh_inputs.inputValue().asMatrix())
        tmIn = [OpenMaya.MTransformationMatrix(m) for m in inputs ]

        dh_inputsR = data.inputArrayValue( gear_rollSplineKine.inputsRoll )
        inputsR = []
        roll = []
        for i in range(dh_inputsR.elementCount()):
                dh_inputsR.jumpToElement(i)
                inputsR.append(dh_inputsR.inputValue().asFloat())

                roll.append(dt.radians(dh_inputsR.inputValue().asFloat()))

        # Output Parent
        outputParent = data.inputValue( gear_rollSplineKine.outputParent ).asMatrix()

        # Get inputs sliders -------------------------------
        count = dh_inputs.elementCount()
        u = data.inputValue(gear_rollSplineKine.u).asFloat()
        resample = data.inputValue(gear_rollSplineKine.resample).asBool()
        subdiv = data.inputValue(gear_rollSplineKine.subdiv).asLong()
        absolute = data.inputValue(gear_rollSplineKine.absolute).asBool()

        if count < 1:
            return

        # Process ------------------------------------------
        # Get roll, pos, tan, rot, scl

        pos = []
        tan = []
        rot = []
        scl = []

        for mParent, m in zip(tmInP, tmIn):
            # Get the roll value
            # roll.append(m.eulerRotation().x)

            # map the object to world space and get pos, tan, rot and scl
            # m = self.mapObjectPoseToWorldSpace(mParent, m)
            pos.append( m.getTranslation(OpenMaya.MSpace.kWorld) )
            rot.append(mParent.rotation())

            util = OpenMaya.MScriptUtil()
            util.createFromDouble(0.0, 0.0, 0.0)
            ptr = util.asDoublePtr()
            m.getScale(ptr, OpenMaya.MFnMatrixAttribute.kDouble)
            scl.append(OpenMaya.MVector(util.getDoubleArrayItem(ptr, 0), util.getDoubleArrayItem(ptr, 1), util.getDoubleArrayItem(ptr, 2)))
            tan.append(OpenMaya.MVector(util.getDoubleArrayItem(ptr, 0)*2.5,0,0).rotateBy(m.rotation()))

        modelXF = tmInP[0]

        # Get step and indexes
        # We define between wich controlers the object is to be able to
        # calculate the bezier 4 points front this 2 objects
        step = 1.0 / max(1, count-1)
        index1 = int(min(count-2, u/step))
        index2 = index1 + 1
        index1temp = index1
        index2temp = index2
        v = (u - step * index1) / step
        vtemp = v

        # calculate the bezier
        if not resample: # straight bezier solve
            bezierPos, xAxis = self.bezier4point(pos[index1], tan[index1], pos[index2], tan[index2], v)

        elif not absolute:

            presample=[None]*subdiv
            presampletan=[None]*subdiv
            samplelen=[0.0]*subdiv
            samplestep = 1.0 / (subdiv-1.0)
            sampleu = samplestep

            presample[0] = pos[index1]
            presampletan[0] = tan[index1]

            prevsample = pos[index1]

            overalllen = 0

            for i in range(1, subdiv):


                p, t = self.bezier4point(pos[index1], tan[index1], pos[index2], tan[index2], sampleu)
                presample[i] = p
                presampletan[i] = t

                diff = p - prevsample
                overalllen += diff.length()
                samplelen[i] = overalllen
                prevsample = p

                sampleu += samplestep

            sampleu = 0

            for i in range(subdiv-1):

                samplelen[i+1] = samplelen[i+1] / (overalllen+0.0)
                if v >= samplelen[i] and v <= samplelen[i+1]:
                    v = (v - samplelen[i]) / (samplelen[i+1] - samplelen[i])
                    bezierPos = self.linearlyInterpolate(presample[i], presample[i+1], v)
                    xAxis = self.linearlyInterpolate(presampletan[i], presampletan[i+1], v)
                    break

                sampleu += samplestep

        else:
            presample=[None]*subdiv
            presampletan=[None]*subdiv
            samplelen=[0]*subdiv

            samplestep = 1.0 / (subdiv-1.0)
            sampleu = samplestep

            presample[0] = pos[0]
            presampletan[0] = tan[0]

            prevsample = pos[0]
            samplelen[0] = 0

            overalllen = 0
            for i in range(1,subdiv):

                index1 = int(min(count-2,sampleu / step))
                index2 = index1+1
                v = (sampleu - step * index1) / step

                p, t = self.bezier4point(pos[index1],tan[index1],pos[index2],tan[index2],v)
                presample[i] = p
                presampletan[i] = t

                diff = p - prevsample
                overalllen += diff.length()
                samplelen[i] = overalllen
                prevsample = p

                sampleu += samplestep

            sampleu = 0
            for i in range(subdiv-1):

                samplelen[i+1] = samplelen[i+1] / overalllen
                if u >= samplelen[i] and u <= samplelen[i+1]:
                    u = (u - samplelen[i]) / (samplelen[i+1] - samplelen[i])
                    bezierPos = self.linearlyInterpolate(presample[i], presample[i+1], u)
                    xAxis = self.linearlyInterpolate(presampletan[i], presampletan[i+1], u)
                    break

                sampleu += samplestep

        # compute the scaling (straight interpolation!)
        scl1 = self.linearlyInterpolate(scl[index1temp], scl[index2temp],vtemp)

        # compute the rotation!
        q = self.slerp(rot[index1temp], rot[index2temp], vtemp)
        yAxis = OpenMaya.MVector(0,1,0).rotateBy(q)

        # use directly or project the roll values!
        # print roll
        a = roll[index1temp] * (1.0 - vtemp) + roll[index2temp] * vtemp
        xAxis.normalize()
        yAxis = yAxis.rotateBy( OpenMaya.MQuaternion(xAxis.x * math.sin(a/2.0), xAxis.y * math.sin(a/2.0), xAxis.z * math.sin(a/2.0), math.cos(a/2.0)))

        zAxis = xAxis ^ yAxis
        yAxis = zAxis ^ xAxis
        xAxis.normalize()
        yAxis.normalize()
        zAxis.normalize()

        # Output -------------------------------------------
        result = OpenMaya.MTransformationMatrix()

        # translation
        result.setTranslation(bezierPos, OpenMaya.MSpace.kWorld)
        # rotation
        q = self.getQuaternionFromAxes(xAxis,yAxis,zAxis)
        result.setRotationQuaternion(q.x, q.y, q.z, q.w)
        # scaling
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(1, scl1.y, scl1.z)
        result.setScale(util.asDoublePtr(), OpenMaya.MFnMatrixAttribute.kDouble)

        if plug == gear_rollSplineKine.output:
            h = data.outputValue( gear_rollSplineKine.output )
            h.setMMatrix( result.asMatrix() * outputParent.inverse() )

            data.setClean( plug )
        else:
            return OpenMaya.MStatus.kUnknownParameter

        return OpenMaya.MStatus.kSuccess

    # ======================================================
    def bezier4point(self, a, tan_a, d, tan_d, u):

        b = a + tan_a
        c = d - tan_d

        ab = self.linearlyInterpolate(a,b,u)
        bc = self.linearlyInterpolate(b,c,u)
        cd = self.linearlyInterpolate(c,d,u)
        abbc = self.linearlyInterpolate(ab,bc,u)
        bccd = self.linearlyInterpolate(bc,cd,u)
        abbcbccd = self.linearlyInterpolate(abbc,bccd,u)

        return abbcbccd, bccd - abbc

    def linearlyInterpolate(self, v0, v1, blend=.5):

        vector = v1 - v0
        vector *= blend
        vector += v0

        return vector

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
