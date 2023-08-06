#!/usr/bin/env python
from __future__ import print_function
import sys
from ..uns_simu import *
from .ccod import *

from . import crectify as crect
from multiprocessing import Lock
import time
import os,sys
import matplotlib
import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import time
import scipy.ndimage as ndi
import subprocess
#from IPython import embed

#
# ----
#
class C2dplot:
    """
    Draw 2d image
    """
    #
    # ----
    #
    # constructor
    __analysis=None
    dimx=1080
    dimy=1080
    pixel=20
    gp=5.0
    __COD_DIR_NAME="codFAST"

    def __init__(self,analysis=None,verbose=False,verbose_debug=False):
        """
        Constructor of C2dplot class

        - analysis : is a class object instantiate from CUnsAnalysis class
        """

        self.__vdebug=verbose_debug
        self.__verbose=verbose

        if analysis is not None:
            matplotlib.use('Agg')
            self.__analysis=analysis
            self.__smartAnalysisInit()


    #
    # __smartAnalysisInit
    #
    def __smartAnalysisInit(self):
        """
        start some initialisations for Online Analysis
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
            self.__movie_dir=data.sim_info['dir']+"/ANALYSIS/movie2"

        # add selected components to movie_dir
        self.__movie_dir_std=self.__movie_dir+"/std/"+data.movie_select
        self.__movie_dir_contour=self.__movie_dir+"/contour/"+data.movie_select
        if self.__vdebug:
            print("MOVIE DIR = ", type(self.__movie_dir), data.sim_info['name'])
        self.simname=data.sim_info['name']

        self.__comp_data  =[]      # list to store compononent to proceed

        #self.__parseSelect(data)
        self.__createDir(data)


    #
    #
    #
    def buildMovie(self,simname,dirmovie=None,overwrite=False,ncores=None):
        """
        buildMovie, build movie created using process_analysis.py program

        *IN*
        simname : simulation name, must belong to unsio database
        """

        sql3 = UnsSimu(simname)
        r = sql3.getInfo()

        if (r) : # simulation exist
            if dirmovie is not None:
                dir_movie=dirmovie
            else:
                dir_movie=r['dir']+'/ANALYSIS/movie2'   # movie directory
            if self.__vdebug:
                print("Dir movie =",dir_movie)
            for d in ["contour","std"]:
                for s in glob.glob(dir_movie+"/"+d+"/*"):
                    dir_frame=os.path.basename(s)
                    movie_name=dir_movie+"/"+d+"_"+dir_frame+".avi"
                    if not os.path.isfile(movie_name) or overwrite:
                        print("make_divx.pl",s,"frame",movie_name,"25",str(ncores),file=sys.stderr)
                        subprocess.call(["make_divx.pl",s,"frame",movie_name,"25",str(ncores)])
    #
    # smartAnalysis
    #
    def smartAnalysis(self,analysis=None,component=None,xrange="20",mergers=None,center_cod=None,cmap="gas:jet,stars:rainbow,halo:PuOr",contour=False,noxz=False,sigma=6.0):
        """
        Main core function to compute MOVIE on current snapshot store in data_analysis
        """
        if analysis is None:
            data=self.__analysis
        else:
            data=analysis

        uns_snap=data.uns_snap # link to UNS object
        ok,time=uns_snap.unsin.getData("time")
        if self.__vdebug:
            print("Core [%d] time <%f>"%(data.core_id,time))
        if not contour:
            my_dir=self.__movie_dir_std
        else:
            my_dir=self.__movie_dir_contour
        t_file=my_dir+"/.time_completed"
        if not self.__checkTimeExist(time,t_file): # time not computed yet
            filename=uns_snap.unsin.getFileName()
            basefile=os.path.basename(filename)
            no=int(basefile.split("_")[-1]) # compute no
            out=my_dir+"/frame"
            self.fullProcess(data.uns_snap,out=out,component=component,xrange=xrange,sigma=sigma,
                             cmap=cmap,mergers=mergers,center_cod=center_cod,cpt=no,noxz=noxz,contour=contour)
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
    # __createDir
    #
    def __createDir(self,data):
        """
        create directories for each existing components
        """

        data.lock[data.lock_id].acquire() # lock process
        # build directory
        for my_dir in (self.__movie_dir_std, self.__movie_dir_contour):
            if (not os.path.isdir(my_dir)) :
                try:
                    if self.__vdebug:
                        print("Core ID ",data.core_id," create directory [%s]\n"%(my_dir))
                    os.makedirs(my_dir)

                except OSError:
                    print("Unable to create directory [%s]\n"%(self.my_dir))
                    data.lock[data.lock_id].release()
                    sys.exit()
        data.lock[data.lock_id].release() # release process


    #
    # __grid_density_gaussian_filter
    #
    def __grid_density_gaussian_filter(self,x0, y0, x1, y1, w, h, x,y,r,rho):
        """
        x0 (view_xmin)
        y0 (view_ymin)
        x1 (view_xmax)
        y1 (view_ymax)
        w  (window witdh )
        h  (window height)
        x  (x axis pos)
        y  (y axis pos)
        """
        to = time.clock()
        kx = (w - 1.) / (x1 - x0) # scale on x according to the windows width
        ky = (h - 1.) / (y1 - y0) # scale on y according to the windows height
        if self.__vdebug:
            print ("sigma r=",r," kx,ky",kx,ky,file=sys.stderr)
        #r=10
        border = 0#r
        imgw = int(w + 2 * border) # !!!!! INT
        imgh = int(h + 2 * border) # !!!!! INT
        img = np.zeros((imgh,imgw))
        img += 0.1 # set 0.1 to every pixels

        if x.size>0 : # proceed only if there are particles
            # Windows X axis
            myix= (x - x0)  * kx # integerize particles on x axis according to scalex (kx)
            myix=myix.astype(int)
            myix=myix+border  # array of indexes values
            if self.__vdebug:
                print( "myix =",myix.size,file=sys.stderr)
            maskix=(0<=myix)&(myix<imgw) # keep only particles in the windows X

            # Windows Y axis
            myiy= (y - y0) * ky # integerize particles on y axis according to scaley (ky)
            myiy=myiy.astype(int)
            myiy=myiy+border
            if self.__vdebug:
                print("myiy =", myiy.size,file=sys.stderr)
            maskiy=(0<=myiy)&(myiy<imgh)  # keep only particles in the windows Y

            #print (">>>>",myiy[maskiy].max(),imgh)
            #sys.exit()
            # both X and Y
            maskglob=maskix&maskiy  # keep  particles both in the windows X and Y

            if self.__vdebug:
                print("maskglob=",maskglob.size,file=sys.stderr)
                print("myix[maskglob]=",myix[maskglob].size,myix[maskglob].max(),file=sys.stderr)
                print("myiy[maskglob]=",myiy[maskglob].size,myiy[maskglob].max(),file=sys.stderr)
            #img[myix[maskglob]][myiy[maskglob]]=np.random.random_integers(1024)
                print("IMG:",img.size,img.shape)
            for a,b,rr in zip(myiy[maskglob],myix[maskglob],rho[maskglob]): #myix[maskglob],myiy[maskglob]):
                img[a][b] += 1.#*rr
            #sys.exit()
            #img=math.log(img)
            #duplicated,unique_ind	= np.unique(myix[maskix],return_index=True)

            #print "duplicated,unique_ind",duplicated,duplicated.size,unique_ind, unique_ind.size
            if self.__vdebug:
                print("timing grid_density_gaussian_filter = ", time.clock() - to,file=sys.stderr)

        return ndi.gaussian_filter(img, sigma=(r,r),order=0)  ## gaussian convolution
        #ndi.gaussian_filter(img, (r,r))  ## gaussian convolution

    #
    # __getCenterCod
    #
    def __getCenterCod(self,center_cod,comp=None):
        """
        According to argument 'center_cod'
        - if it's cod file, will return cod
        - if it's '@sim' it will return sim's cod at component comp
        """
        #embed()
        # check if simu
        if self.__vdebug:
            print("IN __getCenterCod [%s]"%(center_cod),file=sys.stderr)
        if os.path.isfile(center_cod) : # it's a file
            ok,time=self.__uns.unsin.getData("time")
            return CCod(None).getCodFromFile(center_cod,time)
        else:
            tmp=center_cod.split('@')
            if (len(tmp)>1): # it's simulation name
                simname=tmp[1]
                if self.__vdebug:
                    print("Simulation name from COD [%s] comp <%s>\n"%(simname,comp))
                    print("SELF.__ANALYSIS = <%s>"%(self.__analysis))
                cod=CCod(simname,verbose_debug=self.__vdebug)
                ok,time=self.__uns.unsin.getData("time")
                cod_base=None
                if self.__analysis is not None:
                    if hasattr(self.__analysis,"cod_dir"):
                        cod_base=self.__analysis.cod_dir
                if self.__vdebug:
                    print(" def __getCenterCod -> cod_base=[%s]"%(cod_base))
                return cod.getCodFromComp(comp,time,cod_file_base=cod_base)


        return False,None,None,None,None


    #
    # __getCenterMerger
    #
    def __getCenterMerger(self,mergers):
        """
        According to argument 'mergers', return position of center of the 2 mergers
        mergers variable can be a filename, or if it's like '@simname', then
        positions of the center is autmatically retreive from simulation 'simname'
        """
        #embed()
        # check if simu
        tmp=mergers.split('@')
        if (len(tmp)>1): # it's simulation name
            simname=tmp[1]
            if self.__vdebug:
                print("Simulation name from merger [%s]\n"%(simname))
                print("SELF.__ANALYSIS = <%s>"%(self.__analysis))
            cod=CCod(simname,verbose_debug=self.__vdebug)
            ok,time=self.__uns.unsin.getData("time")
            cod_base=None
            if self.__analysis is not None:
                if hasattr(self.__analysis,"cod_dir"):
                    cod_base=self.__analysis.cod_dir
            if self.__vdebug:
                print(" def __getCenterMerger -> cod_base=[%s]"%(cod_base))
            ok1,tcxv1=cod.getCodFromComp("halo_1",time,cod_file_base=cod_base)
            if self.__vdebug:
                print ("halo_1:",ok,tcxv1,file=sys.stderr)
            ok2,tcxv2=cod.getCodFromComp("halo_2",time,cod_file_base=cod_base)
            if self.__vdebug:
                print ("halo_2:",ok,tcxv2,file=sys.stderr)
            if ok1 and ok2:
                cxy=np.array([(tcxv2[1]+tcxv1[1])/2.,(tcxv2[2]+tcxv1[2])/2.]) # x2-x1,y2-y1
                cxz=np.array([(tcxv2[1]+tcxv1[1])/2.,(tcxv2[3]+tcxv1[3])/2.]) # x2-x1,y2-y1
                if self.__vdebug:
                    print("cxy:",cxy," cxz:",cxz,file=sys.stderr)
                return True,cxy,cxz,tcxv1[1:4],tcxv2[1:4]

        return False,None,None,None,None

    #
    # __setCmapComponents
    # Set default colormap for each components
    def __setCmapComponents(self,cmap):
        """
        Set default colormap for each components
        """
        #default colormap
        comp_cmap = {}
        comp_cmap['all'  ]='jet'
        comp_cmap['gas'  ]='jet'
        comp_cmap['stars']='rainbow'
        comp_cmap['disk' ]='Set3'
        comp_cmap['bndry']='hsv'
        comp_cmap['halo' ]='PuOr'
        if len(cmap.split(","))==1 and len(cmap.split(":"))==1:
            # set same cmap for all components
            for i,ccomp in enumerate(comp_cmap):
                comp_cmap[ccomp]=cmap
        else : # affect one cmap per component according to 'cmap' argument
            for comp in cmap.split(","):
                ccmap=comp.split(":")
                if len(ccmap)>1:
                    comp_cmap[ccmap[0]]=ccmap[1]
        return comp_cmap

    #
    #
    #
    def fullProcess(self,uns,out="",component=None,xrange=20.,sigma=6.0,mergers="",cmap="jet",
                    cpt=0,noxz=False,contour=False,nc=20,center_cod=None,nopart=False,
                    rect_sim=None, rect_comp="stars-stars",rect_dir="rectify2",rect_suffix="ev",
                    circle=""):
        t0=time.clock()
        sigma_ori=sigma
        xrange_ori=xrange
        # rectify variables
        self.__rect_sim    = rect_sim
        self.__rect_comp   = rect_comp
        self.__rect_dir    = rect_dir
        self.__rect_suffix = rect_suffix
        self.__circle = circle
        self.__x={}
        # set color map
        comp_cmap=self.__setCmapComponents(cmap)

        comp=component.split(",")

        ok,timex=uns.unsin.getData("time")
        if self.__vdebug:
            print ("Loading time : " , time.clock()-t0)

        # read data_rectify
        if self.__rect_sim is not None:
            print("Rectify is activated....\n",file=sys.stderr)
            ok,self.__data_rect=crect.CRectify.infoTimeSimu(self.__rect_sim,timex,self.__rect_comp,
                                                            self.__rect_dir,self.__rect_suffix)
            if not ok:
                print("\nUnable to retreive RECTIFY information...aborting\n\n",file=sys.stderr)
                sys.exit()


        self.__uns=uns
        #
        ok_center,center_xy,center_xz,cx1,cx2=self.__getCenterMerger(mergers)

        if ok_center:
            #compute best windows size
            newcx1=math.fabs(cx1[0]-center_xy[0])
            newcy1=math.fabs(cx1[1]-center_xy[1])
            newcx2=math.fabs(cx2[0]-center_xy[0])
            newcy2=math.fabs(cx2[1]-center_xy[1])

            best_winsize=max(max(newcx1,newcy1),max(newcx2,newcy2))
            if self.__vdebug:
                print("BEST  =", best_winsize,newcx1,newcy1,newcx2,newcy2)
            if best_winsize > xrange_ori:
                xrange=best_winsize+0.2*xrange_ori # add 20% of rmax to best_winsize
            else:
                xrange=xrange_ori

        # set up grid display
        nrows=2
        if noxz: # no XZ projection
            nrows=1
        ncols=len(comp)

        # compute aspect ratio
        mydpi=80

        if nrows<ncols:
            inches=19
            #inches = 1920./mydpi # 1920
            w=inches
            h=inches*nrows/ncols
        else: # nrows>ncols
            inches = 1080./mydpi
            w=inches*ncols/nrows
            h=inches
        if self.__vdebug:
            print("w/h=",w,h,w*mydpi,h*mydpi,file=sys.stderr)

        # specify figure dimensions
        fig=plt.figure(figsize=(w,h),dpi=mydpi)
        #fig=plt.figure(figsize=(w,h))
        if self.__vdebug:
            print ("FIG DPI =",fig.dpi)
        # create grid
        gs = gridspec.GridSpec(nrows, ncols,wspace=0,hspace=0)#height_ratios=h,width_ratios=w)
        #print(gs.get_width_ratios(),gs.get_height_ratios(),gs.get_grid_positions(fig))
        fig.suptitle(os.path.basename(uns.unsin.getFileName())+" - time : %.03f"%(timex))

        for r in range(nrows):
            for c in range(ncols):
                ax = plt.subplot(gs[r, c])
                ax.set(aspect=1)
                #zz=np.random.random((102,102))
                #qq=ndi.gaussian_filter(zz,sigma=1.6,order=0)
                #im = ax.imshow(qq, norm = matplotlib.colors.LogNorm(), cmap="jet")
                #plt.contour(qq,cmap="rainbow")
                if r != nrows-1:
                    ax.set_xticks([])
                if  c!=0:
                    ax.set_yticks([])
                #embed()
                self.__display(uns,out,comp[c],xrange,sigma_ori,mergers,comp_cmap[comp[c]],
                               ok_center, center_xy,center_xz,ax,fig,r,contour=contour,nc=nc,
                               center_cod=center_cod,nopart=nopart)
        fig.subplots_adjust(hspace=0.,wspace=0.)
        if self.__vdebug:
            print("Overall time [%.3f] sec"%(time.clock()-t0),file=sys.stderr)
        if (out==''):
            plt.show()
        else:
            outfile=out+"."+"%05d"%cpt+".jpg"
            if self.__vdebug:
                print (">>>>> ",outfile)
            try:
                plt.savefig(outfile, bbox_inches=0,dpi=fig.dpi)
            except:
                if not os.path.isfile(outfile):
                    print("\nUnable to save figure [%s], aborting...\n"%(outfile),file=sys.stderr)
                sys.exit()
        plt.close(fig)


    #
    #
    #
    def __display(self,uns,out,component,xrange,sigma_ori,mergers,cmap,ok_center,
                  center_xy,center_xz,ax,fig,row,contour=False,nc=20,center_cod=None,nopart=False):

        t0=time.clock()
        comp=component

        # get data
        ok,pos=uns.unsin.getData(comp,"pos") # positions

        if self.__vdebug:
            print("return getpos :",ok)

        if ok:
            # get data
            ok,rho=uns.unsin.getData(comp,"rho") # rho

            if not ok:
                rho=np.ones(int(pos.size/3))

            # get data
            ok,mass=uns.unsin.getData(comp  ,"mass") # gas density
            if not ok:
                mass=np.ones(int(pos.size/3))

            # reshape array in x,y,z arrays
            pos=np.reshape(pos,(-1,3))        # pos reshaped in a 2D array [nbody,3]
#            if self.__rect_sim is not None:
#               print("rectifying....")
#               x0 = pos * self.__data_rect[6:9]
#               x1 = pos * self.__data_rect[9:12]
#               x2 = pos * self.__data_rect[12:15]
#
#               #pos[:,0]  = np.sum(x0,axis=1)
#               #pos[:,1]  = np.sum(x1,axis=1)
#               #pos[:,2]  = np.sum(x2,axis=1)
#            else:
#               pass

            x = pos[:,0]                      # x coordinates
            if row==0:
                y = pos[:,1]                      # y coordinates
            else:
                y = pos[:,2]                      # z coordinates

            nbody = x.size
            if self.__vdebug:
                print("Ok_center [%d] center_cod <%s>"%(ok_center,center_cod))
            if  ok_center:# it's a merger requested which exist
                x -= center_xy[0]
                if row==0:
                    y -= center_xy[1]
                else:
                    y -= center_xz[1]
            else:
                if center_cod is not None: # center on COD requested
                    ok,tcxv=self.__getCenterCod(center_cod,comp)
                    if not ok :
                        print("Failed to __getCenterCod, aborting...\n",file=sys.stderr)
                        sys.exit()
                    else:
                        print("tcxv=",tcxv[1:4],file=sys.stderr)
                        x -= tcxv[1]
                        if row==0: # y = y
                            y -= tcxv[2]
                        else:      # y = z
                            y -= tcxv[3]
                else: # COM center according COM or COD if RHO exist
                    xcom=np.average(x.astype(np.float64),weights=mass*rho)
                    ycom=np.average(y.astype(np.float64),weights=mass*rho)
                    if self.__vdebug:
                        print ("COM = ",xcom,ycom,file=sys.stderr)
                    x -= xcom
                    y -= ycom
            # proceed on rectify
            if self.__rect_sim is not None:
                fix_pos=crect.CRectify.fixRotation(self.__data_rect[6:9],
                                                   self.__data_rect[9:12],
                                                   self.__data_rect[12:15])
                print("\n\n FIX POS=",fix_pos)
                x0 = pos * self.__data_rect[6:9]
                x1 = pos * self.__data_rect[9:12]
                x2 = pos * self.__data_rect[12:15]

                if row==0:
                    x = np.sum(x0,axis=1)
                    self.__x[component]=np.copy(x) # we copy the result of x0 the first time (row=0)
                    # otherwise x coordinates will not be centered
                    # at next row. It's because we we offset y coordinates
                    # either with center_xy (row 0) or center_xz (row>0)
                    y = np.sum(x1,axis=1)
                else:
                    x = self.__x[component] # np.sum(x0,axis=1)
                    y = np.sum(x2,axis=1)

                if fix_pos == 1:
                    x = x*-1
                if fix_pos == 2:
                    y = y*-1
                if fix_pos == 3:
                    sel=(x>0)&(y<0)
                    sel2=(x<0)&(y>0)
                    sel3=(x>0)&(y>0)
                    sel4=(x<0)&(y<0)
                    x[sel]=x[sel]*-1
                    y[sel]=y[sel]*-1

                    x[sel2]=x[sel2]*-1
                    y[sel2]=y[sel2]*-1

                    x_copy= np.copy(x[sel3])
                    y_copy= np.copy(y[sel3])
                    x[sel3] = y_copy
                    y[sel3] = x_copy

                    x2_copy= np.copy(x[sel4])
                    y2_copy= np.copy(y[sel4])
                    x[sel4] = y2_copy
                    y[sel4] = x2_copy

                if fix_pos == 4:
                    sel=(x>0)&(y>0)
                    sel2=(x<0)&(y<0)
                    sel3=(x>0)&(y<0)
                    sel4=(x<0)&(y>0)
                    x[sel]=x[sel]*-1
                    y[sel]=y[sel]*-1

                    x[sel2]=x[sel2]*-1
                    y[sel2]=y[sel2]*-1

                    x_copy= np.copy(x[sel3])
                    y_copy= np.copy(y[sel3])
                    x[sel3] = y_copy
                    y[sel3] = x_copy

                    x2_copy= np.copy(x[sel4])
                    y2_copy= np.copy(y[sel4])
                    x[sel4] = y2_copy
                    y[sel4] = x2_copy

                #x = x*fix_pos[0]
                #y = y*fix_pos[1]
            else:
                pass

        else : # there are no particles
            x=np.empty(0)
            y=np.empty(0)
            #z=np.empty(0)
            rho=np.empty(0)

        # compute boundaries
        if xrange>0 :  # there is a range
            xmin = -xrange
            xmax =  xrange
            ymin = -xrange
            ymax =  xrange
        else:  # there is no range, we take min/max x/y values
            xmin = x.min()
            xmax = x.max()
            ymin = y.min()
            ymax = y.max()


        # data points xrange
        data_ymin = ymin
        data_ymax = ymax
        data_xmin = xmin
        data_xmax = xmax
        # view area xrange
        view_ymin = ymin
        view_ymax = ymax
        view_xmin = xmin
        view_xmax = xmax

        if self.__vdebug and x.size > 0 and y.size > 0:
            print("view xmin/xmax, ymin,ymax",xmin,xmax,ymin,ymax,file=sys.stderr)
            print("data xmin/xmax, ymin,ymax",x.min(),x.max(),y.min(),y.max(),file=sys.stderr)
        # get visible data points
        xlvis = x
        ylvis = y
        if self.__vdebug:
            print("x.size= ", x.size)
        xx=x.size

        DPI = fig.get_dpi()
        if self.__vdebug:
            print ("DPI:", DPI)
        DefaultSize = fig.get_size_inches()
        if self.__vdebug:
            print ("Default size in Inches", DefaultSize)
        width = self.dimx #width  = DPI*DefaultSize[0]
        height= self.dimy #height = DPI*DefaultSize[1]

        if self.__vdebug:
            print ("Which should result in a %i x %i Image"%(width,height))

        # gaussian filter
        t1 = time.clock()
        sigma=sigma_ori
        if self.__vdebug:
            print("Sigma re-computed=",sigma)
        zd = self.__grid_density_gaussian_filter(view_xmin, view_ymin, view_xmax, view_ymax, width,height, x, y, sigma,rho)
        if self.__vdebug:
            print("Gaussian filtering : [%.3f] sec"%(time.clock()-t1),file=sys.stderr)
        # plot time text
        xtext=(view_xmin+0.05*(view_xmax-view_xmin))
        ytext=(view_ymin+0.90*(view_ymax-view_ymin))

        xtext=0.05
        ytext=0.95
        if row==0:
            disp_comp=component
            if not nopart: # display particles number
                disp_comp=disp_comp+":%d"%x.size
            ax.text(xtext,ytext,disp_comp,style='italic',color='black',bbox={'facecolor':'white',
                    'alpha':0.2, 'pad':10},verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)

        #ax.imshow(zd , origin='lower',cmap=cmap,interpolation='nearest', norm = matplotlib.colors.LogNorm(),
        #          extent=[view_xmin, view_xmax, view_ymin, view_ymax])
        #ax.imshow(zd , origin='lower',cmap=cmap, norm = matplotlib.colors.LogNorm(),
        #          extent=[view_xmin, view_xmax, view_ymin, view_ymax])

        img=ax.imshow(zd , origin='lower',cmap=cmap, norm = matplotlib.colors.LogNorm(),extent=[view_xmin, view_xmax, view_ymin, view_ymax])

        if self.__circle!="" :
            for prop in self.__circle.split(","):
                radius=prop.split("%")
                lstyle="solid" 
                color="red"
                if len(radius) > 1:
                    color=radius[1].split("#")
                    if len(color) > 1:
                        lstyle=color[1]
                cc=plt.Circle((0.,0.),float(radius[0]),color=str(color[0]),linestyle=lstyle,fill=False)
                ax.add_artist(cc)
        #cax=fig.add_axes(np.linspace(np.log(zd.min()),np.log(zd.max()),4))

        #fig.colorbar(img,orientation='vertical',shrink=0.8,ticks=[np.linspace(1,zd.max(),15)])
        #plt.contour(zd, origin='lower',levels=[0,0.5,1,2,3,4,5,6,7,8,9,20,40],cmap='winter', norm = matplotlib.colors.LogNorm() )
        if contour:
            tc = time.clock()
            plt.contour(zd, origin='lower',levels=np.logspace(np.log(zd.min()),np.log(zd.max()),nc),cmap='winter', norm = matplotlib.colors.LogNorm(),extent=[view_xmin, view_xmax, view_ymin, view_ymax] )
            if self.__vdebug:
                print("Contour : [%.3f] sec"%(time.clock()-tc),file=sys.stderr)

        #plt.contour(zd, origin='lower',levels=np.linspace(np.log(zd.min()),np.log(zd.max()),50),cmap='winter', norm = matplotlib.colors.LogNorm() )

        # to plot contour, comment out the following line
        #plt.contour(zd, origin='lower',levels=[0,1,2,3,4,5,6,7,8,9,20,40],cmap='winter',norm = matplotlib.colors.LogNorm(), extent=[view_xmin, view_xmax, view_ymin, view_ymax])
        #

        #plt.contour(zd, origin='lower',levels=[0,1,2,3,4,5,6,7,8,9,20,40,zd.max(),zd.min()],cmap='winter',norm = matplotlib.colors.LogNorm(),extent=[view_xmin, view_xmax, view_ymin, view_ymax])


        #from IPython import embed
        #embed()
        #plt.contour(zd, origin='lower',cmap='winter',norm = matplotlib.colors.LogNorm(), extent=[view_xmin, view_xmax, view_ymin, view_ymax])
        #plt.contour(zd,norm = matplotlib.colors.LogNorm(), extent=[view_xmin, view_xmax, view_ymin, view_ymax])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
def commandLinePbm2():
    dbname = None
    import argparse
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
    processPbm2(args)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
def processPbm2(args):
    import unsiotools.simulations.c2dplot as c2d
    movie = c2d.C2dplot(verbose_debug=args.verbose)
    try:
        movie.buildMovie(args.simname,overwrite=args.overwrite,ncores=args.ncores)
    except Exception as x :
        import traceback
        print (x,file=sys.stderr)
        traceback.print_exc(file=sys.stdout)
    except KeyboardInterrupt:
        sys.exit()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse
    # help
    parser = argparse.ArgumentParser(description="Display 2D image from UNS data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('snapshot', help="uns input snapshot",default=None)
    parser.add_argument('component', help="selected component",default=None)
    parser.add_argument('--out', help="if blank display on screen, else on given file ",default="",type=str)
    parser.add_argument('--range', help="plot range",default=20,type=str)
    parser.add_argument('--cmap', help="color map name. You can use a common cmap for all components, or a specific one.\
                        Syntax is \"component1:cmap1,component2:cmap2\"\
                        example: stars:rainbow,halo:Purples\n \
                        (to display all colormap available use \"show\" as keyword)",
                        default="gas:jet,stars:Paired,halo:Accent")
                        #other cmap="gas:jet,stars:rainbow,halo:PuOr"
    parser.add_argument('--mergers', help="use results from mergers analysis to re-center (ex; @mdf648) to get file automatically from simulation ",default="",type=str)
    parser.add_argument('--cod', help="use COD file to re-center, or @sim (ex; @mdf648) to get file automatically from simulation ",default=None)
    parser.add_argument('--rect_sim', help="give a simname or a rectify file name to activate rectify",default=None)
    parser.add_argument('--rect_comp', help="used component based file, eg 'stars-stars' or 'gas-stars'",default="stars-stars")
    parser.add_argument('--rect_dir', help="rectify directory name",default="rectify2")
    parser.add_argument('--rect_suffix',help="rectify suffix file name",default="ev")
    parser.add_argument('--sigma', help="gaussian sigma ",default=6.,type=float)
    parser.add_argument('--noxz',help='no XZ projection',dest="noxz", action="store_true", default=False)
    parser.add_argument('--nopart',help='not display particles number',dest="nopart", action="store_true", default=False)
    parser.add_argument('--contour',help='toggle iso contour display',dest="contour", action="store_true", default=False)
    parser.add_argument('--circle',help='Draw circles with given radius{%%color#linestyle}[,radius1,radius2] centered in 0,0,0.'
                                        'Eg. 1.5%%red#dashed,2.6%%yellow#dotted, use real name for color, like red,yellow etc.., possible linestyle={solid,dashed,dashdot,dotted} ',dest="circle", default="", type=str)
    parser.add_argument('--nc',help='#levels contour',default=20,type=int)
    parser.add_argument('--cpt', help="index of the image (out.cpt.jpg)",default=0,type=int)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)

    #parser.print_help()

     # parse
    args = parser.parse_args()

    if args.cmap=="show": # show colormap
        import unsiotools.general.ctools as ct
        ct.displayColormap()
        sys.exit()

    # start main funciton
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    # select matplotlib backend
    if args.out!= "": # non interactive
        import matplotlib
        matplotlib.use('Agg')

    # we import this modules here because
    # matplotlib.use() must be done before importing matplotlib.pyplot
    import unsiotools.simulations.c2dplot as c2d
    import unsiotools.simulations.csnapshot as csnap
    try:
        cpt = args.cpt
        uns=csnap.CSnapshot(args.snapshot,args.component,verbose_debug=args.verbose)
        #ok=uns.nextFrame("")
        while(uns.unsin.nextFrame("")):
            c=c2d.C2dplot(verbose_debug=args.verbose)
            c.fullProcess(uns=uns,out=args.out,component=args.component,xrange=float(args.range),sigma=args.sigma,
                          mergers=args.mergers,cmap=args.cmap,cpt=cpt,noxz=args.noxz, contour=args.contour,
                          nc=args.nc,center_cod=args.cod,nopart=args.nopart,
                          rect_sim=args.rect_sim,rect_comp=args.rect_comp,rect_dir=args.rect_dir,rect_suffix=args.rect_suffix, circle=args.circle)
            cpt =cpt+1
#        else:
#            print ("[%s] is not a UNS snapshot ..."%(simname))
    except Exception as x :
        import traceback
        print (x,file=sys.stderr)
        traceback.print_exc(file=sys.stdout)
    except KeyboardInterrupt:
        sys.exit()


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
