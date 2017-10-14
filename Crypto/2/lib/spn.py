# -*- coding: utf-8 -*-

s = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
p = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

#--------------------------------------------
def binary(x, k):
    y = binary1(x)
    if len(y) < k:
        return '0' * (k-len(y)) + y
    return y

def binary1(x):
    if x != 0:
        y = binary1(x >> 1) + str(x & 1)
        if y == '':
            return '0'
        else:
            return y
    else:
        return ''
#--------------------------------------------

def sbox(x):
    return s[x]

def pbox(x):
    y = 0
    for i in range(len(p)):
        if x & (1 << i) != 0:
            y ^= (1 << p[i])
    return y

def asbox(x):
    return self.s.index(x)

def apbox(self, x):
    y = 0
    for i in range(len(self.p)):
        if (x & (1 << self.p[i])) != 0:
            y ^= (1 << i)
    return y
#--------------------------------------------

def demux(x):
    y = []
    for i in range(4):
        y.append((x >> (i * 4)) & 0xf)
    return y

def mux(x):
    y = 0
    for i in range(4):
        y ^= (x[i] << (i * 4))
    return y

def mix(p, k):
    return p ^ k
#--------------------------------------------

def round_keys(k):
    rk = []
    rk.append((k >> 16) & (2**16 - 1))
    rk.append((k >> 12) & (2**16 - 1))
    rk.append((k >>  8) & (2**16 - 1))
    rk.append((k >>  4) & (2**16 - 1))
    rk.append( k        & (2**16 - 1))
    return rk

def round_keys_to_decrypt(key):
    k = round_keys(key)
    l = []
    l.append(k[-1])
    for i in range(3, 0, -1):
        l.append(apbox(k[i]))
    l.append(k[0])
    return l
#--------------------------------------------

def round(p, k):
    u = mix(p, k)
    v = []
    for x in demux(u):
        v.append(sbox(x))
    w = pbox(mux(v))
    return w

def decrypt_round(p, k):
    u = mix(p, k)
    v = []
    for x in demux(u):
        v.append(asbox(x))
    w = apbox(mux(v))
    return w
#--------------------------------------------

def last_round(p, k1, k2):
    u = mix(p, k1)
    v = []
    for x in demux(u):
        v.append(sbox(x))
    u = mix(mux(v), k2)
    return u

def decrypt_last_round(p, k1, k2):
    u = mix(p, k1)
    v = []
    for x in demux(u):
        v.append(asbox(x))
    u = mix(mux(v), k2)
    return u
#--------------------------------------------

def encrypt(p, rk, rounds):
    x = p
    for i in range(rounds-1):
        x = round(x, rk[i])
    x = last_round(x, rk[rounds-1], rk[rounds])
    return x

def decrypt(p, lk, rounds):
    x = p
    for i in range(rounds-1):
        x = decrypt_round(x, lk[i])
    x = decrypt_last_round(x, lk[rounds-1], lk[rounds])
    return x
#--------------------------------------------

def encrypt_data(data, key, rounds):
    e = []
    rk = round_keys(key)
    for x in data:
        e.append(encrypt(x, rk, rounds))
    return e

def decrypt_data(data, key, rounds):
    d = []
    lk = round_keys_to_decrypt(key)
    for x in data:
        d.append(decrypt(x, lk, rounds))
    return d
