
from pico2d import *
import gfw
import math

SPEED = 2

class Bullet:
    def __init__(self, x, y, tx, ty):
        self.x = x
        self.y = y
        self.image = gfw.image.load('res/bullet.png')
        self.fidx, self.fidy = 0, 0
        self.speed = 0
        self.state = 0 # 0 날라가는 중
        self.radius = self.image.h // 4
        self.src_width = self.image.w // 5
        self.src_height = self.image.h
        self.animation_delay = 0
        self.attack_check = 0
        self.dx = tx - x
        self.dy = ty - y
        self.dist = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.dist != 0:
            temp = SPEED / self.dist
        self.dx = self.dx * temp

        global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
        BOUNDARY_LEFT = -self.image.w // 5
        BOUNDARY_DOWN = -self.image.h
        BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
        BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN
        self.dy = self.dy * temp
        

    def update(self):
        self.animation_delay -= 1
        if self.animation_delay <= 0:
            self.animation_delay = 10

        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def draw(self):
        if self.animation_delay == 1:
            self.fidx = (self.fidx + 1) % 5
        sx = self.fidx * self.src_width
        sy = self.fidy * self.src_height
        self.image.clip_draw(sx, sy, self.src_width, self.src_height, self.x, self.y)

    def handle_event(self, e):
        pass

    def out_of_screen(self):
        print(self.x)
        if self.x < BOUNDARY_LEFT: 
            return 1
        if self.x > BOUNDARY_RIGHT: 
            return 1
        if self.y < BOUNDARY_DOWN: 
            return 1
        if self.y > BOUNDARY_UP: 
            return 1
        return 0