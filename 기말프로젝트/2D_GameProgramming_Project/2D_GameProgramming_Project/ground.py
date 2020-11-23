from pico2d import *
import gfw


class Ground:

    def __init__(self):
        self.x = get_canvas_width() // 2
        self.y = get_canvas_height() // 3
        self.image1 = gfw.image.load('res/Floor2.png')
        self.image2 = gfw.image.load('res/Floor.png')

    def update(self):
        pass

    def draw(self):
        self.image1.draw(self.x, self.y)
        self.image2.draw(self.x, self.y)

    def handle_event(self, e):
        pass