from pico2d import *
import gfw
import math

MOVE_PPS = 150
ATTACK_DIST = 35
ANIMATION_D = 5

class Player:
    def __init__(self):
        self.x = get_canvas_width() // 2
        self.y = get_canvas_height() // 3
        self.font = gfw.font.load('res/ConsolaMalgun.ttf', 35)
        self.image = gfw.image.load('res/player.png')
        self.ground_collide = gfw.image.load('res/Floor.png')
        self.ground_collide2 = gfw.image.load('res/Floor2.png')
        self.heart_red = gfw.image.load('res/heart_red.png')
        self.heart_white = gfw.image.load('res/heart_white.png')
        self.at_sound1 = load_wav('res/attack.wav')
        self.at_sound1.set_volume(100)
        self.hr_sound1 = load_wav('res/hurt.wav')
        self.hr_sound1.set_volume(100)
        self.dx, self.dy = 0, 0
        self.fidx, self.fidy = 0, 9
        self.direction = 0 # 0 왼쪽 1 오른쪽
        self.keydown = 0
        self.attackcount = 0
        self.attackx, self.attacky = 0, 0
        self.life = 5
        self.back = 0
        self.state = 0 # 0 평소 1 공격 2 낙사 3 무적 4 사망
        self.radius = self.image.h // 40
        self.src_width = self.image.w // 7
        self.src_height = self.image.h // 10
        self.delay_gethit = 0
        self.delay_attack = 30
        self.animation_delay = 0
        self.death_animation = 0

        global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
        BOUNDARY_LEFT = -self.image.w // 10
        BOUNDARY_DOWN = -self.image.h // 10
        BOUNDARY_RIGHT = get_canvas_width() - BOUNDARY_LEFT
        BOUNDARY_UP = get_canvas_height() - BOUNDARY_DOWN

    def update(self):
        self.fall()
        self.death()
        self.animation_delay -= 1
        if self.delay_attack != 0:
            self.delay_attack -= 1

        if self.animation_delay <= 0:
            self.animation_delay = ANIMATION_D

        if self.state == 0:
            x, y = self.x, self.y
            x += self.dx * MOVE_PPS * gfw.delta_time
            y += self.dy * MOVE_PPS * gfw.delta_time
            self.x, self.y = x, y

        if self.state == 1:
            if self.attackx < 0:
                self.direction = 0
                self.fidy = 2
            elif self.attackx > 0:
                self.direction = 1
                self.fidy = 7
            self.x += self.attackx
            self.y += self.attacky
            self.attackcount -= 1

            if self.attackcount == 0:
                self.state = 0
                if self.direction == 0 and self.keydown > 0:
                    self.fidy = 3
                if self.direction == 1 and self.keydown > 0:
                    self.fidy = 8
                if self.direction == 0 and self.keydown == 0:
                    self.fidy = 4
                if self.direction == 1 and self.keydown == 0:
                    self.fidy = 9

        if self.state == 2:
            self.x = self.x
            self.y -= 4

        if self.state == 3:
            x, y = self.x, self.y
            x += self.dx * MOVE_PPS * gfw.delta_time
            y += self.dy * MOVE_PPS * gfw.delta_time
            self.x, self.y = x, y
            self.delay_gethit -= 1
            if self.delay_gethit == 0:
                self.state = 0

        if self.state == 4:
            if self.death_animation == 0:
                self.animation_delay = 4
                self.death_animation = 1         
                self.fidx = 0
            if self.direction == 0:
                self.fidy = 0
            if self.direction == 1:
                self.fidy = 5

    def draw(self):
        if self.animation_delay == 1:
            self.fidx = (self.fidx + 1) % 7
        sx = self.fidx * self.src_width
        sy = self.fidy * self.src_height
        self.image.clip_draw(sx, sy, self.src_width, self.src_height, self.x, self.y)
        x = get_canvas_width() - 30 #오른쪽
        y = get_canvas_height() - 30 #아래
        for i in range(self.life):
            heart = self.heart_red if i < self.life else self.heart_white
            heart.draw(x, y)
            x -= heart.w
        pos = 30, get_canvas_height() - 30
        x = get_canvas_width() // 2
        y = get_canvas_height() // 3
        if self.state == 2 and self.back == 1:
            self.ground_collide2.draw(x, y)
            self.ground_collide.draw(x, y)
        #self.font.draw(*pos, 'Score: %.1f' % self.score, SCORE_TEXT_COLOR)

    def handle_event(self, e):
        if e.type == SDL_QUIT:
            gfw.quit()
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.keydown += 1
                self.direction = 0
                self.fidy = 3
                self.dx -= 1
            if e.key == SDLK_RIGHT:
                self.keydown += 1
                self.direction = 1
                self.fidy = 8
                self.dx += 1
            if e.key == SDLK_DOWN:
                self.keydown += 1
                if self.direction == 1:
                    self.fidy = 8
                elif self.direction == 0:
                    self.fidy = 3
                self.dy -= 1
            if e.key == SDLK_UP:
                self.keydown += 1
                if self.direction == 1:
                    self.fidy = 8
                elif self.direction == 0:
                    self.fidy = 3
                self.dy += 1

        if e.type == SDL_KEYUP:
            self.keydown -= 1
            if e.key == SDLK_LEFT:
                if self.keydown == 0:
                    self.fidy = 4
                self.dx += 1
            if e.key == SDLK_RIGHT:
                if self.keydown == 0:
                    self.fidy = 9
                self.dx -= 1
            if e.key == SDLK_DOWN:
                if self.keydown == 0:
                    if self.direction == 1:
                        self.fidy = 9
                    elif self.direction == 0:
                        self.fidy = 4
                self.dy += 1
            if e.key == SDLK_UP:
                if self.keydown == 0:
                    if self.direction == 1:
                        self.fidy = 9
                    elif self.direction == 0:
                        self.fidy = 4
                self.dy -= 1

        elif e.type == SDL_MOUSEBUTTONDOWN and self.delay_attack == 0:
            self.delay_attack = 30
            if self.attackcount == 0:
                self.at_sound1.play()
                self.attack((e.x, get_canvas_height() - e.y - 1))
                self.state = 1

    def attack(self, target):
        x, y = target
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        temp = ATTACK_DIST / dist
        dx = dx * temp * 4
        dy = dy * temp * 4
        self.attackcount = 5
        self.attackx = dx / 5
        self.attacky = dy / 5
        

    def fall(self):
        cx, cy = get_canvas_width() // 2, get_canvas_height() // 3
        fx, fy = self.ground_collide.w // 2, self.ground_collide.h // 2
        
        if self.x < cx - fx - 10 or self.x > cx + fx + 10 or self.y < cy - fy + 10:
            self.state = 2
        if self.y > cy + fy + 30:
            self.state = 2
            self.back = 1

        if self.x < BOUNDARY_LEFT or self.x > BOUNDARY_RIGHT or self.y < BOUNDARY_DOWN or self.y > BOUNDARY_UP:
            self.life = 0

    def collide(self, state):
        if state == 1 and self.state == 0:
            self.life -= 1
            self.hr_sound1.play()
            self.state = 3
            self.delay_gethit = 100
            self.death()

    def death(self):
        if self.life <= 0:
            self.state = 4
            return 1
        elif self.life > 0:
            return 0