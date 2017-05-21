# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
from pylab import *

numTiles = 10 * 9 * 9
numTilings = 10

tilingSize = 8 # (subset)
positionTileMovementValue = -0.2125/numTilings
velocityTileMovementValue = -0.0175/numTilings

numEpisodes = 30
alpha = 0.05
lmbda = 0.9
n = numTiles * 3
F = [-1]*numTilings

t = np.arange(-1.2, 0.5, 0.01)
k = 0

plt.show(block=False)

def tilecode(x, y, tileIndices):
    x += 1.2
    y += 0.07

    for i in range (numTilings):
        positionMovementConstant = i * positionTileMovementValue
        velocityMovementConstant = i * velocityTileMovementValue
        
        xcoord = int(tilingSize * (x - positionMovementConstant)/1.7)
        ycoord = int(tilingSize * (y - velocityMovementConstant)/0.14)

        tileIndices[i] = i * 81 + (ycoord * 9 + xcoord)

def init():
    position = -0.5 + random() * 0.2
    return position, 0.0

def render_plot(position):
    global k
    if not k % 10:
        plt.clf()
        plt.plot(t, sin(pi*t))
        plt.axvline(x=-1.2)
        plt.axvline(x=0.5)
        plt.scatter(position, sin(pi*position))
        plt.draw()
        plt.pause(0.0001)
        k = 0
    k += 1

def update(S, A):
    position, velocity = S
        
    R = -1
    A -= 1

    velocity += 0.001 * A - 0.0025 * cos(3 * position)
    velocity = max(min(velocity, 0.07), -0.07)

    position += velocity

    if position >= 0.5:
        return R, None

    if position < -1.2:
        position = -1.2
        velocity = 0.0

    render_plot(position)
    return R, (position, velocity)

def eps_greedy(Qs, epsilon=0):
    return randint(3) if random() < epsilon else argmax(Qs)
    
def Qs(F):
    Q = np.zeros(3)
    for a in range(3):
        for i in F:
            Q[a] += theta[i + (a * numTiles)]     # update Qa
    return Q

theta = -0.01 * random(n)
for episode in range(numEpisodes):
    step = 0
    S = init()                               # initialize state
    e = np.zeros(n)                          # initialize e (eligibility trace vector)
    
    while S is not None:
        print("Episode: {}, Step: {}".format(episode, step))

        A = 0
        tilecode(S[0], S[1], F)              # get a list of four tile indices

        Q = Qs(F)
        A = eps_greedy(Q)                    # pick the action
        R, S_next = update(S, A)             # observe reward, and next state
        delta = R - Q[A]
        
        for i in F:
            e[i + (A * numTiles)] = 1          # replacing traces
        
        # if S is terminal, then update theta; go to next episode
        if S_next == None:
            theta += alpha * delta * e
            break
        
        tilecode(S_next[0], S_next[1], F)
        delta += max(Qs(F))
        theta += alpha * delta * e           # update theta
        e *= lmbda                           # update e
        S = S_next                           # update current state to next state for next iteration
        step += 1
