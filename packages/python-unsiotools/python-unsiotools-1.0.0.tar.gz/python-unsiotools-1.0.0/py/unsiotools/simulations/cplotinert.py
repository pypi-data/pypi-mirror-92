#!/usr/bin/env python
from __future__ import print_function
from ..uns_simu import *

import time
import os,sys
import numpy as np
import math
import time

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#from IPython import embed

#
# ----
#
class CPlotInert:
    """
    plot results of moment of Inertia computing (MOI)
    """
    #

    def __init__(self,simname,disp=True,ncut=20,component="halo",outfile=None,verbose=False,verbose_debug=False,progress=True):
        """
        Constructor of CPlotInert class

        Arguments :
        simname   : simulation name, must belong to uns database
        disp      : True , display in screen, False on file
        component : component's name (not used so far bc we only compute moment of inertia - MOI - on HALO)
        outfile   : if None, save graphic on simulation directory, else in outfile
        ncut      : #cuts used during MOI computing
        progress  : display progress bar
        """
        self.__vdebug=verbose_debug
        self.__verbose=verbose

        self.__simname=simname
        self.__disp=disp
        self.__outfile=outfile
        self.__component=component
        self.__progress=progress

        sql3 = UnsSimu(simname)
        r = sql3.getInfo()

        if (r) : # simulation exist
            self.__dir_moi=r['dir']+'/ANALYSIS/inert'   # movie directory

            self.__process()


    #
    # __readData
    #
    def __readData(self,dir):
        """
        Read MOI data loacted in "dir"+/.parallel/*res.*" files

        Input:
        dir  : directory whare was computed MOI

        return data_boa, data_coa
        """
        allres=sorted(glob.glob(dir+"/.parallel/*res.*"))
        data_boa=np.zeros([len(allres),21])
        data_coa=np.zeros([len(allres),21])
        #print(len(allres))
        n=0
        tot=len(allres)
        for res in (allres):
            if self.__progress:
                print(res+" %.01f%%"%((n+1)*100./tot,),file=sys.stderr,end='\r')
            f=open(res)
            f.readline() #skip time
            icut=0
            #try:
            myline=list(map(np.float,(f.readline().split())))
            #print(myline)
            lambda1=myline[10]
            lambda2=myline[11]
            lambda3=myline[12]
            data_boa[n,0]=myline[0] # time
            data_boa[n,1]=np.sqrt(lambda2/lambda1)
            data_coa[n,0]=myline[0] # time
            data_coa[n,1]=np.sqrt(lambda3/lambda1)
            n=n+1
            #except:
            #print("Bug :",myline)
            f.close()
        return data_boa,data_coa

    #
    # __plot
    #
    def __plot(self,plt,data_boa, data_coa):
        """
        plot b/a and c/a data
        Input:
        data_boa, data_coa: 2D numpy array [ntimes,2] with B over A and C over A data along time
        """

        plt.plot(data_coa[:,0],data_coa[:,1],label="c/a")
        plt.plot(data_boa[:,0],data_boa[:,1],label="b/a")
        plt.axis([0,10,0,1])
        plt.legend(loc='best')

    #
    # __process
    #
    def __process(self):
        """
        """
        #fig=plt.figure()
        # create grid
        #!!gs = gridspec.GridSpec(1, 2,wspace=0,hspace=0,width_ratios=[2,2],height_ratios=[1,1])#height_ratios=h,width_ratios=w)
        #print(gs.get_width_ratios(),gs.get_height_ratios(),gs.get_grid_positions(fig))
        #!!fig.suptitle("%s %s"%(self.__simname,self.__component))
        import os
        allres=sorted(glob.glob(self.__dir_moi+"/inertia_*"))
        # keep only directories
        allresdir=[]
        for d in allres:
            if os.path.isdir(d):
                allresdir.append(d)


        fig,axes = plt.subplots(ncols=len(allresdir),sharey=False,figsize=(12, 6))#gridspec_kw={'width_ratios': [2, 2]})
        fig.suptitle("%s %s"%(self.__simname,self.__component))

        n=0
        for res in allresdir:
            #ax = plt.subplot(gs[0,n])
            ax= axes[n]
            ax.set_xlabel("Gyears")
            dens=float(res.split("_")[1])
            ax.set_title("%.1f %% density"%(dens))
            print("Dir <%s>, density [%d]"%(res,dens),file=sys.stderr)
            data_boa,data_coa = self.__readData(res)
            self.__plot(ax,data_boa,data_coa)
            n=n+1
            print("\n",file=sys.stderr)

        if not self.__disp: # don't display on screen
            if self.__outfile is None: # save in simulation's directory
                self.__outfile = self.__dir_moi+"/"+self.__simname+".jpg"
            plt.savefig(self.__outfile)
        else :
            plt.show()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line for uns_plot_inert.py program
def commandLine():
    import argparse

    # help
    parser = argparse.ArgumentParser(description="Display Moment of Inertia results",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('simname', help="uns input simulation name",default=None)
    parser.add_argument('--component', help="selected component",default="halo")
    parser.add_argument('--ncut', help="#cuts ",default=20,type=int)
    parser.add_argument('--outfile', help="output file name",default=None)
    parser.add_argument('--nodisp', help='dont display on screen',dest="nodisp", action="store_true", default=False)
    parser.add_argument('--noprogress', help='dont display a progress bar',dest="noprogress", action="store_true", default=False)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()
    # start main function
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        pinert=CPlotInert(args.simname,component=args.component,ncut=args.ncut, progress=not args.noprogress,
                            disp=not args.nodisp,outfile=args.outfile,verbose_debug=args.verbose)
    except Exception as x :
        print (x,file=sys.stderr)
    except KeyboardInterrupt:
        sys.exit()

# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
