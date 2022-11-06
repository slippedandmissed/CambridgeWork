#!/usr/bin/python3.9

import numpy as np
import matplotlib.pyplot as plt


def draw(points, centroids, filename="fig.png"):
  fig, ax = plt.subplots(figsize=(5, 5))
  ax.scatter(*centroids.T, s=40, color="red", label="Centroids")
  ax.scatter(*points.T, s=20, color="blue", label="Points")
  ax.legend()

  fig.savefig(filename)

def relax(points, centroids):
  clusters = []
  for i in range(centroids.shape[0]):
    clusters.append([])
  for p in points:
    dsts = np.sqrt(np.sum((centroids-p)*(centroids-p), axis=-1))
    clusters[np.argmin(dsts)].append(p)
  

  for i, c in enumerate(clusters):
    centroids[i] = np.mean(np.array(c), axis=0)

points = np.array([[0, 2], [2, 4], [4, 0], [4, 2]], dtype=float)
centroids = np.array([points[1], points[2]], dtype=float)

for i in range(5):
  draw(points, centroids, f"step{i}.png")
  relax(points, centroids)