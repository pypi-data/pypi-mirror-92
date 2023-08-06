#!/usr/bin/python
from __future__ import print_function

import numpy as np
import sys
try:
    from .. import py_unstools
except ImportError:
    print("WARNING !!!, falcon failed to import module [py_unstools]",file=sys.stderr)



class CFalcon:
    """
    methods imported from FalcON engine
    see help on:
    - getGravity
    - getDensity
    """
    def __init__(self):
        #print ("simname = ", simname)
        pass

    def getGravity(self,pos,mass,eps,G=1.0,theta=0.6,kernel_type=1,ncrit=6):
        """
        Compute acceleration and potential using falcON algorithm (see https://iopscience.iop.org/article/10.1086/312724/pdf)

        Arguments:
        pos         : float32 one dimension numpy array ( nbody x 3 )
        mass        : float32 one dimension numpy array ( nbody     )
        eps         : softening value
        G           : gravitationnal constant Value
        theta       : opening angle
        kernel_type : kernel type
        ncrit       : #bodies separation criteria

        Return : ok,acc,phi

        ok          : boolean True if success
        acc         : float32 one dimension numpy array (nbody x 3) with acceleration values
        phi         : float32 one dimension numpy array (nbody    ) with potential values

        """
        # init returns array
        acc = np.zeros(pos.size,'f')   # acc is 3D !!
        phi = np.zeros(mass.size,'f')
        # compute gravity
        falcon=py_unstools.cfalcon()
        ok=falcon.compute_gravity(pos,mass,acc,phi,eps,G,theta,kernel_type,ncrit)
        return ok,acc,phi

    def getDensity(self,pos,mass,K=32,N=1,method=0,ncrit=None):
        """
        Compute density using falcON algorithm (see https://iopscience.iop.org/article/10.1086/312724/pdf)

        Arguments:
        pos         : float32 one dimension numpy array ( nbody x 3 )
        mass        : float32 one dimension numpy array ( nbody     )
        K           : #neighnours (default 32)
        N           : order of Ferrers's kernel
        method      : 0 based on hackdens, 1 on ferrers (default 0)
        ncrit       : #bodies separation criteria (default max(1,K/4))

        Return : ok,rho,hsml

        ok          : boolean True if success
        rho         : float32 one dimension numpy array (nbody) with density values
        hsml        : float32 one dimension numpy array (nbody) with distance of Kth neighnour

        """
        if (ncrit==None):
            ncrit=int(max(1,K/4))

        # init returns arrays
        rho=np.zeros(mass.size,'f')
        hsml=np.zeros(mass.size,'f')
        # compute density
        falcon=py_unstools.cfalcon()
        ok=falcon.compute_density(pos,mass,rho,hsml,method,K,N,ncrit)
        return ok,rho,hsml
