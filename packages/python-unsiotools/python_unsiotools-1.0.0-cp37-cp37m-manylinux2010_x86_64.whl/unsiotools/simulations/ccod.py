#!/usr/bin/env python
from __future__ import print_function
import sys
from ..uns_simu import *

from .cfalcon import *
from . import ctree as CT

from multiprocessing import Process, Lock,Pool
import multiprocessing
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as Queue
else:
    import queue as Queue
#import Queue # necessary to raise Queue.Empty signal
import time
import os
import signal

import matplotlib.pyplot as plt

#
# ----
#
class CCod:
    "compute Center Of Density on UNS snapshots"
    __sql3=None
    simname=None
    __r=None
    __slist=None # snap list
    __verbose=False
    __dbname=None
    __cod_file_base=None
    __ctree_threshold=10000
    __fastcod=True
    __halo_part=np.zeros(10,dtype=int)
    __is_multiple_halo=False
    __ok_halo_N=False
    __halo_comp=None
    __halo_N=None
    #__COD_DIR_NAME="codFAST"
    __COD_DIR_NAME="xCODvCOM"
    #
    # ----
    #
    # constructor
    def __init__(self,simname,analysis=None,cod_dir_name=None,cod_base=None,dbname=None,
                 threshold=None,verbose=False,verbose_debug=False):
        """
        simname must be a UNS simulation belonging to a uns sqlite3 database.
        infos regarding to simname simulation are loaded into privates variables
        """
        self.__vdebug=verbose_debug
        self.__verbose=verbose

        if threshold is not None:
            self.__ctree_threshold =threshold

        if cod_dir_name is not None:
            self.__COD_DIR_NAME=cod_dir_name

        print ("SIMNAME =",simname)
        if analysis is None :
            if simname is not None:
                self.__dbname=dbname
                if self.__vdebug:
                    print ("simname = ", simname,file=sys.stderr)
                self.simname = simname
                self.__sql3 = UnsSimu(simname,dbname=self.__dbname,verbose=self.__verbose)
                self.__r = self.__sql3.getInfo() # return None if does not exist

                if self.__vdebug:
                    self.__sql3.printInfo(simname)
                self.__slist = self.__sql3.getSnapshotList()
                if self.__r is not None:
                    self.__cod_file_base=self.__r["dir"]+"/ANALYSIS/"+self.__COD_DIR_NAME
                else:
                    message="From CCOD UNS simulation [%s] does not belong to unsio Database"%(self.simname)
                    raise Exception(message)
                self.__is_multiple_halo = self.__getHaloParticlesNumber() #
            else:
                print("Warning : In COD constructor, you gave None for simname",file=sys.stderr)
        else :
            print("COD analysis is activated",file=sys.stderr)
            self.__r=analysis.sim_info
            self.simname=analysis.sim_info['name']
            self.__is_multiple_halo = self.__getHaloParticlesNumber() #
            if self.__vdebug:
                if self.__is_multiple_halo:
                    print("MULTIPLE HALO present\n",file=sys.stderr)
                else:
                    print("SINGLE HALO present\n",file=sys.stderr)
            self.__smartAnalysis(analysis)

    #
    # isMultipleHalo
    #
    def isMultipleHalo(self):
        """
        return if simulation has multiple halo
        """
        return self.__is_multiple_halo
    #
    # ----
    #
    # compute COD according "select"ion component
    def compute(self,select,ncores=None,cod_file=None, fastcod=True,threshold=10000):
        """
        compute Center of Density on list of list of components

        select: string
                list of components, example :
                simple list : select=gas,disk
                two list    : select=gas,disk:stars  (note ':' to separate lists)

        ncores : integer
                #cores used for multiprocessing, if None then all availables cores will be used

        cod_file : string
                  cod's file name, if None it will be automatically build to be stored in sim's directory

        fastcod  : boolean (default true)
                    True : compute fas_cod using octree
                    rue : compute fas_cod using octree

        threshold : number of max dens particles estimated by ctree depht keept
                    if > 0 use this value as number of particles
                    if < 0 use as percentage of particles
                    default (10000 particles)
        """
        from . import csnapshot as cs
        if self.__r is None:
            print ("Simulation",self.simname," does not exist",file=sys.stderr)
            return False

        self.__ctree_threshold=threshold
        self.__fastcod=fastcod
        if cod_file is None:
            self.__cod_file_base=self.__r["dir"]+"/ANALYSIS/"+self.__COD_DIR_NAME
            # create directory
            if not os.path.isdir(self.__cod_file_base):
                try:
                    os.makedirs( self.__cod_file_base)
                except:
                    print ("Cannot create directory <%s>, aborting"%(self.__cod_file_base),file=sys.stderr)
                    sys.exit()
        if self.__vdebug:
            print ("COD FILE BASE =",self.__cod_file_base,file=sys.stderr)
        # Figure out best selected components
        self.__best_select=""
        for colon_s in select.split(":"):
            for coma_s in colon_s.split(","):
                if self.__vdebug:
                    print (">> :",coma_s,file=sys.stderr)
                if self.__best_select.find(coma_s)==-1: # substring not found
                    if len(self.__best_select)==0:
                        sep=""
                    else:
                        sep=","
                    self.__best_select += sep+ coma_s

        if self.__vdebug:
            print("Best select :",self.__best_select,file=sys.stderr)


        # get half of list of snapshot to check if all components exist

        half_snap=self.__slist[len(self.__slist)/2]
        if self.__vdebug:
            print("Half snapshot =",half_snap,file=sys.stderr)
        #sys.exit()
        test_snap=cs.CSnapshot(half_snap, self.__best_select)
        ok=test_snap.unsin.nextFrame()

        # rebuild select string with existing components
        self.__new_select=""
        for colon_s in select.split(":"):
            ok,data=test_snap.unsin.getData(colon_s,"pos")
            if not ok:
                ok,comp,ii=self.__checkSelectCompN(colon_s)
                print(ok,comp,ii,file=sys.stderr)
            if ok:
                if len(self.__new_select)==0:
                        sep=""
                else:
                        sep=":"
                self.__new_select += sep+ colon_s
        if self.__vdebug:
            print("new select :",self.__new_select,file=sys.stderr)
        test_snap.unsin.close()
        self.__is_multiple_halo = self.__getHaloParticlesNumber() #
        self.__startProcess(select,ncores,cod_file)
        self.computeMergingTime(outdir=None,store_analysis=True)

    #
    # ----
    #
    # launch parallel process
    def __startProcess(self,select,ncores=None,code_file=None):
        """
        Start COD computation in parallel on nores
        """
        # compute cores
        if ncores is None:
            ncores=multiprocessing.cpu_count()
        if self.__vdebug:
            print ("#cores used :",ncores,file=sys.stderr)

        # Feed QUEUE with list of snapshots
        q = multiprocessing.Queue()
        for snap in self.__slist: # loop on list os snsphots
            #print "SNAP put :",snap
            q.put(snap) # out a snapshot in the list

        # start process jobs
        processes=[]  # list of processes
        n=0

        # manage signint signal
        #original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN) # IGNOROE before process creation

        # lock to control access to file
        lock=Lock()

        # loop on all #cores and start a process
        for p in range(ncores):
            p = Process(target=self.__codProcess, args=(q,n,lock,))  # create
            p.start()  # start
            processes.append(p) # append list of process, used for joining
            n += 1

        # wait all processes to complete
        try:
            for p in processes:
                print ("waiting.. ",p,file=sys.stderr)
                p.join()
        except KeyboardInterrupt: # allow to interupt all workers with  CTRL+C
            for p in processes:
                print ("Terminating.. ",p,file=sys.stderr)
                p.terminate()
                p.join()
        while not q.empty():
            q.get(block=False)
    #
    # ----
    #
    def __codProcess(self,queue_list,n,lock):
        """
        Compute COD on core
        """
        from . import csnapshot as cs

        my_snap=self.__findLastSnapshotWithNoCod(queue_list,n,lock)
        stop=False
        cpt=0
        first=True
        while (not stop and my_snap is not None): # and not queue_list.empty()  ) :
            try:
                print ("Core [",n,"] waiting...",file=sys.stderr)
                if first:         # first time my_snap populated with self.__findLastSnapshotWithNoCod()
                    first=False
                else:
                    my_snap=queue_list.get(True,0.05) # we must use this line
                                                      # True means bloc during 0.05 sec,
                                                      # if nothing, then get raise Queue.Empty exception
                #my_snap=queue_list.get()  # do not use this, could block if nothing to get
                #time.sleep(0.01)
                uns_snap=cs.CSnapshot(my_snap,self.__best_select)
                ok=uns_snap.unsin.nextFrame("mxvI")
                okt,time=uns_snap.unsin.getData("time")

                # checkCodTime
                for select in self.__new_select.split(":"):
                    mycod_file=self.__cod_file_base+"/"+self.simname+"."+select+".cod"
                    lock.acquire()
                    #exist_time=self.__isTimeInCod(mycod_file,time)
                    exist_time,tcxv=self.getCodFromFile(mycod_file,time,n)
                    lock.release()
                    #print ("MYCOD =",mycod_file,time,exist_time)
                    if not exist_time:
                        if self.__vdebug:
                            print (">> computing density on: ", select,file=sys.stderr)

                        # check select if it is halo_N string
                        #
                        self.__ok_halo_N,self.__halo_comp,self.__halo_N=self.__checkSelectCompN(select)


                        if self.__ok_halo_N: # then it's an halo_X like
                            select=self.__halo_comp # rewrite halo_N to halo

                        if self.__ok_halo_N and not  self.__is_multiple_halo:# no multiple Halo, no need to compute
                            continue

                        ok,pos=uns_snap.unsin.getData(select,"pos")

                        cxv=np.zeros(6)
                        if ok and pos.size/3 > 32: # more than 32 particles at that time
                            ok,mass=uns_snap.unsin.getData(select,"mass")
                            ok,vel =uns_snap.unsin.getData(select,"vel")


                            if self.__ok_halo_N and self.__is_multiple_halo : # WE MUST RE ORDER PARTICLES
                                print (">> select =",select,file=sys.stderr)
                                ok,id=uns_snap.unsin.getData(select,"id")
                                print ("ok, id.size=",ok,id.size,file=sys.stderr)
                                ok,mass,pos,vel=self.__extractHalo(id,mass,pos,vel)
                                print("after extracting halo mass.size:", mass.size,file=sys.stderr)
                                #!!!!sys.exit()
                            if not self.__fastcod:
                                #c=CFalcon() # new falcon object
                                ok,rho,hsml=CFalcon().getDensity(pos,mass) # compute density

                                # compute cod

                                cxv=uns_snap.center(pos,vel,rho*mass)
                            else : # fastcod
                                ctree=CT.CTree(pos,vel,mass)  # instantiate a ctree object
                                cxv=ctree.fastCod3(self.__ctree_threshold)
                                # compute COM
                                comxv=uns_snap.center(pos,vel,mass)
                                print ("COD TCXV : ", time,cxv,file=sys.stderr)
                                print ("COM TCXV : ", time,comxv,file=sys.stderr)
                                # copy vCOM to cCOD
                                cxv[3:]=comxv[3:]
                                print ("COD TxCODvCOM : ", time,cxv,file=sys.stderr)


                        else: # no data
                            pass
                        lock.acquire()
                        out=open(mycod_file,"a+")
                        #cxv=np.insert(cxv,0,time)
                        #out.write(str(cxv).replace("[","").replace("]","")+"\n")
                        out.write("%e %e %e %e %e %e %e\n"%(time,cxv[0],cxv[1],cxv[2],cxv[3],cxv[4],cxv[5]))
                        out.close()
                        lock.release()

                cpt+=1
                print ("Core [",n,"] got snap : ",my_snap,cpt,file=sys.stderr)
            except Queue.Empty:
                stop = True # mo more data
                if self.__verbose:
                    print ("Queue.empty execption trapped...",file=sys.stderr)
            #except (KeyboardInterrupt, SystemExit):
            #    print ("Exiting...")
            #    #lock.release()
            #    sys.exit()
            #    terminate()
            #    stop = True #

        print ("Core [",n,"] DONE !",cpt,file=sys.stderr)

        #print "Core [",n,"] got snap : ",queue_list.get()

    #
    # ----
    #
    def getExtractHalo(self,id,mass,pos,vel, halo_id):
        #self.__ok_halo_N,self.__halo_comp,self.__halo_N=self.__checkSelectCompN("halo_"+str(halo_id))
        #print(self.__ok_halo_N,self.__halo_comp,self.__halo_N)
        # There is a mistake in cod file mdfxxx-gal0N.halo.cod wich are inverted
        # mdfxxx-gal01.halo.cod should be  mdfxxx-gal02.halo.co
        self.__halo_N=halo_id
        return self.__extractHalo(id,mass,pos,vel)
    #
    # ----
    #
    def __extractHalo(self,id,mass,pos,vel):
        id_sort=np.argsort(id) # sort according to ID order
        offset=0
        myidsort=np.zeros(1)
        if self.__halo_N==1:   # first halo
            mylast=self.__halo_part[0]
            myidsort = id_sort[0:mylast]
        else :                 # second halo
            mylast=self.__halo_part[1]
            offset = self.__halo_part[0]+mylast
            myidsort = id_sort[self.__halo_part[0]:offset]
        if self.__vdebug:
            print("__extractHalo : __halo_N=",self.__halo_N,mylast)
        pos = np.reshape(pos,(-1,3)) # reshape pos to nbody,3
        pos = np.reshape(pos[myidsort],-1) # select ids
        vel = np.reshape(vel,(-1,3)) # reshape vel to nbody,3
        vel = np.reshape(vel[myidsort],-1) # select ids

        return True,mass[myidsort],pos,vel

    #
    # ----
    #
    # check in select string component is indexed like halo_1 halo_2 etc..
    def __checkSelectCompN(self,ss,max=10):
        """
        check string 'ss' given as parameter is indexed like halo_X (X
        """
        xx=ss.find("_")
        if (xx!=-1):
            comp=ss[0:xx]
            #print "comp=",comp
            for i in range(max):
                if (ss==comp+"_%d"%(i)):
                    return True,comp,i-1
        return False,None,None
    #
    # ----
    #
    # try to read model_param.txt file in SIMULATION directory and fill up an array with #particles per galaxy/halo
    def __getHaloParticlesNumber(self,model_param="model_param.txt"):

        ok=False
        infile=self.__r['dir']+"/"+model_param
        if os.path.exists(infile):
            if self.__vdebug:
                print("Model file exist :",infile,file=sys.stderr)
            fh = open(infile)
            for line in fh:
                line=line.strip()
                if line.find('_halo_nbody')>=0 :
                    ok=True
                    sline=line.split()
                    ind=int(((sline[0].split("_"))[0].split("l"))[1])
                    if self.__vdebug:
                        print (sline,ind,type(self.__halo_part),file=sys.stderr)
                    self.__halo_part[ind-1] = int(sline[1])
        else:
            print("\n\n!!! File [%s] does not exist !!!!\n\n"%(model_param),file=sys.stderr)
        self.__halo_part=self.__halo_part[np.where(self.__halo_part>0)]
        if self.__vdebug:
            print (">>> ",self.__halo_part,self.__halo_part.size,file=sys.stderr)
        return ok
    #
    # ----
    # Compute mering time between two halos galaxy
    def computeMergingTime(self,halo_1=None,halo_2=None,simname=None,outdir="./",txtfile="merging_time.txt",pngfile="merging_time.png",dmax=1.0,seger=False, plot=True,store_analysis=False):

        merging_time=-1

        if halo_1 is None: # we are in a simulation
            if self.__cod_file_base is None: # no cod computation ?
                return 0
            else :
                if not seger:
                    c_halo_1=self.__cod_file_base+"/"+self.simname+".halo_1.cod"
                    c_halo_2=self.__cod_file_base+"/"+self.simname+".halo_2.cod"
                    if outdir is None:
                        outdir=self.__cod_file_base
                    simname=self.simname
                else:  # seger
                    c_halo_1=self.__cod_file_base+"/../seger.analysis/g1g2_center/g1_halo.cod0.01.txt"
                    c_halo_2=self.__cod_file_base+"/../seger.analysis/g1g2_center/g2_halo.cod0.01.txt"
                    outdir=None
                    simname=self.simname+"(seger)"

        else:
            c_halo_1=halo_1
            c_halo_2=halo_2
            simname="None"
        if self.__vdebug:
            print("c_halo_1 [%s]\nc_halo_2 [%s]\n"%(c_halo_1,c_halo_2),file=sys.stderr)
        if os.path.isfile(c_halo_1) and os.path.isfile(c_halo_2):
            # load files in numpy arrays
            data1=np.loadtxt(c_halo_1,dtype=np.float32)
            data2=np.loadtxt(c_halo_2,dtype=np.float32)
            # sort according time
            time1_sort=data1[:,0].argsort()
            time2_sort=data2[:,0].argsort()
            n = min(time1_sort.size,time2_sort.size) # get minimum in case of #lines
            time1_sort = time1_sort[0:n]
            time2_sort = time2_sort[0:n]
            # compute distance
            x2=(data1[time1_sort][:,1]-data2[time2_sort][:,1])**2
            y2=(data1[time1_sort][:,2]-data2[time2_sort][:,2])**2
            z2=(data1[time1_sort][:,3]-data2[time2_sort][:,3])**2
            distance=np.sqrt(x2+y2+z2)
            # select times only when distance > dmax
            a=(distance>=dmax)
            x=np.where(a)
            if x[0].size==0:
                print("\n\n\n NO MERGING TIME FOUND \n\n\n",file=sys.stderr)
                return -1
            id_merge = x[0][-1]+1 # id matching to merging time
            merging_time=data1[id_merge][0]
            print("Merging time =",merging_time,"\nmerging distance =",
                  distance[id_merge],"\nmax distance from merging=",
                  distance[data1[time1_sort][:,0]>merging_time].max(),file=sys.stderr)

            if txtfile is not None and outdir is not None :
                m_txt=outdir+"/"+txtfile
                print("Saving txt ",m_txt,file=sys.stderr)
                f=open(m_txt,"w")
                f.write(str(merging_time)+"\n")
                f.close()

            if store_analysis and self.__r is not None:
                m_txt=self.__r["dir"]+"/ANALYSIS/merging_time.txt"
                f=open(m_txt,"w")
                f.write("merging_time "+str(merging_time)+"\n")
                f.close()

            if plot:
                # plot
                # first plot: plot distance between 2 halos on whole simulation
                plt.subplot(211)
                plt.plot(data1[time1_sort][:,0],distance[time1_sort],'b')
                plt.axvline(merging_time,color='g',dashes=(10,3),label="merging")
                plt.title('Distance between 2 Halos : '+simname)
                plt.xlabel('Gyears')
                plt.ylabel('Kpc')
                ax = plt.axis() # get axis coordinates
                plt.text(merging_time+0.01,(ax[3]-ax[2])/2,"%.3f"%(merging_time)) # print merging time
                #plt.show()
                # second plot: plot distance between 2 halos from merging time
                plt.subplot(212)
                #plt.title('Distance between 2 Halos')
                plt.xlabel('Gyears')
                plt.ylabel('Kpc')
                select_t=(data1[time1_sort][:,0]>merging_time)
                plt.plot(data1[time1_sort[select_t]][:,0],distance[time1_sort[select_t]],'b')

                plt.axvline(merging_time,color='g',dashes=(10,3))
                ax = plt.axis() # get axis coordinates
                plt.text(merging_time+0.01,(ax[3]-ax[2])/2,"%.3f"%(merging_time)) # print merging time
                plt.tight_layout()


                if pngfile is not None and outdir is not None:
                    img_png=outdir+"/"+pngfile
                    print("Saving plot :",img_png,file=sys.stderr)
                    plt.savefig(img_png)
                else:
                    plt.show()
        return merging_time

    #
    #
    #
    def getMergingTime(self, txtfile="merging_time.txt"):
        """
        Get merging time from file
        """
        ok=False
        mtime=-1
        if self.__cod_file_base is None: # no cod computation ?
            return ok,-1

        mtf=self.__cod_file_base+"/"+txtfile
        if os.path.isfile(mtf):
            f=open(mtf,"r")
            try:
                mtime=float(f.readline())
                ok=True
            except EOFError:
                print("Unable to read file <%s>\n"%(mtf),file=sys.stderr)
                pass
        print("File <%s> does not exist\n"%(mtf),file=sys.stderr)
        return ok,mtime



    #
    # ----
    #
    def getCodFromComp(self, component, time,cod_file_base=None,n=-1):
        """
        check if current time exist in cod file build with componen
        """
        if cod_file_base is None:
            cod_file=self.__cod_file_base+"/"+self.simname+"."+component+".cod"
        else:
            cod_file=cod_file_base+"/"+self.simname+"."+component+".cod"
        if self.__vdebug:
            print("getCodFromComp file [%s]"%(cod_file),file=sys.stderr)

        return self.getCodFromFile(cod_file,time,n)


    #
    # ----
    #
    def getCodFromFile(self, cod_file, time,n=-1):
        """
        check if current time exist in cod file
        """
        ok=False
        tcxv=[]
        if os.path.isfile(cod_file):
            f=open(cod_file,"r")
            try:
                while True:
                    tcxv=list(map(np.float64,(f.readline().split())))
                    #print ("TCXV =",n,tcxv,len(tcxv))
                    if (len(tcxv)>0):
                        atime=tcxv[0]
                        if (atime-0.001)<time and (atime+0.001)>time:
                            return True,tcxv
                    else:
                        return False,[]
            except EOFError:
                pass

        return ok,tcxv

    #
    # ----
    #
    def __findLastSnapshotWithNoCod(self,queue_list,n,lock):
        """
        find out last snapshot with computed COD
        """
        from . import csnapshot as cs

        stop=False
        cpt=0
        my_snap=None
        while (not stop): # and not queue_list.empty()  ) :
            try:
                my_snap=queue_list.get(True,0.05) # we must use this line
                                                  # True means bloc during 0.05 sec,
                                                  # if nothing, then get raise Queue.Empty exception
                #my_snap=queue_list.get()  # do not use this, could block if nothing to get
                #time.sleep(0.01)
                uns_snap=cs.CSnapshot(my_snap,self.__best_select)
                ok=uns_snap.nextFrame("none")
                okt,time=uns_snap.unsin.getData("time")
                uns_snap.close()
                print ("Looking for no COD [",n,"] at time :",time,file=sys.stderr)
                # checkCodTime
                for select in self.__new_select.split(":"):
                    mycod_file=self.__cod_file_base+"/"+self.simname+"."+select+".cod"
                    lock.acquire()
                    #exist_time=self.__isTimeInCod(mycod_file,time)
                    exist_time,tcxv=self.getCodFromFile(mycod_file,time,n)
                    lock.release()
                    if not exist_time:
                        print ("Latest COD with no time=",mycod_file,time,exist_time,file=sys.stderr)
                        return my_snap

            except Queue.Empty:
                stop = True # mo more data
                my_snap=None
                if self.__verbose:
                    print ("Queue.empty execption trapped...",file=sys.stderr)

        return my_snap
    #
    # __smartAnalysis
    #
    def __smartAnalysis(self,data):
        """
        This is a special method called by constructor during smart pipeline analysis
        """
        if hasattr(data,'cod'):
            print ("COD exist",file=sys.stderr)
        else:
            # we go here the first time
            print ("COD does not exist",file=sys.stderr)
            data.cod=True
            # then we run some initialisations
            self.__smartAnalysisInit(data)


    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self,data):
        """
        start some initialisations
        """

        ### COD Dir name
        if hasattr(data,'cod_dir'):
            pass
            #
        else: # default simdir simulation
            data.cod_dir=data.sim_info['dir']+"/ANALYSIS/"+self.__COD_DIR_NAME

        print("CoD DIR = ", data.cod_dir, data.sim_info['name'],file=sys.stderr)
        self.__cod_file_base=data.cod_dir

        data.cod_select=data.cod_select.replace(" ", "")

        ### re build select component variable according to components existing at mid
        ### simulation time (pre-computed by cuns_analysis.py and set to data.list_components
        self.__new_select=""
        for colon_s in data.cod_select.split(":"):
            ok=True
            for comma_s in colon_s.split(","):
                xx=data.list_components.find(comma_s)  # find if selection exist
                if xx==-1:
                    ok=False
                    break
            if not ok:  #check if it not an halo_X selection
                ok,comp,ii=self.__checkSelectCompN(colon_s)
                if self.__vdebug:
                    print(ok,comp,ii,file=sys.stderr)
            if ok:
                if len(self.__new_select)==0:
                        sep=""
                else:
                        sep=":"
                self.__new_select += sep+ colon_s
        if self.__vdebug:
            print("new select :",self.__new_select,file=sys.stderr)

        #
        # build directories and links
        #
        # lock process
        data.lock[data.lock_id].acquire()
        if (not os.path.isdir(data.cod_dir)) : # build dir
            try:
                print("Core ID ",data.core_id," create directory [%s]\n"%(data.cod_dir),file=sys.stderr)
                os.makedirs(data.cod_dir)
            except OSError:
                print("Unable to create directory [%s]\n"%(data.cod_dir),file=sys.stderr)
                data.lock[data.lock_id].release()
                sys.exit()

        # make links
        cod_basename=data.cod_dir+"/"+data.sim_info['name']
        simname=data.sim_info['name']
        if self.__vdebug:
            print("Make links, cod_basename[%s]\n"%(cod_basename),file=sys.stderr)

        if self.__new_select.find('gas') ==-1 and \
           self.__new_select.find('disk')!=-1 :      # gas no and disk yes
            mysrc=simname+".disk.cod"
            mylink=cod_basename+".disk,stars.cod"
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)

            mysrc=simname+".halo,disk.cod"
            mylink=cod_basename+".halo,disk,stars.cod"
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)


        if self.__new_select.find('gas') !=-1 and \
           self.__new_select.find('disk')==-1 :      # gas yes and disk no
            mysrc=simname+".stars.cod"
            mylink=cod_basename+".disk,stars.cod"
            if self.__vdebug:
                print ("Links : src[%s] dest[%s]\n"%(mysrc,mylink),file=sys.stderr)
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)

            mysrc=simname+".halo,stars.cod"
            mylink=cod_basename+".halo,disk,stars.cod"
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)

        if self.__new_select.find('halo_1') !=-1:   # halo_1  yes
            mysrc=simname+".halo_1.cod"
            mylink=cod_basename+"-gal01.halo.cod"
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)

        if self.__new_select.find('halo_2') !=-1:   # halo_2  yes
            mysrc=simname+".halo_2.cod"
            mylink=cod_basename+"-gal02.halo.cod"
            if not os.path.islink(mylink):
                os.symlink(mysrc,mylink)

        # release process
        data.lock[data.lock_id].release()


    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None):
        """
        Main core function to compute COD on current snapshot store in data_analysis
        """
        if analysis is None:
            print("\nProgram aborted because you did not set 'analysis' variable from smartAnalysis method\n",file=sys.stderr)
            sys.exit()

        data=analysis
        uns_snap=data.uns_snap

        ok,time=uns_snap.unsin.getData("time")
        if self.__vdebug:
            print(self.simname+" time : "+str(time),file=sys.stderr)


        # checkCodTime
        for select in self.__new_select.split(":"):
            mycod_file=self.__cod_file_base+"/"+self.simname+"."+select+".cod"
            data.lock[data.lock_id].acquire()
            #exist_time=self.__isTimeInCod(mycod_file,time)
            exist_time,tcxv=self.getCodFromFile(mycod_file,time)
            data.lock[data.lock_id].release()
            #print ("MYCOD =",mycod_file,time,exist_time)
            if not exist_time:
                if self.__vdebug:
                    print (">> computing density on: ", select,file=sys.stderr)

                # check select if it is halo_N string
                #
                self.__ok_halo_N,self.__halo_comp,self.__halo_N=self.__checkSelectCompN(select)

                if self.__ok_halo_N: # then it's an halo_X like
                    select=self.__halo_comp # rewrite halo_N to halo

                if self.__ok_halo_N and not  self.__is_multiple_halo:# no multiple Halo, no need to compute
                    continue

                ok,pos=uns_snap.unsin.getData(select,"pos")

                cxv=np.zeros(6)
                if ok and pos.size/3 > 32: # more than 32 particles at that time
                    ok,mass=uns_snap.unsin.getData(select,"mass")
                    ok,vel =uns_snap.unsin.getData(select,"vel")


                    if self.__ok_halo_N and self.__is_multiple_halo: # WE MUST RE ORDER PARTICLES
                        #if self.__vdebug:
                        #    print (">> select =",select)
                        ok,id=uns_snap.unsin.getData(select,"id")
                        #if self.__vdebug:
                        #    print ("ok, id.size=",ok,id.size)
                        ok,mass,pos,vel=self.__extractHalo(id,mass,pos,vel)
                        #if self.__vdebug:
                        #    print("after extracting halo mass.size:", mass.size)
                        #!!!!sys.exit()
                    if not self.__fastcod:
                        #c=CFalcon() # new falcon object
                        ok,rho,hsml=CFalcon().getDensity(pos,mass) # compute density

                        # compute cod

                        cxv=uns_snap.center(pos,vel,rho*mass)
                    else : # fastcod
                        ctree=CT.CTree(pos,vel,mass)  # instantiate a ctree object
                        cxv=ctree.fastCod3(self.__ctree_threshold)
                        # compute COM
                        comxv=uns_snap.center(pos,vel,mass)
                        if self.__vdebug:
                            print ("COD TCXV : ", time,cxv,file=sys.stderr)
                            print ("COM TCXV : ", time,comxv,file=sys.stderr)
                        # copy vCOM to cCOD
                        cxv[3:]=comxv[3:]

                    if self.__vdebug:
                        print ("TCXV : ", time,cxv,file=sys.stderr)

                else: # no data
                    pass
                data.lock[data.lock_id].acquire()
                out=open(mycod_file,"a+")
                #cxv=np.insert(cxv,0,time)
                #out.write(str(cxv).replace("[","").replace("]","")+"\n")
                out.write("%e %e %e %e %e %e %e\n"%(time,cxv[0],cxv[1],cxv[2],cxv[3],cxv[4],cxv[5]))
                out.close()
                data.lock[data.lock_id].release()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# import some modules for mains programs
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLineMT, parse the command line for merging_time.py program
def commandLineMT():
    dbname=None
    ncores=None
    pngfile=None
    txtfile=None
    cod1=None
    cod2=None
    dmax=1.0


    # help
    parser = argparse.ArgumentParser(description="Display merging time",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('--dmax', help='max distance of separation (kpc)',default=dmax,type=float)
    parser.add_argument('--cod1', help='first cod file',default=cod1)
    parser.add_argument('--cod2', help='second cod file',default=cod2)
    parser.add_argument('--seger', help='use sergey files',dest="seger",action='store_true',default=False)
    #parser.add_argument('--no-seger', help='use base simulation files',dest="seger",action='store_false',default=True)
    parser.add_argument('--pngfile', help='png filename, if None interactive plot',default=pngfile)
    parser.add_argument('--txtfile', help='merging time filename, if None not saved',default=txtfile)
    parser.add_argument('--plot', help='Enable ploting',dest='plot',action='store_true',default=False)
    #parser.add_argument('--no-plot', help='Disable ploting',dest='plot',action='store_false',default=True)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)
    parser.add_argument('--saveanalysis',help='save merging time in ANALYSIS directory', dest="store_analysis", action="store_true", default=False)
    #parser.add_argument('--no-verbose',help='verbose mode off', dest="verbose", action="store_false", default=True)

    # parse
    args = parser.parse_args()

    if args.pngfile=="None":
        args.pngfile=None
    # start main funciton
    processMT(args)


# -----------------------------------------------------
# processMT, is the core function for merging_time.py program
def processMT(args):
    cod = CCod(simname=args.simname,verbose_debug=args.verbose,dbname=args.dbname)
    try:
        mt=cod.computeMergingTime(halo_1=args.cod1,halo_2=args.cod2,pngfile=args.pngfile,txtfile=args.txtfile,dmax=args.dmax,seger=args.seger,plot=args.plot,store_analysis=args.store_analysis)
        if mt<0.0:
            mt=0.0
        print("%f\n"%(mt))
    except KeyboardInterrupt:
        sys.exit()

# commandLine, parse the command line for uns_cod.py program
def commandLine():
    dbname=None
    ncores=None
    fastcod=True
    threshold=10000
     # help
    parser = argparse.ArgumentParser(description="Compute COD on simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('select', help='Selected component')
    parser.add_argument('--fastcod', help='compute density by selecting particles from octree',default=fastcod)
    parser.add_argument('--threshold', help='number of particles used for fastcod (<0 percentage)',default=threshold,type=int)
    parser.add_argument('--ncores', help='Use ncores, None means all',default=ncores,type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function of uns_cod.py program
def process(args):
    cod = CCod(simname=args.simname,verbose_debug=args.verbose,dbname=args.dbname)
    cod.compute(select=args.select,ncores=args.ncores,fastcod=args.fastcod,threshold=args.threshold)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
