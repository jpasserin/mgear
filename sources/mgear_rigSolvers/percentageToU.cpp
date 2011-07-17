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
MTypeId gear_percentageToU::id( 0x27007 );

// Define the Node's attribute specifiers

MObject gear_percentageToU::curve;
MObject gear_percentageToU::normalizedU;
MObject gear_percentageToU::percentage;
MObject gear_percentageToU::steps;
MObject gear_percentageToU::u;

gear_percentageToU::gear_percentageToU() {} // constructor
gear_percentageToU::~gear_percentageToU() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_percentageToU::creator()
{
   return new gear_percentageToU();
}

// INIT =========================================
MStatus gear_percentageToU::initialize()
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
		
	percentage = nAttr.create( "percentage", "p", MFnNumericData::kFloat, 0 );
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( percentage );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    steps = nAttr.create("steps", "s", MFnNumericData::kShort, 40);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( steps );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    // Outputs
    u = nAttr.create("u", "u", MFnNumericData::kFloat, .5, 0);
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setReadable(true);
    nAttr.setKeyable(false);
    stat = addAttribute( u );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    // Connections 
    stat = attributeAffects ( curve, u );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( steps, u );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( percentage, u );
		if (!stat) {stat.perror("attributeAffects"); return stat;}
    stat = attributeAffects ( normalizedU, u );
		if (!stat) {stat.perror("attributeAffects"); return stat;}


   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_percentageToU::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;
	// Error check
    if (plug != percentage)
        return MS::kUnknownParameter;
	
	// Curve
	MFnNurbsCurve crv = data.inputValue( curve ).asNurbsCurve();

	// Sliders
	bool in_normU = data.inputValue( normalizedU ).asBool();
	double in_percentage = (double)data.inputValue( percentage ).asFloat() * .01;
	const unsigned in_steps = data.inputValue( steps ).asShort();

	// Process
	// Get length
	MVectorArray u_subpos(in_steps);
	MPoint pt;
	MDoubleArray u_list(in_steps);
	for(unsigned i = 0 ; i < in_steps ; i++ ){
		u_list[i] = normalizedUToU(i /(in_steps - 1.0), crv.numCVs());

		crv.getPointAtParam(u_list[i], pt, MSpace::kWorld);
		u_subpos[i] = MVector(pt);
	}
	
	
	double t_length = 0;
	MDoubleArray dist(in_steps);
	MVector v;
	for (unsigned i = 0; i < in_steps ; i++){
		if (i>0){
			v = u_subpos[i] - u_subpos[i-1];
			t_length += v.length();
			dist[i] = t_length;
		}
	}

	MDoubleArray u_perc(in_steps);
	for (unsigned i = 0; i < in_steps ; i++){
		u_perc[i] = dist[i] / t_length;
	}

	
    // Get closest indices
    unsigned index = findClosestInArray(in_percentage, u_perc);
	unsigned indexA, indexB;
    if (in_percentage <= u_perc[index]){
        indexA = abs(int(index));
        indexB = index;
		if ( indexA > indexB){
			indexA = indexB;
			indexB = indexA+1;
		}
	}
    else {
        indexA = index;
        indexB = index + 1;
	}
	
    // blend value
    double blend = set01range(in_percentage, u_perc[indexA], u_perc[indexB]);
            
    double out_u = linearInterpolate(u_list[indexA], u_list[indexB], blend);
        
    if (in_normU)
        out_u = uToNormalizedU(out_u, crv.numCVs());
	
	// Ouput
	MDataHandle h = data.outputValue( u );
    h.setDouble( out_u );
    data.setClean( plug );

	return MS::kSuccess;
}

