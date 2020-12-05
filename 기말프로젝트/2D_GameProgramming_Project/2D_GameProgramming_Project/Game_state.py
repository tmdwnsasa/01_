from pico2d import *
import gfw
import random
import obj_gen
from player import Player
from enemy_melee import Enemy_melee
from enemy_ranged import Enemy_range
from enemy_charged import Enemy_charge
from bg import Bg
from ground import Ground

STATE_IN_GAME, STATE_GAME_OVER = range(2)
global GAME_OVER
GAME_OVER = 28

def collides_distance(a, b):
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    dist_sq = (ax-bx)**2 + (ay-by)**2
    return dist_sq < (a.radius + b.radius) ** 2

def enter():
    gfw.world.init(['bg', 'ground', 'enemy_melee','enemy_range','enemy_charge', 'player'])
    obj_gen.init()

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

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
    global GAME_OVER

    if game_state != STATE_IN_GAME:
        return

    dead = player.death()
    if dead == 1:    #GAME OVER
        GAME_OVER -= 1
        if GAME_OVER <= 0:
            game_state = STATE_GAME_OVER

    
    gfw.world.update()
    obj_gen.update()

    for o in gfw.world.objects_at(gfw.layer.enemy_melee):
        if o.death() == 1:
            gfw.world.remove(o)
        o.move(player)
        if collides_distance(o, player):
            o.collide(player.state)
            player.collide(o.state)

    for o in gfw.world.objects_at(gfw.layer.enemy_range):
        if o.death() == 1:
            gfw.world.remove(o)
        o.move(player)

    for o in gfw.world.objects_at(gfw.layer.enemy_charge):
        if o.death() == 1:
            gfw.world.remove(o)
        o.move(player)
        if collides_distance(o, player):
            o.collide(player.state)
            player.collide(o.state)

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