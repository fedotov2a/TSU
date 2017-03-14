#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      maxim
#
# Created:     14.11.2013
# Copyright:   (c) maxim 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
from scipy.signal import deconvolve
def xcorr(x,m,scaleopt='none'):
    r=np.correlate(x, x, mode = 'full')
    i0 = r.argmax()
    r=r[i0-m:i0+m+1]
    eta=np.arange(-m,m+1)
    zn = 1
    if scaleopt == 'unbiased':
        zn=len(x)-np.abs(eta)
    if scaleopt == 'biased':
        zn=len(x)
    r=r/zn
    return r,eta

def durbin(r,m):
    l=0
    E=np.zeros(m+1)
    E[0]=r[0]
    a=np.zeros(m+1)
    k=np.zeros(m+1)
    a[0] = 0
    for l in range(1,m+1):
        r_=r[l-1::-1]
        a_=a[1:l+1]
        ss=np.dot(a_,r_)
        k[l]=(ss-r[l])/E[l-1]
        a[l]=-k[l]
##        for j in range(1,l+1):
##            a[j]=a[j]+k[l]*a[l-j]
        a[1:l] += k[l]*a[l-1:0:-1]
        E[l]=E[l-1]*(1-k[l]**2)
    a1 = a[1:]
    return a1,E,-k[1:]

def generate_lsp(a,m):
    # [p,q,pf,qf]=generate_lsp(a,m)
    # MAXORD-  Maximum  order  of  P  or  Q(here  24)
    MAXORD  =   24
    MAXNO   =  m
    #   INIT   LOCAL  VARIABLES
    p  =   np.zeros (   MAXORD  )
    q  =   np.zeros (   MAXORD  )
    mp   = m + 1
    mh   = m//2
    # GENERATE P AND Q POLYNOMIALS
    p = a[ 1:mh+1 ] + a[ m:m-mh:-1 ]
    q = a[ 1:mh+1 ] - a[ m:m-mh:-1 ]
    p = p[0:mh]
    q = q[0:mh]
    # ALL THE COEFFICIENTS
    pf = np.hstack([1,p,p[-1::-1],1])
    qf = np.hstack([1,q,-q[-1::-1],-1])
    # find frequencies by root-solving
    aa=np.roots(np.hstack(pf)) # find roots of polynomial
    ffreq_p = np.arctan2(aa.imag,aa.real)/(2*np.pi) # convert to Hz
    ffreq_p = ffreq_p[(ffreq_p>0)] # only look for roots >0Hz up to fs/2
    #print(ffreq_p)
    aa=np.roots(np.hstack(qf)) # find roots of polynomial
    ffreq_q = np.arctan2(aa.imag,aa.real)/(2*np.pi) # convert to Hz
    ffreq_q = ffreq_q[(ffreq_q>0)] # only look for roots >0Hz up to fs/2
    #print(ffreq_q)
    ffreq = np.hstack([ffreq_q,ffreq_p])
    ffreq = np.sort(ffreq)
    #print(ffreq)

    return pf,qf,ffreq[0:-1]

def lsf2poly(lsf):
    """Convert line spectral frequencies to prediction filter coefficients

    returns a vector a containing the prediction filter coefficients from a vector lsf of line spectral frequencies.

    .. doctest::

        >>> lsf = [0.7842 ,   1.5605  ,  1.8776 ,   1.8984,    2.3593]
        >>> a = lsf2poly(lsf)
        array([  1.00000000e+00,   6.14837835e-01,   9.89884967e-01,
            9.31594056e-05,   3.13713832e-03,  -8.12002261e-03 ])

    .. seealso:: poly2lsf, rc2poly, ac2poly, rc2is
    """
    #   Reference: A.M. Kondoz, "Digital Speech: Coding for Low Bit Rate Communications
    #   Systems" John Wiley & Sons 1994 ,Chapter 4

    # Line spectral frequencies must be real.

    lsf = np.array(lsf)

    if max(lsf) > np.pi or min(lsf) < 0:
        raise ValueError('Line spectral frequencies must be between 0 and pi.')

    p = len(lsf) # model order

    # Form zeros using the LSFs and unit amplitudes
    z  = np.exp(1.j * lsf)

    # Separate the zeros to those belonging to P and Q
    rQ = z[0::2]
    rP = z[1::2]

    # Include the conjugates as well
    rQ = np.concatenate((rQ, rQ.conjugate()))
    rP = np.concatenate((rP, rP.conjugate()))

    # Form the polynomials P and Q, note that these should be real
    Q  = np.poly(rQ);
    P  = np.poly(rP);

    # Form the sum and difference filters by including known roots at z = 1 and
    # z = -1

    if p%2:
        # Odd order: z = +1 and z = -1 are roots of the difference filter, P1(z)
        P1 = np.convolve(P, [1, 0, -1])
        Q1 = Q
    else:
        # Even order: z = -1 is a root of the sum filter, Q1(z) and z = 1 is a
        # root of the difference filter, P1(z)
        P1 = np.convolve(P, [1, -1])
        Q1 = np.convolve(Q, [1,  1])

    # Prediction polynomial is formed by averaging P1 and Q1

    a = .5 * (P1+Q1)
    return a[0:-1:1] # do not return last element


def poly2lsf(a):
    """Prediction polynomial to line spectral frequencies.

    converts the prediction polynomial specified by A,
    into the corresponding line spectral frequencies, LSF.
    normalizes the prediction polynomial by A(1).

    .. doctest::

        >>> a = [1.0000  ,  0.6149   , 0.9899   , 0.0000 ,   0.0031,   -0.0082
        >>> lsf = poly2lsf(a)
        >>> lsf =  array([  0.7842,    1.5605 ,   1.8776 ,   1.8984,    2.3593])

    .. seealso:: lsf2poly, poly2rc, poly2qc, rc2is
    """

    #Line spectral frequencies are not defined for complex polynomials.

    # Normalize the polynomial

    a = np.array(a)
    if a[0] != 1:
        a/=a[0]

    if max(np.abs(np.roots(a))) >= 1.0:
        error('The polynomial must have all roots inside of the unit circle.');


    # Form the sum and differnce filters

    p  = len(a)-1   # The leading one in the polynomial is not used
    a1 = np.concatenate((a, np.array([0])))
    a2 = a1[-1::-1]
    P1 = a1 - a2        # Difference filter
    Q1 = a1 + a2        # Sum Filter

    # If order is even, remove the known root at z = 1 for P1 and z = -1 for Q1
    # If odd, remove both the roots from P1

    if p%2: # Odd order
        P, r = deconvolve(P1,[1, 0 ,-1])
        Q = Q1
    else:          # Even order
        P, r = deconvolve(P1, [1, -1])
        Q, r = deconvolve(Q1, [1,  1])

    rP  = np.roots(P)
    rQ  = np.roots(Q)

    aP  = np.angle(rP[1::2])
    aQ  = np.angle(rQ[1::2])

    lsf = sorted(np.concatenate((-aP,-aQ)))

    return np.array(lsf)/(2*np.pi)

def lsp_quant( freq, no, bits, lspQ ):
    '''
    freq - Unquantized LSFs
    no - Number of LSFs (10 here)
    bits - Array of bits to be allocated for each LSF
    lspQ - Quantization table matrix
    return findex - Vector of indices to quantized LSFs, references lspQ
    '''
    # DEFINE CONSTANTS
    FSCALE = 8000.00
    MAXNO = 10

    # INIT RETURN VECTOR
    findex = np.zeros( MAXNO )

    # INIT LOCAL VARIABLES
    freq = FSCALE * freq
    levels = ( 2 ** bits ) - 1

    # QUANTIZE ALL LSP FREQUENCIES AND FORCE MONOTONICITY
    for i in range(no):
        # QUANTIZE TO NEAREST OUTPUT LEVEL
        dist = np.abs( freq[i] - lspQ[i,0:levels[i]+1])
        findex[i] = np.argmin( dist )

    return findex

def findex2lsp(findex,lspQ):
    lspq = np.zeros(len(findex))
    for i in range(len(findex)):
        # QUANTIZE TO NEAREST OUTPUT LEVEL
        lspq[i] = lspQ[i,findex[i]];
    return lspq

def main():
    pass

if __name__ == '__main__':
    main()
