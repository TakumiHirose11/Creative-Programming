from turtle import title
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class Board(BoxLayout):
    pass


class Root(FloatLayout):
    def gotoTitle(self):
        self.clear_widgets()
        self.add_widget(Factory.Title())
    
    def gotoBoard(self):
        self.clear_widgets()
        self.add_widget(Factory.Board())

class YonmokuApp(App):
    title = "3D Yonmoku"
    def build(self):
        self.root.gotoTitle()

YonmokuApp().run()

        