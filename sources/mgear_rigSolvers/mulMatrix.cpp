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
MTypeId gear_mulMatrix::id( 0x27006 );

// Define the Node's attribute specifiers

MObject gear_mulMatrix::matrixA; 
MObject gear_mulMatrix::matrixB; 
MObject gear_mulMatrix::output; 

gear_mulMatrix::gear_mulMatrix() {} // constructor
gear_mulMatrix::~gear_mulMatrix() {} // destructor

/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_mulMatrix::creator()
{
   return new gear_mulMatrix();
}

// INIT =========================================
MStatus gear_mulMatrix::initialize()
{
  MFnMatrixAttribute mAttr;
	MStatus stat;

	// INPUTS
	matrixA = mAttr.create( "matrixA", "mA" );
	mAttr.setStorable(true);
	mAttr.setKeyable(true);
	mAttr.setConnectable(true);
	stat = addAttribute( matrixA );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	matrixB = mAttr.create( "matrixB", "mB" );
	mAttr.setStorable(true);
	mAttr.setKeyable(true);
	mAttr.setConnectable(true);
	stat = addAttribute( matrixB );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	// OUTPUTS
	output = mAttr.create( "output", "out" );
	mAttr.setStorable(false);
	mAttr.setKeyable(false);
	mAttr.setConnectable(true);
	stat = addAttribute( output );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	// CONNECTIONS
	stat = attributeAffects( matrixA, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( matrixB, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

   return MS::kSuccess;
}
// COMPUTE ======================================
MStatus gear_mulMatrix::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus returnStatus;

	if( plug != output )
		return MS::kUnknownParameter;

	// Input
	MMatrix mA = data.inputValue( matrixA ).asMatrix();
	MMatrix mB = data.inputValue( matrixB ).asMatrix();

	MMatrix mC = mA * mB;
	double i = mC.matrix[0][0];


	// Output
	MDataHandle h;
	h = data.outputValue( output );
	h.setMMatrix( mC );
	data.setClean(plug);

	return MS::kSuccess;
}

