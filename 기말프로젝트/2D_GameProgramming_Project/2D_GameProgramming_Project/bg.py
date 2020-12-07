    
from pico2d import *
import gfw

MOVE_PPS = 300

class Bg:
    def __init__(self):
        self.x = 400.0
        self.y = 300.0
        self.sx = 0
        self.sy = 0
        self.src_width = 800
        self.src_height = 600
        self.image = gfw.image.load('res/Background.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.sx, self.sy, self.src_width, self.src_height, self.x, self.y)
     
    def getpos_player(self, p):
        self.sx = int(p.x- 200) // 2 
        self.sy = 0
        pass

    def handle_event(self, e):
        pass