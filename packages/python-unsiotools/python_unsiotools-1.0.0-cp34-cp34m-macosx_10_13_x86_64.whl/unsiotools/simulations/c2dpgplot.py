#!/usr/bin/python
from __future__ import print_function
from ..uns_simu import *
#from .csnapshot import *
import sys
try:
    from .. import py_unstools # rectify swig
except ImportError:
    print("WARNING !!!,c2dpgplot failed to import module [py_unstools]",file=sys.stderr)


from multiprocessing import Lock
import time
import os
import numpy as np

#
# ----
#
class C2dpgplot:
    """
    Draw 2d image using uns_project C2dplot engine
    """
    #
    # ----
    #
    # constructor
    __analysis=None
    dimx=1024
    dimy=1024
    pixel=20
    gp=5.0
    __c=None

    def __init__(self,analysis=None,dimx=1024,dimy=1024,pixel=20,gp=5.0,verbose=False,verbose_debug=False):
        """
        Constructor of C2dplot class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """

        self.__vdebug=verbose_debug
        self.__verbose=verbose
        self.dimx  = dimx
        self.dimy  = dimy
        self.pixel = pixel
        self.gp    = gp
        self.__c=py_unstools.C2dplotF(1,self.pixel,self.dimx,self.dimy,self.gp)


        if analysis is not None:
            self.__analysis=analysis
            self.__smartAnalysisInit()
        else:
            pass

    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        data=self.__analysis

    #
    # draw
    #
    def draw(self,uns_snap,select,outdev,prop="",xy=True,xz=True,zy=False,com=True,\
             hsml=False,cmap=0,title="plot",pfname=1,times="all",no=0,rrange="35",\
             psort=0,itf=1,cb=0):
        """
        draw 2D image using uns_projects C2dplot engine
        """

        # try to load positions
        ok,pos=uns_snap.unsin.getData(select,"pos")
        if ok:
            # load time
            ok,time=uns_snap.unsin.getData("time")

            # build range vector
            nrange=np.empty([3,2],dtype='f')
            if  str(rrange).find(":")!=-1:
                left,right=str(rrange).split(":")
                nrange[:,0]=float(left)
                nrange[:,1]=float(right)
            else:
                nrange[:,0]=-float(rrange)
                nrange[:,1]= float(rrange)
            nrange=np.reshape(nrange,nrange.size) #reshape in 1D

            legend=""
            comp_prop=select
            weight=np.array([],dtype='f')

            # properties
            if prop != "":
                ok,weight=uns_snap.unsin.getData(select,prop)
                if not ok:
                    print("No properties [%s] for the selection"%(prop))
                else:
                    if prop=="age":
                        legend="Time of birth "
                    else:
                        comp_prop=comp_prop+" "+prop
            else:
                pass

            # sort
            if psort:
                legend=legend+"sort "
            else:
                legend=legend+"add "
            # image transfer function
            sitf=["linear","log","square"]
            if (itf>=0 and itf<=3):
                legend=legend+sitf[itf]
            # com
            if com:
                ok,mass=uns_snap.unsin.getData(select,"mass")
                if mass.size<1:
                    mass=np.ones(pos.size/3)
                uns_snap.center(pos,None,mass,center=True)
                print("center pos=",pos)
            # print file name ?
            if pfname:
                filename=uns_snap.unsin.getFileName()
            else:
                filename=""
            # color bar
            if cb:
                cb=True
            else:
                cb=False
            #weight=np.ones(pos.size/3,dtype="f")

            hsml=np.array([],dtype='f')

            #print(pos.size,outdev,no,weight)
            #print(outdev,no,pos,nrange,title,comp_prop,filename,time.item(),xy,xz,zy,\
            #                       True,weight,psort,hsml,itf,cb,legend,cmap)
            print("TIME =",time,type(time))
            self.__c.compute_image(outdev,no,pos,nrange,title,comp_prop,filename,time,xy,xz,zy,\
                                   True,weight,psort,hsml,itf,cb,legend,cmap)

        else:
            print("There is no position in snapshot...")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse

    # help
    parser = argparse.ArgumentParser(description="Compute 2D image using uns_projects c2dpgplot engine",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('snapshot', help="uns input snapshot",default=None)
    parser.add_argument('component', help="selected component",default=None)
    parser.add_argument('--range', help="plot range (X or -A:B) ",default=35,type=str)
    parser.add_argument('--psort', help="sort particles according to properties",default=0,type=int)
    parser.add_argument('--prop', help="properties to plot (age,rho)",default="",type=str)
    parser.add_argument('--pfname', help="print filename (1:True, 0:False)",default=1,type=int)
    parser.add_argument('--cb', help="display color bar (1:True, 0:False)",default=0,type=int)
    parser.add_argument('--cmap', help="color map (0:rainbow, 1:heat, 2:gray)",default=0,type=int)
    parser.add_argument('--dev', help="pgplot device",default="?")
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    import unsiotools.simulations.c2dpgplot as c2dpg
    import unsiotools.simulations.csnapshot as csnap
    try:
        uns=csnap.CSnapshot(args.snapshot,args.component,verbose_debug=args.verbose)
        ok=uns.unsin.nextFrame("")
        if ok:
            c=c2dpg.C2dpgplot()
            c.draw(uns_snap=uns,select=args.component,outdev=args.dev,rrange=args.range,\
                   prop=args.prop,psort=args.psort,pfname=args.pfname,cb=args.cb,cmap=args.cmap)
        else:
            print ("[%s] is not a UNS snapshot ..."%(simname))
    except Exception as x :
        print (x)
        #import traceback
        #traceback.print_exc(file=sys.stdout)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
