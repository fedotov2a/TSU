# -*- coding: utf-8 -*-

from random import randrange, randint, getrandbits

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def get_inverse_eea(a, mod):
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

#-----------------------------------------------------------------------------------------------
def euler_func(n):
    ''' 
    Функция Эйлера.
    Возвращает количество чисел в ряду 1, 2, 3, ..., n-1, взаимно простых с n
    Если n - простое, то count = n-1
    '''
    count = 1
    for x in range(2, n):
        count += 1 if gcd(x, n) == 1 else 0
    return count

def group_order(n):
    '''
    Порядок группы = |G|, |G| - количество элементов
    Утв. Z/nZ = euler_func(n)
    '''
    return euler_func(n)

def z_nz_group(n):
    '''
    Множество классов вычетов по модулю n
    '''
    res = []
    for x in range(1, n):
        if gcd(x, n) == 1:
            res.append(x)
    return res

def cyclic_group(n):
    '''
    Проверяет цикличная ли группа
    '''
    z_nz = z_nz_group(n)
    for x in z_nz:
        gr = []
        for i in range(len(z_nz)):
            gr.append(x**i % n)

        gr.sort()

        if gr == z_nz:
            return x

    return None

#-----------------------------------------------------------------------------------------------
def pow_right_left(a, x, p):
    '''
    Возведение в степень справа-налево
    Вход: a, x, p - целые числа
    Выход: y = a**x mod p
    '''
    y = 1
    s = a
    xb = bin(x)[2:]
    for i in range(len(xb)-1, -1, -1):
        if int(xb[i]) == 1:
            y = (y * s) % p
        s = (s**2) % p
    return y

def pow_left_right(a, x, p):
    '''
    Возведение в степень слева-направо
    Вход: a, x, p - целые числа
    Выход: y = a**x mod p
    '''
    y = 1
    xb = bin(x)[2:]
    for i in range(len(xb)):
        y = (y**2) % p
        if int(xb[i]) == 1:
            y = (y * a) % p
    return y

def pow_(a, x, p):
    '''
    Возведение в степень ???
    Вход: a, x, p - целые числа
    Выход: y = a**x mod p
    '''
    y = 1
    xb = bin(x)[2:]
    for i in range(len(xb)):
        y = (y**2) % p
        if int(xb[i]) == 1:
            y = (y * a) % p
    return y

#-----------------------------------------------------------------------------------------------
def multiplicative_order(g, n):
    '''
    Порядок числа g в группе G по модулю n - это такое число,
    что g**m = 1(mod n), m >= 1
    '''
    m = 1
    while pow_(g, m, n) != 1:
        m += 1
    return m

def primitive_roots(n):
    '''
    Возвращает первообразные корни.
    Если порядок элемента g равен euler_func(n), то g - первообразный корень по модулю n
    '''
    primitive_roots = []
    z_nz = z_nz_group(n)
    for g in z_nz:
        is_primitive_root = multiplicative_order(g, n) == euler_func(n)
        if is_primitive_root:
            primitive_roots.append(g)
    return primitive_roots

#-----------------------------------------------------------------------------------------------
def sieveEratosthen(n):
    '''
    Решето Эратосфена
    '''
    numbers = list(range(2, n + 1))
    for number in numbers:
        if number > (n + 1)**(1 / 2):
            break
        if number != 0:
            for c in range(2 * number, n + 1, number):
                numbers[c - 2] = 0
    return [x for x in numbers if x != 0]

#-----------------------------------------------------------------------------------------------
def rabin_miller(n):
    # n - нечетное
    # Returns True if num is a prime number.
    q = n - 1
    k = 0
    while q % 2 == 0:
        # keep halving s until it is even (and use t
        # to count how many times we halve s)
        q = q // 2
        k += 1

    t = 5
    for trials in range(t):  # try to falsify num's primality 5 times
        a = randrange(2, n - 1)
        v = pow_(a, q, n)
        # print('trials = {}, a = {}, v = {}'.format(trials, a, v))
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != n - 1:
                if i == k - 1:
                    return False, 0
                else:
                    i += 1
                    v = (v**2) % n
    probability_of_prime = 1 - 1.0 / (4**t)
    return True, probability_of_prime

def is_prime(n):
    # Return True if n is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().
    if n < 2:
        return False   # 0, 1, and negative numbers are not prime
    # About 1/3 of the time we can quickly determine if n is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabin_miller().
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 
                  41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 
                  89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
                  139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 
                  193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 
                  251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 
                  311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 
                  373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 
                  433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 
                  491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 
                  569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 
                  619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 
                  683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 
                  757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 
                  827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 
                  887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 
                  971, 977, 983, 991, 997]
    if n in low_primes:
        return True
    # See if any of the low prime numbers can divide n
    for prime in low_primes:
        if n % prime == 0:
            return False
    # If all else fails, call rabin_miller() to determine if n is a prime.
    return rabin_miller(n)[0]

#-----------------------------------------------------------------------------------------------
def pi(x):
    '''
    Возвращает количество простых чисел меньших x
    '''
    numbers = [2] + [x for x in list(range(3, x)) if x % 2 != 0]
    count = 0
    for x in numbers:
        if is_prime(x):
            count += 1
    return count

#-----------------------------------------------------------------------------------------------
def get_blocks_from_text(message, block_size):
    '''
    Converts a string message to a list of block integers. Each integer
    represents block_size string characters.
    '''
    message_bytes = message.encode('ascii')  # convert the string to bytes

    block_ints = []
    for blockStart in range(0, len(message_bytes), block_size):
        # Calculate the block integer for this block of text
        block_int = 0

        for i in range(blockStart, min(blockStart + block_size, len(message_bytes))):
            block_int += message_bytes[i] * (256 ** (i % block_size))
        block_ints.append(block_int)
    return block_ints

def get_blocks_from_data(data, block_size):
    block_ints = []
    for blockStart in range(0, len(data), block_size):
        block_int = 0
        for i in range(blockStart, min(blockStart + block_size, len(data))):
            block_int += data[i] * (256 ** (i % block_size))
        block_ints.append(block_int)
    return block_ints

def get_text_from_blocks(block_ints, message_length, block_size):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                ascii_number = block_int // (256 ** i)
                block_int %= 256 ** i
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return ''.join(message)

def get_data_from_blocks(block_ints, message_length, block_size):
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                ascii_number = block_int // (256 ** i)
                block_int %= 256 ** i
                block_message.insert(0, ascii_number)
        message.extend(block_message)
    return message

#-----------------------------------------------------------------------------------------------
def generate_large_prime(bitfield_width):
    '''
    Возвращает простое число, в двоичной СС которой содержится bitfield_width бит
    '''
    candidate = 0
    while True:
        candidate = getrandbits(bitfield_width)
        candidate += 1 if not candidate & 1 else 0  # искусственно делаем нечетное число
        candidate |= (1 << bitfield_width - 1)      # два старших
        candidate |= (2 << bitfield_width - 3)      # бита теперь равны 1
        if is_prime(candidate):
            break

    return candidate

# http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
# faster than primitive_roots(n)
def get_primitive_root(p):
    if p == 2: return 1

    p1 = 2
    p2 = (p-1) // p1

    #test random g's until one is found that is a primitive root mod p
    while True:
        g = randint(2, p-1)
        #g is a primitive root if for all prime factors of p-1, p[i]
        if pow_(g, (p-1) // p1, p) != 1 and pow_(g, (p-1) // p2, p) != 1:
            return g

def get_inverse_ltf(a, p):
    '''
    Обратное значение по умножению, используя малую Теорему Ферма, если p - простое
    '''
    return pow_(a, p-2, p)

#-----------------------------------------------------------------------------------------------
def generate_keys(bitfield_width=256):
    p = generate_large_prime(bitfield_width)    # большое простое число
    g = get_primitive_root(p)                   # первообразный корень
    x = randint(2, p)                           # закрытый ключ 1 < x < p
    y = pow_(g, x, p)                           # открытый ключ

    return {'public_key': (p, g, y), 'private_key': x}

def elgamal_encrypt(y, g, p, m):
    '''
    y = public key
    g = generator
    p = prime
    message = number < p
    '''
    k = randint(2, p-1)
    c1 = pow_(g, k, p)
    c2 = (m * pow_(y, k, p)) % p

    return c1, c2

def elgamal_decrypt(x, p, c1, c2):
    '''
    x = private key
    p = prime
    (с1 ,с2) = ciphertext
    '''
    return (get_inverse_ltf(pow_(c1, x, p), p) * c2) % p

#-----------------------------------------------------------------------------------------------