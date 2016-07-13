"""
Класс пазла Пятнашки
"""

import random
from heapq import heappush, heappop


class Puzzle:

    def __init__(self, sizeH, sizeV):
        self.sizeH = sizeH                                  # Размер по горизонтали и вертикали
        self.sizeV = sizeV
        self.start = tuple([[0, 0] for i in range(sizeH * sizeV)])                      # Пустое начальное состояние
        self.goal = tuple([[i, j] for i in range(sizeV) for j in range(sizeH)])         # Конечное состояние
        self.puzzle = []                                                                     # Последовательность чисел в пазле

    ##
    # Генерация пазла вида ([0,0],[1,2]...[2,2]), где
    # в каждом i-м списке кортежа хранится позиция i-ого элемета в матрице размерностью sizeH, sizeV
    # 0-й элемент соответсвует пустой клетке и всегда идет последним
    # sizeH, sizeV - размерность генерируемого пазла
    # Выход:
    # Кортеж из списков позиций сгенерируемого пазла ([0,0],[1,2]...[2,2])

    def generate_puzzle(self):

        sizeH = self.sizeH
        sizeV = self.sizeV

        isGenerate = 1
        while isGenerate:
            puzzle = []
            while len(puzzle) < sizeH * sizeV - 1:
                x = int(random.random() * sizeH * sizeV)
                if (not x in puzzle) and (x != 0):
                    puzzle.append(x)
            summ = 0                                        # Проверка на сходимость пазла
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
                self.start = turple_repl(coordinates, sizeH * sizeV - 1, self.start)
            else:
                y = x - 1
                self.start = turple_repl(coordinates, y, self.start)
        self.puzzle = puzzle
        return self.start

    def set_start(self, start):
        self.start = start

    # Поиск решения из текущего состояния start

    def searchSolution(self):
        sizeV = self.sizeV
        sizeH = self.sizeH
        goal = self.goal
        start = self.start
        # print('In Search Solution')
        closed = []                                                         # список обработанных состояний
        path_map = []                                                       # пройденная карта
        g = 0                                               # оценка стоимости пути от начального узла до узла n
        h = self.coast(start, goal)
        f = h + g
        openset_heap = []
        heappush(openset_heap, [h, g, f, start, start])  # множество состояний, которые предстоит обработать
        while len(openset_heap) != 0:
            x = heappop(openset_heap)
            if x[3] == goal:
                current_node = x
                path_map.append(goal)
                while current_node[3] != start:
                    path_map.append(current_node[3])
                    current_node = current_node[4]
                return path_map

            closed.append(x[3])
            b = x[3]
            c = b[sizeH * sizeV - 1]
            tentative_g_score = x[1] + 1
            new_ = self.searh_graph(c, b)                       # раскрытие/постановка в очередь смежных состояний
            if len(new_) != 0:
                for i in new_:
                    if i in closed:
                        continue
                    iInOpenSet = self.chekInOpenSet(i, openset_heap,
                                               tentative_g_score)  # Будем получать сразу два признака, наличия в списке
                    # открытых узлов и стоимость от начала до него
                    if not iInOpenSet[0]:
                        tentative_is_better = True
                    else:
                        if tentative_g_score < iInOpenSet[1]:
                            tentative_is_better = True
                        else:
                            tentative_is_better = False
                    if tentative_is_better:
                        g = tentative_g_score
                        h = self.coast(i, goal)
                        f = h + g
                        heappush(openset_heap, [h, g, f, i, x])
            else:
                print('Not search :(')
                return path_map

    # Расчет стоимости (дистанции/количества шагов) пути от позиции node до node_result
    # Вход:
    # node стартовая позиция
    # node_result - конечная позиция
    # Выход:
    # distance - расчитанная дистанция
    def coast(self, node, node_result):
        assert len(node) == len(node_result)
        sizeH =  self.sizeH
        sizeV = self.sizeV
        distance = 0
        for i in range(len(node)):  # Расчет манхетонновского расстояния в нодах
            distance = distance + abs(node[i][0] - node_result[i][0]) + abs(node[i][1] - node_result[i][1])
        if (distance != 0) and (sizeV > 2) and (sizeH > 2):
            for i in range(sizeV):  # Добавление в случаях наличия линейных конфликтов
                a = sizeH * i
                if i != sizeV - 1:  # Не для последней строчки
                    distance += self.checkLinearConflict(i, node[int(a):int(a + sizeH)])
                else:
                    # В последней строчке, не учитываем последнее значение
                    distance += self.checkLinearConflict(i, node[int(a):int(a + sizeH - 2)])
            for i in range(sizeH):  # Добавление в случаях наличия конфликтов в столбцах
                column = []
                if i != sizeH - 1:
                    for j in range(sizeV):
                        column.append(node[i + j * sizeH])
                elif sizeV > 3:
                    for j in range(sizeV - 1):
                        column.append(node[i + j * sizeH])
                distance += self.checkColumnConflict(i, column)
            # Добавление в случае конфликта последнего хода
            if (node[(sizeH - 1) * sizeV - 1] != [sizeV - 2, sizeH - 1]) or (
                node[sizeH * sizeV - 2] != [sizeH - 1, sizeV - 1]):
                distance += 2
            # Проверка угловых конфликтов
            # Левый верхний угол
            if node[1] == [0, 1] and node[sizeH] == [1, 0] and node[0] != [0, 0]:
                if self.checkLinearConflict(0, node[1:3]) != 2:
                    if self.checkColumnConflict(0, [node[sizeV], node[2 * sizeV]]) != 2:
                        distance += 2
            # Правый верхний угол
            # print(node[sizeH-2], node[2*sizeH-1], node[sizeH-1])
            if node[sizeH-2] == [0, sizeH-2] and node[2*sizeH-1] == [1, sizeH-1] and node[sizeH-1] != [0, sizeH-1]:
                if self.checkLinearConflict(0, node[sizeH-3:sizeH-1]) != 2:
                    if sizeV > 3 and self.checkColumnConflict(sizeH-1, [node[2*sizeH-1], node[3*sizeH-1]]):
                        distance += 2
            # Левый нижний угол верхний угол
            # print(node[sizeH*(sizeV-2)], node[sizeH*(sizeV - 1) + 1], node[sizeH*(sizeV - 1)])
            if node[sizeH*(sizeV-2)] == [sizeV-2, 0] and node[sizeH*(sizeV - 1) + 1] == [sizeV - 1, 1] and node[sizeH*(sizeV - 1)] != [sizeV - 1, 0]:
                if sizeH > 3 and self.checkLinearConflict(sizeV - 1, node[sizeH*(sizeV - 1):sizeH*(sizeV-1)+2]) != 2:
                    if self.checkColumnConflict(0, [node[sizeH*(sizeV-3)], node[sizeH*(sizeV-2)]]):
                        distance += 2
        return int(distance)

    # Проверка линейного конфликта
    # Вход:
    # line - строка с координатами для проверки
    # index - индекс данной линии в пазле
    # Выход:
    # isConflict - наличие конфликта Да/Нет
    def checkLinearConflict(self, index, line):
        isConflict = 0
        for i in range(len(line)-1):
            a = line[i]
            if a[0] == index:                           # контролируем только свою линию
                for b in line[i+1::]:
                    if (a[0] == b[0]) and (a[1] > b[1]):
                        isConflict = 2
                        break
        return isConflict

    # Проверка линейного конфликта в столбце
    # Вход:
    # line - строка с координатами для проверки
    # index - индекс данного столбца в пазле
    # Выход:
    # isConflict - наличие конфликта Да/Нет
    def checkColumnConflict(self, index, line):
        isConflict = 0
        for i in range(len(line) - 1):
            a = line[i]
            if a[1] == index:  # контролируем только свой столбец
                for b in line[i+1::]:
                    if (a[1] == b[1]) and (a[0] > b[0]):
                        isConflict = 2
                        break
        return isConflict


    # раскрытие/постановка в очередь смежных состояний
    # Вход:
    # set_ - текущий пазл
    # position - позиция, в которой находится пустое поле (0)
    # Выход:
    # Кортеж с возможными вариантами пазла из текущей позиции
    def searh_graph(self, position, set_):
        sizeV = self.sizeV
        sizeH = self.sizeH

        graphs = ()
        if position[0] > 0:
            tmp = [position[0] - 1, position[1]]
            reply_set_ = turple_repl(tmp, sizeH * sizeV - 1, set_)
            reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
            graphs = turple_repl(reply_set_[::], len(graphs), graphs)
        if position[0] < (sizeV - 1):
            tmp = [position[0] + 1, position[1]]
            reply_set_ = turple_repl(tmp, sizeH * sizeV - 1, set_)
            reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
            graphs = turple_repl(reply_set_[::], len(graphs), graphs)
        if position[1] > 0:
            tmp = [position[0], position[1] - 1]
            reply_set_ = turple_repl(tmp, sizeH * sizeV - 1, set_)
            reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
            graphs = turple_repl(reply_set_[::], len(graphs), graphs)
        if position[1] < (sizeH - 1):
            tmp = [position[0], position[1] + 1]
            reply_set_ = turple_repl(tmp, sizeH * sizeV - 1, set_)
            reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
            graphs = turple_repl(reply_set_[::], len(graphs), graphs)
        return graphs


    # Полученик признака наличия узла (состояния пазла) в списке открытых узлов и стоимость от начала до него
    # Вход:
    # openset - список всех открытых узлов
    # sets - текущий пазл
    # g - значение оценки стоимости
    # Выход:
    # iInOpenset - признак присутствия узла в списке открытых, значение стоимости
    def chekInOpenSet(self, sets, openset, g):
        iInOpenset = [False, []]
        assert isinstance(openset, list)
        for i in openset:
            if i[3] == sets:
                iInOpenset = [True, i[1]]  # Оцениваем по g - количеству ходов
                break
        return iInOpenset

# Замена элемента в кортеже
# Вход:
# t - исходный кортеж
# new_el - элемент для вставки в кортеж
# pos - позиция для вставки
# Выход:
# Кортеж со вставленным элементом
def turple_repl(new_el, pos, t):
    assert isinstance(t, tuple)
    pos = int(pos)
    return t[:pos] + (new_el,) + t[pos + 1:]

