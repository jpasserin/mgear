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
MTypeId gear_curveCns::id( 0x27000 );
MObject gear_curveCns::inputs; 
 
/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_curveCns::creator() { return new gear_curveCns; }
 
// INIT =========================================
MStatus gear_curveCns::initialize()
{
	MFnMatrixAttribute mAttr;
	MStatus stat;

	// INPUTS
	inputs = mAttr.create( "inputs", "inputs" );
	mAttr.setStorable(true);
    mAttr.setReadable(false);
    mAttr.setIndexMatters(false);
    mAttr.setArray(true);
	stat = addAttribute( inputs );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	// CONNECTIONS
	stat = attributeAffects( inputs, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

    return MS::kSuccess;
}

// COMPUTE ======================================
MStatus gear_curveCns::deform( MDataBlock& data, MItGeometry& iter, const MMatrix &mat, unsigned int mIndex )
{
    MStatus returnStatus;

	MArrayDataHandle adh = data.inputArrayValue( inputs );
	int deformer_count = adh.elementCount( &returnStatus );

	// Process
	while (! iter.isDone()){
		if (iter.index() < deformer_count){
			adh.jumpToElement(iter.index());
			MTransformationMatrix m(adh.inputValue().asMatrix() * mat.inverse());
			MVector v = m.getTranslation(MSpace::kWorld, &returnStatus );
			MPoint pt(v);
			iter.setPosition(pt);
		}
		iter.next();
	}
 
    return MS::kSuccess;
}
 
 