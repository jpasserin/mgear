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

## @package mgear.maya.rig.component.leg_2jnt_01
# @author Jeremie Passerin
#
#############################################
# GLOBAL
#############################################
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
import mgear.maya.applyop as aop
import mgear.maya.fcurve as fcu

#############################################
# COMPONENT
#############################################
class Component(MainComponent):

    def addObjects(self):

        self.normal = self.getNormalFromPos(self.guide.apos)

        self.length0 = vec.getDistance(self.guide.apos[0], self.guide.apos[1])
        self.length1 = vec.getDistance(self.guide.apos[1], self.guide.apos[2])
        self.length2 = vec.getDistance(self.guide.apos[2], self.guide.apos[3])

        # FK Controlers -----------------------------------
        t = tra.getTransformLookingAt(self.guide.apos[0], self.guide.apos[1], self.normal, "xz", self.negate)
        
        self.fk0_npo = pri.addTransform(self.root, self.getName("fk0_npo"), t)
        
        self.fk0_ctl = self.addCtl(self.fk0_npo, "fk0_ctl", t, self.color_fk, "cube", w=self.length0, h=self.size*.1, d=self.size*.1, po=dt.Vector(.5*self.length0*self.n_factor,0,0))

        t = tra.getTransformLookingAt(self.guide.apos[1], self.guide.apos[2], self.normal, "xz", self.negate)
        self.fk1_ctl = self.addCtl(self.fk0_ctl, "fk1_ctl", t, self.color_fk, "cube", w=self.length1, h=self.size*.1, d=self.size*.1, po=dt.Vector(.5*self.length1*self.n_factor,0,0))

        t = tra.getTransformLookingAt(self.guide.apos[2], self.guide.apos[3], self.normal, "xz", self.negate)
        self.fk2_ctl = self.addCtl(self.fk1_ctl, "fk2_ctl", t, self.color_fk, "cube", w=self.length2, h=self.size*.1, d=self.size*.1, po=dt.Vector(.5*self.length2*self.n_factor,0,0))
        self.fk_ctl = [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl]

        # IK Controlers -----------------------------------

        self.ik_cns = pri.addTransformFromPos(self.root, self.getName("ik_cns"), self.guide.pos["ankle"])

        self.ikcns_ctl = self.addCtl(self.ik_cns, "ikcns_ctl", tra.getTransformFromPos(self.guide.pos["ankle"]), self.color_ik, "null", w=self.size*.12)

        m = tra.getTransformLookingAt(self.guide.pos["ankle"], self.guide.pos["eff"], self.x_axis, "zx", False)
        self.ik_ctl = self.addCtl(self.ikcns_ctl, "ik_ctl", tra.getTransformFromPos(self.guide.pos["ankle"]), self.color_ik, "cube", w=self.size*.12, h=self.size*.12, d=self.size*.12)

        # upv
        v = self.guide.apos[2] - self.guide.apos[0]
        v = self.normal ^ v
        v.normalize()
        v *= self.size*.5
        v += self.guide.apos[1]

        self.upv_cns = pri.addTransformFromPos(self.root, self.getName("upv_cns"), v)

        self.upv_ctl = self.addCtl(self.upv_cns, "upv_ctl", tra.getTransform(self.upv_cns), self.color_ik, "diamond", w=self.size*.12)
        att.setKeyableAttributes(self.upv_ctl, self.t_params)

        # References --------------------------------------
        self.ik_ref = pri.addTransform(self.ik_ctl, self.getName("ik_ref"), tra.getTransform(self.ik_ctl))
        self.fk_ref = pri.addTransform(self.fk_ctl[2], self.getName("fk_ref"), tra.getTransform(self.ik_ctl))

        # Chain --------------------------------------------
        # The outputs of the ikfk2bone solver
        self.bone0 = pri.addLocator(self.root, self.getName("0_jnt"), tra.getTransform(self.fk_ctl[0]))
        self.bone0_shp = self.bone0.getShape()
        self.bone0_shp.setAttr("localPositionX", self.n_factor*.5)
        self.bone0_shp.setAttr("localScale", .5, 0, 0)
        self.bone0.setAttr("sx", self.length0)
        self.bone0.setAttr("visibility", False)

        self.bone1 = pri.addLocator(self.root, self.getName("1_jnt"), tra.getTransform(self.fk_ctl[1]))
        self.bone1_shp = self.bone1.getShape()
        self.bone1_shp.setAttr("localPositionX", self.n_factor*.5)
        self.bone1_shp.setAttr("localScale", .5, 0, 0)
        self.bone1.setAttr("sx", self.length1)
        self.bone1.setAttr("visibility", False)

        self.ctrn_loc = pri.addTransformFromPos(self.root, self.getName("ctrn_loc"), self.guide.apos[1])
        self.eff_loc  = pri.addTransformFromPos(self.root, self.getName("eff_loc"), self.guide.apos[2])

        # tws_ref
        t = tra.getRotationFromAxis(dt.Vector(0,-1,0), self.normal, "xz", self.negate)
        t = tra.setMatrixPosition(t, self.guide.pos["ankle"])  
        
        self.tws_ref = pri.addTransform(self.eff_loc, self.getName("tws_ref"), t)
        
        # Mid Controler ------------------------------------
        self.mid_ctl = self.addCtl(self.ctrn_loc, "mid_ctl", tra.getTransform(self.ctrn_loc), self.color_ik, "sphere", w=self.size*.2)

        # Twist references ---------------------------------
        x = dt.Vector(0,-1,0)
        x = x * tra.getTransform(self.eff_loc)
        z = dt.Vector(self.normal.x,self.normal.y,self.normal.z)
        z = z * tra.getTransform(self.eff_loc)

        m = tra.getRotationFromAxis(x, z, "xz", self.negate)
        m = tra.setMatrixPosition(m, tra.getTranslation(self.ik_ctl))

        # self.tws_ref = pri.addTransform(self.eff_loc, self.getName("tws_ref"), m)

        self.tws0_loc = pri.addTransform(self.root, self.getName("tws0_loc"), tra.getTransform(self.fk_ctl[0]))
        self.tws0_rot = pri.addTransform(self.tws0_loc, self.getName("tws0_rot"), tra.getTransform(self.fk_ctl[0]))

        self.tws1_loc = pri.addTransform(self.ctrn_loc, self.getName("tws1_loc"), tra.getTransform(self.ctrn_loc))
        self.tws1_rot = pri.addTransform(self.tws1_loc, self.getName("tws1_rot"), tra.getTransform(self.ctrn_loc))

        self.tws2_loc = pri.addTransform(self.root, self.getName("tws2_loc"), tra.getTransform(self.tws_ref))
        self.tws2_rot = pri.addTransform(self.tws2_loc, self.getName("tws2_rot"), tra.getTransform(self.tws_ref))
        self.tws2_rot.setAttr("sx", .001)

        # Divisions ----------------------------------------
        # We have at least one division at the start, the end and one for the elbow.
        self.divisions = self.settings["div0"] + self.settings["div1"] + 3

        self.div_cns = []
        for i in range(self.divisions):

            div_cns = pri.addTransform(self.root, self.getName("div%s_loc" % i))

            self.div_cns.append(div_cns)

            self.addShadow(div_cns, i)

        # End reference ------------------------------------
        # To help the deformation on the ankle
        self.end_ref = pri.addTransform(self.tws2_rot, self.getName("end_ref"), m)
        self.addShadow(self.end_ref, "end")

    def addAttributes(self):

        # Anim -------------------------------------------
        self.blend_att = self.addAnimParam("blend", "Fk/Ik Blend", "double", self.settings["blend"], 0, 1)
        self.roll_att = self.addAnimParam("roll", "Roll", "double", 0, -180, 180)

        self.scale_att = self.addAnimParam("ikscale", "Scale", "double", 1, .001, 99)
        self.maxstretch_att = self.addAnimParam("maxstretch", "Max Stretch", "double", 1.5, 1, 99)
        self.slide_att = self.addAnimParam("slide", "Slide", "double", .5, 0, 1)
        self.softness_att = self.addAnimParam("softness", "Softness", "double", 0, 0, 1)
        self.reverse_att = self.addAnimParam("reverse", "Reverse", "double", 0, 0, 1)
        self.roundness_att = self.addAnimParam("roundness", "Roundness", "double", 0, 0, 1)
        self.volume_att = self.addAnimParam("volume", "Volume", "double", 1, 0, 1)
        
        # Ref
        if self.settings["ikrefarray"]:
            ref_names = self.settings["ikrefarray"].split(",")
            if len(ref_names) > 1:
                self.ikref_att = self.addAnimEnumParam("ikref", "Ik Ref", 0, self.settings["ikrefarray"].split(","))
                
        if self.settings["upvrefarray"]:
            ref_names = self.settings["upvrefarray"].split(",")
            if len(ref_names) > 1:
                self.upvref_att = self.addAnimEnumParam("upvref", "UpV Ref", 0, self.settings["upvrefarray"].split(","))

        # Setup ------------------------------------------
        # Eval Fcurve
        self.st_value = fcu.getFCurveValues(self.settings["st_profile"], self.divisions)
        self.sq_value = fcu.getFCurveValues(self.settings["sq_profile"], self.divisions)
        
        self.st_att = [ self.addSetupParam("stretch_%s"%i, "Stretch %s"%i, "double", self.st_value[i], -1, 0) for i in range(self.divisions) ]
        self.sq_att = [ self.addSetupParam("squash_%s"%i, "Squash %s"%i, "double", self.sq_value[i], 0, 1) for i in range(self.divisions) ]

        self.resample_att = self.addSetupParam("resample", "Resample", "bool", True)
        self.absolute_att = self.addSetupParam("absolute", "Absolute", "bool", False)

    def addOperators(self):

        # Visibilities -------------------------------------
        #shape.dispGeometry
        # fk
        fkvis_node = nod.createReverseNode(self.blend_att)
        
        for shp in self.fk0_ctl.getShapes():
            connectAttr(fkvis_node+".outputX", shp.attr("visibility"))
        for shp in self.fk1_ctl.getShapes():
            connectAttr(fkvis_node+".outputX", shp.attr("visibility"))
        for shp in self.fk2_ctl.getShapes():
            connectAttr(fkvis_node+".outputX", shp.attr("visibility"))

        # ik
        for shp in self.upv_ctl.getShapes():
            connectAttr(self.blend_att, shp.attr("visibility"))
        for shp in self.ikcns_ctl.getShapes():
            connectAttr(self.blend_att, shp.attr("visibility"))
        for shp in self.ik_ctl.getShapes():
            connectAttr(self.blend_att, shp.attr("visibility"))

        # IK Solver -----------------------------------------
        out = [self.bone0, self.bone1, self.ctrn_loc, self.eff_loc]
        node = aop.gear_ikfk2bone_op(out, self.root, self.ik_ref, self.upv_ctl, self.fk_ctl[0], self.fk_ctl[1], self.fk_ref, self.length0, self.length1, self.negate)

        connectAttr(self.blend_att, node+".blend")
        connectAttr(self.roll_att, node+".roll")
        connectAttr(self.scale_att, node+".scaleA")
        connectAttr(self.scale_att, node+".scaleB")
        connectAttr(self.maxstretch_att, node+".maxstretch")
        connectAttr(self.slide_att, node+".slide")
        connectAttr(self.softness_att, node+".softness")
        connectAttr(self.reverse_att, node+".reverse")

        # Twist references ---------------------------------
        pointConstraint(self.root, self.tws0_loc, maintainOffset=True)
        cns = aop.aimCns(self.tws0_loc, self.mid_ctl, self.n_sign+"xz", 2, [-1,0,0], self.root, False)

        pointConstraint(self.mid_ctl, self.tws1_loc, maintainOffset=False)
        scaleConstraint(self.mid_ctl, self.tws1_loc, maintainOffset=False)
        orientConstraint(self.mid_ctl, self.tws1_rot, maintainOffset=False)

        pointConstraint(self.eff_loc, self.tws2_loc, maintainOffset=False)
        scaleConstraint(self.eff_loc, self.tws2_loc, maintainOffset=False)
        orientConstraint(self.bone1, self.tws2_loc, maintainOffset=False) 
        orientConstraint(self.tws_ref, self.tws2_rot, maintainOffset=False)
        # att.setRotOrder(self.tws2_rot, "YZX")

        self.tws0_loc.setAttr("sx", .001)
        self.tws2_loc.setAttr("sx", .001)

        add_node = nod.createAddNode(self.roundness_att, .001)
        connectAttr(add_node+".output", self.tws1_rot.attr("sx"))

        # Volume -------------------------------------------
        distA_node = nod.createDistNode(self.tws0_loc, self.tws1_loc)
        distB_node = nod.createDistNode(self.tws1_loc, self.tws2_loc)
        add_node = nod.createAddNode(distA_node+".distance", distB_node+".distance")
        div_node = nod.createDivNode(add_node+".output", self.root.attr("sx"))
        self.volDriver_att = div_node+".outputX"

        # Divisions ----------------------------------------
        # at 0 or 1 the division will follow exactly the rotation of the controler.. and we wont have this nice tangent + roll
        for i, div_cns in enumerate(self.div_cns):

            if i < (self.settings["div0"]+1):
                perc = i*.5 / (self.settings["div0"]+1.0)
            else:
                perc = .5 + (i-self.settings["div0"]-1.0)*.5 / (self.settings["div1"]+1.0)

            perc = max(.001, min(.999, perc))

            # Roll
            if self.negate:
                node = aop.gear_rollsplinekine_op(div_cns, [self.tws2_rot, self.tws1_rot, self.tws0_rot], 1-perc)
            else:
                node = aop.gear_rollsplinekine_op(div_cns, [self.tws0_rot, self.tws1_rot, self.tws2_rot], perc)

            connectAttr(self.resample_att, node+".resample")
            connectAttr(self.absolute_att, node+".absolute")

            # Squash n Stretch
            node = aop.gear_squashstretch2_op(div_cns, None, getAttr(self.volDriver_att), "x")
            connectAttr(self.volume_att, node+".blend")
            connectAttr(self.volDriver_att, node+".driver")
            connectAttr(self.st_att[i], node+".stretch")
            connectAttr(self.sq_att[i], node+".squash")

        return

    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Set the relation beetween object from guide to rig.\n
    # @param self
    def setRelation(self):
        self.relatives["root"] = self.bone0
        self.relatives["knee"] = self.bone1
        self.relatives["ankle"] = self.tws2_rot
        self.relatives["eff"] = self.tws2_rot

    ## standard connection definition.
    # @param self
    def connect_standard(self):
        self.connect_standardWithIkRef()