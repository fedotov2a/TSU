# -*- coding: utf-8 -*-

def e(x, m, mod=256):
    return (x + m) % mod

def d(x, m, mod=256):
    return (x - m) % mod

def ed(data, key, mod=256):
    res = []
    for i, x in enumerate(data):
        res.append(e(x, ord(key[i % len(key)]), mod))
    return res

def dd(data, key, mod=256):
    res = []
    for i, x in enumerate(data):
        res.append(d(x, ord(key[i % len(key)]), mod))
    return res