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
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

#####################################################
# INIT / UNINIT
#####################################################
# INIT ==============================================
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Jeremie Passerin', '1.0', 'Any')
    try:
        plugin.registerNode('gear_curveCns', gear_curveCns.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_curveCns.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to deregister node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr(gear_curveCns())

# INIT ==============================================
def initialize():

    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    # Inputs
    gear_curveCns.inputs = mAttr.create( "inputs", "in", OpenMaya.MFnMatrixAttribute.kDouble )
    mAttr.setStorable(True)
    mAttr.setReadable(False)
    mAttr.setIndexMatters(False)
    mAttr.setArray(True)
    gear_curveCns.addAttribute( gear_curveCns.inputs )

    # Connections
    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    addAttrAffects(gear_curveCns, OpenMayaMPx.cvar.MPxDeformerNode_outputGeom, [ gear_curveCns.inputs ])

    # Make deformer weights paintable
    # cmds.makePaintable('gear_curveCns', 'weights', attrType='multiFloat', shapeMode='deformer')

# CLASS =============================================
class gear_curveCns(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x33000007)

    inputs = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def deform(self, data, itGeo, inMatrix, mIndex):
    
        # Inputs
        dh_inputs = data.inputArrayValue( gear_curveCns.inputs )
        deformer_count = dh_inputs.elementCount()
        t = []
        for i in range(deformer_count):
                dh_inputs.jumpToElement(i)
                t.append( OpenMaya.MTransformationMatrix(dh_inputs.inputValue().asMatrix() * inMatrix.inverse()) )
        
        # Process
        while not itGeo.isDone():
            if itGeo.index() < deformer_count:
                pt = OpenMaya.MPoint(t[itGeo.index()].getTranslation(OpenMaya.MSpace.kWorld))
                itGeo.setPosition(pt)
            itGeo.next()

        return OpenMaya.MStatus.kSuccess

#####################################################
# ADD ATTRIBUTE METHODS
#####################################################
def addAttrAffects(node, outAttr, inAttr=[]):

    for attr in inAttr:
        node.attributeAffects ( attr, outAttr )

