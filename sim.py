import simpy
import scipy.stats as stats
from lcg import lcg

# generate 9 random no.s using lcg

def genrn ():
    r1 = lcg(3,5,0,99,9).gen()
    return r1
r1 = genrn()
# now slice the array from els range(0,4) and range(4,9)
