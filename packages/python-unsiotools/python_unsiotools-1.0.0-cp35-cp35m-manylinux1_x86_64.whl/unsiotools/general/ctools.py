#!/usr/bin/python
from __future__ import print_function

import numpy as np
import sys,os

class CTools:
    """Usefull methods"""
#
# ----
#
    def __init__(self):
        pass

#
# ----
#
def displayColormap():
    """
    Display matplotlib colormap
    """
    import matplotlib.pyplot as plt

    a = np.linspace(0, 1, 256).reshape(1,-1)
    a = np.vstack((a,a))

    # Get a list of the colormaps in matplotlib.  Ignore the ones that end with
    # '_r' because these are simply reversed versions of ones that don't end
    # with '_r'
    maps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))
    nmaps = len(maps) + 1

    fig = plt.figure(figsize=(5,10))
    fig.subplots_adjust(top=0.99, bottom=0.01, left=0.2, right=0.99)
    for i,m in enumerate(maps):
        ax = plt.subplot(nmaps, 1, i+1)
        plt.axis("off")
        plt.imshow(a, aspect='auto', cmap=plt.get_cmap(m), origin='lower')
        pos = list(ax.get_position().bounds)
        fig.text(pos[0] - 0.01, pos[1], m, fontsize=10, horizontalalignment='right')

    plt.show()        
#
# ----
#
def rotateFile(infile,sep=".",debug=False):
    """
    rotate infile by adding separator 'sep' + incremental digit
    example :
    infile="hello"
    if "hello" exist, then "hello.0" or "hello.1" ..... name will replace "hello"

    return bool,outfile
    
    bool is True if file has been rotated
    
    """

    outfile=infile
    rot=False
    if os.path.exists(infile):
        if debug:
            print("File/dir/link [%s] exist.."%(infile),file=sys.stderr)
        cpt=0
        stop=False
        rot=True
        while not stop:
            outfile="%s%s%d"%(infile,sep,cpt)
            if not os.path.exists(outfile):
                stop=True
            else:
                cpt=cpt+1

        os.rename(infile,outfile)
        if debug:
            print("Rotate file [%s] to [%s]"%(infile,outfile),file=sys.stderr)

    return rot,outfile
