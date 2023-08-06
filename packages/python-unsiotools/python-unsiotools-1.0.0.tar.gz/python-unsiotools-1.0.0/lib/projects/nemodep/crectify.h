// ============================================================================
// Copyright Jean-Charles LAMBERT - 2014
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)
// e-mail:   Jean-Charles.Lambert@lam.fr
// address:  Dynamique des galaxies
//           Laboratoire d'Astrophysique de Marseille
//           Pole de l'Etoile, site de Chateau-Gombert
//           38, rue Frederic Joliot-Curie
//           13388 Marseille cedex 13 France
//           CNRS U.M.R 6110
// ============================================================================

/*
  @author Jean-Charles Lambert <Jean-Charles.Lambert@lam.fr>
*/

/*
This class aims to rectify a galaxy in XY plan. It's based on snaprect program
from the NEMO project, see:
http://carma.astro.umd.edu/nemo/man_html/snaprect.1.html
*/
#ifndef CRECTIFY_H
#define CRECTIFY_H
#include <string>
#include "cfalcon.h"
#include <cassert>
#define SINGLEPREC
#define real float
extern "C" {
#include <vectmath.h>
}
#include "csnaptools.h"
#undef real // prevent conflict with SWIG py_unsio.i
namespace uns_proj {

class CDataIndex {
public:
  CDataIndex() {}
  CDataIndex(const float _data, const int _index){
    setDI(_data, _index);
  }
  void foo() {

  }

  void setDI(float _data, int _index ) {
    data = _data;
    index = _index;
  }

  static bool sortData(const CDataIndex& a, const CDataIndex& b);
  float data;
  int index;
};

class CRectify {
public:
  CRectify(bool _verbose=false);
  //------------------------------------------------------------------------------
  // Rectify
  // this method rectify position and vitesse for tge current time, according to
  // the followings rules :
  // _use_rho = true, use density as weighting factor, if _rho array is empty then
  //            local density is computed
  //          = false, use mass as weighting factor
  // _threshold=when compute density, program will keep only particles above threshold
  //            which must be a value between 0.0% and 100.0%
  // _rectify = true, positions and velocities will be rectified
  //          = false, vectors only are computed
  // _cod_file= is a filename contening COD of snapshots
  //            if you don't provide this file, you must set _use_tho=true
  // _rect_file=output file with results of the rectification, with the following format
  //            time 6xCOD 9xVectors
  //
  bool rectify(const int nbody,const float time,
               float * pos, float * vel,float * mass, float * weight,
               const bool _use_rho, const bool rectify=false,
               std::string cod_file="",std::string rect_file="", const float radius=50.0, const float dmin=0.0, const float dmax=100.0);



  //
  // computeEigenVectors : (SWIG interface for python)
  // compute eigen vectors on current snapshot
  // return bool,array
  //
  // array is one dimension with 16 elements:
  // t codx(3) codv(3) eigen_values(flatten matrix 3x3)
  int computeEigenVectors(int n1, float * _pos , int n2, float * _vel,
              int n3, float * _mass, int n4, float * _rho,
              int n5, float * _rect_array,
              const float _time,
              const bool _use_rho, const bool _rectify=false,
              std::string _cod_file="",
              const float _radius=50.0,const float _dmin=0.0, const float _dmax=100.0) {

    if (n2 && n3 && n4) {;} // remove compiler warning
      assert(n5==16);

      only_eigen_values=true;  // !!!
      std::cerr << "Use rho="<<_use_rho << " dmin=" << _dmin << " dmax=" << _dmax << "\n";
      bool ok=rectify(n1/3,_time,_pos,_vel,_mass,_rho,_use_rho,_rectify,_cod_file,"",_radius,_dmin,_dmax);

      // fill up returns array
      int ii=0;
      _rect_array[ii++] = time;
      for (int i=0; i<6; i++) {
        _rect_array[ii++] = codf[i];
      }
      if (ok) {
        for (int i=0; i<3; i++) {
          _rect_array[ii++] = frame[i][0];
          _rect_array[ii++] = frame[i][1];
          _rect_array[ii++] = frame[i][2];
        }
      } else {
        for (int i=0; i<3; i++) {
          _rect_array[ii++] = 0.0;
          _rect_array[ii++] = 0.0;
          _rect_array[ii++] = 0.0;
        }
      }

      return ok;
    }

  void process();
  //------------------------------------------------------------------------------
  // snapTransform STATIC
  // rectify positions and velocities using rect_file
  // this function returns :
  // true if time value has been found in rect file
  // false otherwise
  static bool snapTransform(const int nbody,const float time,
                            float * pos, float * vel,std::string rect_file, int &status);
  void initOldFrame() {
    float init_frame[][3] = {
      { 1.0, 0.0, 0.0, },
      { 0.0, 1.0, 0.0, },
      { 0.0, 0.0, 1.0, }};
    memcpy(oldframe,init_frame,9*sizeof(float));
  }

private:
  jclut::CDensity * density;
  float time, * pos, * vel, * mass, * rho;
  float radius,dmin, dmax;
  float oldframe[3][3];
  std::string cod_file, rect_file;
  bool rect, use_rho;
  int nbody;
  bool w_sum_ok; // w_sum is positif
  std::vector<CDataIndex> rho_di;
  void init();
  void processRho();
  void findCenter();
  void findMoment();
  void snapTransform();
  void computeVectors();
  void eigenFrame(float frame[3][3], matrix mat);
  void xyz2rtp(float xyz[3], float rtp[3]);
  void printvec(std::string name, float vec[3]);
  void saveRectVector();

  matrix w_qpole;
  double cod[6];
  float codf[6];
  float frame[3][3];
  std::vector <float> vpos,vvel,vmass,vrho;
  bool verbose;
  bool only_eigen_values; // toggle only eigen values computation
};

}

extern "C" {
    bool rectify_snap_(const int * nbody,const float * time,
                       float * pos, float * vel,
                       const char * rect_file, int *status, const int lenstring) {

      std::string filename=jclut::CSnaptools::fixFortran(rect_file,lenstring);

      return uns_proj::CRectify::snapTransform(*nbody,*time,pos,vel,filename,*status);
    }

    // fortran wrapper, parameters
    // IN[integer]     nbody : #bodies
    // IN[real4]       time
    // IN[real4 array] pos, vel, mass, rho
    // IN[integer]     use_rho : 0 or 1 to compute density
    // IN[character]   cod_file
    //OUT[character]   rectfile (eigens vectors values)
    // IN[float]       cuting_radius
    // IN[float]       dmin (%density min)
    // IN[float]       dmax (%density max)

    // for mdf (stars, set use_rho=0 and set a cuting_radius,
    // then rho,dmin,dmax are not used, can be 0)
    bool rectify_full_(const int * nbody,const float * time,
                       float * pos, float * vel, float * mass, float * rho,
                       int * use_rho,const char * cod_file, const char * rect_file,
                       float * radius, float * dmin, float * dmax,
                       const int len_cod, const int len_rect) {

      std::string mycodf=jclut::CSnaptools::fixFortran(cod_file,len_cod);
      std::string myrectf=jclut::CSnaptools::fixFortran(rect_file,len_rect);
      // Rectify object
      uns_proj::CRectify * crectify = new uns_proj::CRectify();
      bool status=crectify->rectify(*nbody,*time,pos,vel,mass,rho,*use_rho,true,mycodf,
                        myrectf,*radius,*dmin,*dmax);
      delete crectify;
      return status;
    }
}
#endif // CRECTIFY_H
