from pico2d import *
from mario import Mario
from map_loader import MapLoader
from time import time
import os
os.environ['PYSDL2_DLL_PATH'] = os.path.abspath('.')

import sys

from utils import resource_path


class FixedBackground:
    def __init__(self):
        self.image = load_image(resource_path('sprites/stage_1_1.png'))
        self.bgm = load_music(resource_path('sounds/01. Ground Theme.mp3'))
        self.bgm.set_volume(40)
        self.bgm.repeat_play()

    def draw(self, section_start, scaled_width, screen_height):
        self.image.draw_to_origin(-section_start, 0, scaled_width, screen_height)

    def restart_music(self):
        self.bgm.stop()
        self.bgm.repeat_play()

def draw_text(text, x, y, size, color=(255, 255, 255)):
    font = load_font('C:/Windows/Fonts/Arial.ttf', size)
    font.draw(x - len(text) * size // 4, y, text, color)


def draw_score(score):
    draw_text(f'SCORE: {score}', 100, 550, 30)


def draw_life(lives):
    draw_text(f'LIFE: {lives}', 700, 550, 30)


def main():
    open_canvas(800, 600)

    # 타이틀 화면 로드
    title_image = load_image(resource_path('sprites/title.png'))
    game_over_image = load_image(resource_path('sprites/game_over.png'))
    game_clear_image = load_image(resource_path('sprites/game_clear.png'))
    game_over_sound = load_music(resource_path('sounds/smb_gameover.mp3'))
    game_over_sound.set_volume(40)
    game_clear_sound = load_music(resource_path('sounds/smb_stage_clear.mp3'))
    game_clear_sound.set_volume(40)

    screen_width, screen_height = 800, 600

    # 배경 및 음악
    background = FixedBackground()

    # 타이틀 화면 표시
    show_title_screen = True
    while show_title_screen:
        clear_canvas()
        title_image.draw_to_origin(0, 0, screen_width, screen_height)
        update_canvas()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                close_canvas()
                return
            elif event.type == SDL_KEYDOWN:
                show_title_screen = False

    mario = Mario()
    map_loader = MapLoader()

    # 이미지의 가로 길이를 배경에 맞춰서 계산
    scale = screen_height / background.image.h
    scaled_width = int(background.image.w * scale)
    section_width = screen_width
    num_sections = scaled_width // section_width
    current_section = 0

    # 타이머 설정
    game_timer = 300  # 타이ptr머 기본값
    start_time = time()  # 시작 시간
    timer_paused = False  # 타이머 멈춤 상태 플래그
    final_time = None  # 최종 시간을 저장하기 위한 변수
    game_over = False  # 게임 오버 상태
    game_clear = False  # 게임 클리어 상태
    game_clear_music_played = False  # 게임 클리어 음악 재생 여부
    game_clear_time = None  # 게임 클리어 시작 시간

    def reset_to_section_1():
        nonlocal current_section, timer_paused, start_time, final_time, game_over
        if mario.lives > 0:
            current_section = 0
            mario.reset_position()
            map_loader.reset_map()
            background.restart_music()
            timer_paused = False
            start_time = time()
            final_time = None
        else:
            game_over = True  # 게임 오버 상태로 전환

    running = True
    while running:
        clear_canvas()

        if game_over:
            # 게임 오버 화면 표시
            game_over_image.draw_to_origin(0, 0, screen_width, screen_height)
            update_canvas()

            # 게임 오버 사운드 재생
            if not game_over_sound.is_playing():
                game_over_sound.play()

            # 입력 대기
            events = get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN:
                    running = False  # 게임 종료
            delay(0.1)
            continue

        if game_clear:
            clear_canvas()
            draw_text("GAME CLEAR!", 400, 300, 60, color=(0, 0, 0))
            draw_text(f"FINAL SCORE: {mario.score}", 400, 200, 50, color=(0, 0, 0))
            update_canvas()

            if not game_clear_music_played:
                game_clear_sound.play()
                game_clear_music_played = True

            events = get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN:
                    running = False
            delay(0.1)
            continue

            # 최종 점수와 클리어 문구 출력
            draw_text("GAME CLEAR!", 400, 300, 60, color=(0, 0, 0))
            draw_text(f"FINAL SCORE: {mario.score}", 400, 200, 50, color=(0, 0, 0))
            update_canvas()
            delay(0.1)
            continue

        # 타이머 업데이트
        if not timer_paused:
            elapsed_time = time() - start_time
            remaining_time = max(0, game_timer - int(elapsed_time))
        elif final_time is not None:
            remaining_time = final_time  # 타이머 멈춘 후 값 유지

        # 현재 섹션의 시작 위치
        section_start = current_section * section_width

        # 배경 그리기
        background.draw(section_start, scaled_width, screen_height)

        # 맵 데이터 그리기
        map_loader.draw(current_section)

        # 마리오 업데이트
        if mario.is_dead:
            mario.update_death(reset_to_section_1)

        else:
            mario.update(
                map_loader.get_blocks(current_section),
                map_loader.get_enemies(current_section),
                map_loader.get_powerups(current_section),
                map_loader.get_coins(current_section),
                reset_to_section_1,
                map_loader
            )

        # 깃발 충돌 처리 및 게임 클리어 조건
        if current_section == num_sections - 1:
            for flag in map_loader.flags:
                flag_left, flag_bottom, flag_right, flag_top = flag.get_collision_box()
                if (
                        mario.x > flag_left and mario.x < flag_right and
                        mario.y > flag_bottom and mario.y < flag_top
                ):
                    flag.is_active = False
                    mario.grab_flag(mario.is_big, flag.x, background)
                    if not timer_paused:  # 타이머가 처음 멈출 때만 처리
                        timer_paused = True
                        final_time = remaining_time  # 멈춘 시간 저장
                    if not mario.on_flag:
                        game_clear = True  # 게임 클리어 상태로 전환

        # x 좌표가 8200에 도달하면 게임 클리어 처리
        if mario.x >= 8200:
            if not game_clear:  # 중복 처리 방지
                print("Mario reached the end!")
                game_clear = True
                game_clear_time = time()
                if not game_clear_music_played:
                    game_clear_sound.play()
                    game_clear_music_played = True

        # 파워업 업데이트
        for powerup in map_loader.get_powerups(current_section):
            powerup.update(map_loader.get_blocks(current_section))

        # 동전 애니메이션 업데이트
        for coin in map_loader.get_coins(current_section):
            coin.update()

        # 섹션 이동 처리
        if current_section == num_sections - 1:
            pass
        else:
            if mario.x >= screen_width:
                if current_section < num_sections - 1:
                    current_section += 1
                    mario.x = 0
                    map_loader.reset_enemies(current_section)
                else:
                    mario.x = screen_width - 1
            elif mario.x <= 0:
                if current_section > 0:
                    current_section -= 1
                    mario.x = screen_width
                    map_loader.reset_enemies(current_section)
                else:
                    mario.x = 1

        # 마리오 그리기
        mario.draw()

        # 적 업데이트 및 그리기
        for enemy in map_loader.get_enemies(current_section):
            enemy.update(map_loader.get_blocks(current_section))
            enemy.draw(0)

        # 파워업 그리기
        for powerup in map_loader.get_powerups(current_section):
            powerup.draw(0)

        # 동전 그리기
        for coin in map_loader.get_coins(current_section):
            coin.draw(0)

        # 점수 표시
        draw_score(mario.score)

        # 라이프 표시
        draw_life(mario.lives)

        # 타이머 텍스트 표시
        draw_text(f'TIME: {remaining_time}', 400, 550, 30)

        update_canvas()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
                mario.handle_event(event)
                # P 키를 누르면 다음 섹션으로 이동
                if event.type == SDL_KEYDOWN and event.key == SDLK_p:
                    if current_section < num_sections - 1:
                        current_section += 1
                        mario.x = 40
                        map_loader.reset_enemies(current_section)
                    else:
                        mario.x = screen_width - 1

        delay(0.03)

    close_canvas()


if __name__ == '__main__':
    main()
