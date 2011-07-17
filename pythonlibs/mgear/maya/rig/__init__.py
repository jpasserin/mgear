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

## @package mgear.maya.rig
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
# Built in
import sys
import re
import os
import datetime
import getpass

# Maya
from pymel.core import *
from pymel.util import *
import pymel.core.datatypes as dt

# mgear
import mgear
from mgear.maya.rig.guide import RigGuide
from mgear.maya.rig.component import MainComponent

import mgear.maya.primitive as pri
import mgear.maya.icon as ico
import mgear.maya.attribute as att
import mgear.maya.node as nod

##########################################################
# RIG
##########################################################
## The main rig class.
class Rig(object):

    # =====================================================
    ## Init Method
    # @param self
    def __init__(self):

        self.guide = RigGuide()

        ## Dictionary of Groups.
        self.groups = {}
        
        ## Dictionary of component.\n
        # Keys are the component fullname (ie. 'arm_L0')
        self.components = {}
        self.componentsIndex = []

    # =====================================================
    ## Build the rig from selected guides.
    # @param self
    def buildFromSelection(self):

        # Cet the option first otherwise the change wight might do won't be taken
        sel = ls(selection=True)

        # Check guide is valid
        self.guide.setFromSelection()
        if not self.guide.valid:
            return

        # Build
        self.build()

    # =====================================================
    # @param self
    def build(self):

        self.options = self.guide.values
        self.guides = self.guide.components

        mgear.log("= GEAR RIG SYSTEM ==============================================")

        self.initialHierarchy()
        self.processComponents()
        self.finalize()

        mgear.log("= GEAR BUILD RIG DONE ================ [ " + "Not Yet Implemented" + " ] ======")

        return self.model

    # =====================================================
    ## Build the initial hierarchy of the rig
    # Create the rig model, the main properties, and a couple of base organisation nulls
    # Get the global size of the rig
    # @param self
    def initialHierarchy(self):
    
        mgear.log("Initial Hierarchy")

        # --------------------------------------------------
        # Model
        self.model = pri.addTransformFromPos(None, self.options["rig_name"])
        att.lockAttribute(self.model)

        # --------------------------------------------------
        # Global Ctl
        self.global_ctl = self.addCtl(self.model, "global_C0_ctl", dt.Matrix(), self.options["C_color_fk"], "crossarrow", w=10)
        
        # --------------------------------------------------
        # INFOS
        self.isRig_att       = att.addAttribute(self.model, "is_rig", "bool", True)
        self.rigName_att     = att.addAttribute(self.model, "rig_name", "string", self.options["rig_name"])
        self.user_att        = att.addAttribute(self.model, "user", "string", getpass.getuser())
        self.isWip_att       = att.addAttribute(self.model, "wip", "bool", self.options["mode"] != 0)
        self.date_att        = att.addAttribute(self.model, "date", "string", str(datetime.datetime.now()))
        self.mayaVersion_att = att.addAttribute(self.model, "maya_version", "string", str(mel.eval("getApplicationVersionAsFloat")))
        self.gearVersion_att = att.addAttribute(self.model, "gear_version", "string", mgear.getVersion())
        self.synoptic_att    = att.addAttribute(self.model, "synoptic", "string", str(self.options["synoptic"]))
        self.comments_att    = att.addAttribute(self.model, "comments", "string", str(self.options["comments"]))
        self.ctlVis_att      = att.addAttribute(self.model, "ctl_vis", "bool", True)
        self.shdVis_att      = att.addAttribute(self.model, "shd_vis", "bool", False)
        
        self.qsA_att         = att.addAttribute(self.model, "quickselA", "string", "")
        self.qsB_att         = att.addAttribute(self.model, "quickselB", "string", "")
        self.qsC_att         = att.addAttribute(self.model, "quickselC", "string", "")
        self.qsD_att         = att.addAttribute(self.model, "quickselD", "string", "")
        self.qsE_att         = att.addAttribute(self.model, "quickselE", "string", "")
        self.qsF_att         = att.addAttribute(self.model, "quickselF", "string", "")

        # --------------------------------------------------
        # UI SETUP AND ANIM
        self.oglLevel_att  = att.addAttribute(self.model, "ogl_level", "long", 0, None, None, 0, 3)

        # --------------------------------------------------
        # Basic set of null
        if self.options["shadow_rig"]:
            self.shd_org = pri.addTransformFromPos(self.model, "shd_org")
            connectAttr(self.shdVis_att, self.shd_org.attr("visibility"))

    # =====================================================
    def processComponents(self):

        # Init
        self.components_infos = {}
        for guide in self.guides.values():
            mgear.log("Init : "+ guide.fullName + " ("+guide.type+")")

            module_name = "mgear.maya.rig.component."+guide.type
            module = __import__(module_name, globals(), locals(), ["*"], -1)
            Component = getattr(module , "Component")

            component = Component(self, guide)
            if component.fullName not in self.componentsIndex:
                self.components[component.fullName] = component
                self.componentsIndex.append(component.fullName)

                self.components_infos[component.fullName] = [guide.compType, guide.getVersion(), guide.author]

        # Creation steps
        self.steps = MainComponent.steps

        for i, name in enumerate(self.steps):
            for count, compName in enumerate(self.componentsIndex):
                component = self.components[compName]
                mgear.log(name+" : "+ component.fullName + " ("+component.type+")")
                component.stepMethods[i]()

            if self.options["step"] >= 1 and i >= self.options["step"]-1:
                break
                
    
    # =====================================================
    ## Build the initial hierarchy of the rig
    # @param self
    def finalize(self):

        # Properties --------------------------------------
        mgear.log("Finalize")
            
        # Groups ------------------------------------------
        mgear.log("Creating groups")
        # Retrieve group content from components
        for name in self.componentsIndex:
            component = self.components[name]
            for name, objects in component.groups.items():
                self.addToGroup(objects, name)

        # Creating all groups
        select(cl=True)
        for name, objects in self.groups.items():
            s = sets(n=self.model.name()+"_"+name+"_grp")
            s.union( objects ) 
            
        # Bind pose ---------------------------------------
        print self.groups["controlers"]
        select(self.groups["controlers"])
        node = dagPose(save=True, selection=True)
        print node
            
    # =====================================================
    def addCtl(self, parent, name, m, color, icon, **kwargs):

        if name in self.guide.controlers.keys():
            ctl_ref = self.guide.controlers[name]
            ctl = pri.addTransform(parent, name, m)
            for shape in ctl_ref.getShapes():
                ctl.addChild(shape, shape=True, add=True)
        else:
            ctl = ico.create(parent, name, m, color, icon, **kwargs)
            
        self.addToGroup(ctl, "controlers")
        
        return ctl
        
    # =====================================================
    ## Add the object in a collection for later group creation.
    # @param self
    # @param objs Single or List of X3DObject - object to put in group.
    # @param names Single or List of String - names of the groups to create.
    def addToGroup(self, objects, names=["hidden"]):

        if not isinstance(names, list):
            names = [names]

        if not isinstance(objects, list):
            objects = [objects]

        # objects = [obj for obj in objects if obj is not None]

        for name in names:
            if name not in self.groups.keys():
                self.groups[name] = []

            self.groups[name].extend(objects)
            
    # =====================================================
    ## Return the object in the rig matching the guide object.
    # @param self
    # @param guideName String - Name of the guide object
    def findChild(self, guideName):

        if guideName is None:
            return self.global_ctl

        localName = guideName.split("|")[-1]
        comp_name = "_".join(localName.split("_")[:2])
        child_name = "_".join(localName.split("_")[2:])

        if comp_name not in self.components.keys():
            return self.global_ctl

        return self.components[comp_name].getRelation(child_name)

    def findComponent(self, guideName):
    
        if guideName is None:
            return None

        comp_name = "_".join(guideName.split("_")[:2])
        child_name = "_".join(guideName.split("_")[2:])

        if comp_name not in self.components.keys():
            return None

        return self.components[comp_name]

    def findUIHost(self, guideName):

        if guideName is None:
            return self.ui

        comp_name = "_".join(guideName.split("_")[:2])
        child_name = "_".join(guideName.split("_")[2:])

        if comp_name not in self.components.keys():
            return self.ui

        if self.components[comp_name].ui is None:
            self.components[comp_name].ui = UIHost(self.components[comp_name].root)

        return self.components[comp_name].ui

