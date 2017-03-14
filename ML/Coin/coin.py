import matplotlib.pyplot as plt

limit = 100
p = 0.25
eps = 1e-07

optimal_function = [0 for i in range(limit+1)]
optimal_strategy = [0 for i in range(limit-1)]

end = False
while not end:
	for m in range(limit-1, 0, -1):
		max_bet = m
		max_bet = (limit - m) if max_bet > (limit - m) else max_bet

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
			end = True

		optimal_function[m] = Vmax

for i in range(limit-1):
	print("money: {} | p_win: {:.2f} | opt_str: {}".format(i+1, optimal_function[i+1], optimal_strategy[i]))

plt.figure(1)
plt.subplot(211)
plt.title('For p = {} and eps = {}\nOptimal function'.format(p, eps))
plt.plot(optimal_function[:-1], 'red')

plt.subplot(212)
plt.title('Optimal strategy')
plt.plot(optimal_strategy, 'blue')
plt.show()	
