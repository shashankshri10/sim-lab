import simpy
import scipy.stats as stats
from lcg import lcg
import numpy as np

lines =["Event List Part 1\n"]
wtm=[0 for i in range(0,5)]
absarr=[0 for i in range(0,5)]
ttm=[0 for i in range(0,5)]
pcus=0
ncus=0
priority_cus_ind=[]
simstats=[]

def checkIn(env,cind,pty,counters,st,iat):
    # cind is cutomer index, ctype is priority or normal customer
    global ncus
    global pcus
    global wtm
    global absarr
    global ttm
    global priority_cus_ind
    ctype="high" if (pty==0) else "normal"
    if (pty==1):
        ncus+=1
    else:
        pcus+=1
        priority_cus_ind.append(cind)
    tm=0
    for i in range(0,cind):
        tm=tm+iat[i]
    if (cind != 0):
        yield env.timeout(tm)
    absarr[cind]=env.now
    lines.append('Customer %d with %s priority arrived at %.2f'%(cind+1,ctype,env.now))
    print('Customer %d with %s priority arrived at %.2f'%(cind+1,ctype,env.now))
    with counters.request(priority=pty) as req:
        yield req
        wtm[cind]=env.now-absarr[cind] # wait time in queue
        lines.append('Customer %d with %s priority started check in at %.2f'%(cind+1,ctype,env.now))
        print('Customer %d with %s priority started check in at %.2f'%(cind+1,ctype,env.now))
        yield env.timeout(st[cind])
        ttm[cind]=env.now-absarr[cind] # total time = wait tm + service tm
        lines.append('Customer %d with %s priority finished check in and leaving at %.2f'%(cind+1,ctype,env.now))
        print('Customer %d with %s priority finished check in and leaving at %.2f'%(cind+1,ctype,env.now))

# generate 9 random no.s using lcg
def genrn ():
    r1 = lcg(3,5,0,99,9).gen()
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
iat = [stats.expon.ppf(r1[i],scale = 5) for i in range(0,4)]
# service time generation
w = [24,76,0]
bin_edges = [0,5,10,15]
st = [stats.rv_histogram((w,bin_edges)).ppf(r1[i]) for i in range(4,9)]
# rnos for priority generation
rpty = [11164,36318,75061,33674,26320]

env = simpy.Environment()
counters = simpy.PriorityResource(env,capacity=2)
for i in range(0,5):
    pty = genpty(rpty[i],5)
    env.process(checkIn(env,i,pty,counters,st,iat))
env.run()
print('\n---Simulation finished---\n')
with open('sim1res.txt','w') as f:
    f.write('\n'.join(lines))
    f.close
simstats=["---Simulation Report Part 1---\n"]
def sim_stats(simstats):
    simstats.append('Average wait time = %.2f'% (np.mean(wtm)))
    simstats.append('Maximum wait time = %.2f'% (np.max(wtm)))
    simstats.append('Average total time = %.2f'% (np.mean(ttm)))
    simstats.append('Maximum total time = %.2f'% (np.max(ttm)))
    simstats.append('Total run time of the simulation = %.2f' %(ttm[4]+absarr[4]))
    simstats.append('Number of normal customers = %d'% (ncus))
    simstats.append('Number of Priority customers = %d'% (pcus))
    if (len(priority_cus_ind)!=0):
        val=0
        mval=-1
        for i in range(0,len(priority_cus_ind)):
            val+=wtm[priority_cus_ind[i]]
            mval=max(mval,wtm[priority_cus_ind[i]])
        val/=len(priority_cus_ind)
        simstats.append('Average wait time for priority customers = %.2f'% (val))
        simstats.append('Maximum wait time for priority customers = %.2f'% (mval))
    else:
        simstats.append('Average wait time for priority customers = N/A')
        simstats.append('Average wait time for priority customers = N/A')
        # print(absarr)
    print('\n---Statistics generated---\n')
    return simstats

simstats = sim_stats(simstats)
with open('sim1stats.txt','w') as f:
    f.write('\n'.join(simstats))
    f.close