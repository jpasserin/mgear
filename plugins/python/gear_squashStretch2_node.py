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

## @package RollSplineKine_node.py
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
        plugin.registerNode('gear_squashStretch2', gear_squashStretch2.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_squashStretch2.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_squashStretch2() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs Matrices -------------------------------
    gear_squashStretch2.global_scale = nAttr.createPoint("global_scale", "gs" )
    gear_squashStretch2.global_scalex = nAttr.child(0)
    gear_squashStretch2.global_scaley = nAttr.child(1)
    gear_squashStretch2.global_scalez = nAttr.child(2)
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_squashStretch2.addAttribute( gear_squashStretch2.global_scale )

    # Inputs Sliders --------------------------------

    gear_squashStretch2.blend = addNumericAttr("blend", "b", OpenMaya.MFnNumericData.kFloat, 1, 0, 1)
    gear_squashStretch2.addAttribute( gear_squashStretch2.blend )
    gear_squashStretch2.driver = addNumericAttr("driver", "d", OpenMaya.MFnNumericData.kFloat, 0)
    gear_squashStretch2.addAttribute( gear_squashStretch2.driver )
    gear_squashStretch2.driver_min = addNumericAttr("driver_min", "dmin", OpenMaya.MFnNumericData.kFloat, 0)
    gear_squashStretch2.addAttribute( gear_squashStretch2.driver_min )
    gear_squashStretch2.driver_ctr = addNumericAttr("driver_ctr", "dctr", OpenMaya.MFnNumericData.kFloat, 0)
    gear_squashStretch2.addAttribute( gear_squashStretch2.driver_ctr )
    gear_squashStretch2.driver_max = addNumericAttr("driver_max", "dmax", OpenMaya.MFnNumericData.kFloat, 0)
    gear_squashStretch2.addAttribute( gear_squashStretch2.driver_max )

    gear_squashStretch2.axis = eAttr.create( "axis", "a", 0 )
    eAttr.addField("x", 0)
    eAttr.addField("y", 1)
    eAttr.addField("z", 2)
    eAttr.setWritable(True)
    eAttr.setStorable(True)
    eAttr.setReadable(True)
    eAttr.setKeyable(False)
    gear_squashStretch2.addAttribute( gear_squashStretch2.axis )

    gear_squashStretch2.squash = addNumericAttr("squash", "sq", OpenMaya.MFnNumericData.kFloat, 0, -1, 1)
    gear_squashStretch2.addAttribute( gear_squashStretch2.squash )
    gear_squashStretch2.stretch = addNumericAttr("stretch", "st", OpenMaya.MFnNumericData.kFloat, 0, -1, 1)
    gear_squashStretch2.addAttribute( gear_squashStretch2.stretch )

    # Outputs ---------------------------------------

    gear_squashStretch2.output = nAttr.createPoint("output", "out" )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    gear_squashStretch2.addAttribute( gear_squashStretch2.output )

    # Connections -----------------------------------
    addAttrAffects(gear_squashStretch2, gear_squashStretch2.output, [ gear_squashStretch2.global_scale,
                                                            gear_squashStretch2.blend, gear_squashStretch2.driver,
                                                            gear_squashStretch2.driver_min, gear_squashStretch2.driver_ctr, gear_squashStretch2.driver_max,
                                                            gear_squashStretch2.axis, gear_squashStretch2.squash, gear_squashStretch2.stretch ])

# CLASS =============================================
class gear_squashStretch2(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000004)

    global_scale = OpenMaya.MObject()
    global_scalex = OpenMaya.MObject()
    global_scaley = OpenMaya.MObject()
    global_scalez = OpenMaya.MObject()
    
    blend = OpenMaya.MObject()
    driver = OpenMaya.MObject()
    driver_min = OpenMaya.MObject()
    driver_ctr = OpenMaya.MObject()
    driver_max = OpenMaya.MObject()
    axis = OpenMaya.MObject()
    squash = OpenMaya.MObject()
    stretch = OpenMaya.MObject()

    output = OpenMaya.MObject()

    def compute(self, plug, data):

        if plug != gear_squashStretch2.output:
            return OpenMaya.MStatus.kUnknownParameter

        # Get inputs matrices ------------------------------
        inputData = data.inputValue( gear_squashStretch2.global_scale )
        sx = inputData.child(gear_squashStretch2.global_scalex).asFloat()
        sy = inputData.child(gear_squashStretch2.global_scaley).asFloat()
        sz = inputData.child(gear_squashStretch2.global_scalez).asFloat()
        gscale = OpenMaya.MVector(sx, sy, sz)

        # Get inputs sliders -------------------------------
        blend = data.inputValue(gear_squashStretch2.blend).asFloat()
        driver = data.inputValue(gear_squashStretch2.driver).asFloat()
        driver_min = data.inputValue(gear_squashStretch2.driver_min).asFloat()
        driver_ctr = data.inputValue(gear_squashStretch2.driver_ctr).asFloat()
        driver_max = data.inputValue(gear_squashStretch2.driver_max).asFloat()
        axis = data.inputValue(gear_squashStretch2.axis).asLong()
        squash = data.inputValue(gear_squashStretch2.squash).asFloat()
        stretch = data.inputValue(gear_squashStretch2.stretch).asFloat()

        # Process ------------------------------------------
        # Ratio
        st_ratio = self.clamp(max(driver - driver_ctr, 0) / max(driver_max - driver_ctr, 0.0001), 0,1)
        sq_ratio = self.clamp(max(driver_ctr - driver, 0) / max(driver_ctr - driver_min, 0.0001), 0,1)

        squash *= sq_ratio
        stretch *= st_ratio

        scl = OpenMaya.MVector(gscale.x, gscale.y, gscale.z)
        
        if axis != 0:
          scl.x = gscale.x * max( 0, 1.0 + squash + stretch )

        if axis != 1:
          scl.y = gscale.y * max( 0, 1.0 + squash + stretch )

        if axis != 2:
          scl.z = gscale.z * max( 0, 1.0 + squash + stretch )

        scl = self.linearlyInterpolate(gscale, scl, blend)

        # Output -------------------------------------------
        h_scale = data.outputValue( gear_squashStretch2.output )
        h_scale.set3Float( scl.x, scl.y, scl.z )
        data.setClean( plug )

        data.setClean( plug )

        return OpenMaya.MStatus.kSuccess

    def linearlyInterpolate(self, v0, v1, blend=.5):

        vector = v1 - v0
        vector *= blend
        vector += v0

        return vector
        
    def clamp(self, u, minimum, maximum):
        return min(max(u,minimum), maximum)

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
