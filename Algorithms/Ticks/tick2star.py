#!/usr/bin/python3.9

def table(a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    prev = []
    for i in range(len(a)+1):
        row = []
        prev.append(row)
        for j in range(len(b)+1):
            if i == 0 or j == 0:
                row.append(0)
            elif a[i-1] == b[j-1]:
                row.append(prev[i-1][j-1]+1)
            else:
                row.append(max(prev[i-1][j], prev[i][j-1]))
    return list(i[1:] for i in prev[1:]) 

def copy_into(src, dst):
    for y, row in enumerate(src):
        for x, cell in enumerate(row):
            if dst[y][x] is None:
                dst[y][x] = cell


def memoize(func):
    cache = {}
    def helper(a, b):
        if not a in cache:
            cache[a] = {}
        if not b in cache[a]:
            cache[a][b] = func(a, b)
        return cache[a][b]
    return helper

@memoize
def table_topdown_recursive(a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    tbl = [[None for j in range(len(b))] for i in range(len(a))]
    val = lambda x: x[-1][-1] if len(x) > 0 and len(x[-1]) > 0 else 0
    if a[-1] == b[-1]:
        l = table_topdown_recursive(a[:-1], b[:-1])
        copy_into(l, tbl)
        tbl[-1][-1] = val(l)+1
    else:
        l1 = table_topdown_recursive(a[:-1], b)
        l2 = table_topdown_recursive(a, b[:-1])
        copy_into(l1, tbl)
        copy_into(l2, tbl)
        tbl[-1][-1] = max(val(l1), val(l2))
    return tbl

def table_topdown_nonrecursive(a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    tbl = [[None for j in range(len(b)+1)] for i in range(len(a)+1)]
    stack = [(len(a), len(b))]
    while len(stack) > 0:
        i, j = stack.pop()
        while tbl[i][j] is None:
            if i == 0 or j == 0:
                tbl[i][j] = 0
            elif a[i-1] == b[j-1]:
                if tbl[i-1][j-1] is not None:
                    tbl[i][j] = 1 + tbl[i-1][j-1]
                else:
                    stack.append((i, j))
                    i -= 1
                    j -= 1
            else:
                l1 = tbl[i-1][j]
                l2 = tbl[i][j-1]
                if l1 is None:
                    stack.append((i,j))
                    i -= 1
                elif l2 is None:
                    stack.append((i, j))
                    j -= 1
                else:
                    tbl[i][j] = max(l1, l2)
    return list(i[1:] for i in tbl[1:]) 



def match_length(tbl):
    if len(tbl) == 0 or len(tbl[-1]) == 0:
        return 0
    return tbl[-1][-1]

def match_string(a, b, tbl):
    if len(tbl) == 0 or len(tbl[-1]) == 0:
        return ""
    tbl = [[0]*(len(b)+1)]+list([0]+i for i in tbl)
    tbl = [[(0 if cell is None else cell) for cell in row] for row in tbl]
    substring = ""
    for i in tbl:
        print(i)
    i = len(a)
    j = len(b)
    while tbl[i][j] > 0:
        if a[i-1]==b[j-1]:
            substring = a[i-1] + substring
            i -= 1
            j -= 1
        elif tbl[i][j-1] > tbl[i-1][j]:
            if tbl[i][j-1] < tbl[i][j]:
                substring = b[j-1] + substring
            j-=1
        else:
            if tbl[i-1][j] < tbl[i][j]:
                substring = a[i-1] + substring
            i-=1
    return substring


s1 = "XMJYAUZ"
s2 = "MZJAWXU"
tbl = table_topdown_recursive(s1, s2)
list(print(i) for i in tbl)
print(match_length(tbl))
print(match_string(s1,s2,tbl))