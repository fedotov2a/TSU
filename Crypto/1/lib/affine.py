# -*- coding: utf-8 -*-

def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    if gcd(a, m) != 1:
        return None

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def encrypt(m, a, b):
    return (a * m + b) % 256

def decrypt(m, a, b):
    return ((m - b) * findModInverse(a, 256)) % 256

def encrypt_data(data, a, b):
    cypher_data = []
    for m in data:
        cypher_data.append(encrypt(m, a, b))
    return cypher_data
    
def decrypt_data(data, a, b):
    decypher_data = []
    for m in data:
        decypher_data.append(decrypt(m, a, b))
    return decypher_data