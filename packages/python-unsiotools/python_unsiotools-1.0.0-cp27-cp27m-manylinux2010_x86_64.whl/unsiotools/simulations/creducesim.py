#!/usr/bin/env python
from __future__ import print_function

from ..uns_simu import *
import os,sys,subprocess

#
# class CReducesim
#
class CReducesim:
    """
    This class aims to reduce the size of an UNS simulation, by removing halo components on
    """
    __simu=None
    __info=None
    __verbose=False
    __loaded=False
    __test=False
    simname=None
    select=None

    def __init__(self,simname,keep,overwrite,dir=None,test=True,dbname=None,verbose=False,verbose_debug=False):

        self.simname=simname
        self.__keep=keep
        self.__overwrite=overwrite
        self.__dir=dir
        self.__verbose=verbose
        self.__verbose_debug=verbose_debug
        self.__test=test

        try:
            self.__simu=UnsSimu(simname,verbose=verbose)
        except Exception as x :
            raise Exception(x.message)

        self.__info=self.__simu.getInfo() # get simulation info
        self.__simname=self.__info["name"]
        self.__simtype=(self.__info["dir"]).split("/")[2]
        self.__list=self.__simu.getSnapshotList()

        # get real path even if there is a link
        # remove /net/direct in case mounted
        realpath=(os.path.realpath(self.__list[0])).replace("/net/direct","")
        print("Real Path [%s]"%(realpath),file=sys.stderr)

        if self.__dir is None:
            # get file system root
            inrootdir=realpath.split("/")[1]
            print("inrootdir = [%s] <%s>"%(inrootdir,self.__simtype),file=sys.stderr)
            self.__dir="/"+inrootdir+"/"+self.__simtype+"2/"+self.__simname+"/SNAPS"
            print("target dir <%s>"%(self.__dir),file=sys.stderr)

        # check dir
        if not os.path.isdir(self.__dir):
            print("Create directory [%s]"%(self.__dir),file=sys.stderr)
            try:
                if not self.__test:
                    os.makedirs(self.__dir)
            except :
                print("Unable to create directory [%s]"%(self.__dir))
                raise Exception("Unable to create directory [%s]"%(self.__dir))

#
# resizeSim
#
    def resizeSim(self):
        """
        resize simulation by removing halo  component every list_snapshots%keep!=1
        uns2uns process is called during this operation
        """
        if self.__simu is None:
            raise Exception("No simulation instantiated....")

        cpt=1
        for snap in self.__list:
            print(snap,file=sys.stderr)

            if cpt%self.__keep == 1:
                select="all"
            else:
                select="gas,stars,disk,bndry,bulge"

            basename=os.path.basename(snap) # input
            newsnap=self.__dir+"/"+basename   # output
            # check output file
            if not os.path.isfile(newsnap) or self.__overwrite:
                cmd="uns2uns %s %s select=%s type=gadget3"%(snap,newsnap,select)
                print("%s"%(cmd),file=sys.stdout)
                if not self.__test:
                    subprocess.call(["uns2uns",snap,newsnap,"select="+select,"type=gadget3"])

            cpt+=1

# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        simu=CReducesim(simname=args.simname,keep=args.keep,overwrite=args.overwrite,dir=args.dir,test=args.test,verbose=args.verbose)
    except Exception as x :
        print (x.message)
    else:
        simu.resizeSim()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse
    dbname=None

     # help
    parser = argparse.ArgumentParser(description="Remove halo from a simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='UNS Simulation name')
    parser.add_argument('--dir', help='directory to store new files',default=None)
    parser.add_argument('--keep', help='keep halo every frequency',default=10,type=int)
    parser.add_argument('--overwrite',help='overwrite new frame if present', dest="overwrite", action="store_true", default=False)
    parser.add_argument('--test',help='test without doing anything', dest="test",action="store_true", default=False)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
