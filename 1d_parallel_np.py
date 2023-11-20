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
file_name = f'data/1d/parallel/{L}/{L}_{iteration}_{chunk}.dat'
os.makedirs(f'data/1d/parallel/{L}', exist_ok=True)
print(jobname)
if os.path.isfile(file_name):
    os.remove(file_name)

@jit
def toppoling(h,active_sites,outflow,area,s):
    for x in active_sites:
        h[x] -= 2
        s += 1
        for _ in range(2):
            p = np.random.rand()
            if p < 0.5:#right
                dx = 1
                #print('r')
            else:
                dx = -1
                #print('l')
            if 0 <= x + dx < L:
                h[x+dx] += 1
                area[x+dx] = True
            else:
                outflow += 1
    return h,active_sites,outflow,area,s
@jit
def fas(h):
    return np.where(1 < h)[0]

def main_loop(h):
    area = np.full((L), False)
    outflow,t,s = 0,0,0

    add_grain_index = np.random.randint(low=0,high=L)
    h[add_grain_index] += 1
    area[add_grain_index] = True

    active_sites = fas(h)
    while len(active_sites):
        t += 1
        h,active_sites,outflow,area,s = toppoling(h,active_sites,outflow,area,s)
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