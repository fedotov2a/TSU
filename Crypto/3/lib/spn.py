# -*- coding: utf-8 -*-

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


class SPN1:
    # s = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    # p = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    s = [9, 12, 15, 1, 0, 2, 10, 8, 14, 7, 6, 3, 11, 13, 4, 5]
    p = [15, 8, 0, 13, 6, 5, 14, 9, 2, 11, 10, 3, 7, 12, 4, 1]

    def sbox(self, x):
        return self.s[x]

    def pbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if x & (1 << i) != 0:
                y ^= (1 << self.p[i])
        return y

    def asbox(self, x):
        return self.s.index(x)

    def apbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << self.p[i])) != 0:
                y ^= (1 << i)
        return y
    #--------------------------------------------

    def demux(self, x):
        y = []
        for i in range(4):
            y.append((x >> (i * 4)) & 0xf)
        return y

    def mux(self, x):
        y = 0
        for i in range(4):
            y ^= (x[i] << (i * 4))
        return y

    def mix(self, p, k):
        return p ^ k
    #--------------------------------------------

    def round_keys(self, k):
        rk = []
        rk.append((k >> 16) & (2**16 - 1))
        rk.append((k >> 12) & (2**16 - 1))
        rk.append((k >>  8) & (2**16 - 1))
        rk.append((k >>  4) & (2**16 - 1))
        rk.append( k        & (2**16 - 1))
        return rk

    def round_keys_to_decrypt(self, key):
        k = round_keys(key)
        l = []
        l.append(k[-1])
        for i in range(3, 0, -1):
            l.append(apbox(k[i]))
        l.append(k[0])
        return l
    #--------------------------------------------

    def round(self, p, k):
        u = self.mix(p, k)
        v = []
        for x in self.demux(u):
            v.append(self.sbox(x))
        w = self.pbox(self.mux(v))
        return w

    def decrypt_round(self, p, k):
        u = self.mix(p, k)
        v = []
        for x in self.demux(u):
            v.append(self.asbox(x))
        w = self.apbox(self.mux(v))
        return w
    #--------------------------------------------

    def last_round(self, p, k1, k2):
        u = self.mix(p, k1)
        v = []
        for x in self.demux(u):
            v.append(self.sbox(x))
        u = self.mix(self.mux(v), k2)
        return u

    def decrypt_last_round(self, p, k1, k2):
        u = self.mix(p, k1)
        v = []
        for x in self.demux(u):
            v.append(self.asbox(x))
        u = self.mix(self.mux(v), k2)
        return u
    #--------------------------------------------

    def encrypt(self, p, rk, rounds):
        x = p
        for i in range(rounds-1):
            x = self.round(x, rk[i])
        x = self.last_round(x, rk[rounds-1], rk[rounds])
        return x

    def decrypt(self, p, lk, rounds):
        x = p
        for i in range(rounds-1):
            x = self.decrypt_round(x, lk[i])
        x = self.decrypt_last_round(x, lk[rounds-1], lk[rounds])
        return x
    #--------------------------------------------

    def encrypt_data(self, data, key, rounds):
        e = []
        rk = self.round_keys(key)
        for x in data:
            e.append(self.encrypt(x, rk, rounds))
        return e

    def decrypt_data(self, data, key, rounds):
        d = []
        lk = self.round_keys_to_decrypt(key)
        for x in data:
            d.append(self.decrypt(x, lk, rounds))
        return d