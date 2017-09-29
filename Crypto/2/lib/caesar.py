# -*- coding: utf-8 -*-

def e(x, key, mod=256):
	return (x + key) % mod

def d(x, key, mod=256):
	return (x - key) % mod

def ed(data, key, mod=256):
	res = []
	for x in data:
		res.append(e(x, key, mod))
	return res

def dd(data, key, mod=256):
	res = []
	for x in data:
		res.append(d(x, key, mod))
	return res