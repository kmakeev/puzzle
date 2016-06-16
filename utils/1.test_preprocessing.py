__author__ = 'Makeev K.P.'

"""
Генерация решенией пазла пятнашки и сохранение его в файл для дальнейшей обработки
Вход - none,
sizeH, sizeV - размер полей по горизонтали и вертикали
count - количество генерируемых решений
max_turn - максимально допустимое количество ходов в решении
path - путь для сохранения файлов
Выход -  файлы с решениями пазла размерностью sizeH на sizeV
"""

import keras.utils.io_utils as HDF5Matrix
import numpy as np
from puzzle import Puzzle


sizeH = 4
sizeV = 4
file_name = []
number_solution = 0
count = 1000
max_turn = 100
path = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\Solution'

while number_solution <= count:
    puzz = Puzzle(sizeH, sizeV)
    start = puzz.generate_puzzle()
    print('Start puzzle', start)

    solution = np.array(puzz.searchSolution())
    l = len(solution)-1                     # поправка на начальное состоние
    print(' Have solution in -', l, ' step!')
    if (l > 0) and (l < max_turn):
        file_name = path + str(number_solution) + '-' + str(len(solution))
        HDF5Matrix.save_array(solution, file_name)
        number_solution += 1
        print('Saving in ', file_name)
