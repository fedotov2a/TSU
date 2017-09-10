import sys
sys.path.insert(0, 'lib') # директория lib, где лежат ниже импортируемые файлы

import read_write_file
import caesar
import affine
import detectEnglish
import substitution

# Цезарь
# шифрование и дешифрование символа и массива символов по известному ключу
def p1():
    m = 24      # сообщение
    key = 37    # ключ
    c = caesar.encrypt(m, key)
    print('c =', c)
    m1 = caesar.decrypt(c, key)
    print('m1 =', m1)
    data = [34, 67, 123, 79, 201]
    encrypt_data = caesar.encrypt_data(data, key)
    print('encrypt_data =', encrypt_data)
    decrypt_data = caesar.decrypt_data(encrypt_data, key)
    print('decrypt_data =', decrypt_data)

# шифрование содержимого текстового файла
def p2():
    data = read_write_file.read_data_1byte('data/f1.txt')
    print('data =', data[:15])
    txt = ''.join([chr(s) for s in data[:15]])
    print('text =', txt)

# шифрование текстового файла по известному ключу
def p3():
    data = read_write_file.read_data_1byte('data/f1.txt')
    encrypt_data = caesar.encrypt_data(data, key=67)
    txt = ''.join([chr(s) for s in encrypt_data])
    read_write_file.write_data_1byte('encrypt_data/f1_encrypt.txt', encrypt_data)

# дешифрование текстовго файла по известному ключу
def p4():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f1_encrypt.txt')
    decrypt_data = caesar.decrypt_data(encrypt_data, key=67)
    txt = ''.join([chr(s) for s in decrypt_data])
    read_write_file.write_data_1byte('decrypt_data/f1_decrypt_know_key.txt', decrypt_data)

# дешифрование текстового файла перебором ключа
def p5():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f1_encrypt.txt')
    
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        txt = ''.join([chr(s) for s in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('key =', k)
            print('decrypt_data =', txt)
            break
    read_write_file.write_data_1byte('decrypt_data/f1_decrypt_unknown_key.txt', decrypt_data)

# шифрование PNG
def p6():
    data = read_write_file.read_data_1byte('data/f2.png')
    encrypt_data = caesar.encrypt_data(data, key=143)
    read_write_file.write_data_1byte('encrypt_data/f2_encrypt.png', encrypt_data)

# дешифрование PNG перебором ключа
# первые два байта PNG - 0x89 и 0x50
def p7():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f2_encrypt.png')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        if decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50:
            print('key =', k)
            break
    read_write_file.write_data_1byte('decrypt_data/f2_decrypt.png', decrypt_data)

# Цезарь
# дешифрование текстового файла перебором ключа
def p8():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/t3_caesar_c_all.txt')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        txt = ''.join([chr(s) for s in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('key =', k)
            print('decrypt_data =', txt)
            read_write_file.write_data_1byte('decrypt_data/t3_caesar_c_all_decrypt.txt', decrypt_data)
            break

# Цезарь
# дешифровка BMP
# первые два байта BMP - 0x42 и 0x4D
def p9():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/c4_caesar_c_all.bmp')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        if decrypt_data[0] == 0x42 and decrypt_data[1] == 0x4d:
            print('key =', k)
            read_write_file.write_data_1byte('decrypt_data/c4_caesar_c_all_decrypt.bmp', decrypt_data)
            break

# зашифровать, оставив первые 50 байт без изменения
def p10():
    data = read_write_file.read_data_1byte('decrypt_data/c4_caesar_c_all_decrypt.bmp')
    encrypt_data = data[:50] + caesar.encrypt_data(data[50:], key=142)
    read_write_file.write_data_1byte('encrypt_data/c4_caesar_c_all_encrypted_50.bmp', encrypt_data)    

# моноалфавитный шифр
def p11():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/c3_subst_c_all.png')
    for k in range(256):
        decrypt_data = substitution.decrypt_data(encrypt_data)
        if decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50:
            print('k =', k)
            break
    read_write_file.write_data_1byte('decrypt_data/c3_subst_c_all_decrypt.png', decrypt_data)

# зашифровать PNG, оставив 350 байт без изменения
def p11_1():
    data = read_write_file.read_data_1byte('decrypt_data/c3_subst_c_all_decrypt.png')
    encrypt_data = data[:350] + substitution.encrypt_data(data[350:])
    read_write_file.write_data_1byte('encrypt_data/c3_subst_c_all_encrypted_350.png', encrypt_data)

# файл ff2_affine_c_all - проблема с ключом
# поэтому свой пример
def p12():
    data = read_write_file.read_data_1byte('data/f3.bmp')
    a = 167
    b = 35
    encrypt_data = affine.encrypt_data(data, a, b)
    read_write_file.write_data_1byte('encrypt_data/f3_affine_encrypt.bmp', encrypt_data)

def p12_1():
    a = 167
    b = 35
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f3_affine_encrypt.bmp')
    decrypt_data = affine.decrypt_data(encrypt_data, a, b)
    read_write_file.write_data_1byte('decrypt_data/f3_affine_decrypt.bmp', decrypt_data)

    encrypt_data = decrypt_data[:50] + affine.encrypt_data(decrypt_data[50:], a, b)
    read_write_file.write_data_1byte('encrypt_data/f3_affine_c_encrypted_50.png', encrypt_data)

def p13():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text10_affine_c_all.txt')
    count_keys = 0
    is_english = False
    for a in range(256):
        if affine.gcd(a, 256) == 1:
            for b in range(256):
                count_keys += 1
                decrypt_data = affine.decrypt_data(encrypt_data[:30], a, b)
                text = ''.join([chr(s) for s in decrypt_data[:30]])
                is_english = detectEnglish.isEnglish(text)
                if is_english:
                    print('k =', count_keys)
                    print('a =', a)
                    print('b =', b)
                    decrypt_data = affine.decrypt_data(encrypt_data, a, b)
                    read_write_file.write_data_1byte('decrypt_data/text10_affine_c_all_decrypt.txt', decrypt_data)
                    break
        if is_english:
            break

def p14():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/b4_affine_c_all.png')
    count_keys = 0
    is_PNG = False
    for a in range(256):
        if affine.gcd(a,256) == 1:
            for b in range(256):
                count_keys += 1
                decrypt_data = affine.decrypt_data(encrypt_data[:2], a, b)
                is_PNG = decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50
                if is_PNG:
                    print('k =', count_keys)
                    print('a =', a)
                    print('b =', b)
                    decrypt_data = affine.decrypt_data(encrypt_data, a, b)
                    read_write_file.write_data_1byte('decrypt_data/b4_affine_c_all_decrypt.png', decrypt_data)
                    break
        if is_PNG:
            break

# шифр Вижинера
def p15():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/im6_vigener_c_all.bmp')
    key = 'magistr'
    decrypt_data = []
    for i in range(len(encrypt_data)):
        m = (encrypt_data[i] - ord(key[i % len(key)])) % 256
        decrypt_data.append(m)
    read_write_file.write_data_1byte('decrypt_data/im6_vigener_decrypt.bmp', decrypt_data)

def p16():
    data = read_write_file.read_data_1byte('decrypt_data/im6_vigener_decrypt.bmp')
    key = 'magistr'
    encrypt_data = []

    for i, d in enumerate(data[50:]):
        encrypt_data.append((d + ord(key[i % len(key)])) % 256)

    read_write_file.write_data_1byte('encrypt_data/im6_vigener_encrypt_50.bmp', data[:50] + encrypt_data)

def p17():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text4_vigener_c_all.txt')
    word = 'housewives'
    for i in range(len(encrypt_data)):
        key = ''
        ww = encrypt_data[i:i+len(word)]
        for j, w in enumerate(ww):
            k = (w - ord(word[j % len(word)])) % 256
            key += chr(k)
        is_english = detectEnglish.isEnglish(key[:3])
        if is_english:
            print(key) # key = student

    key = 'student'
    decrypt_data = []
    for i, e in enumerate(encrypt_data):
        decrypt_data.append((e - ord(key[i % len(key)])) % 256)
    read_write_file.write_data_1byte('decrypt_data/text4_vigener_c_all_decrypt.txt', decrypt_data)

def p18():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text1_vigener_c.txt')
    word = 'it therefore'
    for i in range(len(encrypt_data)):
        key = ''
        ww = encrypt_data[i:i+len(word)]
        for j, w in enumerate(ww):
            k = (w - ord(word[j % len(word)])) % 256
            key += chr(k)
        # print(key)
        is_english = detectEnglish.isEnglish(key[:3])
        if is_english:
            print(key)  # KEYBOARD

    key = 'KEYBOARD'
    decrypt_data = []
    for i, e in enumerate(encrypt_data[48:]):
        decrypt_data.append((e - ord(key[i % len(key)])) % 256)
    read_write_file.write_data_1byte('decrypt_data/text1_vigener_c_all_decrypt.txt', decrypt_data)

def p19():
    import itertools

    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text2_permutation_c.txt')
    template = '123456'
    ew = detectEnglish.ENGLISH_WORDS
    for p in itertools.permutations(template, len(template)):
        perm = ''.join(p)
        decrypt_data = ''
        for i in range(0, 24, len(perm)):
            ww = encrypt_data[i:i+len(perm)]
            for j in range(len(perm)):
                decrypt_data += chr(ww[int(perm[j])-1])
        
        dd_split = decrypt_data.upper().split(' ')
        for d in dd_split:
            if d == '' or d == 'I': continue
            if d not in ew:
                break
        else:
            print('text =', decrypt_data)
            print('permutation =', perm)
            break

def p19_1():
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/text2_permutation_c.txt')
    key = '231465'
    decrypt_data = []
    for i in range(0, len(encrypt_data), len(key)):
        ww = encrypt_data[i:i+len(key)]
        for j in range(len(key)):
            decrypt_data.append(ww[int(key[j]) - 1])
    read_write_file.write_data_1byte('decrypt_data/text2_permutation_c_decrypt.txt', decrypt_data)


p19()