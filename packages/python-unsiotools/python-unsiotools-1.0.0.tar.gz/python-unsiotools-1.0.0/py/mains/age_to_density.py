#!/usr/bin/env python
#

from __future__ import print_function
#
# save stars particles to density field for displaying with glnemo2

# MANDATORY
from unsio.input import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

import sys

#from IPython import embed

class snap:
    time   = None
    nbody  = None
    mass   = None
    pos    = None
    vel    = None
    ids    = None
    ages   = None
    hsml   = None
    rho    = None
    metal  = None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dt=3
    f_hsml=0.0001
    parser = argparse.ArgumentParser(description="Save stars ages into density field of a NEMO snapshot ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='UNS input file with stars particle')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('--dt', help="save particles:[age > time-time*dt%%],(time=current time)",default=dt,type=float)
    parser.add_argument('--hsml', help='hsml value',type=float,default=f_hsml)

    #parser.add_argument('time', help="time of reference to keep stars particles")


    args = parser.parse_args()

    process(args.input,args.output,args.dt,args.hsml)#,args.time)



# -----------------------------------------------------
# selectAges
def selectAges(snap,dt,f_hsml): #,times):

    select=(snap.ages>=(snap.time-snap.time*dt/100.))   # select particles in the ramge of ages

    snap.pos=np.reshape(snap.pos,(-1,3)) # pos reshaped in a 2D array [nbody,3]
    snap.vel=np.reshape(snap.vel,(-1,3)) # pos reshaped in a 2D array [nbody,3]

    # rescale pos
    snap.pos = snap.pos[select]
    snap.pos = np.reshape(snap.pos,snap.pos.size) # flatten the array (mandatory for unsio)

    # rescale vel
    snap.vel = snap.vel[select]
    snap.vel = np.reshape(snap.vel,snap.vel.size) # flatten the array (mandatory for unsio)

    #rescale mass
    snap.mass = snap.mass[select]

    # rescale ages
    snap.ages = snap.ages[select]

    # hsml
    snap.hsml=np.zeros(snap.ages.size,dtype='float32')
    snap.hsml += f_hsml

# -----------------------------------------------------
# compute, is the core function
def process(simname,out,dt,hsml): #,times):
    components="stars"
    verbose=False

    #timef=float(times)

    # Create a UNSIO object
    uns = CUNS_IN(simname,components,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print ("simname=",simname, " out=",out,file=sys.stderr)

    # load frame
    ok=uns.nextFrame("")
    #print ok

    if (ok) :
        ok,snap.ages = uns.getData("stars","age")
        if ( ok ) :
            #print "ok ",ok, snap.ages
            print ("min=", snap.ages.min()," max=",snap.ages.max(),file=sys.stderr)
            #embed()
            ok,snap.time = uns.getData("time")
            ok,snap.pos  = uns.getData("stars","pos")
            ok,snap.vel  = uns.getData("stars","vel")
            ok,snap.mass = uns.getData("stars","mass")

            # select ages according to dt
            selectAges(snap,dt,hsml)

            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file

            # save data
            unso.setValueF("time",snap.time)       # save time
            unso.setArrayF("all","pos",snap.pos)   # save pos
            unso.setArrayF("all","vel",snap.vel)   # save vel
            unso.setArrayF("all","mass",snap.mass) # save mass
            unso.setArrayF("all","rho",snap.ages)  # save ages to rho
            unso.setArrayF("all","hsml",snap.hsml) # save hsml

            unso.save()

        else:
            print ("there are no age for stars in this snapshot !!!",file=sys.stderr)


    else :
        print ("Didn't load anything....",file=sys.stderr)


# -----------------------------------------------------
# main program
commandLine()   # parse command line
