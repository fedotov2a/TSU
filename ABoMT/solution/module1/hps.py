# -*- coding: utf-8 -*-
import numpy as np

def HPS(x, N, R):
    fs = 8000
    k = 2000 * N // fs
    sp = np.fft.fft(x * np.hamming(len(x)), N)
    f = np.arange(len(sp))*(fs/len(sp))
    sp = sp[:k]
    f  = f[:k]
    
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
    
    print(m)
    print(f1[m])
    return [m, f1[m]]
    
#Кореляционный метод
def corrMethod(x):
    r = np.correlate(x, x, mode='full')
    r = r[int(r.size/2):]
    ms20 = int(20/1000*fs)
    ms2 = int(2/1000*fs)
    i = r[ms2:ms20].argmax()
    print('i={} ms2={} ms20={}'.format(i, ms2, ms20))
    return r, fs/(i+ms2)



def pitch(x, m, N):
    peak = 0
    graph = np.arange(200)
    fig,plot = plt.subplots()
    for l in np.arange(20, 150):
        autoc = 0
        for n in np.arange(m - N + 1, m):
            autoc = autoc + x[n] * x[n - l]
        graph[l] = autoc
        if autoc > peak :
            peak = autoc
            lag = l
    plot.plot(graph)
    plt.show()
    return lag


def pitch_md(x, m, N):
    min_ = np.inf
    graph = np.arange(200)
    fig,plot = plt.subplots()
    for l in np.arange(20, 150):
        mdf = 0
        for n in np.arange(m - N + 1, m):
            mdf = mdf + np.abs(x[n] - x[n-l])
        graph[l]=mdf
        if mdf < min_:
            min_ = mdf
            lag = l
    plot.plot(graph)
    plt.show()
    return lag
    

    
def main():
    pass

if __name__ == "__main__":
    main()
