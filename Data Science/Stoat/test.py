import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

w = h = 600

particles = np.array([
    [50, 100, 1],
    [200, 200, 0.5]
])

p = np.zeros((w, h))
for x, y, weight in particles:
    grid = np.indices((w, h))
    dx = grid[0] - x
    dy = grid[1] - y
    r = np.sqrt(dx * dx + dy * dy)
    stddev = weight * 10
    p += scipy.stats.norm.pdf(r, 0, stddev) * weight

p /= np.max(p) * 255


fig,ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
ax.imshow(p.transpose(1,0), origin='lower', cmap='gray', vmin=0, interpolation='none')
ax.set_xlim([0,w])
ax.set_ylim([0,h])
plt.axis('off')
plt.show()
