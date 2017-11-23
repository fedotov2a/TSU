# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'lib') # директория lib, где лежат ниже импортируемые файлы

from crypto_func import *
import read_write_file

def p1():
    # n = 0
    n = 221
    # while n % 2 == 0:
    #     n = randrange(501, 2002)
    is_prime, p = rabin_miller(n)
    if is_prime:
        print('{} is prime with probability = {}'.format(n, p))
    else:
        print('{} is composite'.format(n))

def p2():
    print(1000000000061, rabin_miller(1000000000061))
    print(1000000000063, rabin_miller(1000000000063))

def p3():
    k = 0
    numbers = [x for x in list(range(13000, 14000)) if x % 2 != 0]
    for x in numbers:
        pr, p = rabin_miller(x)
        if pr:
            k += 1
            print(x)
        if k == 10:
            break

def p4():
    for bit in [41, 53, 120]:
        n = generate_large_prime(bit)
        print('{} = {} содержит {} бит'.format(n, bin(n)[2:], len(bin(n)[2:])))

def p5():
    data = read_write_file.read_data_1byte('name.txt')
    ints = get_blocks_from_data(data, 3)
    print('ints =', ints)
    blocks = get_data_from_blocks(ints, len(data), 3)
    read_write_file.write_data_1byte('res_name.txt', blocks)

def p6(): # ElGamal
    m = 331
    p = 467
    g = 2
    a = 153
    A = pow_(g, a, p)
    print(A)
    c1, c2 = elgamal_encrypt(A, g, p, m)
    print(c1, c2)

    print(elgamal_decrypt(a, p, c1, c2))


    print('-----------')
    p = 2**31 - 1
    g = 7
    pub_key = 833287206
    c1 = 1457850878
    c2 = 2110264777

    print(elgamal_decrypt(pub_key, p, c1, c2))

def p7():
    name = 'Fedotov Alexander Alexandrovich'
    m = get_blocks_from_text(name, len(name))[0]
    keys = generate_keys()
    p, g, y = keys['public_key']
    x       = keys['private_key']

    c1, c2 = elgamal_encrypt(y, g, p, m)
    print('Message:', m)
    print('Public key:')
    print('p =', p)
    print('g =', g)
    print('y =', y)
    print('Private key:\nx =', x)
    print('Cipher:')
    print('c1 =', c1)
    print('c2 =', c2)

    print(elgamal_decrypt(x, p, c1, c2))

p3()


# print(get_blocks_from_text('Hello world!', 12))
# print(get_blocks_from_data([72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33], 12))
# print(get_text_from_blocks([10334410032606748633331426632], 12, 12))
# print(get_data_from_blocks([10334410032606748633331426632], 12, 12))

# print(pow_left_right(125552, 1345543, 13) == pow_right_left(125552, 1345543, 13))
# print('phi(53) = {}\nphi(21) = {}\nphi(159) = {}'.format(euler_func(53), euler_func(21), euler_func(159)))

# import math
# print('x = {} pi(x) = {} x/ln(x) = {}'.format(10**2, pi(10**2), int(10**2  / math.log(10**2)) + 1 ))
# print('x = {} pi(x) = {} x/ln(x) = {}'.format(10**3, pi(10**3), int(10**3  / math.log(10**3)) + 1 ))
# print('x = {} pi(x) = {} x/ln(x) = {}'.format(10**4, pi(10**4), int(10**4  / math.log(10**4)) + 1 ))
# print('x = {} pi(x) = {} x/ln(x) = {}'.format(10**5, pi(10**5), int(10**5  / math.log(10**5)) + 1 ))
