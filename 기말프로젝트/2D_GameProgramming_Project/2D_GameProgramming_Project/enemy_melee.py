from pico2d import *
import gfw
import math

MOVE_PPS = 300
ATTACK_DIST = 0.5

class Enemy_melee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = gfw.image.load('res/Enemy_melee.png')
        self.hi_sound = load_wav('res/hit.wav')
        self.hi_sound.set_volume(100)
        self.dx, self.dy = 0, 0
        self.fidx, self.fidy = 0, 8
        self.direction = 0 # 0 왼쪽 1 오른쪽
        self.speed = 0
        self.life = 3
        self.die = 0
        self.back = 0
        self.dist = 0
        self.state = 0 # 0 평소 1 공격 2 무적(맞고 넉백)
        self.radius = self.image.h // 40
        self.src_width = self.image.w // 5
        self.src_height = self.image.h // 10
        self.delay_gethit = 0
        self.delay_attack = 0
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
        self.collide(0)
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
        if state == 1 and self.state == 0:
            self.hi_sound.play()
            self.life -= 1
            self.state = 2
            self.delay_gethit = 100
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

        if self.state == 0:         #추격
            if self.dx < 0:
                self.fidy = 3
                self.direction = 0
            elif self.dx > 0:
                self.fidy = 8
                self.direction = 1
            self.attack(self.dist, p)
            self.x = self.x + self.dx
            self.y = self.y + self.dy

        if self.state == 1:         #공격
            self.animation_delay -= 1
            self.attackcount -= 2
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
                self.state = 0

        if self.state == 3:         #사망
            self.delay_die -= 1
            if self.direction == 1:
                self.fidy = 5
            elif self.direction == 0:
                self.fidy = 0
            if self.delay_die == 0:
                self.die = 1



        return x, y
    
    def attack(self, dist, player):
        if dist <= 40 and self.direction == 1 and self.attackcount == 0 and player.state == 0:
            self.fidx = 0
            self.fidy = 7
            self.attackcount = 40
            self.state = 1
            self.dx = 0
            self.dy = 0
        elif dist <= 40 and self.direction == 0 and self.attackcount == 0 and player.state == 0:
            self.fidx = 0
            self.fidy = 2
            self.attackcount = 40
            self.state = 1
            self.dx = 0
            self.dy = 0