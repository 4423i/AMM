import numpy as np
def main_loop(h):
    L = len(h)
    active_sites = []
    outflow,t,s,a = 0,0,0,set()

    add_grain_index = 1
    h[add_grain_index] += 1
    a.add(add_grain_index)
    if 1 < h[add_grain_index]:
        active_sites.append(add_grain_index)
    while len(active_sites):
        t += 1/len(active_sites)
        #print(h)
        #np.random.shuffle(active_sites)
        x = active_sites[0]
        active_sites = active_sites[1:]
        h[x] -= 2
        s += 1
        P = [0,1]
        for j in range(2):
            p = P[j]#np.random.rand()
            if p < 0.5:#right
                dx = 1
                #print('r')
            else:
                dx = -1
                #print('l')
            if 0 <= x + dx < L:
                h[x+dx] += 1
                a.add(x+dx)
            else:
                outflow += 1
            #print(f'toppled {h}')
        active_sites = [i for i,v in enumerate(h) if 1 < v]
    rho = np.mean(h)
    return h,outflow,t,s,a,rho

test_numer = 2
for _ in range(test_numer):
    file_name = f'seq/{_}.test'
    with open(file_name) as f:
        input_h = list(map(int,f.readline().replace('\n','').split(' ')))
        answer = list(map(int,f.readline().replace('\n','').split(' ')))
        t = int(f.readline())
        s = int(f.readline())
        a = int(f.readline())


        h,T,S,A = main_loop(input_h)
        if (h,T,S,A) != (answer,t,s,a):
            print('error')
            print('expected',answer,t,s,a)
            print('logic',h,T,S,A)
            exit()