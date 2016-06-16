__author__ = 'Makeev K.P.'
("\n"
 "Game Puzzle\n"
 "Приложение пятнашки\n")

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.properties import (ListProperty,
                             NumericProperty,
                             BooleanProperty)

from utils.puzzle import Puzzle
from utils.puzzle import turple_repl

Builder.load_string("""

<AllPanel>:
    id: tbp
    tab_pos: 'top_mid'
#    size_hint: (1,1)
    do_default_tab: False
    tab_height: 60
    tab_width: 200
    PuzzleLayout_on_Tab1
        id: _PuzzleLayout_on_Tab1
        PuzzleGrid_on_Tab1
            id: idPuzzleGrid_on_Tab1
            size_hint: (0.75, 0.8)
            pos_hint: {'x':0, 'y': 0.1}
        Label:
            text: 'Step - ' + str(_PuzzleLayout_on_Tab1.step)
            font_size: 24
            size_hint: (0.2, 0.1)
            pos_hint: {'x':0.77, 'y': 0.9}
    FloatLayout:
        Label:
            id: tab2_content
            text: 'Tab2'
        Label:
            id: tab3_content
            text: 'Tab3'
    TabbedPanelHeader:
        id: tab1
        border: 0, 0, 0, 0
        content: _PuzzleLayout_on_Tab1.__self__
        BoxLayout:
            x: tab1.x
            y: tab1.y
            width: tab1.width
            height: tab1.height - 6
            orientation: 'horizontal'
            Image:
                id: human_image
                source: 'src//human.png'
            Label:
                text: 'Human'
    TabbedPanelHeader:
        id: tab2
        border: 0, 0, 0, 0
        content: tab2_content.__self__
        BoxLayout:
            x: tab2.x
            y: tab2.y
            width: tab2.width
            height: tab2.height - 6
            orientation: 'horizontal'
            Image:
                source: 'src//calculate.png'
            Label:
                text: 'Heuristic'
    TabbedPanelHeader:
        id: tab3
        border: 0, 0, 0, 0
        content: tab3_content.__self__
        BoxLayout:
            x: tab3.x
            y: tab3.y
            width: tab3.width
            height: tab3.height - 6
            orientation: 'horizontal'
            Image:
                source: 'src//brain.png'
            Label:
                text: 'Neural net'

<GridEntry>:
    id: element
    font_size: self.height-5
    text: element.str_value(element.num)


""")


class GridEntry(Button):                                   # класс для одной кнопки на PuzzleGrid
    num = NumericProperty(1)
    position = ListProperty([0, 0])

    def str_value(self, a):                                # Возврат числа как строки, и пустой строки для нуля
        if not self.num == 0:
            return str(a)
        return ''
    pass


class PuzzleLayout_on_Tab1(FloatLayout):                            # собсвенный макет подложки
    step = NumericProperty(0)                                       # количество сделанных шагов

    def __init__(self, *args, **kwargs):
        super(PuzzleLayout_on_Tab1, self).__init__(*args, **kwargs)



# Пазл для первой панели
class PuzzleGrid_on_Tab1(GridLayout):                        # GridLayout для паззла

    sizeH = 4
    sizeV = 4
    puzzle = ListProperty()                                 # свойство, хранит пазл в виде цифр
    puzzle_before_turn = ListProperty([1, 1, 1])            # пазл дo сделанного хода
    isWin = BooleanProperty(False)                          # признак того, что все собрали
    puzz = Puzzle(sizeH, sizeV)                             # сам пазл в виде объеката
    start = puzz.generate_puzzle()
    puzzle = puzz.puzzle

    def __init__(self, *args, **kwargs):                    # конструктор
        super(PuzzleGrid_on_Tab1, self).__init__(*args, **kwargs)
        self.generateGrid(self.sizeH, self.sizeV)
        self.bind(isWin=self.checkWin)

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
            self.isWin = not self.isWin                                         # сигналим изменение

# Вызыватеся после каждого сделанного хода по изменению свойства isWin, в т.ч. и для проверки окончания игры
    def checkWin(self, instance, value):
        self.puzzle_before_turn = self.start
        self.generateStart()
        # self.puzzle = instance.puzzle
        if self.check_result():
            print('You win')
        else:
            print ('not win')
            #self.content = Button(text='You win!', font_size=48)
            #self.popup = Popup(title='Message', content=self.content, size_hint=(0.4, 0.4), auto_dismiss=False)
            # self.content.bind(on_press=self.popup.dismiss)
            #self.content.bind(on_press=self.newGame)
            #self.popup.open()

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
        if result: print(' In chek win, puzzle - ', self.puzzle)
        return result


class AllPanel(TabbedPanel):

    def __init__(self, *args, **kwargs):
        super(AllPanel, self).__init__(*args, **kwargs)

#        self.isTrain = self.parent.ids['isCheckBox'].active

        # self.puzzle_Grid = PuzzleGrid_on_Tab1(puzzle=self.puzzle)
        # self.puzzle_Layout_on_tab1 = PuzzleLayout_on_Tab1();
        # self.puzzle_Grid.bind(isWin=self.launch_popup)
        # self.puzzle_Grid.generateGrid(self.sizeV, self.sizeH)
        #self.puzzle_Layout_on_tab1.add_widget(self.puzzle_Grid)


class PuzzleApp(App):

    tabbed_panel = AllPanel()

    def build(self):
        tabbed_panel = self.tabbed_panel

        return tabbed_panel

if __name__ == '__main__':
    PuzzleApp().run()
