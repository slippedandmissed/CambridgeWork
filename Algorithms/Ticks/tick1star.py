#!/usr/bin/python3.9

count = 0

def cmp_simple(x,y):
    global count
    count += 1
    return -1 if x<y else (1 if x>y else 0)

def parent(i):
    return (i-1)//2

def children(i):
    return (2*i+1, 2*i+2)

def fix(x, i, cmp):
    def swap(k):
        tmp = x[k]
        x[k] = x[i]
        x[i] = tmp
        fix(x, k, cmp)
    l, r = children(i)

    if l<len(x) and cmp(x[l], x[i]) > 0:
        if r<len(x) and cmp(x[l],x[r]) < 0:
            swap(r)
        else:
            swap(l)
        return True
    elif r<len(x) and cmp(x[r], x[i]) > 0:
        swap(r)
        return True
    return False


def heapify(x, cmp):
    for i in range(len(x)-1, -1, -1):
        fix(x, i, cmp)

def push(x, e, cmp):
    x.append(e)
    i = parent(len(x)-1)
    while i >= 0 and fix(x, i, cmp):
        i = parent(i)

def popmax(x, cmp):
    h = x[0]
    t = x.pop()
    if len(x) > 0:
        x[0] = t
        fix(x, 0, cmp)
    return h

def popmax_bu(x, cmp):
    h = x[0]
    tmp = x.pop()
    if len(x) == 1:
        x[0] = tmp
    elif len(x) > 0:
        L = 0
        atLeaf = False
        while not atLeaf:
            l, r = children(L)
            if l >= len(x):
                atLeaf = True
            elif r >= len(x):
                L = l
                atLeaf = True
            else:
                L = r if cmp(x[l], x[r]) < 0 else l
        p = L
        while cmp(x[p], tmp) < 0:
            p = parent(p)

        i = p
        while i >= 0:
            t = x[i]
            x[i] = tmp
            tmp = t
            i = parent(i)
    return h

x = ['a', 'z', 'b', 'y', 'c', 'x', 'd', 'w', 'e', 'v', 'f', 'u', 'g', 't', 'h', 's', 'i', 'r', 'j', 'q', 'k', 'p', 'l', 'o', 'm', 'n']
heapify(x, cmp_simple)
print(str(x)+"   "+str(count))
count = 0

for i in range(len(x)):
    print(popmax_bu(x, cmp_simple)+" "+str(count))
    count = 0
