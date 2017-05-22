# -*- coding: utf-8 -*-
from pylab import plt, np
from pylab import random, randint, choice
from pylab import sin, cos, pi
from pylab import argmax

# ограничение расстояния
pos_left  = -1.2
pos_right =  0.5

# ограничение скорости
vel_left  = -0.07
vel_right =  0.07

# сетки
number_grids   = 10
tile_side_size = 9
num_tiles      = number_grids * tile_side_size * tile_side_size

# шаг сетки
tile_width  = (pos_right - pos_left) / (tile_side_size - 1)
tile_height = (vel_right - vel_left) / (tile_side_size - 1)

shift_pos = tile_width / number_grids
shift_vel = tile_height / number_grids

episodes   = 30
alpha      = 0.05
lmbda      = 0.9
num_action = 3
n          = num_tiles * num_action

# для отрисовки
t = np.arange(pos_left, pos_right, 0.01)
frame = 0
plt.show(block=False)

def get_F(x, y):
    x -= pos_left
    y -= vel_left

    F = [-1] * number_grids
    for i in range(number_grids):
        x_res = int((tile_side_size - 1) * (x + i * shift_pos) / (pos_right - pos_left))
        y_res = int((tile_side_size - 1) * (y + i * shift_vel) / (vel_right - vel_left))
        F[i]  = i * tile_side_size**2 + (y_res * tile_side_size + x_res)

    return F

def init():
    pos = -0.5 + 0.2 * random() * choice([-1, 1])
    vel =  0.0
    return pos, vel

def render_plot(pos, vel, a, episode, step):
    global frame
    if not frame % 10:
        plt.clf()
        plt.title('Episode: {} | Step: {}\na = {} \npos = {:.5f} | vel = {:.5f}'
                  .format(episode, step, ['L ←', 'R →', 'N -'][a+1], pos, vel))
        plt.plot(t, sin(pi*t))
        plt.axvline(x=pos_left)
        plt.axvline(x=pos_right)
        plt.scatter(pos, sin(pi*pos))
        plt.draw()
        plt.pause(0.0001)
        frame = 0
    frame += 1

# обновление позиции и скорости
def update(S, a, episode, step):
    pos, vel = S
    r = -1
    a -= 1

    vel += 0.001 * a - 0.0025 * cos(3 * pos)
    vel = max(min(vel, vel_right), vel_left)
    pos += vel

    if pos >= pos_right:
        return r, None

    if pos < pos_left:
        pos = -1.2
        vel =  0.0

    render_plot(pos, vel, a, episode, step)
    return r, (pos, vel)

# eps-жадный выбор
def eps_greedy(Qs, epsilon=0):
    return randint(num_action) if random() < epsilon else argmax(Qs)

# обновление функции ценности действия
def Qs(F):
    Q = np.zeros(num_action)
    for a in range(num_action):
        for f in F:
            Q[a] += theta[f + (a * num_tiles)]
    return Q

# Sarsa(lambda)
theta = random(n)                            # theta - случайные значения
for episode in range(episodes):
    step = 0
    S = init()                               # начальное состояние. S[0] - позиция, S[1] - скорость
    e = np.zeros(n)                          # след
    
    while S is not None:                     # пока S не терминальное состояние
        action = 0
        F = get_F(S[0], S[1])

        Q         = Qs(F)
        action    = eps_greedy(Q)                        # выбор действия
        R, S_next = update(S, action, episode, step)     # подкрепление и текущее состояние
        delta     = R - Q[action]
        
        for f in F:
            e[f + (action * num_tiles)] = 1              # отметить состояния, в которые попадали
        
        if S_next == None:                               # Если S_next терминальное, завершаем эпизод
            theta += alpha * delta * e
            break
        
        F = get_F(S_next[0], S_next[1])
        delta += max(Qs(F))
        theta += alpha * delta * e
        e     *= lmbda
        S      = S_next
        step  += 1
