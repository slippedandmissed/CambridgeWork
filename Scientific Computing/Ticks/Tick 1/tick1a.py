#!/usr/bin/python3.9

import ucamcl
import numpy as np
import random
import matplotlib.pyplot as plt


def random_sizes(N, avg_size): return np.random.geometric(1/avg_size, size=N)

def trunc_sizes(vector):
    N = len(vector)
    sums = np.cumsum(vector)
    truncated = np.copy(vector[:np.where((sums-vector < N) & (N <= sums) == True)[0][0]+1])
    truncated[-1] += (N-np.sum(truncated))
    return truncated

def person_in(vector): return np.repeat(np.arange(len(vector)), vector)

def first_occ(vector): return np.concatenate(([0], np.cumsum(vector)[:-1]))

def exposure(infected, loc_sizes): return np.repeat(np.add.reduceat((infected == 1).astype(int), first_occ(loc_sizes)), loc_sizes)

def sim(N, T, n0, avg_loc_size=2.1, prob_infect=0.07, prob_recover=0.1):
    loc_sizes = trunc_sizes(random_sizes(N, avg_loc_size))
    infected = np.zeros(N, dtype=int)
    infected[:n0] = 1
    
    result = np.zeros((T, 4), dtype=int)
    for t in range(T):
        np.random.shuffle(infected)
        exp = exposure(infected, loc_sizes)
        new_infections = ((infected == 0) & (exp > 0) & (np.random.uniform(0, 1, N) <= prob_infect))
        new_recoveries = ((infected == 1) & (np.random.uniform(0, 1, N) <= prob_recover))
        result[t][0] = np.sum(new_infections)
        result[t][1] = np.sum(new_recoveries)
        infected[new_infections] = 1
        infected[new_recoveries] = -1
        result[t][2] = np.sum(infected == 1)
        result[t][3] = np.sum(infected == -1)
    return result


N = 50000
T = 200
n0 = 200
x = sim(N, T, n0)

fig, axs = plt.subplots(2, sharex=True)

time = np.arange(0, T)
recovered = x[:,3]
infected = x[:,2]
new_infected = x[:,0]
been_infected = infected + recovered
axs[0].plot(time, recovered/N * 100, label="recovered")
axs[0].plot(time, been_infected/N * 100, label="been infected")
axs[0].set_ylabel("% of popn")
axs[0].legend()

axs[1].plot(time, infected, label="infected")
axs[1].plot(time, new_infected, label="new infected")
axs[1].set_ylabel("num. people")
axs[1].legend()

plt.xlabel("day")

plt.show()

GRADER = ucamcl.autograder('https://markmy.solutions', course='scicomp').subsection('tick1a')
q = GRADER.fetch_question('q1')
ans = trunc_sizes(q.s)
GRADER.submit_answer(q, ans)
q = GRADER.fetch_question('q2')
ans = {'person_in': person_in(q.loc_sizes), 'first_occ': first_occ(q.loc_sizes)}
GRADER.submit_answer(q, ans)
q = GRADER.fetch_question('q3')
ans = exposure(np.array(q.infected), q.loc_sizes)
GRADER.submit_answer(q, ans)
q = GRADER.fetch_question('q4')
x = sim(N=q.N, T=q.T, n0=q.n0, avg_loc_size=q.avg_loc_size, prob_infect=q.prob_infect, prob_recover=q.prob_recover)
ans = x[-1,3]/q.N
GRADER.submit_answer(q, ans)
