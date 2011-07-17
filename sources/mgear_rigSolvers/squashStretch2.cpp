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
MTypeId gear_squashStretch2::id( 0x27003 );

// Define the Node's attribute specifiers

MObject gear_squashStretch2::global_scale;
MObject gear_squashStretch2::global_scalex;
MObject gear_squashStretch2::global_scaley;
MObject gear_squashStretch2::global_scalez;

MObject gear_squashStretch2::blend;
MObject gear_squashStretch2::driver;
MObject gear_squashStretch2::driver_min;
MObject gear_squashStretch2::driver_ctr;
MObject gear_squashStretch2::driver_max;

MObject gear_squashStretch2::axis;
MObject gear_squashStretch2::squash;
MObject gear_squashStretch2::stretch;

MObject gear_squashStretch2::output;

gear_squashStretch2::gear_squashStretch2() {} // constructor
gear_squashStretch2::~gear_squashStretch2() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_squashStretch2::creator()
{
   return new gear_squashStretch2();
}

// INIT =========================================
MStatus gear_squashStretch2::initialize()
{
	MFnNumericAttribute nAttr;
	MFnEnumAttribute eAttr;
	MStatus stat;

    // Inputs 
    global_scale = nAttr.createPoint("global_scale", "gs" );
    global_scalex = nAttr.child(0);
    global_scaley = nAttr.child(1);
    global_scalez = nAttr.child(2);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setReadable(true);
    nAttr.setKeyable(false);
    stat = addAttribute( global_scale );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	// Sliders
	blend = nAttr.create("blend", "b", MFnNumericData::kFloat, 1);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
    stat = addAttribute( blend );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	driver = nAttr.create("driver", "d", MFnNumericData::kFloat, 3);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( driver );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	driver_min = nAttr.create("driver_min", "dmin", MFnNumericData::kFloat, 1);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( driver_min );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	driver_ctr = nAttr.create("driver_ctr", "dctr", MFnNumericData::kFloat, 3);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( driver_ctr );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	driver_max = nAttr.create("driver_max", "dmax", MFnNumericData::kFloat, 6);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( driver_max );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    axis = eAttr.create( "axis", "a", 0 );
    eAttr.addField("x", 0);
    eAttr.addField("y", 1);
    eAttr.addField("z", 2);
    eAttr.setWritable(true);
    eAttr.setStorable(true);
    eAttr.setReadable(true);
    eAttr.setKeyable(false);
    addAttribute( axis );
	
	squash = nAttr.create("squash", "sq", MFnNumericData::kFloat, .5);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(-1);
    stat = addAttribute( squash );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	stretch = nAttr.create("stretch", "st", MFnNumericData::kFloat, -.5);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(-1);
    stat = addAttribute( stretch );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	// Outputs
	output = nAttr.createPoint("output", "out" );
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setReadable(true);
    addAttribute( output );

	// Connections
    stat = attributeAffects ( global_scale, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( blend, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( driver, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( driver_min, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( driver_ctr, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( driver_max, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( axis, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( squash, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( stretch, output );
		if (!stat) {stat.perror("attributeAffects"); return stat;}


   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_squashStretch2::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;
	// Error check
    if (plug != output)
        return MS::kUnknownParameter;

	// Inputs 
    MVector gscale = data.inputValue( global_scale ).asFloatVector();
	double sx = gscale.x;
	double sy = gscale.y;
	double sz = gscale.z;

	// Sliders
	double in_blend = (double)data.inputValue( blend ).asFloat();
	double in_driver = (double)data.inputValue( driver ).asFloat();
	double in_dmin = (double)data.inputValue( driver_min ).asFloat();
	double in_dctr = (double)data.inputValue( driver_ctr ).asFloat();
	double in_dmax = (double)data.inputValue( driver_max ).asFloat();
	int in_axis = data.inputValue( axis ).asShort();
	double in_sq = (double)data.inputValue( squash ).asFloat();
	double in_st = (double)data.inputValue( stretch ).asFloat();
	
	// Process
    in_st *= clamp(max(in_driver - in_dctr, 0.0) / max(in_dmax - in_dctr, 0.0001), 0.0, 1.0);
    in_sq *= clamp(max(in_dctr - in_driver, 0.0) / max(in_dctr - in_dmin, 0.0001), 0.0, 1.0);

    if (in_axis != 0)
        sx *= max( 0.0, 1.0 + in_sq + in_st );

    if (in_axis != 1)
        sy *= max( 0.0, 1.0 + in_sq + in_st );

    if (in_axis != 2)
        sz *= max( 0.0, 1.0 + in_sq + in_st );
	
    MVector scl = MVector(sx, sy, sz);
    scl = linearInterpolate(gscale, scl, in_blend);
	
	// Output
    MDataHandle h = data.outputValue( output );
	h.set3Float( (float)scl.x, (float)scl.y, (float)scl.z );
    data.setClean( plug );

	return MS::kSuccess;
}

