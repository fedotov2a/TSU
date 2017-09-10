import caesar
import read_write_file
import detectEnglish

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
    data = read_write_file.read_data_1byte('f1.txt')
    print('data =', data[:15])
    txt = ''.join([chr(s) for s in data[:15]])
    print('text =', txt)

# шифрование текстового файла по известному ключу
def p3():
    data = read_write_file.read_data_1byte('f1.txt')
    print('data =', data[:15])

    encrypt_data = caesar.encrypt_data(data, key=67)
    print('encrypt_data =', encrypt_data[:15])

    txt = ''.join([chr(s) for s in encrypt_data[:15]])
    print('encrypt_text =', txt)

    read_write_file.write_data_1byte('f1_encrypt.txt', encrypt_data)

# дешифрование текстовго файла по известному ключу
def p4():
    encrypt_data = read_write_file.read_data_1byte('f1_encrypt.txt')
    print('encrypt_data =', encrypt_data[:15])

    decrypt_data = caesar.decrypt_data(encrypt_data, key=67)
    print('decrypt_data =', decrypt_data[:15])

    txt = ''.join([chr(s) for s in decrypt_data[:15]])
    print('decrypt_data =', txt)

    read_write_file.write_data_1byte('f1_decrypt.txt', decrypt_data)

# дешифрование текстового файла перебором ключа
def p5():
    encrypt_data = read_write_file.read_data_1byte('f1_encrypt.txt')
    
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data[:15], key=k)
        txt = ''.join([chr(s) for s in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('key =', k)
            print('decrypt_data =', txt)
            break

# шифрование PNG
def p6():
    data = read_write_file.read_data_1byte('f2.png')
    encrypt_data = caesar.encrypt_data(data, key=143)
    read_write_file.write_data_1byte('f2_encrypt.png', encrypt_data)

# дешифрование PNG перебором ключа
# первые два байта PNG - 0x89 и 0x50
def p7():
    encrypt_data = read_write_file.read_data_1byte('f2_encrypt.png')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        if decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50:
            print('key =', k)
            print('decrypt_data =', decrypt_data[:10])
            read_write_file.write_data_1byte('f2_decrypt.png', decrypt_data)
            break

# Цезарь
# дешифрование текстового файла перебором ключа
def p8():
    encrypt_data = read_write_file.read_data_1byte('t3_caesar_c_all.txt')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        txt = ''.join([chr(s) for s in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            print('key =', k)
            print('decrypt_data =', txt)
            read_write_file.write_data_1byte('t3_caesar_c_all_decrypt.txt', decrypt_data)
            break

# Цезарь
# дешифровка BMP
# первые два байта BMP - 0x42 и 0x4D
def p9():
    encrypt_data = read_write_file.read_data_1byte('c4_caesar_c_all.bmp')
    for k in range(256):
        decrypt_data = caesar.decrypt_data(encrypt_data, key=k)
        if decrypt_data[0] == 0x42 and decrypt_data[1] == 0x4d:
            print('key =', k)
            print('decrypt_data =', decrypt_data[:10])
            read_write_file.write_data_1byte('c4_caesar_c_all_decrypt.bmp', decrypt_data)
            break

    # зашифровать, оставив первые 50 байт без изменения
    data = read_write_file.read_data_1byte('c4_caesar_c_all_decrypt.bmp')
    encrypt_data = data[:50] + caesar.encrypt_data(data[50:], key=70)
    read_write_file.write_data_1byte('c4_caesar_c_all_encrypted_50.bmp', encrypt_data)    
    
# пример формиррования k для модуля substitution.py
def p10():
    import random
    k = list(range(256))
    random.shuffle(k)
    print(k)

# моноалфавитный шифр
def p11():
    import substitution
    encrypt_data = read_write_file.read_data_1byte('c3_subst_c_all.png')
    print(encrypt_data[:10])
    
    for k in range(256):
        decrypt_data = substitution.decrypt_data(encrypt_data)
        if decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50:
            print('k =', k)
            read_write_file.write_data_1byte('c3_subst_c_all_decrypt.png', decrypt_data)
            break

    # зашифровать PNG, оставив 350 байт без изменения
    data = read_write_file.read_data_1byte('c3_subst_c_all_decrypt.png')
    encrypt_data = data[:350] + substitution.encrypt_data(data[350:])
    read_write_file.write_data_1byte('c3_subst_c_all_encrypted_partially.png', encrypt_data)

# файл ff2_affine_c_all - проблема с ключом
# поэтому свой пример
def p12():
    import affin

    e = read_write_file.read_data_1byte('ff2_affin.bmp')
    a = 167
    b = 35

    encrypt_data = affin.encrypt_data(data, a, b)
    read_write_file.write_data_1byte('ff2_affin_encrypt.bmp', encrypt_data)
    
    from time import sleep
    sleep(0.2)

    encrypt_data = read_write_file.read_data_1byte('ff2_affin_encrypt.bmp')
    decrypt_data = affin.decrypt_data(encrypt_data, a, b)
    read_write_file.write_data_1byte('ff2_affin_decrypt.bmp', decrypt_data)


def p13():
    import acrypt
    import affin

    encrypt_data = read_write_file.read_data_1byte('text10_affine_c_all.txt')
    count_keys = 0
    is_english = False
    for a in range(256):
        if affin.gcd(a, 256) == 1:
            for b in range(256):
                count_keys += 1
                decrypt_data = affin.decrypt_data(encrypt_data[:30], a, b)
                text = ''.join([chr(s) for s in decrypt_data[:30]])
                is_english = detectEnglish.isEnglish(text)
                if is_english:
                    print('k =', count_keys)
                    print('a =', a)
                    print('b =', b)
                    decrypt_data = affin.decrypt_data(encrypt_data, a, b)
                    read_write_file.write_data_1byte('text10_affine_c_all_decrypt.txt', decrypt_data)
                    break
        if is_english:
            break

def p14():
    import acrypt
    import affin
    encrypt_data = read_write_file.read_data_1byte('b4_affine_c_all.png')
    
    count_keys = 0
    is_PNG = False
    for a in range(256):
        if affin.gcd(a,256) == 1:
            for b in range(256):
                count_keys += 1
                decrypt_data = affin.decrypt_data(encrypt_data[:2], a, b)
                is_PNG = decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50
                if is_PNG:
                    print('k =', count_keys)
                    print('a =', a)
                    print('b =', b)
                    decrypt_data = affin.decrypt_data(encrypt_data, a, b)
                    read_write_file.write_data_1byte('b4_affine_c_all_decrypt.png', decrypt_data)
                    break
        if is_PNG:
            break

# шифр Вижинера
def p15():
    encrypt_data = read_write_file.read_data_1byte('im6_vigener_c_all.bmp')
    key = 'magistr'
    decrypt_data = []
    for i in range(len(encrypt_data)):
        m = (encrypt_data[i] - ord(key[i % len(key)])) % 256
        decrypt_data.append(m)
    read_write_file.write_data_1byte('im6_vigener_decrypt.bmp', decrypt_data)

def p16():
    data = read_write_file.read_data_1byte('im6_vigener_decrypt.bmp')
    key = 'magistr'
    encrypt_data = []

    for i, d in enumerate(data[50:]):
        encrypt_data.append((d + ord(key[i % len(key)])) % 256)

    read_write_file.write_data_1byte('im6_vigener_encrypt_50.bmp', data[:50] + encrypt_data)

def p17():
    encrypt_data = read_write_file.read_data_1byte('text4_vigener_c_all.txt')
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
    read_write_file.write_data_1byte('text4_vigener_c_all_decrypt.txt', decrypt_data)

def p18():
    encrypt_data = read_write_file.read_data_1byte('text1_vigener_c.txt')
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
    for i, e in enumerate(encrypt_data):
        
        decrypt_data.append((e - ord(key[i % len(key)])) % 256)
    read_write_file.write_data_1byte('text1_vigener_c_all_decrypt.txt', decrypt_data)

p18()