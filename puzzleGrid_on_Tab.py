from kivy.properties import (ListProperty, BooleanProperty)
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
from gridentry import GridEntry

from utils.puzzle import Puzzle
from utils.puzzle import turple_repl

import threading

from keras.preprocessing.sequence import pad_sequences
import numpy as np
import math



# Класс сетки пазла
class PuzzleGrid_on_Tab(GridLayout):

    sizeH = 4
    sizeV = 4
    datadim = 2 * 4 * 4
    puzzle = ListProperty()                                 # свойство, хранит пазл в виде цифр
    puzzle_before_turn = ListProperty([1, 1, 1])            # пазл дo сделанного хода
    isWin = BooleanProperty(False)                          # признак того, что все собрали
    check = BooleanProperty(False)                          # Для отслеживания хода
    puzz = Puzzle(sizeH, sizeV)                             # сам пазл в виде списка координат
    start = puzz.generate_puzzle()
    puzzle = puzz.puzzle
    step = 0
    play = BooleanProperty(False)
    # start_Th = threading.Event()
    start_Th_II = threading.Event()

    def __init__(self, *args, **kwargs):                    # конструктор
        super(PuzzleGrid_on_Tab, self).__init__(*args, **kwargs)
        self.generateGrid(self.sizeH, self.sizeV)
        self.bind(check=self.checkWin)
        self.bind(isWin=self.win)


        # Clock.schedule_interval(self.show_time, 1)

    def generateGrid(self, V, H):                           # генерирурем PuzzleGrid
        a = 0
        self.cols = H
        for row in range(V):
            for column in range(H):
                grid_entry = GridEntry(num=self.puzzle[a], position=(row, column))
                grid_entry.bind(on_press=self.button_pressed)
                self.add_widget(grid_entry)
                a += 1

    def button_pressed(self, button):                                       # Обработчика нажатия кнопки
        # self.isTrain = self.parent.ids['isCheckBox'].active  # Таким образом можно определить объект по id в KV файле

        for i in range(len(self.children)):
            if self.children[i].num == 0:
                j = i
        index = self.children.index(button)
        grid_tmp1 = self.children[index]
        grid_tmp2 = self.children[j]
        delta_x = abs(int(grid_tmp1.position[0]) - int(grid_tmp2.position[0]))
        delta_y = abs(int(grid_tmp1.position[1]) - int(grid_tmp2.position[1]))
        if (delta_x + delta_y) == 1:
            a = grid_tmp1.num
            b = grid_tmp2.num
            position_tmp = grid_tmp1.position
            grid_tmp1.position = grid_tmp2.position
            grid_tmp2.position = position_tmp
            self.children[j] = grid_tmp1
            self.children[index] = grid_tmp2                                    # Замена объектов для отображения
            c = self.puzzle.index(a)
            d = self.puzzle.index(b)
            e = self.puzzle[c]
            self.puzzle[c] = self.puzzle[d]
            self.puzzle[d] = e                                                  # Замена значений в массиве puzzle
            self.parent.step += 1                                               # Увеличиваем счетчик ходов
            self.check = not self.check                                         # сигналим изменение

# Изменение размерности поля
    def resize(self, a, b):
        self.sizeV = a
        self.sizeH = b
        self.puzz = Puzzle(self.sizeH, self.sizeV)
        self.start = self.puzz.generate_puzzle()
        self.parent.step = 0
        self.parent.time = 0
        # self.path_map = []
        self.puzzle = self.puzz.puzzle
        self.clear_widgets(self.children)
        self.generateGrid(self.sizeH, self.sizeV)
        # self.bind(check=self.checkWin)
        self.generateStart()

# Вызыватеся после каждого сделанного хода по изменению свойства isWin, в т.ч. и для проверки окончания игры
    def checkWin(self, instance, value):
        self.puzzle_before_turn = self.start
        self.generateStart()
        if self.check_result():
            self.isWin = True
        else:
            pass
            # print('not win')
            #self.content = Button(text='You win!', font_size=48)
            #self.popup = Popup(title='Message', content=self.content, size_hint=(0.4, 0.4), auto_dismiss=False)
            # self.content.bind(on_press=self.popup.dismiss)
            #self.content.bind(on_press=self.newGame)
            #self.popup.open()

    def win(self, instance, value):
        # print('Win', instance, value)
        Clock.unschedule(self.show_time)
        self.isWin = False

    def new_game(self):
        self.puzz = Puzzle(self.sizeH, self.sizeV)
        self.start = self.puzz.generate_puzzle()
        self.parent.step = 0
        self.parent.time = 0
        # self.path_map = []
        self.puzzle = self.puzz.puzzle
        self.clear_widgets(self.children)
        self.generateGrid(self.sizeH, self.sizeV)
        # self.bind(check=self.checkWin)
        self.generateStart()
        Clock.unschedule(self.show_time)
        Clock.schedule_interval(self.show_time, 1)


# Генерация пазла на основе текущего расположения фишек
    def generateStart(self):
        self.start = tuple([[0, 0] for i in range(self.sizeH * self.sizeV)])
        for x in self.puzzle:
            index = self.puzzle.index(x)
            coordinates = [0, 0]
            coordinates[0] = index // self.sizeH
            coordinates[1] = index % self.sizeH
            if (x == 0):
                self.start = turple_repl(coordinates, self.sizeH * self.sizeV - 1, self.start)
            else:
                y = x - 1
                self.start = turple_repl(coordinates, y, self.start)

# Проверка текущего состояния на финальное
    def check_result(self):
        result = True
        for i in range(1, len(self.puzzle), 1):
            if self.puzzle[i - 1] != i:
                result = False
                break
        if result:
            print(' In chek win, puzzle - ', self.puzzle)
            self.play = False
        return result

    def show_time(self, dt):
        # print (dt)
        self.parent.time += 1

# Запуск эвристического поиска решения
    def start_evr(self):
        print('In start/stop play on Evr')
        if not self.play:
        #if not self.start_Th.isSet():
            self.puzz.set_start(self.start)
            self.p1 = threading.Thread(target=self.searchOnEvrStart)  # Для запуска поиска решения в отдельном потоке
            # self.start_Th.set()
            self.play = True
            self.p1.start()
        else:
            print('In Stop')
            Clock.unschedule(self.my_play)
            self.play = False

    def searchOnEvrStart(self):
        self.path_map = self.puzz.searchSolution()
        print(self.path_map)
        print(len(self.path_map) - 1)
        self.step = len(self.path_map) - 1
        Clock.schedule_interval(self.my_play, 0.7)
        # self.start_Th.clear()

    def my_play(self, dt):  # Игра с помощью найденного эвристического решения

        if self.step != 0:
            # print(self.path_map[self.step])
            pos = self.path_map[self.step][self.sizeH * self.sizeV - 1]
            # print('Go to -', pos)
            self.press(pos)  # передаем куда пошла пустая 16-клетка
            self.step -= 1
        else:
            # self.start_Th.clear()
            Clock.unschedule(self.my_play)
            self.play = False

    # Запуск игры с помощью нейронной сети
    def start_on_II(self):
        print('In start/stop play on II')

        #if not self.start_Th_II.isSet() and self.isSoapPresent:
        if not self.play:
            self.p2 = threading.Thread(target=self.searchOnIIStart)  # Для запуска обращений к сервису в отдельном потоке
            # self.start_Th_II.set()
            self.play = True
            self.p2.start()
        else:
            self.play = False

    # Игра с помощью нейронной сети
    def searchOnIIStart(self):
        print("In Thread II, schedule... ")
        while not self.isWin and self.play:
            self.puzz.set_start(self.start)
            values = self.puzz.searh_values()
            # print('Values - ', values)
            values.shape = (-1, 2, 2 * self.sizeH * self.sizeV)
            pos = [0, 0]
            maxIIValue = 0
            self.iiValues = []
            for X in values:
                X.shape = (-1, 2 * self.sizeH * self.sizeV)
                X = np.array(pad_sequences(X, maxlen=self.datadim, padding='post'))
                X.shape = (-1, 2 * self.datadim)
                prediction = self.client.service.get_predict_on_batch({'float': X[0].tolist()})
                X.shape = (-1, self.datadim, 2)
                self.iiValues.append(prediction[0][0])
                if (prediction[0][0] > maxIIValue):
                    maxIIValue = prediction[0][0]
                    pos = X[0][self.datadim / 2 + self.sizeH * self.sizeV - 1]
            self.iiValues.sort()
            print('Values - ', self.iiValues)
            print('MaxIIValue - ', maxIIValue)
            print('Pos in MaxIIValue - ', pos)
            self.press(pos.tolist())
        # self.play = False
        # Clock.unschedule(self.my_playII)

    def press(self, pos):  # Эммитируем нажатиа на кнопку в которой указана передаваемая позиция

        for i in self.children:  # ищем объект кнопки, содержащий переданную позицию
            if i.position == pos:
                break
        self.button_pressed(i)  # эммитируем нажатие найденного объекта кнопки



