from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model


class Board(BoxLayout):
    pass

class Graph(BoxLayout):
    def __init__(self,*args, **kwargs):
        super(Graph,self).__init__(**kwargs)
        
        l = Label(text="3Dmodel")
        self.add_widget(l)

class Game(BoxLayout):

    def __init__(self,*args, **kwargs):
        super(Game,self).__init__(**kwargs)

        Left = BoxLayout(orientation = 'vertical')
        board = Board()
        graph = Graph()
        Left.add_widget(board)
        Left.add_widget(graph)

        Right = BoxLayout(orientation = 'vertical')
        info = BoxLayout()
        log = BoxLayout()
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

        