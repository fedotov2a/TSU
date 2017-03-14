# -*- coding: utf-8 -*-

import scipy.io
import scipy.linalg
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft
from scipy.signal.windows import hamming
import lpc

def spectral_distortion(h, h1):
    return np.sum( (10*np.log10(np.abs(h)) - 10*np.log10(abs(np.abs(h1))))**2 ) / len(h)

def main():
    # читаем звуковой файл
    # Fs = 8000 для kdt_410_8.wav
    Fs, data = scipy.io.wavfile.read('kdt_410_8.wav')
#    data = np.sqrt(30)*np.random.randn(160)
#    Fs = 8000

    # делаем взаимно однозначное отображение в отрезок [-1, 1]
    data = data / data.max()
#    plt.plot(data)

    # выделяем вокализованный фрагмент
    # и берем 160 отсчётов
    N = Fs * 0.02
#    s = data[6049:6049 + N]
    s = data[12130:12130 + N]
#    s = data[14105:14105 + N]
#    s = data[0:0 + N]
#    plt.plot(s)
    
    # вычисляем автокорреляционную функцию
    # r   - автокорреляционная функция сигнала
    # eta - массив целых значений в отрезке [-M, M]
#    M = 10
    M = 10
    r, eta = lpc.xcorr(s, M, 'biased')
    plt.plot(r)
    
    # решаем систему уравнений методом Левинсона-Дарбина
    # и находим:
    # a - коэффициенты линейного предсказания
    # e - 
    # k - коэффициенты отражения
    a, e, k = lpc.durbin(r[M:],M)
    print('a=', a)
    print('e=', e)
    print('k=', k)

    print("------------------------------------------------------------------")
    '''
        FREQUENCY RESPONSE 
        показываем диапазон частот
    '''
    # plot frequency response
    NFFT = 1024
    
    # создаем массив на 512 элементов
    k = np.arange(0, NFFT//2)
    
    # формируем сигнал с помощью окна Хэмминга и преобразования Фурье
    X = np.abs( fft(s * hamming(N), NFFT) )
#    plt.plot(X)
    
    # делаем конкатенацию матрицы [[1]] с элементами матрицы a, взятых с обратным знаком
    denum = np.hstack( [np.matrix(1), -np.matrix(a)] )
    Theta = 1 * np.abs( 1 / fft(denum, NFFT) )
    
    fig,ax = plt.subplots(2,1)
    ax[0].plot( 2*k / NFFT * Fs/2, 20 * np.log10(Theta[0,k]) )
    #a[4]=a[4]+0.0001

    # plot frequency response (standart function)
    w,h=scipy.signal.freqz(np.array([1]),np.hstack([1,-a]))
#    print('w= ', w)
#    print('h= ', h)
    ax[1].plot(w/np.pi*Fs/2, 20*np.log10(np.abs(h)), 'r')

    '''
     показать как влияет изменение параметров на АЧХ фильтра
    '''
    fig,ax = plt.subplots()

#     plot frequency response (standart function)
    w,h=scipy.signal.freqz(np.array([1]),np.hstack([1,-a]))
    ax.plot(w/np.pi*Fs/2,20*np.log10(np.abs(h)),'b')

    # искажаем параметры
#    a1 = a + 0.1
    # plot frequency response (standart function)
#    w,h1=scipy.signal.freqz(np.array([1]),np.hstack([1,-a1]))
#    ax.plot(w/np.pi*Fs/2,20*np.log10(np.abs(h1)),'r')

    # The spectral distortion (SD) between H and H1 is defined by (в дБ)
#    sd = np.sum((10*np.log10(np.abs(h)) - 10*np.log10(abs(np.abs(h1))))**2)/len(h)
#    sd = spectral_distortion(h, h1)

    # оформить в виде функции: sd=spectral_distortion(h,h1)

    # построить графики и получить значения sd при изменении всех коэффициентов
    # на 0.05, на 0.1, на 0.2
    
    a_005 = a + 0.05
    w_005, h_005 = scipy.signal.freqz(np.array([1]),np.hstack([1,-a_005]))
    ax.plot(w_005/np.pi*Fs/2, 20*np.log10(np.abs(h_005)),'r')

    sd_005 = spectral_distortion(h, h_005)
    print(sd_005)
    
    a_01 = a + 0.1
    w_01, h_01 = scipy.signal.freqz(np.array([1]),np.hstack([1,-a_01]))
    ax.plot(w_01/np.pi*Fs/2, 20*np.log10(np.abs(h_01)),'g')

    # The spectral distortion (SD) between H and H1 is defined by (в дБ)
    sd_01 = spectral_distortion(h, h_01)
    print(sd_01)
    
    a_02 = a + 0.2
    w_02, h_02 = scipy.signal.freqz(np.array([1]),np.hstack([1,-a_02]))
    ax.plot(w_02/np.pi*Fs/2, 20*np.log10(np.abs(h_02)),'y')

    # The spectral distortion (SD) between H and H1 is defined by (в дБ)
    sd_02 = spectral_distortion(h, h_02)
    print(sd_02)
    
    
    # показать как влияет изменение коэффициентов отражения на АЧХ фильтра
    # построить графики и получить значения sd при изменении всех коэффициентов
    # на 0.05, на 0.1, на 0.2
#
#
#    '''
#     find frequencies by root-solving
#    '''
    fig,ax = plt.subplots()

    # plot frequency response (standart function)
    # строим диапазон частот
    w,h=scipy.signal.freqz(np.array([1]),np.hstack([1,-a]))
    ax.plot(w/np.pi*Fs/2,20*np.log10(np.abs(h)),'b')

    # find roots of polynomial
    aa=np.roots(np.hstack([1,-a]))
    # convert to Hz
    ffreq = np.arctan2(aa.imag, aa.real)*Fs/(2*np.pi)
    # only look for roots >0Hz up to fs/2
    ffreq = ffreq[(ffreq>0)]
    print(ffreq)
    oy=20*np.log10(np.abs(h))
    
    ax.stem(ffreq,np.max(oy)*np.ones(len(ffreq)))
    ax.grid()

    '''
    LINE SPECTRAL FREQUENCIES
    '''
    # две функции расчета lsf: generate_lsp и poly2lsf
    pf,qf,lsf = lpc.generate_lsp(np.hstack([1,-a]),M)
    print('pf=',pf)
    print('qf=',qf)
    print('lsf1=',lsf * 8000)

    aa=np.hstack([1,-a])
    lsf = lpc.poly2lsf(aa)
#    print('lsf2=',lsf)

    # обратная функция
    aa_ = lpc.lsf2poly(lsf*(2*np.pi))
#    print('aa = ', aa)
#    print('aa_ = ', aa_)

    '''
    QUANTIZING THE LINE SPECTRAL FREQUENCIES

    '''
    #Quantization table matrix
    lspQ = np.array([
		[100, 170, 225, 250, 280, 340, 420, 500, 0, 0, 0, 0, 0, 0, 0, 0],
		[210, 235, 265, 295, 325, 360, 400, 440, 480, 520, 560, 610, 670, 740, 810, 880],
		[420, 460, 500, 540, 585, 640, 705, 775, 850, 950, 1050, 1150, 1250, 1350, 1450, 1550],
		[620, 660, 720, 795, 880, 970, 1080, 1170, 1270, 1370, 1470, 1570, 1670, 1770, 1870, 1970],
		[1000, 1050, 1130, 1210, 1285, 1350, 1430, 1510, 1590, 1670, 1750, 1850, 1950, 2050, 2150, 2250],
		[1470, 1570, 1690, 1830, 2000, 2200, 2400, 2600, 0, 0, 0, 0, 0, 0, 0, 0 ],
		[1800, 1880, 1960, 2100, 2300, 2480, 2700, 2900, 0, 0, 0, 0, 0, 0, 0, 0 ],
		[2225, 2400, 2525, 2650, 2800, 2950, 3150, 3350, 0, 0, 0, 0, 0, 0, 0, 0 ],
		[2760, 2880, 3000, 3100, 3200, 3310, 3430, 3550, 0, 0, 0, 0, 0, 0, 0, 0 ],
		[3190, 3270, 3350, 3420, 3490, 3590, 3710, 3830, 0, 0, 0, 0, 0, 0, 0, 0 ]
	])
    bits = np.array([3, 4, 4, 4, 4, 3, 3, 3, 3, 3])
    findex = lpc.lsp_quant(lsf, M, bits, lspQ)


    # Conversion of findex to quant. lsf
    freq_q = lpc.findex2lsp(findex,lspQ)
    print('freq_q', freq_q)

    # Conversion of LSP  to LP coefficients
    aq = lpc.lsf2poly(freq_q/Fs*(2*np.pi))
    print('aq = ', aq)
    print(a)
    # сравнить с исх. коэффициентами:
    
    # построить частотную характеристику фильтра 
    # оценить искажение /  построить график spectrum distortion    
    fig,ax = plt.subplots()
    w, h_ = scipy.signal.freqz(np.array([1]),np.hstack([1,-a]))
    ax.plot(w/np.pi*Fs/2,20*np.log10(np.abs(h_)),'b')
    
    w, h_1 = scipy.signal.freqz(np.array([1]),aq)
    ax.plot(w/np.pi*Fs/2,20*np.log10(np.abs(h_1)),'r')
    
    sd_ = spectral_distortion(h_, h_1)
    print(sd_)
    
    # синтезировать сегмент сигнала по коэфф.лин. пред. до и после квантования
    e_ = e    
    for i in range(4):
        e_ = np.hstack([e_, e_])
        
    s_a = scipy.signal.lfilter(np.array([1]), np.hstack([1, -a]), e_)    
    s_aq = scipy.signal.lfilter(np.array([1]), aq, e_)
#    
#    e_wn = np.sqrt(10)*np.random.randn(160) 
#    s_a = scipy.signal.lfilter(np.array([1]), np.hstack([1, -a]), e_wn)    
#    s_aq = scipy.signal.lfilter(np.array([1]), np.hstack([1, -aq]), e_wn)
    
    
    fig,ax = plt.subplots(2,1)
    ax[0].plot(s_a)
    ax[1].plot(s_aq)
    # построить графики
    # повторить все для другого вокализованного сегмента и невокализованного



    plt.show()



if __name__ == '__main__':
    main()

