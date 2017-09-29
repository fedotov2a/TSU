import sys
sys.path.insert(0, 'lib') # директория lib, где лежат ниже импортируемые файлы

import read_write_file
import caesar
import affine
import detectEnglish
import substitution
import hill
import encryption_modes as em
import spn

def p1():
    # c = [19, 7, 4, 6, 14, 11, 3, 8, 18, 1, 20, 17, 8, 4, 3, 8, 13, 14, 17, 14, 13, 14]
    # print(decrypt_data([[5, 17], [4, 15]], encrypt_data([[5, 17], [4, 15]], c)))
    # print(rev_matrix([[137, 80], [78, 71]], 256))
    print(rev_matrix([[87, 104], [111, 115]], 256))
    # print(mm_mod([[23, 239], [3, 52]], [[76, 15], [163, 201]], 256))
    # print(mm_mod([[137, 78], [80, 71]], [[76, 15], [163, 201]], 256))
    # print(mult_matrix_mod([[89,80], [14, 215]], [23, 239], 256))
    # print(mult_matrix_mod([[89,80], [14, 215]], [3, 52], 256))
    # print(mult_matrix_mod([[175, 251], [75, 214]], [137, 80], 256))

def p2():
    key = [[189, 58], [21, 151]]
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/im3_hill_c_all.bmp')
    decrypt = hill.dd(encrypt_data, key)
    read_write_file.write_data_1byte('decrypt_data/im3_hill_c_all_decrypt.bmp', decrypt)

def p3():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/b4_hill_c_all.png')
    a = [[137, 80], [78, 71]]
    b = encrypt_data[:4]
    inv_a = hill.get_inverse_matrix_mod(a)
    key = [hill.mult_AP_mod(inv_a, [b[0], b[2]]), 
           hill.mult_AP_mod(inv_a, [b[1], b[3]])]
    print(key)
    decrypt_data = hill.dd(encrypt_data, key)
    read_write_file.write_data_1byte('decrypt_data/b4_hill_c_all_decrypt.png', decrypt_data)

def p4():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text2_hill_c_all.txt')
    a = [[ord('W'), ord('h')], [ord('o'), ord('s')]]
    b = encrypt_data[:4]
    inv_a = hill.get_inverse_matrix_mod(a)
    key = [hill.mult_AP_mod(inv_a, [b[0], b[2]]), 
           hill.mult_AP_mod(inv_a, [b[1], b[3]])]
    print(key)
    decrypt_data = hill.dd(encrypt_data, key)
    read_write_file.write_data_1byte('decrypt_data/text2_hill_c_all_decrypt.txt', decrypt_data)

def p5():
    print(affine.get_inverse_mod(550, 1759))
    # .. ??
    
def p6():
    key = 123
    iv = 5
    data = read_write_file.read_data_1byte('data/f3.bmp')
    cbc_e = em.cbc_e(data, key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('encrypt_data/f3_cbc_e.bmp', cbc_e)

    data = read_write_file.read_data_1byte('encrypt_data/f3_cbc_e.bmp')
    cbc_d = em.cbc_d(data, key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('decrypt_data/f3_cbc_d.bmp', cbc_d)

def p6_1():
    key = 123
    iv = 5
    data = read_write_file.read_data_1byte('decrypt_data/f3_cbc_d.bmp')
    ecb_e = em.ecb_e(data[50:], key, crypto_mode='caesar')
    cbc_e = em.cbc_e(data[50:], key, iv, crypto_mode='caesar')

    read_write_file.write_data_1byte('encrypt_data/f3_ecb_e_c_50.bmp', data[:50] + ecb_e)
    read_write_file.write_data_1byte('encrypt_data/f3_cbc_e_c_50.bmp', data[:50] + cbc_e)

def p7():
    key = 56
    iv = 9
    data = read_write_file.read_data_1byte('data/f4.bmp')
    ecb_e = em.ecb_e(data[50:], key, crypto_mode='caesar')
    ofb_e = em.ofb_e(data[50:], key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('encrypt_data/f4_ecb_c_e_50.bmp', data[:50] + ecb_e)
    read_write_file.write_data_1byte('encrypt_data/f4_ofb_c_e_50.bmp', data[:50] + ofb_e)

def p8():
    key = 174
    iv = 9
    data = read_write_file.read_data_1byte('data/f5.bmp')
    cfb_e = em.cfb_e(data, key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('encrypt_data/f5_cfb_c_e.bmp', cfb_e)

    data = read_write_file.read_data_1byte('encrypt_data/f5_cfb_c_e.bmp')
    cfb_d = em.cfb_d(data, key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('decrypt_data/f5_cfb_c_d.bmp', cfb_d)


def p8_1():
    key = 174
    iv = 9
    data = read_write_file.read_data_1byte('data/f5.bmp')
    ecb_e = em.ecb_e(data[50:], key, crypto_mode='caesar')
    ofb_e = em.ofb_e(data[50:], key, iv, crypto_mode='caesar')
    read_write_file.write_data_1byte('encrypt_data/f5_ecb_c_e_50.bmp', data[:50] + ecb_e)
    read_write_file.write_data_1byte('encrypt_data/f5_ofb_c_e_50.bmp', data[:50] + ofb_e)

def p9():
    key = 223
    iv = 78
    data = read_write_file.read_data_1byte('data/f7.bmp')
    ecb_e = em.ecb_e(data[50:], key, crypto_mode='caesar')
    ctr_e = em.ctr_e(data[50:], key, crypto_mode='caesar')
    read_write_file.write_data_1byte('encrypt_data/f7_ecb_c_e_50.bmp', data[:50] + ecb_e)
    read_write_file.write_data_1byte('encrypt_data/f7_ctr_c_e_50.bmp', data[:50] + ctr_e)    

def p10():
    key = 331
    iv = 53
    data = read_write_file.read_data_1byte('data/f6.bmp')

    ecb_e = em.ecb_e(data[50:], key, crypto_mode='caesar')
    cbc_e = em.cbc_e(data[50:], key, iv, crypto_mode='caesar')
    cfb_e = em.cfb_e(data[50:], key, iv, crypto_mode='caesar')
    ofb_e = em.ofb_e(data[50:], key, iv, crypto_mode='caesar')
    ctr_e = em.ctr_e(data[50:], key, crypto_mode='caesar')

    read_write_file.write_data_1byte('encrypt_data/f6_ecb_c_e_50.bmp', data[:50] + ecb_e)
    read_write_file.write_data_1byte('encrypt_data/f6_cbc_c_e_50.bmp', data[:50] + cbc_e)
    read_write_file.write_data_1byte('encrypt_data/f6_cfb_c_e_50.bmp', data[:50] + cfb_e)
    read_write_file.write_data_1byte('encrypt_data/f6_ofb_c_e_50.bmp', data[:50] + ofb_e)
    read_write_file.write_data_1byte('encrypt_data/f6_ctr_c_e_50.bmp', data[:50] + ctr_e)


def p11():
    data = read_write_file.read_data_1byte('encrypt_data/im3_vigener_cbc_c_all.bmp')
    key = 'MODELING'
    iv = 67
    cbc_d = em.cbc_d(data, key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('decrypt_data/im3_vigener_cbc_c_all_decrypt.bmp', cbc_d)

    data = read_write_file.read_data_1byte('decrypt_data/im3_vigener_cbc_c_all_decrypt.bmp')
    cbc_e = em.cbc_e(data[50:], key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('encrypt_data/im3_vigener_cbc_c_all_50.bmp', data[:50] + cbc_e)

def p12():
    data = read_write_file.read_data_1byte('encrypt_data/im4_vigener_ofb_c_all.bmp')
    key = 'MODULATOR'
    iv = 217
    ofb_d = em.ofb_d(data, key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('decrypt_data/im4_vigener_ofb_c_all_decrypt.bmp', ofb_d)
    
    data = read_write_file.read_data_1byte('decrypt_data/im4_vigener_ofb_c_all_decrypt.bmp')
    ofb_e = em.ofb_e(data[50:], key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('encrypt_data/im4_vigener_ofb_c_all_50.bmp', data[:50] + ofb_e)

def p13():
    data = read_write_file.read_data_1byte('encrypt_data/im5_vigener_cfb_c_all.bmp')
    key = 'MONARCH'
    iv = 172
    cfb_d = em.cfb_d(data, key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('decrypt_data/im5_vigener_cfb_c_all_decrypt.bmp', cfb_d)
    
    data = read_write_file.read_data_1byte('decrypt_data/im5_vigener_cfb_c_all_decrypt.bmp')
    cfb_e = em.cfb_e(data[50:], key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('encrypt_data/im5_vigener_cfb_c_all_50.bmp', data[:50] + cfb_e)

def p14():
    data = read_write_file.read_data_1byte('encrypt_data/im6_vigener_ctr_c.bmp')
    key = 'MONOLITH'
    iv = 167
    ctr_d = em.ctr_d(data[50:], key, iv, crypto_mode='vigener') # ?
    read_write_file.write_data_1byte('decrypt_data/im6_vigener_ctr_c_decrypt.bmp', data[:50] + ctr_d)
    
    data = read_write_file.read_data_1byte('decrypt_data/im6_vigener_ctr_c_decrypt.bmp')
    ctr_e = em.ctr_e(data[50:], key, iv, crypto_mode='vigener')
    read_write_file.write_data_1byte('encrypt_data/im6_vigener_ctr_c_50.bmp', data[:50] + ctr_e)

def p15():
    data = read_write_file.read_data_1byte('encrypt_data/im15_affine_cbc_c_all.bmp')
    a = 129
    b = 107
    iv = 243
    key = [a, b]
    cbc_d = em.cbc_d(data, key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('decrypt_data/im15_affine_cbc_c_all_decrypt.bmp', cbc_d)

    data = read_write_file.read_data_1byte('decrypt_data/im15_affine_cbc_c_all_decrypt.bmp')
    cbc_e = em.cbc_e(data[50:], key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('encrypt_data/im15_affine_cbc_c_all_50.bmp', data[:50] + cbc_e)

def p16():
    data = read_write_file.read_data_1byte('encrypt_data/im16_affine_ofb_c_all.bmp')
    a = 233
    b = 216
    iv = 141
    key = [a, b]
    ofb_d = em.ofb_d(data, key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('decrypt_data/im16_affine_ofb_c_all_decrypt.bmp', ofb_d)

    data = read_write_file.read_data_1byte('decrypt_data/im16_affine_ofb_c_all_decrypt.bmp')
    ofb_e = em.ofb_e(data[50:], key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('encrypt_data/im16_affine_ofb_c_all_50.bmp', data[:50] + ofb_e)

def p17():
    data = read_write_file.read_data_1byte('encrypt_data/im17_affine_сfb_c_all.bmp')
    a = 117
    b = 239
    iv = 19
    key = [a, b]
    cfb_d = em.cfb_d(data, key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('decrypt_data/im17_affine_cfb_c_all_decrypt.bmp', cfb_d)

    data = read_write_file.read_data_1byte('decrypt_data/im17_affine_cfb_c_all_decrypt.bmp')
    cfb_e = em.cfb_e(data[50:], key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('encrypt_data/im17_affine_cfb_c_all_50.bmp', data[:50] + cfb_e)

def p18():
    data = read_write_file.read_data_1byte('data/f8.bmp')
    a = 13
    b = 181
    iv = 92
    key = [a, b]
    ctr_e = em.ctr_e(data[50:], key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('encrypt_data/f8_ctr_a_e_50.bmp', data[:50] + ctr_e)

    data = read_write_file.read_data_1byte('encrypt_data/f8_ctr_a_e_50.bmp')
    ctr_d = em.ctr_e(data[50:], key, iv, crypto_mode='affine')
    read_write_file.write_data_1byte('decrypt_data/f8_ctr_a_e_50_decrypt.bmp', data[:50] + ctr_d)

def p19():
    x = int('0010011010110111', 2)
    rounds = 4
    k = int('00111010100101001101011000111111', 2)
    rk = spn.round_keys(k)
    print('k= ', spn.binary(k, 16))
    print('k1= ', spn.binary(rk[0], 4))
    print('k2= ', spn.binary(rk[1], 4))
    print('k3= ', spn.binary(rk[2], 4))
    print('k4= ', spn.binary(rk[3], 4))
    print('k5= ', spn.binary(rk[4], 4))
    y = spn.encrypt(x, rk, rounds)
    print('y= ', spn.binary(y, 4))
    k = int('00111010100101001101011000111111', 2)
    spn.round_keys_to_decrypt(k)

p19()