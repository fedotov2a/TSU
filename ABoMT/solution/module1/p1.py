# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.io
import scipy.signal
from scipy.signal import lfilter
import numpy as np

def HPS(x, N, R):
    fs = 8000
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
    
    

def main():
# --.1
#    data = scipy.io.loadmat('ma1_1', squeeze_me=True, struct_as_record=False)
    sample_rate, data = wav.read('kdt_413.wav')
    fs = 16000
    t_frame = 0.02
    kol_sampes = fs * t_frame
#    signal = data['ma1_1']
#    vocal_frame = signal[4160:4160 + kol_sampes]
    vocal_frame = data[8580:8580 + kol_sampes]
    
#    plt.plot(data)
    plt.plot(vocal_frame)

# --.2    
    sp = np.fft.fft(vocal_frame)
    f = np.arange(len(sp))*(fs/len(sp))
#    plt.plot(f, 20 * np.log10(np.abs(sp)))

# --.3
    n = 2048
    sp = np.fft.fft(vocal_frame, n)
    f = np.arange(len(sp))*(fs/len(sp))
#    plt.plot(f, 20 * np.log10(np.abs(sp)))
    
# --.4
    sp = np.fft.fft(vocal_frame*np.hamming(len(vocal_frame)), n)
    f = np.arange(len(sp))*(fs/len(sp))
#    plt.plot(f, 20 * np.log10(np.abs(sp)))

# --.5
    f1 = f[0:512]
#    d = 20 * np.log10(np.abs(sp))
#    d = d[0:512]
    d = sp[0:512]
#    plt.plot(f1, d)
    
# --.6  
    sp2 = d[0:-1:2]
#    plt.plot(f1[0:len(sp2)], sp2)

# --.7
    sp3 = d[0:-1:3]
#    plt.plot(f1[0:len(sp3)], sp3)

# --.8
    sp4 = d[0:-1:4]
#    plt.plot(f1[0:len(sp4)], sp4)

# --.9
    sp5 = d[0:-1:5]
#    plt.plot(f1[0:len(sp5)], sp5)
    
# --.10
    p = sp[:len(sp5)] * sp2[:len(sp5)] * sp3[:len(sp5)] * sp4[:len(sp5)] * sp5
#    print(p)
    f1 = f[0:len(sp5):1]
#    plt.plot(f1, 20 * np.log10(np.abs(p)))

# --.11
    y = 20 * np.log10(np.abs(p))
    y1 = y[0:len(y)//2]
    m = y1.argmax()
#    print(m)
#    print(f1[m])

# --.12
    hps = HPS(vocal_frame, 2048, 5)
    print(hps[0])
    print(hps[1])


if __name__ == '__main__':
    main()