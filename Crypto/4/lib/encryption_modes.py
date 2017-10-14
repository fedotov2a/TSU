# -*- coding: utf-8 -*-

import caesar
import vigener
import affine
from sdes import SDes
def ecb_e(data, key, mod=256, crypto_mode='caesar'):
    if crypto_mode == 'caesar': 
        return caesar.ed(data, key, mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        return sdes.encrypt_data(data)

def ecb_d(data, key, mod=256, crypto_mode='caesar'):
    if crypto_mode == 'caesar':
        return caesar.dd(data, key, mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        return sdes.decrypt_data(data)

def cbc_e(data, key, iv, mod=256, crypto_mode='caesar'):
    res = []
    a = data[0] ^ iv
    if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(a)
    res.append(a)
    for i in range(1, len(data)):
        a = data[i] ^ res[i-1]
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        res.append(a)
    return res

def cbc_d(data, key, iv, mod=256, crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.d(data[0], key, mod)
    elif crypto_mode == 'vigener': a = vigener.d(data[0], ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.d(data[0], key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.decrypt_block(data[0])
    a ^= iv
    res.append(a)
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.d(data[i], key, mod)
        elif crypto_mode == 'vigener': a = vigener.d(data[i], ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.d(data[i], key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.decrypt_block(data[i])
        a ^= data[i-1]
        res.append(a)
    return res

def ofb_e(data, key, iv, mod=256, crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    res.append(a ^ data[0])
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        res.append(a ^ data[i])
    return res

def ofb_d(data, key, iv, mod=256, crypto_mode='caesar'):
    return ofb_e(data, key, iv, mod=mod, crypto_mode=crypto_mode)

def cfb_e(data, key, iv, mod=256, crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    a ^= data[0]
    res.append(a)
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(a, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(a, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(a, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(a)
        a ^= data[i]
        res.append(a)
    return res

def cfb_d(data, key, iv, mod=256, crypto_mode='caesar'):
    res = []
    if   crypto_mode == 'caesar':  a = caesar.e(iv, key, mod)       # encrypt!
    elif crypto_mode == 'vigener': a = vigener.e(iv, ord(key[0]), mod)
    elif crypto_mode == 'affine':  a = affine.e(iv, key[0], key[1], mod)
    elif crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)
        a = sdes.encrypt_block(iv)
    res.append(a ^ data[0])
    for i in range(1, len(data)):
        if   crypto_mode == 'caesar':  a = caesar.e(data[i-1], key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(data[i-1], ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(data[i-1], key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(data[i-1])
        res.append(a ^ data[i])
    return res

def ctr_e(data, key, counter=0, mod=256, crypto_mode='caesar'):
    if crypto_mode == 'sdes':
        sdes = SDes()
        sdes.key_schedule(key)

    res = []
    for i, x in enumerate(data):
        if   crypto_mode == 'caesar':  a = caesar.e(counter, key, mod)
        elif crypto_mode == 'vigener': a = vigener.e(counter, ord(key[i % len(key)]), mod)
        elif crypto_mode == 'affine':  a = affine.e(counter, key[0], key[1], mod)
        elif crypto_mode == 'sdes':    a = sdes.encrypt_block(counter)
        res.append(a ^ x)
        counter += 1
    return res

def ctr_d(data, key, counter=0, mod=256, crypto_mode='caesar'):
    return ctr_e(data, key, counter=counter, mod=mod, crypto_mode=crypto_mode)