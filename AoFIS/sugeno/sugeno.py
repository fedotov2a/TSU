small  = 0
middle = 1
big    = 2

m = 1500    # kg

# кинетическая энергия
def e_kin(v):
    return round(0.5 * m * v**2, 3)

# нечеткое отношение для скорости
# "маленькая скорость" - полутрапеция с правой стороной Mu([0, 10]) = 1, Mu(15) = 0
# "средняя скорость" - треугольное распределение Mu(10) = 0, Mu(15) = 1, Mu(20) = 0 
# "большая скорость" - полутрапеция с левой стороной Mu(15) = 0, Mu([20, +inf]) = 1 
def fuzzy_v(v):
    s = [10, 15]
    m = [10, 15, 20]
    b = [15, 20]
    
    # s - маленький
    # m - средний
    # b - большой
    # l - левая граница распределения
    # r - правая граница распределения
    # формулы расчета степени принадлежности к каждому распределению
    s_l = 1 if v < s[0] else 0
    s_r = round((s[1] - v) / (s[1] - s[0]), 3)
    m_l = round((v - m[0]) / (m[1] - m[0]), 3)
    m_r = round((m[2] - v) / (m[2] - m[1]), 3)
    b_l = round((v - b[0]) / (b[1] - b[0]), 3)
    b_r = 1 if v > b[1] else 0

    # если степень принадлежност больше 0 и меньше либо равно 1, то это то, что нужно :)
    mu = {'s_l': s_l, 's_r': s_r, 'm_l': m_l, 'm_r': m_r, 'b_l': b_l, 'b_r': b_r}
    mu = {key: val for key, val in mu.items() if val > 0 and val <= 1}

    return mu

# нечеткое отношение для расстояния
# "маленькое расстояние" - полутрапеция с правой стороной Mu([0, 20]) = 1, Mu(40) = 0
# "среднее расстояние" - трапециевидное распределение Mu(20) = 0, Mu([40, 280]) = 1, Mu(300) = 0 
# "большое расстояние" - полутрапеция с левой стороной Mu(280) = 0, Mu([300, +inf]) = 1 
def fuzzy_l(l):
    s = [20, 40]
    m = [20, 40, 280, 300]
    b = [280, 300]

    # s - маленький
    # m - средний
    # b - большой
    # l - левая граница распределения
    # m - средняя граница (у трапеции верхнее основание)
    # r - правая граница распределения
    # формулы расчета степени принадлежности к каждому распределению
    s_l = 1 if l < s[0] else 0
    s_r = round((s[1] - l) / (s[1] - s[0]), 3)
    m_l = round((l - m[0]) / (m[1] - m[0]), 3)
    m_m = 1 if m[1] < l < m[2] else 0
    m_r = round((m[3] - l) / (m[3] - m[2]), 3)
    b_l = round((l - b[0]) / (b[1] - b[0]), 3)
    b_r = 1 if l > b[1] else 0

    mu = {'s_l': s_l, 's_r': s_r, 'm_l': m_l, 'm_m': m_m, 'm_r': m_r, 'b_l': b_l, 'b_r': b_r}
    mu = {key: val for key, val in mu.items() if val > 0 and val <= 1}

    return mu

# контроллер
def sugeno(v, l):
    # e = e_kin(v)
    # right_out = [[7*e/8, 4*e/9, 2*e/3],
    #              [-43*e/60, 5*e/8, 3*e/4],
    #              [-e, -e/4, e/2]]

    # правый вывод правил
    # значения не настроены, мне лень
    right_out = [[300, 4*10**3, 6*10**5],
                 [3*10**3, 2*10**3, 3.5*10**3],
                 [700, 400, 100]]
    
    # получить степени принадлежностей
    mu_v = fuzzy_v(v)
    mu_l = fuzzy_l(l)

    # print('v:', mu_v)
    # print('l:', mu_l)

    # считаем выход
    # out = sum(y_i) * w_i / sum(w_i)
    # где y_i - значения из таблицы, w_i - степень активации правила; t-норма - минимум
    y = 0
    w = 0
    for kv, vv in mu_v.items():
        if   kv[0] == 's': i = small
        elif kv[0] == 'm': i = middle
        elif kv[0] == 'b': i = big

        for kl, vl in mu_l.items():
            if   kl[0] == 's': j = small
            elif kl[0] == 'm': j = middle
            elif kl[0] == 'b': j = big
            
            # print(min(vv, vl))
            w += min(vv, vl)                    # sum(w_i)
            y += right_out[j][i] * min(vv, vl)  # sum(y_i) * w_i
            # print('ji: {} {} {}'.format(j, i, right_out[j][i]))
    
    y = round(y, 3)
    w = round(w, 3)

    return y / w


l = 150     # m
v = 40      # km/h
v /= 3.6    # m/s

# для построения графика
v_graphic = []
l_graphic = []

print('Beg: v = {} m/s v = {} km/h l = {} m'.format(v, v*3.6, l))
for t in range(500):
    v_graphic.append(v)
    l_graphic.append(l)

    e_brake = sugeno(v, l)
    e_k = e_kin(v) - e_brake
    l -= v

    if l < 0:
        print('crash v = {} km/h v = {} m/s'.format(v*3.6, v))
        break

    v = int(((2 * e_k) / m)**(1/2))

    if v == 0:
        print('stop l = {} m'.format(l))
        break

print('End: v = {} km/h'.format(v*3.6, l))


# рисуем график зависимости расстояния от скорости
# график лучше читать справа налево, т.к начинаем не с нулевой скорости
import matplotlib.pyplot as plt
plt.plot(v_graphic, l_graphic)
plt.show()