#!python
#
# TEST CFalcon class
#
import unsiotools.simulations.cfalcon as falcon
from hashlib import sha1
import numpy as np

np.random.seed(666)
pos=np.float32(np.random.random_sample((300,)))
mass=np.float32(np.random.random_sample((100,)))

cf=falcon.CFalcon()

ok,rho,hsml=cf.getDensity(pos,mass)

print(ok,rho)
ref_rho=int('250b01261fe96162b043b27e6cba643052c0e867',16)
ref_hsml=int('1bd01498d33a400ccbd7a841a74572960e869b19',16)
sha1_rho=int(sha1(rho).hexdigest(),16)
sha1_hsml=int(sha1(hsml).hexdigest(),16)

print("Reference :")
print("sha1(rho )=",ref_rho)
print("sha1(hsml)=",ref_hsml)
print("Computed :")
print("sha1(rho )=",sha1_rho)
print("sha1(hsml)=",sha1_hsml)
print("diff:",ref_rho-sha1_rho," ",ref_hsml-sha1_hsml)
