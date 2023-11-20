import os,json
from collections import deque
import numpy as np

with open('config.json') as f:
    config = json.load(f)
dimension = '2d'
L = np.power(2,config[dimension]['N'])
h_c = config[dimension]['h']
iteration = 10**int(config[dimension]['iteration'])
jobname = f'{dimension}_{L}_{iteration}'
file_name = f'data/{dimension}/{L}_{iteration}.dat'
print(jobname)
if os.path.isfile(file_name):
    os.remove(file_name)

def main_loop(h):
    #print('loooping')
    outflow = 0
    avalanche_area = set()
    avalanche_size = 0
    avalanche_time = 0

    rx = np.random.randint(low=0, high=L, size=None, dtype=int)
    ry = np.random.randint(low=0, high=L, size=None, dtype=int)
    h[ry][rx] += 1
    avalanche_area.add(f'{ry}:{rx}')

    que = deque()
    if h_c <= h[ry][rx]:
        que.append([rx,ry])
    #avalanche cnt start
    while True:
        newque = deque()
        if len(que) > 0:
            avalanche_time += 1
            while que:
                x,y = que.pop()
                if h_c <= h[y][x]:
                    h[y][x] -= h_c
                    avalanche_size += 1
                    for _ in range(h_c):
                        p = np.random.rand()
                        if p <= 0.25:
                            dx = 1
                            dy = 0
                        elif p <= 0.5:
                            dx = -1
                            dy = 0
                        elif p <= 0.75:
                            dx = 0
                            dy = 1
                        else:
                            dx = 0
                            dy = -1
                        if 0 <= x+dx < L:
                            if 0 <= y+dy < L:
                                h[y+dy][x+dx] += 1
                                avalanche_area.add(f'{y+dy}:{x+dx}')
                                if h_c <= h[y+dy][x+dx]:
                                    newque.append([x+dx,y+dy])
                            else:
                                outflow += 1
                        else:
                            outflow += 1
            que = newque
        else:
            break

    average_height = np.mean(h)
    return h,outflow,avalanche_size,avalanche_time,len(avalanche_area),average_height

h = [[0 for _ in range(L)] for _ in range(L)]

window_param = 1000
Outflows = []
for _ in range(window_param):
    h,outflow,avalanche_size,avalanche_time,avalanche_area,average_height = main_loop(h)
    Outflows.append(outflow)
Outflow_sum = sum(Outflows)
Outflows = deque(Outflows)
thermalisation = 0
while True:
    thermalisation += 1
    h,outflow,avalanche_size,avalanche_time,avalanche_area,average_height = main_loop(h)
    left = Outflows.popleft()
    Outflows.append(outflow)
    if len(Outflows) != window_param:
        print('error')
        exit()
    Outflow_sum -= left
    Outflow_sum += outflow

    mean_outflow = Outflow_sum / window_param

    if abs(mean_outflow-1) < 0.1/100:
        break
print('initialization',thermalisation)

for _ in range(iteration):
    h,outflow,avalanche_size,avalanche_time,avalanche_area,average_height = main_loop(h)
    with open(file_name, 'a') as f:
        f.write(f"{outflow},{avalanche_size},{avalanche_time},{avalanche_area},{average_height}\n")