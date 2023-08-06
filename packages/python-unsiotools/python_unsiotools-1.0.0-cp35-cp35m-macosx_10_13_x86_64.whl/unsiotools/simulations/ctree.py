#!/usr/bin/python
from __future__ import print_function
import sys

try:
    from .. import py_unstools as ut         # import py_unstools package
except ImportError:
    print("WARNING !!!, ctree failed to import module [py_unstools]",file=sys.stderr)

import numpy as np
from . import cfalcon as cf

import unsio

# -----------------------------------------------------
#
class CTree:
    """
    methods imported from CTree C++ class
    """
    __tree=None
    # data given to constructor
    __pos=None
    __mass=None
    __vel=None
    __time=0.0
    # data computed in tree
    __tree_pos=None
    __tree_vel=None
    __tree_mass=None
    __tree_rho=None
    __tree_hsml=None
    #
    # constructor
    #
    def __init__(self,pos,vel=None,mass=None,fcells=0.9,rsize=0.4,time=0.0,seed=None):
        self.__pos=pos
        self.__mass=mass
        self.__vel=vel
        self.__time=float(time)
        # initialyse random generator number
        np.random.seed(seed)
        if (type(pos[0])==np.float32):
            self.__tree=ut.CTreeF(pos,mass,fcells,rsize)

        else: # assume 64 bits (double)
            self.__tree=ut.CTreeD(pos,mass,fcells,rsize)



    #
    # getLevels
    #
    def getLevels(self):
        """Return an numpy array with for each particles its level in the octree"""
        ok,levels=self.__tree.get_levels(self.__tree.getNbody())
        return ok,levels


    #
    # fastCod
    #
    def fastCod(self,threshold=10000):
        """
        compute cod using octree

        Argument:
        threshold > 0 : use this values as number of particles selected for computing cod
        threshold < 0 : use this |values| as a percentage of the total particles for computing cod

        Return:

        """
        from . import csnapshot as cs

        if threshold<0: # it's percentage of nbodies
            threshold = (abs(threshold)*self.__tree.getNbody())/100
        else:
            threshold = min(threshold,self.__tree.getNbody())

        #print("Threshold = ",threshold)

        ok,levels=self.getLevels()
        #idx=np.argsort(levels)
        idx=(-levels).argsort()
        print("idx=",idx.size,idx,levels[idx])

        p=np.reshape(self.__pos,(-1,3))
        p=p[idx[0:threshold],]
        #print(p.shape,p.size)
        m=self.__mass[idx[0:threshold]]

        p=np.reshape(p,(-1,))
        #print(p.shape,p.size)
        #print (p[:,])
        c=cf.CFalcon() # new falcon object
        ok,rho,hsml=c.getDensity(p,m) # compute density
        #print (ok)

        v=None
        if self.__vel is not None:
             v=np.reshape(self.__vel,(-1,3))
             v=v[idx[0:threshold],]
             v=np.reshape(v,(-1,))
        cxv=cs.CSnapshot(None).center(p,v,m*rho)

        unso=unsio.CunsOut("/home/jcl/x_x","gadget2")

        unso.setArrayF("gas","pos",p)
        unso.setArrayF("gas","mass",m)
        unso.setArrayF("gas","rho",rho)
        unso.setArrayF("gas","hsml",hsml)
        unso.save()
        return cxv[0:3]

    #
    # fastCod2
    #
    def fastCod2(self,threshold=10000):
        """
        compute cod using octree

        Argument:
        threshold > 0 : use this values as number of particles selected for computing cod
        threshold < 0 : use this |values| as a percentage of the total particles for computing cod

        Return:

        """
        from . import csnapshot as cs

        if threshold<0: # it's percentage of nbodies
            threshold = (abs(threshold)*self.__tree.getNbody())/100
        else:
            threshold = min(threshold,self.__tree.getNbody())

        #print("Threshold = ",threshold)

        ok,radius=self.__tree.get_closest_distance_to_mesh(self.__tree.getNbody())
        #idx=np.argsort(radius)
        idx=(radius).argsort()
        print("idx=",idx.size,idx,radius[idx])

        p=np.reshape(self.__pos,(-1,3))
        p=p[idx[0:threshold],]
        #print(p.shape,p.size)
        m=self.__mass[idx[0:threshold]]

        p=np.reshape(p,(-1,))
        #print(p.shape,p.size)
        #print (p[:,])
        c=cf.CFalcon() # new falcon object
        ok,rho,hsml=c.getDensity(p,m) # compute density
        #print (ok)

        v=None
        if self.__vel is not None:
             v=np.reshape(self.__vel,(-1,3))
             v=v[idx[0:threshold],]
             v=np.reshape(v,(-1,))
        cxv=cs.CSnapshot(None).center(p,v,m*rho)


        unso=unsio.CunsOut("/home/jcl/x_x","gadget2")

        unso.setArrayF("gas","pos",p)
        unso.setArrayF("gas","mass",m)
        unso.setArrayF("gas","rho",rho)
        unso.setArrayF("gas","hsml",hsml)
        unso.save()
        return cxv[0:3]

    #
    # fastCod3
    #
    def fastCod3(self,threshold=10000,outfile=None):
        """
        compute cod using octree

        Argument:
        threshold > 0 : use this values as number of particles selected for computing cod
        threshold < 0 : use this |values| as a percentage of the total particles for computing cod

        outfile : if not None save 'outfile' to NEMO format

        Return:
        cxv : COD, 1D numpy array of size 6
        rpos : positions of particles used to compute cod 1D num array
        """
        from . import csnapshot as cs

        if threshold<0: # it's percentage of nbodies
            threshold = (abs(threshold)*self.__tree.getNbody())/100
        else:
            threshold = min(threshold,self.__tree.getNbody())

        #print("Threshold = ",threshold)

        ok,levels=self.getLevels() # get octree levels for each particles

        # we randomize indexes bc simulation code save particles processor per processor
        # in kinda block structures
        shuffle=np.arange(levels.size)
        np.random.shuffle(shuffle)

        idx=(-levels[shuffle]).argsort()
        #print("idx=",idx.size,idx,levels[shuffle[idx]])

        shuffle_idx_threshold=shuffle[idx[0:threshold]] # to save some speed

        p=np.reshape(self.__pos,(-1,3)) # convert flat array to [nbody,3]
        p=p[shuffle_idx_threshold,]     # get randomized thresholded indexes for pos
        #print(p.shape,p.size)
        m=self.__mass[shuffle_idx_threshold] # get randomized thresholded indexes for mass

        p=np.reshape(p,(-1,)) # flatten pos array

        #print(p.shape,p.size)
        #print (p[:,])
        c=cf.CFalcon() # new falcon object
        ok,rho,hsml=c.getDensity(p,m) # compute density
        self.__tree_pos  = p
        self.__tree_mass = m
        self.__tree_rho  = rho
        self.__tree_hsml = hsml
        #print (ok)

        v=None
        if self.__vel is not None:
             v=np.reshape(self.__vel,(-1,3))
             v=v[shuffle_idx_threshold, ]
             v=np.reshape(v,(-1,))
             self.__tree_vel=v
        cxv=cs.CSnapshot(None).center(p,v,m*rho)


        if v is None: # no velocities
            cxv[3]=0.0
            cxv[4]=0.0
            cxv[5]=0.0
        if outfile is not None:
            unso=unsio.CunsOut(outfile,"nemo")
            unso.setValueF("time",self.__time)
            unso.setArrayF("all","pos",p)
            if self.__vel is not None:
                unso.setArrayF("all","vel",v)
            unso.setArrayF("all","mass",m)
            unso.setArrayF("all","rho",rho)
            unso.setArrayF("all","hsml",hsml)
            unso.save()
        return cxv

    #
    # getTreeDensity
    #
    def getTreeDensity(self):
        """
        return rho and hsml computed in tree
        """
        return self.__tree_rho,self.__tree_hsml

    #
    # getTreePart
    #
    def getTreePart(self):
        """
        return pos,vel and mass used to computed the tree
        """
        return self.__tree_pos,self.__tree_vel, self.__tree_mass
