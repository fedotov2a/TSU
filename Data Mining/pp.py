# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from numbers import Number

def to_int(var):
    try: return int(var)
    except: return float('NaN')

def is_nan(var):
    return var != float('NaN')

def parse_house(data):
    house_info = data.replace('/', ' ').split(' ')

    the_floor_number = to_int(house_info[0])
    floors_number    = to_int(house_info[1])
    house_type       = 'NaN' if house_info[2] == '?' else house_info[2]

    first_floor = False
    boundary = False

    if is_nan(the_floor_number): first_floor = the_floor_number == 1
    if is_nan(floors_number):    boundary    = the_floor_number == 1 or the_floor_number == floors_number

    relation = the_floor_number / floors_number
    return floors_number, the_floor_number, first_floor, boundary, relation, house_type

def parse_types(t):
    types = ['Б', 'П', 'М', 'К']
    res = []
    for x in types:
        res.append(t == x)
    return res

data = pd.read_csv('flats.csv', sep=';', encoding='Windows-1251')       # DataFrame данные о квартирах

if data['Цена,руб'].dtype is not Number:                                # Преобразовать столбец с ценой в числовой тип
    data['Цена,руб'] = data['Цена,руб'].str.replace(' ', '')
    data['Цена,руб'] = pd.to_numeric(data['Цена,руб'])

data = data.sort_values(by='Цена,руб')                                                  # Сортируем по столбцу с ценой
data = data.drop_duplicates(['Улица', '№ дома', 'Дом', 'Площадь'], keep='first')        # Удаляем повторяющиеся записи

data['Кол-во этажей в доме'], data['Этаж'], \
  data['Первый этаж'], data['Крайний этаж'], \
    data['Отношение этаж/кол-во этажей'], data['Тип дома'] = zip(*data['Дом'].map(parse_house))      # Парсим столбец Дом
   
house_types_all = data[['Тип дома']]                                                                 # Составляем таблицу по типам домов, количеству и процентному соотношению
house_types_all.insert(loc=1, column='Кол-во', value = np.ones(len(house_types_all)))
house_types_all = house_types_all.groupby('Тип дома').sum()
total = house_types_all['Кол-во'].sum()
house_types_all['Проценты'] = house_types_all['Кол-во'].apply(lambda x: round(float(x / total) * 100, 2))

small_number_types_count = house_types_all.loc[house_types_all['Кол-во'] == 1, 'Кол-во'].sum()           # Уберем типы с кол-вом 1 и добавим их в NaN
house_types_all = house_types_all[house_types_all['Кол-во'] != 1]
house_types_all.at['NaN', 'Кол-во'] = house_types_all.at['NaN', 'Кол-во'] + small_number_types_count
house_types_all.at['NaN', 'Проценты'] = round(float(house_types_all.at['NaN', 'Кол-во']/total) * 100, 2)

house_types_all['Б'], house_types_all['П'], house_types_all['М'], house_types_all['К'] = zip(*house_types_all.index.to_series().map(parse_types))
house_types_all.index = house_types_all.index.to_series().replace({'П':'Б-П', 'Б':'Б-П', 'К':'М-К', 'М':'М-К'}) 
house_types_all = house_types_all.groupby(house_types_all.index, sort=False).sum()                               # Выведем число записей каждого типа в шт и процентах
house_types_all['Проценты'] = house_types_all['Кол-во'].apply(lambda x: round(float(x/total) * 100, 2))

print(house_types_all)