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

## @package mgear.maya.node
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
from pymel.core import *

#############################################
# CREATE SIMPLE NODES
#############################################
# ===========================================
## Decompose Matrix
def createDecomposeMatrixNode(m):

    node = createNode("decomposeMatrix")
    
    connectAttr(m, node+".inputMatrix")
    
    return node
    
# ===========================================
## Distance Node
def createDistNode(objA, objB):

    node = createNode("distanceBetween")

    dm_nodeA = createNode("decomposeMatrix")
    dm_nodeB = createNode("decomposeMatrix")

    connectAttr(objA+".worldMatrix", dm_nodeA+".inputMatrix")
    connectAttr(objB+".worldMatrix", dm_nodeB+".inputMatrix")

    connectAttr(dm_nodeA+".outputTranslate", node+".point1")
    connectAttr(dm_nodeB+".outputTranslate", node+".point2")

    return node
        
# ===========================================
## Blend Node
def createBlendNode(inputA, inputB, blender=.5):

    node = createNode("blendColors")

    if not isinstance(inputA, list):
        inputA = [inputA]

    if not isinstance(inputB, list):
        inputB = [inputB]

    for item, s in zip(inputA, "RGB"):
        if isinstance(item, str) or isinstance(item, unicode) or isinstance(item, Attribute):
            connectAttr(item, node+".color1"+s)
        else:
            setAttr(node+".color1"+s, item)

    for item, s in zip(inputB, "RGB"):
        if isinstance(item, str) or isinstance(item, unicode) or isinstance(item, Attribute):
            connectAttr(item, node+".color2"+s)
        else:
            setAttr(node+".color2"+s, item)
            
    if isinstance(blender, str) or isinstance(blender, unicode) or isinstance(blender, Attribute):
        connectAttr(blender, node+".blender")
    else:
        setAttr(node+".blender", blender)

    return node
    
# ===========================================
## Reverse Node
def createReverseNode(input):

    node = createNode("reverse")
    
    if not isinstance(input, list):
        input = [input]
        
    for item, s in zip(input, "XYZ"):
        if isinstance(item, str) or isinstance(item, unicode) or isinstance(item, Attribute):
            connectAttr(item, node+".input"+s)
        else:
            setAttr(node+".input"+s, item)
            
    return node
    
# ===========================================
## CurveInfo Node
def createCurveInfoNode(crv):

    node = createNode("curveInfo")
    
    shape = listRelatives(crv, shapes=True)[0]
    
    connectAttr(shape+".local", node+".inputCurve")
    
    return node

# ===========================================
## Add Node
def createAddNode(inputA, inputB):

    node = createNode("addDoubleLinear")

    if isinstance(inputA, str) or isinstance(inputA, unicode) or isinstance(inputA, Attribute):
        connectAttr(inputA, node+".input1")
    else:
        setAttr(node+".input1", inputA)

    if isinstance(inputB, str) or isinstance(inputB, unicode) or isinstance(inputB, Attribute):
        connectAttr(inputB, node+".input2")
    else:
        setAttr(node+".input2", inputB)

    return node
    
# ===========================================
## Sub Node
def createSubNode(inputA, inputB):

    node = createNode("addDoubleLinear")

    if isinstance(inputA, str) or isinstance(inputA, unicode) or isinstance(inputA, Attribute):
        connectAttr(inputA, node+".input1")
    else:
        setAttr(node+".input1", inputA)

    if isinstance(inputB, str) or isinstance(inputB, unicode) or isinstance(inputB, Attribute):
        neg_node = createNode("multiplyDivide")
        connectAttr(inputB, neg_node+".input1X")
        setAttr(neg_node+".input2X", -1)
        connectAttr(neg_node+".outputX", node+".input2")
    else:
        setAttr(node+".input2", -inputB)

    return node

# ===========================================
## Multiply Node
def createMulNode(inputA, inputB):

    return createMulDivNode(inputA, inputB, 1)

# ===========================================
## Divide Node
def createDivNode(inputA, inputB):

    return createMulDivNode(inputA, inputB, 2)

# ===========================================
## MultiplyDivide Node
def createMulDivNode(inputA, inputB, operation=1):

    node = createNode("multiplyDivide")
    setAttr(node+".operation", operation)

    if not isinstance(inputA, list):
        inputA = [inputA]

    if not isinstance(inputB, list):
        inputB = [inputB]

    for item, s in zip(inputA, "XYZ"):
        if isinstance(item, str) or isinstance(item, unicode) or isinstance(item, Attribute):
            connectAttr(item, node+".input1"+s)
        else:
            setAttr(node+".input1"+s, item)

    for item, s in zip(inputB, "XYZ"):
        if isinstance(item, str) or isinstance(item, unicode) or isinstance(item, Attribute):
            connectAttr(item, node+".input2"+s)
        else:
            setAttr(node+".input2"+s, item)

    return node

# ===========================================
## Clamp Node
def createClampNode(input, in_min, in_max):

    node = createNode("clamp")

    if not isinstance(input, list):
        input = [input]
    if not isinstance(in_min, list):
        in_min = [in_min]
    if not isinstance(in_max, list):
        in_max = [in_max]

    for in_item, min_item, max_item, s in zip(input, in_min, in_max, "RGB"):

        if isinstance(in_item, str) or isinstance(in_item, unicode) or isinstance(in_item, Attribute):
            connectAttr(in_item, node+".input"+s)
        else:
            setAttr(node+".input"+s, in_item)

        if isinstance(min_item, str) or isinstance(min_item, unicode) or isinstance(min_item, Attribute):
            connectAttr(min_item, node+".min"+s)
        else:
            setAttr(node+".min"+s, min_item)

        if isinstance(max_item, str) or isinstance(max_item, unicode) or isinstance(max_item, Attribute):
            connectAttr(max_item, node+".max"+s)
        else:
            setAttr(node+".max"+s, max_item)

    return node

#############################################
# CREATE MULTI NODES
#############################################
# ===========================================
## Negate Node
def createNegateNodeMulti(name, inputs=[]):

    s = "XYZ"
    count=0
    i=0
    outputs = []
    for input in inputs:
        if count==0:
            real_name = name+"_"+str(i)
            node_name = createNode("multiplyDivide", n=real_name)
            i+=1

        connectAttr(input, node_name+".input1"+s[count], f=True)
        setAttr(node_name+".input2"+s[count], -1)

        outputs.append(node_name+".output"+s[count])
        count = (count+1)%3

    return outputs

# ===========================================
## Add Node
def createAddNodeMulti(inputs=[]):

    outputs = [inputs[0]]

    for i, input in enumerate(inputs[1:]):
        node_name = createNode("addDoubleLinear")

        if isinstance(outputs[-1], str) or isinstance(outputs[-1], unicode) or isinstance(outputs[-1], Attribute):
            connectAttr(outputs[-1], node_name+".input1", f=True)
        else:
            setAttr(node_name+".input1", outputs[-1])

        if isinstance(input, str) or isinstance(input, unicode) or isinstance(input, Attribute):
            connectAttr(input, node_name+".input2", f=True)
        else:
            setAttr(node_name+".input2", input)

        outputs.append(node_name+".output")

    return outputs

# ===========================================
## Mul Node
def createMulNodeMulti(name, inputs=[]):

    outputs = [inputs[0]]

    for i, input in enumerate(inputs[1:]):
        real_name = name+"_"+str(i)
        node_name = createNode("multiplyDivide", n=real_name)
        setAttr(node_name+".operation", 1)

        if isinstance(outputs[-1], str) or isinstance(outputs[-1], unicode) or isinstance(outputs[-1], Attribute):
            connectAttr(outputs[-1], node_name+".input1X", f=True)
        else:
            setAttr(node_name+".input1X", outputs[-1])

        if isinstance(input, str) or isinstance(input, unicode) or isinstance(input, Attribute):
            connectAttr(input, node_name+".input2X", f=True)
        else:
            setAttr(node_name+".input2X", input)

        outputs.append(node_name+".output")

    return outputs

# ===========================================
## Div Node
def createDivNodeMulti(name, inputs1=[], inputs2=[]):

    for i, input in enumerate(inputs[1:]):
        real_name = name+"_"+str(i)
        node_name = createNode("multiplyDivide", n=real_name)
        setAttr(node_name+".operation", 2)

        if isinstance(outputs[-1], str) or isinstance(outputs[-1], unicode) or isinstance(outputs[-1], Attribute):
            connectAttr(outputs[-1], node_name+".input1X", f=True)
        else:
            setAttr(node_name+".input1X", outputs[-1])

        if isinstance(input, str) or isinstance(input, unicode) or isinstance(input, Attribute):
            connectAttr(input, node_name+".input2X", f=True)
        else:
            setAttr(node_name+".input2X", input)

        outputs.append(node_name+".output")

    return outputs

# ===========================================
## Clamp Node
def createClampNodeMulti(name, inputs=[], in_min=[], in_max=[]):

    s = "RGB"
    count=0
    i=0
    outputs = []
    for input, min, max in zip(inputs, in_min, in_max):
        if count==0:
            real_name = name+"_"+str(i)
            node_name = createNode("clamp", n=real_name)
            i+=1

        connectAttr(input, node_name+".input"+s[count], f=True)

        if isinstance(min, str) or isinstance(min, unicode) or isinstance(min, Attribute):
            connectAttr(min, node_name+".min"+s[count], f=True)
        else:
            setAttr(node_name+".min"+s[count], min)

        if isinstance(max, str) or isinstance(max, unicode) or isinstance(max, Attribute):
            connectAttr(max, node_name+".max"+s[count], f=True)
        else:
            setAttr(node_name+".max"+s[count], max)

        outputs.append(node_name+".output"+s[count])
        count = (count+1)%3

    return outputs



