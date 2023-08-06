#!/usr/bin/python
from __future__ import print_function

import sqlite3
import os,sys,glob

class UnsSimu:
    'sqlite3 management for UNS sqlite3 database'
    __conn=0    # connection database handler
    name=""   # simulation name
    dbname="/pil/programs/DB/simulation.dbl" # database simulation name
    __status=1
    __dbunsio=".unsio"
    __verbose=False
    # constructor
    def  __init__(self,name=None,dbname=None,verbose=False) :
        self.name=name
        self.__verbose=verbose
        if (dbname is not None ) :
            self.dbname = dbname
            if (not os.path.isfile(dbname)) :
                print('sqlite3 db file ['+dbname+'] does not exist...\n',file=sys.stderr)
                self.__status = 0;
            else :
                self.__conn = sqlite3.connect(dbname)
                self.__status = 1
        else : # we must parse .unsio file
            status,self.dbname=self.parseDotUnsio("")
            try:
                self.__conn = sqlite3.connect(self.dbname)
                c = self.__conn.cursor()
                c.execute("select name from eps") # try a request to check if sdb3 is valid
            except sqlite3.Error:
                print ("File [",self.dbname,"] is not a valid sqlite3 DB",file=sys.stderr)
                sys.exit()


        #print "CONN = ",self.__conn
        if (self.__conn != 0):
            self.__conn.row_factory = sqlite3.Row

        # try to get info
        info=self.getInfo()

    # parse $HOME/.unsio file to detect db file name
    def parseDotUnsio(self,file):
        inputfile =file
        if (file == "" ):
            inputfile=os.environ['HOME']+"/"+self.__dbunsio
            #print ("Input file:",inputfile)

        gparam={}
        try:
            gp=open(inputfile,"r")
        except IOError:
            print ("no file ["+inputfile+"], will use default :"+self.dbname,file=sys.stderr)
            return False,self.dbname

        for line in gp:
            data=line.split()
            if (len(data)>1 and data[0][0]!='%' and data[0][0]!='#'):
                gparam[data[0]] = data[2]
                #print(">>", data[0], " -- ",gparam[data[0]])

        if ('dbname' in gparam and gparam['dbname']!="") :
            if (not os.path.isfile(gparam['dbname'])) :
                print ("FILE [",gparam['dbname'],"] does not exist !!",file=sys.stderr)
                return False, self.dbname
            else :
                return True,gparam['dbname']
        else:
            return False,self.dbname


    def printInfo(self,name=None):
        if name is None:
            name=self.name
        r = self.getInfo(name)
        if (r):
            for keys in r.keys():
                print ( keys," : ",r[keys],file=sys.stderr)            #for row in cursor:

    def getInfo(self,name=None):
        if name is None:
            name=self.name
        if ( self.__status) :
            self.__conn.text_factory = bytes
            c = self.__conn.cursor()
            sql="select * from info where name=='"+name+"'"
            cursor=c.execute(sql)
            #all_rows = c.fetchall()
            #print('1):', all_rows)
            r = c.fetchone()
            rr={}
            if r is None:
                raise  Exception("Simulation %s does not belong to uns database"%(name))
            else :
                for keys in r.keys():
                    rr[keys]=r[keys].decode('UTF-8')

            return rr


    def _listSnap(self,base,ext=""):
        snap_list = sorted(glob.glob(base+'_?'+ext))
        snap_list = snap_list+sorted(glob.glob(base+'_??'+ext))
        snap_list = snap_list+sorted(glob.glob(base+'_???'+ext))
        snap_list = snap_list+sorted(glob.glob(base+'_????'+ext))
        snap_list = snap_list+sorted(glob.glob(base+'_?????'+ext))
        return snap_list

    def getSnapshotList(self,name=None):
        if name is None:
            name=self.name
        r = self.getInfo(name)
        if (r and ( r['type']=="Gadget" or r['type']=="Gadget3") ):
            if ( os.path.exists(r['dir'] )):
                base = r['dir']+"/"+r['base']

                snap_list=self._listSnap(base)
                if len(snap_list)==0:
                    snap_list=self._listSnap(base,'.hdf5') #try hdf5 extension
                return snap_list
            else:
                print("Path [%s] does not exist.."%(r['dir']),file=sys.stderr)
        else:
            print("fails....",file=sys.stderr)


#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    import argparse
    dbname=None
    ncores=None

    # help
    parser = argparse.ArgumentParser(description="Test UnsSimu class",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('--verbose',help='verbose mode', default=False)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        unsimu=UnsSimu(args.simname)
        unsimu.printInfo()
        print(unsimu.getSnapshotList())

    except Exception as x :
        print (x.message)

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
