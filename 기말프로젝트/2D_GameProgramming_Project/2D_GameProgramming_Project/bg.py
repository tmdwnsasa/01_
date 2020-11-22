    
from pico2d import *
import gfw

MOVE_PPS = 300

class Bg:
    def __init__(self):
        self.x = get_canvas_width() // 2
        self.y = get_canvas_height() // 2
        self.image = gfw.image.load('res/Background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_event(self, e):
        pass