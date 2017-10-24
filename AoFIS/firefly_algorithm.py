import numpy as np
import matplotlib.pyplot as plt

# ограничение первой областью
def restriction1(x):
    a = max(x[0], x[1]) >= 0
    b = 6*x[0] - 3*x[1] - max(2*x[0], 1*x[1]) * 0.8 <= 12.2
    c = 6*x[0] - 3*x[1] + max(2*x[0], 1*x[1]) * 0.8 >= 5.8
    
    return a and b and c

# ограничение второй областью
def restriction2(x):
    a = max(x[0], x[1]) >= 0
    b = 3*x[0] - 5*x[1] - max(0.5*x[0], 1*x[1]) * 0.7 <= 3.05
    c = 3*x[0] - 5*x[1] + max(0.5*x[0], 1*x[1]) * 0.7 >= 0.95

    return a and b and c

# функция (максимизируем её)
def f(x):
    r1 = restriction1(x)
    r2 = restriction2(x)

    return x[0] + 6*x[1] + 0.3 * max(x[0], x[1]) if r1 and r2 else -np.inf
  
def fitness(population):
    return [f(x) for x in population]

dimension = 2
fireflies = 50
episodes  = 100

ub = 5.0
lb = 0.0
population = np.random.uniform(0, 1, (fireflies, dimension)) * (ub - lb) + lb       # сгенерировать случайные равномерно распределенные fireflies точек в области [(lb, lb), (ub, ub)]

beta0 = 1.0     # коэффициент привлекательности
gamma = 1.0     # коэффициент поглощещния света
alpha = 0.5     # коэффициент мутации

for e in range(episodes):
    light = fitness(population)             # интенсивность света каждого светлячка
    arg = np.argsort(light, axis=0)[::-1]   # расположить светлячков по интенсивности света от большего к меньшему
    population = population[arg, :]         # обновить популяцию

    for i in range(fireflies):
        for j in range(fireflies):
            if light[i] < light[j]:
                r = np.sqrt(np.sum((population[i, :] - population[j, :])**2))       # евклидово расстояние от i-го светлячка до j-го
                beta_r = beta0 * np.exp(-gamma * r**2)                              # вычисление привлекательности между i-ым и j-ым светлячком
                population[i, :] += beta_r * (population[j, :] - population[i, :]) + alpha * (np.random.rand(dimension) - 0.5)      # передвинуть i-го светлячка к j-ому

                light = fitness(population)             # обновить интенсивность света
                arg = np.argsort(light, axis=0)[::-1]   # сортировка
                population = population[arg, :]         # обновить популяцию

    best = population[0]
    print('ep = {}, p = {}, light = {}'.format(e, population[0], light[0]))
print('best:', best)

# отрисовка
xx0 = []
yy0 = []
xx1 = []
yy1 = []
xx2 = []
yy2 = []

r = np.arange(-10.0, 10.0, 0.01)
for y in r:
    for x in r:
        r1 = restriction1([x, y])
        r2 = restriction2([x, y])
        if r1 and r2:
            xx0.append(x)
            yy0.append(y)
        elif r1:
            xx1.append(x)
            yy1.append(y)
        elif r2:
            xx2.append(x)
            yy2.append(y)

plt.plot(xx1, yy1)
plt.plot(xx2, yy2)
plt.plot(xx0, yy0, 'yellow')
plt.plot(best[0], best[1], 'r+', markersize=15)
plt.show()