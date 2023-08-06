#!/usr/bin/python
from __future__ import print_function
from ..uns_simu import *
from .csnapshot import *
from .cfalcon import *
from .ctree import *

from multiprocessing import Process, Lock,Pool
import multiprocessing
try:
    # python3
    import queue as Queue
    pyver=3
except ImportError:
    # python2
    import Queue
    pyver=2

import time
import os
import signal


#
# ----
#
class CCom:
    """
    compute Center Of Mass on UNS snapshots
    """
    #
    # ----
    #
    # constructor
    __analysis=None
    def __init__(self,analysis,verbose=False,verbose_debug=False):
        """
        Constructor of CCom class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """
        self.__vdebug=verbose_debug
        self.__verbose=verbose

        if analysis is not None:
            self.__analysis=analysis
            self.__smartAnalysisInit()

    #
    # __smartAnalysis
    def __smartAnalysis(self):
        """
        This is a special method called by constructor during smart pipeline analysis
        """
        if hasattr(self.__analysis,'com'):
            print ("COM exist")
        else:
            # we go here the first time
            print ("COM does not exist")
            self.__analysis.com=True
            # then we run some initialisations
            self.__smartAnalysisInit()

    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        ### build COM Dir
        if hasattr(self.__analysis,'com_dir'):
            pass
            #
        else: # default simdir simulation
            self.__analysis.com_dir=self.__analysis.sim_info['dir']+"/ANALYSIS/com"

        print("COM DIR = ", self.__analysis.com_dir, self.__analysis.sim_info['name'])
        self.__com_file_base=self.__analysis.com_dir
        self.__analysis.com_file=self.__analysis.com_dir+"/com_all.txt"

        # lock process
        self.__analysis.lock[self.__analysis.lock_id].acquire()
        # build directory
        if (not os.path.isdir(self.__analysis.com_dir)) :
            try:
                print("Core ID ",self.__analysis.core_id," create directory [%s]\n"%(self.__analysis.com_dir))
                os.makedirs(self.__analysis.com_dir)

            except OSError:
                print("Unable to create directory [%s]\n"%(self.__analysis.com_dir))
                self.__analysis.lock[self.__analysis.lock_id].release()
                sys.exit()

        #
        if not os.path.isfile(self.__analysis.com_file):
            f=open(self.__analysis.com_file,"w")
            try:
                f.write("%s\n"%(self.__analysis.sim_info['name']))
                f.close()
            except:
                print("Unable to create file [%s], aborting"%(self.__analysis.com_file))
                self.__analysis.lock[self.__analysis.lock_id].release()
                sys.exit()

        # release process
        self.__analysis.lock[self.__analysis.lock_id].release()


    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None):
        """
        Main core function to compute COD on current snapshot store in data_analysis
        """
        if analysis is None:
            data=self.__analysis
        else:
            data=analysis


        if not hasattr(data,'com_select'):
            print("\n\nAlgo error,data_analysis structure must contain 'com_select' field, aborting...\n")
            sys.exit()

        data.com_select=data.com_select.replace(" ", "")

        self.simname = data.sim_info['name']
        #
        uns_snap=data.uns_snap
        ok,time=uns_snap.unsin.getData("time")
        if self.__vdebug:
            print(self.simname+" time [%e] "%(time))


        # read COM file
        if not hasattr(data,'com_first_new_time'):
            data.lock[data.lock_id].acquire()
            exist_time,ticxv=self.getComFromFile(data.com_file,1,time)
            data.lock[data.lock_id].release()
            if not exist_time:
                data.com_first_new_time=True
        else: # speed up searching
            if self.__vdebug:
                print("speedup COM searching....\n")
            exist_time=False

        icxv=np.zeros((6,7))
        cpt=0
        if not exist_time:
            if self.__vdebug:
                print("Time [%f] does not exist!!\n"%(time))
            for select in data.com_select.split(":"):
                #if self.__vdebug:
                #    print("COM select[%s]\n"%(select))
                icxv[cpt][0] = cpt
                ok,mass=uns_snap.unsin.getData(select,"mass")
                if mass.size==0 : # no mass
                    if self.__vdebug:
                        print("COM no mass...\n")
                    icxv[cpt][1:]=99999.
                else:
                    ok1,pos=uns_snap.unsin.getData(select,"pos")
                    ok2,vel=uns_snap.unsin.getData(select,"vel")
                    if pos.size>1 or vel.size>1 :
                        icxv[cpt][1:]=uns_snap.center(pos,vel,mass)
                cpt=cpt+1

            # save COM on disk
            data.lock[data.lock_id].acquire()
            self.saveComToFile(data.com_file,time,icxv)
            data.lock[data.lock_id].release()

    #
    # ----
    #
    def saveComToFile(self,com_file,time,icxv):
        """
        save COM record to file

        com_file : COM file name
        time     : current time to save
        icxv     : 2D numpy array, usually (6,7)
                    6 lines for components
                    7 columns ( comp's index, cx,cy,cz,cvx,cvy,cvz )
        """
        try:
            print("SAVING to com_file[%s]\n"%(com_file))
            f=open(com_file,"a")
            for n in range(icxv.shape[0]):
                f.write("%e\n"%(time))
                f.write("%d %e %e %e %e %e %e\n"%(icxv[n][0]+1,\
                                                  icxv[n][1],icxv[n][2],icxv[n][3],\
                                                  icxv[n][4],icxv[n][5],icxv[n][6]))
            f.close()
        except:
            print("\n\nUnable to save COM to file ... aborting...\n")
            sys.exit()

    #
    # ----
    #
    def getComFromFile(self, com_file,index, time,n=-1):
        """
        check if current time exist in com file
        """
        ok=False
        tcxv=[]
        if os.path.isfile(com_file):
            try:
                f=open(com_file,"r")
                simname=f.readline()
                while True:
                    tcxv=[]
                    xx=f.readline()
                    if (len(xx)>0):
                        tcxv.append( np.float64(xx))
                        tcxv.append(list(map(np.float64,(f.readline().split()))))
                        if (len(tcxv)>0):
                            atime=tcxv[0]
                            read_index=tcxv[1][0]
                            if (atime-0.001)<time and (atime+0.001)>time and (index-0.001)<read_index and (index+0.001)>read_index:
                                f.close()
                                return True,tcxv
                        else:
                            f.close()
                            return False,[]
                    else:
                        return False,[]
            except EOFError:
                pass

        return ok,tcxv
