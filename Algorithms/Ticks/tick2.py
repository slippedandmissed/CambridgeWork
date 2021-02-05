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

def match_length(tbl):
    if len(tbl) == 0 or len(tbl[-1]) == 0:
        return 0
    return tbl[-1][-1]

def match_string(a, b, tbl):
    if len(tbl) == 0 or len(tbl[-1]) == 0:
        return ""
    tbl = [[0]*(len(b)+1)]+list([0]+i for i in tbl)
    substring = ""
    i = len(a)
    j = len(b)
    while tbl[i][j] > 0:
        if a[i-1]==b[j-1]:
            substring = a[i-1]+substring
            i-=1
            j-=1
        elif tbl[i][j-1] > tbl[i-1][j]:
            j-=1
        else:
            i-=1
    return substring


s1 = "ABBA"
s2 = "CACA"
tbl = table(s1, s2)
list(print(i) for i in tbl)
print(match_length(tbl))
print(match_string(s1,s2,tbl))