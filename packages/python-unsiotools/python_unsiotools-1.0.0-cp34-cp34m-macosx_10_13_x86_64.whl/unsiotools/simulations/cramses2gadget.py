#!/usr/bin/env python
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# For more information about how to use UNSIO, visit:
# http://projets.lam.fr/projects/unsio/
# -----------------------------------------------------------------------
#  Copyright Jean-Charles LAMBERT (CeSAM)- 2008-2019
#
#  e-mail:   Jean-Charles.Lambert@lam.fr
#  address:  Centre de donneeS Astrophysique de Marseille (CeSAM)
#            Laboratoire d'Astrophysique de Marseille
#            Pole de l'Etoile, site de Chateau-Gombert
#            38, rue Frederic Joliot-Curie
#            13388 Marseille cedex 13 France
#            CNRS U.M.R 6110
# -----------------------------------------------------------------------

# unsio module loading
#import unsio
from unsio.input import *
from unsio.output import *
import math
import argparse
import numpy as np
# cmd line
import sys, getopt

class RamsesHeader:
    info={}
    boxsize=None
    xfactor=None
    mfactor=None

    a="aexp"
    H0="H0"
    omega_m="omega_m"
    omega_l="omega_l"
    ramses_length_unit="unit_l"
    ramses_dens_unit="unit_d"
    ramses_time_unit="unit_t"
    __ramsesdir=None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self,ramsesdir):
        self.__ramsesdir=ramsesdir
        self.__readHeader()
        self.__setUnits()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # __readHeader
    def __readHeader(self):
        print("processHeader",file=sys.stderr)
        self.__id_files=(self.__ramsesdir.split("_")[-1]).split("/")[0]
        print("id_files=",self.__id_files)
        self.__info_file=self.__ramsesdir+"/info_"+self.__id_files+".txt"
        print("info file=",self.__info_file)

        try:
            f=open(self.__info_file,"r")
        except:
            print("Unable to open file [%s]"%(self.__info_file))
            sys.exit(1)
        for line in f:
            kd=line.split("=")
            if len(kd)==2:
                key=kd[0].rstrip()
                value=(kd[1].rstrip()).lstrip()
                self.info[key] = value
                print("[%s] / <%s> "%(key,self.info[key]))

    def __setUnits(self):
        # some units
        kpc_in_cm  = 3.08E21
        Msun_in_cm = 1.9891E33
        h = 0.01 * float(self.info["H0"])
        a = float(self.info["aexp"])
        ramses_length_unit = float(self.info["unit_l"])
        ramses_time_unit   = float(self.info["unit_t"])
        ramses_dens_unit   = float(self.info["unit_d"])
        self.boxsize = float(self.info["boxlen"])

        # define units of destination format (= GADGET standard units)
        # (the numeric value must be set to the desired unit expressed in cgs units)
        gadget_length_unit = kpc_in_cm / h
        gadget_mass_unit   = 1E10 * Msun_in_cm / h
        gadget_velocity_unit = 1E5 * math.sqrt(a) # sqrt(a) factor: see GADGET users guide
        gadget_etherm_unit = 1E10 # units of v^2, but without the sqrt(a) factor

        # calculate unit conversion factors from ramses to gadget
        self.xfactor  = ramses_length_unit / gadget_length_unit / a # [ RF ]
        self.vfactor  = (ramses_length_unit/ramses_time_unit) / gadget_velocity_unit
        self.mfactor  = ramses_dens_unit * (ramses_length_unit**3) / gadget_mass_unit
        self.ufactor  = (ramses_length_unit/ramses_time_unit)**2 / gadget_etherm_unit

        #
        self.boxsize = self.boxsize
        self.h = h
        self.a = a
        self.omega_m = float(self.info["omega_m"])
        self.omega_l = float(self.info["omega_l"])
        self.H0      = float(self.info["H0"])
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None

     # help
    parser = argparse.ArgumentParser(description="Convert Ramses to Gadget2 snapshot",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('ramses', help='ramses input snapshot eg:output_01290')
    parser.add_argument('gadget2', help='gadget2 output snapshot')
    parser.add_argument('components', help='list of components eg:gas,stars')
    parser.add_argument('--time', help='selected time', default="all")
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    compute(args.ramses,args.gadget2,args.components,args.time)




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# printAndSaveProp
# print properties for the component comp given as argument
# and save them
def printAndSaveProp(uns,unso,comp,r2g):
    info="""\
    ----------------------------------------------
    Component : [%s]
    ----------------------------------------------
    """
    print(info % (comp))
    # return a 1D numpy data array with mass
    ok,mass=uns.getData(comp,"mass")
    if ok:
        print("mass =",mass,mass.size)
        efactor=1.0
        if comp=="gas":
            efactor=r2g.boxsize**3 # in unsio mass X boxsize**3
        if comp=="stars":
            unso.setData(1,"flagsfr")

        mass=r2g.mfactor*mass/(efactor) 
        unso.setData(mass,comp,"mass") # save mass
    # return a 1D numpy data array with pos
    ok,pos=uns.getData(comp,"pos")
    if ok:
        print("pos =",pos)
        efactor=1.0
        if comp=="gas":
            efactor=r2g.boxsize # in unsio pos X boxsize
        pos=r2g.xfactor*pos/efactor
        unso.setData(pos,comp,"pos") # save pos

    # return a 1D numpy data array with vel
    ok,vel=uns.getData(comp,"vel")
    if ok:
        print("vel =",vel)
        vel=r2g.vfactor*vel
        unso.setData(vel,comp,"vel") # save vel

    # return a 1D numpy data array with rho
    ok,rho=uns.getData(comp,"rho")
    if ok:
        print("rho =",rho)
        unso.setData(rho,comp,"rho") # save rho

    # return a 1D numpy data array with temperature
    ok,temp=uns.getData(comp,"temp")
    if ok:
        print("temp =",temp)
        if comp=="gas":
            temp=r2g.ufactor*temp
        unso.setData(temp,comp,"u") # save temperature

    # return a 1D numpy data array with hsml
    ok,hsml=uns.getData(comp,"hsml")
    if ok:
        print("hsml =",hsml)
        if comp=="gas":
            hsml = hsml/r2g.boxsize
        unso.setData(hsml,comp,"hsml") # save hsml

    # return a 1D numpy data array with particles age
    ok,age=uns.getData(comp,"age")
    if ok:
        print("age =",age)
        unso.setData(age,comp,"age") # save age

    # return a 1D numpy data array with mettalicity
    ok,metal=uns.getData(comp,"metal")
    if ok:
        print("metal =",metal)
        unso.setData(metal,comp,"metal") # save mettalicity


    # return a 1D numy data array with id
    ok,indexes=uns.getData(comp,"id")
    if ok:
        print("indexes =", indexes)
        unso.setData(indexes,comp,"id") # save id


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# compute
# loop on all selected time steps and print out properties
# for every components from "comp" variable
# and save them in a gadegt2 file
def compute(file,out,comp,times):

    r2g=RamsesHeader(file)

    print("Header.boxsize=",r2g.boxsize)
    print("Header.a=",r2g.a)
    print("Header.xfactor=",r2g.xfactor)
    print("Header.vfactor=",r2g.vfactor)
    print("Header.mfactor=",r2g.mfactor)
    print("Header.ufactor=",r2g.ufactor)


    print("file=",file, " outfile=",out," comp=",comp, " times=",times)

    # instantiate a CunsIn object, here we request to load "all" components
    uns=CUNS_IN(file,"all",times)

    # load frame
    cpt=0
    while (uns.nextFrame("")):  # load every snasphots

        nameout=out+".%05d"%cpt # create out filename
        print("Filename Out =",nameout)
        # instantiate a CunsOut object in "gadget2" format
        unso=CUNS_OUT(nameout,"gadget2",verbose_debug=True)

        ok,tsnap=uns.getData("time") # return snasphot time
        print("Snapshot input time : ","%.03f"%tsnap)
        print("Snapshot output time : ","%.03f"%r2g.a)
        unso.setData(r2g.a,"time") # save snapshot time

        # set Header
        print("set boxsize =",r2g.boxsize*r2g.xfactor)
        ok=unso.setData(r2g.boxsize*r2g.xfactor,"boxsize")
        print("set omega_l =",r2g.omega_l)
        ok=unso.setData(r2g.omega_l,"omega_l")
        print("set omega_m =",r2g.omega_m)
        ok=unso.setData(r2g.omega_m,"omega_m")
        print("set H0 =",r2g.H0)
        ok=unso.setData(r2g.H0,"H0")
        print("set redshift =",1./r2g.a-1.)
        ok=unso.setData(1./r2g.a-1.,"redshift")
        # loop on all components stored in comp variable
        for onecomp in (comp.split(",")):
            printAndSaveProp(uns,unso,onecomp,r2g) # print(properties for the component

        unso.save()  # save snasphot
        cpt+=1 # one more frame
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
if __name__ == "__main__":
    commandLine()
