# -*- coding: utf-8 -*-

import sys
import imageio      # Для чтения видео
import numpy as np
from numpy import linalg    # Для решение СЛУ
from skimage.morphology import skeletonize      # Для скелетизации линии лазера
from PIL import Image, ImageDraw                # Для рисования на изображении
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5 import uic

class VideoAnalyzer(QMainWindow):
    
    VID_SIZE = (640, 480) # Работает с видео размерами 640x480
    BREAK_FRAME = 1000    # Ограничение по кадрам
    THRESHOLD = 150       # Порог бинаризации

    RED = 0     # Красная компонента в изображении,
                # представленном массивом: image[row][pix][color]
                # или 
                # [[[RED, G, B], [RED, G, B] ... ], ..., [[RED, G, B], [RED, G, B] ...]]

    # Изображение представляется массивом image[row][pix][color]
    # Последовательность изображений: vid = [image_1, ..., image_N]
    vid_src = []          # Исходная последовательность изображений
    vid_skelet = []       # Последовательность изображений после скелетизации

    # Файл с 3D точками
    file_with_3d_points = open('3d_points.txt', 'w')

    # Опорные области представляются в виде 4-х точек (двумерных)
    # support_area:
    #               key: 'top_left_point' - верхняя левая точка
    #                    'top_right_point' - верхняя правая точка
    #                    'bottom_left_point' - нижняя левая точка
    #                    'bottom_right_point' - нижняя правая точка
    #               value: {x, y}
    # Координаты {x, y} записаны в системе координат изображения.
    support_area_top = {
                      'top_left_point':     {'x': 0, 'y': 0},
                      'top_right_point':    {'x': 0, 'y': 0},
                      'bottom_left_point':  {'x': 0, 'y': 0},
                      'bottom_right_point': {'x': 0, 'y': 0},
                     }

    support_area_bottom = {
                      'top_left_point':     {'x': 0, 'y': 0},
                      'top_right_point':    {'x': 0, 'y': 0},
                      'bottom_left_point':  {'x': 0, 'y': 0},
                      'bottom_right_point': {'x': 0, 'y': 0},
                     }

    support_area_left = {
                      'top_left_point':     {'x': 0, 'y': 0},
                      'top_right_point':    {'x': 0, 'y': 0},
                      'bottom_left_point':  {'x': 0, 'y': 0},
                      'bottom_right_point': {'x': 0, 'y': 0},
                     }

    support_area_right = {
                      'top_left_point':     {'x': 0, 'y': 0},
                      'top_right_point':    {'x': 0, 'y': 0},
                      'bottom_left_point':  {'x': 0, 'y': 0},
                      'bottom_right_point': {'x': 0, 'y': 0},
                     }

    support_areas = {
                     'top_area':    support_area_top,
                     'bottom_area': support_area_bottom,
                     'left_area':   support_area_left,
                     'right_area':  support_area_right,
                     }

    # Коэффициенты прямых линий, которые образуют опорную область
    #       key: 'top_area' - верхняя область
    #            'bottom_area' - нижняя область
    #            'left_area' - левая область
    #            'right_area' - правая область
    #       value: 
    #           key:    'top_line' - верхняя линия
    #                   'bottom_line' - нижняя линия
    #                   'left_line' - левая линия
    #                   'right_line' - правая линия
    #           value: {a, b}
    coeff_lines_support_area = {
                               'top_area': {
                                      'top_line':    {'a': 0, 'b': 0},
                                      'bottom_line': {'a': 0, 'b': 0},
                                      'left_line':   {'a': 0, 'b': 0},
                                      'right_line':  {'a': 0, 'b': 0},
                                     },
                               'bottom_area': {
                                      'top_line':    {'a': 0, 'b': 0},
                                      'bottom_line': {'a': 0, 'b': 0},
                                      'left_line':   {'a': 0, 'b': 0},
                                      'right_line':  {'a': 0, 'b': 0},
                                     },
                               'left_area': {
                                      'top_line':    {'a': 0, 'b': 0},
                                      'bottom_line': {'a': 0, 'b': 0},
                                      'left_line':   {'a': 0, 'b': 0},
                                      'right_line':  {'a': 0, 'b': 0},
                                     },
                               'right_area': {
                                      'top_line':    {'a': 0, 'b': 0},
                                      'bottom_line': {'a': 0, 'b': 0},
                                      'left_line':   {'a': 0, 'b': 0},
                                      'right_line':  {'a': 0, 'b': 0},
                                     },
                                }

    # Координаты опорных областей в трехмерных координатах
    # support_area_3d:
    #               key: 'top_left_point' - верхняя левая точка
    #                    'top_right_point' - верхняя правая точка
    #                    'bottom_left_point' - нижняя левая точка
    #                    'bottom_right_point' - нижняя правая точка
    #               value: {x, y, z}
    # Координаты {x, y, z} записаны в системе координат рамки (не изображения).
    # Начало координат находится в центре рамки.
    support_area_top_3d = {
                         'top_left_point':     {'x': -69.7, 'y': 113.541, 'z': 25.1},
                         'top_right_point':    {'x': 69.7,  'y': 114.248, 'z': 25.1},
                         'bottom_left_point':  {'x': -69.7, 'y': 88.085,  'z': 0},
                         'bottom_right_point': {'x': 69.7,  'y': 88.578,  'z': 0},
                        }

    support_area_bottom_3d = {
                         'top_left_point':     {'x': -69.7, 'y': -88.085,  'z': 0},
                         'top_right_point':    {'x': 69.7,  'y': -87.378,  'z': 0},
                         'bottom_left_point':  {'x': -69.7, 'y': -113.541, 'z': 25.1},
                         'bottom_right_point': {'x': 69.7,  'y': -112.48, 'z': 25.1},
                        }

    support_area_left_3d = {
                         'top_left_point':     {'x': -112.48,  'y': 69.7,  'z': 25.1},
                         'top_right_point':    {'x': -87.378,  'y': 69.7,  'z': 0},
                         'bottom_left_point':  {'x': -113.541, 'y': -69.7, 'z': 25.1},
                         'bottom_right_point': {'x': -88.085,  'y': -69.7, 'z': 0},
                        }

    support_area_right_3d = {
                         'top_left_point':     {'x': 88.58,   'y': 69.7,  'z': 0},
                         'top_right_point':    {'x': 114.248, 'y': 69.7,  'z': 25.1},
                         'bottom_left_point':  {'x': 87.378,  'y': -69.7, 'z': 0},
                         'bottom_right_point': {'x': 112.48,  'y': -69.7, 'z': 25.1},
                        }

    support_areas_3d = {
                        'top_area':    support_area_top_3d,
                        'bottom_area': support_area_bottom_3d,
                        'left_area':   support_area_left_3d,
                        'right_area':  support_area_right_3d,
                       }

    # Точки линии лазера на опорных областях
    # key: 'top_area'
    #      'bottom_area'
    #      'left_area'
    #      'right_area'
    # value: [[x0, y0], ..., [xN, yN]]
    laser_points_on_support_area = {
                                    'top_area':    [],
                                    'bottom_area': [],
                                    'left_area':   [],
                                    'right_area':  [],
                                   }

    # Коэффициенты линии лазера.
    # Аппроксимированных по МНК.
    # key: 'top_area'
    #      'bottom_area'
    #      'left_area'
    #      'right_area'
    # value: {a, b}
    coeff_approximate_laser_line = {
                                    'top_area':    {'a': 0, 'b': 0},
                                    'bottom_area': {'a': 0, 'b': 0},
                                    'left_area':   {'a': 0, 'b': 0},
                                    'right_area':  {'a': 0, 'b': 0},
                                    }


    # Коэффициенты опорных плоскостей
    coeff_support_planes = {
                            'top_area':    {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                            'bottom_area': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                            'left_area':   {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                            'right_area':  {'A': 0, 'B': 0, 'C': 0, 'D': 0},
                            }

    # Матрица внутренних параметров камеры
    instrict_parameters_of_camera = []


    # Коэффициенты плоскости лазера
    coeff_laser_plane = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    #----------------Методы---------------------

    def __init__(self):
        '''
        Конструктор.
        '''
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        
        self.move(70, 70)
        self.setFixedSize(1200, 680)

        self.COUNT_POINTS = 16
        self.curr_count_points = 0

        # Вешаем события на мышь
        self.canvas_lbl.mousePressEvent = self.get_coord_support_points

        # Соединяем элементы UI с функциями
        self.start_btn.clicked.connect(self.run)
        self.open_vid_file_act.triggered.connect(self.open_vid)

    #---------------------------------------------------------------------------------------
    def get_coord_support_points(self, event):
        '''
        Получает позицию курсора на канвасе и записывает координаты.

        Последовательность выбора точек жестко зашита:
            1. Верхняя область
                1.1. Верхняя левая точка
                1.2. Верхняя правая точка
                1.3. Нижняя левая точка
                1.4. Нижняя правая точка
            2. Нижняя область
                2.1-2.4. аналогично
            3. Левая область
                3.1-3.4. аналогично
            4. Правая область
                4.1-4.4. аналогично
        '''
        if self.curr_count_points < self.COUNT_POINTS:
            # Просто константы
            sa = ['top_area', 'bottom_area', 'left_area', 'right_area']
            sp = ['top_left_point', 'top_right_point', 'bottom_left_point', 'bottom_right_point']

            x, y = event.pos().x(), event.pos().y()
            
            self.teOutput.append('x: ' + str(x) + ' y: ' + str(y))
            if self.curr_count_points != self.COUNT_POINTS - 1:
                self.teOutput.append(sa[(self.curr_count_points + 1) // 4] + ' ' + sp[(self.curr_count_points + 1) % 4] + ':')

            x, y = self.to_other_coordinates_2d(x, y)

            self.support_areas[sa[self.curr_count_points // 4]][sp[self.curr_count_points % 4]]['x'] = x
            self.support_areas[sa[self.curr_count_points // 4]][sp[self.curr_count_points % 4]]['y'] = y

            self.curr_count_points += 1

    #---------------------------------------------------------------------------------------
    def open_vid(self):
        '''
        Открывает видеофайл.

        Работает в Anaconda3 ver.4.3.0.1 для win-x86
        А также дополнительно установленным ffmpeg: 
            conda install ffmpeg -c conda-forge
            imageio.plugins.ffmpeg.download() - хотя работает без этого
                                                возможно из-за того, что вместе с этим файлом лежит ffmpeg.exe
        '''
        filename, ok = QFileDialog.getOpenFileName(self, "Open Video File", "", "Avi files (*.avi);;Mp4 files (*.mp4);;All files (*.*)")

        if ok:
            self.vid_src = imageio.get_reader(filename,  'ffmpeg')
            
            temp_img = self.vid_src.get_data(50)
            imageio.imwrite('__temp.jpg', temp_img)
            self.canvas_lbl.setPixmap(QPixmap('__temp.jpg'))

            self.teOutput.append('Select points:')
            self.teOutput.append('top_area top_left_point:')

    def get_vid_skeleton(self):
        '''
        Скелетизация каждого кадра.
        '''
        self.progressBar.reset()
        self.progressBar.setMaximum(self.BREAK_FRAME)
        for i, frame in enumerate(self.vid_src):
            if i == self.BREAK_FRAME:
                break
            frame_red = frame[:, :, self.RED]       # Оставляет только красную компоненту на изображении
            frame_bin = frame_red > self.THRESHOLD  # Бинаризация изображения
            frame_skelet = skeletonize(frame_bin)   # Скелетизация изображения

            self.vid_skelet.append(frame_skelet)
            self.progressBar.setValue(i)

    #------------------------------------------------------------------------------------

    #----------------Методы для нахождения коэффициентов линий опорных областей-------------
    def get_coeff_line(self, x1, y1, x2, y2):
        '''
        Получает коэффициенты прямой по двум точкам.
        ax + by + c = 0 => a = y1 - y2, b = x2 - x1, c = x1 * y2 - x2 * y1;
        y = px + q      => p = -a / b, q = -c / b;
        '''
        a = y1 - y2
        b = x2 - x1
        c = x1 * y2 - x2 * y1

        try:
            p = -a / b
            q = -c / b
        except:
            p = -a / (b + 1)
            q = -c / (b + 1)

        return {'a': p, 'b': q}

    def find_coeff_for_lines_on_support_area(self):
        '''
        Находит коэффициенты прямых линий, которые образуют опорную область.
        '''
        for key_area, supp_area in self.support_areas.items():
            x1 = supp_area['top_left_point']['x']
            y1 = supp_area['top_left_point']['y']

            x2 = supp_area['top_right_point']['x']
            y2 = supp_area['top_right_point']['y']

            x3 = supp_area['bottom_left_point']['x']
            y3 = supp_area['bottom_left_point']['y']

            x4 = supp_area['bottom_right_point']['x']
            y4 = supp_area['bottom_right_point']['y']

            top_line    = self.get_coeff_line(x1, y1, x2, y2)
            bottom_line = self.get_coeff_line(x3, y3, x4, y4)
            left_line   = self.get_coeff_line(x1, y1, x3, y3)
            right_line  = self.get_coeff_line(x2, y2, x4, y4)

            self.coeff_lines_support_area[key_area]['top_line']['a'] = top_line['a']
            self.coeff_lines_support_area[key_area]['top_line']['b'] = top_line['b']

            self.coeff_lines_support_area[key_area]['bottom_line']['a'] = bottom_line['a']
            self.coeff_lines_support_area[key_area]['bottom_line']['b'] = bottom_line['b']

            self.coeff_lines_support_area[key_area]['left_line']['a'] = left_line['a']
            self.coeff_lines_support_area[key_area]['left_line']['b'] = left_line['b']

            self.coeff_lines_support_area[key_area]['right_line']['a'] = right_line['a']
            self.coeff_lines_support_area[key_area]['right_line']['b'] = right_line['b']

            self.teOutput.append(key_area)
            self.teOutput.append('top_line: ' + 'a: ' + str(round(top_line['a'], 3)) + ' b: ' + str(round(top_line['b'], 3)))
            self.teOutput.append('bottom_line: ' + 'a: ' + str(round(bottom_line['a'], 3)) + ' b: ' + str(round(bottom_line['b'], 3)))
            self.teOutput.append('left_line: ' + 'a: ' + str(round(left_line['a'], 3)) + ' b: ' + str(round(left_line['b'], 3)))
            self.teOutput.append('right_line: ' + 'a: ' + str(round(right_line['a'], 3)) + ' b: ' + str(round(right_line['b'], 3)))

    #----------------------------------------------------------------------------------

    #-----------------Методы для обнаружения линии лазера на опорных областях----------
    def find_min_max_points(self, support_area):
        '''
        Находит минимальные и максимальные координаты точек опорной области.
        '''
        x_min = 0xffff
        y_min = 0xffff
        x_max = 0
        y_max = 0

        for _, xy in support_area.items():
            x_, y_ = self.to_default_coordinates_2d(xy['x'], xy['y'])
            if x_ < x_min:
                x_min = x_

            if x_ >= x_max:
                x_max = x_

            if y_ < y_min:
                y_min = y_

            if y_ >= y_max:
                y_max = y_

        return {'x_min': x_min, 'y_min': y_min,
                'x_max': x_max, 'y_max': y_max,}

    def find_laser_lines_on_support_areas(self, skeleton_image):
        '''
        Находит на опорных областях линию лазера.
        '''
        self.laser_points_on_support_area = {
                                            'top_area': [],
                                            'bottom_area': [],
                                            'left_area': [],
                                            'right_area': [],
                                            }

        for key_area, supp_area in self.support_areas.items():
            min_max = self.find_min_max_points(supp_area)

            for y in range(min_max['y_min'], min_max['y_max']):
                for x in range(min_max['x_min'], min_max['x_max']):
                    try:
                        if skeleton_image[y][x] == True:
                            x_, y_ = self.to_other_coordinates_2d(x, y)
                            self.laser_points_on_support_area[key_area].append([x_, y_])
                    except:
                        continue

    #--------------------------------------------------------------------------------

    #------------Метод наименьших квадратов для линий на опорных областях------------

    def check_laser_lines(self):
        '''
        Проверяет есть ли в кадре две линии лазера, которые находятся на опорных областях.
        '''
        count_lines = 0
        for key_area, arr in self.laser_points_on_support_area.items():
            # Считаем, что линия состоит более, чем из 10 точек
            if len(arr) > 10:
                count_lines += 1
               
        if count_lines < 2:
            return None

        else:
            # Выбрать две линии с наибольшим количеством точек
            result = {}
            for _ in range(2):
                k_max = ''
                v_max = []
                for k, v in self.laser_points_on_support_area.items():
                    if len(v) > len(v_max) and k not in result:
                        k_max = k
                        v_max = v

                result[k_max] = v_max

            return result

    def least_square_method(self):
        '''
        Метод наименьших квадратов.
        '''
        points = self.check_laser_lines()
        if points is None:
            return None

        for key_area, v in points.items():
            n = len(v)
            x_sum = 0
            y_sum = 0
            xy_sum = 0
            x2_sum = 0
            
            for x, y in v:
                x_sum += x
                y_sum += y
                xy_sum += (x*y)
                x2_sum += (x**2)

            try:
                a = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum**2)
                b = (y_sum - a * x_sum) / n
            except:
                a = 0
                b = 0

            self.coeff_approximate_laser_line[key_area]['a'] = a
            self.coeff_approximate_laser_line[key_area]['b'] = b

        return points

    #----------------------------------------------------------------------------

    def find_support_planes(self):
        '''
        Находит коэффициенты A, B, C, D опорных плоскостей.
        '''
        for key_area, val in self.coeff_support_planes.items():
            x1 = self.support_areas_3d[key_area]['top_left_point']['x']
            y1 = self.support_areas_3d[key_area]['top_left_point']['y']
            z1 = self.support_areas_3d[key_area]['top_left_point']['z']

            x2 = self.support_areas_3d[key_area]['top_right_point']['x']
            y2 = self.support_areas_3d[key_area]['top_right_point']['y']
            z2 = self.support_areas_3d[key_area]['top_right_point']['z']

            x3 = self.support_areas_3d[key_area]['bottom_left_point']['x']
            y3 = self.support_areas_3d[key_area]['bottom_left_point']['y']
            z3 = self.support_areas_3d[key_area]['bottom_left_point']['z']

            p1 = np.array([x1, y1, z1])
            p2 = np.array([x2, y2, z2])
            p3 = np.array([x3, y3, z3])

            # Вектора на плоскости
            v1 = p1 - p2
            v2 = p1 - p3

            # Вектор нормали плоскости
            nv = np.cross(v1, v2)
            a, b, c = nv

            d = -np.dot(nv, p3)

            self.coeff_support_planes[key_area]['A'] = a
            self.coeff_support_planes[key_area]['B'] = b
            self.coeff_support_planes[key_area]['C'] = c
            self.coeff_support_planes[key_area]['D'] = d

            self.teOutput.append(key_area + ': A: ' + str(round(a, 3)) + ' B: ' + str(round(b, 3)) + ' C: ' + str(round(c, 3)) + ' D: ' + str(round(d, 3)))

    def get_instrict_parameters_of_camera(self):
        '''
        Находит внутренние параметры камеры.

        [x0_3d, y0_3d, z0_3d, 1, 0, 0, 0, 0, -x0_2d * x0_3d, -x0_2d * y0_3d, -x0_2d * z0_3d] [r0]      [x0_2d]
        [0, 0, 0, 0, x0_3d, y0_3d, z0_3d, 1, -y0_2d * x0_3d, -y0_2d * y0_3d, -y0_2d * z0_3d] [r1]      [y0_2d]
        .                                   .                                                  .          .
        .                                   .                                                  .    =     .
        .                                   .                                                  .          .
        [xN_3d, yN_3d, zN_3d, 1, 0, 0, 0, 0, -xN_2d * xN_3d, -xN_2d * yN_3d, -xN_2d * zN_3d] [rN-1]     [xN_2d]
        [0, 0, 0, 0, xN_3d, yN_3d, zN_3d, 1, -yN_2d * xN_3d, -yN_2d * yN_3d, -yN_2d * zN_3d] [rN]       [yN_2d]
        
        Вектор r - внутренние параметры камеры имеет размерность (N+1), но чтобы решить данную систему
                   нужно взять N элементов, а N+1 элемент принять за единицу.

        Система решается следующим образом:
        D * R = B <=> D^T * D * R = D^T * B <=> R = (D^T * D)^-1 * D^T * B, где D^T - транспонированная матрица, D^-1 - обратная матрица.

        '''
        matrix_a = []
        matrix_b = []

        # Подготовка и заполнение данными
        for key_area, sa in self.support_areas_3d.items():
            for key_point, arr in sa.items():
                x_3d = arr['x']
                y_3d = arr['y']
                z_3d = arr['z']

                x_2d = self.support_areas[key_area][key_point]['x']
                y_2d = self.support_areas[key_area][key_point]['y']

                matrix_a.append([x_3d, y_3d, z_3d, 1, 0, 0, 0, 0, -x_2d * x_3d, -x_2d * y_3d, -x_2d * z_3d])
                matrix_a.append([0, 0, 0, 0, x_3d, y_3d, z_3d, 1, -y_2d * x_3d, -y_2d * y_3d, -y_2d * z_3d])

                matrix_b.append(x_2d)
                matrix_b.append(y_2d)

        a = np.array(matrix_a)
        b = np.array(matrix_b)

        # Решение системы линейных уравнений
        a_tr = a.transpose()
        a = np.matmul(a_tr, a)
        a_inv = linalg.inv(a)

        r = np.matmul(a_inv, np.matmul(a_tr, b))

        self.instrict_parameters_of_camera = r.tolist()
        self.instrict_parameters_of_camera.append(1.0)

    def get_two_points_of_laser_on_support_area(self, key_area):
        '''
        Получает две точки на опорной плоскости.
        '''
        laser_line_a = self.coeff_approximate_laser_line[key_area]['a']
        laser_line_b = self.coeff_approximate_laser_line[key_area]['b']

        if key_area == 'top_area' or key_area == 'bottom_area':
            top_line_a = self.coeff_lines_support_area[key_area]['top_line']['a']
            top_line_b = self.coeff_lines_support_area[key_area]['top_line']['b']

            bottom_line_a = self.coeff_lines_support_area[key_area]['bottom_line']['a']
            bottom_line_b = self.coeff_lines_support_area[key_area]['bottom_line']['b']

            try:
                top_x = (top_line_b - laser_line_b) / (laser_line_a - top_line_a)
            except:
                top_x = (top_line_b - laser_line_b) / (laser_line_a - top_line_a + 1)
            top_y = laser_line_a * top_x + laser_line_b


            try:
                bottom_x = (bottom_line_b - laser_line_b) / (laser_line_a - bottom_line_a)
            except:
                bottom_x = (bottom_line_b - laser_line_b) / (laser_line_a - bottom_line_a + 1)
            bottom_y = laser_line_a * bottom_x + laser_line_b

            return {'x1': top_x, 'y1': top_y, 'x2': bottom_x, 'y2': bottom_y}

        else:
            left_line_a = self.coeff_lines_support_area[key_area]['left_line']['a']
            left_line_b = self.coeff_lines_support_area[key_area]['left_line']['b']

            right_line_a = self.coeff_lines_support_area[key_area]['right_line']['a']
            right_line_b = self.coeff_lines_support_area[key_area]['right_line']['b']

            try:
                left_x = (left_line_b - laser_line_b) / (laser_line_a - left_line_a)
            except:
                left_x = (left_line_b - laser_line_b) / (laser_line_a - left_line_a + 1)
            left_y = laser_line_a * left_x + laser_line_b

            try:
                right_x = (right_line_b - laser_line_b) / (laser_line_a - right_line_a)
            except:
                right_x = (right_line_b - laser_line_b) / (laser_line_a - right_line_a + 1)
            right_y = laser_line_a * right_x + laser_line_b

            return {'x1': left_x, 'y1':left_y, 'x2': right_x, 'y2': right_y}

    def find_laser_points_on_support_area_3d(self, key_area, xy):
        '''
        Находит 3D координаты точек лазера на опорных плоскостях.
        '''
        matrix_a = self.instrict_parameters_of_camera[:]
        matrix_a.append(self.coeff_support_planes[key_area]['A'])
        matrix_a.append(self.coeff_support_planes[key_area]['B'])
        matrix_a.append(self.coeff_support_planes[key_area]['C'])
        matrix_a.append(self.coeff_support_planes[key_area]['D'])
        matrix_a = [matrix_a[0:4], matrix_a[4:8], matrix_a[8:12], matrix_a[12:]]
        matrix_a = np.array(matrix_a)

        matrix_b1 = []
        matrix_b1.append(xy['x1'])
        matrix_b1.append(xy['y1'])
        matrix_b1.append(1)
        matrix_b1.append(0)
        matrix_b1 = np.array(matrix_b1)

        matrix_b2 = []
        matrix_b2.append(xy['x2'])
        matrix_b2.append(xy['y2'])
        matrix_b2.append(1)
        matrix_b2.append(0)
        matrix_b2 = np.array(matrix_b2)

        point_1_3d = linalg.solve(matrix_a, matrix_b1).tolist()
        point_2_3d = linalg.solve(matrix_a, matrix_b2).tolist()

        for i in range(len(point_1_3d) - 1):
            point_1_3d[i] /= point_1_3d[-1]
            point_2_3d[i] /= point_2_3d[-1]

        del(point_1_3d[-1])
        del(point_2_3d[-1])

        point_1_3d = {'x': point_1_3d[0], 'y': point_1_3d[1], 'z': point_1_3d[2]}
        point_2_3d = {'x': point_2_3d[0], 'y': point_2_3d[1], 'z': point_2_3d[2]}

        return [point_1_3d, point_2_3d]

    def find_laser_plane(self, laser_points_3d):
        '''
        Находит параметры плоскости лазера по точкам на опорной области.
        '''
        p1 = np.array([laser_points_3d[1]['x'], laser_points_3d[1]['y'], laser_points_3d[1]['z']])
        p2 = np.array([laser_points_3d[2]['x'], laser_points_3d[2]['y'], laser_points_3d[2]['z']])
        p3 = np.array([laser_points_3d[3]['x'], laser_points_3d[3]['y'], laser_points_3d[3]['z']])

        # Вектора на плоскости
        v1 = p1 - p2
        v2 = p1 - p3

        # Вектор нормали плоскости
        nv = np.cross(v1, v2)
        a, b, c = nv

        d = -np.dot(nv, p3)

        self.coeff_laser_plane['A'] = a
        self.coeff_laser_plane['B'] = b
        self.coeff_laser_plane['C'] = c
        self.coeff_laser_plane['D'] = d

    def get_3d_points_of_surface(self, num_frame):
        '''
        Получает 3D координаты поверхности
        '''
        x_min_surface = self.support_area_top['bottom_left_point']['x'] - 10
        y_min_surface = self.support_area_top['bottom_left_point']['y'] - 10
        x_min_surface, y_min_surface = self.to_default_coordinates_2d(x_min_surface, y_min_surface)

        x_max_surface = self.support_area_bottom['top_right_point']['x'] + 5
        y_max_surface = self.support_area_bottom['top_right_point']['y'] + 5
        x_max_surface, y_max_surface = self.to_default_coordinates_2d(x_max_surface, y_max_surface)

        for y in range(y_min_surface, y_max_surface):
            for x in range(x_min_surface, x_max_surface):
                if self.vid_skelet[num_frame][y][x] == True:
                    x_, y_ = self.to_other_coordinates_2d(x, y)

                    matrix_a = self.instrict_parameters_of_camera[:]
                    matrix_a.append(self.coeff_laser_plane['A'])
                    matrix_a.append(self.coeff_laser_plane['B'])
                    matrix_a.append(self.coeff_laser_plane['C'])
                    matrix_a.append(self.coeff_laser_plane['D'])
                    matrix_a = [matrix_a[0:4], matrix_a[4:8], matrix_a[8:12], matrix_a[12:]]
                    matrix_a = np.array(matrix_a)

                    matrix_b = []
                    matrix_b.append(x_)
                    matrix_b.append(y_)
                    matrix_b.append(1)
                    matrix_b.append(0)
                    matrix_b = np.array(matrix_b)

                    if linalg.det(matrix_a) != 0.0:
                        point_3d = linalg.solve(matrix_a, matrix_b).tolist()

                        for i in range(len(point_3d) - 1):
                            point_3d[i] /= point_3d[-1]

                        del(point_3d[-1])

                        self.file_with_3d_points.write(str(point_3d[0]) + ' ' +
                                                       str(point_3d[1]) + ' ' +
                                                       str(point_3d[2]) + '\n')

    def to_other_coordinates_2d(self, x, y):
        '''
        Переводит экранные координаты в систему координат плоскости изображения.
        '''
        return (x - self.VID_SIZE[0] // 2, self.VID_SIZE[1] // 2 - y)

    def to_default_coordinates_2d(self, x, y):
        '''
        Переводит координаты плоскости изображения в экранные координаты.
        '''
        return (self.VID_SIZE[0] // 2 + x, self.VID_SIZE[1] // 2 - y)

    def paint_surface(self):
        '''
        По облаку точек рисует 3D поврехность.
        '''
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        file = open('3d_points.txt', 'r')
        x = []
        y = []
        z = []

        for i, line in enumerate(file):
            x_, y_, z_ = line.split(' ')
            if float(z_) > 20:
                continue
            x.append(float(x_))
            y.append(float(y_))
            z.append(float(z_))

        file.close()

        ax.plot_trisurf(x, y, z, cmap='jet')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

#---------------------------------
    def analyze_frame(self, points, im, num_frame):
        '''
        Анализирует кадр из видеоряда.
        '''
        if points is None:
            return
        else:
            draw = ImageDraw.Draw(im)

            laser_points_3d = []
            for key_area, value in points.items():
                a = self.coeff_approximate_laser_line[key_area]['a']
                b = self.coeff_approximate_laser_line[key_area]['b']

                xy = self.get_two_points_of_laser_on_support_area(key_area)
                laser_points_3d.append(self.find_laser_points_on_support_area_3d(key_area, xy)[0])
                laser_points_3d.append(self.find_laser_points_on_support_area_3d(key_area, xy)[1])

                r = 6
                x1, y1 = self.to_default_coordinates_2d(xy['x1'], xy['y1'])
                x2, y2 = self.to_default_coordinates_2d(xy['x2'], xy['y2'])

                draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill='blue')
                draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill='blue')

            if not num_frame % 5:
                imageio.imwrite('__temp.jpg', np.asarray(im))    # Рисуется на draw, im тоже изменяется
                self.canvas_lbl.setPixmap(QPixmap('__temp.jpg'))
            
            self.find_laser_plane(laser_points_3d)
            self.get_3d_points_of_surface(num_frame)

    def run(self):
        '''
        Запускает алгоритм нахождения 3D точек.
        '''
        self.teOutput.append('Find lines coeff on support area...')
        self.find_coeff_for_lines_on_support_area()
        self.teOutput.append('----Done----')

        self.teOutput.append('Find instrict parameters of camera...')
        self.get_instrict_parameters_of_camera()

        s_out = ''
        for k in range(3):
            for x in self.instrict_parameters_of_camera[(4*k):(4*(k+1))]:
                s_out += str(round(x, 3)) + ', '
            self.teOutput.append(s_out)
            s_out = ''

        self.teOutput.append('----Done----')

        self.teOutput.append('Find support planes...')
        self.find_support_planes()
        self.teOutput.append('----Done----')

        self.teOutput.append('Skeletonize laser...')
        self.get_vid_skeleton()
        self.teOutput.append('----Done----')

        self.teOutput.append('Find 3D points...')
        self.progressBar.reset()

        for i, frame in enumerate(self.vid_src):
            self.progressBar.setValue(i)
            if i == self.BREAK_FRAME:
                break

            self.find_laser_lines_on_support_areas(self.vid_skelet[i])
            points = self.least_square_method()

            im = Image.fromarray(frame)
            self.analyze_frame(points, im, i)

        self.teOutput.append('----Done----')

        self.vid_src.close()
        self.file_with_3d_points.close()

        self.paint_surface()

app = QApplication(sys.argv)
w = VideoAnalyzer()
w.show()
sys.exit(app.exec_())
