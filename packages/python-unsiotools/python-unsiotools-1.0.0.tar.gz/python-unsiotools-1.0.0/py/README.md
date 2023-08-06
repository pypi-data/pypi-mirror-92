
## ABOUT
UNSIOTOOLS contains a collection of [unsio](https://projets.lam.fr/projects/unsio) based programs and depends of the [Nemo](https://teuben.github.io/nemo/) package.
You have access to [falcON](https://iopscience.iop.org/article/10.1086/312724/pdf) algorithm to compute density and gravity.


## Installing python wrapper
```
pip install python-unsiotools -U
```
## To get some docstring help
```
# Help on falcON class
pydoc unsiotools.simulations.cfalcon
```
## Usage

- In the example below, we load a RAMSES simulation, and compute density on HALO particles
```python
import unsio.input as uns_in  # unsio reading module
import unsiotools.simulations.cfalcon as falcon

myfile="/home/jcl/output_00004" # input RAMSES simulation
# we instantiate a CUNS_IN object
my_in=uns_in.CUNS_IN(myfile,"halo") # We select components HALO
#
# Reading
#
if my_in.nextFrame(): # load snapshot
  # read halo positions
  status,pos=my_in.getData("halo","pos")
  # read halo mass
  status,mass=my_in.getData("halo","mass")
  # read time simulation
  status,timex=my_in.getData("time")

# we compute density
cf=falcon.CFalcon()
ok,rho,hsml=cf.getDensity(pos,mass)

print("Rho=",rho)
```
- In this more simple example, we compute density on random data. Note that data must be in **float32** format
```python
import unsiotools.simulations.cfalcon as falcon
import numpy as np

pos=np.float32(np.random.random_sample((300,)))
mass=np.float32(np.random.random_sample((100,)))

cf=falcon.CFalcon()

ok,rho,hsml=cf.getDensity(pos,mass)

print(ok,rho)

```

## Licence
UNSIOTOOLS is open source and released under the terms of the [CeCILL2 Licence](http://www.cecill.info/licences/Licence_CeCILL_V2-en.html)

## Webpage
PLease visit :
- [UNSIO project home page](https://projets.lam.fr/projects/unsio)
- [UNSIO Python reading manual](https://projets.lam.fr/projects/unsio/wiki/PythonReadDataNew)
- [UNSIO Python writing manual](https://projets.lam.fr/projects/unsio/wiki/PythonWriteDataNew)
- [UNSIO Pypi page](https://pypi.org/project/python-unsio/)
- [NEMO home page](https://teuben.github.io/nemo/)

## Copyright
**Copyright Jean-Charles LAMBERT**     
**Jean-Charles.Lambert_at_lam.fr**     
