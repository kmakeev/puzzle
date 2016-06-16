"""
Генерация пазла вида ([0,0],[1,2]...[2,2]), где
в каждом i-м списке кортежа хранится позиция i-ого элемета в матрице размерностью sizeH, sizeV
0-й элемент соответсвует пустой клетке и всегда идет последним
Вход:
sizeH, sizeV - размерность генерируемого пазла

Выход:
Кортеж из списков позиций сгенерируемого пазла ([0,0],[1,2]...[2,2])
"""

import random
from turple_repl import turple_repl

class Puzzle:


def generate_puzzle(self, sizeH, sizeV):
    self.start = tuple([[0, 0] for i in range(sizeH*sizeV)])
    isGenerate = 1
    while isGenerate:
        puzzle = []
        while len(puzzle) < sizeH*sizeV-1:
            x = int(random.random()*sizeH*sizeV)
            if (not x in puzzle) and (x != 0):
                puzzle.append(x)
        summ = 0                                        # Проверка на сходимость
        for i in puzzle:
            if i != 0:
                b = 0
                c = puzzle.index(i)
                for j in puzzle[c:len(puzzle)]:
                    if j < i:
                        b += 1
                summ = summ + b
        isGenerate = summ % 2
    puzzle.append(0)
    for x in puzzle:
        index = puzzle.index(x)
        coordinates = [0, 0]
        coordinates[0] = index // sizeH
        coordinates[1] = index % sizeH
        if (x == 0):
            start = turple_repl(coordinates, sizeH*sizeV-1, start)
        else:
            y = x-1
            start = turple_repl(coordinates, y, start)
    print(puzzle)
    return start
