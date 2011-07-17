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
MTypeId gear_uToPercentage::id( 0x27009 );

// Define the Node's attribute specifiers

MObject gear_uToPercentage::curve;
MObject gear_uToPercentage::normalizedU;
MObject gear_uToPercentage::u;
MObject gear_uToPercentage::steps;
MObject gear_uToPercentage::percentage;

gear_uToPercentage::gear_uToPercentage() {} // constructor
gear_uToPercentage::~gear_uToPercentage() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_uToPercentage::creator()
{
   return new gear_uToPercentage();
}

// INIT =========================================
MStatus gear_uToPercentage::initialize()
{
	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;
	MStatus stat;
	
    // Curve
    curve = tAttr.create("curve", "crv", MFnData::kNurbsCurve);
    stat = addAttribute( curve );
		if (!stat) {stat.perror("addAttribute"); return stat;}

		
   // Sliders
    normalizedU = nAttr.create("normalizedU", "n", MFnNumericData::kBoolean, false);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( normalizedU );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    u = nAttr.create("u", "u", MFnNumericData::kFloat, .5, 0);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( u );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    steps = nAttr.create("steps", "s", MFnNumericData::kShort, 40);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( steps );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    // Outputs
	percentage = nAttr.create( "percentage", "p", MFnNumericData::kFloat, 0 );
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setReadable(true);
    nAttr.setKeyable(false);
    stat = addAttribute( percentage );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
    // Connections 
    stat = attributeAffects ( curve, percentage );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( steps, percentage );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( u, percentage );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( normalizedU, percentage );
		if (!stat) {stat.perror("attributeAffects"); return stat;}

   

   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_uToPercentage::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;
	// Error check
    if (plug != percentage)
        return MS::kUnknownParameter;

	// Curve
	MFnNurbsCurve crv = data.inputValue( curve ).asNurbsCurve();

	// Sliders
	bool in_normU = data.inputValue( normalizedU ).asBool();
	double in_u = (double)data.inputValue( u ).asFloat();
	unsigned in_steps = data.inputValue( steps ).asShort();

	// Process
	if (in_normU)
		in_u = normalizedUToU(in_u, crv.numCVs());

	// Get length
	MVectorArray u_subpos(in_steps);
	MVectorArray t_subpos(in_steps);
	MPoint pt;
	double step;
	for (unsigned i = 0; i < in_steps ; i++){

		step = i * in_u / (in_steps - 1.0);
		crv.getPointAtParam(step, pt, MSpace::kWorld);
		u_subpos[i] = MVector(pt);

        step = i/(in_steps - 1.0);
		crv.getPointAtParam(step, pt, MSpace::kWorld);
		t_subpos[i] = MVector(pt);

	}
	
	double u_length = 0;
	double t_length = 0;
	MVector v;
	for (unsigned i = 0; i < in_steps ; i++){
		if (i>0){
			v = u_subpos[i] - u_subpos[i-1];
			u_length += v.length();
			v = t_subpos[i] - t_subpos[i-1];
			t_length += v.length();
		}
	}

	double out_perc = (u_length / t_length) * 100;
		
	// Output
    MDataHandle h = data.outputValue( percentage );
    h.setDouble( out_perc );
    data.setClean( plug );

	return MS::kSuccess;
}

