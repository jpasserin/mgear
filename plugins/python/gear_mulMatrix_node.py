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
#####################################################
# GLOBAL
#####################################################
import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

ar = OpenMaya.MScriptUtil()

#####################################################
# INIT / UNINIT
#####################################################
# INIT ==============================================
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Jeremie Passerin', '1.0', 'Any')
    try:
        plugin.registerNode('gear_mulMatrix', gear_mulMatrix.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_mulMatrix.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr( gear_mulMatrix() )

# INIT ==============================================
def initialize():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs ----------------------------------------
    gear_mulMatrix.matrixA = mAttr.create( "matrixA", "mA", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setWritable(True)
    mAttr.setStorable(True)
    mAttr.setReadable(True)
    mAttr.setKeyable(True)
    gear_mulMatrix.addAttribute( gear_mulMatrix.matrixA )

    gear_mulMatrix.matrixB = mAttr.create( "matrixB", "mB", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setWritable(True)
    mAttr.setStorable(True)
    mAttr.setReadable(True)
    mAttr.setKeyable(True)
    gear_mulMatrix.addAttribute( gear_mulMatrix.matrixB )

    # Outputs ---------------------------------------
    gear_mulMatrix.output = mAttr.create( "output", "out", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setWritable(False)
    mAttr.setStorable(False)
    mAttr.setReadable(True)
    mAttr.setKeyable(False)
    gear_mulMatrix.addAttribute( gear_mulMatrix.output )

    # Connections -----------------------------------
    gear_mulMatrix.attributeAffects ( gear_mulMatrix.matrixA, gear_mulMatrix.output )
    gear_mulMatrix.attributeAffects ( gear_mulMatrix.matrixB, gear_mulMatrix.output )

# CLASS =============================================
class gear_mulMatrix(OpenMayaMPx.MPxNode):

    kPluginNodeId = OpenMaya.MTypeId(0x33000008)

    matrixA = OpenMaya.MObject()
    matrixB = OpenMaya.MObject()

    translate = OpenMaya.MObject()
    rotate = OpenMaya.MObject()
    scale = OpenMaya.MObject()

    def compute(self, plug, data):

        if plug != gear_mulMatrix.output:
            return OpenMaya.MStatus.kUnknownParameter

        mA = data.inputValue( gear_mulMatrix.matrixA ).asMatrix()
        mB = data.inputValue( gear_mulMatrix.matrixB ).asMatrix()

        mC = mA * mB

        h = data.outputValue( gear_mulMatrix.output )
        h.setMMatrix( mC )
        data.setClean( plug )

        return OpenMaya.MStatus.kSuccess

