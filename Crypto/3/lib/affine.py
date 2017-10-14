# -*- coding: utf-8 -*-

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def get_inverse_mod(a, mod):
    # Returns the modular inverse of a % mod, which is
    # the number x such that a*x % mod = 1

    if gcd(a, mod) != 1:
        return None

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, mod
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % mod

def e(x, a, b, mod=256):
    return (a * x + b) % mod

def d(x, a, b, mod=256):
    return ((x - b) * get_inverse_mod(a, mod)) % mod

def ed(data, a, b, mod=256):
    res = []
    for x in data:
        res.append(e(x, a, b, mod))
    return res
    
def dd(data, a, b, mod=256):
    res = []
    for x in data:
        res.append(d(x, a, b, mod))
    return res