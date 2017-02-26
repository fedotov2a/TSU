# -*- coding: utf-8 -*-
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

W = 0
H = 1
R = 0
G = 1
B = 2
GRAY = 0

# Порог
THRESHOLD = 400

# Фильтры (маски)
dot_matrix = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
horizontal_line_matrix = [-1, -1, -1, 2, 2, 2, -1, -1, -1]
vertical_line_matrix  = [-1, 2, -1, -1, 2, -1, -1, 2, -1]
plus45_matrix  = [-1, -1, 2, -1, 2, -1, 2, -1, -1]
minus45_matrix = [2, -1, -1, -1, 2, -1, -1, -1, 2]

#------------------------------------------------------------------------------

# Конвертирование изображения формата PIL_Image в PIL_ImageTk
# Чтобы корректно отрисовывалось изображение на форме
def pil2tk_image(pil_image):
    im_tk = ImageTk.PhotoImage(pil_image)
    return im_tk

# Преобразование в серое изображение
def rgb2gray(image_rgb):
    rgb_pixel_map = image_rgb.load()
    
    image_gray = Image.new(image_rgb.mode, image_rgb.size)
    gray_pixel_map = image_gray.load()
    
    width  = image_rgb.size[W]
    height = image_rgb.size[H]

    for y in range(height):
        for x in range(width):
            p = int(rgb_pixel_map[x, y][R] * 0.299 + 
                    rgb_pixel_map[x, y][G] * 0.587 + 
                    rgb_pixel_map[x, y][B] * 0.114)
            gray_pixel_map[x, y] = (p, p, p)
            
    return image_gray

# Получение области 3x3 вокруг пикселя(x, y)
def get_area(pixel_map, x, y):
    area_image = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            area_image.append(pixel_map[x+i, y+j][GRAY])
    return area_image

# Подсчет откликов для разных фильтров
def calc_response(area_image):
    r_dot          = np.dot(area_image, dot_matrix)
    r_h_line       = np.dot(area_image, horizontal_line_matrix)
    r_v_line       = np.dot(area_image, vertical_line_matrix)
    r_plus45_line  = np.dot(area_image, plus45_matrix)
    r_minus45_line = np.dot(area_image, minus45_matrix)
    
    return max([r_dot, r_h_line, r_v_line, r_plus45_line, r_minus45_line])

# Копирование карты пикселей
def copy_image_map(out_map, src_map, width, height):
    for i in range(height):
        for j in range(width):
            out_map[i, j] = src_map[i, j]
    return out_map

# Получение усредненного значения по каждой компоненте пикселя
def get_avg_value(pixel_map, artefacts, x, y):
    k = 1
    r = 0
    g = 0
    b = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if artefacts[x+i][y+j] == False:
                k += 1
                r += pixel_map[x+i, y+j][R]
                g += pixel_map[x+i, y+j][G]
                b += pixel_map[x+i, y+j][B]
    r = int(r / k)
    g = int(g / k)
    b = int(b / k)
    
    return (r, g, b)

#------------------------------------------------------------------------------

# Определение битых пикселей
def get_artefacts_map(image_gray):
    pixel_map = image_gray.load()
    
    width  = image_gray.size[W]
    height = image_gray.size[H]
     
    artefacts_map = [[False] * width for i in range(height)]
    
    for x in range(1, height-1):
        for y in range(1, width-1):
            area_image = get_area(pixel_map, x, y)
            r = calc_response(area_image)
            artefacts_map[x][y] = True if abs(r) >= THRESHOLD else False
    
    return artefacts_map

# Перекрашивание битых пикселей
# Возвращает изображение, не карту пикселей!
def retouch(image_rgb, artefacts):
    pixel_map = image_rgb.load()
    
    new_img = Image.new(image_rgb.mode, image_rgb.size)
    new_img_map = new_img.load()   
    
    width  = image_rgb.size[W]
    height = image_rgb.size[H]
    
    new_img_map = copy_image_map(new_img_map, pixel_map, width, height)
    
    for x in range(1, height-1):
        for y in range(1, width-1):
            if artefacts[x][y] == True:
                new_img_map[x, y] = get_avg_value(pixel_map, artefacts, x, y)

    return new_img

#------------------------------------------------------------------------------
root = tk.Tk()
root.geometry("1042x650")

# Загрузка изображения
img_ruined_rgb = Image.open("me_r.bmp")

# Преобразование в 50 оттенков серого
img_ruined_gray = rgb2gray(img_ruined_rgb)

# Рассчет откликов и формирование карты битых пикселей
artefacts_map = get_artefacts_map(img_ruined_gray)

# Перекрашивание битых пикселей
img_retouch = retouch(img_ruined_rgb, artefacts_map)
img_retouch.save("me_s.bmp")

# Конвертирование для отрисовки на форме
img_ruined  = pil2tk_image(img_ruined_rgb)
img_saved   = pil2tk_image(img_retouch)

# Рисуем картинку слева
label_left = tk.Label(root, image = img_ruined)
label_left.image = img_ruined
label_left.pack()
label_left.place(x=0, y=0, width=512, height=512)

# Рисуем картинку справа
label_right = tk.Label(root, image = img_saved)
label_right.image = img_saved
label_right.pack()
label_right.place(x=530, y=0, width=512, height=512)

root.mainloop()