// ============================================================================
// Copyright Jean-Charles LAMBERT - 2009                                       
// e-mail:   Jean-Charles.Lambert@oamp.fr                                      
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

#ifndef CSNAPTOOLS_H
#define CSNAPTOOLS_H
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <map>

#include <cmath>

namespace jclut {


    class CSnaptools {
    public:
      CSnaptools() {;}
      
      template <class T> static void moveToCod(const int nbody,T * pos, T * Vel, T * mass, T * rho, double cod[6], bool move, bool verbose=false);
      template <class T> static void moveToCom(const int nbody,T * pos, T * mass, bool verbose=false);
      template <class T> static bool getTimeDataFile(std::string _file,const T time,const int n,
                                                     T data[],const T offset=0.0001,const  bool verbose=false);

      template <class T> static void zrotate(const int nbody,T * pos, T * vel, T * acc,const double angle);
      template <class T> static void rotatevec(T * vec, T * mat);

      static bool isFileExist(std::string, bool abortOnFalse=false);
      static std::string basename(const std::string);
      static std::string dirname(const std::string);
      static std::string parseString(std::string & next_string, const std::string sep=",");
      template <class T> static std::vector<T> stringToVector(const std::string s, const int min, T val, std::string sep=",");
      template <class T> static std::vector<T> rangeToVectorIndexes(const std::string s, const int max, std::string sep=",");
      static std::map<std::string, std::vector<int> > mapStringVectorIndexes(const std::string s, const int max, std::string sep1="+",std::string sep2="@",std::string sep3=",");
      template <class T> static bool isStringANumber(const std::string mystring, T &data);
      template <class T> static T minArray(const int, const T * array);
      template <class T> static T maxArray(const int, const T * array);
      template <class T> inline static T stringToNumber(const std::string mystring) {
        T value;
        std::stringstream parse(""); // string parsed
        parse << mystring;
        parse >> value;
        return value;
      };
      static std::string fixFortran(const char *,const bool lower=true);
      static std::string fixFortran(const char *,const int len, const bool lower=true);
      static std::string toupper(std::string);
      static std::string tolower(std::string);
    };   
}
extern"C" {
void derotate_f_(const char * rotatefile, const float * time,const int * nbody,float * pos, float * vel, float * acc, const int lenstring );
void center_on_cod_file_(const char * codfile, const float * time, const int * nbody,float * pos, float * vel, float * mass, const int lenstring );
}

#endif
//
  
