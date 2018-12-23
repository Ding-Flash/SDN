from fetch import *
from topo import network

N = 2
M = 4
T = 25000000
alpha = 0.8
belta = 0.2
Con = [[] for i in range(N)]
Sw = [0]*(M+1)

for i in range(N):
    Con[i].append(i*2+1)
    Con[i].append(i*2+2)
for i in range(M):
    Sw[i+1] = (int)((i)/2)

def getmaxf(by):
    maxf = 0
    for i in range(len(by)-1):
        tmp = by[i+1]-by[i]
        if tmp>maxf:
            maxf = tmp
    return maxf

def getload(con):
    res = getall(con)
    print(res.keys())
    sum0 = 0
    for i in Con[con]:
        for j in range(2):
            st = str(i)+':'+str(j+1)
            tmp = res[st]
            rby = tmp['rx_bytes']
            tby = tmp['tx_bytes']
            sum0 = sum0 + getmaxf(rby) + getmaxf(tby)
    return sum0

def getswflow(sw):
    res = getall(Sw[sw])
    sum0 = 0
    for j in range(2):
        st = str(sw)+':'+str(j+1)
        tmp = res[st]
        rby = tmp['rx_bytes']
        tby = tmp['tx_bytes']
        sum0 = sum0+getmaxf(rby)+getmaxf(tby)
    return sum0

'''
def getswflow(sw):
    con = Sw[sw]
    res = getmiss(con)
    idx = Con[con].index(sw)
    tmp = res[str(idx)]
    by = tmp['bytes']
    return by[-1]-by[-5]

def getload(con):
    res = getmiss(con)
    sum = 0
    for i in Con[con]:
        tmp = res[str(i)]
        by = tmp['bytes']
        sum = sum+by[-1]-by[-5]
    return sum
'''

def update(sw, cn, net):
    sname = 's'+str(sw)
    cname = 'c'+str(cn)
    s = net.get(sname)
    c = net.get(cname)
    print(sname, cname)
    s.start([c])    

def shrink(net):
    S = []
    C = [0]*N
    B = [1]*N
    for i in range(N):
        C[i] = getload(i)
        if C[i]<belta*T:
            B[i] = 0
            for j in Con[i]:
                S.append(j)
    for j in S:
        sf = getswflow(j)
        max_F = 0
        mt = -1
        for i in range(N):
            if B[i]>0:
                if (sf+C[i]>max_F) and (sf+C[i]<=alpha*T):
                    max_F = sf+C[i]
                    mt = i
        Con[mt].append(j)
        idx = Con[Sw[j]].index(j)
        del Con[Sw[j]][idx]
        Sw[j] = mt
        C[mt] += sf
        update(j,mt,net)

def isbalenced(C):
    for i in C:
        if i>alpha*T:
            return 0
    return 1

def balance(net):
    S = []
    C = [0]*N
    D = [[1,1] for i in range(N)]
    for i in range(N):
        C[i] = getload(i)
        print(C[i])
        if C[i]>alpha*T:
            for j in Con[i]:
                S.append(j)
    for i in range(N):
        for j in range(N):
            if i!=j:
                D[i][j] = abs(C[i]-C[j])
    for j in S:
        if isbalenced(C):
            break
        con = Sw[j]
        sf = getswflow(j)
        print(j)
        print('$')
        print(sf)
        min_F = 0x3f3f3f3f
        mt = -1
        for i in range(N):
            if i!=con:
                if D[i][con]<min_F and C[i]+sf<=alpha*T:
                    min_F = D[i][con]
                    mt = i
        Con[mt].append(j)
        idx = Con[Sw[j]].index(j)
        del Con[Sw[j]][idx]
        Sw[j] = mt
        C[mt] += sf
        C[con] -= sf
        update(j,mt,net)
        ix = S.index(j)
        del S[ix]


def printtopo():
    for i in range(N):
        print('controller %d connects %d switches:'%(i,len(Con[i])))
        for j in Con[i]:
            print('s'+str(j))

        
