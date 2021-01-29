#!/usr/bin/python3.9

def parent(i):
    return (i-1)//2

def children(i):
    return (2*i+1, 2*i+2)

def fix(x, i):
    def swap(k):
        tmp = x[k]
        x[k] = x[i]
        x[i] = tmp
        fix(x, k)
    l, r = children(i)
    lGreater = l<len(x) and x[l] > x[i]
    rGreater = r<len(x) and x[r] > x[i]

    if lGreater and not rGreater:
        swap(l)
        return True
    elif rGreater and not lGreater:
        swap(r)
        return True
    elif lGreater and rGreater:
        if x[l] > x[r]:
            swap(l)
        else:
            swap(r)
        return True
    return False


def heapify(x):
    for i in range(len(x)-1, -1, -1):
        fix(x, i)

def push(x, e):
    x.append(e)
    i = parent(len(x)-1)
    while i >= 0 and fix(x, i):
        i = parent(i)

def popmax(x):
    h = x[0]
    t = x.pop()
    if len(x) > 0:
        x[0] = t
        fix(x, 0)
    return h


x = [3,4,2,5,7,6,10,8,4]
heapify(x)
print(x)

push(x, 11)
print(x)

print(popmax(x))
print(x)