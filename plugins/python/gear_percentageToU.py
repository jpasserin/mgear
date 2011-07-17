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

## @package gear_percentageToU.py
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
        plugin.registerNode('gear_percentageToU', gear_percentageToU.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_percentageToU.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_percentageToU() )

# INIT ==============================================
def initialize():

    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs ----------------------------------------
    # Curve
    gear_percentageToU.curve = tAttr.create('curve', 'crv', OpenMaya.MFnData.kNurbsCurve)
    gear_percentageToU.addAttribute( gear_percentageToU.curve )

    # Sliders
    gear_percentageToU.normalizedU = addNumericAttr("normalizedU", "n", OpenMaya.MFnNumericData.kBoolean, False)
    gear_percentageToU.addAttribute( gear_percentageToU.normalizedU )
    gear_percentageToU.percentage = addNumericAttr("percentage", "p", OpenMaya.MFnNumericData.kFloat, 50, 0, 100)
    gear_percentageToU.addAttribute( gear_percentageToU.percentage )
    gear_percentageToU.steps = addNumericAttr("steps", "s", OpenMaya.MFnNumericData.kShort, 40, 1)
    gear_percentageToU.addAttribute( gear_percentageToU.steps )

    # Outputs ---------------------------------------
    gear_percentageToU.u = nAttr.create( "u", "u", OpenMaya.MFnNumericData.kFloat, 0 )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_percentageToU.addAttribute( gear_percentageToU.u )

    # Connections -----------------------------------
    gear_percentageToU.attributeAffects ( gear_percentageToU.curve, gear_percentageToU.u )
    gear_percentageToU.attributeAffects ( gear_percentageToU.steps, gear_percentageToU.u )
    gear_percentageToU.attributeAffects ( gear_percentageToU.percentage, gear_percentageToU.u )
    gear_percentageToU.attributeAffects ( gear_percentageToU.normalizedU, gear_percentageToU.u )

# CLASS =============================================
class gear_percentageToU(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000010)

    curve = OpenMaya.MObject()

    normalizedU = OpenMaya.MObject()
    u = OpenMaya.MObject()
    steps = OpenMaya.MObject()
    percentage = OpenMaya.MObject()

    def compute(self, plug, data):

        # Inputs ------------------------------------
        # Input NurbsCurve
        curve = data.inputValue(gear_percentageToU.curve).asNurbsCurve()
        if curve.isNull():
            return OpenMaya.MStatus.kSuccess
        curve = OpenMaya.MFnNurbsCurve(curve)

        # Sliders
        normalizedU = data.inputValue(gear_percentageToU.normalizedU).asBool()
        percentage = data.inputValue(gear_percentageToU.percentage).asFloat()
        steps = data.inputValue(gear_percentageToU.steps).asShort()

        # Process -----------------------------------
        percentage *= .01
        
        # Get lengths
        positions = []
        pt = OpenMaya.MPoint()
        u_list = [ self.normalizedUToU(i /(steps - 1.0), curve.numCVs()) for i in range(steps) ]
        for u in u_list:
            curve.getPointAtParam(u, pt, OpenMaya.MSpace.kWorld)
            positions.append(OpenMaya.MVector(pt))

        inter = [ positions[i] - positions[i-1] for i in range(len(positions)) if i > 0 ]
        dist = [ v.length() for v in inter ]
        total_length = sum(dist)
        u_length = [ sum(dist[:i+1]) for i in range(len(dist)) ]
        u_perc = [ i / total_length for i in u_length ]
        
        # Get closest indices
        index = self.findClosestInArray(percentage, u_perc)
  
        if percentage <= u_perc[index]:
            indices = [abs(index-1), index]
            indices.sort()
            indexA = indices[0]
            indexB = indices[1]
        else:
            indexA = index
            indexB = index + 1
        
        # blend value
        blend = self.set01Range(percentage, u_perc[indexA], u_perc[indexB])
            
        u = self.linearInterpolate(u_list[indexA], u_list[indexB], blend)
        
        if normalizedU:
            u = self.uToNormalizedU(u, curve.numCVs())
            
        # Outputs -----------------------------------
        if plug == gear_percentageToU.u:
            h = data.outputValue( gear_percentageToU.u )
            h.setFloat( u )

            data.setClean( plug )
        else:
            return OpenMaya.MStatus.kUnknownParameter

        return OpenMaya.MStatus.kSuccess

    # ===============================================
    def normalizedUToU(self, u, point_count):
        return u*(point_count-3.0)

    def uToNormalizedU(self, u, point_count):
        return u/(point_count-3.0)
        
    def findClosestInArray(self, value, array):
   
        difference = [ math.fabs(i-value) for i in array ]
        index = difference.index(min(difference))
        
        return index
        
    def set01Range(self, value, first, second):
        return (value - first) / (second - first)
        
    def linearInterpolate(self, first, second, blend):
        return first * (1-blend) + second * blend
    

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
