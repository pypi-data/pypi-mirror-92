#!/usr/bin/env python

import sys
import unsio
from unsiotools.uns_simu import *
from unsiotools.simulations import csnapshot
from unsiotools.simulations import ccod
import argparse
import numpy as np

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None
    fastcod=True
    threshold=10000
     # help
    parser = argparse.ArgumentParser(description="Extract halo from multiple MDF halo simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('input', help='UNS input file')
    parser.add_argument('output', help='Nemo output file')
    parser.add_argument('haloN', help='Select halo number (1 or 2)',type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):

    cod=ccod.CCod(args.simname,verbose_debug=args.verbose)
    if cod.isMultipleHalo():
        print("Muliple halo = ",cod.isMultipleHalo())
        uns_snap=csnapshot.CSnapshot(args.input,"halo")
        ok = uns_snap.unsin.nextFrame()
        if ok:
            select="halo"
            ok,timex=uns_snap.unsin.getData("time")
            print("timex=",timex,type(timex))
            ok,pos=uns_snap.unsin.getData(select,"pos")
            ok,mass=uns_snap.unsin.getData(select,"mass")
            ok,vel =uns_snap.unsin.getData(select,"vel")
            ok,id=uns_snap.unsin.getData(select,"id")
            ok,mass,pos,vel = cod.getExtractHalo(id,mass,pos,vel,args.haloN)
            print(mass,pos,vel)
            unso=unsio.CunsOut(args.output,"nemo")
            unso.setValueF("time",timex)
            unso.setArrayF("all","pos",pos)
            unso.setArrayF("all","mass",mass)
            unso.setArrayF("all","vel",vel)
            unso.save()
        else:
            print("Unable to load data from [%s]"%(agrs.snapshot))
    else :
        print("No multiple halo detected for simulation [%s]"%(args.simname))




#
# ----
#
def extractHalo(self,id,mass,pos,vel):
    id_sort=np.argsort(id) # sort according to ID order
    offset=0
    myidsort=np.zeros(1)
    if self.__halo_N==1:   # first halo
        mylast=self.__halo_part[0]
        myidsort = id_sort[0:mylast]
    else :                 # second halo
        mylast=self.__halo_part[1]
        offset = self.__halo_part[0]+mylast
        myidsort = id_sort[self.__halo_part[0]:offset]
    #print("myidsort : ",myidsort,mylast,self.__halo_part)
    pos = np.reshape(pos,(-1,3)) # reshape pos to nbody,3
    pos = np.reshape(pos[myidsort],-1) # select ids
    vel = np.reshape(vel,(-1,3)) # reshape vel to nbody,3
    vel = np.reshape(vel[myidsort],-1) # select ids

    return True,mass[myidsort],pos,vel

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
