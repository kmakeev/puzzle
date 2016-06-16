__author__ = 'Makeev K.P.'

"""Обработка сгенерированных решений:
Чтение сгенерированных решений из файлов, получение на их основе данных для тренировки модели, сохранение полученыых массивов данных
в файлы

Вход:
sizeH, sizeV - размер пазла по горизонтали и вертикали в файлах с найденными решениями

для обучения
file_nameX - путь до места сохранения массовов с данными эталонных значений/данных для тестирования
file_nameY - путь до места сохранения массовов с данными эталонных значений/данных для тестирования
dir_ - место расположения файлов

"""


import keras.utils.io_utils as HDF5Matrix
import numpy as np
from check_values import check_values
import os

# обрабатываем файлы с данными для модели
sizeH = 3
sizeV = 3

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\Y_train'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\X_train'
dir_ = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\'
x_train = np.array([])
y_train = np.array([])


for name in os.listdir(dir_):
    file = os.path.join(dir_, name)
    if os.path.isfile(file):
        print('Read ', file)
        solution = HDF5Matrix.load_array(file)
        l = len(solution)
        for i in range(l-1):
            # Для каждого хода из записанных данных получаем эталонные варианты
            values = check_values(solution[i+1], solution[i], sizeH, sizeV)
            for i in values:
                if type(i) is int:
                   y_train = np.append(y_train, i)
                else:
                    x_train = np.append(x_train, i)
print('Reading finish')
x_train.shape = (-1, 2, 2*sizeH*sizeV)

print('Y_TRAIN LENGTH- ', len(y_train))
print('X_TRAIN LENGTH- ', len(x_train))
print('X_TRAIN - ', x_train)
print('Saving x_train, y_train')
HDF5Matrix.save_array(x_train, file_nameX)
HDF5Matrix.save_array(y_train, file_nameY)

# чтение данных для проверки из отдельного каталога

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\Y_test'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\X_test'
dir_ = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\2'
x_train = np.array([])
y_train = np.array([])


for name in os.listdir(dir_):
    file = os.path.join(dir_, name)
    if os.path.isfile(file):
        print('Read for test', file)
        solution = HDF5Matrix.load_array(file)
        l = len(solution)
        for i in range(l-1):
            values = check_values(solution[i+1], solution[i], sizeH, sizeV)
            for i in values:
                if type(i) is int:
                   y_train = np.append(y_train, i)
                else:
                   x_train = np.append(x_train, i)

print('Reading for test finish')
x_train.shape = (-1, 2, 2*sizeH*sizeV)

print('Y_TEST LENGTH- ', len(y_train))
print('X_TEST LENGTH- ', len(x_train))
print('X_TEST - ', x_train)
print('Saving x_test, y_test')
HDF5Matrix.save_array(x_train, file_nameX)
HDF5Matrix.save_array(y_train, file_nameY)
