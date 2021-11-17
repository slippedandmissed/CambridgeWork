import numpy as np
import matplotlib.pyplot as plt

def rx():
    u = np.random.uniform(0, 1, size=(10000))
    return u * (1-u)

x = rx()
v, b = np.histogram(x)
cumulative = np.cumsum(v)

plt.plot(b[:-1], cumulative)
plt.show()
