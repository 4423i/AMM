import os,json
from collections import deque
import numpy as np

with open('config.json') as f:
    config = json.load(f)
dimension = '1d'
L = np.power(2,config[dimension]['N'])
h_c = config[dimension]['h']
iteration = 10**int(config[dimension]['iteration'])
jobname = f'{dimension}_{L}_{iteration}'
file_name = f'data/seq/{L}_{iteration}.dat'
print(jobname)
if os.path.isfile(file_name):
    os.remove(file_name)

def main_loop(h):
    L = len(h)
    active_sites = []
    area = [False for _ in range(L)]
    outflow,t,s,a = 0,0,0,set()

    add_grain_index = np.random.randint(low=0,high=L)
    h[add_grain_index] += 1
    area[add_grain_index] = True

    active_sites = [i for i,v in enumerate(h) if 1 < v]
    while len(active_sites):
        t += 1/len(active_sites)
        #print(h)
        np.random.shuffle(active_sites)
        x = active_sites[0]
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
            #print(f'toppled {h}')
        active_sites = [i for i,v in enumerate(h) if 1 < v]
    a = sum(area)
    rho = np.mean(h)
    return h,outflow,t,s,a,rho

h = [0 for _ in range(L)]
Outflows = []
for _ in range(100000):
    h,outflow,time,size,area,rho = main_loop(h)
with open(file_name, 'a') as f:
    f.write(f"outflow,time,size,area,rho\n")
for _ in range(iteration):
    h,outflow,time,size,area,rho = main_loop(h)
    with open(file_name, 'a') as f:
        f.write(f"{outflow},{time},{size},{area},{rho}\n")