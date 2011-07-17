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

## @package gear_inverseRotOrder_node.py
# @author Jeremie Passerin
#

#####################################################
# GLOBAL
#####################################################
import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

#####################################################
# INIT / UNINIT
#####################################################
# INIT ==============================================
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Jeremie Passerin', '1.0', 'Any')
    try:
        plugin.registerNode('gear_inverseRotOrder', gear_inverseRotOrder.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_inverseRotOrder.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_inverseRotOrder() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs ----------------------------------------
    gear_inverseRotOrder.rotOrder = eAttr.create( "rotOrder", "ro", 0 )
    eAttr.addField("xyz", 0)
    eAttr.addField("yzx", 1)
    eAttr.addField("zxy", 2)
    eAttr.addField("xzy", 3)
    eAttr.addField("yxz", 4)
    eAttr.addField("zyx", 5)
    eAttr.setWritable(True)
    eAttr.setStorable(True)
    eAttr.setReadable(True)
    eAttr.setKeyable(True)
    gear_inverseRotOrder.addAttribute( gear_inverseRotOrder.rotOrder )
    
    # Outputs ---------------------------------------
    gear_inverseRotOrder.output = nAttr.create( "output", "out", OpenMaya.MFnNumericData.kShort, 0 )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setKeyable(False)
    gear_inverseRotOrder.addAttribute( gear_inverseRotOrder.output )

    # Connections -----------------------------------
    gear_inverseRotOrder.attributeAffects ( gear_inverseRotOrder.rotOrder, gear_inverseRotOrder.output )

# CLASS =============================================
class gear_inverseRotOrder(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000005)

    rotOrder = OpenMaya.MObject()
    output = OpenMaya.MObject()

    def compute(self, plug, data):
    
        # Error check
        if plug != gear_inverseRotOrder.output:
            return OpenMaya.MStatus.kUnknownParameter
        
        # Get inputs
        rotOrder = data.inputValue( gear_inverseRotOrder.rotOrder ).asShort()
        
        inv_rot = [ 5, 3, 4, 1, 2, 0 ]
        
        # Output
        h_pointAt = data.outputValue( gear_inverseRotOrder.output )
        h_pointAt.setShort( inv_rot[rotOrder] )
        data.setClean( plug )

        return OpenMaya.MStatus.kSuccess
        