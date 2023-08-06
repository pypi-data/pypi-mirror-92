#!/usr/bin/env python

import sys
import argparse
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
