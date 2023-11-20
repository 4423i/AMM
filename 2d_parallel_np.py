import os
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Abelian Manna Model on 1d')
    parser.add_argument('--h_c', metavar='h_c',dest='h_c', type=int, default=2)
    parser.add_argument('--initial', metavar='initial',dest='initial', type=int, default=100000)
    parser.add_argument('--L', metavar='L', dest='L', type=int)
    parser.add_argument('--iter', metavar='iter', dest='iter', type=int)
    parser.add_argument('--chunk', metavar='chunk', dest='chunk', type=str)
    return parser.parse_args()
args = parse_args()

dimension = '2d'
h_c = args.h_c
initial = args.initial
L = args.L
iteration = args.iter
chunk = args.chunk
jobname = f'{dimension}_{L}_{iteration}_{chunk}'
file_name = f'data/2d/parallel/{L}/{L}_{iteration}_{chunk}.dat'
os.makedirs(f'data/2d/parallel/{L}', exist_ok=True)
print(jobname)
if os.path.isfile(file_name):
    os.remove(file_name)

def toppoling(h,active_sites,outflow,area,s):
    new_sites = []
    for y,x in active_sites:
        h[y,x] -= 2
        if 1 < h[y,x]:
            new_sites.append([y,x])
        s += 1
        for _ in range(2):
            p = np.random.rand()
            if p < 0.25:#right
                dx,dy = 1,0
            elif p < 0.5:
                dx,dy = -1,0
            elif p < 0.75:
                dx,dy = 0,1
            else:
                dx,dy = 0,-1

            if 0 <= x + dx < L:
                if 0 <= y + dy < L:
                    h[y+dy,x+dx] += 1
                    area[y+dy,x+dx] = True
                    if 1 < h[y+dy,x+dx]:
                        new_sites.append([y+dy,x+dx])
                else:
                    outflow += 1
            else:
                outflow += 1
    active_sites = np.unique(new_sites, axis=0)
    return h,active_sites,outflow,area,s

def main_loop(h):
    area = np.full((L,L), False)
    outflow,t,s = 0,0,0

    ry = np.random.randint(low=0,high=L)
    rx = np.random.randint(low=0,high=L)
    h[ry, rx] += 1
    area[ry, rx] = True
    active_sites = []
    if 1 < h[ry, rx]:
        active_sites.append([ry,rx])
    active_sites = np.array(active_sites)
    while len(active_sites):
        t += 1
        h,active_sites,outflow,area,s = toppoling(h,active_sites,outflow,area,s)
    a = sum(sum(area))
    rho = np.mean(h)
    return h,outflow,t,s,a,rho

h = np.zeros((L,L))

for _ in range(initial):
    h,outflow,time,size,area,rho = main_loop(h)

with open(file_name, 'a') as f:
    f.write(f"outflow,time,size,area,rho\n")
for _ in range(iteration//100):
    h,outflow,time,size,area,rho = main_loop(h)
    with open(file_name, 'a') as f:
        f.write(f"{outflow},{time},{size},{area},{rho}\n")