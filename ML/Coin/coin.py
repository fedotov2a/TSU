# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

limit = 100     # деньги игрока
p = 0.55        # вероятность выпадения орла (вероятность выигрыша)
eps = 1e-07

optimal_function = [0 for i in range(limit+1)]      # оптимальная функция ценности действия
optimal_strategy = [0 for i in range(limit-1)]      # оптимальный размер ставки, в зависимости от i-го капитала

win = False
while not win:
    for m in range(limit-1, 0, -1):
        max_bet = m
        max_bet = min(m, limit-m)

        Vmax = 0
        for bet in range(1, max_bet+1):
            r = 0
            Vs = (1 - p) * (r + optimal_function[m - bet])

            r = 1 if (m + bet) == limit else 0
            Vs += p * (r + optimal_function[m + bet])

            if Vs >= Vmax:
                Vmax = Vs
                optimal_strategy[m-1] = bet

        if m == limit-1 and abs(Vmax - optimal_function[m]) < eps:
            optimal_function[m] = Vmax
            win = True

        optimal_function[m] = Vmax

for i in range(limit-1):
    print("money: {} | p_win: {:.4f} | opt_str: {}".format(i+1, optimal_function[i+1], optimal_strategy[i]))

plt.figure(1)
plt.subplot(211)
plt.title('For p = {} and eps = {}\nOptimal function'.format(p, eps))
plt.plot(optimal_function[:-1], 'red')

plt.subplot(212)
plt.title('Optimal strategy')
plt.plot(optimal_strategy, 'blue')
plt.show()  
