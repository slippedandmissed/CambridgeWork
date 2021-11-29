#!/usr/bin/python3.9

import numpy as np
import scipy.stats
import pandas
import matplotlib.pyplot as plt
import matplotlib.patches
import imageio
import sys
from IPython.display import clear_output

map_image = imageio.imread('voronoi-map-goal-16000-shaded.png')
if len(sys.argv) > 1 and sys.argv[1] == "recalculate":

    localization = pandas.read_csv('localization.csv')
    localization.sort_values(['id','t'], inplace=True)

    # Pull out observations for the animal we want to track
    observations = localization.loc[localization.id==0, ['r','g','b']].values

    df = localization

    fig,(ax,ax2) = plt.subplots(2,1, figsize=(4,5), gridspec_kw={'height_ratios':[4,.5]})
    ax.imshow(map_image.transpose(1,0,2), alpha=.5)
    w,h = map_image.shape[:2]
    ax.set_xlim([0,w])
    ax.set_ylim([0,h])

    for i in range(1,5):
        ax.plot(df.loc[df.id==i,'x'].values, df.loc[df.id==i,'y'].values, lw=1, label=i)
    ax.axis('off')
    ax.legend()
    ax.set_title('Animals 1--4, GPS tracks')

    ax2.bar(np.arange(len(observations)), np.ones(len(observations)), color=observations, width=2)
    ax2.set_xlim([0,len(observations)])
    ax2.set_yticks([])
    ax2.set_title('Animal id=0, camera only')

    plt.tight_layout()
    # plt.show()

    W,H = map_image.shape[:2]
    M = num_particles = 2000

    # Empirical representation of the distribution of X0
    δ0 = np.column_stack([np.random.uniform(0,W-1,size=M), np.random.uniform(0,H-1,size=M), np.ones(M)/M])

    def show_particles(particles, ax=None, s=1, c='red', alpha=.5):
        # Plot an array of particles, with size proportional to weight.
        # (Scale up the sizes by setting s larger.)
        if ax is None:
            fig,ax = plt.subplots(figsize=(2.5,2.5))
        ax.imshow(map_image.transpose(1,0,2), alpha=alpha, origin='lower')
        w,h = map_image.shape[:2]
        ax.set_xlim([0,w])
        ax.set_ylim([0,h])
        w = particles[:,2]
        ax.scatter(particles[:,0],particles[:,1], s=w/np.sum(w)*s, color=c)
        ax.axis('off')

    fig,ax = plt.subplots(figsize=(4,4))
    show_particles(δ0, s=400, ax=ax)
    ax.set_title('$X_0$')
    # plt.show()

    y0 = observations[0]
    print(f"First observation: rgb = {y0}")

    def patch(im, xy, size=3):
        s = (size-1) / 2
        nx,ny = np.meshgrid(np.arange(-s,s+1), np.arange(-s,s+1))
        nx,ny = np.stack([nx,ny], axis=0).reshape((2,-1))
        neighbourhood = np.row_stack([nx,ny])
        w,h = im.shape[:2]
        neighbours = neighbourhood + np.array(xy).reshape(-1,1)
        neighbours = nx,ny = np.round(neighbours).astype(int)
        nx,ny = neighbours[:, (nx>=0) & (nx<w) & (ny>=0) & (ny<h)]
        patch = im[nx,ny,:3]
        return np.mean(patch, axis=0)/255

    loc = δ0[0,:2]
    print(f"First particle is at {loc}")

    col = patch(map_image, loc, size=3)
    print(f"Map terrain around this particle: rgb = {col}")

    def pr(y, loc):
        return np.product(scipy.stats.norm.pdf(y, patch(map_image, loc), 0.05))

    # Sanity check
    y0 = observations[0]
    loc = δ0[0,:2]
    w = pr(y0, loc)
    import numbers
    assert isinstance(w, numbers.Number) and w>=0

    y0 = observations[0]
    w = np.array([pr(y0, (x,y)) for x,y,_ in δ0])
    π0 = np.copy(δ0)
    π0[:,2] = w / sum(w)

    fig,(axδ,axπ) = plt.subplots(1,2, figsize=(8,4), sharex=True, sharey=True)
    show_particles(δ0, ax=axδ, s=600)
    show_particles(π0, ax=axπ, s=600)
    axπ.add_patch(matplotlib.patches.Rectangle((0,0),100,100,color=y0))
    axπ.text(50,50,'$y_0$', c='white', ha='center', va='center', fontsize=14)
    axδ.set_title('$X_0$')
    axπ.set_title('$(X_0|y_0)$')
    # plt.show()

    def walk(loc):
        angle = np.random.uniform(0, 2*np.pi)
        r = np.random.exponential(5)
        dx = np.cos(angle) * r
        dy = np.sin(angle) * r
        return np.clip(np.add(loc, [dx, dy]), [0, 0], [W-1, H-1])

    loc = π0[0,:2]
    loc2 = walk(loc)
    assert len(loc2)==2 and isinstance(loc2[0], numbers.Number) and isinstance(loc2[1], numbers.Number)
    assert loc2[0]>=0 and loc2[0]<=W-1 and loc2[1]>=0 and loc2[1]<=H-1

    δ1 = np.copy(π0)
    for i in range(len(δ1)):
        δ1[i,:2] = walk(δ1[i,:2])

    fig,ax = plt.subplots(figsize=(4,4))
    show_particles(π0, ax=ax, s=4000, c='blue', alpha=.25)
    show_particles(δ1, ax=ax, s=4000, c='red', alpha=.25)
    ax.set_xlim([200,400])
    ax.set_ylim([100,300])
    # plt.show()

    particles = np.copy(π0)

    # plt.ion()

    # weights = []

    # fig,ax = plt.subplots(figsize=(3.5,3.5))
    # for n,obs in enumerate(observations[:101]):
    #     # Compute δ, the locations after a movement step
    #     for i in range(num_particles):
    #         particles[i,:2] = walk(particles[i,:2])
    #     # Compute π, the posterior after observing y
    #     w = np.array([pr(obs, (px,py)) for px,py,_ in particles])
    #     weights.append(w)
    #     particles[:,2] = w / sum(w)

    #     # Plot the current particles
    #     ax.clear()
    #     show_particles(particles, ax, s=20)
    #     ax.set_title(f"Timestep {n+1}")
    #     fig.canvas.draw()
    #     fig.canvas.flush_events()

    # fig,axes = plt.subplots(5,1, figsize=(8,6), sharey=True)
    # for n,ax in zip([0,1,5,50,100],axes):
    #     w = weights[n] / sum(weights[n])
    #     ax.hist(w, bins=60)
    #     ax.axvline(x=1/len(particles), color='black', linewidth=4, linestyle='dashed')
    # plt.show()

    def prune_spawn(particles):
        w = np.array([pr(obs, (px,py)) for px,py,_ in particles])
        w = w/sum(w)
        indices = np.argsort(w)
        q1 = indices[:len(indices)//5]
        q3 = indices[len(indices)//5 * 4:]
        spawned_weights = w[q3] * 0.5
        w[q3] = spawned_weights
        w[q1] = spawned_weights
        particles[q1] = particles[q3]
        particles[:,2] = w

    particles = np.copy(π0)

    plt.ion()

    fig,ax = plt.subplots(figsize=(3.5,3.5))
    for n,obs in enumerate(observations[:100]):
        print(n)
        # Compute δ, the locations after a movement step
        for i in range(num_particles):
            particles[i,:2] = walk(particles[i,:2])
        # Compute π, the posterior after observing y
        w = np.array([pr(obs, (px,py)) for px,py,_ in particles])
        particles[:,2] = w / sum(w)
        # Prune/spawn
        prune_spawn(particles)

        # Plot the current particles
        ax.clear()
        show_particles(particles, ax, s=20)
        ax.set_title(f"Timestep {n+1}")
        fig.canvas.draw()
        fig.canvas.flush_events()
    np.savetxt("particles.csv", particles, delimiter=",")

particles = np.loadtxt("particles.csv", delimiter=",")

w, h = map_image.shape[:2]

plt.ion()

fig,ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
plt.axis('off')
ax.set_xlim([0,w])
ax.set_ylim([0,h])

p = np.zeros((w, h))
for i, (x, y, weight) in enumerate(particles):
    grid = np.indices((w, h))
    dx = grid[0] - x
    dy = grid[1] - y
    r = np.sqrt(dx * dx + dy * dy)
    stddev = weight * 200
    p += scipy.stats.norm.pdf(r, 0, stddev) * weight
    ax.clear()
    plt.axis('off')
    ax.set_xlim([0,w])
    ax.set_ylim([0,h])

    ax.set_title(f"Particle {i+1}/{len(particles)}")
    ax.imshow((p/np.max(p)*255).transpose(1,0), origin='lower', cmap='gray', vmin=0, interpolation='none')
    fig.canvas.draw()
    fig.canvas.flush_events()

p /= np.max(p) * 255

fig,ax = plt.subplots(figsize=(w/100, h/100), dpi=100, frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(p.transpose(1,0), origin='lower', cmap='gray', vmin=0, interpolation='none', aspect='auto')
ax.set_xlim([0,w])
ax.set_ylim([0,h])
plt.axis('off')

plt.savefig("myprediction.png", dpi=100)