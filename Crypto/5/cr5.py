import sys
sys.path.insert(0, 'lib') # директория lib, где лежат ниже импортируемые файлы

import saes
import read_write_file
import encryption_modes as em
import detectEnglish

def p1():
    m = int('10011', 2)
    f = int('1011', 2)
    g = int('0111', 2)

    product = saes.gf_multiply_modular(f, g, m, n=4)
    print('f*g = {}'.format(saes.binary(product, 4)))

def p2():
    a = int('1011', 2)
    b = int('0011', 2)
    q, r = saes.gf_divide(a, b)
    print('q = {}, r = {}'.format(saes.binary(q, 4), saes.binary(r, 4)))

def p3():
    n = 4
    a = 3
    m = int('10011', 2)
    inv_a = saes.gf_mi(a, m, n)
    print('a = {}'.format(saes.binary(a, n)))
    print('inv_a = {}'.format(saes.binary(inv_a, n)))
    product = saes.gf_multiply_modular(a, inv_a, m, n)
    print('a * inv_a = {}'.format(saes.binary(product, n)))

def p4():
    matrix = list([['1', '4'], ['4', '1']])
    mod = int('10011', 2)
    k = int('1010011100111011', 2)
    p = int('0110111101101011', 2)

    s = saes.SAes(matrix, mod)
    k0, k1, k2 = s.key_expansion(k)

    print('k0: {} k1: {} k2: {}'.format(saes.binary(k0, 16), saes.binary(k1, 16), saes.binary(k2, 16)))
    
    s.encrypt(p, k0, k1, k2)
    print(s.state_matrix) 

def p5():
    matrix = list([['1', '4'], ['4', '1']])
    mod = int('10011', 2)
    key = 834

    data = read_write_file.read_data_2byte('encrypt_data/dd1_saes_c_all.bmp')

    saes_d = em.ecb_d(data, key, mod=mod, matrix=matrix, crypto_mode='saes')
    print(saes_d[:4])
    read_write_file.write_data_2byte('decrypt_data/dd1_saes_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/dd1_saes_c_all_decrypt.bmp')
    saes_ecb50 = em.ecb_e(data[50:], key, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/dd1_saes_c_all_50.bmp', data[:50] + saes_ecb50)


def p6():
    matrix = list([['b', '4'], ['e', 'd']])
    mod = int('10011', 2)
    key = 2318

    data = read_write_file.read_data_2byte('encrypt_data/im43_saes_c_all.bmp')

    saes_d = em.ecb_d(data, key, mod=mod, matrix=matrix, crypto_mode='saes')
    print(saes_d[:4])
    read_write_file.write_data_2byte('decrypt_data/im43_saes_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/im43_saes_c_all_decrypt.bmp')
    saes_ecb50 = em.ecb_e(data[50:], key, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/im43_saes_c_all_50.bmp', data[:50] + saes_ecb50)

def p7():
    matrix = list([['a', 'c'], ['8', '6']])
    mod = int('11001', 2)
    key = 1021
    iv = 456

    data = read_write_file.read_data_2byte('encrypt_data/dd5_saes_cbc_c_all.bmp')

    saes_d = em.cbc_d(data, key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('decrypt_data/dd5_saes_cbc_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/dd5_saes_cbc_c_all_decrypt.bmp')
    saes_cbc50 = em.cbc_e(data[50:], key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/dd5_saes_cbc_c_all_50.bmp', data[:50] + saes_cbc50)

def p8():
    matrix = list([['5', '3'], ['2', 'c']])
    mod = int('11001', 2)
    key = 12345
    iv = 5171

    data = read_write_file.read_data_2byte('encrypt_data/dd8_saes_ofb_c_all.bmp')

    saes_d = em.ofb_d(data, key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('decrypt_data/dd8_saes_ofb_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/dd8_saes_ofb_c_all_decrypt.bmp')
    saes_ofb50 = em.ofb_e(data[50:], key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/dd8_saes_ofb_c_all_50.bmp', data[:50] + saes_ofb50)

def p9():
    matrix = list([['3', '8'], ['2', 'b']])
    mod = int('10011', 2)
    tail_key = '011101001'
    # key = 14569
    iv = 3523

    data0 = read_write_file.read_data_2byte('data/t0.txt')
    print(max(data0))
    # saes_e = em.ofb_e(data, key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    # read_write_file.write_data_2byte('encrypt_data/t0_e_ofb.txt', saes_e)

    data = read_write_file.read_data_2byte('encrypt_data/t0_e_ofb.txt')
    
    for head_key in range(2**7):
        key = int(bin(head_key)[2:] + tail_key, 2)
        if key == 14569:
            print(key)
        saes_d = em.ofb_d(data, key, iv, mod=mod, matrix=matrix, crypto_mode='saes')

        saes_d2 = []
        for i in range(0, len(saes_d), 2):
            saes_d2.append(saes_d[i] >> 8)
            saes_d2.append(saes_d[i] & 127)

        txt = ''.join([chr(s) for s in saes_d2])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('Detect english text with key:', key)
            read_write_file.write_data_2byte('decrypt_data/t20_saes_ofb_c_all_decrypt.txt', saes_d)
            break

def p10():
    matrix = list([['7', 'd'], ['4', '5']])
    mod = int('11001', 2)
    key = 24545
    iv = 9165

    data = read_write_file.read_data_2byte('encrypt_data/dd10_saes_cfb_c_all.bmp')

    saes_d = em.cfb_d(data, key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('decrypt_data/dd10_saes_cfb_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/dd10_saes_cfb_c_all_decrypt.bmp')
    saes_cfb50 = em.cfb_e(data[50:], key, iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/dd10_saes_cfb_c_all_50.bmp', data[:50] + saes_cfb50)

def p11():
    matrix = list([['7', '3'], ['2', 'e']])
    mod = int('10011', 2)
    key = 2645
    iv = 23184

    data = read_write_file.read_data_2byte('encrypt_data/dd12_saes_ctr_c_all.bmp')

    saes_d = em.ctr_d(data, key, counter=iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('decrypt_data/dd12_saes_ctr_c_all_decrypt.bmp', saes_d)

    data = read_write_file.read_data_2byte('decrypt_data/dd12_saes_ctr_c_all_decrypt.bmp')
    saes_ctr50 = em.ctr_e(data[50:], key, counter=iv, mod=mod, matrix=matrix, crypto_mode='saes')
    read_write_file.write_data_2byte('encrypt_data/dd12_saes_ctr_c_all_50.bmp', data[:50] + saes_ctr50)



p9()



# Посмотреть про AES полная история, эксплуатация и т.д
# как он стал стд, попытки взлома