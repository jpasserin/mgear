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

## @package mgear.maya.rig.guide
# @author Jeremie Passerin
#

##########################################################
# GLOBAL
##########################################################
# Built-in
import os

# maya
import maya.cmds as cmds

# pymel
from pymel.core.general import *
import pymel.core.datatypes as dt

# mgear
import mgear
import mgear.maya.attribute as att
import mgear.maya.dag as dag
import mgear.maya.vector as vec

#
GUIDE_UI_WINDOW_NAME = "guide_UI_window"

COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "component")
TEMPLATE_PATH = os.path.join(COMPONENT_PATH, "templates")
VERSION = 1.0

##########################################################
# GUIDE
##########################################################
## The main guide class.\n
# Provide the methods to add parameters, set parameter values, create property...
class MainGuide(object):

    def __init__(self):

        # Parameters names, definition and values.
        self.paramNames = [] ## List of parameter name cause it's actually important to keep them sorted.
        self.paramDefs = {} ## Dictionary of parameter definition.
        self.values = {} ## Dictionary of options values.

        # We will check a few things and make sure the guide we are loading is up to date.
        # If parameters or object are missing a warning message will be display and the guide should be updated.
        self.valid = True

    def setParamDefValuesFromProperty(self, node):

        for scriptName, paramDef in self.paramDefs.items():
            if not attributeQuery(scriptName, node=node, exists=True):
                mgear.log("Can't find parameter '%s' in %s"%(scriptName, node), mgear.sev_warning)
                self.valid = False
            else:
                cnx = listConnections(node+"."+scriptName, destination=False, source=True)
                if cnx:
                    paramDef.value = None
                    self.values[scriptName] = cnx[0]
                else:
                    paramDef.value = getAttr(node+"."+scriptName)
                    self.values[scriptName] = getAttr(node+"."+scriptName)

    def addParam(self, scriptName, shortName, valueType, value, minimum=None, maximum=None, keyable=False, readable=False, storable=False, writable=False):

            paramDef = att.ParamDef2(scriptName, shortName, valueType, value, minimum, maximum, keyable, readable, storable, writable)
            self.paramDefs[scriptName] = paramDef
            self.values[scriptName] = value
            self.paramNames.append(scriptName)

            return paramDef

    ## Add a paramDef to the list.\n
    # Note that animatable and keyable are false per default.
    # @param self
    # @param scriptName String - Parameter scriptname.
    # @return FCurveParamDef - The newly created parameter definition.
    def addFCurveParam(self, scriptName, keys, interpolation=0):

        paramDef = att.FCurveParamDef(scriptName, keys, interpolation)
        self.paramDefs[scriptName] = paramDef
        self.values[scriptName] = None
        self.paramNames.append(scriptName)

        return paramDef

##########################################################
# RIG GUIDE
##########################################################
## Rig guide class.\n
# This is the class for complete rig guide definition.\n
# It contains the component guide in correct hierarchy order and the options to generate the rig.\n
# Provide the methods to add more component, import/export guide.
class RigGuide(MainGuide):

    def __init__(self):

        # Parameters names, definition and values.
        self.paramNames = [] ## List of parameter name cause it's actually important to keep them sorted.
        self.paramDefs = {} ## Dictionary of parameter definition.
        self.values = {} ## Dictionary of options values.

        # We will check a few things and make sure the guide we are loading is up to date.
        # If parameters or object are missing a warning message will be display and the guide should be updated.
        self.valid = True

        self.controlers = {} ## Dictionary of controlers
        # Keys are the component fullname (ie. 'arm_L0')
        self.components = {} ## Dictionary of component
        self.componentsIndex = [] ## List of component name sorted by order creation (hierarchy order)
        self.parents = [] ## List of the parent of each component, in same order as self.components

        self.addParameters()

    # =====================================================
    # PARAMETERS FOR RIG OPTIONS

    ## Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        # --------------------------------------------------
        # Main Tab
        self.pRigName = self.addParam("rig_name", "rn", "string", "rig")

        self.pMode = self.addParam("mode", "m", "int", 0)
        self.pStep = self.addParam("step", "step", "long", 0, 0)

        # --------------------------------------------------
        # Colors
        self.pRColorfk = self.addParam("R_color_fk", "rcolfk", "double", 6, 1, 31)
        self.pRColorik = self.addParam("R_color_ik", "rcolik", "double", 5, 1, 31)

        self.pCColorfk = self.addParam("C_color_fk", "ccolfk", "double", 30, 1, 31)
        self.pCColorik = self.addParam("C_color_ik", "ccolik", "double", 9, 1, 31)

        self.pLColorfk = self.addParam("L_color_fk", "lcolfk", "double", 13, 1, 31)
        self.pLColorik = self.addParam("L_color_ik", "lcolik", "double", 4, 1, 31)

        # self.pRColorfkr = self.addParam("R_color_fk_r", "rcolfkr", "double", 0, 0, 1)
        # self.pRColorfkg = self.addParam("R_color_fk_g", "rcolfkg", "double", 0, 0, 1)
        # self.pRColorfkb = self.addParam("R_color_fk_b", "rcolfkb", "double", .75, 0, 1)

        # self.pRColorikr = self.addParam("R_color_ik_r", "rcolikr", "double", 0, 0, 1)
        # self.pRColorikg = self.addParam("R_color_ik_g", "rcolikg", "double", .5, 0, 1)
        # self.pRColorikb = self.addParam("R_color_ik_b", "rcolikb", "double", .75, 0, 1)

        # self.pCColorfkr = self.addParam("C_color_fk_r", "ccolfkr", "double", .5, 0, 1)
        # self.pCColorfkg = self.addParam("C_color_fk_g", "ccolfkg", "double", 0, 0, 1)
        # self.pCColorfkb = self.addParam("C_color_fk_b", "ccolfkb", "double", .5, 0, 1)

        # self.pCColorikr = self.addParam("C_color_ik_r", "ccolikr", "double", .75, 0, 1)
        # self.pCColorikg = self.addParam("C_color_ik_g", "ccolikg", "double", .25, 0, 1)
        # self.pCColorikb = self.addParam("C_color_ik_b", "ccolikb", "double", .75, 0, 1)

        # self.pLColorfkr = self.addParam("L_color_fk_r", "lcolfkr", "double", .75, 0, 1)
        # self.pLColorfkg = self.addParam("L_color_fk_g", "lcolfkg", "double", 0, 0, 1)
        # self.pLColorfkb = self.addParam("L_color_fk_b", "lcolfkb", "double", 0, 0, 1)

        # self.pLColorikr = self.addParam("L_color_ik_r", "lcolikr", "double", .75, 0, 1)
        # self.pLColorikg = self.addParam("L_color_ik_g", "lcolikg", "double", 0.5, 0, 1)
        # self.pLColorikb = self.addParam("L_color_ik_b", "lcolikb", "double", 0, 0, 1)

        # --------------------------------------------------
        # Settings
        self.pShadowRig = self.addParam("shadow_rig", "sr", "bool", False)

        self.pSynoptic = self.addParam("synoptic", "syn", "string", "")

        # --------------------------------------------------
        # Comments
        self.pComments = self.addParam("comments", "co", "string", "")

    # =====================================================
    # SET
    ## set the guide hierarchy from selection.
    # @param self
    def setFromSelection(self):

        selection = ls(selection=True)
        if not selection:
            mgear.log("Select one or more guide root or a guide model", mgear.sev_error)
            self.valid = False
            return False

        for node in selection:
            self.setFromHierarchy(node, node.hasAttr("ismodel"))

        return True

    ## set the guide from given hierarchy.
    # @param self
    # @param root X3DObject - The root of the hierarchy to parse.
    # @param branch Boolean - True to parse children components
    def setFromHierarchy(self, root, branch=True):

        # Start
        mgear.log("Checking guide")

        # Get the model and the root
        self.model = root.getParent(generations=-1)
        while True:
            if root.hasAttr("comp_type") or self.model == root:
                break
            root = root.getParent()

        # ---------------------------------------------------
        # First check and set the options
        mgear.log("Get options")
        if not root.hasAttr("rig_name"):
            mgear.log("%s is not a proper rig guide."%self.model, mgear.sev_error)
            self.valid = False
            return

        self.setParamDefValuesFromProperty(self.model)

        # ---------------------------------------------------
        # Get the controlers
        mgear.log("Get controlers")
        self.controlers_org = dag.findChild(self.model, "controlers_org")
        if self.controlers_org:
            for child in self.controlers_org.getChildren():
                self.controlers[child.name().split("|")[-1]] = child

        # ---------------------------------------------------
        # Components
        mgear.log("Get components")
        self.findComponentRecursive(root, branch)

        # Parenting
        if self.valid:
            mgear.log("Get parenting")
            for name  in self.componentsIndex:
                compChild = self.components[name]
                compChild_parent = compChild.root.getParent()
                for name in self.componentsIndex:
                    compParent = self.components[name]
                    for localName, element in compParent.getObjects(self.model).items():
                        if element is not None and element == compChild_parent:
                            compChild.parentComponent = compParent
                            compChild.parentLocalName = localName
                            break



            # More option values
            self.addOptionsValues()

        # End
        if not self.valid:
            mgear.log("The guide doesn't seem to be up to date. Check logged messages and update the guide.", mgear.sev_warning)

        mgear.log("Guide loaded from hierarchy in [ " + "Not Yet Implemented" + " ]")

    ## Gather or change some options values according to some others.
    # @param self
    def addOptionsValues(self):

        # Convert color sliders to list
        # for s in "RCL":
            # self.values[s+"_color_fk"] = [self.values[s+"_color_fk_r"],self.values[s+"_color_fk_g"],self.values[s+"_color_fk_b"]]
            # self.values[s+"_color_ik"] = [self.values[s+"_color_ik_r"],self.values[s+"_color_ik_g"],self.values[s+"_color_ik_b"]]

        # Get rig size to adapt size of object to the scale of the character
        maximum = 1
        v = dt.Vector()
        for comp in self.components.values():
            for pos in comp.apos:
                d = vec.getDistance(v, pos)
                maximum = max(d, maximum)

        self.values["size"] = max(maximum * .05, .1)

    def findComponentRecursive(self, node, branch=True):

        if node.hasAttr("comp_type"):
            comp_type = node.getAttr("comp_type")
            comp_guide = self.getComponentGuide(comp_type)

            if comp_guide:
                comp_guide.setFromHierarchy(node)
                mgear.log(comp_guide.fullName+" ("+comp_type+")")
                if not comp_guide.valid:
                    self.valid = False

                self.componentsIndex.append(comp_guide.fullName)
                self.components[comp_guide.fullName] = comp_guide

        if branch:
            for child in node.getChildren():
                self.findComponentRecursive(child)

    def getComponentGuide(self, comp_type):

        # Check component type
        path = os.path.join(COMPONENT_PATH, comp_type, "guide.py")
        if not os.path.exists(path):
            mgear.log("Can't find guide definition for : " + comp_type + ".\n"+ path, mgear.sev_error)
            return False

        # Import module and get class
        module_name = "mgear.maya.rig.component."+comp_type+".guide"
        module = __import__(module_name, globals(), locals(), ["*"], -1)
        ComponentGuide = getattr(module , "Guide")

        return ComponentGuide()

##############################
# CLASS
##############################
class Guide_UI(object):

    def __init__(self):

        # Remove existing window
        if cmds.window(GUIDE_UI_WINDOW_NAME, exists=True):
            cmds.deleteUI(GUIDE_UI_WINDOW_NAME)

        # Create Window and main tab
        self.ui_window = cmds.window(GUIDE_UI_WINDOW_NAME, width=400, height=600, title="Guide Tools", sizeable=True)
        self.ui_topLevelColumn = cmds.columnLayout(adjustableColumn=True, columnAlign="center")

        self.ui_tabs = cmds.tabLayout(width=300, height=600, innerMarginWidth=5, innerMarginHeight=5)
        tabWidth = cmds.tabLayout(self.ui_tabs, q=True, width=True)

        #
        self.ui_compColumn = cmds.columnLayout(adj=True, rs=3)
        self.ui_compFrameLayout = cmds.frameLayout(height=300, collapsable=False, borderVisible=False, labelVisible=False)
        self.ui_compList_Scroll = cmds.scrollLayout(hst=0)
        self.ui_compList_column = cmds.columnLayout(columnWidth=300, adj=True, rs=2)
        cmds.separator()

        # List of components
        import mgear.maya.rig.component as comp
        path = os.path.dirname(comp.__file__)
        for comp_name in os.listdir(path):

            if not os.path.exists(os.path.join(path, comp_name, "__init__.py")):
                continue

            module = __import__("mgear.maya.rig.component."+comp_name, globals(), locals(), ["*"], -1)
            reload(module)

            buttonSize = 32
            row = cmds.rowLayout(numberOfColumns=2, columnWidth=([1, buttonSize]), adjustableColumn=2, columnAttach=([1, "both", 0], [2, "both", 5]))
            cmds.symbolButton(width=buttonSize, height=buttonSize, bgc=[1,1,1])

            textColumn = cmds.columnLayout(columnAlign="center")
            cmds.text(align="center", width=250, label=module.NAME)

            cmds.scrollField(text=module.DESCRIPTION, editable=False, width=250, height=50, wordWrap=True)

            cmds.setParent(self.ui_compList_column)
            cmds.separator()

        # Display the window
        cmds.tabLayout(self.ui_tabs, edit=True, tabLabelIndex=([1, "Modules"]))
        cmds.showWindow(self.ui_window)


    def test(self):

        print "YESSS IM HERE !!"

def test():
    print "fuck yeah"