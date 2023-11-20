import os
import numpy as np
import argparse
from numba import jit

def parse_args():
    parser = argparse.ArgumentParser(description='Abelian Manna Model on 1d')
    parser.add_argument('--h_c', metavar='h_c',dest='h_c', type=int, default=2)
    parser.add_argument('--initial', metavar='initial',dest='initial', type=int, default=100000)
    parser.add_argument('--L', metavar='L', dest='L', type=int)
    parser.add_argument('--iter', metavar='iter', dest='iter', type=int)
    parser.add_argument('--chunk', metavar='chunk', dest='chunk', type=str)
    return parser.parse_args()
args = parse_args()

dimension = '1d'
h_c = args.h_c
initial = args.initial
L = args.L
iteration = args.iter
chunk = args.chunk
jobname = f'{dimension}_{L}_{iteration}_{chunk}'
file_name = f'data/seq/{L}/{L}_{iteration}_{chunk}.dat'
os.makedirs(f'data/seq/{L}', exist_ok=True)
print(jobname)
if os.path.isfile(file_name):
    os.remove(file_name)

@jit
def toppling(h,active_sites,outflow,area,s):
    # I randomly pick up toppling site in actite_sites
    ri = np.random.randint(low=0,high=len(active_sites))
    x = active_sites[ri]
    h[x] -= 2
    s += 1
    for _ in range(2):
        p = np.random.rand()
        if p < 0.5:
            dx = 1
        else:
            dx = -1
        if 0 <= x + dx < L:
            h[x+dx] += 1
            area[x+dx] = True
        else:
            outflow += 1
    return h,active_sites,outflow,area,s

@jit
def fas(h):
    # Finding active sites
    # this function returns index of actives sites
    return np.where(1 < h)[0]

def main_loop(h):
    #Initialise avalanche observable
    area = np.full((L), False)
    outflow,t,s = 0,0,0

    add_grain_index = np.random.randint(low=0,high=L)#Chose a random site on the lattice
    h[add_grain_index] += 1
    area[add_grain_index] = True

    active_sites = fas(h)
    while len(active_sites):#If there is active sites, the toppling start
        t += 1/len(active_sites)
        h,active_sites,outflow,area,s = toppling(h,active_sites,outflow,area,s)
        #after toppling, recount the active sites
        active_sites = fas(h)
    a = sum(area)
    rho = np.mean(h)
    return h,outflow,t,s,a,rho

h = np.zeros(L)

for _ in range(initial):
    h,outflow,time,size,area,rho = main_loop(h)

with open(file_name, 'a') as f:
    f.write(f"outflow,time,size,area,rho\n")
for _ in range(iteration//100):
    h,outflow,time,size,area,rho = main_loop(h)
    with open(file_name, 'a') as f:
        f.write(f"{outflow},{time},{size},{area},{rho}\n")