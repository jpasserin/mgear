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
MTypeId gear_slideCurve2::id( 0x27002 );

MObject gear_slideCurve2::master_crv; 
MObject gear_slideCurve2::master_mat;

MObject gear_slideCurve2::slave_length; 
MObject gear_slideCurve2::master_length; 
MObject gear_slideCurve2::position; 
MObject gear_slideCurve2::maxstretch; 
MObject gear_slideCurve2::maxsquash; 
MObject gear_slideCurve2::softness; 
 
/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
// CREATOR ======================================
void* gear_slideCurve2::creator() { return new gear_slideCurve2; }
 
// INIT =========================================
MStatus gear_slideCurve2::initialize()
{
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MStatus stat;

	// INPUTS MESH
	
    master_crv = tAttr.create("master_crv", "mcrv", MFnData::kNurbsCurve);
    stat = addAttribute( master_crv );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	master_mat = mAttr.create( "master_mat", "mmat" );
	mAttr.setStorable(true);
    mAttr.setReadable(false);
	stat = addAttribute( master_mat );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	// SLIDERS
	slave_length = nAttr.create("slave_length", "sl", MFnNumericData::kFloat, 1);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( slave_length );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	master_length = nAttr.create("master_length", "ml", MFnNumericData::kFloat, 1);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
    stat = addAttribute( master_length );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	position = nAttr.create("position", "p", MFnNumericData::kFloat, 0.0);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
	nAttr.setMax(1);
    stat = addAttribute( position );
		if (!stat) {stat.perror("addAttribute"); return stat;}

	maxstretch = nAttr.create("maxstretch", "mst", MFnNumericData::kFloat, 1.5);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(1);
    stat = addAttribute( maxstretch );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	maxsquash = nAttr.create("maxsquash", "msq", MFnNumericData::kFloat, .5);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
	nAttr.setMax(1);
    stat = addAttribute( maxsquash );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	softness = nAttr.create("softness", "s", MFnNumericData::kFloat, 0.5);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
	nAttr.setMax(1);
    stat = addAttribute( softness );
		if (!stat) {stat.perror("addAttribute"); return stat;}
		
	// CONNECTIONS
	stat = attributeAffects( master_crv, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( master_mat, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	stat = attributeAffects( master_length, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( slave_length, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( position, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( maxstretch, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( maxsquash, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( softness, outputGeom );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

    return MS::kSuccess;
}

// COMPUTE ======================================
MStatus gear_slideCurve2::deform( MDataBlock& data, MItGeometry& iter, const MMatrix &mat, unsigned int mIndex )
{
    MStatus returnStatus;
	
    // Inputs ---------------------------------------------------------
    // Input NurbsCurve
	// Curve
	MFnNurbsCurve crv = data.inputValue( master_crv ).asNurbsCurve();
    MMatrix m = data.inputValue(master_mat).asMatrix();
        
    // Input Sliders
    double in_sl = (double)data.inputValue(slave_length).asFloat();
    double in_ml = (double)data.inputValue(master_length).asFloat();
    double in_position = (double)data.inputValue(position).asFloat();
    double in_maxstretch = (double)data.inputValue(maxstretch).asFloat();
	double in_maxsquash = (double)data.inputValue(maxsquash).asFloat();
    double in_softness = (double)data.inputValue(softness).asFloat();
	
    // Init -----------------------------------------------------------
    double mstCrvLength = crv.length();

    int slvPointCount = iter.exactCount(); // Can we use .count() ? 
    int mstPointCount = crv.numCVs();
	
    // Stretch --------------------------------------------------------
	double expo = 1;
    if ((mstCrvLength > in_ml) && (in_maxstretch > 1)){
        if (in_softness != 0){
            double stretch = (mstCrvLength - in_ml) / (in_sl * in_maxstretch);
            expo = 1 - exp(-(stretch) / in_softness);
		}

        double ext = min(in_sl * (in_maxstretch - 1) * expo, mstCrvLength - in_ml);

        in_sl += ext;
	}
    else if ((mstCrvLength < in_ml) && (in_maxsquash < 1)){
        if (in_softness != 0){
            double squash = (in_ml - mstCrvLength) / (in_sl * in_maxsquash);
            expo = 1 - exp(-(squash) / in_softness);
		}

        double ext = min(in_sl * (1 - in_maxsquash) * expo, in_ml - mstCrvLength);

        in_sl -= ext;
	}
		
    // Position --------------------------------------------------------
    double size = in_sl / mstCrvLength;
    double sizeLeft = 1 - size;

    double start = in_position * sizeLeft;
    double end = start + size;

	double tStart, tEnd;
	crv.getKnotDomain(tStart, tEnd);
	
    // Process --------------------------------------------------------
    double step = (end - start) / (slvPointCount - 1.0);
    MPoint pt;
	MVector tan;
    while (! iter.isDone()){
        double perc = start + (iter.index() * step);

        double u = crv.findParamFromLength(perc * mstCrvLength);

        if ((0 <= perc) && (perc <= 1))
            crv.getPointAtParam(u, pt, MSpace::kWorld);
        else{
			double overPerc;
            if (perc < 0){
                overPerc = perc;
                crv.getPointAtParam(0, pt, MSpace::kWorld);
                tan = crv.tangent(0);
			}
            else{
                overPerc = perc - 1;
                crv.getPointAtParam(mstPointCount-3.0, pt, MSpace::kWorld);
                tan = crv.tangent(mstPointCount-3.0);

            tan.normalize();
            tan *= mstCrvLength * overPerc;

            pt += tan;
			}
		}

        pt *= mat.inverse();
        pt *= m;
        iter.setPosition(pt);
        iter.next();
	}
 
    return MS::kSuccess;
}
 
 