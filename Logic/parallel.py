import numpy as np
def main_loop(h):
    L = len(h)
    active_sites = []
    outflow,t,s,a = 0,0,0,set()

    add_grain_index = 1
    h[add_grain_index] += 1
    a.add(add_grain_index)
    active_sites = [i for i,v in enumerate(h) if 1 < v]
    while True:
        if len(active_sites) == 0:
            break
        t += 1
        print(h)
        #np.random.shuffle(active_sites)
        for x in active_sites:
            print(f'toppoling site {x}')
            h[x] -= 2
            s += 1
            P = [0,1]
            for j in range(2):
                p = np.random.rand()
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
                print(f'toppled {h}')
        active_sites = [i for i,v in enumerate(h) if 1 < v]
    rho = np.mean(h)
    return h,outflow,t,s,a,rho
h = [1,1,1,1]
print(main_loop(h))
exit()
test_numer = 10
for _ in range(1,test_numer):
    file_name = f'parallel/{_}.test'
    with open(file_name) as f:
        input_h = list(map(int,f.readline().replace('\n','').split(' ')))
        answer = list(map(int,f.readline().replace('\n','').split(' ')))
        t = int(f.readline())
        s = int(f.readline())
        a = int(f.readline())


        h,o,T,S,A,rho = main_loop(input_h)
        if (h,T,S,len(A)) != (answer,t,s,a):
            print('error')
            print('expected',answer,t,s,a)
            print('logic',h,T,S,A)
            exit()