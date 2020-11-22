from pico2d import *
import gfw
import math

MOVE_PPS = 300
ATTACK_DIST = 2

class Enemy:
    def __init__(self):
        self.x = get_canvas_width() // 2 + 100
        self.y = get_canvas_height() // 3
        self.image = gfw.image.load('res/Enemy_melee.png')
        self.dx, self.dy = 0, 0
        self.fidx, self.fidy = 0, 9
        self.direction = 0 # 0 왼쪽 1 오른쪽
        self.speed = 0
        self.life = 3
        self.back = 0
        self.state = 0 # 0 평소 1 공격 2 낙사 3무적
        self.radius = self.image.h // 40
        self.src_width = self.image.w // 5
        self.src_height = self.image.h // 10
        self.delay_gethit = 0

        global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
        BOUNDARY_LEFT = -self.image.w // 10
        BOUNDARY_DOWN = -self.image.h // 10
        BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
        BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN

    def update(self):
        self.collide(0)
        self.death()
        if self.delay_gethit > 0:
            self.delay_gethit -= 1

        if self.state == 0:
            x, y = self.x, self.y
            self.x, self.y = x, y

        if self.state == 1:
            if self.attackx < 0:
                self.direction = 0
            elif self.attackx > 0:
                self.direction = 1
            self.x += self.attackx
            self.y += self.attacky
            self.attackcount -= 1
            if self.attackcount == 0:
                self.state = 0
                if self.direction == 0 and self.keydown > 0:
                    self.fidy = 3
                if self.direction == 1 and self.keydown > 0:
                    self.fidy = 8

        if self.state == 2:
            self.x = self.x
            self.y = self.y - 5

    def draw(self):
        self.fidx = (self.fidx + 1) % 5
        sx = self.fidx * self.src_width
        sy = self.fidy * self.src_height
        self.image.clip_draw(sx, sy, self.src_width, self.src_height, self.x, self.y)
        x = get_canvas_width() // 2
        y = get_canvas_height() // 3

    def handle_event(self, e):
        pass

    def attack(self, target):
        x, y = target
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        temp = ATTACK_DIST / dist
        dx = dx * temp
        dy = dy * temp
        self.attackcount = 10
        self.attackx = dx / 10
        self.attacky = dy / 10
        
    def collide(self, state):
        if state == 1 and self.state == 0:
            self.life -= 1
            self.state = 3
            self.delay_gethit = 100

    def death(self):
        if self.x < BOUNDARY_LEFT or self.x > BOUNDARY_RIGHT or self.y < BOUNDARY_DOWN or self.y > BOUNDARY_UP:
            self.life = 0
        return self.life <= 0

    def melee(self, p):
        x, y= self.x, self.y
        px, py = p.x, p.y
        dx = px - x
        dy = py - y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        temp = ATTACK_DIST / dist
        dx = dx * temp
        dy = dy * temp
        self.x = self.x + dx
        self.y = self.y + dy
        return x, y