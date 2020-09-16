from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

def handle_events():
    global running
    global dx
    global x, y
    events = get_events()
    for event in events:
        if event.type ==SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                dx=-3
            elif event.key == SDLK_RIGHT:
                dx=3
            elif event.key == SDLK_SPACE:
                dx=0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                dx=0
            elif event.key == SDLK_RIGHT:
                dx=0
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x, KPU_HEIGHT - 1 - event.y+200
	
open_canvas(KPU_WIDTH, KPU_WIDTH)

gra = load_image('grass.png')
ch = load_image('run_animation.png')

x = 0
y = 0
dx = 0
fidx = 0
running = True
while running:
    clear_canvas()
    gra.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    ch.clip_draw(fidx*100,0,100,100,x,y)
    hide_cursor()
    update_canvas()

    handle_events()
    fidx = (fidx +1) %8
    x+=dx
    delay(0.01)
close_canvas()
