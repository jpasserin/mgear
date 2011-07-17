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

#include <maya/MFnPlugin.h>

/////////////////////////////////////////////////
// LOAD / UNLOAD
/////////////////////////////////////////////////
// INIT =========================================
MStatus initializePlugin( MObject obj )
{ 
	MStatus status;
	MFnPlugin plugin( obj, "Jeremie Passerin", "1.0", "Any");

	status = plugin.registerNode( "gear_curveCns", gear_curveCns::id, gear_curveCns::creator, gear_curveCns::initialize, MPxNode::kDeformerNode );
		if (!status) {status.perror("registerNode() failed."); return status;}
	
	status = plugin.registerNode( "gear_rollSplineKine", gear_rollSplineKine::id, gear_rollSplineKine::creator, gear_rollSplineKine::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_slideCurve2", gear_slideCurve2::id, gear_slideCurve2::creator, gear_slideCurve2::initialize, MPxNode::kDeformerNode );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_squashStretch2", gear_squashStretch2::id, gear_squashStretch2::creator, gear_squashStretch2::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_ikfk2Bone", gear_ikfk2Bone::id, gear_ikfk2Bone::creator, gear_ikfk2Bone::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_inverseRotOrder", gear_inverseRotOrder::id, gear_inverseRotOrder::creator, gear_inverseRotOrder::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_mulMatrix", gear_mulMatrix::id, gear_mulMatrix::creator, gear_mulMatrix::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_percentageToU", gear_percentageToU::id, gear_percentageToU::creator, gear_percentageToU::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_spinePointAt", gear_spinePointAt::id, gear_spinePointAt::creator, gear_spinePointAt::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}

	status = plugin.registerNode( "gear_uToPercentage", gear_uToPercentage::id, gear_uToPercentage::creator, gear_uToPercentage::initialize );
		if (!status) {status.perror("registerNode() failed."); return status;}
		


	return status;
}

// UNINIT =======================================
MStatus uninitializePlugin( MObject obj)
{
	MStatus status;
	MFnPlugin plugin( obj );
	
	status = plugin.deregisterNode( gear_curveCns::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_slideCurve2::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_rollSplineKine::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_squashStretch2::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
		
   
	status = plugin.deregisterNode( gear_ikfk2Bone::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_inverseRotOrder::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_mulMatrix::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_percentageToU::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}

	status = plugin.deregisterNode( gear_spinePointAt::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}
	status = plugin.deregisterNode( gear_uToPercentage::id );
		if (!status) {status.perror("deregisterNode() failed."); return status;}


		
	return MS::kSuccess;
}