# -*- coding: utf-8 -*-

def binary(x, k):
    return bin(x)[2:].zfill(k)

class SDes():
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]   
    P8  = [6, 3, 7, 4, 8, 5, 10, 9]
    LS1 = [2, 3, 4, 5, 1]
    LS2 = [3, 4, 5, 1, 2]
    LS3 = [4, 5, 1, 2, 3]
    IP  = [2, 6, 3, 1, 4, 8, 5, 7]
    IPinv = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    SW = [5, 6, 7, 8, 1, 2, 3, 4]

    # таблицы замен
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]

    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]
    
    def __init__(self):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0
    
    @staticmethod
    def pbox(x, p, nx):
        # перестановка бит в nx-битовом числе x по таблице перестановок p
        y = 0
        np = len(p)
        for i in reversed(range(np)):
            if (x & (1 << (nx - 0 - p[i]))) != 0:
                y ^= (1 << (np - 1 - i))
        return y
    
    def p10(self, x):
        return self.pbox(x, self.P10, 10)
    
    def p8(self, x):
        return self.pbox(x, self.P8, 10)
    
    def p4(self, x):
        return self.pbox(x, self.P4, 4)
    
    def ip(self, x):
        return self.pbox(x, self.IP, 8)
    
    def ipinv(self, x):
        return self.pbox(x, self.IPinv, 8)
    
    def ep(self, x):
        return self.pbox(x, self.EP, 4)
    
    def sw(self, x):
        return self.pbox(x, self.SW, 8)
    
    def ls1(self, x):
        return self.pbox(x, self.LS1, 5)
    
    def ls2(self, x):
        return self.pbox(x, self.LS2, 5)

    def ls3(self, x):
        return self.pbox(x, self.LS3, 5)
    
    @staticmethod
    def divide_into_two(k, n):
        """
        функция разделяет n-битовое число k на два (n/2)-битовых числа
        """
        n2 = n//2
        mask = 2**n2 - 1
        l1 = (k >> n2) & mask
        l2 = k & mask

        return l1, l2
    
    @staticmethod
    def mux(l, r, n):
        """
        # l, r - n-битовые числа
        # возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
        """
        y = 0
        y ^= r
        y ^= l << n

        return y
    
    @staticmethod
    def apply_subst(x, s):
        """
        замена по таблице s
        """
        r = 2*(x >> 3) + (x & 1)
        c = 2*((x >> 2) & 1) + ((x >> 1) & 1)

        return s[r][c]
    
    def s0(self, x):
        """
        замена по таблице s0
        """
        return self.apply_subst(x, self.S0)

    def s1(self, x):
        """
        замена по таблице s1
        """
        return self.apply_subst(x, self.S1)

    def key_schedule(self, key):
        """
        Алгоритм расширения ключа. Функция формирует из ключа шифрования key два
        раундовых ключа self.k1, self.k2
        """
        p_10  = self.p10(key)
        ls_1_left = self.ls1(self.divide_into_two(p_10, 10)[0])
        ls_1_right = self.ls1(self.divide_into_two(p_10, 10)[1])
        self.k1 = self.p8(self.mux(ls_1_left, ls_1_right, 5))

        ls_2_left = self.ls2(ls_1_left)
        ls_2_right = self.ls2(ls_1_right)
        self.k2 = self.p8(self.mux(ls_2_left, ls_2_right, 5))

    def key_schedule3(self, key):
        """
        Алгоритм расширения ключа. Функция формирует из ключа шифрования key два
        раундовых ключа self.k1, self.k2
        """
        p_10  = self.p10(key)
        ls_1_left = self.ls1(self.divide_into_two(p_10, 10)[0])
        ls_1_right = self.ls1(self.divide_into_two(p_10, 10)[1])
        self.k1 = self.p8(self.mux(ls_1_left, ls_1_right, 5))

        ls_2_left = self.ls2(ls_1_left)
        ls_2_right = self.ls2(ls_1_right)
        self.k2 = self.p8(self.mux(ls_2_left, ls_2_right, 5))

        ls_3_left = self.ls3(ls_2_left)
        ls_3_right = self.ls3(ls_2_right)
        self.k3 = self.p8(self.mux(ls_3_left, ls_3_right, 5))

    def F(self, block, k):
        """
        Функция выполняет обработку 4-х битового блока данных block
        с использованием раундового подключа k
        """
        e_p = self.ep(block)
        xor = e_p ^ k
        xor_left = self.divide_into_two(xor, 8)[0]
        xor_right = self.divide_into_two(xor, 8)[1]

        s_0 = self.s0(xor_left)
        s_1 = self.s1(xor_right)
        p_4 = self.p4(self.mux(s_0, s_1, 2))

        return p_4

    def f_k(self, block, SK):
        """
        Функция выполняет обработку 8-ми битового блока данных block
        с использованием раундового 8-ми битного подключа SK
        """
        block_left = self.divide_into_two(block, 8)[0]
        block_right = self.divide_into_two(block, 8)[1]
        f = self.F(block_right, SK)
        xor = block_left ^ f
        res = self.mux(xor, block_right, 4)

        return res

    def sdes(self, block, k1, k2):
        """
        Выполняет шифрование 8-ми битового блока данных block
        с раундовыми ключами k1, k2
        """
        block_ip = self.ip(block)
        fk1 = self.f_k(block_ip, k1)
        block_sw = self.sw(fk1); print(binary(block_sw, 8))
        
        fk2 = self.f_k(block_sw, k2)
        res = self.ipinv(fk2); print(binary(res, 8))
        
        return res

    def sdes3(self, block, k1, k2, k3):
        """
        Выполняет шифрование 8-ми битового блока данных block
        с раундовыми ключами k1, k2
        """
        block_ip = self.ip(block)
        fk1 = self.f_k(block_ip, k1)
        block_sw = self.sw(fk1)

        fk2 = self.f_k(block_sw, k2)
        block_sw = self.sw(fk2)

        fk3 = self.f_k(block_sw, k3)
        res = self.ipinv(fk3)
        
        return res

    def encrypt_block(self, plaintext_block):
        return self.sdes(plaintext_block, self.k1, self.k2)

    def decrypt_block(self, ciphertext_block):
        return self.sdes(ciphertext_block, self.k2, self.k1)

    def encrypt_data(self, data):
        res = []
        for x in data:
            res.append(self.encrypt_block(x))
        return res

    def decrypt_data(self, data):
        res = []
        for x in data:
            res.append(self.decrypt_block(x))
        return res