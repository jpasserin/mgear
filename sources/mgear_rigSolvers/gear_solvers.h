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
#ifndef _rigSolvers
#define _rigSolvers

#define McheckErr(stat,msg)         \
    if ( MS::kSuccess != stat ) {   \
                cerr << msg;                \
                return MS::kFailure;        \
        }

/////////////////////////////////////////////////
// INCLUDE
/////////////////////////////////////////////////


#include <maya/MGlobal.h>
#include <maya/MPxNode.h>
#include <maya/MPxDeformerNode.h>

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>

#include <maya/MQuaternion.h>
#include <maya/MVector.h>
#include <maya/MVectorArray.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MDoubleArray.h>
#include <maya/MEulerRotation.h>


#include <maya/MFnMesh.h>
#include <maya/MItGeometry.h>
#include <maya/MDagModifier.h>
#include <maya/MPointArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MPoint.h>

#include <maya/MTypeId.h> 


#include <maya/MStatus.h>
 
 
 

#define PI 3.14159265


/////////////////////////////////////////////////
// STRUCTS
/////////////////////////////////////////////////
struct s_GetFKTransform
{
   double lengthA;
   double lengthB;
   bool negate;
   MTransformationMatrix root;
   MTransformationMatrix bone1;
   MTransformationMatrix bone2;
   MTransformationMatrix eff;
};

struct s_GetIKTransform
{
   double lengthA;
   double lengthB;
   bool negate;
   double roll;
   double scaleA;
   double scaleB;
   double maxstretch;
   double softness;
   double slide;
   double reverse;
   MTransformationMatrix root;
   MTransformationMatrix eff;
   MTransformationMatrix	 upv;
};

/////////////////////////////////////////////////
// CLASSES
/////////////////////////////////////////////////
class gear_slideCurve2 : public MPxDeformerNode
{
public:
                    gear_slideCurve2() {};
    virtual MStatus deform( MDataBlock& data, MItGeometry& itGeo, const MMatrix &localToWorldMatrix, unsigned int mIndex );
    static  void*   creator();
    static  MStatus initialize();
 
    static MTypeId      id;

	// Input
	static MObject	 master_crv;
	static MObject	 master_mat;

	static MObject	 slave_length;
	static MObject	 master_length;
	static MObject	 position;

	static MObject	 maxstretch;
	static MObject	 maxsquash;
	static MObject	 softness;
};

class gear_curveCns : public MPxDeformerNode
{
public:
                    gear_curveCns() {};
    virtual MStatus deform( MDataBlock& data, MItGeometry& itGeo, const MMatrix &localToWorldMatrix, unsigned int mIndex );
    static  void*   creator();
    static  MStatus initialize();
 
    static MTypeId      id;
    static  MObject     inputs; 
};

class gear_rollSplineKine : public MPxNode
{
 public:
      gear_rollSplineKine();	
   virtual	 ~gear_rollSplineKine();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;

	// Input
	static MObject	 ctlParent;
	static MObject	 inputs;
	static MObject	 inputsRoll;
	static MObject	 outputParent;

	static MObject	 u;
	static MObject	 resample;
	static MObject	 subdiv;
	static MObject	 absolute;

	// Output
	static MObject	 output;

};
class gear_squashStretch2 : public MPxNode
{
 public:
      gear_squashStretch2();	
   virtual	 ~gear_squashStretch2();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;
	
	// Input
	static MObject	 global_scale;
	static MObject	 global_scalex;
	static MObject	 global_scaley;
	static MObject	 global_scalez;

	static MObject	 blend;
	static MObject	 driver;
	static MObject	 driver_min;
	static MObject	 driver_ctr;
	static MObject	 driver_max;
	static MObject	 axis;
	static MObject	 squash;
	static MObject	 stretch;

	// Output
	static MObject	 output;

};

class gear_percentageToU : public MPxNode
{
 public:
      gear_percentageToU();	
   virtual	 ~gear_percentageToU();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;
	
	// Input
	static MObject	 curve;
	static MObject	 normalizedU;
	static MObject	 percentage;
	static MObject	 steps;

	// Output
	static MObject	 u;

};

class gear_uToPercentage : public MPxNode
{
 public:
      gear_uToPercentage();	
   virtual	 ~gear_uToPercentage();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;
	
	// Input
	static MObject	 curve;
	static MObject	 normalizedU;
	static MObject	 u;
	static MObject	 steps;

	// Output
	static MObject	 percentage;

};

class gear_spinePointAt : public MPxNode
{
 public:
      gear_spinePointAt();	
   virtual	 ~gear_spinePointAt();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;
	
	// Input
	static MObject	 rotA;
	static MObject	 rotAx;
	static MObject	 rotAy;
	static MObject	 rotAz;
	static MObject	 rotB;
	static MObject	 rotBx;
	static MObject	 rotBy;
	static MObject	 rotBz;
	static MObject	 axe;
	static MObject	 blend;

	// Output
	static MObject	 pointAt;

};

class gear_inverseRotOrder : public MPxNode
{
 public:
      gear_inverseRotOrder();	
   virtual	 ~gear_inverseRotOrder();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;

	// Input
	static MObject	 rotOrder;

	// Output
	static MObject	 output;

};

class gear_mulMatrix : public MPxNode
{
 public:
      gear_mulMatrix();	
   virtual	 ~gear_mulMatrix();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();

 public:
	static MTypeId id;

	// Input
	static MObject	 matrixA;
	static MObject	 matrixB;

	// Output
	static MObject	 output;

};


class gear_ikfk2Bone : public MPxNode
{
 public:
      gear_ikfk2Bone();	
   virtual	 ~gear_ikfk2Bone();	

   virtual MStatus compute( const MPlug& plug, MDataBlock& data );
   static void* creator();
   static MStatus initialize();
   MTransformationMatrix getIKTransform(s_GetIKTransform values, MString outportName);
   MTransformationMatrix getFKTransform(s_GetFKTransform values, MString outportName);

 public:

	// ATTRIBUTES
	static MObject	 blend;

	static MObject	 lengthA;
	static MObject	 lengthB;
	static MObject	 negate;

	static MObject	 scaleA;
	static MObject	 scaleB;
	static MObject	 roll;	

	static MObject	 maxstretch;
	static MObject	 slide;
	static MObject	 softness;	
	static MObject	 reverse;	
	
	// INPUTS
	static MObject	 root;
	static MObject	 ikref;
	static MObject	 upv;
	static MObject	 fk0;
	static MObject	 fk1;
	static MObject	 fk2;

	// OUTPUTS
	static MObject	 inAparent;
	static MObject	 inBparent;
	static MObject	 inCenterparent;
	static MObject	 inEffparent;

	static MObject	 outA;
	static MObject	 outB;
	static MObject	 outCenter;
	static MObject	 outEff;

	static MTypeId id;
};


/////////////////////////////////////////////////
// METHODS
/////////////////////////////////////////////////
MQuaternion e2q(double x, double y, double z);
MQuaternion slerp2(MQuaternion qA, MQuaternion qB, double blend);
double clamp(double d, double min_value, double max_value);
int clamp(int d, int min_value, int max_value);
double getDot(MQuaternion qA, MQuaternion qB);
double radians2degrees(double a);
double degrees2radians(double a);
double round(const double value, const int precision);
double normalizedUToU(double u, int point_count);
double uToNormalizedU(double u, int point_count);
unsigned findClosestInArray(double value, MDoubleArray in_array);  
double set01range(double value, double first, double second);
double linearInterpolate(double first, double second, double blend);
MVector linearInterpolate(MVector v0, MVector v1, double blend);
MVectorArray bezier4point( MVector a, MVector tan_a, MVector d, MVector tan_d, double u);
MVector rotateVectorAlongAxis(MVector v, MVector axis, double a);
MQuaternion getQuaternionFromAxes(MVector vx, MVector vy, MVector vz);
MTransformationMatrix mapWorldPoseToObjectSpace(MTransformationMatrix objectSpace, MTransformationMatrix pose);
MTransformationMatrix mapObjectPoseToWorldSpace(MTransformationMatrix objectSpace, MTransformationMatrix pose);
MTransformationMatrix interpolateTransform(MTransformationMatrix xf1, MTransformationMatrix xf2, double blend);


#endif