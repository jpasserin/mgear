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

## @package gear_uToPercentage.py
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
        plugin.registerNode('gear_uToPercentage', gear_uToPercentage.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_uToPercentage.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_uToPercentage() )

# INIT ==============================================
def initialize():

    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs ----------------------------------------
    # Curve
    gear_uToPercentage.curve = tAttr.create('curve', 'crv', OpenMaya.MFnData.kNurbsCurve)
    gear_uToPercentage.addAttribute( gear_uToPercentage.curve )

    # Sliders
    gear_uToPercentage.normalizedU = addNumericAttr("normalizedU", "n", OpenMaya.MFnNumericData.kBoolean, False)
    gear_uToPercentage.addAttribute( gear_uToPercentage.normalizedU )
    gear_uToPercentage.u = addNumericAttr("u", "u", OpenMaya.MFnNumericData.kFloat, .5, 0)
    gear_uToPercentage.addAttribute( gear_uToPercentage.u )
    gear_uToPercentage.steps = addNumericAttr("steps", "s", OpenMaya.MFnNumericData.kShort, 40, 1)
    gear_uToPercentage.addAttribute( gear_uToPercentage.steps )

    # Outputs ---------------------------------------
    gear_uToPercentage.percentage = nAttr.create( "percentage", "p", OpenMaya.MFnNumericData.kFloat, 0 )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_uToPercentage.addAttribute( gear_uToPercentage.percentage )

    # Connections -----------------------------------
    gear_uToPercentage.attributeAffects ( gear_uToPercentage.curve, gear_uToPercentage.percentage )
    gear_uToPercentage.attributeAffects ( gear_uToPercentage.steps, gear_uToPercentage.percentage )
    gear_uToPercentage.attributeAffects ( gear_uToPercentage.u, gear_uToPercentage.percentage )
    gear_uToPercentage.attributeAffects ( gear_uToPercentage.normalizedU, gear_uToPercentage.percentage )

# CLASS =============================================
class gear_uToPercentage(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000009)

    curve = OpenMaya.MObject()

    normalizedU = OpenMaya.MObject()
    u = OpenMaya.MObject()
    steps = OpenMaya.MObject()
    percentage = OpenMaya.MObject()

    def compute(self, plug, data):

        # Inputs ------------------------------------
        # Input NurbsCurve
        curve = data.inputValue(gear_uToPercentage.curve).asNurbsCurve()
        if curve.isNull():
            return OpenMaya.MStatus.kSuccess
        curve = OpenMaya.MFnNurbsCurve(curve)

        # Sliders
        normalizedU = data.inputValue(gear_uToPercentage.normalizedU).asBool()
        u = data.inputValue(gear_uToPercentage.u).asFloat()
        steps = data.inputValue(gear_uToPercentage.steps).asShort()
        
        # Process -----------------------------------
        if normalizedU:
            u = self.normalizedUToU(u, curve.numCVs())

        # Get length at u position
        positions = []
        pt = OpenMaya.MPoint()
        for i in range(steps):
            step = i *  u/(steps - 1.0)
            curve.getPointAtParam(step, pt, OpenMaya.MSpace.kWorld)
            positions.append(OpenMaya.MVector(pt))

        inter = [ positions[i] - positions[i-1] for i in range(len(positions)) if i > 0 ]
        dist = [ v.length() for v in inter ]
        u_length = sum(dist)

        # Get total length
        positions = []
        pt = OpenMaya.MPoint()
        for i in range(steps):
            step = i/(steps - 1.0)
            curve.getPointAtParam(step, pt, OpenMaya.MSpace.kWorld)
            positions.append(OpenMaya.MVector(pt))

        inter = [ positions[i] - positions[i-1] for i in range(len(positions)) if i > 0 ]
        dist = [ v.length() for v in inter ]
        total_length = sum(dist)

        # Get Percentage
        percentage = ( u_length / total_length ) * 100

        # Outputs -----------------------------------
        if plug == gear_uToPercentage.percentage:
            h = data.outputValue( gear_uToPercentage.percentage )
            h.setFloat( percentage )

            data.setClean( plug )
        else:
            return OpenMaya.MStatus.kUnknownParameter

        return OpenMaya.MStatus.kSuccess

    # ===============================================
    def normalizedUToU(self, u, point_count):
        return u*(point_count-3.0)

    def uToNormalizedU(self, u, point_count):
        return u/(point_count-3.0)

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

def addAttrAffects(node, outAttr, inAttr=[]):

    for attr in inAttr:
        node.attributeAffects ( attr, outAttr )
