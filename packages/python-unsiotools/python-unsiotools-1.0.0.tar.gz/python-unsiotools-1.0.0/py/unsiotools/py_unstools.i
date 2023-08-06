//-*- C -*- 
// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2017
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)              
// e-mail:   Jean-Charles.Lambert@lam.fr                                      
// address:  Aix Marseille Universite, CNRS, LAM 
//           Laboratoire d'Astrophysique de Marseille                          
//           Pole de l'Etoile, site de Chateau-Gombert                         
//           38, rue Frederic Joliot-Curie                                     
//           13388 Marseille cedex 13 France                                   
//           CNRS UMR 7326 
// ============================================================================
// Swig python interface for UNS_PROJECTS
// ============================================================================

// python module name
%module py_unstools

%{
#define SWIG_FILE_WITH_INIT
#include "cfalcon.h"
#include "ctree.h"
#include "crectify.h"
#include "c2dplot.h"
%}
   
%include "numpy.i"
%include "std_string.i"

%init %{
 import_array();
%}


// CF http://web.mit.edu/6.863/spring2011/packages/numpy_src/doc/swig/doc/numpy_swig.html

// IN_ARRAY are defined as arrays of data that are passed into a routine but are not altered in-place or returned to the user.
// INPLACE_ARRAY1 are defined as arrays that are modified in-place
// ARGOUT_ARRAY1 are arrays that appear in the input arguments in C, but are in fact output arrays
// ARGOUT_VIEWARRAY1 are for when your C code provides you with a view of its internal data and does not require any memory to be allocated by the user. //                   This can be dangerous

// for compute_gravity, compute_density
%apply (int DIM1  , float  * IN_ARRAY1) {(int n1, float  * pos), (int n2, float  * mass)}
%apply (int DIM1  , double * IN_ARRAY1) {(int n1, double * pos), (int n2, double * mass)}
// for compute_density
%apply ( int DIM1, float * INPLACE_ARRAY1  ) {( int n3, float * inplace1 ),( int n4, float * inplace2 )};


%inline %{
   typedef float real; // real is not known
%}

// Parse the original header file
%include "cfalcon.h"


%extend jclut::cfalcon {

  bool compute_gravity(int n1, float * pos, int n2, float * mass, int n3,  float * inplace1, int  n4, float * inplace2,
		  float eps, 
		  float G=1.0,
		  float theta=0.6,
		  int kernel_type=1,
		  int ncrit=6) {

    assert(n1==n3);
    assert(n4==n1/3);
    $self->addGravity(n1/3,pos,mass,inplace1,inplace2,eps,G,theta,kernel_type,ncrit);

    return 1;
  }
  bool compute_density(int n1, float * pos, int n2, float * mass, int n3, float * inplace1, int n4, float * inplace2,
		   const int method=0, const int K=32,const int N=1, const int ncrit=0) {
    jclut::CDensity * d = new jclut::CDensity();
    d->setData(n1/3,pos,mass);
    d->compute(method,K,N,ncrit);

    assert(n2==n3);
    assert(n3==n4);
    memcpy(inplace1,d->getRho(),sizeof(float)*n1/3);
    memcpy(inplace2,d->getHsml(),sizeof(float)*n1/3);
    delete d;
    return 1;
  }
};

//
// -- CTree class
//
%apply (int DIM1  , float  * IN_ARRAY1) {(const int n1, const float  * pos), (const int n2, const float  * mass)}
%apply (int DIM1  , double * IN_ARRAY1) {(const int n1, const double * pos), (const int n2, const double * mass)}
%apply (int DIM1  , int    * ARGOUT_ARRAY1) {(int n, int * levels)} // get_levels
%apply (int DIM1  , double    * ARGOUT_ARRAY1) {(int n, double * radius)} // get_closest_distance_to_mesh

%rename(CTreeF) CTree(const int n1, const float * pos, const int n2, const float * mass,
     const double _fcells, const double _rsize);
%rename(CTreeD) CTree(const int n1, const double * pos, const int n2, const double * mass,
     const double _fcells, const double _rsize);

%include "ctree.h" // parse header

%extend jcltree::CTree {
  int get_levels(int n, int * levels) {
    assert(n==$self->getNbody());
    for (int i=0; i<n; i++) {
      levels[i]=($self->getBodyData()+i)->level;
    }
    return 1;
  }
  int get_closest_distance_to_mesh(int n, double * radius) {
    assert(n==$self->getNbody());
    for (int i=0; i<n; i++) {
      radius[i]=$self->distanceBodyToMesh(i);
    }
    return 1;
  }
}


%template(CTreeF) jcltree::CTree<float>;
%template(CTreeD) jcltree::CTree<double>;

//
// -- CRectify class
//
%apply (int DIM1  , float  * INPLACE_ARRAY1) {
             (int n1, float  * _pos ), 
	     (int n2, float  * _vel ), 
	     (int n3, float  * _mass),
	     (int n4, float  * _rho )
}

%apply   (int DIM1  , float * ARGOUT_ARRAY1) {
             (int n5, float  * _rect_array )
}

%apply (int DIM1  , float  * INPLACE_ARRAY1) {
             (int nn1, float  * ppos )
}
%include "crectify.h"


%extend uns_proj::CRectify {
}
//
// -- C2dplot class
//
%apply (int DIM1, float * IN_ARRAY1) {(int n1, float * pos),(int n2, float * weight),(int n3, float * hsml),(int n4, float * _range)}
%apply (int DIM1, double* IN_ARRAY1) {(int n1, double* pos),(int n2, double* weight),(int n3, double* hsml)}

%include "c2dplot.h"

%extend uns_proj::C2dplot {
  bool compute_image(std::string _dev, const int _no_frame,int n1, T * pos , int n4, float * _range, 
		    std::string _title,std::string _sel_comp,std::string _filename, float _timu,
		    bool _xy, bool _xz, bool _zy, bool _sview, int n2, T * weight,
		    const int _psort, int n3, T  * hsml, const int _itf, const bool _wedge, 
		    std::string _legend, const int _cmap) {

    // float _range[3][2]
    T *p_hsml = NULL;
    if (n3 !=0) {
      p_hsml=hsml;
    }
    T *p_weight = NULL;
    if (n2 !=0) {
      p_weight=weight;
    }
    
    $self->compute(_dev,_no_frame,n1/3,pos,(float (*)[2]) _range,_title,_sel_comp,_filename,
	    _timu,_xy,_xz,_zy,_sview, p_weight, _psort, p_hsml, _itf, _wedge, _legend,_cmap);

  }
}

%template(C2dplotF) uns_proj::C2dplot<float >;
%template(C2dplotD) uns_proj::C2dplot<double>;
//
