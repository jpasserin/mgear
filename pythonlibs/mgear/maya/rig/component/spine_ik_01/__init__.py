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

## @package mgear.maya.rig.component.spine_ik_01
# @author Jeremie Passerin
#

#############################################
# GLOBAL
#############################################
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

#############################################
# COMPONENT
#############################################
class Component(MainComponent):

    def addObjects(self):

        # Ik Controlers ------------------------------------
        t = tra.getTransformLookingAt(self.guide.apos[0], self.guide.apos[1], self.guide.blades["blade"].z, "yx", self.negate)
        self.ik0_npo = pri.addTransform(self.root, self.getName("ik0_npo"), t)
        self.ik0_ctl = self.addCtl(self.ik0_npo, "ik0_ctl", t, self.color_ik, "compas", w=self.size)
        att.setKeyableAttributes(self.ik0_ctl)
        att.setRotOrder(self.ik0_ctl, "XZY")

        t = tra.setMatrixPosition(t, self.guide.apos[1])
        self.ik1_npo = pri.addTransform(self.root, self.getName("ik1_npo"), t)
        self.ik1_ctl = self.addCtl(self.ik1_npo, "ik1_ctl", t, self.color_ik, "compas", w=self.size)
        att.setKeyableAttributes(self.ik1_ctl)
        att.setRotOrder(self.ik1_ctl, "XZY")

        # Tangent controlers -------------------------------
        t = tra.setMatrixPosition(t, vec.linearlyInterpolate(self.guide.apos[0], self.guide.apos[1], .33))
        self.tan0_npo = pri.addTransform(self.ik0_ctl, self.getName("tan0_npo"), t)
        self.tan0_ctl = self.addCtl(self.tan0_npo, "tan0_ctl", t, self.color_ik, "sphere", w=self.size*.2)
        att.setKeyableAttributes(self.tan0_ctl, self.t_params)

        t = tra.setMatrixPosition(t, vec.linearlyInterpolate(self.guide.apos[0], self.guide.apos[1], .66))
        self.tan1_npo = pri.addTransform(self.ik1_ctl, self.getName("tan1_npo"), t)
        self.tan1_ctl = self.addCtl(self.tan1_npo, "tan1_ctl", t, self.color_ik, "sphere", w=self.size*.2)
        att.setKeyableAttributes(self.tan1_ctl, self.t_params)

        # Curves -------------------------------------------
        self.mst_crv = cur.addCnsCurve(self.root, self.getName("mst_crv"), [self.ik0_ctl, self.tan0_ctl, self.tan1_ctl, self.ik1_ctl], 3)
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
                fk_ctl = self.addCtl(fk_npo, "fk%s_ctl"%(i-1), tra.getTransform(parentctl), self.color_fk, "cube", w=self.size, h=self.size*.05, d=self.size)
                att.setKeyableAttributes(self.fk_ctl)
                att.setRotOrder(fk_ctl, "XZY")

            # setAttr(fk_npo+".inheritsTransform", False)
            self.scl_npo.append(scl_npo)
            self.fk_npo.append(fk_npo)
            self.fk_ctl.append(fk_ctl)
            parentctl = fk_ctl

            # Deformers (Shadow)
            self.addShadow(fk_ctl, i)

        # Connections (Hooks) ------------------------------
        self.cnx0 = pri.addTransform(self.root, self.getName("0_cnx"))
        self.cnx1 = pri.addTransform(self.root, self.getName("1_cnx"))

    def addAttributes(self):

        # Anim -------------------------------------------
        self.position_att = self.addAnimParam("position", "Position", "double", self.settings["position"], 0, 1)
        self.maxstretch_att = self.addAnimParam("maxstretch", "Max Stretch", "double", self.settings["maxstretch"], 1)
        self.maxsquash_att = self.addAnimParam("maxsquash", "Max Squash", "double", self.settings["maxsquash"], 0, 1)
        self.softness_att = self.addAnimParam("softness", "Softness", "double", self.settings["softness"], 0, 1)

        self.lock_ori0_att = self.addAnimParam("lock_ori0", "Lock Ori 0", "double", self.settings["lock_ori"], 0, 1)
        self.lock_ori1_att = self.addAnimParam("lock_ori1", "Lock Ori 1", "double", self.settings["lock_ori"], 0, 1)

        self.tan0_att = self.addAnimParam("tan0", "Tangent 0", "double", 1, 0)
        self.tan1_att = self.addAnimParam("tan1", "Tangent 1", "double", 1, 0)

        # Volume
        self.volume_att = self.addAnimParam("volume", "Volume", "double", 1, 0, 1)
        
        # Setup ------------------------------------------
        # Eval Fcurve
        self.st_value = fcu.getFCurveValues(self.settings["st_profile"], self.settings["division"])
        self.sq_value = fcu.getFCurveValues(self.settings["sq_profile"], self.settings["division"])
        
        self.st_att = [ self.addSetupParam("stretch_%s"%i, "Stretch %s"%i, "double", self.st_value[i], -1, 0) for i in range(self.settings["division"]) ]
        self.sq_att = [ self.addSetupParam("squash_%s"%i, "Squash %s"%i, "double", self.sq_value[i], 0, 1) for i in range(self.settings["division"]) ]

    def addOperators(self):

        # Tangent position ---------------------------------
        # common part
        d = vec.getDistance(self.guide.apos[0], self.guide.apos[1])
        dist_node = nod.createDistNode(self.ik0_ctl, self.ik1_ctl)
        rootWorld_node = nod.createDecomposeMatrixNode(self.root.attr("worldMatrix"))
        div_node = nod.createDivNode(dist_node+".distance", rootWorld_node+".outputScaleX")
        div_node = nod.createDivNode(div_node+".outputX", d)
        
        # tan0
        mul_node = nod.createMulNode(self.tan0_att, self.tan0_npo.getAttr("ty"))
        res_node = nod.createMulNode(mul_node+".outputX", div_node+".outputX")
        connectAttr( res_node+".outputX", self.tan0_npo.attr("ty"))
        
        # tan1
        mul_node = nod.createMulNode(self.tan1_att, self.tan1_npo.getAttr("ty"))
        res_node = nod.createMulNode(mul_node+".outputX", div_node+".outputX")
        connectAttr( res_node+".outputX", self.tan1_npo.attr("ty"))

        # Curves -------------------------------------------
        op = aop.gear_curveslide2_op(self.slv_crv, self.mst_crv, 0, 1.5, .5, .5)
        
        connectAttr(self.position_att, op+".position")
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
            aop.gear_spinePointAtOp(cns, self.ik0_ctl, self.ik1_ctl, u, "Z")

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
            if i == 0 :
                dm_node = nod.createDecomposeMatrixNode(self.ik0_ctl+".worldMatrix")
                blend_node = nod.createBlendNode([dm_node+".outputRotate%s"%s for s in "XYZ"], [cns+".rotate%s"%s for s in "XYZ"], self.lock_ori0_att)
                self.div_cns[i].attr("rotate").disconnect()
                connectAttr(blend_node+".output", self.div_cns[i]+".rotate")
            elif i == self.settings["division"] - 1 :
                dm_node = nod.createDecomposeMatrixNode(self.ik1_ctl+".worldMatrix")
                blend_node = nod.createBlendNode([dm_node+".outputRotate%s"%s for s in "XYZ"], [cns+".rotate%s"%s for s in "XYZ"], self.lock_ori1_att)
                self.div_cns[i].attr("rotate").disconnect()
                connectAttr(blend_node+".output", self.div_cns[i]+".rotate")

        # Connections (Hooks) ------------------------------
        pointConstraint(self.div_cns[0], self.cnx0)
        orientConstraint(self.div_cns[0], self.cnx0)
        pointConstraint(self.fk_ctl[-1], self.cnx1)
        orientConstraint(self.fk_ctl[-1], self.cnx1)
        
    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Set the relation beetween object from guide to rig.\n
    # @param self
    def setRelation(self):
        self.relatives["root"] = self.cnx0
        self.relatives["eff"] = self.cnx1
