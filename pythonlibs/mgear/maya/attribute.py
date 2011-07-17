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
    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.

    Author:     Jeremie Passerin      geerem@hotmail.com
    Url:        http://www.jeremiepasserin.com
    Date:       2011 / 07 / 13

'''

## @package mgear.maya.attribute
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
import mgear

from pymel.core.general import *
import pymel.core.datatypes as dt

#############################################
# NODE
#############################################
def addAttribute(node, longName, attributeType, defaultValue, niceName=None, shortName=None, minValue=None, maxValue=None, keyable=True, readable=True, storable=True, writable=True):

    if node.hasAttr(longName):
        mgear.log("Attribute already exists", mgear.error)
        return
    
    data = {}

    # data["longName"] = longName
    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName
        
    if attributeType == "string":
        data["dataType"] = attributeType
    else:
        data["attributeType"] = attributeType

    if minValue is not None:
        data["minValue"] = minValue
    if maxValue is not None:
        data["maxValue"] = maxValue

    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable
    
    node.addAttr(longName, **data)
    node.setAttr(longName, defaultValue)
    
    return node.attr(longName)

def addEnumAttribute(node, longName, defaultValue, enum, niceName=None, shortName=None, keyable=True, readable=True, storable=True, writable=True):

    if node.hasAttr(longName):
        mgear.log("Attribute already exists", mgear.error)
        return
        
    data = {}

    # data["longName"] = longName
    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName
    
    data["attributeType"] = "enum"
    data["en"] = ":".join(enum)
    
    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable
    
    node.addAttr(longName, **data)
    node.setAttr(longName, defaultValue)

    return node.attr(longName)
    
def lockAttribute(node, attributes=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]):

    for attr_name in attributes:
        node.setAttr(attr_name, lock=True, keyable=False)

# ========================================================
## Set Capabilities of given local parameters to keyable or nonKeyable
# @param node X3DObject - The object to set.
# @param params List of String - The local parameter to set as keyable. params not in the list will be locked (expression + readonly)\n
# if None, ["tx", "ty", "tz", "rorder", "rx", "ry", "rz", "sx", "sy", "sz"] is used
# @return
def setKeyableAttributes(nodes, params=["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz"]):

    localParams = ["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz", "v"]

    if not isinstance(nodes, list):
        nodes = [nodes]

    for attr_name in params:
        for node in nodes:
            node.setAttr(attr_name, lock=False, keyable=True)
    
    for attr_name in localParams:
        if attr_name not in params:
            for node in nodes:
                node.setAttr(attr_name, lock=True, keyable=False)

# ========================================================
## Set the rotorder of the object
# @param node X3DObject - The object to set the rot order on
# @param s String - Value of the rotorder. Possible values : ("XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX")
# @return
def setRotOrder(node, s="XYZ"):

    a = ["XYZ", "YZX", "ZXY", "XZY", "YXZ", "ZYX"]

    if s not in a:
        mgear.log("Invalid Rotorder : "+s, mgear.siError)
        return False
        
    # Unless Softimage there is no event on the rotorder parameter to automatically adapt the angle values
    # So let's do it manually using the EulerRotation class

    er = dt.EulerRotation([getAttr(node+".rx"),getAttr(node+".ry"),getAttr(node+".rz")], unit="degrees")
    er.reorderIt(s)
    
    node.setAttr("ro", a.index(s))
    node.setAttr("rotate", er.x, er.y, er.z)
    
##########################################################
# PARAMETER DEFINITION
##########################################################
# ========================================================
class ParamDef(object):

    ## Init Method.
    # @param self
    # @param scriptName String - Parameter scriptname
    # @return ParamDef - The stored parameter definition
    def __init__(self, scriptName):

        self.scriptName = scriptName
        self.value = None
        self.valueType = None

    ## Add a parameter to property using the parameter definition.
    # @param self
    # @param prop Property - The property to add the parameter to.
    def create(self, node):

        node, attr_name = addAttribute(node, self.scriptName, self.valueType, self.value, self.niceName, self.shortName, self.minimum, self.maximum, self.keyable, self.readable, self.storable, self.writable)

        return node, attr_name

## Create a parameter definition using the AddParameter2 mapping.\n
class ParamDef2(ParamDef):

    ## Init Method.
    # @param self
    # @param scriptName String - Parameter scriptname
    # @param valueType Integer - siVariantType
    # @param value Variant - Default parameter value
    # @param minimum Variant - mininum value
    # @param maximum Variant - maximum value
    # @param sugMinimum Variant - suggested mininum value
    # @param sugMaximum Variant - suggested maximum value
    # @param classification Integer - parameter classification
    # @param capabilities Integer - parameter capabilities
    # @return ParamDef - The stored parameter definition
    def __init__(self, scriptName, valueType, value, niceName=None, shortName=None, minimum=None, maximum=None, keyable=True, readable=True, storable=True, writable=True):

        self.scriptName = scriptName
        self.niceName = niceName
        self.shortName = shortName
        self.valueType = valueType
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.keyable = keyable
        self.readable = readable
        self.storable = storable
        self.writable = writable

## Create an Fcurve parameter definition.\n
class FCurveParamDef(ParamDef):

    ## Init Method.
    # @param self
    # @param scriptName String - Parameter scriptname
    # @return ParamDef - The stored parameter definition
    def __init__(self, scriptName, keys=None, interpolation=0, extrapolation=0):

        self.scriptName = scriptName
        self.keys = keys
        self.interpolation = interpolation
        self.extrapolation = extrapolation
        self.value = None
        self.valueType = None

    ## Add a parameter to property using the parameter definition.
    # @param self
    # @param prop Property - The property to add the parameter to.
    def create(self, node):
    
        node, attr_name = addAttribute(node, self.scriptName, self.shortName, "double", 0)
        
        fcv_node = PyNode(createNode("animCurveUU"))
        fcv_node.connectAttr("output", node.getAttr(attr_name))
        
        # if self.keys is not None:
            # fcu.drawFCurve(param.Value, self.keys, self.interpolation, self.extrapolation)
        # else:
            # param.Value.Interpolation = self.interpolation
            # param.Value.Interpolation = self.extrapolation

        self.value = param.Value

        return node, attr_name
