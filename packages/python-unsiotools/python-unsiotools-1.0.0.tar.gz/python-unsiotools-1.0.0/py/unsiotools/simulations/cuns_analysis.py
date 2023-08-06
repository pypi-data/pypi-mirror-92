#!/usr/bin/python
from __future__ import print_function
import numpy as np
import sys
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
import matplotlib
matplotlib.use('Agg')

import time
import os
import signal

from ..uns_simu import *
from .csnapshot import *


class CUnsAnalysis:
    'Analysis pipeline'
    __sql3=None
    simname=None
    __r=None
    __slist=None # snap list
    __verbose=False
    __analysis_script=None
    __select="all"
    __nb_lock=15  # #lock files

    class CData:
        """
        store information used during analysis process
        """
        uns_snap=None    # pointer to UNS snpshot
        snap_id=None
        first=True
        lock=[]

    # constructor
    def  __init__(self,simname,script,dbname=None,verbose=False,verbose_debug=False):
        """
        simname must be a UNS simulation belonging to a uns sqlite3 database.
        infos regarding to simname simulation are loaded into privates variables
        """
        self.__vdebug=verbose_debug
        self.__dbname=dbname
        self.__analysis_script=script
        self.__verbose=verbose
        if self.__vdebug:
            print ("simname = ", simname)
        self.simname = simname
        self.__sql3 = UnsSimu(simname,dbname=self.__dbname,verbose=self.__verbose)
        self.__r = self.__sql3.getInfo() # return None if does not exist
        
        if self.__vdebug:
            self.__sql3.printInfo(simname)
        self.__slist = self.__sql3.getSnapshotList()
        if (self.__slist is None):
            message="In CLASS <"+self.__class__.__name__+"> :  Unknown simulation ["+simname+"] in UNS database..."
            raise Exception(message)
        else:
            self.__detectComponents()

        # create data analysis object
        self.__data=self.CData()


        self.__data.list_components=self.__new_select
        self.__data.simname=self.simname
        self.__data.slist=self.__slist
        self.__data.sim_info=self.__r    # unsio simulation info
        self.__data.lock=[]              # locking mechanism
        for i in range(self.__nb_lock):
            self.__data.lock.append(Lock())


    #
    # ----
    #
    # detectComponents
    def __detectComponents(self):
        """
        from list of snapshots, load half of the list and find out which
        components are presents
        """
        # get half of list of snapshot to check if all components exist
        half_snap=self.__slist[int(len(self.__slist)/2)]
        if self.__vdebug:
            print("Half snapshot =",half_snap)
        #sys.exit()
        test_snap=CSnapshot(half_snap, "all" )
        ok=test_snap.unsin.nextFrame()

        # rebuild select string with existing components
        self.__new_select=""
        whole_select="halo:disk:gas:stars:bndry"
        for colon_s in whole_select.split(":"):
            ok,data=test_snap.unsin.getData(colon_s,"pos")
            if ok:
                if len(self.__new_select)==0:
                        sep=""
                else:
                        sep=":"
                self.__new_select += sep+ colon_s
        if self.__vdebug:
            print("new select :",self.__new_select)
        test_snap.unsin.close()

    #
    # ----
    #
    # start analysis
    def compute(self,ncores=None,select="all"):
        """
        Start parallel computation on nores
        """
        # selected components
        self.__select=select

        # compute cores
        if ncores is None:
            ncores=multiprocessing.cpu_count()
        if self.__vdebug:
            print ("#cores used :",ncores)

        # Feed QUEUE with list of snapshots
        q = multiprocessing.Queue()
        n=0
        for snap in self.__slist: # loop on list os snsphots
            #print "SNAP put :",snap
            q.put("%s %d"%(snap,n)) # out a snapshot in the list + index
            n=n+1

        # start process jobs
        processes=[]  # list of processes
        n=0

        # manage signint signal
        #original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN) # IGNOROE before process creation

        # lock to control access to file
        lock=Lock()

        # loop on all #cores and start a process
        for p in range(ncores):
            p = Process(target=self.__analysisProcess, args=(q,n,lock,))  # create
            p.start()  # start
            processes.append(p) # append list of process, used for joining
            n += 1

        # wait all processes to complete
        try:
            for p in processes:
                print ("waiting.. ",p)
                p.join()
        except KeyboardInterrupt: # allow to interupt all workers with  CTRL+C
            for p in processes:
                print ("Terminating.. ",p)
                p.terminate()
                p.join()
        while not q.empty():
            q.get(block=False)

    #
    # ----
    #
    # start analysis
    def __analysisProcess(self,queue_list,n,lock):
        """
        Get a new file from list
        Load UNS snapshot
        Start analysis script
        """

        data=self.__data
        data.core_id=n # core'sid

        stop=False
        cpt=0
        first=True
        while (not stop):
            try:
                print ("Core [",n,"] waiting...")
                my_snap,idx=queue_list.get(True,0.05).split() # we must use this line
                                                              # True means bloc during 0.05 sec,
                                                              # if nothing, then get raise Queue.Empty exception
                data.snap_id=int(idx)
                #my_snap=queue_list.get()  # do not use this, could block if nothing to get
                #time.sleep(0.01)
                data.uns_snap=CSnapshot(my_snap,self.__select,verbose_debug=self.__vdebug)
                ok=data.uns_snap.unsin.nextFrame("") # load in memory
                if ok:
                    # start analysis script
                    if pyver==2:
                      execfile(self.__analysis_script)
                    else : # python3 ?
                      exec(open(self.__analysis_script).read())

                cpt+=1
                print ("Core [",n,"] got snap : ",my_snap,cpt)
            except Queue.Empty:
                stop = True # mo more data
                if self.__verbose:
                    print ("Queue.empty execption trapped...")

        print ("Core [",n,"] DONE !",cpt)

        #print "Core [",n,"] got snap : ",queue_list.get()

import argparse
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None

     # help
    parser = argparse.ArgumentParser(description="Parallel pipeline analysis program",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('script', help='Analysis script')
    parser.add_argument('--ncores', help='Use ncores, None means all',default=ncores,type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

    print ("Matplotlib backend Using:",matplotlib.get_backend(),file=sys.stderr)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        analysis=CUnsAnalysis(simname=args.simname, script=args.script,verbose_debug=args.verbose)
    except Exception as x :
        print (x)
    else:
        analysis.compute(args.ncores)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
