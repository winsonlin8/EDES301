import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageTk

class DrawCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.current_color = 'black'  # Default color

    def draw_ellipse(self, x1, y1, x2, y2, fill=None):
        if fill is None:
            fill = self.current_color
        self.draw.ellipse([x1, y1, x2, y2], fill=fill)

    def get_image(self):
        return self.image

    def set_color(self, color):
        self.current_color = color

class Application:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

        self.tk_canvas = tk.Canvas(master, width=self.canvas.width, height=self.canvas.height)
        self.tk_canvas.pack()
        self.update_canvas()
        self.tk_canvas.bind("<B1-Motion>", self.paint)

        # Add color changing options
        self.color_button = tk.Button(master, text="Change Color", command=self.change_color)
        self.color_button.pack()

    def paint(self, event):
        radius = 3
        x1, y1 = (event.x - radius), (event.y - radius)
        x2, y2 = (event.x + radius), (event.y + radius)
        self.canvas.draw_ellipse(x1, y1, x2, y2)
        self.update_canvas()

    def update_canvas(self):
        self.photo_image = ImageTk.PhotoImage(self.canvas.get_image())
        self.tk_canvas.imgtk = self.photo_image  # keep reference
        self.tk_canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def change_color(self):
        # Use the color chooser to get a new color
        color_code = colorchooser.askcolor(title ="Choose color")[1]
        if color_code:
            self.canvas.set_color(color_code)

def main():
    root = tk.Tk()
    canvas = DrawCanvas(320, 240)  # ILI9341 screen resolution
    app = Application(root, canvas)
    root.mainloop()

if __name__ == '__main__':
    main()
