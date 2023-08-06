#!/usr/bin/python
from __future__ import print_function
from .ctree import *
from .csnapshot import *
from ..uns_simu import *
from . import ccod as cod

import time
import os,sys
import numpy as np
import math
import time

#from IPython import embed

#
# ----
#
class COrbits:
    """
    Compute quantities on orbits
    """
    #
    # ----
    #
    __uns=None
    def __init__(self,analysis=None,snapshot=None,sname=None,
                 component="disk",verbose=False,verbose_debug=False):

        # instantiate CSnapshot
        #self.__uns=CSnapshot(snapshot,component,verbose_debug=self.__vdebug)
        pass

    #
    # ----
    #
    def computeDistance(self,snapshot,component,outfile,codfile):

        snap=CSnapshot(snapshot,component)
        ok = snap.nextFrame("")
        if ok:
            ok1,pos=snap.getData(component,"pos")
            ok2,id=snap.getData(component,"id")
            ok3,tps=snap.getData("time")

            if ok1 and ok2 and ok3 :
                ok,tcxv=cod.CCod(None).getCodFromFile(codfile,tps)
                if ok :
                    x=pos[0::3]
                    y=pos[1::3]
                    z=pos[2::3]

                    d1=np.sqrt((x-tcxv[1])**2+(y-tcxv[2])**2)
                    d2=np.sqrt((x-tcxv[1])**2+(y-tcxv[2])**2+(z-tcxv[3])**2)
                    d3=np.sqrt((x-tcxv[1])**2+(z-tcxv[3])**2)
                    d4=np.sqrt((y-tcxv[2])**2+(z-tcxv[3])**2)
                    xc=np.abs(x-tcxv[1])
                    yc=np.abs(x-tcxv[2])
                    zc=np.abs(x-tcxv[3])

                    # time array
                    ta=np.zeros(1)
                    ta=tps
                    np.save(outfile+"_data",np.column_stack((id,d1,d2,d3,d4,xc,yc,zc)))
                    np.save(outfile+"_time",ta)
                else:
                    print("No cod at time [%f]"%(tps),file=sys.stderr)

            else :
                print("Unable to read all the arrays...",ok1,ok2,ok3,file=sys.stderr)
            pass
        else :
            print("snap.nextFrame() failed....\n",file=sys.stderr)
