from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.config import Config
Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '800')

from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model


class Board(BoxLayout):
    def __init__(self,*args, **kwargs):
        super(Board,self).__init__(**kwargs)
    pass

class Graph(BoxLayout):
    def __init__(self,*args, **kwargs):
        super(Graph,self).__init__(**kwargs)

class Board_button(Button):
    def __init__(self,*args, **kwargs):
        super(Board_button,self).__init__(**kwargs)

class Layer(BoxLayout):
    def __init__(self,*args, **kwargs):
        super(Layer,self).__init__(**kwargs)

        layer = BoxLayout(orientation="vertical")
        for _ in range(4):
            l = BoxLayout(orientation="horizontal")
            for __ in range(4):
                l.add_widget(Board_button())
            layer.add_widget(l)
        
        self.add_widget(layer)
            
class Log(BoxLayout):
    def __init__(self,*args, **kwargs):
        super(Log,self).__init__(**kwargs)

       

class Game(BoxLayout):
    orientation = 'horizontal'
    def __init__(self,*args, **kwargs):
        super(Game,self).__init__(**kwargs)

        Left = BoxLayout(orientation = 'vertical',size_hint_x = 0.7)
        board = Board()
        graph = Graph()
        Left.add_widget(board)
        Left.add_widget(graph)

        Right = BoxLayout(orientation = 'vertical',size_hint_x = 0.3)
        info = BoxLayout()
        log = Log()
        Right.add_widget(info)
        Right.add_widget(log)

        self.add_widget(Left)
        self.add_widget(Right)
    


class Root(FloatLayout):
    state = State()

    def gotoTitle(self):
        self.clear_widgets()
        self.add_widget(Factory.Title())
    
    def gotoGame(self):
        self.clear_widgets()
        self.add_widget(Factory.Game())

class YonmokuApp(App):
    title = "3D Yonmoku"
    def build(self):
        self.root.gotoTitle()

YonmokuApp().run()

        