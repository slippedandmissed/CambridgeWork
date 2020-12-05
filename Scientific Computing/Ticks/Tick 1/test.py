#!/usr/bin/python3.9

import numpy as np

N = 10
x = np.zeros(N)

x[0] = 1

arrangement = np.arange(N)
np.random.shuffle(arrangement)
shuffled = x[arrangement]

shuffled[0] = 2

reverse = np.argsort(arrangement)

y = shuffled[reverse]

print(x)
print(arrangement)
print(shuffled)
print(reverse)
print(y)