from pico2d import *
import gfw
import random
from enemy_melee import Enemy_melee
from enemy_ranged import Enemy_range
from enemy_charged import Enemy_charge


max_count = 4

def init():
    global ground
    ground = gfw.image.load('res/Floor.png')
    global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
    BOUNDARY_LEFT = get_canvas_width() // 2 - ground.w // 2
    BOUNDARY_DOWN = get_canvas_height() // 3 - ground.h // 2
    BOUNDARY_RIGHT = get_canvas_width() // 2 + ground.w // 2
    BOUNDARY_UP = get_canvas_height() // 3 + ground.h // 2

def get_border_coords():
    cw, ch = get_canvas_width(), get_canvas_height()
    sw, sh = ground.w, ground.h

    side = random.randint(1, 4)
    if side == 1: #left
        x = BOUNDARY_LEFT
        y = random.random() * sh-sh/2 + ch // 3

    elif side == 2: #down
        x = random.random() * sw-sw/2 + cw // 2
        y = BOUNDARY_DOWN

    elif side == 3: #right
        x = BOUNDARY_RIGHT
        y = random.random() * sh-sh/2 + ch // 3

    else: #up
        x = random.random() * sw-sw/2 + cw // 2
        y = BOUNDARY_UP
    return x, y

def get_rand_pos():
    cw, ch = get_canvas_width(), get_canvas_height()
    sw, sh = ground.w, ground.h

    x = random.random() * sw-sw/2 + cw // 2
    y = random.random() * sh-sh/2 + ch // 3
    return x, y

def generate():
    which = random.randint(1, 3)
    if which == 1:
        x, y = get_border_coords()
        e1 = Enemy_melee(x, y)
        gfw.world.add(gfw.layer.enemy_melee, e1 )
    if which == 2:
        x, y = get_rand_pos()
        e2 = Enemy_range(x, y)
        gfw.world.add(gfw.layer.enemy_range, e2 )
    if which == 3:
        x, y = get_border_coords()
        e3 = Enemy_charge(x, y)
        gfw.world.add(gfw.layer.enemy_charge, e3 )

def update():
    count = gfw.world.count_at(gfw.layer.enemy_melee) + gfw.world.count_at(gfw.layer.enemy_range) + gfw.world.count_at(gfw.layer.enemy_charge)
    if count < max_count:
        generate()