# -*- coding: utf-8 -*-
from numpy.random import choice
from numpy.random import normal
from numpy import e as exp

import matplotlib.pyplot as plt

def Qgreedy(sum_r, num_a, n):
    max_action = 0
    max_arg = sum_r[0] / num_a[0] if num_a[0] != 0 else 0
        
    for i in range(n):
        if num_a[i] != 0:
            if max_arg < (sum_r[i] / num_a[i]):
                max_arg = sum_r[i] / num_a[i]
                max_action = i

    return max_action

def Qsoft(sum_r, num_a, n, t):
    sum_soft = 0
    for i in range(n):
        if num_a[i] != 0:
            sum_soft += exp ** ((sum_r[i] / num_a[i]) / t)
    
    p = [0 for i in range(n)]
    for i in range(n):
        if num_a[i] != 0:
            p[i] = exp ** ((sum_r[i] / num_a[i]) / t)
            p[i] /= sum_soft

    return choice(n, p=p)

N = 10
plays = 1000
tasks = 2000

R = [[0] * N for y in range(tasks)]
max_action = [0 for y in range(tasks)]

for task in range(tasks):
    mQa = normal(0, 1)
    max_action[task] = -1
    maxR = -10
    
    for i in range(N):
        R[task][i] = normal(mQa, 1)
        if maxR <= R[task][i]:
            maxR = R[task][i]
            max_action[task] = i

greedy_sum_r          = [[0] * N for y in range(tasks)]
greedy_number_action  = [[0] * N for y in range(tasks)]
greedy_change_r       = [0 for i in range(plays)]
greedy_optimal_choice = [0 for i in range(plays)]
eps = 0.01

soft_sum_r          = [[0] * N for y in range(tasks)]
soft_number_action  = [[0] * N for y in range(tasks)]
soft_change_r       = [0 for i in range(plays)]
soft_optimal_choice = [0 for i in range(plays)]
t = 0.4

for i in range(plays):
    greedy_count_max_action = 0
    soft_count_max_action = 0

    for task in range(tasks):
        greedy = choice(2, p=[eps, 1-eps])
        action = Qgreedy(greedy_sum_r[task], greedy_number_action[task], N) if greedy == 1 else choice(N)
        r = R[task][action]

        greedy_sum_r[task][action] += r
        greedy_number_action[task][action] += 1

        greedy_change_r[i] += r
        greedy_count_max_action += 1 if action == max_action[task] else 0

        action = i if i < N else Qsoft(soft_sum_r[task], soft_number_action[task], N, t) 
        r = R[task][action]
        
        soft_sum_r[task][action] += r
        soft_number_action[task][action] += 1
        
        soft_change_r[i] += r
        soft_count_max_action += 1 if action == max_action[task] else 0

    greedy_change_r[i] /= tasks
    greedy_optimal_choice[i] = greedy_count_max_action / tasks
    soft_change_r[i] /= tasks
    soft_optimal_choice[i] = soft_count_max_action / tasks

plt.figure(1)
plt.subplot(211)
plt.title('Жадный алгоритм')
plt.xlabel('Раунды')
plt.ylabel('Среднее вознаграждение')
plt.plot(greedy_change_r)

plt.subplot(212)
plt.xlabel('Раунды')
plt.ylabel('Оптимальный выбор')
plt.plot(greedy_optimal_choice)

plt.show()

plt.figure(2)
plt.subplot(211)
plt.title('Мягкий максимум. Распределение Гиббса')
plt.xlabel('Раунды')
plt.ylabel('Среднее вознаграждение')
plt.plot(soft_change_r)

plt.subplot(212)
plt.xlabel('Раунды')
plt.ylabel('Оптимальный выбор')
plt.plot(soft_optimal_choice)

plt.show()