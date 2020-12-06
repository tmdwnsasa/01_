from pico2d import *
import gfw
import math
from bullet import Bullet


MOVE_PPS = 300
ATTACK_DIST = 0.5

class Enemy_range:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = gfw.image.load('res/Enemy_range.png')
        self.dx, self.dy = 0, 0
        self.fidx, self.fidy = 0, 9
        self.direction = 0 # 0 왼쪽 1 오른쪽
        self.speed = 0
        self.life = 3
        self.die = 0
        self.back = 0
        self.dist = 0
        self.state = 1 #1 공격 2 무적(맞고 넉백)
        self.radius = self.image.h // 40
        self.src_width = self.image.w // 5
        self.src_height = self.image.h // 10
        self.delay_gethit = 0
        self.delay_attack = 100
        self.delay_die = 40
        self.animation_delay = 0
        self.attack_check = 0
        self.attackcount = 0

        global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
        BOUNDARY_LEFT = -self.image.w // 10
        BOUNDARY_DOWN = -self.image.h // 10
        BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
        BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN

    def update(self):
        self.death()
        self.animation_delay -= 1
        if self.animation_delay <= 0:
            self.animation_delay = 10
        if self.delay_gethit > 0:
            self.delay_gethit -= 1
        if self.life == 0:
            self.state = 3
        

    def draw(self):
        if self.animation_delay == 1:
            self.fidx = (self.fidx + 1) % 5
        sx = self.fidx * self.src_width
        sy = self.fidy * self.src_height
        self.image.clip_draw(sx, sy, self.src_width, self.src_height, self.x, self.y)
        x = get_canvas_width() // 2
        y = get_canvas_height() // 3

    def handle_event(self, e):
        pass
        
    def collide(self, state):
        if state == 1 and self.state == 1:
            self.life -= 1
            self.state = 2
            self.delay_gethit = 50
            self.fidx = 0

    def death(self):
        if self.x < BOUNDARY_LEFT or self.x > BOUNDARY_RIGHT or self.y < BOUNDARY_DOWN or self.y > BOUNDARY_UP:
            self.life = 0
        return self.die

    def move(self, p):
        temp = 0
        x, y= self.x, self.y
        px, py = p.x, p.y
        self.dx = px - x
        self.dy = py - y
        self.dist = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.dist != 0:
            temp = ATTACK_DIST / self.dist
        self.dx = self.dx * temp
        self.dy = self.dy * temp

        if self.state == 1:         #공격
            if self.x < p.x:
                direction = 1
            if self.x > p.x:
                direction = 0
            self.delay_attack -= 1
            if self.delay_attack == 0:
                self.attack(p)
            self.attackcount -= 1
            if self.direction == 0:
                self.fidy = 2
            if self.direction == 1:
                self.fidy = 7
            if self.attackcount == 0:
                self.state = 0

        if self.state == 2:         #경직
            self.delay_gethit -= 1
            if self.direction == 1:
                self.fidy = 6
            elif self.direction == 0:
                self.fidy = 1
            if self.delay_gethit == 0:
                self.state = 1

        if self.state == 3:         #사망
            self.delay_die -= 1
            if self.direction == 1:
                self.fidy = 5
            elif self.direction == 0:
                self.fidy = 0
            if self.delay_die == 0:
                self.die = 1
        return x, y
    
    def attack(self, player):
        self.delay_attack = 300
        e4 = Bullet(self.x, self.y, player.x, player.y)
        gfw.world.add(gfw.layer.bullet, e4)