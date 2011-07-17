/*

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

*/
/////////////////////////////////////////////////
// INCLUDE
/////////////////////////////////////////////////
#include "gear_solvers.h"

/////////////////////////////////////////////////
// GLOBAL
/////////////////////////////////////////////////
MTypeId gear_spinePointAt::id( 0x27008 );

// Define the Node's attribute specifiers

MObject gear_spinePointAt::rotA;
MObject gear_spinePointAt::rotAx;
MObject gear_spinePointAt::rotAy;
MObject gear_spinePointAt::rotAz;
MObject gear_spinePointAt::rotB;
MObject gear_spinePointAt::rotBx;
MObject gear_spinePointAt::rotBy;
MObject gear_spinePointAt::rotBz;
MObject gear_spinePointAt::axe;
MObject gear_spinePointAt::blend;
MObject gear_spinePointAt::pointAt;

gear_spinePointAt::gear_spinePointAt() {} // constructor
gear_spinePointAt::~gear_spinePointAt() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_spinePointAt::creator()
{
   return new gear_spinePointAt();
}

// INIT =========================================
MStatus gear_spinePointAt::initialize()
{
   MFnNumericAttribute nAttr;
   MFnEnumAttribute eAttr;
   MStatus stat;
   
    // Inputs 
    rotA = nAttr.createPoint("rotA", "ra" );
    rotAx = nAttr.child(0);
    rotAy = nAttr.child(1);
    rotAz = nAttr.child(2);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setReadable(true);
    nAttr.setKeyable(false);
    stat = addAttribute( rotA );
		if (!stat) {stat.perror("addAttribute"); return stat;}
    
    rotB = nAttr.createPoint("rotB", "rb" );
    rotBx = nAttr.child(0);
    rotBy = nAttr.child(1);
    rotBz = nAttr.child(2);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setReadable(true);
    nAttr.setKeyable(false);
    stat = addAttribute( rotB );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
    axe = eAttr.create( "axe", "a", 2 );
    eAttr.addField("X", 0);
    eAttr.addField("Y", 1);
    eAttr.addField("Z", 2);
    eAttr.addField("-X", 3);
    eAttr.addField("-Y", 4);
    eAttr.addField("-Z", 5);
    eAttr.setWritable(true);
    eAttr.setStorable(true);
    eAttr.setReadable(true);
    eAttr.setKeyable(false);
    stat = addAttribute( axe );
		if (!stat) {stat.perror("addAttribute"); return stat;}
    
    blend = nAttr.create( "blend", "b", MFnNumericData::kFloat, 0.5 );
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setReadable(true);
    nAttr.setKeyable(true);
    nAttr.setMin(0);
    nAttr.setMax(1);
    stat = addAttribute( blend );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    // Outputs
	pointAt = nAttr.createPoint("pointAt", "pa" );
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setReadable(true);
    stat = addAttribute( pointAt );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
    // Connections
    stat = attributeAffects ( rotA, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotAx, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotAy, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotAz, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotB, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotBx, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotBy, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( rotBz, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( axe, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( blend, pointAt );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_spinePointAt::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;

	if( plug != pointAt )
		return MS::kUnknownParameter;
	
	MString sx, sy, sz, sw;

    // Get inputs
	MDataHandle h;
	MVector v;
    h = data.inputValue( rotA );
	v = h.asFloatVector();
    double rAx = v.x;
    double rAy = v.y;
    double rAz = v.z;

    h = data.inputValue( rotB );
	v = h.asFloatVector();
    double rBx = v.x;
    double rBy = v.y;
    double rBz = v.z;
        
	h = data.inputValue( axe );
    int axe = h.asShort();
        
	h = data.inputValue( blend );
    double in_blend = (double)h.asFloat();
	
    // Process
    // There is no such thing as siTransformation in Maya, 
    // so what we really need to compute this +/-360 roll is the global rotation of the object
    // We then need to convert this eulerRotation to Quaternion
    // Maybe it would be faster to use the MEulerRotation class, but anyway, this code can do it
    MQuaternion qA = e2q(rAx, rAy, rAz);
    MQuaternion qB = e2q(rBx, rBy, rBz);
	
    MQuaternion qC = slerp2(qA, qB, in_blend);

	MVector vOut;
	switch ( axe )
	{
		case 0:
			vOut = MVector(1,0,0);
			break;
		case 1:
			vOut = MVector(0,1,0);
			break;
		case 2:
			vOut = MVector(0,0,1);
			break;
		case 3:
			vOut = MVector(-1,0,0);
			break;
		case 4:
			vOut = MVector(0,-1,0);
			break;
		case 5:
			vOut = MVector(0,0,-1);
			break;
	}
	
    vOut = vOut.rotateBy(qC);
    float x = (float)vOut.x;
    float y = (float)vOut.y;
    float z = (float)vOut.z;

    // Output
    h = data.outputValue( pointAt );
	h.set3Float( x, y, z );

	// This doesn't work
    // h.setMVector( vOut );
    // h.set3Double( vOut );

    data.setClean( plug );

	return MS::kSuccess;
}

