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

## @package mgear.maya.rig.component.guide
# @author Jeremie Passerin
#

##########################################################
# GLOBAL
##########################################################
# pyMel
from pymel.core.general import *

# mgear
import mgear.string as string
import mgear.maya.dag as dag
import mgear.maya.transform as tra
import mgear.maya.vector as vec

import mgear
from mgear.maya.rig.guide import MainGuide

##########################################################
# COMPONENT GUIDE
##########################################################
## Main class for component guide creation.\n
# This class handles all the parameters and objectDefs creation.\n
# It also now how to parse its own hierachy of object to retrieve position and transform.\n
# Finally it also now how to export itself as xml_node.
class ComponentGuide(MainGuide):

    compType = "component"  ## Component type
    compName = "component"  ## Component default name
    compSide = "C"
    compIndex = 0 ## Component default index

    description = "" ## Description of the component

    connectors = []
    compatible = []
    ctl_grp = ""

    # ====================================================
    ## Init method.
    # @param self
    # @param ref an xml definition or a SI3DObject
    def __init__(self):

        # Parameters names, definition and values.
        self.paramNames = [] ## List of parameter name cause it's actually important to keep them sorted.
        self.paramDefs = {} ## Dictionary of parameter definition.
        self.values = {} ## Dictionary of options values.

        # We will check a few things and make sure the guide we are loading is up to date.
        # If parameters or object are missing a warning message will be display and the guide should be updated.
        self.valid = True

        self.root = None
        self.id = None

        # parent component identification
        self.parentComponent = None
        self.parentLocalName = None

        # List and dictionary used during the creation of the component
        self.tra = {} ## dictionary of global transform
        self.atra = [] ## list of global transform
        self.pos = {} ## dictionary of global postion
        self.apos = [] ## list of global position
        self.prim = {} ## List of primitive
        self.blades = {}
        self.size = .1
        self.root_size = None

        # List and dictionary used to define data of the guide that should be saved
        self.pick_transform = [] ## User will have to pick the position of this object name
        self.save_transform = [] ## Transform of object name in this list will be saved
        self.save_primitive = [] ## Primitive of object name in this list will be saved
        self.save_blade = [] ## Normal and BiNormal of object will be saved
        self.minmax = {} ## Define the min and max object for multi location objects

        # Init the guide
        self.postInit()
        self.initialHierarchy()
        self.addParameters()

    ## Define the objects name and categories.\n
    # REIMPLEMENT. This method should be reimplemented in each component.
    # @param self
    def postInit(self):
        self.save_transform = ["root"]
        return

    # ====================================================
    # OBJECTS AND PARAMETERS
    ## Initial hierachy. It's no more than the basic set of parameters and layout needed for the setting property.
    # @param self
    def initialHierarchy(self):

        # Parameters --------------------------------------
        # This are the necessary parameter for conponent guide definition
        self.pCompType = self.addParam("comp_type", "ct", "string", self.compType)
        self.pCompName = self.addParam("comp_name", "cn", "string", self.compName)
        self.pCompSide = self.addParam("comp_side", "side", "string", self.compSide)
        self.pCompIndex = self.addParam("comp_index", "id", "long", self.compIndex, 0)
        self.pConnector = self.addParam("connector", "cnx", "string", "standard")
        self.pUIHost = self.addParam("ui_host", "uih", "string", "")

        # Items -------------------------------------------
        typeItems = [self.compType, self.compType]
        for type in self.compatible:
            typeItems.append(type)
            typeItems.append(type)

        connectorItems = ["standard", "standard"]
        for item in self.connectors:
            connectorItems.append(item)
            connectorItems.append(item)

    ## Create the parameter definitions of the guide.\n
    # REIMPLEMENT. This method should be reimplemented in each component.
    # @param self
    def addParameters(self):
        return

    # ====================================================
    # SET / GET
    def setFromHierarchy(self, root):

        self.root = root
        self.model = self.root.getParent(generations=-1)

        # ---------------------------------------------------
        # First check and set the settings
        if not self.root.hasAttr("comp_type"):
            mgear.log("%s is not a proper guide."%self.root.longName(), mgear.sev_error)
            self.valid = False
            return

        self.setParamDefValuesFromProperty(self.root)

        # ---------------------------------------------------
        # Then get the objects
        for name in self.save_transform:
            if "#" in name:
                i = 0
                while not self.minmax[name].max > 0 or i < self.minmax[name].max:
                    localName = string.replaceSharpWithPadding(name, i)

                    node = dag.findChild(self.model, self.getName(localName))
                    if not node:
                        break

                    self.tra[localName] = node.getMatrix(worldSpace=True)
                    self.atra.append(node.getMatrix(worldSpace=True))
                    self.pos[localName] = node.getTranslation(space="world")
                    self.apos.append(node.getTranslation(space="world"))

                    i += 1

                if i < self.minmax[name].min:
                    mgear.log("Minimum of object requiered for "+name+" hasn't been reached", mgear.sev_warning)
                    self.valid = False
                    continue

            else:
                node = dag.findChild(self.model, self.getName(name))
                if not node:
                    mgear.log("Object missing : %s"%name, mgear.sev_warning)
                    self.valid = False
                    continue

                self.tra[name] = node.getMatrix(worldSpace=True)
                self.atra.append(node.getMatrix(worldSpace=True))
                self.pos[name] = node.getTranslation(space="world")
                self.apos.append(node.getTranslation(space="world"))

        for name in self.save_blade:
        
            node = dag.findChild(self.model, self.getName(name))
            if not node:
                mgear.log("Object missing : %s"%name, mgear.sev_warning)
                self.valid = False
                continue

            self.blades[name] = vec.Blade(node.getMatrix(worldSpace=True))
            
        self.size = self.getSize()


    # ====================================================
    # MISC
    ##
    # @param self
    # @paran model
    # @return Dictionary of X3DObject
    def getObjects(self, model):
        objects = {}
        
        children = listRelatives(model, ad=True)
        select(children)
        for child in ls(self.fullName+"_*", selection=True):
            objects[child[child.index(self.fullName+"_")+len(self.fullName+"_"):]] = child
            
        return objects

    # @param self
    def addMinMax(self, name, minimum=1, maximum=-1):
        if "#" not in name:
            mgear.log("Invalid definition for min/max. You should have a '#' in the name", mgear.sev_error)
        self.minmax[name] = MinMax(minimum, maximum)

    ##
    # @param self
    # @return Double
    def getSize(self):

        # size
        size = .01
        for pos in self.apos:
            d = vec.getDistance(self.pos["root"], pos)
            size = max(size, d)
        size = max(size, .01)

        return size

    ## Return the fullname of given element of the component.
    # @param self
    # @param name String - Localname of the element.
    def getName(self, name):
        return self.fullName + "_" + name

    ## Return the fullname of the component.
    # @param self
    def getFullName(self):
        return self.values["comp_name"] + "_" + self.values["comp_side"] + str(self.values["comp_index"])

    ## Return the type of the component.
    # @param self
    def getType(self):
        return self.compType

    ##
    # @param self
    def getObjectNames(self):

        names = set()
        names.update(self.save_transform)
        names.update(self.save_primitive)
        names.update(self.save_blade)

        return names

    def getVersion(self):
        return ".".join([str(i) for i in self.version])

    fullName = property(getFullName)
    type = property(getType)
    objectNames = property(getObjectNames)

##########################################################
# OTHER CLASSES
##########################################################
class MinMax(object):

    def __init__(self, minimum=1, maximum=-1):
        self.min = minimum
        self.max = maximum