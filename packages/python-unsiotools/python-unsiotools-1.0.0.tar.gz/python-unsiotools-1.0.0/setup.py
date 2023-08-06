#!/usr/bin/env python

"""

>> PACKAGING

Dependencies :
==============
apt-get install python3-stdeb fakeroot python3-all-dev python3-all swig python3-numpy python3-setuptools
apt-get install python-stdeb fakeroot python-all-dev python-all swig python-numpy python-setuptools libsqlite3-dev
( see https://pypi.org/project/stdeb/)

NEMO (https://github.com/teuben/nemo)
you must have NEMO package installed (especially falcON) to build this module

To build RPM :
==============
python3 setup.py  bdist_rpm --release 1mga6

To build deb package :
======================
python3 setup.py --command-packages=stdeb.command bdist_deb sdist_dsc --with-python2=True --with-python3=True --dist-dir=my_deb --debian-version 0ubuntu16.04

To build MacOSX :
=================
1) use clang compiler and python3
2) build
CC=/usr/bin/cc CXX=/usr/bin/c++ python3 setup.py build_ext -L ${HOME}/local/unsio/lib -R ${HOME}/local/unsio/lib
3) install locally
python3 setup.py install --user
4) set DYLD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=${HOME}/local/unsio/lib

>> INSTALL

to install locally :
====================
python3 setup.py install --user


"""

#from distutils.core import setup, Extension
import numpy,os,sys
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py
import platform

#  find out numpy include directory.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

#DEHNEN=$ENV{NEMO}/usr/dehnen
if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 4):
    raise RuntimeError("Python version 2.7 or >= 3.4 required.")

# detect python version (2 or 3)
pyversion="3"
if sys.version_info[0]<3 :
  pyversion=""

with open('py/README.md', 'r') as f:
    long_description = f.read()

# trick to add SWIG generated module
# see https://stackoverflow.com/questions/12491328/python-distutils-not-include-the-swig-generated-module
# and especially : https://stackoverflow.com/questions/29477298/setup-py-run-build-ext-before-anything-else/48942866#48942866
# and the fix for python2 https://stackoverflow.com/questions/1713038/super-fails-with-error-typeerror-argument-1-must-be-type-not-classobj-when/1713052#1713052

class build_py(_build_py, object):
    def run(self):
        self.run_command("build_ext")
        if pyversion == "":  # python2
            return super(build_py, self).run()
        else:                # python3
            return super().run()

#
# version management
#
MAJOR = '1'
MINOR = '0'
MICRO = '0'
VERSION = '%s.%s.%s' % (MAJOR, MINOR, MICRO)

#
# write_version : write unsio version in py/unsio/version.py file
# it's imported from __init__.py as __version__

def write_version_py(filename='py/unsiotools/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM PYTHON-UNSIO SETUP.PY
#
version = '%(version)s'
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION})

    finally:
        a.close()

# setup_package :
#

def setup_package():
    # generate version
    write_version_py()

    # detect if linux
    machine=platform.platform()
    LINUX=machine.lower().find("linux")
    if LINUX >= 0:
        # linux detected
        LIBGFORTRAN=["gfortran"]
    else:
        # should be a macosx machine, then no gfortran for pgplot
        LIBGFORTRAN=[]

    # metada for setup
    metadata = dict(
        name='python-unsiotools',
        version=VERSION,
        description='Python wrapper to unsiotools',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Jean-Charles LAMBERT',
        author_email='jean-charles.lambert@lam.fr',
        url='https://projets.lam.fr/projects/uns_projects',
        license='CeCILL2.1 (https://opensource.org/licenses/CECILL-2.1)',
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Programming Language :: C",
            "Programming Language :: C++",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering :: Astronomy",
            "Topic :: Software Development"],
        platforms=["Linux", "Mac OS-X", "Unix"],
        python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
        package_dir={'':'py'}, # all packages are under 'py' directory
        packages=['unsiotools', 'unsiotools/simulations','unsiotools/general'],
        cmdclass={'build_py': build_py},
        py_modules=['unsiotools/py_unstools'],
        ext_modules = [
            Extension("unsiotools/_py_unstools",
                      sources=[ "py/unsiotools/py_unstools.i"],
                      swig_opts=['-c++','-modern', '-DNO_CUDA -DNOBOOST',
                                 '-Isrc','-I./py/unsiotools', '-Iswig','-Ilib/utils','-Ilib/utils/nemodep', '-Ilib/projects/nemodep'],
                      include_dirs = [numpy_include,'src',
                                      'lib/utils',
                                      'lib/utils/nemodep',
                                      'lib/projects/nemodep',
                                      os.environ['NEMO']+'/usr/dehnen/utils',
                                      os.environ['NEMO']+'/usr/dehnen/utils/inc',
                                      os.environ['NEMO']+'/usr/dehnen/falcON',
                                      os.environ['NEMO']+'/usr/dehnen/falcON/inc',
                                      os.environ['NEMO']+'/usr/dehnen/falcON/public',
                                      os.environ['NEMO']+'/inc'
                      ],
                      extra_compile_args = ['-O2','-std=c++03'],
                      define_macros=[('NOBOOST',None),  # equivalent to -DNOBOOST
                                     ('falcON_SINGLE',None),
                                     ('falcON_NEMO',None),
                                     ('NO_CUDA',None) ],
                      # NOTE : libraries linking order is VERY important !!!
                      #libraries=['JCLutils', 'JCLprojects','unsio',  'WDutils', 'falcON', 'nemo','cpgplot', 'pgplot','sqlite3','X11','gfortran'],
                      libraries=['JCLutils', 'JCLprojects','unsio',  'WDutils', 'falcON', 'nemo','cpgplot', 'pgplot','sqlite3','X11']+LIBGFORTRAN,
                      library_dirs=['/tmp/local/unsio/lib','/usr/lib/x86_64-linux-gnu','/usr/lib64','/lib64',os.environ['HOME']+'/local/unsio/lib',os.environ['HOME']+'/local/unsio/lib64',
                                    os.environ['NEMO']+'/lib',
                                    os.environ['HOME']+'/local/unsio/lib/x86_64-linux-gnu',
                                    os.environ['NEMO']+'/usr/dehnen/utils/lib',
                                    os.environ['NEMO']+'/usr/dehnen/falcON/lib'],
                      runtime_library_dirs=['/usr/lib/x86_64-linux-gnu','/usr/lib64','/lib64',os.environ['HOME']+'/local/unsio/lib64',
                                            os.environ['HOME']+'/local/unsio/lib/x86_64-linux-gnu',
                                            os.environ['NEMO']+'/lib',
                                            os.environ['NEMO']+'/usr/dehnen/utils/lib',
                                            os.environ['NEMO']+'/usr/dehnen/falcON/lib' ]
            )
        ],
        scripts=[
            'py/mains/uns_extract_halo.py',
            'py/mains/age_to_density.py',
            'py/mains/uns_2dplot.py',
            "py/unsiotools/examples/test_cfalcon.py",
        ],
        entry_points={
            "console_scripts": [
                #"uns_2dplot.py       = unsiotools.simulations.c2dplot:commandLine",
                "uns_2dpgplot.py     = unsiotools.simulations.c2dpgplot:commandLine",
                "merging_time.py     = unsiotools.simulations.ccod:commandLineMT",
                "uns_cod.py          = unsiotools.simulations.ccod:commandLine",
                "uns_inert.py        = unsiotools.simulations.cinert:commandLine",
                "uns_plot_inert.py   = unsiotools.simulations.cplotinert:commandLine",
                "post_build_movie.py = unsiotools.simulations.cmovie:commandLine",
                "post_build_movie2.py = unsiotools.simulations.c2dplot:commandLinePbm2",
                "process_analysis.py = unsiotools.simulations.cuns_analysis:commandLine",
                "remove_sim_halo.py  = unsiotools.simulations.creducesim:commandLine",
                "ramses2gadget.py    = unsiotools.simulations.cramses2gadget:commandLine",
            ],
        },
        install_requires=['python-unsio','matplotlib','scipy','numpy'],
        setup_requires=['']
    )
    setup(**metadata)

# main
#
if __name__ == '__main__':
    setup_package()
