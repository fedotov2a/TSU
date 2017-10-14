import sys
sys.path.insert(0, 'lib') # директория lib, где лежат ниже импортируемые файлы

from sdes import SDes
import read_write_file
import encryption_modes as em
import detectEnglish

def p7():
    sdes = SDes()
    k = int('0111111101', 2)
    data = [234, 54, 135, 98, 47]

    sdes.key_schedule(k)
    print(sdes.encrypt_data(data))

def p8():
    sdes = SDes()
    key = int('0111111101', 2)
    p1 = int('00000000', 2)
    p2 = int('10000000', 2)

    sdes.key_schedule(key)
    sdes.encrypt_block(p1)
    sdes.encrypt_block(p2)

def p9():
    sdes = SDes()
    k1 = int('0111111101', 2)
    k2 = int('0011111101', 2)
    
    p = int('10100100', 2)

    sdes.key_schedule(k1)
    sdes.encrypt_block(p)
    
    sdes.key_schedule(k2)
    sdes.encrypt_block(p)

def p10():
    key = 645
    data = read_write_file.read_data_1byte('encrypt_data/aa1_sdes_c_all.bmp')

    sdes_d = em.ecb_d(data, key, crypto_mode='sdes')
    read_write_file.write_data_1byte('decrypt_data/aa1_sdes_c_all_decrypt.bmp', sdes_d)

    data = read_write_file.read_data_1byte('decrypt_data/aa1_sdes_c_all_decrypt.bmp')
    sdes_e50 = em.ecb_e(data[50:], key, crypto_mode='sdes')
    read_write_file.write_data_1byte('encrypt_data/aa1_sdes_c_all_50.bmp', data[:50] + sdes_e50)

def p11():
    key = 845
    iv = 56
    data = read_write_file.read_data_1byte('encrypt_data/aa2_sdes_c_cbc_all.bmp')

    sdes_d = em.cbc_d(data, key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('decrypt_data/aa2_sdes_c_cbc_all_decrypt.bmp', sdes_d)

    data = read_write_file.read_data_1byte('decrypt_data/aa2_sdes_c_cbc_all_decrypt.bmp')
    sdes_e50 = em.cbc_e(data[50:], key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('encrypt_data/aa2_sdes_c_cbc_all_50.bmp', data[:50] + sdes_e50)

def p12():
    iv = 202
    data = read_write_file.read_data_1byte('encrypt_data/t15_sdes_c_cbc_all.txt')
    k_last8 = int('11101001', 2)

    for p in range(4):
        key = int(bin(p)[2:] + bin(k_last8)[2:], 2)
        sdes_d = em.cbc_d(data, key, iv, crypto_mode='sdes')

        txt = ''.join([chr(s) for s in sdes_d])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('Detect english text with key:', key)
            read_write_file.write_data_1byte('decrypt_data/t15_sdes_c_cbc_all_decrypt.txt', sdes_d)

def p13():
    key = 932
    iv = 234
    data = read_write_file.read_data_1byte('encrypt_data/aa3_sdes_c_ofb_all.bmp')

    sdes_d = em.ofb_d(data, key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('decrypt_data/aa3_sdes_c_ofb_all_decrypt.bmp', sdes_d)

    data = read_write_file.read_data_1byte('decrypt_data/aa3_sdes_c_ofb_all_decrypt.bmp')
    sdes_ecb50 = em.ecb_e(data[50:], key, crypto_mode='sdes')
    sdes_ofb50 = em.ofb_e(data[50:], key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('encrypt_data/aa3_sdes_c_ecb_all_50.bmp', data[:50] + sdes_ecb50)
    read_write_file.write_data_1byte('encrypt_data/aa3_sdes_c_ofb_all_50.bmp', data[:50] + sdes_ofb50)

def p14():
    key = 455
    iv = 162
    data = read_write_file.read_data_1byte('encrypt_data/aa4_sdes_c_cfb_all.bmp')

    sdes_d = em.cfb_d(data, key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('decrypt_data/aa4_sdes_c_cfb_all_decrypt.bmp', sdes_d)

    data = read_write_file.read_data_1byte('decrypt_data/aa4_sdes_c_cfb_all_decrypt.bmp')
    sdes_ecb50 = em.ecb_e(data[50:], key, crypto_mode='sdes')
    sdes_cfb50 = em.cfb_e(data[50:], key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('encrypt_data/aa4_sdes_c_ecb_all_50.bmp', data[:50] + sdes_ecb50)
    read_write_file.write_data_1byte('encrypt_data/aa4_sdes_c_cfb_all_50.bmp', data[:50] + sdes_cfb50)

def p15():
    key = 572
    iv = 157
    data = read_write_file.read_data_1byte('encrypt_data/im38_sdes_c_ctr_all.bmp')

    sdes_d = em.ctr_d(data, key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('decrypt_data/im38_sdes_c_ctr_all_decrypt.bmp', sdes_d)

    data = read_write_file.read_data_1byte('decrypt_data/im38_sdes_c_ctr_all_decrypt.bmp')
    sdes_ecb50 = em.ecb_e(data[50:], key, crypto_mode='sdes')
    sdes_ctr50 = em.ctr_e(data[50:], key, iv, crypto_mode='sdes')
    read_write_file.write_data_1byte('encrypt_data/im38_sdes_c_ecb_all_50.bmp', data[:50] + sdes_ecb50)
    read_write_file.write_data_1byte('encrypt_data/im38_sdes_c_ctr_all_50.bmp', data[:50] + sdes_ctr50)

def p8_3():
    sdes = SDes()
    key = int('0111111101', 2)
    p1 = int('00000000', 2)
    p2 = int('10000000', 2)

    sdes.key_schedule3(key)

    sdes.sdes3(p1, sdes.k1, sdes.k2, sdes.k3)
    sdes.sdes3(p2, sdes.k1, sdes.k2, sdes.k3)

def p9_3():
    sdes = SDes()
    k1 = int('0111111101', 2)
    k2 = int('0011111101', 2)
    
    p = int('10100100', 2)

    sdes.key_schedule3(k1)
    sdes.sdes3(p, sdes.k1, sdes.k2, sdes.k3)
    
    sdes.key_schedule3(k2)
    sdes.sdes3(p, sdes.k1, sdes.k2, sdes.k3)


p9_3()
