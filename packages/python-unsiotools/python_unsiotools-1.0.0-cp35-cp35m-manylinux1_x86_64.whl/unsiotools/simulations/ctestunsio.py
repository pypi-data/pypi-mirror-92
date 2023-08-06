#!/usr/bin/env python
from __future__ import print_function

#from uns_simu import *
import os,sys
import numpy as np
import tempfile

import unsio as unsio
from csnapshot import *

import subprocess
#
# class CTestunsio
#
class CTestunsio:
    """
    This class aims to test UNSIO library
    """

    __3D       = [3,"pos","vel","acc"]
    __1D       = [1,"mass","pot"]
    __1Dgas    = [1,"rho","hsml","metal"]
    __1Dstars  = [1,"metal","age"]
    __1Dint    = [1,"id"]

    __comp = {'halo':[__1D,__3D],'gas':[__1D,__3D,__1Dgas],'stars':[__1D,__3D,__1Dstars],'disk':[__1D,__3D],'bndry':[__1D,__3D],'bulge':[__1D,__3D]}
    __compNemo = { 'all':[__1D,__3D,__1Dgas] }
# -----------------------------------------------------
# 
    def __init__(self,nbody=None,seed=666,single=True,verbose=None, uns2uns=False):
        self.__nbody   = nbody
        self.__verbose = verbose
        self.__seed    = seed
        self.__single  = single
        self.__uns2uns = uns2uns

        self.__initSeed(self.__seed)

# -----------------------------------------------------
# 
    def __initSeed(self,seed=None):
        if seed is None:
            seed=self.__seed

        np.random.seed(seed)

# -----------------------------------------------------
# 
    def __dataF(self,n):
        if (self.__single):
            x=np.float32(np.random.sample(n))
        else:
            x=np.float64(np.random.sample(n))
        return x
# -----------------------------------------------------
# 
    def __saveArray(self,comp,attr,dim,real=True):

        if real:
            data=self.__dataF(self.__nbody*dim)
            ok=self.__unso.setArrayF(comp,attr,data) # save real arrays
        else:
            ok=self.__unso.setArrayI(comp,attr,np.arange(self.__nbody*dim,dtype=np.int32)) # save real arrays

# -----------------------------------------------------
# 
    def saveModel(self,filename=None,unstype="gadget3",single=True):
        """
        save model in requested format
        """
        self.__initSeed() # reset random generator

        # create temporary file
        if filename is None:
            f = tempfile.NamedTemporaryFile()
            self.__model_file = f.name
            f.close()
        else:
            self.__model_file = filename

        fff = self.__model_file
        ## SAVE FILE
        # instantiate output object
        if (single):
            print("SINGLE precision floating values")
            self.__unso=unsio.CunsOut(self.__model_file,unstype);    # output file
        else:
            print("DOUBLE precision floating values")
            self.__unso=unsio.CunsOutD(self.__model_file,unstype);    # output file

        print("\nSaving in ",unstype," format......")
        self.__unso.setValueF("time",0)      # save time

        select_comp =  self.__comp # comp for gadget2 gadget3
        if unstype=="nemo":
            select_comp =  self.__compNemo # comp for nemo

        for comp,all_array in select_comp.iteritems():
            print ("[%-6s] : "%(comp),file=sys.stderr,end="")
            # save reals array
            for block_array in all_array:
                dim=block_array[0]
                for array in block_array[1:]:
                    print(" %s"%(array), end="")
                    self.__saveArray(comp,array,dim,real=True)  # save real 

            # save integer arrays
            dim=self.__1Dint[0]
            for array in self.__1Dint[1:]:
                print(" %s"%(array), end="")
                self.__saveArray(comp,array,dim,real=False) # save integer

            print("\n")

        self.__unso.save() # trigger save ops
        self.__unso.close()

        if self.__uns2uns : # test uns2uns
            ff = tempfile.NamedTemporaryFile()
            myfile = ff.name
            ff.close()
            
            if single:
                outfloat="float=t"
            else:
                outfloat="float=f"
            cmd="uns2uns in=%s out=%s select=%s type=%s %s"%(self.__model_file,myfile,"all",unstype,outfloat)
            print("<%s>"%(cmd),file=sys.stderr)
            #subprocess.call([cmd],shell=True)
            subprocess.call(["uns2uns","in="+self.__model_file,"out="+myfile,"select=all","type="+unstype,outfloat])

            #sys.exit()
            os.remove(self.__model_file)
            self.__model_file=myfile
        
        print("Outfile = [%s]"%(self.__model_file))

# -----------------------------------------------------
# 
    def __compareArray(self,comp,attr,dim,real=True):

        if real:# float
            data_ref=self.__dataF(self.__nbody*dim)
        else: #integer
            data_ref=np.arange(self.__nbody,dtype=np.int32)


        ok,data=self.__unsi.getData(comp,attr)
        #print("%f "%(data_ref[0]),end="",file=sys.stderr)
        if ok:
            #print ("Checking comp[%s] attribute [%s] size [%d] "%(comp,attr,data.size),type(data),data,file=sys.stderr)
            #print (" <%s>"%(attr),file=sys.stderr,end="")
            ok=(data_ref==data).all()
            if not ok:
                print("\nInconsitency:  <%s> [%s]"%(comp,attr),data_ref.size,data.size,file=sys.stderr)
                print(data_ref,data)
                sys.exit()

# -----------------------------------------------------
# 
    def __compareModel(self,unstype="gadget3",single=True):
        """
        load model from disk and compare with generated values
        """
        self.__initSeed() # reset random generator
        
        if not os.path.isfile(self.__model_file):
            print("File [%s] does not exist, aborting..\n"%(self.__model_file),file=sys.stderr)
            sys.exit()

        # instantiate CSnapshot object
        self.__unsi=CSnapshot(self.__model_file,float32=single)
        self.__unsi.nextFrame() # load snaphot

        select_comp =  self.__comp # comp for gadget2 gadget3
        if unstype=="nemo":
            select_comp =  self.__compNemo # comp for nemo

        for comp,all_array in select_comp.iteritems():
            print ("checking [%-6s] : "%(comp),file=sys.stderr,end="")
            # compare real array
            for block_array in all_array:
                dim=block_array[0]
                for array in block_array[1:]:
                    print(" %s"%(array), end="")
                    self.__compareArray(comp,array,dim,real=True)

            # compare integer arrays
            dim=self.__1Dint[0]
            for array in self.__1Dint[1:]:
                print(" %s"%(array), end="")
                self.__compareArray(comp,array,dim,real=False)

            print("\n")

        self.__unsi.close()

# -----------------------------------------------------
# 
    def testIO(self):
        """
        test models snasphot that unsio knows howto dump on a file
        """

        model=["gadget3","gadget2","nemo"]
        for mm in model:
            print ("Testing model [%s]"%(mm),file=sys.stderr)
            self.saveModel(unstype=mm,single=self.__single)
            print ("\n\nComparing model [%s]"%(mm),file=sys.stderr)
            self.__compareModel(unstype=mm,single=self.__single)
            # remove temporary file
            os.remove(self.__model_file)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse
     # help
    parser = argparse.ArgumentParser(description="Test UNSIO library",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('--nbody', help='#bodies to test', type=int, default=100000)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)
    parser.add_argument('--double',help='test with double real',dest="double", action="store_true", default=False)
    parser.add_argument('--uns2uns',help='save intermediate file with uns2uns',dest="uns2uns", action="store_true", default=False)
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def process(args):
    uns=CTestunsio(nbody=args.nbody,single=not args.double, uns2uns=args.uns2uns)
    #uns.saveModel("")
    uns.testIO()


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()

