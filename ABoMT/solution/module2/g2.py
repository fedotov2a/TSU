# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.io
import scipy.signal
from scipy.signal import lfilter
import numpy as np

def main():
    

# -- syntes
    data = scipy.io.loadmat('var2', squeeze_me=True, struct_as_record=False)
    a = data['a']   # коэффициенты линейного предсказания
    P = data['P']   # период основного тона
    G = data['G']   # коэффициент усиления
    
    fs = 16000    
    N  = 0.02 * fs

    print(a, P, G)
    
    e1 = np.zeros(320)
    e1[0] = G[0]
    e1[140] = G[0]
    e1[280] = G[0]
    
    e2 = np.zeros(320)
    e2[104] = G[1]
    e2[248] = G[1]
    
    e3 = np.zeros(320)
    e3[72] = G[1]
    e3[216] = G[1]
    
#    e = np.zeros(320 * 3)
#    e = np.concatenate((e1, e2, e3))
    
    a0 = a[:,0]    
    a1 = a[:,1]
    a2 = a[:,2]
    
    s1 = scipy.signal.lfilter(np.array([1]), np.hstack([1, -a0]), e1)
    s2 = scipy.signal.lfilter(np.array([1]), np.hstack([1, -a1]), e2)
    s3 = scipy.signal.lfilter(np.array([1]), np.hstack([1, -a2]), e3)
    
    s = np.concatenate((s1, s2, s3))
    
    plt.plot(s)
    
    

if __name__ == '__main__':
    main()