# -*- coding: utf-8 -*-

import caesar
import vigener
import affine
from sdes import SDes
from saes import SAes

def ecb_e(data, key, mod=256, matrix=[], crypto_mode='caesar'):
    if crypto_mode == 'caesar': 
        return caesar.ed(data, key, mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        return sdes.encrypt_data(data)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        return saes.encrypt_data(data, key)

def ecb_d(data, key, mod=256, matrix=[], crypto_mode='caesar'):
    if crypto_mode == 'caesar':
        return caesar.dd(data, key, mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        return sdes.decrypt_data(data)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        return saes.decrypt_data(data, key)

def cbc_e(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    res = []
    a = data[0] ^ iv
    k0 = 0
    k1 = 0
    k2 = 0
    if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(a)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)
        a = saes.encrypt(a, k0, k1, k2)

    res.append(a)
    for i in range(1, len(data)):
        a = data[i] ^ res[i-1]
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        elif crypto_mode == 'saes':    a = saes.encrypt(a, k0, k1, k2) 
        res.append(a)
    return res

def cbc_d(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    res = []
    k0 = 0
    k1 = 0
    k2 = 0
    if   crypto_mode == 'caesar':  a = caesar.d(data[0], key, mod)
    elif crypto_mode == 'vigener': a = vigener.d(data[0], ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.d(data[0], key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.decrypt_block(data[0])
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)
        a = saes.decrypt(data[0], k0, k1, k2)

    a ^= iv
    res.append(a)
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.d(data[i], key, mod)
        elif crypto_mode == 'vigener': a = vigener.d(data[i], ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.d(data[i], key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.decrypt_block(data[i])
        elif crypto_mode == 'saes':    a = saes.decrypt(data[i], k0, k1, k2)
        a ^= data[i-1]
        res.append(a)
    return res

def ofb_e(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)
        a = saes.encrypt(iv, k0, k1, k2)

    res.append(a ^ data[0])
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        elif crypto_mode == 'saes':    a = saes.encrypt(a, k0, k1, k2)
        res.append(a ^ data[i])
    return res

def ofb_d(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    return ofb_e(data, key, iv, mod=mod, matrix=matrix, crypto_mode=crypto_mode)

def cfb_e(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)
        a = saes.encrypt(iv, k0, k1, k2)

    a ^= data[0]
    res.append(a)
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        elif crypto_mode == 'saes':    a = saes.encrypt(a, k0, k1, k2)
        a ^= data[i]
        res.append(a)
    return res

def cfb_d(data, key, iv, mod=256, matrix=[], crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)       # encrypt!
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)
        a = saes.encrypt(iv, k0, k1, k2)

    res.append(a ^ data[0])
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(data[i-1], key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(data[i-1], ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(data[i-1], key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(data[i-1])
        elif crypto_mode == 'saes':    a = saes.encrypt(data[i-1], k0, k1, k2)
        res.append(a ^ data[i])
    return res

def ctr_e(data, key, counter=0, mod=256, matrix=[], crypto_mode='caesar'):
    if crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
    elif crypto_mode == 'saes':
        saes = SAes(matrix, mod)
        k0, k1, k2 = saes.key_expansion(key)

    res = []
    for i, x in enumerate(data):
        if   crypto_mode == 'caesar':  a = caesar.e(counter, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(counter, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(counter, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(counter)
        elif crypto_mode == 'saes':    a = saes.encrypt(counter, k0, k1, k2)
        res.append(a ^ x)
        counter += 1
    return res

def ctr_d(data, key, counter=0, mod=256, matrix=[], crypto_mode='caesar'):
    return ctr_e(data, key, counter=counter, mod=mod, matrix=matrix, crypto_mode=crypto_mode)