from pico2d import *
from mario import Mario

# 캔버스 열기
open_canvas()

# 마리오 객체 생성
mario = Mario()

running = True
while running:
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        else:
            mario.handle_event(event)

    mario.update()

    clear_canvas()
    mario.draw()
    update_canvas()

    delay(0.01)

close_canvas()
