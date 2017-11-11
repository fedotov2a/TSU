# -*- coding: utf-8 -*-

import numpy as np

def binary(x, k):
    return bin(x)[2:].zfill(k)

def gf_multiply_modular(a, b, mod, n):
    """
    INPUTS
    a - полином (множимое)
    b - полином (множитель)
    mod - неприводимый полином
    n - порядок неприводимого полинома
    OUTPUTS:
    product - результат перемножения двух полиномов a и b
    """
    # маска для наиболее значимого бита в слове
    msb = 2**(n - 1)
    # маска на все биты
    mask = 2**n - 1
    # r(x) = x^n mod m(x)
    r = mod ^ (2**n)
    product = 0 # результат умножения
    mm = 1
    for i in range(n):
        if b & mm > 0:
            # если у множителя текущий бит 1
            product ^= a
        # выполняем последовательное умножение на х
        if a & msb == 0:
            # если старший бит 0, то просто сдвигаем на 1 бит
            a <<= 1
        else:
            # если старший бит 1, то сдвиг на 1 бит
            a <<= 1
            # и сложение по модулю 2 с r(x)
            a ^= r
            # берем только n бит
            a &= mask
        # формируем маску для получения очередного бита в множителе
        mm += mm
    return product

def gf_divide(a, b):
    # деление полинома на полином
    # результат: частное, остаток (полиномы)
    dividend = a # делимое
    divisor = b # делитель
    a = 0
    # бит в делимом
    m = len(bin(dividend))-2
    # бит в делителе
    n = len(bin(divisor))-2
    s = divisor << m
    msb = 2 ** (m + n - 1)
    for i in range(m):
        dividend <<= 1
        if dividend & msb > 0:
            dividend ^= s
            dividend ^= 1
    maskq = 2**m - 1
    maskr = 2**n - 1
    r = (dividend >> m) & maskr
    q = dividend & maskq

    return q, r

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def gf_mi(b, m, n):
    """
    INPUTS
    b (integer)– полином, для которого надо найти обратное по умножению
    m (integer) – неприводимый полином
    n (integer)- порядок неприводимого полинома
    OUTPUTS:
    b2 (integer) – полином, обратный по умножению к b
    """

    # if gcd(b, m) != 1:
    #     return None

    a1, a2, a3 = 1, 0, m
    b1, b2, b3 = 0, 1, b

    while b3 != 1:
        q, r = gf_divide(a3, b3)
        t1, t2, t3 = a1 ^ gf_multiply_modular(q, b1, m, n), a2 ^ gf_multiply_modular(q, b2, m, n), r
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3

    return b2

def divide_into_two(k, n):
    """
    функция разделяет n-битовое число k на два (n/2)-битовых числа
    """
    n2 = n//2
    mask = 2**n2 - 1
    l1 = (k >> n2) & mask
    l2 = k & mask

    return l1, l2

def mux(l, r, n):
    """
    # l, r - n-битовые числа
    # возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
    """
    y = 0
    y ^= r
    y ^= l << n

    return y

class SAes():
    S_Box = np.array([['9', '4', 'a', 'b'], ['d', '1', '8', '5'], ['6', '2', '0', '3'], ['c', 'e', 'f', '7']])
    S_InvBox = np.array([['a', '5', '9', 'b'], ['1', '7', '8', 'f'], ['6', '0', '2', '3'], ['c', '4', 'd', 'e']])
    RCON1 = int('10000000', 2)
    RCON2 = int('00110000', 2)
    modulus = int('10011', 2)
    # column_Matrix = list([['1', '4'], ['4', '1']])
    # column_InvMatrix = list([['9', '2'], ['2', '9']])
    column_Matrix = None
    column_InvMatrix = None
    state_matrix = []
    
    def __init__(self, matrix, mod):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """
        # self.k0 = 0
        # self.k1 = 0
        # self.k2 = 0

        self.column_Matrix = matrix
        self.modulus = mod

        # print(self.column_Matrix)

        # InvMatrix
        n_ = 4
        m00 = int(self.column_Matrix[0][0], 16)
        m01 = int(self.column_Matrix[0][1], 16)
        m10 = int(self.column_Matrix[1][0], 16)
        m11 = int(self.column_Matrix[1][1], 16)
        det = gf_multiply_modular(m00, m11, self.modulus, n_) ^ gf_multiply_modular(m01, m10, self.modulus, n_)
        det_inv = gf_mi(det, self.modulus, n_)

        m00_inv = hex(gf_multiply_modular(m00, det_inv, self.modulus, n_)).split('x')[-1]
        m01_inv = hex(gf_multiply_modular(m01, det_inv, self.modulus, n_)).split('x')[-1]
        m10_inv = hex(gf_multiply_modular(m10, det_inv, self.modulus, n_)).split('x')[-1]
        m11_inv = hex(gf_multiply_modular(m11, det_inv, self.modulus, n_)).split('x')[-1]

        self.column_InvMatrix = list([[m11_inv, m01_inv], [m10_inv, m00_inv]])
        # print(self.column_InvMatrix)

    def sbox(self, v):
        """
        Замена 4-битового значения по таблице S_Box
        """
        r, c = divide_into_two(v, 4)
        rez = self.S_Box[r, c]
        return int(rez, 16)

    def sbox_inv(self, v):
        """
        Замена 4-битового значения по таблице S_InvBox
        """
        r, c = divide_into_two(v, 4)
        rez = self.S_InvBox[r, c]
        return int(rez, 16)

    def g(self, w, i):
        """
        g функция в алгоритме расширения ключа
        """
        n00, n11 = divide_into_two(w, 8)
        n0 = self.sbox(n00)
        n1 = self.sbox(n11)
        n1n0 = mux(n1, n0, 4)
        if i == 1:
            rez = n1n0 ^ self.RCON1
        else:
            rez = n1n0 ^ self.RCON2
        return rez

    def key_expansion(self, key):
        """
        Алгоритм расширения ключа
        """
        w0, w1 = divide_into_two(key, 16)
        w2 = w0 ^ self.g(w1, 1)
        w3 = w1 ^ w2
        w4 = w2 ^ self.g(w3, 2)
        w5 = w3 ^ w4
        return key, mux(w2, w3, 8), mux(w4, w5, 8)

    def to_state_matrix(self, block):
        """
        Формирование матрицы состояния из 16-ти битового числа
        """
        b1, b2   = divide_into_two(block, 16)
        b11, b12 = divide_into_two(b1, 8)
        b21, b22 = divide_into_two(b2, 8)
        self.state_matrix = [[b11, b21], [b12, b22]]

    def add_round_key(self, k):
        """
        Сложение с раундовым ключом (Add round key)
        """
        k1, k2   = divide_into_two(k, 16)
        k11, k12 = divide_into_two(k1, 8)
        k21, k22 = divide_into_two(k2, 8)
        self.state_matrix[0][0] ^= k11
        self.state_matrix[1][0] ^= k12
        self.state_matrix[0][1] ^= k21
        self.state_matrix[1][1] ^= k22

    def nibble_substitution(self):
        """
        Замена элементов матрицы состояния S (Nibble Substitution)
        """
        self.state_matrix[0][0] = self.sbox(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox(self.state_matrix[1][1])

    def nibble_substitution_inv(self):
        """
        Замена элементов матрицы состояния S_inv (Nibble Substitution Inverse)
        """
        self.state_matrix[0][0] = self.sbox_inv(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox_inv(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox_inv(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox_inv(self.state_matrix[1][1])
    
    def shift_row(self):
        """
        Перестановка элементов в матрице состояния S (Shift Row)
        """
        a = self.state_matrix[1][0]
        self.state_matrix[1][0] = self.state_matrix[1][1]
        self.state_matrix[1][1] = a

    def shift_row_inv(self):
        """
        Перестановка элементов в матрице состояния S (Shift Row)
        """
        self.shift_row()
    
    def mix_columns(self):
        """
        Перемешивание элементов в столбцах матрицы S (Mix Columns)
        """
        m00 = int(self.column_Matrix[0][0], 16)
        m01 = int(self.column_Matrix[0][1], 16)
        m10 = int(self.column_Matrix[1][0], 16)
        m11 = int(self.column_Matrix[1][1], 16)
        st00 = self.state_matrix[0][0]
        st10 = self.state_matrix[1][0]
        a = gf_multiply_modular(m00, st00, self.modulus, 4)
        b = gf_multiply_modular(m01, st10, self.modulus, 4)
        c = gf_multiply_modular(m10, st00, self.modulus, 4)
        d = gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][0] = a ^ b
        self.state_matrix[1][0] = c ^ d
        st00 = self.state_matrix[0][1]
        st10 = self.state_matrix[1][1]
        a = gf_multiply_modular(m00, st00, self.modulus, 4)
        b = gf_multiply_modular(m01, st10, self.modulus, 4)
        c = gf_multiply_modular(m10, st00, self.modulus, 4)
        d = gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][1] = a ^ b
        self.state_matrix[1][1] = c ^ d

    def mix_columns_inv(self):
        """
        Перемешивание элементов в столбцах матрицы S (Mix Columns Inv)
        """
        m00 = int(self.column_InvMatrix[0][0], 16)
        m01 = int(self.column_InvMatrix[0][1], 16)
        m10 = int(self.column_InvMatrix[1][0], 16)
        m11 = int(self.column_InvMatrix[1][1], 16)
        st00 = self.state_matrix[0][0]
        st10 = self.state_matrix[1][0]
        a = gf_multiply_modular(m00, st00, self.modulus, 4)
        b = gf_multiply_modular(m01, st10, self.modulus, 4)
        c = gf_multiply_modular(m10, st00, self.modulus, 4)
        d = gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][0] = a ^ b
        self.state_matrix[1][0] = c ^ d
        st00 = self.state_matrix[0][1]
        st10 = self.state_matrix[1][1]
        a = gf_multiply_modular(m00, st00, self.modulus, 4)
        b = gf_multiply_modular(m01, st10, self.modulus, 4)
        c = gf_multiply_modular(m10, st00, self.modulus, 4)
        d = gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][1] = a ^ b
        self.state_matrix[1][1] = c ^ d

    def from_state_matrix(self):
        """
        Формирование 16-ти битового числа из матрицы состояния
        """
        b1 = mux(self.state_matrix[0][0], self.state_matrix[1][0], 4)
        b2 = mux(self.state_matrix[0][1], self.state_matrix[1][1], 4)
        return mux(b1, b2, 8)
    
    def encrypt(self, plaintext, k0, k1, k2):
        """
        Алгоритм шифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(plaintext)
        self.add_round_key(k0)
        self.nibble_substitution()
        self.shift_row()
        self.mix_columns()

        self.add_round_key(k1)
        self.nibble_substitution()
        self.shift_row()

        self.add_round_key(k2)

        ciphertext = self.from_state_matrix()
        return ciphertext

    def decrypt(self, ciphertext, k0, k1, k2):
        """
        Алгоритм расшифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(ciphertext)
        self.add_round_key(k2)
        self.shift_row_inv()
        self.nibble_substitution_inv()
        self.add_round_key(k1)
        
        self.mix_columns_inv()
        self.shift_row_inv()
        self.nibble_substitution_inv()

        self.add_round_key(k0)

        plaintext = self.from_state_matrix()
        return plaintext


    def encrypt_data(self, data, key):
        """
        шифрование 8-битовых чисел в data на ключе key
        """
        k0, k1, k2 = self.key_expansion(key)
        res = []
        for x in data:
            res.append(self.encrypt(x, k0, k1, k2))
        return res


    def decrypt_data(self, data, key):
        """
        шифрование 8-битовых чисел в data на ключе key
        """
        k0, k1, k2 = self.key_expansion(key)
        res = []
        for x in data:
            res.append(self.decrypt(x, k0, k1, k2))
        return res