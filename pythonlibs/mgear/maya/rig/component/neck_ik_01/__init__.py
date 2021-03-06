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

## @package mgear.maya.rig.component.neck_ik_01
# @author Jeremie Passerin
#

##########################################################
# GLOBAL
##########################################################
# Maya
from pymel.core.general import *
from pymel.core.animation import *
from pymel.core.modeling import *
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
import mgear.maya.curve as cur
import mgear.maya.fcurve as fcu

##########################################################
# COMPONENT
##########################################################
## The main component class.
class Component(MainComponent):

    # =====================================================
    # OBJECTS
    # =====================================================
    ## Build the initial hierarchy of the component.\n
    # Add the root and if needed the shadow root
    # @param self
    def initialHierarchy(self):

        # Root ---------------------------------------------
        # For this component we need the root to be correctly oriented
        t = tra.getTransformLookingAt(self.guide.apos[0], self.guide.apos[1], self.guide.blades["blade"].z, "yx", self.negate)
        self.root = pri.addTransform(self.model, self.getName("root"), t)

        # Shd ----------------------------------------------
        if self.options["shadow_rig"]:
            self.shd_org = pri.addTransform(self.rig.shd_org, self.getName("shd_org"))

    ## Add all the objects needed to create the component.
    # @param self
    def addObjects(self):

        # Ik Controlers ------------------------------------
        t = tra.getTransformLookingAt(self.guide.pos["tan1"], self.guide.pos["neck"], self.guide.blades["blade"].z, "yx", self.negate)
        t = tra.setMatrixPosition(t, self.guide.pos["neck"])
        self.ik_cns = pri.addTransform(self.root, self.getName("ik_cns"), t)

        self.ik_ctl = self.addCtl(self.ik_cns, "ik_ctl", t, self.color_ik, "compas", w=self.size*.5)
        att.setKeyableAttributes(self.ik_ctl)
        att.setRotOrder(self.ik_ctl, "XZY")

        # Tangents -----------------------------------------
        t = tra.setMatrixPosition(t, self.guide.pos["tan1"])
        self.tan1_loc = pri.addTransform(self.ik_ctl, self.getName("tan1_loc"), t)

        t = tra.getTransformLookingAt(self.guide.pos["root"], self.guide.pos["tan0"], self.guide.blades["blade"].z, "yx", self.negate)
        t = tra.setMatrixPosition(t, self.guide.pos["tan0"])
        self.tan0_loc = pri.addTransform(self.root, self.getName("tan0_loc"), t)

        # Curves -------------------------------------------
        self.mst_crv = cur.addCnsCurve(self.root, self.getName("mst_crv"), [self.root, self.tan0_loc, self.tan1_loc, self.ik_ctl], 3)
        self.slv_crv = cur.addCurve(self.root, self.getName("slv_crv"), [dt.Vector()]*10, False, 3)
        self.mst_crv.setAttr("visibility", False)
        self.slv_crv.setAttr("visibility", False)

        # Division -----------------------------------------
        # The user only define how many intermediate division he wants.
        # First and last divisions are an obligation.
        parentdiv = self.root
        parentctl = self.root
        self.div_cns = []
        self.fk_ctl = []
        self.fk_npo = []
        self.scl_npo = []
        for i in range(self.settings["division"]):

            # References
            div_cns = pri.addTransform(parentdiv, self.getName("%s_cns"%i))
            setAttr(div_cns+".inheritsTransform", False)
            self.div_cns.append(div_cns)
            parentdiv = div_cns

            scl_npo = pri.addTransform(parentctl, self.getName("%s_scl_npo"%i), tra.getTransform(parentctl))

            # Controlers (First and last one are fake)
            if i in [0, self.settings["division"] - 1]:
                fk_ctl = pri.addTransform(scl_npo, self.getName("%s_loc"%i), tra.getTransform(parentctl))
                fk_npo = fk_ctl
            else:
                fk_npo = pri.addTransform(scl_npo, self.getName("fk%s_npo"%(i-1)), tra.getTransform(parentctl))
                fk_ctl = self.addCtl(fk_npo, "fk%s_ctl"%(i-1), tra.getTransform(parentctl), self.color_fk, "cube", w=self.size*.2, h=self.size*.05, d=self.size*.2)
                att.setKeyableAttributes(self.fk_ctl)
                att.setRotOrder(fk_ctl, "XZY")


            # setAttr(fk_npo+".inheritsTransform", False)
            self.scl_npo.append(scl_npo)
            self.fk_npo.append(fk_npo)
            self.fk_ctl.append(fk_ctl)
            parentctl = fk_ctl

            # Deformers (Shadow)
            self.addShadow(fk_ctl, i)

        # Head ---------------------------------------------
        t = tra.getTransformLookingAt(self.guide.pos["head"], self.guide.pos["eff"], self.guide.blades["blade"].z, "yx", self.negate)
        self.head_cns = pri.addTransform(self.root, self.getName("head_cns"), t)

        dist = vec.getDistance(self.guide.pos["head"], self.guide.pos["eff"])
        self.head_ctl = self.addCtl(self.head_cns, "head_ctl", t, self.color_fk, "cube", w=self.size*.5, h=dist, d=self.size*.5, po=dt.Vector(0,dist*.5,0))
        att.setRotOrder(self.head_ctl, "XZY")

        self.addShadow(self.head_ctl, "head")

    # =====================================================
    # PROPERTY
    # =====================================================
    ## Add parameters to the anim and setup properties to control the component.
    # @param self
    def addAttributes(self):
        # Anim -------------------------------------------
        self.maxstretch_att = self.addAnimParam("maxstretch", "Max Stretch", "double", self.settings["maxstretch"], 1)
        self.maxsquash_att = self.addAnimParam("maxsquash", "MaxSquash", "double", self.settings["maxsquash"], 0, 1)
        self.softness_att = self.addAnimParam("softness", "Softness", "double", self.settings["softness"], 0, 1)

        self.lock_ori_att = self.addAnimParam("lock_ori", "Lock Ori", "double", 1, 0, 1)

        self.tan0_att = self.addAnimParam("tan0", "Tangent 0", "double", 1, 0)
        self.tan1_att = self.addAnimParam("tan1", "Tangent 1", "double", 1, 0)

        # Volume
        self.volume_att = self.addAnimParam("volume", "Volume", "double", 1, 0, 1)

        # Ref
        if self.settings["ikrefarray"]:
            ref_names = self.settings["ikrefarray"].split(",")
            if len(ref_names) > 1:
                self.ikref_att = self.addAnimEnumParam("ikref", "Ik Ref", 0, self.settings["ikrefarray"].split(","))

        if self.settings["headrefarray"]:
            ref_names = self.settings["headrefarray"].split(",")
            if len(ref_names) > 1:
                ref_names.insert(0, "self")
                self.headref_att = self.addAnimEnumParam("headref", "Head Ref", 0, ref_names)

        # Setup ------------------------------------------
        # Eval Fcurve
        self.st_value = fcu.getFCurveValues(self.settings["st_profile"], self.settings["division"])
        self.sq_value = fcu.getFCurveValues(self.settings["sq_profile"], self.settings["division"])

        self.st_att = [ self.addSetupParam("stretch_%s"%i, "Stretch %s"%i, "double", self.st_value[i], -1, 0) for i in range(self.settings["division"]) ]
        self.sq_att = [ self.addSetupParam("squash_%s"%i, "Squash %s"%i, "double", self.sq_value[i], 0, 1) for i in range(self.settings["division"]) ]

    # =====================================================
    # OPERATORS
    # =====================================================
    ## Apply operators, constraints, expressions to the hierarchy.\n
    # In order to keep the code clean and easier to debug,
    # we shouldn't create any new object in this method.
    # @param self
    def addOperators(self):

        # Tangent position ---------------------------------
        # common part
        d = vec.getDistance(self.guide.pos["root"], self.guide.pos["neck"])
        dist_node = nod.createDistNode(self.root, self.ik_ctl)
        rootWorld_node = nod.createDecomposeMatrixNode(self.root.attr("worldMatrix"))
        div_node = nod.createDivNode(dist_node+".distance", rootWorld_node+".outputScaleX")
        div_node = nod.createDivNode(div_node+".outputX", d)

        # tan0
        mul_node = nod.createMulNode(self.tan0_att, self.tan0_loc.getAttr("ty"))
        res_node = nod.createMulNode(mul_node+".outputX", div_node+".outputX")
        connectAttr( res_node+".outputX", self.tan0_loc+".ty")

        # tan1
        mul_node = nod.createMulNode(self.tan1_att, self.tan1_loc.getAttr("ty"))
        res_node = nod.createMulNode(mul_node+".outputX", div_node+".outputX")
        connectAttr( res_node+".outputX", self.tan1_loc.attr("ty"))

        # Curves -------------------------------------------
        op = aop.gear_curveslide2_op(self.slv_crv, self.mst_crv, 0, 1.5, .5, .5)
        connectAttr(self.maxstretch_att, op+".maxstretch")
        connectAttr(self.maxsquash_att, op+".maxsquash")
        connectAttr(self.softness_att, op+".softness")

        # Volume driver ------------------------------------
        crv_node = nod.createCurveInfoNode(self.slv_crv)

        # Division -----------------------------------------
        for i in range(self.settings["division"]):

            # References
            u = i / (self.settings["division"] - 1.0)

            cns = aop.pathCns(self.div_cns[i], self.slv_crv, False, u, True)
            cns.setAttr("frontAxis", 1)# front axis is 'Y'
            cns.setAttr("upAxis", 2)# front axis is 'Z'

            # Roll
            aop.gear_spinePointAtOp(cns, self.root, self.ik_ctl, u, "Z")

            # Squash n Stretch
            op = aop.gear_squashstretch2_op(self.fk_npo[i], self.root, arclen(self.slv_crv), "y")
            connectAttr(self.volume_att, op+".blend")
            connectAttr(crv_node+".arcLength", op+".driver")
            connectAttr(self.st_att[i], op+".stretch")
            connectAttr(self.sq_att[i], op+".squash")

            # scl compas
            if i != 0:
                div_node = nod.createDivNode([1,1,1], [self.fk_npo[i-1]+".sx", self.fk_npo[i-1]+".sy", self.fk_npo[i-1]+".sz"])
                connectAttr(div_node+".output", self.scl_npo[i]+".scale")

            # Controlers
            if i == 0:
                mulmat_node = aop.gear_mulmatrix_op(self.div_cns[i].attr("worldMatrix"), self.root.attr("worldInverseMatrix"))
            else:
                mulmat_node = aop.gear_mulmatrix_op(self.div_cns[i].attr("worldMatrix"), self.div_cns[i-1].attr("worldInverseMatrix"))

            dm_node = nod.createDecomposeMatrixNode(mulmat_node+".output")
            connectAttr(dm_node+".outputTranslate", self.fk_npo[i].attr("t"))
            connectAttr(dm_node+".outputRotate", self.fk_npo[i].attr("r"))
            #connectAttr(dm_node+".outputScale", self.fk_npo[i].attr("s"))

            # Orientation Lock
            if i == self.settings["division"] - 1 :
                dm_node = nod.createDecomposeMatrixNode(self.ik_ctl+".worldMatrix")
                blend_node = nod.createBlendNode([dm_node+".outputRotate%s"%s for s in "XYZ"], [cns+".rotate%s"%s for s in "XYZ"], self.lock_ori_att)
                self.div_cns[i].attr("rotate").disconnect()
                connectAttr(blend_node+".output", self.div_cns[i]+".rotate")


        # Head ---------------------------------------------
        self.fk_ctl[-1].addChild(self.head_cns)

    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Set the relation beetween object from guide to rig.\n
    # @param self
    def setRelation(self):
        self.relatives["root"] = self.root
        self.relatives["tan1"] = self.root
        self.relatives["tan2"] = self.head_ctl
        self.relatives["neck"] = self.head_ctl
        self.relatives["head"] = self.head_ctl
        self.relatives["eff"] = self.head_ctl

    ## standard connection definition.
    # @param self
    def connect_standard(self):
        self.connect_standardWithIkRef()

    ## standard connection definition with ik and upv references.
    # @param self
    def connect_standardWithIkRef(self):

        self.parent.addChild(self.root)

        self.connectRef(self.settings["ikrefarray"], self.ik_cns)


        if self.settings["headrefarray"]:
            ref_names = self.settings["headrefarray"].split(",")

            ref = []
            for ref_name in ref_names:
                ref.append(self.rig.findChild(ref_name))

            ref.append(self.head_cns)
            cns_node = parentConstraint(*ref, skipTranslate="none", maintainOffset=True)
            cns_attr = parentConstraint(cns_node, query=True, weightAliasList=True)
            self.head_cns.attr("tx").disconnect()
            self.head_cns.attr("ty").disconnect()
            self.head_cns.attr("tz").disconnect()

            for i, attr in enumerate(cns_attr):
                node_name = createNode("condition")
                connectAttr(self.headref_att, node_name+".firstTerm")
                setAttr(node_name+".secondTerm", i+1)
                setAttr(node_name+".operation", 0)
                setAttr(node_name+".colorIfTrueR", 1)
                setAttr(node_name+".colorIfFalseR", 0)
                connectAttr(node_name+".outColorR", attr)
