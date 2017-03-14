# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.io
import scipy.signal
from scipy.signal import lfilter
import numpy as np

def xcorr(x,m,scaleopt='none'):
    r = np.correlate(x, x, mode = 'full')
    i0 = r.argmax()
    r = r[i0-m:i0+m+1]
    eta = np.arange(-m, m+1)
    zn = 1
    if scaleopt == 'unbiased':
        zn=len(x)-np.abs(eta)
    if scaleopt == 'biased':
        zn=len(x)
    r=r/zn
    return r, eta
    
#def E(R, a, p):
#    s = 0
#    for i in range(p):
#       s = s + a[0, i] * R[i]
#    
#    return R[0] - s
    
#def durbin(r, M):
#    kappa = np.zeros(M)
#    a     = np.zeros(M)
#    xi    = [r[0], np.zeros[M]]
#    eps = 0.001
#    
#    for j in range(M):
#        kappa[j] = (r[j+1] - a[:(j-1)] * r[j:-1:2]) / (xi[j] + eps)
#        a[j]     = kappa[j]
#        a[:j-1] = a[:j-1] - kappa[j] * a[j-1:-1:1]
#        xi[j+1] = xi[j] * (1 - kappa[j] * kappa[j])
#    return [a, xi, kappa]
#    

def main():
    x = np.array([1, 2, 3, 4, 5])
    M = 3
    r, eta = xcorr(x, M, 'unbiased')
    print(r, eta)
    
    r, eta = xcorr(x, M, 'biased')
    print(r, eta)
    
    r, eta = xcorr(x, M, 'none')
    print(r, eta)
    
    #---
    dta = scipy.io.loadmat('digits',squeeze_me=True,struct_as_record=False)
    s = dta['digits'].three1
    x = s.astype('int32')
#    plt.plot(x)
    
    #---
    m = 2756
    N = 256
    x = x[m-N:m]
    M = 14
    r, eta = xcorr(x, M, 'biased')
    R = np.matrix(scipy.linalg.toeplitz(r[M:M+M]))
    b = np.matrix(r[M+1:])
    a = b * np.linalg.inv(R)
    
#    print(a)
#    print(x[:3])
    
#    plt.plot(eta, r)
#    plt.plot(eta, r)
#    plt.show()
    r = r[M:2*M]
#    print(r)
    
    Rx = scipy.linalg.toeplitz(r)
    print(Rx[0:4][0:4])
    
#    a = Rx / b
    a = b * np.linalg.inv(Rx)
    print(a)
    
    #---
    E_ = E(b, a, len(a))    # wat?
    print(E_)
    
    #--5
#    p = np.arange(1, 14)
#    e = []
#    for k in p:
#        M = k
#        r, eta = xcorr(x, M, 'biased')
#        Rx = scipy.linalg.toeplitz(r[M:2*M])
#        rx = r[M+1 : 2 * M+1]
#        a = Rx // rx
#        e.append(1 - rx * a / r[M+1])
#    
#    plt.plot(p, e)

    

    
if __name__ == '__main__':
    main()