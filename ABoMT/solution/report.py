# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import scipy.io
import scipy.signal
from scipy.signal import lfilter
from scipy.signal import convolve
import numpy as np
 


# signal smoothing
def prog1():
    n = 50
    s = [2 * m * 0.9**m for m in range(n)]
    
    w = np.random.uniform(0.0, 1.0, n)
    d = [0.8 * (w[m] - 0.5) for m in range(n)]
    
    x = [(s[m] + d[m]) for m in range(n)]
    y = [((x[m-1] + x[m] + x[m+1]) / 3.0) for m in range(1, n - 1)]
    
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(d, color='r', linestyle='-')
    ax[0].plot(s, color='g', linestyle='--') 
    ax[0].plot(x, color='b', linestyle='-.')
    ax[0].grid()
    ax[0].set_xlabel('Time index n')
    ax[0].set_ylabel('Amplitude')
    
    ax[1].plot(s, color='r', linestyle='-')
    ax[1].plot(y, color='g', linestyle='--') 
    ax[1].grid()
    ax[1].set_xlabel('Time index n')
    ax[1].set_ylabel('Amplitude')
    
    plt.show()

# Amplitude-modulated signal
def prog2():
    n = np.arange(100)
    w_H = 2 * np.pi * 0.1
    w_L = 2 * np.pi * 0.01
    
    x_H = np.cos(w_H * n)
    x_L = np.cos(w_L * n)
    
    A = 1.0
    m = 0.4
    
    y = A * (1.0 + m * x_L) * x_H
    
    plt.plot(y, '.')
    plt.stem(n, y)
    plt.show()

# linearly frequency-modulated signal
def prog3():
    n = np.arange(100)
    a = np.pi / 2.0 / 100.0
    y = np.cos(a * n**2)
    
    a2 = np.pi / 4.0 / 100.0
    y2 = np.cos(a2 * (n * (0.8 * n + 40)))
    
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(y2, '-')
    ax[0].stem(n, y2)
    ax[0].grid()

    #ax[1].plot(n[40:60], y[40:60]) 
    ax[1].stem(n[40:60], y[40:60])
    ax[1].grid()
    
    plt.show()
    
# moving average filter
def prog4():
    n = np.arange(100)
    s1 = np.sin(2 * np.pi * 0.05 * n)    
    s2 = np.sin(2 * np.pi * 0.47 * n)
    x = s1 + s2
    
    m = 2
    num = np.ones(m)
    y = lfilter(num, 1, x) / m
    
    y2 = np.zeros(100)
    y2[0] = x[0] / 2.0
    for n in np.arange(1,100):
        y2[n] = (x[n]-x[n-1]) / 2.0
        
    
    a = np.pi / 2 / 100
    M = 2
    n2 = np.arange(100)
    x2 = np.cos(a * n2**2)

    y3 = lfilter(np.ones(M), 1, x2) / M

    y4 = np.zeros(100)
    y4[0] = x2[0]/2
    for n in np.arange(1,100):
        y4[n] = (x2[n]-x2[n-1]) / 2



    fig, ax = plt.subplots(2, 2)
    
    ax[0][0].plot(s1)
    ax[0][0].grid()

    ax[0][1].plot(s2)
    ax[0][1].grid()    
    
    ax[1][1].plot(y3)
    ax[1][1].grid()

    ax[1][0].plot(y4)
    ax[1][0].grid()
 
    plt.show()
    
def prog5():
    n = np.arange(40)
    x1 = np.cos(2 * np.pi * 0.1 * n)
    x2 = np.cos(2 * np.pi * 0.4 * n)
 
    a =  2
    b = -3
    x = a * x1 + b * x2
    
    coeff_x = [2.2403, 2.4908, 2.2403]
    coeff_y = [1, -0.4, 0.75]
    
    y1 = lfilter(coeff_x, coeff_y, x1)
    y2 = lfilter(coeff_x, coeff_y, x2)
    y  = lfilter(coeff_x, coeff_y, x)
    
    diff = y - (a * y1 + b * y2)
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].stem(y)
    ax[0].grid()

    ax[1].stem(a * y1 + b * y2)
    ax[1].grid()
    
    ax[2].stem(diff)
    ax[2].grid()
 
    plt.show()

def prog5_1():
    n = np.arange(40)
    x1 = np.cos(2 * np.pi * 0.1 * n)
    x2 = np.cos(2 * np.pi * 0.4 * n)
 
    a =  2
    b = -3
    x = a * x1 + b * x2
    
    y1 = np.zeros(40)
    y2 = np.zeros(40)
    y  = np.zeros(40)
    
    for k in np.arange(1, 40):
        y1[k] = x1[k] * x1[k-1]
        y2[k] = x2[k] * x2[k-1]
        y[k]  = x[k] * x[k-1]
    
    diff = y - (a * y1 + b * y2)
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].stem(y)
    ax[0].grid()

    ax[1].stem(a * y1 + b * y2)
    ax[1].grid()
    
    ax[2].stem(diff)
    ax[2].grid()
 
    plt.show()
    
def prog6():
    n = np.arange(100)
    x1 = np.cos(2 * np.pi * 0.1 * n)
    x2 = np.cos(2 * np.pi * 0.4 * n)
    
    x1_ = np.cos(2 * np.pi * 0.1 * (n-10))
    x2_ = np.cos(2 * np.pi * 0.4 * (n-10))

 
    a = 2
    b = 3
    x  = a * x1  + b * x2
    x_ = a * x1_ + b * x2_
    
    coeff_x = [2.2403, 2.4908, 2.2403]
    coeff_y = [1, -0.4, 0.75]
    
    y = lfilter(coeff_x, coeff_y, x)
    yd = lfilter(coeff_x, coeff_y, x_)
    
    diff_y = y - yd
    diff_x = x - x_    
    
    x_n1_1 = np.cos(2 * np.pi * 0.1 * (n-1))
    x_n1_2 = np.cos(2 * np.pi * 0.4 * (n-1))
    x_n1   = a * x_n1_1 + b * x_n1_2
    x_n    = n * x
    
    y_n = lfilter(coeff_x, coeff_y, x_n + x_n1)
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].stem(y_n)
    ax[0].grid()

    ax[1].stem(diff_y)
    ax[1].grid()
    
    ax[2].stem(diff_x)
    ax[2].grid()
 
    plt.show()
    
def prog7():
    N = 40
    x = np.zeros(N)
    x[0] = 1
    coeff_x = [2.2403, 2.4908, 2.2403]
    coeff_y = [1, -0.4, 0.75]
    
    h = lfilter(coeff_x, coeff_y, x)
    nn = np.arange(N)
    
    N2 = 45
    coeff_x1 = [0.9, -0.45, 0.35, 0.002]
    coeff_y1 = [1,   0.71, -0.46, -0.62]
    x = np.zeros(N2)
    x[0] = 1
    h = lfilter(coeff_x1, coeff_y1, x)
    nn = np.arange(N2)
    
    plt.stem(nn, h)
    plt.grid()
 
    plt.show()
    
def prog8():
    N = 40
    x = np.zeros(N)
    x[0] = 1
    
    coeff_x_4 = [0.06, -0.19, 0.27, -0.26, 0.12]
    coeff_y_4 = [1, 1.6, 2.28, 1.325, 0.68]
    
    coeff_x1_2 = [0.3, -0.2, 0.4]
    coeff_y1_2 = [1, 0.9, 0.8]
    
    coeff_x2_2 = [0.2, -0.5, 0.3]
    coeff_y2_2 = [1, 0.7, 0.85]
        
    h_4 = lfilter(coeff_x_4, coeff_y_4, x)
    nn_4 = np.arange(N)
    
    h1_2 = lfilter(coeff_x1_2, coeff_y1_2, x)
    nn1_2 = np.arange(N) 
    
    h2_2 = lfilter(coeff_x2_2, coeff_y2_2, h1_2)
    nn2_2 = np.arange(N)
    
    diff = h_4 - h2_2
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].stem(nn_4, h_4)
    ax[0].grid()

    ax[1].stem(nn1_2, h2_2)
    ax[1].grid()
    
    ax[2].stem(diff)
    ax[2].grid()
 
    plt.show()

def prog8_1():
    n = np.arange(40)
    x = np.sin(2 * np.pi * 0.1 * n)
    
    coeff_x = [0.06, -0.19, 0.27, -0.26, 0.12]   
    coeff_y = [1, 1.6, 2.28, 1.325, 0.68]
    
    y = lfilter(coeff_x, coeff_y, x)
    
    coeff_x1 = [0.3, -0.2, 0.4]
    coeff_y1 = [1, 0.9, 0.8]
    
    y1 = lfilter(coeff_x1, coeff_y1, x)
    
    coeff_x2 = [0.2, -0.5, 0.3]
    coeff_y2 = [1, 0.7, 0.85]
    
    y2 = lfilter(coeff_x2, coeff_y2, y1)
    
    diff = y - y2
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].stem(n, y)
    ax[0].grid()

    ax[1].stem(n, y2)
    ax[1].grid()
    
    ax[2].stem(diff)
    ax[2].grid()
 
    plt.show()

    
def prog9():
    h = [3, 2, 1, -2, 1, 0, -4, 0, 3]
    x = [1, -2, 3, -4, 3, 2, 1]
    
    y_conv = convolve(x, h)
    y_filter = lfilter(h, 1, np.concatenate((x,np.zeros(8)), axis=0))
    
    fig, ax = plt.subplots(2, 1)
    
    ax[0].stem(y_conv)
    ax[0].grid()
    
    ax[1].stem(y_filter)
    ax[1].grid()
    
    plt.show()

    
def prog10():
    n = np.arange(300)
    x1 = np.cos(20 * np.pi * n / 256)
    x2 = np.cos(200 * np.pi * n / 256)
    x = x1 + x2
    
    coeff_x1 = [0.5, 0.27, 0.77]
    coeff_y1 = [1]
    
    coeff_x2 = [0.45, 0.5, 0.45]
    coeff_y2 = [1, -0.53, 0.46]
    
    y1 = lfilter(coeff_x1, coeff_y1, x)
    y2 = lfilter(coeff_x2, coeff_y2, x)

    fig, ax = plt.subplots(3, 1)
    
    ax[0].plot(x)
    ax[0].grid()

    ax[1].plot(y1)
    ax[1].grid()
    
    ax[2].plot(y2)
    ax[2].grid()
 
    plt.show()
    
def prog10_1():
    n = np.arange(300)
    
    x = np.cos(2 * np.pi * n**2 * 0.5 / 300)
    
    coeff_x1 = [0.5, 0.27, 0.77]
    coeff_y1 = [1]
    
    coeff_x2 = [0.45, 0.5, 0.45]
    coeff_y2 = [1, -0.53, 0.46]
    
    y1 = lfilter(coeff_x1, coeff_y1, x)
    y2 = lfilter(coeff_x2, coeff_y2, x)
    
    fig, ax = plt.subplots(3, 1)
    
    ax[0].plot(x)
    ax[0].grid()

    ax[1].plot(y1)
    ax[1].grid()
    
    ax[2].plot(y2)
    ax[2].grid()
 
    plt.show()
    
    
def main():
    prog10_1()
    

if __name__ == '__main__':
    main()
