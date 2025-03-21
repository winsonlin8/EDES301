from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '240')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class KivyCanvas(Widget):
    def __init__(self, **kwargs):
        super(KivyCanvas, self).__init__(**kwargs)
        self.color_tuples = [(0, 0, 0), (1, 0, 0), (1, 0.647, 0), (1, 0.8, 0),
                             (0, 1, 0), (0, 0, 1), (0.294, 0, 0.509), (1, 0.752, 0.796)]
        self.color_names = ["Black", "Red", "Orange", "Yellow", "Green", 
                            "Blue", "Indigo", "Pink"]
        self.color_index = 0

        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.set_color()  # Set initial drawing color

    def set_color(self):
        with self.canvas:
            Color(*self.color_tuples[self.color_index])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.draw_ellipse(touch)
            return True
        return super(KivyCanvas, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.draw_ellipse(touch)
            return True
        return super(KivyCanvas, self).on_touch_move(touch)

    def draw_ellipse(self, touch):
        with self.canvas:
            d = 6.0
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def clear_canvas(self):
        self.canvas.clear()
        self.update_rect()
        self.set_color()  # Reset the current color after clearing

    def change_color(self):
        self.color_index = (self.color_index + 1) % len(self.color_names)
        self.set_color()

class CanvasApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        canvas = KivyCanvas(size_hint=(1, 0.85))
        btn_layout = BoxLayout(size_hint_y=None, height=30)
        
        color_btn = Button(text='Color', size_hint_x=None, width=60)
        clear_btn = Button(text='Clear', size_hint_x=None, width=60)
        color_label = Label(text="Color: " + canvas.color_names[canvas.color_index], size_hint_x=None, width=200)

        color_btn.bind(on_press=lambda x: [canvas.change_color(), setattr(color_label, 'text', "Color: " + canvas.color_names[canvas.color_index])])
        clear_btn.bind(on_press=lambda x: canvas.clear_canvas())

        btn_layout.add_widget(color_btn)
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(color_label)
        
        root.add_widget(canvas)
        root.add_widget(btn_layout)
        
        return root

if __name__ == '__main__':
    CanvasApp().run()
