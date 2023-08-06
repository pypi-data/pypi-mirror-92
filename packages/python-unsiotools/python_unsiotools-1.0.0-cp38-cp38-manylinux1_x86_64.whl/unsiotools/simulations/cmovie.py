#!/usr/bin/python
from __future__ import print_function
from ..uns_simu import *
from .csnapshot import *
from .c2dpgplot import *
import sys
#try:
#    import py_unstools # rectify swig
#except ImportError:
#    print("WARNING !!!,cmovie  failed to import module [py_unstools]",file=sys.stderr)


import subprocess

from multiprocessing import Lock,cpu_count
import time
import os


#
# ----
#
class CMovie:
    """
    Create movie from UNS data
    """
    #
    # ----
    #
    # constructor
    __analysis=None
    __newradius=None
    __prop=None
    __extdir=None
    __select=None
    __basedir=None
    __percen=None
    __lock=None

    def __init__(self,analysis=None,verbose=False,verbose_debug=False):
        """
        Constructor of CMovie class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """

        self.__vdebug=verbose_debug
        self.__verbose=verbose

        if analysis is not None:
            self.__analysis=analysis
            self.__smartAnalysisInit()

    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None):
        """
        Main core function to compute MOVIE on current snapshot store in data_analysis
        """
        if analysis is None:
            data=self.__analysis
        else:
            data=analysis

        uns_snap=data.uns_snap # link to UNS object
        ok,time=uns_snap.unsin.getData("time")
        print("Core [%d] time <%f>"%(data.core_id,time))

        element=0
        # loop on all existing component
        for comp,prop,percen,newradius,extdir,fdir in self.__comp_data:
            t_file=fdir+"/.time_completed"
            radius=self.__newradius_0[element]  # in case of newradius==0 (computed in INIT phase)
            element=element+1
            if not self.__checkTimeExist(time,t_file): # time not computed yet
                if newradius==1: # we must compute newradius for this frame
                    if percen < 0 : # we use percen*(-1) as range
                        radius=percen*-1
                    else:
                        status,radius=uns_snap.getMaxRadius(select=comp,percen=percen)
                        if self.__vdebug:
                            print("Computed radius [%f]\n"%(radius))

                radius = radius*1.1 # add 10% more radius
                filename=uns_snap.unsin.getFileName()
                basefile=os.path.basename(filename)
                no=int(basefile.split("_")[-1]) # compute no
                if prop=="age":
                    pixel=40
                else:
                    pixel=20
                myframe=fdir+"/frame.%05d.gif"%(no)
                print("MY FRAME = ",myframe)

                c=C2dpgplot(pixel=pixel) # object
                if prop=="none" or prop=="rho":
                    c.draw(uns_snap=uns_snap,select=comp,outdev=fdir+"/frame",title=basefile,no=no,prop=prop,cb=0,rrange=radius,times=time.item())
                else :
                    c.draw(uns_snap=uns_snap,select=comp,outdev=fdir+"/frame",title=basefile,no=no,prop=prop,cb=1,rrange=radius,times=time.item(),psort=1,itf=0)
                if not os.path.isfile(myframe):   # no frame created
                    subprocess.call(["convert","-size","850x680","xc:black",myframe]) # create a black frame

                self.__saveNewTime(time,t_file) # save new time in ".time_completed" file
            else:
                if self.__vdebug:
                    print("MOVIE: skip time[%.3f] from <%s>\n"%(time,t_file))

    #
    # __checkTimeExist
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
            print("Saving a new movie time[%.3f] in <%s>\n"%(time,t_file))
        try:
            f=open(t_file,"a")
            f.write("%e\n"%(time))
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

    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        data=self.__analysis

        if not hasattr(data,'movie_select'):
            print("\n\nYou must set a fied [movie_select] in your <data> object, aborting...\n\n")
            sys.exit()

        data.movie_select=data.movie_select.replace(" ","") # remove blank

        ### build COM Dir
        if hasattr(data,'movie_dir'):
            self.__movie_dir=data.movie_dir
            #
        else: # default simdir simulation
            self.__movie_dir=data.sim_info['dir']+"/ANALYSIS/movie"
        if self.__vdebug:
            print("MOVIE DIR = ", type(self.__movie_dir), data.sim_info['name'])
        self.simname=data.sim_info['name']

        self.__comp_data  =[]      # list to store compononent to proceed
        self.__newradius_0=[]      # list to store newradius 0

        self.__parseSelect(data)
        self.__createDir(data)


    #
    # __parseSelect
    #
    def __parseSelect(self,data):
        """
        parse selected string
        """

        ### re build select component variable according to components existing at mid
        ### simulation time (pre-computed by cuns_analysis.py and set to data.list_components
        self.__new_select=""
        for colon_s in data.movie_select.split(":"): # colon separate analysis
            print ("COLON_S =",colon_s)
            comp,prop,percen,newradius,extdir=colon_s.split("#")
            xx=data.list_components.find(comp) # find if component exist
            if xx==-1: # comp not exist
                print("CMovie#Warning : component <%s> from select <%s> does not exist...\n"\
                      %(comp,colon_s))
            else:      # comp exist
                fdir=self.__movie_dir+"/w/r_"+newradius+"_p_"+\
                      percen+"_pp_"+prop+"/"+comp

                self.__comp_data.append([comp,prop,float(percen),int(newradius),extdir,fdir])


    #
    # __createDir
    #
    def __createDir(self,data):
        """
        create directories for each existing components
        """

        for comp,prop,percen,newradius,extdir,fdir in self.__comp_data:
            # check newradius
            radius=-1
            if newradius==0: #we must compute radius of the last snapshot
                s=CSnapshot(data.slist[-1],comp)
                ok=s.nextFrame("xv")
                if ok:
                    # compute radius for at percen particles for the last snapshot
                    status,radius=s.getMaxRadius(select=comp,percen=percen)
                else:
                    print ("Cannot compute newradius_0 for [%s] on file "%(comp,data.slist[-1]))
                s.close() # close test snapshot
                print("Comp [%s] newradius_0 = <%f>"%(comp,radius))
            self.__newradius_0.append(radius) # store newradius_0



            data.lock[data.lock_id].acquire() # lock process
            # build directory
            if (not os.path.isdir(fdir)) :
                try:
                    print("Core ID ",data.core_id," create directory [%s]\n"%(fdir))
                    os.makedirs(fdir)

                except OSError:
                    print("Unable to create directory [%s]\n"%(fdir))
                    data.lock[data.lock_id].release()
                    sys.exit()
            data.lock[data.lock_id].release() # release process

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
            print("Saving a new movie time[%.3f] in <%s>\n"%(time,t_file))
        try:
            f=open(t_file,"a")
            f.write("%e\n"%(time))
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

    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations
        """

        data=self.__analysis

        if not hasattr(data,'movie_select'):
            print("\n\nYou must set a fied [movie_select] in your <data> object, aborting...\n\n")
            sys.exit()

        data.movie_select=data.movie_select.replace(" ","") # remove blank

        ### build COM Dir
        if hasattr(data,'movie_dir'):
            self.__movie_dir=data.movie_dir
            #
        else: # default simdir simulation
            self.__movie_dir=data.sim_info['dir']+"/ANALYSIS/movie"
        if self.__vdebug:
            print("MOVIE DIR = ", type(self.__movie_dir), data.sim_info['name'])
        self.simname=data.sim_info['name']

        self.__comp_data  =[]      # list to store compononent to proceed
        self.__newradius_0=[]      # list to store newradius 0

        self.__parseSelect(data)
        self.__createDir(data)


    #
    # __parseSelect
    #
    def __parseSelect(self,data):
        """
        parse selected string
        """

        ### re build select component variable according to components existing at mid
        ### simulation time (pre-computed by cuns_analysis.py and set to data.list_components
        self.__new_select=""
        for colon_s in data.movie_select.split(":"): # colon separate analysis
            print ("COLON_S =",colon_s)
            comp,prop,percen,newradius,extdir=colon_s.split("#")
            xx=data.list_components.find(comp) # find if component exist
            if xx==-1: # comp not exist
                print("CMovie#Warning : component <%s> from select <%s> does not exist...\n"\
                      %(comp,colon_s))
            else:      # comp exist
                fdir=self.__movie_dir+"/w/r_"+newradius+"_p_"+\
                      percen+"_pp_"+prop+"/"+comp

                self.__comp_data.append([comp,prop,float(percen),int(newradius),extdir,fdir])


    #
    # __createDir
    #
    def __createDir(self,data):
        """
        create directories for each existing components
        """

        for comp,prop,percen,newradius,extdir,fdir in self.__comp_data:
            # check newradius
            radius=-1
            if newradius==0: #we must compute radius of the last snapshot
                s=CSnapshot(data.slist[-1],comp)
                ok=s.nextFrame("xv")
                if ok:
                    # compute radius for at percen particles for the last snapshot
                    status,radius=s.getMaxRadius(select=comp,percen=percen)
                else:
                    print ("Cannot compute newradius_0 for [%s] on file "%(comp,data.slist[-1]))
                s.close() # close test snapshot
                print("Comp [%s] newradius_0 = <%f>"%(comp,radius))
            self.__newradius_0.append(radius) # store newradius_0



            data.lock[data.lock_id].acquire() # lock process
            # build directory
            if (not os.path.isdir(fdir)) :
                try:
                    print("Core ID ",data.core_id," create directory [%s]\n"%(fdir))
                    os.makedirs(fdir)

                except OSError:
                    print("Unable to create directory [%s]\n"%(fdir))
                    data.lock[data.lock_id].release()
                    sys.exit()
            data.lock[data.lock_id].release() # release process


    #
    #
    #
    def buildMovie(self,simname,overwrite,ncores):
        """
        buildMovie, build movie created using process_analysis.py program

        *IN*
        simname   (str) : simulation name, must belong to unsio database
        overwrite (bool): overwrite movie file if True
        ncores    (str) : number of cores. if "None" all cores used, otherwise
                          use int(ncores)
        """

        # compute cores
        if ncores==0:
            ncores=cpu_count()
        if self.__vdebug:
            print ("#cores used :",ncores)
            print ("simname :",simname)
        sql3 = UnsSimu(simname,verbose=self.__verbose)
        r = sql3.getInfo(simname)
        if (r) : # simulation exist
            dir_movie=r['dir']+'/ANALYSIS/movie'   # movie directory
            for d in glob.glob(dir_movie+"/w/*"):  # loop on work "w" directory
                base=os.path.basename(d)           # get basename like r_1_p_99_pp_none
                if (base[0:2]=='r_') :
                    q,radius,q,percen,q,property=base.split("_")
                    print("Radius [%f] Percen [%f] Property [%s]\n"%(float(radius),float(percen),property))
                    dir2_movie=dir_movie+"/center"
                    if float(percen)>0:
                        dir2_movie=dir_movie+"/whole"
                    if property!="none":
                        dir2_movie=dir_movie+"/"+property

                    if not os.path.isdir(dir2_movie) :
                        try:
                            os.makedirs(dir2_movie)
                        except OSError:
                            print("Unable to create directory [%s]\n"%(dir2_movie))

                    print ("Dir [%s]\n"%(d))
                    for c in glob.glob(d+"/*"):    # loop on components
                        comp=os.path.basename(c)
                        movie_name=simname+"_"+comp+"_"+property+"_post.avi"
                        print ("comp <%s> filename [%s/%s]\n"%(comp,dir2_movie,movie_name))
                        if  not os.path.isfile(dir2_movie+"/"+movie_name) or overwrite:
                            subprocess.call(["make_divx.pl",d+"/"+comp,"frame",dir2_movie+"/"+movie_name,"25",str(ncores)]) # create a black frame
        else:
            message="In CLASS <"+self.__class__.__name__+"> :  Unknown simulation ["+simname+"] in UNS database..."
            raise Exception(message)

        pass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Build simulation movie after smart analysis",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('simname', help='Simulation name')

    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)
    parser.add_argument('--overwrite',help='overwrite file if exist', dest="overwrite", action="store_true", default=False)
    parser.add_argument('--ncores', help='#cores used, 0 means all',default=4,type=int)
    #parser.add_argument('--no-verbose',help='verbose mode off', dest="verbose", action="store_false", default=True)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    movie = CMovie(verbose_debug=args.verbose)
    try:
        movie.buildMovie(args.simname,args.overwrite,args.ncores)
        pass
    except Exception as x :
        #print(x.message)
        print(x)
        sys.exit()



# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
