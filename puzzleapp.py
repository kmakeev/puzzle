from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from puzzleLayout_on_Tab import PuzzleLayout_on_Tab
from puzzleGrid_on_Tab import PuzzleGrid_on_Tab


__author__ = 'Makeev K.P.'

"""Game Puzzle"""


Builder.load_string("""

<PuzzleApp>
    id: myApp

<AllPanel>:
    id: tbp
    tab_pos: 'top_mid'
    size_hint: (1,1)
    do_default_tab: False
    tab_height: 70
    tab_width: 200
    PuzzleLayout_on_Tab1
        id: _PuzzleLayout_on_Tab1
        PuzzleGrid_on_Tab1
            id: idPuzzleGrid_on_Tab1
            size_hint: (1, 0.85)
            pos_hint: {'x': 0, 'y': 0.15}
        Label:
            text: 'Step - ' + str(_PuzzleLayout_on_Tab1.step)
            font_size: 24
            size_hint: (0.2, 0.1)
            pos_hint: {'x':0.77, 'y': 0.035}
        #Slider:
        #    id: slider1
        #    min: 4
        #    max: 49
        #    value: 16
        #    step: 1
        #    size_hint: (0.27, 0.1)
        #    pos_hint: {'x':0.05, 'y': 0.035}
        #    on_value: idPuzzleGrid_on_Tab1.change_scale(slider1.value)
        Button:
            text: 'New'
            size_hint: (0.2, 0.1)
            pos_hint: {'x': 0.35, 'y': 0.035}
            font_size: self.height - 10
            #on_press: app.playOnEvr()
            on_press: idPuzzleGrid_on_Tab1.new_game()
    PuzzleLayout_on_Tab2
        id: _PuzzleLayout_on_Tab2
        PuzzleGrid_on_Tab2
            id: idPuzzleGrid_on_Tab2
            size_hint: (1, 0.85)
            pos_hint: {'x': 0, 'y': 0.15}
        Label:
            text: 'Step - ' + str(_PuzzleLayout_on_Tab2.step)
            font_size: 24
            size_hint: (0.2, 0.1)
            pos_hint: {'x':0.77, 'y': 0.035}
        #Slider:
        #    id: slider2
        #    min: 4
        #    max: 49
        #    value: 16
        #    step: 1
        #    size_hint: (0.27, 0.1)
        #    pos_hint: {'x':0.05, 'y': 0.035}
        #    on_value: idPuzzleGrid_on_Tab2.change_scale(slider2.value)
    PuzzleLayout_on_Tab3
        id: _PuzzleLayout_on_Tab3
        PuzzleGrid_on_Tab3
            id: idPuzzleGrid_on_Tab3
            size_hint: (1, 0.85)
            pos_hint: {'x': 0, 'y': 0.15}
        Label:
            text: 'Step - ' + str(_PuzzleLayout_on_Tab3.step)
            font_size: 24
            size_hint: (0.2, 0.1)
            pos_hint: {'x':0.77, 'y': 0.035}
        #Slider:
        #    id: slider3
        #    min: 4
        #    max: 49
        #    value: 16
        #    step: 1
        #    size_hint: (0.27, 0.1)
        #    pos_hint: {'x':0.05, 'y': 0.035}
        #    on_value: idPuzzleGrid_on_Tab3.change_scale(slider3.value)
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
            #Label:
            #    text: 'Human'
            Label:
                text: str(_PuzzleLayout_on_Tab1.time) + ' s'
                font_size: 14
    TabbedPanelHeader:
        id: tab2
        border: 0, 0, 0, 0
        content: _PuzzleLayout_on_Tab2.__self__
        BoxLayout:
            x: tab2.x
            y: tab2.y
            width: tab2.width
            height: tab2.height - 6
            orientation: 'horizontal'
            Image:
                source: 'src//calculate.png'
            #Label:
            #    text: 'Heuristic'
            Label:
                text: str(_PuzzleLayout_on_Tab2.time) + ' s'
                font_size: 14
    TabbedPanelHeader:
        id: tab3
        border: 0, 0, 0, 0
        content: _PuzzleLayout_on_Tab3.__self__
        BoxLayout:
            x: tab3.x
            y: tab3.y
            width: tab3.width
            height: tab3.height - 6
            orientation: 'horizontal'
            Image:
                source: 'src//brain.png'
            #Label:
            #    text: 'Neural net'
            Label:
                text: str(_PuzzleLayout_on_Tab3.time) + ' s'
                font_size: 14
#    FloatLayout:
#        id: from_tabbed
#        size_hint: (2.5, 0.9)


<GridEntry>:
    id: element
    font_size: self.height-5
    text: element.str_value(element.num)


""")


# classes layout
class PuzzleLayout_on_Tab1(PuzzleLayout_on_Tab):

    pass

class PuzzleLayout_on_Tab2(PuzzleLayout_on_Tab):
    pass


class PuzzleLayout_on_Tab3(PuzzleLayout_on_Tab):
    pass


# GridLayout паззла human
class PuzzleGrid_on_Tab1(PuzzleGrid_on_Tab):
    pass


class PuzzleGrid_on_Tab2(PuzzleGrid_on_Tab):
    pass


class PuzzleGrid_on_Tab3(PuzzleGrid_on_Tab):
    pass


class AllPanel(TabbedPanel):

    def __init__(self, *args, **kwargs):
        super(AllPanel, self).__init__(*args, **kwargs)



class PuzzleApp(App):

    use_kivy_settings = False
    tabbed_panel = AllPanel()
    icon = 'src//icon.png'
    title = 'Puzzle application'

    def build(self):
        tabbed_panel = self.tabbed_panel
        config = self.config
        s = config.get('puzzle', 'size')
        tabbed_panel.ids['idPuzzleGrid_on_Tab1'].resize(int(s[0]), int(s[2]))
        tabbed_panel.ids['idPuzzleGrid_on_Tab2'].resize(int(s[0]), int(s[2]))
        tabbed_panel.ids['idPuzzleGrid_on_Tab3'].resize(int(s[0]), int(s[2]))
        return tabbed_panel

    def build_config(self, config):
        config.add_section('puzzle')
        config.set('puzzle', 'size', '4x4')

    def build_settings(self, settings):
        settings.add_json_panel('Puzzle Application', self.config, data='''[
            { "type": "title", "title": "Options" },
            { "type": "options", "title": "Field size ",
                "desc": "Fields size of the puzzle",
                "section": "puzzle", "key": "size",
                "options": ["2x2", "3x3", "4x4", "5x5", "6x6", "7x7"]}
            ]''')

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('puzzle', 'size'):
                self.tabbed_panel.ids['idPuzzleGrid_on_Tab1'].resize(int(value[0]), int(value[2]))
                self.tabbed_panel.ids['idPuzzleGrid_on_Tab2'].resize(int(value[0]), int(value[2]))
                self.tabbed_panel.ids['idPuzzleGrid_on_Tab3'].resize(int(value[0]), int(value[2]))

    def on_pause(self):

        return True

    def on_resume(self):
        pass

    def on_resize(self, win, width, heigth):
        print(width, heigth, win)

    def on_start(self):
        self.root_window.fbind('on_resize', self.on_resize)

if __name__ == '__main__':
    PuzzleApp().run()
