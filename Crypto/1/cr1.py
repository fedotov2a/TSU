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

# Литорея
# текст
def p20():
    text = read_write_file.read_data_1byte('data/f5.txt')
    encrypt = ''

    cipher = ['bz', 'cx', 'dw', 'fv', 'gt', 'hs', 'jr', 'kq', 'lp', 'mn']

    for t in text:
        flag = False
        for c in cipher:
            if chr(t).lower() in c:
                encrypt += c[1-c.index(chr(t).lower())]
                flag = True

        if not flag:
            encrypt += chr(t)

    print(encrypt)
    read_write_file.write_data_1byte_text('encrypt_data/f5_encrypt.txt', encrypt)
    
    decrypt = ''

    for t in encrypt:
        flag = False
        for c in cipher:
            if t in c:
                decrypt += c[1-c.index(t)]
                flag = True

        if not flag:
            decrypt += t

    print(decrypt)

# Литорея
# картинка
def p20_1():
    table = list(range(0, 256, 2))
    t1 = table[:len(table)//2]
    t2 = table[len(table)//2:]
    table = t1 + t2[::-1]
    
    data = read_write_file.read_data_1byte('data/f4.bmp')

    encrypt = []
    for d in data:
        if d in table:
            idx = table.index(d)
            encrypt.append(table[(idx+len(table)//2) % len(table)])
        else:
            encrypt.append(d)

    read_write_file.write_data_1byte('encrypt_data/f4_encrypt_l.bmp', encrypt)

    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f4_encrypt_l.bmp')
    decrypt = []
    for d in encrypt_data:
        if d in table:
            idx = table.index(d)
            if idx < len(table)//2:
                decrypt.append(table[(idx+len(table)//2) % len(table)])
            else:
                decrypt.append(table[idx-len(table)//2])
        else:
            decrypt.append(d)
    print(decrypt[:2])
    read_write_file.write_data_1byte('decrypt_data/f4_decrypt_l.bmp', decrypt)


# шифрующие таблицы Трисемуса
# текст
def p21():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    extra_symbol = ' .,!?:;-@#$%^&*'
    keyword = 'magistr'
    m = list(keyword) + sorted(list(set(list(alphabet)) - set(list(keyword))))

    table = []
    for i, a in enumerate(m):
        if not i % len(keyword):
            table.append(''.join(m[i:i+len(keyword)]))
    if len(table[-1]) != len(keyword):
        table[-1] = table[-1] + extra_symbol[:(len(keyword) - len(table[-1]))]

    print(table)

    text = 'fedotov alexandr alexandrovich'
    encrypt = ''
    for t in text:
        for idx, st in enumerate(table):
            if t in st:
                encrypt += table[(idx+1) % len(table)][st.index(t)]
    print(encrypt)

    decrypt = ''
    for t in encrypt:
        for idx, st in enumerate(table):
            if t in st:
                decrypt += table[idx-1][st.index(t)]
    print(decrypt)

# картинка
def p21_1():
    # from random import randint
    # from random import choice
    # alphabet = list(range(256))
    # keyword = []
    # len_keyword = choice([8, 16, 32, 64, 128])
    # k = 0
    # for _ in range(len_keyword + k):
    #     r = randint(0, 256)
    #     while r in keyword:
    #         r = randint(0, 256)
    #     keyword.append(r)

    # m = keyword + sorted(list( set(alphabet) - set(keyword) ))

    # table = []
    # for idx, t in enumerate(m):
    #     if not idx % (len_keyword):
    #         table.append(m[idx:idx+len_keyword])
    # print(table)

    table = [[43, 119, 178, 55, 169, 255, 214, 200, 171, 192, 237, 227, 230, 245, 181, 151],
             [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
             [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
             [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48],
             [49, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65],
             [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81],
             [82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97],
             [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
             [114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130],
             [131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146],
             [147, 148, 149, 150, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163],
             [164, 165, 166, 167, 168, 170, 172, 173, 174, 175, 176, 177, 179, 180, 182, 183],
             [184, 185, 186, 187, 188, 189, 190, 191, 193, 194, 195, 196, 197, 198, 199, 201],
             [202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 215, 216, 217, 218],
             [219, 220, 221, 222, 223, 224, 225, 226, 228, 229, 231, 232, 233, 234, 235, 236],
             [238, 239, 240, 241, 242, 243, 244, 246, 247, 248, 249, 250, 251, 252, 253, 254]]
    data = read_write_file.read_data_1byte('data/f4.bmp')
    encrypt_data = []
    for d in data:
        for idx, t in enumerate(table):
            if d in t:
                encrypt_data.append(table[(idx+1) % len(table)][t.index(d)])

    read_write_file.write_data_1byte('encrypt_data/f4_encrypt.bmp', encrypt_data)
    encrypt_data = read_write_file.read_data_1byte('encrypt_data/f4_encrypt.bmp')
    decrypt_data = []
    for d in encrypt_data:
        for idx, t in enumerate(table):
            if d in t:
                decrypt_data.append(table[idx-1][t.index(d)])
    read_write_file.write_data_1byte('decrypt_data/f4_decrypt.bmp', decrypt_data)

# шифр вертикальной перестановки
# текст
def p22():
    key = '52134'
    text = 'fedotov alexandr alexandrovich'
    table = []
    for i, t in enumerate(text):
        if not i % len(key):
            table.append(text[i:i+len(key)])

    print(table)
    encrypt = ''
    for k in range(len(key)):
        i = key.index(str(k+1))
        for t in table:
            if i < len(t):
                encrypt += t[i]
    print(encrypt)

# картинка
def p22_1():
    # from random import shuffle
    # key = list(range(0, 64))
    # shuffle(key)
    # print(key)

    key = [20, 23, 35, 29, 10, 53, 41, 31, 59, 63, 60, 44, 38, 52, 30, 18,
            5, 14, 32, 22, 17, 36, 26, 15, 47, 24, 54, 11, 39, 27, 4, 
           46, 58, 42, 43, 51, 57, 45, 28, 37, 40, 8, 3, 2, 0, 33, 1, 7,
           9, 49, 50, 16, 34, 55, 56, 19, 21, 25, 61, 6, 48, 62, 12, 13]

    data = read_write_file.read_data_1byte('data/f4.bmp')
    table = []
    for i, d in enumerate(data):
        if not i % len(key):
            table.append(data[i:i+len(key)])
    encrypt = []
    for k in range(len(key)):
        i = key.index(k)
        for t in table:
            if i < len(t):
                encrypt.append(t[i])
    read_write_file.write_data_1byte('encrypt_data/f4_encrypt_v.bmp', encrypt)


# маршрутный шифр
# с первого столбца снизу вверх, по второму столбцу сверху вниз, по третьему снизу вверх и т.д.
def p23():
    text = 'fedotov alexandr alexandrovich'
    st = 6
    table = []
    for i, t in enumerate(text):
        if not i % st:
            table.append(list(text[i:i+st]))
    print(table)
    table_transpose = list(zip(*table))
    print(table_transpose)
    for i, t in enumerate(table_transpose):
        if not i % 2:
            table_transpose[i] = t[::-1]

    print(table_transpose)

    encrypt = ''
    for t in table_transpose:
        for s in t:
            encrypt += s
    print(encrypt)

p21()