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

## @package mgear.maya.dag
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
from pymel.core.general import *

#############################################
# DAG
#############################################
# ===========================================
# Returns the first parent of the hierarchy. (usually the 'Model' in Softimage)
def getTopParent(node):
    return node.getParent(generations=-1)
    
# ===========================================
def getShapes(node):
    return node.listRelatives(shapes=True)
    
# ===========================================
def findChild(node, name):
    return __findChildren(node, name, True)
    
def findChildren(node, name):
    return __findChildren(node, name, False)
    
def __findChildren(node, name, firstOnly=False):
    
    children = [item for item in node.listRelatives(ad=True, type="transform") if item.name().split("|")[-1] == name]
    if not children:
        return False
    if firstOnly:
        return children[0]
    
    return children
        
    
    