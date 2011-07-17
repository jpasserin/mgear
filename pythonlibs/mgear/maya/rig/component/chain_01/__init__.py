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

## @package mgear.maya.rig.component.chain_01
# @author Jeremie Passerin
#

##########################################################
# GLOBAL
##########################################################
# Maya
from pymel.core.general import *
from pymel.core.animation import *
from pymel.util import *
import pymel.core.datatypes as dt

import maya.OpenMaya as om

# mgear
from mgear.maya.rig.component import MainComponent

import mgear.maya.primitive as pri
import mgear.maya.transform as tra
import mgear.maya.attribute as att
import mgear.maya.node as nod
import mgear.maya.icon as ico
import mgear.maya.vector as vec

##########################################################
# COMPONENT
##########################################################
## The main component class.
class Component(MainComponent):

    # =====================================================
    # OBJECTS
    # =====================================================
    ## Add all the objects needed to create the component.
    # @param self
    def addObjects(self):

        self.normal = self.guide.blades["blade"].z
        self.binormal = self.guide.blades["blade"].x

        self.isFk = self.settings["mode"] != 1
        self.isIk = self.settings["mode"] != 0
        self.isFkIk = self.settings["mode"] == 2

        # FK controlers ------------------------------------
        if self.isFk:
            self.fk_npo = []
            self.fk_ctl = []
            parent = self.root
            for i, t in enumerate(tra.getChainTransform(self.guide.apos, self.normal, self.negate)):
                dist = vec.getDistance(self.guide.apos[i], self.guide.apos[i+1])
                fk_npo = pri.addTransform(parent, self.getName("fk%s_npo"%i), t)
                fk_ctl = self.addCtl(fk_npo, "fk%s_ctl"%i, t, self.color_fk, "cube", w=dist, h=self.size*.1, d=self.size*.1, po=dt.Vector(dist*.5*self.n_factor,0,0))
                parent = fk_ctl
                self.fk_npo.append(fk_npo)
                self.fk_ctl.append(fk_ctl)

        # IK controlers ------------------------------------
        if self.isIk:

            normal = vec.getTransposedVector(self.normal, [self.guide.apos[0], self.guide.apos[1]], [self.guide.apos[-2], self.guide.apos[-1]])
            t = tra.getTransformLookingAt(self.guide.apos[-2], self.guide.apos[-1], normal, "xy", self.negate)
            t = tra.setMatrixPosition(t, self.guide.apos[-1])

            self.ik_cns = pri.addTransform(self.root, self.getName("ik_cns"), t)
            self.ikcns_ctl = self.addCtl(self.ik_cns, "ikcns_ctl", t, self.color_ik, "null", w=self.size)
            self.ik_ctl = self.addCtl(self.ikcns_ctl, "ik_ctl", t, self.color_ik, "cube", w=self.size*.3, h=self.size*.3, d=self.size*.3)

            v = self.guide.apos[-1] - self.guide.apos[0]
            v = v ^ self.normal
            v.normalize()
            v *= self.size
            v += self.guide.apos[1]
            self.upv_cns = pri.addTransformFromPos(self.root, self.getName("upv_cns"), v)

            self.upv_ctl = self.addCtl(self.upv_cns, "upv_ctl", tra.getTransform(self.upv_cns), self.color_ik, "diamond", w=self.size*.1)

            # Chain
            self.chain = pri.add2DChain(self.root, self.getName("chain"), self.guide.apos, self.normal, self.negate)
            self.ikh = pri.addIkHandle(self.root, self.getName("ikh"), self.chain)

        # Chain of deformers -------------------------------
        self.loc = []
        parent = self.root
        for i, t in enumerate(tra.getChainTransform(self.guide.apos, self.normal, self.negate)):
            loc = pri.addTransform(parent, self.getName("%s_loc"%i), t)
            self.addShadow(loc, i)

            self.loc.append(loc)
            parent = loc

    # =====================================================
    # PROPERTY
    # =====================================================
    ## Add parameters to the anim and setup properties to control the component.
    # @param self
    def addAttributes(self):

        # Anim -------------------------------------------
        if self.isFkIk:
            self.blend_att = self.addAnimParam("blend", "Fk/Ik Blend", "double", self.settings["blend"], 0, 1)

        if self.isIk:
            self.roll_att = self.addAnimParam("roll", "Roll", "double", 0, -180, 180)

    # =====================================================
    # OPERATORS
    # =====================================================
    ## Apply operators, constraints, expressions to the hierarchy.\n
    # In order to keep the code clean and easier to debug,
    # we shouldn't create any new object in this method.
    # @param self
    def addOperators(self):

        # Visibilities -------------------------------------
        if self.isFkIk:
            # fk
            fkvis_node = nod.createReverseNode(self.blend_att)

            for fk_ctl in self.fk_ctl:
                for shp in fk_ctl.getShapes():
                    connectAttr(fkvis_node+".outputX", shp.attr("visibility"))

            # ik
            for shp in self.upv_ctl.getShapes():
                connectAttr(self.blend_att, shp.attr("visibility"))
            for shp in self.ikcns_ctl.getShapes():
                connectAttr(self.blend_att, shp.attr("visibility"))
            for shp in self.ik_ctl.getShapes():
                connectAttr(self.blend_att, shp.attr("visibility"))

        # IK Chain -----------------------------------------
        if self.isIk:
            #Constraint and up vector
            pointConstraint(self.ik_ctl, self.ikh, maintainOffset=False)
            poleVectorConstraint(self.upv_ctl, self.ikh)

            connectAttr(self.roll_att, self.ikh.attr("twist"))

        # Chain of deformers -------------------------------
        for i, loc in enumerate(self.loc):

            if self.settings["mode"] == 0: # fk only
                parentConstraint(self.fk_ctl[i], loc, maintainOffset=False)

            elif self.settings["mode"] == 1: # ik only
                parentConstraint( self.chain.bones[i], loc, maintainOffset=False)

            elif self.settings["mode"] == 2: # fk/ik

                rev_node = nod.createReverseNode(self.blend_att)

                # orientation
                cns = orientConstraint(self.fk_ctl[i], self.chain[i], loc, maintainOffset=False)
                weight_att = orientConstraint(cns, query=True, weightAliasList=True)
                connectAttr(rev_node+".outputX", weight_att[0])
                connectAttr(self.blend_att, weight_att[1])

                # position / scaling
                blend_node = createNode("blendColors")
                connectAttr(self.chain[i].attr("translate"), blend_node+".color1")
                connectAttr(self.fk_ctl[i].attr("translate"), blend_node+".color2")
                connectAttr(self.blend_att, blend_node+".blender")

                blend_node = createNode("blendColors")
                connectAttr(self.chain[i].attr("scale"), blend_node+".color1")
                connectAttr(self.fk_ctl[i].attr("scale"), blend_node+".color2")
                connectAttr(self.blend_att, blend_node+".blender")

    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Set the relation beetween object from guide to rig.\n
    # @param self
    def setRelation(self):

        self.relatives["root"] = self.loc[0]
        for i in range(1, len(self.loc)):
            self.relatives["%s_loc"%i] = self.loc[i]
        self.relatives["%s_loc"%(len(self.loc)-1)] = self.loc[-1]
