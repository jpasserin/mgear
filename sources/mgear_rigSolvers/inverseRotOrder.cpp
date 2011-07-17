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
MTypeId gear_inverseRotOrder::id( 0x27005 );

// Define the Node's attribute specifiers

MObject gear_inverseRotOrder::rotOrder; 
MObject gear_inverseRotOrder::output; 

gear_inverseRotOrder::gear_inverseRotOrder() {} // constructor
gear_inverseRotOrder::~gear_inverseRotOrder() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_inverseRotOrder::creator()
{
   return new gear_inverseRotOrder();
}

// INIT =========================================
MStatus gear_inverseRotOrder::initialize()
{
   MFnNumericAttribute nAttr;
   MFnEnumAttribute eAttr;
   MStatus stat;
   
    // Inputs
    rotOrder = eAttr.create( "rotOrder", "ro", 0 );
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    eAttr.setWritable(true);
    eAttr.setStorable(true);
    eAttr.setReadable(true);
    eAttr.setKeyable(true);
	stat = addAttribute( rotOrder );
		if (!stat) {stat.perror("addAttribute"); return stat;}
    
    // Outputs
	output = nAttr.create( "output", "out", MFnNumericData::kShort, 0 );
	nAttr.setWritable(false);
	nAttr.setStorable(true);
    nAttr.setReadable(true);
	nAttr.setKeyable(false);
	stat = addAttribute( output );
		if (!stat) {stat.perror("addAttribute"); return stat;}

    // Connections
	stat = attributeAffects( rotOrder, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_inverseRotOrder::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;

	if( plug != output )
		return MS::kUnknownParameter;

	// Input
	int ro  = data.inputValue( rotOrder ).asShort();
	int inv_ro [6] = {5, 3, 4, 1, 2, 0};

	// Output
	MDataHandle h_output = data.outputValue( output );
	h_output.setShort(inv_ro[ro]);
	data.setClean(plug);

	return MS::kSuccess;
}

