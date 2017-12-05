import random
import time
import read_write_file
import crypto_func as cf
import math

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

def crt(A, m1mk):
    '''
    По китайской теореме об остатках
    Возвращает кортеж А = (a1, a2, ..., an)
    где ai = A mod mi, mi принадлежит m1mk
    '''
    return [A % m for m in m1mk]    # ma

def crt_inv(ma, m1mk):
    '''
    Возвращает число А из Z_MZ, по представлению числа ma
    '''
    M = [m1mk[j] * m1mk[j+1] for j in range(len(m1mk) - 1)][0]
    Mi = [int(M / m) for m in m1mk]
    Mi_inv = [get_inverse_eea(Mi[j], m1mk[j]) for j in range(len(m1mk))]
    c = [Mi[j] * Mi_inv[j] for j in range(len(Mi))]
    A = [(ma[j] * c[j] + ma[j+1] * c[j+1]) % M for j in range(len(c) - 1)][0]

    return int(A)


def pow_(a, x, p):
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

def find_first_primitive_root(p):
    '''
    Возвращает первый первообразный корень
    '''
    if p == 2: return 1

    g = 1
    pd = sieveEratosthen(p-1)
    while True:
        g += 1
        find_g = True
        for pi in pd:
            if (p-1) % pi == 0 and pow_(g, (p-1) // pi, p) == 1:
                find_g = False
                break

        if find_g: break

    return g

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
        a = random.randrange(2, n - 1)
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

def generate_large_prime(bitfield_width):
    '''
    Возвращает простое число, в двоичной СС которой содержится bitfield_width бит
    '''
    candidate = 0
    while True:
        candidate = random.getrandbits(bitfield_width)
        candidate += 1 if not candidate & 1 else 0  # искусственно делаем нечетное число
        candidate |= (1 << bitfield_width - 1)      # два старших
        candidate |= (2 << bitfield_width - 3)      # бита теперь равны 1
        if is_prime(candidate):
            break

    return candidate

def find_p_2q_plus_1(bitfield_width):
    while True:
        p = generate_large_prime(bitfield_width)
        if is_prime((p - 1) // 2):
            return p


def find_g(p):  # p = 2q + 1
    '''
    Возвращает первый первообразный корень версия 2
    '''
    if p == 2: return 1

    p1 = 2
    p2 = (p-1) // 2

    g = 2
    while True:
        if pow_(g, p2, p) != 1 and pow_(g, p1, p) != 1:
            return g
        g += 1


def dlog(g, pub_key, p):
    '''
    Задача дискретного логарифмирования перебором
    g - primitive root
    p - prime
    pub_key = g**private_key mod p
    '''

    y = 0
    while True:
        if pow_(g, y, p) == pub_key:
            return y
        y += 1

def find_p_g(bitfield_width):
    p = find_p_2q_plus_1(bitfield_width)
    g = find_g(p)
    return p, g

def p1():
    '''
    зад 1, 2, 3
    '''

    ma = crt(2345, [89, 97])
    print(ma)

    A = crt_inv(ma, [89, 97])
    print(A)


def p2():
    '''
    зад 4
    '''
    for x in range(1000):
        if x % 5 == 1 and x % 8 == 2 and x % 19 == 3:
            print(x)

def p3():
    '''
    зад 5
    '''
    for x in range(45):
        if x % 5 == 3 and x % 9 == 7:
            print(x)

    x = crt_inv([3, 7], [5, 9])
    print(x)


def p4():
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        print('p = {}, g = {}'.format(p, find_first_primitive_root(p)))

def p5():
    p = find_p_2q_plus_1(12)
    print('p = {}, is prime - {}'.format(p, is_prime((p-1)//2)))

def p6():
    p = find_p_2q_plus_1(12)
    g = find_g(p)
    print(p, g)

def p7():
    t0 = time.clock()
    p = find_p_2q_plus_1(17)
    g = find_g(p)
    t1 = time.clock()
    print('p = {}, g = {}, time = {}'.format(p, g, t1 - t0))


    t0 = time.clock()
    g = find_first_primitive_root(p)
    t1 = time.clock()
    print('p = {}, g = {}, time = {}'.format(p, g, t1 - t0))

def p8():
    pd = sieveEratosthen(100)
    for p in pd:
        if find_first_primitive_root(p) == 2:
            print(p, end=', ')


def p9():
    p, g = find_p_g(16)
    private_key = p - 10
    pub_key = pow_(g, private_key, p)
    print('p = {}, g = {}, pub_key = {}, private_key = {}'.format(p, g, pub_key, private_key))
    t0 = time.clock()
    private_key = dlog(g, pub_key, p)
    t1 = time.clock()
    dt = t1 - t0
    print('find private_key = {}, time = {}'.format(private_key, dt))

def p10():
    import matplotlib.pyplot as plt

    bitgr = []
    timegr = []
    for bit in range(10, 23):
        p, g = find_p_g(bit)
        private_key = p - 3
        pub_key = pow_(g, private_key, p)
        print('p = {}, g = {}, pub_key = {}, private_key = {}'.format(p, g, pub_key, private_key))
        t0 = time.clock()
        private_key = dlog(g, private_key, p)
        t1 = time.clock()

        bitgr.append(bit)
        timegr.append(t1 - t0)
        print(bit, t1 - t0)

    plt.plot(bitgr, timegr)
    plt.show()

def p11():
    print(dlog(3, 1, 13))

def p12():
    data = read_write_file.read_data_1byte('fio.txt')
    nums = cf.get_blocks_from_data(data, 3)
    m = max(nums)
    bitfield_width = math.floor(math.log2(m)) + 2

    p, g = find_p_g(bitfield_width)
    private_key = 1994
    pub_key = pow_(g, private_key, p)

    encrypt_nums = []
    for n in nums:
        c1, c2 = cf.elgamal_encrypt(pub_key, g, p, n)
        encrypt_nums.append(c1)
        encrypt_nums.append(c2)

    read_write_file.write_numbers('encrypt_file.txt', encrypt_nums)

    encrypt_nums = read_write_file.read_numbers('encrypt_file.txt')

    decrypt_nums = []
    for i in range(0, len(encrypt_nums) - 1, 2):
        c1 = encrypt_nums[i]
        c2 = encrypt_nums[i+1]

        decrypt_nums.append(cf.elgamal_decrypt(private_key, p, c1, c2))

    decrypt_data = cf.get_data_from_blocks(decrypt_nums, len(data), 3)
    print(decrypt_data)

    read_write_file.write_data_1byte('fio1.txt', decrypt_data)


def p13():
    data = read_write_file.read_numbers('b4_ElG_c.png')
    p = 9887455967
    g = 5
    pub_key = 3359661584
    private_key = 543
    block_size = 4

    d_nums = []

    for i in range(0, len(data) - 1, 2):
        c1 = data[i]
        c2 = data[i+1]

        d_nums.append(cf.elgamal_decrypt(private_key, p, c1, c2))

    d_data = cf.get_data_from_blocks(d_nums, 24776, block_size)
    read_write_file.write_data_1byte('b4_d.png', d_data)


def rsa_encrypt(m, pub_key, n):
    return pow_(m, pub_key, n)

def rsa_decrypt(c, priv_key, n):
    return pow_(c, priv_key, n)

def p14():
    data = read_write_file.read_data_1byte('fio.txt')
    nums = cf.get_blocks_from_data(data, 3)
    m = max(nums)
    bitfield_width = math.floor(math.log2(m)) + 2

    p = find_p_2q_plus_1(bitfield_width)
    q = find_p_2q_plus_1(bitfield_width)
    n = p * q

    e = find_p_2q_plus_1(bitfield_width)
    while q % e == 1 and p % e == 1:
        e = find_p_2q_plus_1(bitfield_width)

    fi_n = (p - 1) * (q - 1)
    priv_key = get_inverse_eea(e, fi_n)

    ed = []
    for d in nums:
        ed.append(rsa_encrypt(d, e, n))

    read_write_file.write_numbers('fio_e.txt', ed)

    data_e = read_write_file.read_numbers('fio_e.txt')
    dd = []
    for c in data_e:
        dd.append(rsa_decrypt(c, priv_key, n))

    dd = cf.get_data_from_blocks(dd, len(data), 3)
    read_write_file.write_data_1byte('fio_d.txt', dd)


def p15():
    data = read_write_file.read_numbers('im49_rsa_c.png')
    p = 7919
    q = 6599
    pub_key = 2011
    priv_key = 17457619
    len_data = 37451
    block_size = 3

    d_nums = []

    for d in data:
        d_nums.append(rsa_decrypt(d, priv_key, p * q))

    d_data = cf.get_data_from_blocks(d_nums, len_data, block_size)
    read_write_file.write_data_1byte('im49_rsa_c_decrypt.png', d_data)



def get_text_from_blocks26(block_ints, message_length, block_size):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                ascii_number = block_int // (26 ** i)
                block_int %= 26 ** i
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return ''.join(message)


def num_to_str(num):
    s = []
    while num != 0:
        letter = chr(num % 26 + ord('A'))
        s.insert(0, letter)
        num = num // 26
    return ''.join(s)

def p16():
    n = 18923
    e = 1261

    p = 127
    q = 149

    fi_n = (p - 1) * (q - 1)
    priv_key = get_inverse_eea(e, fi_n)

    cipher = [12423, 11524, 7243, 7459, 14303, 6127, 10964, 16399,
            9792, 13629, 14407, 18817, 18830, 13556, 3159, 16647,
            5300, 13951, 81, 8986, 8007, 13167, 10022, 17213,
            2264, 961, 17459, 4101, 2999, 14569, 17183, 15827,
            12693, 9553, 18194, 3830, 2664, 13998, 12501, 18873,
            12161, 13071, 16900, 7233, 8270, 17086, 9792, 14266,
            13236, 5300, 13951, 8850, 12129, 6091, 18110, 3332,
            15061, 12347, 7817, 7946, 11675, 13924, 13892, 18031,
            2620, 6276, 8500, 201, 8850, 11178, 16477, 10161,
            3533, 13842, 7537, 12259, 18110, 44, 2364, 15570,
            3460, 9886, 8687, 4481, 11231, 7547, 11383, 17910,
            12867, 13203, 5102, 4742, 5053, 15407, 2976, 9330,
            12192, 56, 2471, 15334, 841, 13995, 17592, 13297,
            2430, 9741, 11675, 424, 6686, 738, 13874, 8168,
            7913, 6246, 14301, 1144, 9056, 15967, 7328, 13203,
            796, 195, 9872, 16979, 15404, 14130, 9105, 2001,
            9792, 14251, 1498, 11296, 1105, 4502, 16979, 1105,
            56, 4118, 11302, 5988, 3363, 15827, 6928, 4191,
            4277, 10617, 874, 13211, 11821, 3090, 18110, 44,
            2364, 15570, 3460, 9886, 9988, 3798, 1158, 9872,
            16979, 15404, 6127, 9872, 3652, 14838, 7437, 2540,
            1367, 2512, 14407, 5053, 1521, 297, 10935, 17137,
            2186, 9433, 13293, 7555, 13618, 13000, 6490, 5310,
            18676, 4782, 11374, 446, 4165, 11634, 3846, 14611,
            2364, 6789, 11634, 4493, 4063, 4576, 17955, 7965,
            11748, 14616, 11453, 17666, 925, 56, 4118, 18031,
            9522, 14838, 7437, 3880, 11476, 8305, 5102, 2999,
            18628, 14326, 9175, 9061, 650, 18110, 8720, 15404,
            2951, 722, 15334, 841, 15610, 2443, 11056, 2186]

    decrypt_nums = [rsa_decrypt(c, priv_key, n) for c in cipher]

    dtext = ''
    for x in decrypt_nums:
        dtext += num_to_str(x)
   
    print(dtext)

p13()