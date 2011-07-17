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

## @package mgear.maya.rig.component
# @author Jeremie Passerin
#

#############################################
# GLOBAL
#############################################
# pymel
from pymel.core.general import *
from pymel.core.animation import *
from pymel.util import *
import pymel.core.datatypes as dt


# mgear
import mgear
import mgear.maya.primitive as pri
import mgear.maya.vector as vec
import mgear.maya.transform as tra
import mgear.maya.attribute as att
import mgear.maya.applyop as aop
import mgear.maya.node as nod
import mgear.maya.icon as ico

#############################################
# COMPONENT
#############################################
class MainComponent(object):

    steps = ["Objects", "Properties", "Operators", "Connect", "Finalize"]

    local_params = ("tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz")
    t_params = ("tx", "ty", "tz")
    r_params = ("rx", "ry", "rz", "ro")
    s_params = ("sx", "sy", "sz")
    tr_params = ("tx", "ty", "tz", "rx", "ry", "rz", "ro")
    rs_params = ("rx", "ry", "rz", "ro", "sx", "sy", "sz")
    x_axis = dt.Vector(1,0,0)
    y_axis = dt.Vector(0,1,0)
    z_axis = dt.Vector(0,0,1)

    # =====================================================
    ## Init Method.
    # @param self
    # @param rig Rig - The parent Rig of this component.
    # @param guide ComponentGuide - The guide for this component.
    def __init__(self, rig, guide):

        # --------------------------------------------------
        # Main Objects
        self.rig = rig
        self.guide = guide

        self.options = self.rig.options
        self.model = self.rig.model
        self.settings = self.guide.values

        self.name = self.settings["comp_name"]
        self.side = self.settings["comp_side"]
        self.index = self.settings["comp_index"]

        # --------------------------------------------------
        # Shortcut to useful settings
        self.size = self.guide.size

        self.color_fk = self.options[self.side + "_color_fk"]
        self.color_ik = self.options[self.side + "_color_ik"]

        self.negate = self.side == "R"
        if self.negate:
            self.n_sign = "-"
            self.n_factor = -1
        else:
            self.n_sign = ""
            self.n_factor = 1

        # --------------------------------------------------
        # Builder init
        self.groups = {} ## Dictionary of groups
        self.controlers = [] ## List of all the controlers of the component

        # --------------------------------------------------
        # Connector init
        self.connections = {}
        self.connections["standard"]  = self.connect_standard

        self.relatives = {}

        # --------------------------------------------------
        # Step
        self.stepMethods = [eval("self.step_0%s"%i) for i in range(len(self.steps))]

    # =====================================================
    # BUILDING STEP
    # =====================================================
    ## Step 00. Initial Hierarchy, create objects and set the connection relation.
    # @param self
    def step_00(self):
        self.initialHierarchy()
        self.addObjects()
        self.setRelation()
        return

    ## Step 01. Get the properties host, create parameters and set layout and logic.
    # @param self
    def step_01(self):
        self.getHost()
        self.addFullNameParam()
        self.addAttributes()
        return

    ## Step 02. Apply all the operators.
    # @param self
    def step_02(self):
        self.addOperators()
        return

    ## Step 03. Connect the component to the rest of the rig.
    # @param self
    def step_03(self):
        self.initConnector()
        self.addConnection()
        self.connect()
        self.postConnect()
        return

    ## Step 04. Finalize the component.
    # @param self
    def step_04(self):
        self.finalize()
        return

    ## NOT YET AVAILABLE
    def step_05(self):
        self.addPostSkin()
        return

    # =========================================
    # Creation methods
    def initialHierarchy(self):

        # Root
        self.root = pri.addTransformFromPos(self.model, self.getName("root"), self.guide.pos["root"])

        # Shd --------------------------------
        if self.options["shadow_rig"]:
            self.shd_org = pri.addTransform(self.rig.shd_org, self.getName("shd_org"))

        return

    def addObjects(self):
        return

    def addShadow(self, obj, name):

        if self.options["shadow_rig"]:
            shd = pri.addJoint(self.shd_org, self.getName(str(name)+"_shd"), tra.getTransform(obj))
            shd.setAttr("jointOrient", 0, 0, 0)
            # parentConstraint(obj, shd, maintainOffset=False)
            # scaleConstraint(obj, shd, maintainOffset=False)
            mulmat_node = aop.gear_mulmatrix_op(obj+".worldMatrix", shd+".parentInverseMatrix")
            dm_node = nod.createDecomposeMatrixNode(mulmat_node+".output")
            connectAttr(dm_node+".outputTranslate", shd+".t")
            connectAttr(dm_node+".outputRotate", shd+".r")
            connectAttr(dm_node+".outputScale", shd+".s")
            self.shd_org = shd
        else:
            shd = pri.addJoint(obj, self.getName(str(name)+"_shd"), tra.getTransform(obj))
            shd.setAttr("jointOrient", 0, 0, 0)
            shd.setAttr("rotate", 0, 0, 0)
            connectAttr(self.rig.shdVis_att, shd.attr("visibility"))

        self.addToGroup(shd, "deformers")
        return shd

    def getNormalFromPos(self, pos):
        if len(pos) < 3:
            mgear.log("%s : Not enough references to define normal"%self.fullName, mgear.sev_error)

        return vec.getPlaneNormal(pos[0], pos[1], pos[2])


    def getBiNormalFromPos(self, pos):
        if len(pos) < 3:
            mgear.log("%s : Not enough references to define binormal"%self.fullName, mgear.sev_error)

        return vec.getPlaneBiNormal(pos[0], pos[1], pos[2])

    # =====================================================
    def addCtl(self, parent, name, m, color, icon, **kwargs):

    
        fullName = self.getName(name)
        if fullName in self.rig.guide.controlers.keys():
            ctl_ref = self.rig.guide.controlers[fullName]
            ctl = pri.addTransform(parent, fullName, m)
            for shape in ctl_ref.getShapes():
                ctl.addChild(shape, shape=True, add=True)
            ico.setcolor(ctl, color)
        else:
            ctl = ico.create(parent, fullName, m, color, icon, **kwargs)
            
        self.addToGroup(ctl, "controlers")
        return ctl
        
    def addToGroup(self, objects, names=["hidden"]):

        if not isinstance(names, list):
            names = [names]

        if not isinstance(objects, list):
            objects = [objects]

        for name in names:
            if name not in self.groups.keys():
                self.groups[name] = []

            self.groups[name].extend(objects)
        
    # =====================================================
    # PROPERTY
    # =====================================================
    ## Get the host for the properties.
    # @param self
    def getHost(self):
    
        self.uihost = self.rig.findChild(self.settings["ui_host"])

    def addAttributes(self):
        return

    ## Add a parameter to the animation property.\n
    # Note that animatable and keyable are True per default.
    # @param self
    def addFullNameParam(self):
    
        attr = self.addAnimEnumParam("", "", 0, ["---------------"] )
        
        return attr
        
    ## Add a parameter to the animation property.\n
    # Note that animatable and keyable are True per default.
    # @param self
    def addAnimParam(self, longName, niceName, attType, value, minValue=None, maxValue=None, keyable=True, readable=True, storable=True, writable=True):

        attr = att.addAttribute(self.uihost, self.getName(longName), attType, value, niceName, None, minValue=minValue, maxValue=maxValue, keyable=keyable, readable=readable, storable=storable, writable=writable)

        return attr

    ## Add a parameter to the animation property.\n
    # Note that animatable and keyable are True per default.
    # @param self
    def addAnimEnumParam(self, longName, niceName, value, enum=[], keyable=True, readable=True, storable=True, writable=True):

        attr = att.addEnumAttribute(self.uihost, self.getName(longName), value, enum, niceName, None, keyable=keyable, readable=readable, storable=storable, writable=writable)

        return attr


    ## Add a parameter to the setup property.\n
    # Note that animatable and keyable are false per default.
    # @param self
    def addSetupParam(self, longName, niceName, attType, value, minValue=None, maxValue=None, keyable=True, readable=True, storable=True, writable=True):

        attr = att.addAttribute(self.root, self.getName(longName), attType, value, niceName, None, minValue=minValue, maxValue=maxValue, keyable=keyable, readable=readable, storable=storable, writable=writable)

        return attr

    # =====================================================
    # OPERATORS
    # =====================================================
    def addOperators(self):
        return

    # =====================================================
    # CONNECTOR
    # =====================================================
    ## Add more connection definition to the set.\n
    # REIMPLEMENT. This method should be reimplemented in each component.\n
    # Only if you need to use an new connection (not the standard).
    # @param self
    def addConnection(self):
        return

    ## Set the relation beetween object from guide to rig.\n
    # REIMPLEMENT. This method should be reimplemented in each component.
    # @param self
    def setRelation(self):
        for name in self.guide.objectNames:
            self.relatives[name] = self.root

    ## Return the relational object from guide to rig.
    # @param self
    # @param local name of the guide object.
    def getRelation(self, name):
        if name not in self.relatives.keys():
            mgear.log("Can't find reference for object : " + self.fullName + "." + name, mgear.sev_error)
            return False

        return self.relatives[name]

    def initConnector(self):

        parent_name = "none"
        if self.guide.parentComponent is not None:
            parent_name = self.guide.parentComponent.getName(self.guide.parentLocalName)

        self.parent = self.rig.findChild(parent_name)
        self.parent_comp = self.rig.findComponent(parent_name)

    ## Connect the component to the rest of the rig using the defined connection.
    # @param
    def connect(self):

        if self.settings["connector"] not in self.connections.keys():
            gear.log("Unable to connect object", gear.sev_error)
            return False

        self.connections[self.settings["connector"]]()

        return True

    ## standard connection definition. This is a simple parenting of the root.
    # @param self
    def connect_standard(self):
        self.parent.addChild(self.root)

    ## standard connection definition with ik and upv references.
    # @param self
    def connect_standardWithIkRef(self):

        self.parent.addChild(self.root)
        
        # Set the Ik Reference
        self.connectRef(self.settings["ikrefarray"], self.ik_cns)
        self.connectRef(self.settings["upvrefarray"], self.upv_cns)
        
        '''
        if self.settings["ikrefarray"]:
            ref_names = self.settings["ikrefarray"].split(",")
            if len(ref_names) == 1:
                ref = self.rig.findChild(ref_names[0])
                parent(self.ik_cns, ref)
            else:
                ref = []
                for ref_name in ref_names:
                    ref.append(self.rig.findChild(ref_name))
                
                ref.append(self.ik_cns)
                cns_node = parentConstraint(*ref, maintainOffset=True)
                cns_attr = parentConstraint(cns_node, query=True, weightAliasList=True)
                
                for i, attr in enumerate(cns_attr):
                    node_name = createNode("condition")
                    connectAttr(self.ikref_att, node_name+".firstTerm")
                    setAttr(node_name+".secondTerm", i)
                    setAttr(node_name+".operation", 0)
                    setAttr(node_name+".colorIfTrueR", 1)
                    setAttr(node_name+".colorIfFalseR", 0)
                    connectAttr(node_name+".outColorR", attr)
                
        # Set the Upv Reference
        if self.settings["upvrefarray"]:
            ref_names = self.settings["upvrefarray"].split(",")
            if len(ref_names) == 1:
                ref = self.rig.findChild(ref_names[0])
                parent(self.upv_cns, ref)
            else:
                ref = []
                for ref_name in ref_names:
                    ref.append(self.rig.findChild(ref_name))
                
                ref.append(self.upv_cns)
                cns_node = parentConstraint(*ref, maintainOffset=True)
                cns_attr = parentConstraint(cns_node, query=True, weightAliasList=True)
                
                for i, attr in enumerate(cns_attr):
                    node_name = createNode("condition")
                    connectAttr(self.ikref_att, node_name+".firstTerm")
                    setAttr(node_name+".secondTerm", i)
                    setAttr(node_name+".operation", 0)
                    setAttr(node_name+".colorIfTrueR", 1)
                    setAttr(node_name+".colorIfFalseR", 0)
                    connectAttr(node_name+".outColorR", attr)
        '''

    def connectRef(self, refArray, cns_obj):
        if refArray:
            ref_names = refArray.split(",")
            if len(ref_names) == 1:
                ref = self.rig.findChild(ref_names[0])
                parent(cns_obj, ref)
            else:
                ref = []
                for ref_name in ref_names:
                    ref.append(self.rig.findChild(ref_name))
                
                ref.append(cns_obj)
                cns_node = parentConstraint(*ref, maintainOffset=True)
                cns_attr = parentConstraint(cns_node, query=True, weightAliasList=True)
                
                for i, attr in enumerate(cns_attr):
                    node_name = createNode("condition")
                    connectAttr(self.ikref_att, node_name+".firstTerm")
                    setAttr(node_name+".secondTerm", i)
                    setAttr(node_name+".operation", 0)
                    setAttr(node_name+".colorIfTrueR", 1)
                    setAttr(node_name+".colorIfFalseR", 0)
                    connectAttr(node_name+".outColorR", attr)
    
    ## Post connection actions.
    # REIMPLEMENT. This method should be reimplemented in each component.\n
    # @param self
    def postConnect(self):
        return

    # =====================================================
    # FINALIZE
    # =====================================================
    def finalize(self):
        return

    # =====================================================
    # MISC
    # =====================================================
    ## Return the name for component element
    # @param self
    # @param name String - Name.
    def getName(self, name="", side=None):

        if side is None:
            side = self.side

        name = str(name)

        if name:
            return self.name + "_" + side + str(self.index) + "_" + name
        else:
            return self.fullName

    # =====================================================
    # PROPERTIES
    # =====================================================
    ## return the fullname of the component
    # @param self
    def getFullName(self):
        return self.guide.fullName

    ## return the type of the component
    # @param self
    def getType(self):
        return self.guide.type

    fullName = property(getFullName)
    type = property(getType)