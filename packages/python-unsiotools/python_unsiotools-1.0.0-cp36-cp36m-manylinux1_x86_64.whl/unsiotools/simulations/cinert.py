#!/usr/bin/python
from __future__ import print_function
from .ctree import *
from .csnapshot import *
from ..uns_simu import *
from .ccod import *
from .cfalcon import *

import time
import os,sys
import numpy as np
import math
import time
import numpy.linalg as linalg
#from IPython import embed

#
# ----
#
class CInert:
    """
    Compute moment of Inertia
    """
    #
    # ----
    #
    # constructor
    __analysis=None
    __res_file_name=None
    __res_fdesc=None
    __inert_dir="./"
    __outfile_main=None
    __snapshot=None
    __outfile=None
    __ncut=None
    __fract_min=None
    __fract_max=None
    __com=None
    __component=None
    __center_file=None

    def __init__(self,analysis=None,snapshot=None,outfile=None,ncut=10, fract_min=0.1,fract_max=0.9,
                 com=True,component=None,center_file=None,tree_density=True,tree_threshold=-10., nonemo=False,
                 verbose=False,verbose_debug=False):
        """
        Constructor of CInert class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """

        self.__vdebug=verbose_debug
        self.__verbose=verbose

        self.__snapshot=snapshot
        self.__outfile=outfile
        self.__ncut=ncut
        self.__fract_min=fract_min
        self.__fract_max=fract_max
        self.__com=com
        self.__component=component
        self.__center_file=center_file
        self.__nonemo=nonemo
        print("SELF_NONEMO = ",self.__nonemo)

        self.__tree_density   = tree_density
        self.__tree_threshold = tree_threshold
        if analysis is None and snapshot is None:
            #import inspect
            raise Exception(__file__+": Error, analysis and snapshot are both None..")

        if analysis is not None:
            self.__analysis=analysis
            self.__smartAnalysisInit()
        else: # standalone (full process)
            # open file
            self.__res_fdesc = self.__buildRes(outfile,snapshot)

    #
    # smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        data=self.__analysis

        ### build INERT Dir
        if hasattr(data,'inert_dir'):
            self.__inert_dir=data.inert_dir
            #
        else: # default simdir simulation
            self.__inert_dir=data.sim_info['dir']+"/ANALYSIS/inert"

        print("INERT DIR = ", self.__inert_dir, data.sim_info['name'])
        self.simname=data.sim_info['name']
        #self.__com_file_base=self.__inert_dir

        # lock process
        data.lock[data.lock_id].acquire()
        # outfile
        self.__outfile_main = self.simname+"_inertN_"+self.__component+".res"
        self.__outfile_head = self.__inert_dir+"/HEAD_"+self.__outfile_main

        # build directory
        if (not os.path.isdir(self.__inert_dir) or not os.path.exists(self.__outfile_head)) :
            try:
                print("Core ID ",data.core_id," create directory [%s]\n"%(self.__inert_dir))
                os.makedirs(self.__inert_dir)
                os.makedirs(self.__inert_dir+"/.parallel")

                # save HEAD
                try:
                    print("Saving header [%s]\n"%(self.__outfile_head ),file=sys.stderr)
                    f=open(self.__outfile_head,"w")
                    f.write("%s\n%d\n"%(self.simname,self.__ncut))
                    f.close()
                except:
                    print("\n\nUnable to save inert_file[%s] ... aborting...\n"%(self.__outfile_head),file=sys.stderr)
                    sys.exit()

            except OSError:
                print("Unable to create directory [%s]\n"%(self.__inert_dir))
                data.lock[data.lock_id].release()
                sys.exit()

        # release process
        data.lock[data.lock_id].release()


    #
    #
    #
    def __buildRes(self,outfile,simname):
        """
        build outfile name

        Return :
        file descriptor
        """
        if outfile is None:
            self.__res_filen_name=simname+"_inertN_"+self.__component+".res"
        else:
            self.__res_filen_name=outfile

        try:
            self.__fdesc=open(self.__res_filen_name,"w")
        except :#IOError :
            print("Unable to open file [%s]\n"%(self.__res_filen_name),file=sys.stderr)
            sys.exit()
        return self.__fdesc

    #
    #
    #
    def fullProcess(self,snapshot,component):
        """
        Run full process on input snapshot
        """
        class CData:
            uns_snap=None
            single_proc=True
            first=True
            lock=[Lock()]
            lock_id=0

        analysis = CData() # instantiate CData object to mimic online analysis


        self.__analysis=analysis

        self.__fdesc.write("%s\n%d\n"%(snapshot,self.__ncut)) # save header

        # instantiate CSnapshot
        uns=CSnapshot(snapshot,component,verbose_debug=self.__vdebug)
        # fill up analysis object
        analysis.uns_snap=uns

        # loop on snapshots
        n = 0
        while(uns.unsin.nextFrame("")):
            analysis.snap_id = n
            self.smartAnalysis(analysis)
            n = n + 1

        # close outfile
        self.__fdesc.close()


    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None):
        """
        Main core function to compute INERT  on current snapshot stored in data_analysis
        """
        if analysis is None:
            data=self.__analysis
        else:
            data=analysis
        t0 = time.clock()
        uns_snap=data.uns_snap # link to UNS object

        ok,self.__time=uns_snap.unsin.getData("time")
        print("Time =",self.__time)

        t_file=self.__inert_dir+"/.time_completed"

        if not self.__checkTimeExist(self.__time,t_file): # time not computed yet

            self.__openOutFile() # open file

            self.__fdesc.write("%e\n"%(self.__time)) # save time

            # read data
            ok,pos  = uns_snap.unsin.getData(self.__component,"pos")
            if not ok:
                raise Exception("No Positions particles for component <%s>...\n"%(self.__component))
            ok,mass = uns_snap.unsin.getData(self.__component,"mass")
            if not ok:
                raise Exception("No Masses particles for component <%s>...\n"%(self.__component))

            if self.__vdebug:
                print("1:",pos)
            # centering
            ok=uns_snap.centerOnFile(pos,None,mass,self.__com,self.__component,self.__center_file,data)
            if self.__vdebug:
                print("2:",pos,ok)

            # compute density
            t00=time.clock()
            if self.__tree_density:
                ctree=CTree(pos,None,mass)  # instantiate a ctree object

                cxv=ctree.fastCod3(self.__tree_threshold)
                rho,hsml=ctree.getTreeDensity()
                pos,vel,mass=ctree.getTreePart()
            else : # full density
                c=CFalcon() # new falcon object
                ok,rho,hsml=c.getDensity(pos,mass) # compute density
                pos=pos
                mass=mass
            print("Computing density : %.02f"%(time.clock()-t00),file=sys.stderr)

            #embed()

            pos=np.reshape(pos,(-1,3))        # pos reshaped in a 2D array [nbody,3]
            #radius=np.sqrt(pos[:,0]*pos[:,0]+pos[:,1]*pos[:,1]+pos[:,2]*pos[:,2])  # compute particles radius
            #rs = radius.argsort() # sort particles according their radius

            sort_rho=(-rho).argsort() # sort according to higher density

            nreal   = pos.size/3 # number total particles
            npart   = (self.__fract_max-self.__fract_min)*nreal #   min<#particles<max
            iinf    = nreal*self.__fract_min
            offset  = iinf
            imax    = nreal*self.__fract_max-1
            step    = npart/self.__ncut   # #particles/step

            print("range = <%d> [%d:%d] %d\n"%(nreal,iinf,imax,step))

            # CALL SNAPINERT from iinf:imax
            #
            #
            ppos = pos [sort_rho[iinf:imax+1] , : ]
            pmass= mass[sort_rho[iinf:imax+1]     ]
            #embed()
            mofi,U,s,rot = self.momentInertia(ppos,pmass)

            # save on file
            #self.__fdesc.write("%f "%(self.__time))
            if not self.__nonemo:
                self.__saveData(mofi,U,s,rot)

            stop=False
            cpt=0
            tot=step  # #particles cutted

            sup = step
            while not stop:
                ifirst = iinf+step*cpt
                ilast  = ifirst+step-1

                if ilast>imax or cpt>self.__ncut:
                    stop=True
                    ilast=imax

                if ifirst< imax:
                    ppos =pos [sort_rho[ifirst:ilast+1] , : ]
                    pmass=mass[sort_rho[ifirst:ilast+1]     ]
                    radius=np.sqrt(ppos[:,0]*ppos[:,0]+ppos[:,1]*ppos[:,1]+ppos[:,2]*ppos[:,2])  # compute particles radius
                    rs=radius.argsort()
                    print("<%07d,%07d> radius [%f,%f]"%(ifirst,ilast,
                                                        radius[rs[0]],
                                                        radius[rs[-1]]),
                                                        file=sys.stderr)

                    #embed()
                    mofi,U,s,rot = self.momentInertia(ppos,pmass)

                    # save on file
                    self.__fdesc.write("%d %d\n"%(ifirst,ilast))
                    if not self.__nonemo:
                        self.__saveData(mofi,U,s,rot)
                #
                cpt=cpt+1

            self.__closeOutFile() # close file
            self.__saveNewTime(self.__time,t_file) # save new time in ".time_completed" file
        else:
            print("INERT: skip time[%.3f] from <%s>\n"%(self.__time,t_file))


    #
    # Inertia
    #
    def momentInertia(self,pos,weight):
        """
        compute Inertia moment based on
        https://scipython.com/blog/the-moment-of-inertia-of-a-random-flight-polymer/
        """

        # Calculate the moment of interia tensor
        mofi = np.empty((3,3))
        x, y, z = pos[:,0], pos[:,1], pos[:,2]

        nemo=not self.__nonemo

        if not nemo:
            print("not Nemo method")
            Ixx = np.sum((y**2 + z**2)*weight)
            Iyy = np.sum((x**2 + z**2)*weight)
            Izz = np.sum((x**2 + y**2)*weight)
            Ixy = -np.sum(x * y * weight)
            Iyz = -np.sum(y * z * weight)
            Ixz = -np.sum(x * z * weight)
        else:  # NEMO version based on snapinert
            # modification regarding to snapinert.c   cf NEMO package
            print("Nemo method")
            Ixx = np.sum(x * x * weight)
            Iyy = np.sum(y * y * weight)
            Izz = np.sum(z * z * weight)
            Ixy = np.sum(x * y * weight)
            Iyz = np.sum(y * z * weight)
            Ixz = np.sum(x * z * weight)


        if nemo:
            p_weight=np.sum(weight) # pos.size/3.
        else:
            p_weight=1.0

        if self.__vdebug:
            print("p_weight =",p_weight)


        mofi = np.array(((Ixx/p_weight, Ixy/p_weight, Ixz/p_weight),
                         (Ixy/p_weight, Iyy/p_weight, Iyz/p_weight),
                         (Ixz/p_weight, Iyz/p_weight, Izz/p_weight)))

        if self.__vdebug:
            print("Inertia matrix:\n",mofi)

        if nemo:
            U, s, rot = linalg.svd(mofi)

            if self.__vdebug:
                print ("U=",U)
                print ("s=",s)
                print ("rot=",rot)
                print ("s[1]/s[0]=",np.sqrt(s[1]/s[0]))
                print ("s[2]/s[0]=",np.sqrt(s[2]/s[0]))

            return mofi,U,s,rot

        else : # nonemo (based on uns_shaperadius
            eval,evec = linalg.eig(mofi)
            idx=eval.argsort()[::]
            eval=eval[idx]
            evec=evec[:,idx]
            print("Sorted")
            print("eval =",eval)
            print("evec =",evec)
            hx=eval[0]
            hy=eval[1]
            hz=eval[2]
            print("b/a=",np.sqrt((hx-hy+hz)/(-hx+hy+hz)))
            print("c/a=",np.sqrt((hx+hy-hz)/(-hx+hy+hz)))
            return 0,0,0,0


#            ,mofi[1,:],mofi[2,:])





    #
    # save data
    #
    def __saveData(self,mofi,U,s,rot):

        data=self.__analysis

        # display on screen
        if self.__vdebug:
            print(self.__time,end="    ")
            self.__fdesc.write("%f "%(self.__time))
        for ii in range(0,3): # Ixx Ixy Ixz
            if self.__vdebug:
                print(mofi[0,ii],end="    ")
            self.__fdesc.write("%f "%(mofi[0,ii]))

        for ii in range(0,3): # Ixy Iyy Iyz
            if self.__vdebug:
                print(mofi[1,ii],end="    ")
            self.__fdesc.write("%f "%(mofi[1,ii]))

        for ii in range(0,3): # Ixz Iyz Izz
            if self.__vdebug:
                print(mofi[2,ii],end="    ")
            self.__fdesc.write("%f "%(mofi[2,ii]))

        for ii in range(0,3): # s[0] s[1] s[2]
            if self.__vdebug:
                print(s[ii],end="    ")
            self.__fdesc.write("%f "%(s[ii]))

        for ii in range(0,3): # -rot[0.:]
            if self.__vdebug:
                print(rot[0,ii],end="    ")
            self.__fdesc.write("%f "%(-rot[0,ii]))

        for ii in range(0,3): # rot[1,:]
            if self.__vdebug:
                print(rot[1,ii],end="    ")
            self.__fdesc.write("%f "%(rot[1,ii]))

        for ii in range(0,3): # rot[2.:]
            if self.__vdebug:
                print(rot[2,ii],end="    ")
            self.__fdesc.write("%f "%(rot[2,ii]))

        print("\n")
        self.__fdesc.write("\n")




    #
    # __openOutFile
    #
    def __openOutFile(self):
        """
        """
        if hasattr(self.__analysis,"single_proc"): # full process analysis, file already open
            return
        else: # parallel analysis
            #print(">>",self.__inert_dir)
            #print(">>",self.__outfile_main)
            #print(">>",self.__analysis.snap_id)
            outfile= self.__inert_dir+"/.parallel/"+self.__outfile_main+".%05d"%(self.__analysis.snap_id)
            self.__buildRes(outfile,self.simname)
    #
    # __closeOutFile
    #
    def __closeOutFile(self):
        """
        """
        if hasattr(self.__analysis,"single_proc"): # full process analysis, file already open
            return
        else: # parallel analysis
            self.__fdesc.close()

    #
    # __saveNewTime
    #
    def __saveNewTime(self,time,t_file):
        """
        write in t_file a new time completed

        *IN*
        time    : current time
        t_file  : filename

        """
        # lock process
        self.__analysis.lock[self.__analysis.lock_id].acquire()
        if self.__vdebug:
            print("Saving a new INERT time[%.3f] in <%s>\n"%(time,t_file))
        try:
            f=open(t_file,"a")
            f.write("%f\n"%(time))
            f.close()
        except:
            print("\n\nUnable to save time[%.3f] in <%s>, aborting....\n"%(time,t_file))
            sys.exit()
        # release process
        self.__analysis.lock[self.__analysis.lock_id].release()

    #
    # __checkTimeExist
    #
    def __checkTimeExist(self,time,t_file):
        """
        check in t_file, if time has been already computed

        *IN*
        time    : current time
        t_file  : file with time value

        *OUT*
        boolean : True if time exist, False otherwise

        """
        if os.path.isfile(t_file):
            try:
                f=open(t_file,"r")
                while True:
                    atime=list(map(np.float,(f.readline().split())))
                    if (len(atime)>0):
                        if (atime[0]-0.001)<time and (atime[0]+0.001)>time:
                            f.close()
                            return True
                    else:
                        f.close()
                        return False

            except EOFError:
                pass
        else:
            if self.__vdebug:
                print("FILE <%s> does not exist...\n"%(t_file))

        return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():

    import argparse

    # help
    parser = argparse.ArgumentParser(description="Compute Moment of Inertia on UNS simulation",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('snapshot', help="uns input snapshot",default=None)
    parser.add_argument('component', help="selected component",default=None)
    parser.add_argument('--outfile', help="output file name",default=None)
    parser.add_argument('--ncut', help="#cuts ",default=20,type=int)
    parser.add_argument('--fmin', help="fract min ",default=0.1,type=float)
    parser.add_argument('--fmax', help="fract max ",default=0.9,type=float)
    parser.add_argument('--tree_threshold', help=">0 #particles, <0 percentage of particles ",default=-10.,type=float)
    parser.add_argument('--notree_density',help='don''t use tree density',dest="notree", action="store_true", default=False)
    parser.add_argument('--cod', help="use COD file to re-center, or @sim (ex; @mdf648) to get file automatically from simulation ",default=None)
    parser.add_argument('--nocom', help='dont use com if no COD file requested',dest="nocom", action="store_true", default=False)
    parser.add_argument('--nonemo', help='dont use Nemo algorithms (based on snapinert)',dest="nonemo", action="store_true", default=False)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()
    # start main function
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    import unsiotools.simulations.cinert as cinert
    try:
        # instantiate CInert object
        inert=cinert.CInert(snapshot=args.snapshot,outfile=args.outfile,ncut=args.ncut,
                            component=args.component,center_file=args.cod,
                            fract_min=args.fmin,fract_max=args.fmax,com=not args.nocom,
                            verbose_debug=args.verbose,
                            tree_density=not args.notree,tree_threshold=args.tree_threshold,nonemo=args.nonemo)
        # start full process
        inert.fullProcess(args.snapshot,args.component)

    except Exception as x :
        print (x,file=sys.stderr)
    except KeyboardInterrupt:
        sys.exit()


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
