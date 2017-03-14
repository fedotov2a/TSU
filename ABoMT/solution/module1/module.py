# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.io
import scipy.signal
from scipy.signal import lfilter
import numpy as np

def HPS(x, N, R):
    fs = 16000
    k = 2000 * N // fs
    sp = np.fft.fft(x * np.hamming(len(x)), N)
    f = np.arange(len(sp))*(fs/len(sp))
    sp = sp[:k]
    f  = f[:k]
    
    if R > 1:
        p_sp = []
        for i in range(2, R+1):
            p_sp.append(sp[0:-1:i])
        
        p_sp_dim = []
        for q in p_sp:
            p_sp_dim.append(q[:len(p_sp[-1])])
        
        p = np.ones(len(p_sp_dim[0]))  
        for q in p_sp_dim:
            p = p * q
    #    print(p)
        f1 = f[0:len(p_sp[-1]):1]
    
        y = 20 * np.log10(np.abs(p))
        y1 = y[0:len(y)//2]
        m = y1.argmax()
    #    
    #    print(m)
    #    print(f1[m])
        return [m, f1[m]]
        
def autocorrelation(x):
    fs = 16000
    r = np.correlate(x, x, mode='full')
    r = r[int(r.size/2):]
    ms20 = int(20/1000 * fs)
    ms2 = int(2/1000 * fs)
    i = r[ms2:ms20].argmax()
    print('i={} ms2={} ms20={}'.format(i, ms2, ms20))
    return r, fs / (i + ms2)
        
def pitch(x, m, N):
    peak = 0
    for l in np.arange(20, 150):
        autoc = 0
        for n in np.arange(m - N + 1, m):
            autoc = autoc + x[n] * x[n-l]
        if autoc > peak :
            peak = autoc
            lag = l
    return lag
    
def pitch_md(x, m, N):
    min_ = np.inf
    for l in np.arange(20, 150):
        mdf = 0
        for n in np.arange(m - N + 1, m):
            mdf = mdf + np.abs(x[n] - x[n-l])
        if mdf < min_:
            min_ = mdf
            lag = l
    return lag
    
def cepstrum(data):
    fs = 16000
    t_frame = 0.02
    kol_sampes = fs * t_frame
    x = data[25124:25124 + kol_sampes] 
    t = np.arange (0, len(x))/fs 
    fig, ax = plt.subplots(3, 1)  
    ax[0].plot(t, x) 
    
    y = np.fft.fft(x*np.hamming(len(x)),2048) 
    fs_05 = fs / 2 
    hz5000 = fs_05 * len(y) / fs 
    f = np.arange(0, hz5000) * fs / len(y) 
    ax[1].plot(f, 20*np.log10(np.abs(y[0 : len(f)]))) 
    ax[1].grid() 
    
    C = np.fft.fft(np.log(abs(y))) 
    ms2 = int(2/1000*fs) 
    ms20 = int(20/1000*fs) 
    q = np.arange(ms2, ms20)/ fs 
    ax[2].plot(q, np.abs(C[ms2:ms20])) 
    ax[2].grid() 
    
    fx = np.abs(C[ms2:ms20]).argmax() 
    print("fx=", fs/(ms2+fx-1)) 
    plt.show()

def main():
    sample_rate, data = wav.read('kdt_413.wav') 
#    fig, ax = plt.subplots(1, 1) 
#    ax.set_xlabel("sec") 
#    ax.set_ylabel("Amplitude") 
#    ax.plot(np.arange(len(data[25124:27301])) / sample_rate, data[25124:27301]) 
#    plt.show()
    
    fs = 16000
    t_frame = 0.02
    kol_sampes = fs * t_frame
    vocal_frame = data[25124:25124 + kol_sampes]
    n = 2048
    sp = np.fft.fft(vocal_frame, n)
    f = np.arange(len(sp))*(fs/len(sp))
    k = 2000 * n // fs
    fig, ax = plt.subplots(1, 1) 
    ax.plot(f[:k], 20 * np.log(np.abs(sp[:k]))) 
    print(f[sp[:k].argmax()]) 
    plt.show()     

    r = autocorrelation(vocal_frame)
    
    hps = HPS(vocal_frame, 2048, 5)
    print("hps={}".format(hps[1]))
    
    p = pitch(vocal_frame, 320, 160)
    print(p)
    
    p_md = pitch_md(vocal_frame, 320, 160)
    print(p_md)
    
    cepstrum(data)    
    
if __name__ == '__main__':
    main()