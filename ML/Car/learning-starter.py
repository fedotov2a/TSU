# -*- coding: utf-8 -*-
import mountaincar
from Tilecoder import numTilings, tilecode, numTiles
from Tilecoder import numTiles as n
from pylab import *

numRuns = 1
numEpisodes = 30
alpha = 0.05/numTilings
gamma = 1
lmbda = 0.9
Epi = Emu = epsilon = 0
n = numTiles * 3 # 4 * 9 * 9 * 3
F = [-1]*numTilings # 4

def egreedy(Qs, epsilon):
    return randint(3) if random() < epsilon else argmax(Qs)
    
def expQunderPi(Qs):
    return Epi*average(Qs) + (1-Epi)*max(Qs)

def Qs(F):
    Q = np.zeros(3)
    # for every possible action a in F
    for a in range(3):
        # numTilings
        for i in F:
            Q[a] = Q[a] + theta[i + (a * numTiles)]     # update Qa
    return Q

for run in range(numRuns):
    theta = -0.01 * random(n)
    
    for episodeNum in range(numEpisodes):
        G = 0
        step = 0
        S = mountaincar.init()                   # initialize state
        e = np.zeros(n)                          # initialize e (eligibility trace vector)
        
        while S is not None:
            print("Episode: {}, Step: {}".format(episodeNum, step))

            A = 0
            tilecode(S[0], S[1], F)              # get a list of four tile indices

            Q = Qs(F)
            A = egreedy(Q, Emu)                  # pick the action
            R, Sprime = mountaincar.sample(S, A) # observe reward, and next state
            delta = R - Q[A]
            G += R
            
            for i in F:
                e[i + (A*numTiles)] = 1          # replacing traces
            
            # if S is terminal, then update theta; go to next episode
            if Sprime == None:
                theta += alpha * delta * e
                break
            
            tilecode(Sprime[0], Sprime[1], F)
            Qprime = Qs(F)
            delta += expQunderPi(Qprime)
            theta += alpha * delta * e           # update theta
            e *= gamma * lmbda                   # update e
            S = Sprime                           # update current state to next state for next iteration
            step += 1