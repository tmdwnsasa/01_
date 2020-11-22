from pico2d import *
import gfw
import random
from player import Player
from enemy import Enemy
from bg import Bg
from ground import Ground

STATE_IN_GAME, STATE_GAME_OVER = range(2)

def collides_distance(a, b):
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    dist_sq = (ax-bx)**2 + (ay-by)**2
    return dist_sq < (a.radius + b.radius) ** 2

def enter():
    gfw.world.init(['bg', 'ground', 'enemy', 'player'])
    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    global enemy
    enemy = Enemy()
    gfw.world.add(gfw.layer.enemy, enemy)

    global bg
    bg = Bg()
    gfw.world.add(gfw.layer.bg, bg)

    global ground
    ground = Ground()
    gfw.world.add(gfw.layer.ground, ground)
    
    global game_state
    game_state = STATE_IN_GAME

def update():
    global game_state

    gfw.world.update();
    if game_state != STATE_IN_GAME:
        return
    for o in gfw.world.objects_at(gfw.layer.enemy):
        if collides_distance(o, player):
            if o.collide(player.state) == 0:
                player.decrease_life()
            elif o.collide(player.state) == 1:
                o.decrease_life()
            dead = player.death()
            if dead:    #GAME OVER
                game_state = STATE_GAME_OVER
def draw():
    gfw.world.draw();

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
    player.handle_event(e)



def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()