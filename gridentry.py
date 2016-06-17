from kivy.properties import (ListProperty,
                             NumericProperty)
from kivy.uix.button import Button


# класс для одной кнопки на PuzzleGrid
class GridEntry(Button):
    num = NumericProperty(1)
    position = ListProperty([0, 0])

    def str_value(self, a):                     # Возврат числа как строки, и пустой строки, если свойство num равно 0
        if not self.num == 0:
            return str(a)
        return ''
    pass