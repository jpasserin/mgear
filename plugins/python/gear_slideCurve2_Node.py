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
import math

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
        plugin.registerNode('gear_slideCurve2', gear_slideCurve2.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError, 'Failed to register node'

# UNINIT ============================================
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(gear_slideCurve2.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to deregister node'

#####################################################
# NODE
#####################################################
# CREATOR ===========================================
def creator():
    return OpenMayaMPx.asMPxPtr(gear_slideCurve2())

# INIT ==============================================
def initialize():

    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # Input Mesh
    gear_slideCurve2.master_crv = tAttr.create('master_crv', 'mcrv', OpenMaya.MFnData.kNurbsCurve)
    gear_slideCurve2.addAttribute( gear_slideCurve2.master_crv )
    gear_slideCurve2.master_mat = addMatrixAttr("master_mat", "mmat")
    gear_slideCurve2.addAttribute( gear_slideCurve2.master_mat )

    # Input Sliders
    gear_slideCurve2.slave_length = addNumericAttr("slave_length", "sl", OpenMaya.MFnNumericData.kFloat, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.slave_length )
    gear_slideCurve2.master_length = addNumericAttr("master_length", "ml", OpenMaya.MFnNumericData.kFloat, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.master_length )

    gear_slideCurve2.position = addNumericAttr("position", "p", OpenMaya.MFnNumericData.kFloat, 0.5, 0, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.position )
    gear_slideCurve2.maxstretch = addNumericAttr("maxstretch", "mst", OpenMaya.MFnNumericData.kFloat, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.maxstretch )
    gear_slideCurve2.maxsquash = addNumericAttr("maxsquash", "msq", OpenMaya.MFnNumericData.kFloat, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.maxsquash )
    gear_slideCurve2.softness = addNumericAttr("softness", "s", OpenMaya.MFnNumericData.kFloat, 0, 0, 1 )
    gear_slideCurve2.addAttribute( gear_slideCurve2.softness )

    # Affects
    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    # Connections -----------------------------------
    addAttrAffects(gear_slideCurve2, OpenMayaMPx.cvar.MPxDeformerNode_outputGeom, [ gear_slideCurve2.master_crv, gear_slideCurve2.master_mat, gear_slideCurve2.slave_length, gear_slideCurve2.master_length,
                                                                               gear_slideCurve2.position, gear_slideCurve2.maxstretch, gear_slideCurve2.maxsquash, gear_slideCurve2.softness])

    # Make deformer weights paintable
    # cmds.makePaintable('gear_slideCurve2', 'weights', attrType='multiFloat', shapeMode='deformer')

# CLASS =============================================
class gear_slideCurve2(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x33000006)

    master_crv = OpenMaya.MObject()

    slave_length = OpenMaya.MObject()
    master_length = OpenMaya.MObject()
    position = OpenMaya.MObject()
    maxstretch = OpenMaya.MObject()
    maxsquash = OpenMaya.MObject()
    softness = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def deform(self, data, itGeo, inMatrix, mIndex):

        # Inputs ---------------------------------------------------------
        # Input NurbsCurve
        master_crv = data.inputValue(gear_slideCurve2.master_crv).asNurbsCurve()
        if master_crv.isNull():
            return OpenMaya.MStatus.kSuccess

        master_crv = OpenMaya.MFnNurbsCurve(master_crv)

        master_mat = data.inputValue(gear_slideCurve2.master_mat).asMatrix()

        # Input Sliders
        slave_length = data.inputValue(gear_slideCurve2.slave_length).asFloat()
        master_length = data.inputValue(gear_slideCurve2.master_length).asFloat()
        position = data.inputValue(gear_slideCurve2.position).asFloat()
        maxstretch = data.inputValue(gear_slideCurve2.maxstretch).asFloat()
        maxsquash = data.inputValue(gear_slideCurve2.maxsquash).asFloat()
        softness = data.inputValue(gear_slideCurve2.softness).asFloat()

        # Init -----------------------------------------------------------
        mstCrvLength = master_crv.length()

        slvPointCount = itGeo.exactCount() # Can we use .count() ?
        mstPointCount = master_crv.numCVs()

        # Stretch --------------------------------------------------------
        if (mstCrvLength > master_length) and (maxstretch > 1):
            if softness == 0:
                expo = 1
            else:
                stretch = (mstCrvLength - master_length) / (slave_length * maxstretch)
                expo = 1 - math.exp(-(stretch) / softness)

            ext = min(slave_length * (maxstretch - 1) * expo, mstCrvLength - master_length)

            slave_length += ext

        elif ((mstCrvLength < master_length) and (maxsquash < 1)):
            if softness == 0:
                expo = 1
            else :
                squash = (master_length - mstCrvLength) / (slave_length * maxsquash)
                expo = 1 - math.exp(-(squash) / softness)

            ext = min(slave_length * (1 - maxsquash) * expo, master_length - mstCrvLength)

            slave_length -= ext

        # Position --------------------------------------------------------
        size = slave_length / mstCrvLength
        sizeLeft = 1 - size

        start = position * sizeLeft
        end = start + size


        tStartMScriptUtil=OpenMaya.MScriptUtil()
        tEndMScriptUtil=OpenMaya.MScriptUtil()

        tStartPtr=tStartMScriptUtil.asDoublePtr()
        tEndPtr=tEndMScriptUtil.asDoublePtr()
        master_crv.getKnotDomain( tStartPtr, tEndPtr )
        tStart=tStartMScriptUtil.getDouble(tStartPtr)
        tEnd=tEndMScriptUtil.getDouble(tEndPtr)

        # Process --------------------------------------------------------
        step = (end - start) / (slvPointCount - 1.0)
        pt = OpenMaya.MPoint()
        while not itGeo.isDone():
            perc = start + (itGeo.index() * step)

            u = master_crv.findParamFromLength(perc * mstCrvLength)

            if 0 <= perc <= 1:
                master_crv.getPointAtParam(u, pt, OpenMaya.MSpace.kWorld)
            else:
                if perc < 0:
                    overPerc = perc
                    master_crv.getPointAtParam(0, pt, OpenMaya.MSpace.kWorld)
                    tan = master_crv.tangent(0)
                else:
                    overPerc = perc - 1
                    master_crv.getPointAtParam(mstPointCount-3.0, pt, OpenMaya.MSpace.kWorld)
                    tan = master_crv.tangent(mstPointCount-3.0)

                tan.normalize()
                tan *= mstCrvLength * overPerc

                pt += tan

            pt *= inMatrix.inverse()
            pt *= master_mat
            itGeo.setPosition(pt)
            itGeo.next()

        return OpenMaya.MStatus.kSuccess

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

