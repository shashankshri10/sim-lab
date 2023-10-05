import simpy
import scipy.stats as stats
from lcg import lcg

# generate 9 random no.s using lcg

def genrn ():
    r1 = lcg(3,5,0,99,9).gen()
    return r1
r1 = genrn()
# now slice the array from els range(0,4) and range(4,9)
iat = [stats.expon.ppf(r1[i],scale = 0.2) for i in range(0,4)]
w = [24,76,0]
bin_edges = [0,5,10,15]
st = [stats.rv_histogram((w,bin_edges)).ppf(r1[i]) for i in range(4,9)]
