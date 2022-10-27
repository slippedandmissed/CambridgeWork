#!/usr/bin/python3.9

import numpy as np

def needleman_wunsch(v, w, s, d=0.1):
    M = len(v)
    N = len(w)
    F = np.zeros((N+1, M+1))
    Ptr = np.empty((N+1, M+1), dtype=int)
    Ptr[0, 0] = -1
    Ptr[0, 1:] = 1
    Ptr[1:, 0] = 0
    for j in range(N+1):
        F[j, 0] = -j*d
    for i in range(M+1):
        F[0, i] = -i*d

    for i in range(1, M+1):
        for j in range(1, N+1):
            x = np.array([
                F[j-1, i] - d,
                F[j, i-1] - d,
                F[j-1, i-1] + s[v[i-1]][w[j-1]]
            ])
            
            F[j, i] = np.max(x)
            Ptr[j, i] = np.argmax(x)
    
    print(F)
    print(Ptr)
        
    j = N
    i = M
    V = []
    W = []

    while (i > 0 or j > 0):
        p = Ptr[j, i]
        if p == 0:
            j -= 1
            V.append("-")
            W.append(w[j])
        elif p == 1:
            i -= 1
            V.append(v[i])
            W.append("-")
        else:
            i -= 1
            j -= 1
            V.append(v[i])
            W.append(w[j])
    
    return ("".join(V[::-1]), "".join(W[::-1]))


def smith_waterman(v, w, s, d=100):
    M = len(v)
    N = len(w)
    F = np.zeros((N+1, M+1))
    Ptr = np.empty((N+1, M+1), dtype=int)
    Ptr[0, 1:] = 3
    Ptr[1:, 0] = 3

    for i in range(1, M+1):
        for j in range(1, N+1):
            x = np.array([
                F[j-1, i] - d,
                F[j, i-1] - d,
                F[j-1, i-1] + s[v[i-1]][w[j-1]],
                0
            ])
            
            F[j, i] = np.max(x)
            Ptr[j, i] = np.argmax(x)
    
    idx = np.argmax(F)

    j = idx // (M+1)
    i = idx % (M+1)
    V = []
    W = []

    while (i > 0 or j > 0):
        p = Ptr[j, i]
        if p == 0:
            j -= 1
            V.append("-")
            W.append(w[j])
        elif p == 1:
            i -= 1
            V.append(v[i])
            W.append("-")
        elif p == 2:
            i -= 1
            j -= 1
            V.append(v[i])
            W.append(w[j])
        else:
            break
    
    return ("".join(V[::-1]), "".join(W[::-1]))

UP = 0
LEFT = 1
DIAG = 2

def kth_row_of_score(k, v, w, s, d=0.1):
    M = len(v)

    Ptr = np.zeros((2, M+1))
    Ptr[0, :] = LEFT
    Ptr[1, 0] = UP

    F = np.zeros((2, M+1))
    for i in range(M+1):
        F[0, i] = -i * d

    for j in range(1, k+1):
        F[1, 0] = -d * j
        for i in range(1, M+1):
            options = np.array([
                F[0, i] - d,
                F[1, i-1] - d,
                F[0, i-1] + s[v[i-1]][w[j-1]]
            ])

            F[1, i] = np.max(options)
            Ptr[1, i] = np.argmax(options)
    
        F[0, :] = F[1, :]
        Ptr[0, :] = Ptr[1, :]
    
    return F[0, :], Ptr[0, :]

def global_alignment(v, w, s, d=0.1):
    M, N = len(v), len(w)
    V_ = ""
    W_ = ""
    
    i = M
    j = N
    F, Ptr = kth_row_of_score(j, v, w, s, d=d)
    score = F[i]
    while j > 0 or i > 0:
        ptr = Ptr[i]
        if ptr == UP:
            j -= 1
            V_ = "-" + V_
            W_ = w[j] + W_
            F, Ptr = kth_row_of_score(j, v, w, s, d=d)
        elif ptr == LEFT:
            i -= 1
            V_ = v[i] + V_
            W_ = "-" + W_
        else:
            assert ptr == DIAG
            i -= 1
            j -= 1
            assert v[i] == w[j]
            V_ = v[i] + V_
            W_ = w[j] + W_
            F, Ptr = kth_row_of_score(j, v, w, s, d=d)
    
    return (V_, W_, score)



v = "CGTA"
w = "GTCA"

s = {
    "A": {
        "A": 1,
        "C": -np.inf,
        "G": -np.inf,
        "T": -np.inf
    },
    "C": {
        "A": -np.inf,
        "C": 1,
        "G": -np.inf,
        "T": -np.inf
    },
    "G": {
        "A": -np.inf,
        "C": -np.inf,
        "G": 1,
        "T": -np.inf
    },
    "T": {
        "A": -np.inf,
        "C": -np.inf,
        "G": -np.inf,
        "T": 1
    }
}

# print(needleman_wunsch(v, w, s))
# print(smith_waterman(v, w, s))
print(global_alignment(v, w, s))