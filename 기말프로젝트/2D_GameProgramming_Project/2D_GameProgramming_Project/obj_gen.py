from pico2d import *
import gfw
import random
from enemy import Enemy

BORDER = 30
max_count = 10

def init():
    global BOUNDARY_LEFT, BOUNDARY_RIGHT, BOUNDARY_DOWN, BOUNDARY_UP
    BOUNDARY_LEFT = -BORDER
    BOUNDARY_DOWN =  -BORDER
    BOUNDARY_RIGHT = get_canvas_width() + BORDER
    BOUNDARY_UP = get_canvas_height() + BORDER

def get_border_coords():
    cw, ch = get_canvas_width(), get_canvas_height()
    dx = random.random()
    if dx < 0.5: dx -= 1
    dy = random.random()
    if dy < 0.5: dy -= 1
    side = random.randint(1, 4)
    if side == 1: #left
        x = -BORDER
        y = random.random() * ch
        if dx < 0: dx = -dx             #dx:  -1.0 ~ -0.5 or 0.5 ~ 1.0

    elif side == 2: #down
        x = random.random() * cw
        y = -BORDER
        dx = random.random() * 2 - 1
        dy = random.random() * 2 - 1
        if dy < 0: dy = -dy

    elif side == 3: #right
        x = cw + BORDER
        y = random.random() * ch
        dx = random.random() * 2 - 1
        dy = random.random() * 2 - 1
        if dx > 0: dx = -dx

    else: #up
        x = random.random() * cw
        y = ch + BORDER
        dx = random.random() * 2 - 1
        dy = random.random() * 2 - 1
        if dy > 0: dy = -dy

    return x, y, dx, dy

def generate():
    x, y, dx, dy = get_border_coords()
    mag = random.uniform(0.5, 1.0)
    m = Missile((x,y), (dx, dy), mag)
    gfw.world.add(gfw.layer.missile, m)

def update():
    count = gfw.world.count_at(gfw.layer.missile)
    if count < max_count:
        generate()
