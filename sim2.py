import simpy
import scipy.stats as stats
from lcg import lcg

def checkIn(env,cind,pty,counters,st,iat):
    # cind is cutomer index, ctype is priority or normal customer
    ctype="high" if (pty==0) else "normal"
    tm=0
    for i in range(0,cind):
        tm=tm+iat[i]
    if (cind != 0):
        yield env.timeout(tm)
    print('Customer %d with %s prority arrived at %.2f'%(cind+1,ctype,env.now))
    with counters.request(priority=pty) as req:
        yield req
        print('Customer %d with %s priority started check in at %.2f'%(cind+1,ctype,env.now))
        yield env.timeout(st[cind])
        print('Customer %d with %s priority finished check in and leaving at %.2f'%(cind+1,ctype,env.now))

# generate 9 random no.s using lcg
def genrn ():
    r1 = lcg(3,5,0,99,99+100+100).gen()
    return r1
# generates pty for customers
def genpty(rnum,ndig):
    ch = rnum/(10**ndig)
    res=1
    if (ch<=0.1): 
        res =0
    return res
r1 = genrn()
# inter arrival time generation
iat = [stats.expon.ppf(r1[i],scale = 5) for i in range(0,99)]
# service time generation
w = [24,76,0]
bin_edges = [0,5,10,15]
st = [stats.rv_histogram((w,bin_edges)).ppf(r1[i]) for i in range(99,199)]
# rnos for priority generation
rpty = [r1[i] for i in range(199,299)]

env = simpy.Environment()
counters = simpy.PriorityResource(env,capacity=2)
for i in range(0,100):
    pty = genpty(rpty[i],0)
    env.process(checkIn(env,i,pty,counters,st,iat))
env.run()
