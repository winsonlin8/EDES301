from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '240')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Fbo, ClearBuffers, ClearColor
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import numpy as np
import cv2
import joblib
import os

MODEL_PATH = '/var/lib/cloud9/EDES301/final_code/quickdraw/drawing_classifier.pkl'

class KivyCanvas(Widget):
    def __init__(self, **kwargs):
        super(KivyCanvas, self).__init__(**kwargs)
        self.color_tuples = [(0, 0, 0), (1, 0, 0), (1, 0.647, 0), (1, 0.8, 0),
                             (0, 1, 0), (0, 0, 1), (0.294, 0, 0.509), (1, 0.752, 0.796)]
        self.color_names = ["Black", "Red", "Orange", "Yellow", "Green", 
                            "Blue", "Indigo", "Pink"]
        self.color_index = 0

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.set_color()

        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            print(f"Model loaded from {MODEL_PATH}")
        else:
            self.model = None
            print("Model not found. Please ensure drawing_classifier.pkl exists.")

        self.prediction_label = None

    def set_color(self):
        with self.canvas:
            self.canvas_color = Color(*self.color_tuples[self.color_index])

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
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.set_color()
        if self.prediction_label:
            self.prediction_label.text = "Prediction: "

    def change_color(self):
        self.color_index = (self.color_index + 1) % len(self.color_names)
        self.set_color()

    def guess_shape(self):
        if self.model is None:
            print("No model loaded.")
            return

        fbo = Fbo(size=self.size)
        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            fbo.add(self.canvas)
        fbo.draw()

        try:
            img = np.frombuffer(fbo.texture.pixels, np.uint8)
            img = img.reshape((fbo.texture.height, fbo.texture.width, 4))
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
            img = cv2.resize(img, (256, 256))

            moments = cv2.moments(img)
            hu_moments = cv2.HuMoments(moments)
            hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
            feature = hu_moments.flatten().reshape(1, -1)

            if feature.shape[1] != 7:
                print(f"Feature shape mismatch: got {feature.shape[1]}, expected 7")
                if self.prediction_label:
                    self.prediction_label.text = "Prediction: Invalid Shape"
                return

            prediction = self.model.predict(feature)[0]
            label = "Circle" if prediction == 1 else "Square"
            print("Prediction:", label)
            if self.prediction_label:
                self.prediction_label.text = f"Prediction: {label}"
        except Exception as e:
            print("Error while predicting:", str(e))
            if self.prediction_label:
                self.prediction_label.text = "Prediction: Error"

class CanvasApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        canvas = KivyCanvas(size_hint=(1, 0.85))
        btn_layout = BoxLayout(size_hint_y=None, height=30)

        color_btn = Button(text='Color', size_hint_x=None, width=60)
        clear_btn = Button(text='Clear', size_hint_x=None, width=60)
        guess_btn = Button(text='Guess', size_hint_x=None, width=60)
        color_label = Label(text="Color: " + canvas.color_names[canvas.color_index], size_hint_x=None, width=150)
        prediction_label = Label(text="Prediction: ", size_hint_x=None, width=200)

        canvas.prediction_label = prediction_label

        color_btn.bind(on_press=lambda x: [canvas.change_color(), setattr(color_label, 'text', "Color: " + canvas.color_names[canvas.color_index])])
        clear_btn.bind(on_press=lambda x: canvas.clear_canvas())
        guess_btn.bind(on_press=lambda x: canvas.guess_shape())

        btn_layout.add_widget(color_btn)
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(guess_btn)
        btn_layout.add_widget(color_label)
        btn_layout.add_widget(prediction_label)

        root.add_widget(canvas)
        root.add_widget(btn_layout)

        return root

if __name__ == '__main__':
    CanvasApp().run()
