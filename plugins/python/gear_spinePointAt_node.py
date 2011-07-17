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

## @package gear_spinePointAt_node.py
# @author Jeremie Passerin
#

'''
This node is a copy of the spinePointAt operator from Michael Isner created for Softimage XSI
More information about it : http://www.isner.com/isnerspine/spine_introduction.htm
'''

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
        plugin.registerNode('gear_spinePointAt', gear_spinePointAt.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_spinePointAt.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_spinePointAt() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs ----------------------------------------
    gear_spinePointAt.rotA = nAttr.createPoint("rotA", "ra" )
    gear_spinePointAt.rotAx = nAttr.child(0)
    gear_spinePointAt.rotAy = nAttr.child(1)
    gear_spinePointAt.rotAz = nAttr.child(2)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_spinePointAt.addAttribute( gear_spinePointAt.rotA )
    
    gear_spinePointAt.rotB = nAttr.createPoint("rotB", "rb" )
    gear_spinePointAt.rotBx = nAttr.child(0)
    gear_spinePointAt.rotBy = nAttr.child(1)
    gear_spinePointAt.rotBz = nAttr.child(2)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_spinePointAt.addAttribute( gear_spinePointAt.rotB )
    
    gear_spinePointAt.axe = eAttr.create( "axe", "a", 2 )
    eAttr.addField("X", 0)
    eAttr.addField("Y", 1)
    eAttr.addField("Z", 2)
    eAttr.addField("-X", 3)
    eAttr.addField("-Y", 4)
    eAttr.addField("-Z", 5)
    eAttr.setWritable(True)
    eAttr.setStorable(True)
    eAttr.setReadable(True)
    eAttr.setKeyable(False)
    gear_spinePointAt.addAttribute( gear_spinePointAt.axe )
    
    gear_spinePointAt.blend = nAttr.create( "blend", "b", OpenMaya.MFnNumericData.kFloat, 0.5 )
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(True)
    nAttr.setMin(0)
    nAttr.setMax(1)
    gear_spinePointAt.addAttribute( gear_spinePointAt.blend )

    # Outputs ---------------------------------------
    gear_spinePointAt.pointAt = nAttr.createPoint("pointAt", "pa" )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    gear_spinePointAt.addAttribute( gear_spinePointAt.pointAt )

    # Connections -----------------------------------
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotA, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotAx, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotAy, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotAz, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotB, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotBx, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotBy, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.rotBz, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.axe, gear_spinePointAt.pointAt )
    gear_spinePointAt.attributeAffects ( gear_spinePointAt.blend, gear_spinePointAt.pointAt )

# CLASS =============================================
class gear_spinePointAt(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000001)

    rotA = OpenMaya.MObject()
    rotB = OpenMaya.MObject()
    axe = OpenMaya.MObject()
    blend = OpenMaya.MObject()
    
    pointAt = OpenMaya.MObject()

    def compute(self, plug, data):
    
        # Error check
        if plug != gear_spinePointAt.pointAt:
            return OpenMaya.MStatus.kUnknownParameter
        
        # Get inputs
        inputData = data.inputValue( gear_spinePointAt.rotA )
        rotAx = inputData.child(gear_spinePointAt.rotAx).asFloat()
        rotAy = inputData.child(gear_spinePointAt.rotAy).asFloat()
        rotAz = inputData.child(gear_spinePointAt.rotAz).asFloat()
        
        inputData = data.inputValue( gear_spinePointAt.rotB )
        rotBx = inputData.child(gear_spinePointAt.rotBx).asFloat()
        rotBy = inputData.child(gear_spinePointAt.rotBy).asFloat()
        rotBz = inputData.child(gear_spinePointAt.rotBz).asFloat()
        
        axe = data.inputValue( gear_spinePointAt.axe ).asShort()
        
        blend = data.inputValue(gear_spinePointAt.blend).asFloat()
       
        # Process
        # There is no such thing as siTransformation in Maya, 
        # so what we really need to compute this +/-360 roll is the global rotation of the object
        # We then need to convert this eulerRotation to Quaternion
        # Maybe it would be faster to use the MEulerRotation class, but anyway, this code can do it
        qA = self.e2q(rotAx, rotAy, rotAz)
        qB = self.e2q(rotBx, rotBy, rotBz)
       
        qC = self.slerp2(qA, qB, blend)
        
        if axe == 0:
            vOut = OpenMaya.MVector(1,0,0)
        elif axe == 1:
            vOut = OpenMaya.MVector(0,1,0)
        elif axe == 2:
            vOut = OpenMaya.MVector(0,0,1)
        elif axe == 3:
            vOut = OpenMaya.MVector(-1,0,0)
        elif axe == 4:
            vOut = OpenMaya.MVector(0,-1,0)
        elif axe == 5:
            vOut = OpenMaya.MVector(0,0,-1)
        
        vOut = vOut.rotateBy(qC)
        x = vOut.x
        y = vOut.y
        z = vOut.z
        
        # Output
        
        h_pointAt = data.outputValue( gear_spinePointAt.pointAt )
        h_pointAt.set3Float( x, y, z )
        
        # BUG ? 
        # This one gives weird result
        # h_pointAt.setMVector( vOut )
        # This one doesn't work at all
        # h_pointAt.set3Float( vOut.x, vOut.y, vOut.z )
        
        data.setClean( plug )

        return OpenMaya.MStatus.kSuccess

    def e2q(self, x, y, z):

        x = dt.radians(x)
        y = dt.radians(y)
        z = dt.radians(z)

        # Assuming the angles are in radians.
        c1 = math.cos(y/2.0)
        s1 = math.sin(y/2.0)
        c2 = math.cos(z/2.0)
        s2 = math.sin(z/2.0)
        c3 = math.cos(x/2.0)
        s3 = math.sin(x/2.0)
        c1c2 = c1*c2
        s1s2 = s1*s2
        qw =c1c2*c3 - s1s2*s3
        qx =c1c2*s3 + s1s2*c3
        qy =s1*c2*c3 + c1*s2*s3
        qz =c1*s2*c3 - s1*c2*s3
        
        q = OpenMaya.MQuaternion(qx,qy,qz,qw)

        return q

    def slerp2(self, qA, qB, blend):
    
        dot = self.getDot(qA, qB)
        
        # if q1 and target are really close then we can interpolate linerarly.
        if dot >= (1 - 1.0e-12):
            scaleA = 1 - blend
            scaleB = blend
        else:
            # use standard spherical linear interpolation
            dot = self.clamp(dot, -1, 1)
        
        if round((-dot * dot+ 1),5) == 0:
            return qA
        else:
            angle = math.acos(dot)

        if round(math.sin(angle), 6) <> 0:
            factor = 1 / math.sin(angle)
        else:
            return qA

        scaleA = math.sin( (1.0 - blend) * angle ) * factor
        scaleB = math.sin( blend * angle ) * factor

        qx  = scaleA * qA.x + scaleB * qB.x
        qy  = scaleA * qA.y + scaleB * qB.y
        qz  = scaleA * qA.z + scaleB * qB.z
        qw  = scaleA * qA.w + scaleB * qB.w
        q = OpenMaya.MQuaternion(qx, qy, qz, qw)

        return q
        
    def clamp(self, d, min_value, max_value):

        d = max(d, min_value)
        d = min(d, max_value)
        return d
    
    def getDot(self, qA, qB):

        dot =  qA.w * qB.w + \
               qA.x * qB.x + \
               qA.y * qB.y + \
               qA.z * qB.z

        return dot

