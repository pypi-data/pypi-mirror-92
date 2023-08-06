#!/usr/bin/python
from __future__ import print_function
from ..uns_simu import *
from .csnapshot import *
import sys

try:
    from .. import py_unstools # rectify swig
except ImportError:
    print("WARNING crectify failed to import module [py_unstools]",file=sys.stderr)

from multiprocessing import Lock
import time
import os
import glob
#from IPython import embed

#
# ----
#
class CRectify:
    """
    Rectify UNS snapshots
    """
    __analysis=None
    __use_rho=False
    __dmin=0.
    __dmax=100.
    #
    # ----
    #
    # constructor
    def __init__(self,analysis=None,use_rho=False,dmin=0.,dmax=100.,verbose=False,verbose_debug=False):
        """
        Constructor of CRectify class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """
        self.__vdebug=verbose_debug
        self.__verbose=verbose
        self.__use_rho=use_rho
        self.__dmin=dmin
        self.__dmax=dmax

        if analysis is not None:
            self.__analysis=analysis
            self.__smartAnalysisInit()

    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        data=self.__analysis

        if not hasattr(data,'rectify_select'):
            print("\n\nYou must set a fied [rectify_select] in your <data> object, aborting...\n\n")
            sys.exit()

        data.rectify_select=data.rectify_select.replace(" ","") # remove blank

        ### build CRECT Dir
        if hasattr(data,'rectify_dir'):
            self.__rectify_dir=data.rectify_dir
            #
        else: # default simdir simulation
            self.__rectify_dir=data.sim_info['dir']+"/ANALYSIS/rectify"

        print("RECTIFY DIR = ", self.__rectify_dir, data.sim_info['name'])
        self.simname=data.sim_info['name']
        #self.__com_file_base=self.__rectify_dir

        # lock process
        data.lock[data.lock_id].acquire()
        # build directory
        if (not os.path.isdir(self.__rectify_dir)) :
            try:
                print("Core ID ",data.core_id," create directory [%s]\n"%(self.__rectify_dir))
                os.makedirs(self.__rectify_dir)

            except OSError:
                print("Unable to create directory [%s]\n"%(self.__rectify_dir))
                data.lock[data.lock_id].release()
                sys.exit()

        # release process
        data.lock[data.lock_id].release()

        # check components vs cod
        ### COD Dir name
        if hasattr(data,'cod_dir'):
            pass
            #
        else: # default simdir simulation
            data.cod_dir=data.sim_info['dir']+"/ANALYSIS/cod"
            #data.cod_dir=data.sim_info['dir']+"/ANALYSIS"+self.__COD_DIR_NAME

        self.__cod_base_dir=data.cod_dir

        self.comp_cod=[] # list to store combo : component/cod to apply rectify

        ### re build select component variable according to components existing at mid
        ### simulation time (pre-computed by cuns_analysis.py and set to data.list_components
        self.__new_select=""
        for colon_s in data.rectify_select.split(":"): # colon separate analysis

            comp_L,cod_R=colon_s.split("#")    # hashtag separate comp_Left from cod_Right
            cod_R=cod_R.split("@")
            if len(cod_R)>1:
                rcut=float(cod_R[1])
                codf=cod_R[0]
            else:
                rcut=50.
                codf=cod_R[0]

            # check components exist?
            ok=True
            for comma_s in comp_L.split(","):
                xx=data.list_components.find(comma_s)  # find if selection exist
                if xx==-1:
                    ok=False
                    print("Rectify#Warning : In combo [%s], component <%s> from select <%s> does not exist...\n"\
                          %(colon_s,comma_s,comp_L))
                    break
            # components are ok, check cod file
            if ok:
                cod_file=self.__cod_base_dir+"/"+self.simname+"."+codf+".cod"
                if (os.path.exists(cod_file)):
                    ok=True
                else:
                    ok=False
                    print("Rectify#Warning : In combo [%s], COD <%s> does not exist...\n"\
                          %(colon_s,cod_file))
            # both comp_L and cod_r exist, build combo
            if ok:
                self.comp_cod.append([comp_L,codf,cod_file,rcut])


        if self.__vdebug:
            for comp_cod in self.comp_cod:
                print("Rectify combo: <%s> with [%s]\n"%(comp_cod[0],comp_cod[2]))

    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None):
        """
        Main core function to compute RECTIFY on current snapshot stored in data_analysis
        """
        if analysis is None:
            data=self.__analysis
        else:
            data=analysis

        uns_snap=data.uns_snap # link to UNS object
        ok,time=uns_snap.unsin.getData("time")

        c=py_unstools.CRectify()

        # loop on combo comp/cod
        for comp_cod in self.comp_cod:
            select   = comp_cod[0]
            cod_sel  = comp_cod[1]
            cod_file = comp_cod[2]
            rcut     = comp_cod[3]
            print("select %s cod_sel %s cod_file %s rcut %s"%(select,cod_sel,cod_file,rcut))
            # pre computed rectify file
            pre_rect_file=self.__rectify_dir+"/"+self.simname+"."+select+"-"+cod_sel+".ev"
            print("rect_file =",pre_rect_file)

            # lock file
            #data.lock[data.lock_id].acquire()
            exist_time,e_vectors=self.__checkTimeInPreRect(time,pre_rect_file)
            print("exist_time =",exist_time)
            #data.lock[data.lock_id].release()

            if not exist_time :
                ok1,pos  = uns_snap.unsin.getData(select,"pos" )
                ok2,vel  = uns_snap.unsin.getData(select,"vel" )
                ok3,mass = uns_snap.unsin.getData(select,"mass")
                ok4,rho = uns_snap.unsin.getData(select,"rho")
                #print("ok1 ok2 ok3 ",ok1,ok2,ok3)
                if pos.size>1 and vel.size>1 and mass.size>1 :
                    if self.__vdebug:
                        print("Rectifing time (%f) select <%s> cod[%s]\n"%(time,select,cod_file))
                    try:
                        print(self.__use_rho,self.__dmin, self.__dmax)
                        ok,eigen_v=c.computeEigenVectors(pos,vel,mass,rho,16,time,self.__use_rho,False,str(cod_file),rcut,self.__dmin, self.__dmax)
                        print("Time [%f] eigen:\n"%(time),eigen_v)
                        data.lock[data.lock_id].acquire()
                        self.__saveEigenVectors(pre_rect_file,eigen_v)
                        data.lock[data.lock_id].release()
                    except:
                        print("UNABLE TO COMPUTE EIGENVECTORS for time (%f) select <%s> cod[%s]\n"%(time,select,cod_file))




    #
    # checkTimeInPreRect
    #
    def __checkTimeInPreRect(self,time,eigen_file):
        """
        check in pre-computed Eigen Vectors stored in file if time has been already computed

        *IN*
        time    : current time
        egein_file : file with eigen vectors values

        *OUT*
        boolean : True if time exist, False otherwise
        numpy   : numppy array[16] => time[1] codx[3] codv[3] eigen_vectors[9]
        array
        """

        if os.path.isfile(eigen_file):
            try:
                f=open(eigen_file,"r")
                while True:
                    tce=list(map(np.float64,(f.readline().split())))
                    if (len(tce)>0):
                        atime=tce[0]
                        if (atime-0.001)<time and (atime+0.001)>time:
                            f.close()
                            return True,tce
                    else:
                        f.close()
                        return False,np.array([])

            except EOFError:
                pass

        return False,np.array([])

    #
    # saveEigenVectors
    #
    def __saveEigenVectors(self,pre_rect_file,eigen_v):
        """
        """

        try:
            print("SAVING to pre_rect_file[%s]\n"%(pre_rect_file))
            f=open(pre_rect_file,"a")
            eigen_v.tofile(f,sep=" ",format="%e")
            f.write("\n")
            f.close()
        except:
            print("\n\nUnable to save pre_rect_file[%s] ... aborting...\n"%(pre_rect_file))
            sys.exit()

    #
    # buildRectFile
    #
    def buildRectFile(self,simname=None,ev_in=None,rect_out=None):
        """
        Build rect file from eigen vectors file
        """

        if simname is not None:
            self.simname = simname
            self.__sql3 = UnsSimu(simname,verbose=self.__verbose)
            self.__r = self.__sql3.getInfo() # return None if does not exist

            if self.__vdebug:
                self.__sql3.printInfo(simname)
            self.__slist = self.__sql3.getSnapshotList()
            if (self.__slist is None):
                message="In CLASS <"+self.__class__.__name__+"> :  Unknown simulation ["+simname+\
                        "] in UNS database..."
                raise Exception(message)
            if ev_in is None:
              simdir=self.__r['dir']+"/ANALYSIS/rectify2/"
              for ev_in in glob.glob(simdir+"*.ev"):
                rect_out=os.path.basename(ev_in)
                rect_out=simdir+rect_out.split(".ev")[0]+".rect"
                print(">> %s [%s]\n"%(ev_in,rect_out))
                self.__convertEv2Rect(ev_in,rect_out)

        else :
            self.__convertEv2Rect(ev_in,rect_out)


    #
    # fixRotation
    #
    @staticmethod
    def fixRotation(ev1,ev2,ev3):
        """
        correct rotation matrix

        return values :
        0 : nothing
        1 : x*-1
        2 : y*-1
        3 : (x>0,y<0)*(-1,-1) (x<0,y>0)*(-1,-1) (x>0,y>0)*(y,x) (x<0,y<0)*(y,x)
        4 : (x>0,y>0)*(-1,-1) (x<0,y<0)*(-1,-1) (x>0,y<0)*(y,x) (x<0,y>0)*(y,x)

        """

        A=np.array([-10, 10, 0])
        B=np.array([ 10, 10, 0])
        C=np.array([-10,-10, 0])
        D=np.array([ 10,-10, 0])

        A1=np.array([np.dot(A,ev1), np.dot(A,ev2), np.dot(A,ev3)])
        B1=np.array([np.dot(B,ev1), np.dot(B,ev2), np.dot(B,ev3)])
        C1=np.array([np.dot(C,ev1), np.dot(C,ev2), np.dot(C,ev3)])
        D1=np.array([np.dot(D,ev1), np.dot(D,ev2), np.dot(D,ev3)])

        ret = 0

        if A1[0]>0 and C1[0]>0:
            ret = 1
        if A1[1]<0 and B1[1]<0:
            ret = 2
        if A1[0]>0 and A1[1]<0:
            ret  = 3
        if C1[0]>0 and C1[1]>0:
            ret =4

        return ret

    #
    # infoTimeSimu
    #
    @staticmethod
    def infoTimeSimu(simname,time,component="gas-stars",rectify_dir_name='rectify2',rectify_suffix="ev",verbose=False):
        """
        return info array at the corresponding time and simu rect file
        arguments:
        simname : input simname or rect file
        time    : requested time to retreive
        component        : component base name for rect file, in case of simulation
        rectify_dir_name : dir name where is store rect files, in case of simulation
        rectify_suffix   : rect file suffox name , in case of simulation
        """
        rect_file=None
        if os.path.isfile(simname) :
            rect_file=simname
        else: # trying UNS database
            sql3 = UnsSimu(simname,verbose=verbose)
            r  = sql3.getInfo()
            if (r is None) :
                print("\nSimulation %s does not belong to UNS database...\n"%(simname))
            else:
                rectify_dir=r['dir']+"/ANALYSIS/"+rectify_dir_name
                rect_file=rectify_dir+"/"+r['name']+"."+component+"."+rectify_suffix
        print("Trying reading file [%s]\n"%(rect_file),file=sys.stderr)
        ok=False
        data=[]
        if os.path.isfile(rect_file):
            f=open(rect_file,"r")
            try:
                while True:
                    data=list(map(np.float64,(f.readline().split())))
                    #print ("DATA =",n,data,len(data))
                    if (len(data)>0):
                        atime=data[0]
                        if (atime-0.001)<time and (atime+0.001)>time:
                            return True,data[1:]
                    else:
                        return False,[]
            except EOFError:
                pass
        else:
            print("Unable to load RECT file [%s]"%(rect_file),file=sys.stderr)

        return ok,[]




    #
    # __convertEv2Rect
    #
    def __convertEv2Rect(self,ev_in=None,rect_out=None):
        if ev_in is not None and os.path.isfile(ev_in):
            f=None
            try:
                if rect_out is not None:
                    f=open(rect_out,"w")
            except (IOError,EOFError):
                print("Unable to open file [%s] for writing, aborting....\n"%(rect_out))
                sys.exit()
            a=np.loadtxt(ev_in) # load file
            ii=a[:,0].argsort()
            ref0=np.array([1.,0.,0.])
            ref1=np.array([0.,1.,0.])
            ref2=np.array([0.,0.,1.])
            for id in ii:
                time=a[id,0]
                cx=a[id,1:4]
                cv=a[id,4:7]
                ev0=a[id,7:10]
                ev1=a[id,10:13]
                ev2=a[id,13:16]
                tmp=np.dot(ref0,ev0)
                if tmp<0.0:
                    ev0 = ev0*-1.
                tmp=np.dot(ref2,ev2)
                if tmp<0.0:
                    ev2 = ev2*-1.
                ev1=np.cross(ev2,ev0)
                ref0=ev0
                ref1=ev1
                ref2=ev2
                if f is not None:
                    f.write("%e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e\n"\
                            %(a[id,0],cx[0],cx[1],cx[2],cv[0],cv[1],cv[2],ev0[0],\
                              ev0[1],ev0[2],ev1[0],ev1[1],ev1[2],ev2[0],ev2[1],ev2[2]))
                else:
                    print("%e %e %e %e %e %e %e %e %e %e %e %e %e %e %e %e"\
                            %(a[id,0],cx[0],cx[1],cx[2],cv[0],cv[1],cv[2],ev0[0],\
                              ev0[1],ev0[2],ev1[0],ev1[1],ev1[2],ev2[0],ev2[1],ev2[2]))
