import matplotlib.pyplot as plt
from pylab import random, cos, sin, pi
from numpy import arange

plt.show(block=False)

t = arange(-1.2, 0.5, 0.01)
k = 0

def init():
    position = -0.5 + random() * 0.2
    return position, 0.0

def sample(S, A):
    position, velocity = S
        
    R = -1
    A = A - 1

    velocity += 0.001*A - 0.0025*cos(3*position)
    
    velocity = max(min(velocity, 0.07), -0.07)
    position += velocity
    # position = max(min(position, 0.5), -1.2)

    if position >= 0.5:
        return R,None
    if position < -1.2:
        position = -1.2
        velocity = 0.0

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

    return R,(position,velocity)