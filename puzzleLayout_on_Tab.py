from kivy.properties import (NumericProperty)
from kivy.uix.floatlayout import FloatLayout


# собсвенный макет подложки для вкладок

class PuzzleLayout_on_Tab(FloatLayout):
    step = NumericProperty(0)                                       # количество сделанных шагов
    time = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(PuzzleLayout_on_Tab, self).__init__(*args, **kwargs)