from pico2d import *
from mario import Mario
from map_loader import MapLoader

class FixedBackground:
    def __init__(self):
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/stage_1_1.png')
        self.bgm = load_music('C:/Githup_2024_2/2DGP-project1/sounds/01. Ground Theme.mp3')
        self.bgm.set_volume(40)
        self.bgm.repeat_play()

    def draw(self, section_start, scaled_width, screen_height):
        self.image.draw_to_origin(-section_start, 0, scaled_width, screen_height)

    def restart_music(self):
        self.bgm.stop()  # 음악을 중단
        self.bgm.repeat_play()  # 음악을 다시 재생


def main():
    open_canvas(800, 600)

    # 타이틀 화면 로드
    title_image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/title.png')
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
                show_title_screen = False  # 아무 키 입력 시 타이틀 화면 종료

    mario = Mario()
    map_loader = MapLoader()

    # 이미지의 가로 길이를 배경에 맞춰서 계산
    scale = screen_height / background.image.h
    scaled_width = int(background.image.w * scale)
    section_width = screen_width
    num_sections = scaled_width // section_width
    current_section = 0

    # `reset_to_section_1` 함수 정의
    def reset_to_section_1():
        nonlocal current_section
        current_section = 0
        mario.reset_position()
        map_loader.reset_map()  # 모든 상태 초기화 및 파워업 제거
        background.restart_music()  # 배경음악을 다시 재생

    running = True
    while running:
        clear_canvas()

        # 현재 섹션의 시작 위치
        section_start = current_section * section_width

        # 배경 그리기 (현재 섹션만 표시)
        background.draw(section_start, scaled_width, screen_height)

        # 맵 데이터 그리기 (현재 섹션의 블럭 및 적 표시)
        map_loader.draw(current_section)

        # 마리오 업데이트
        # 마리오 업데이트
        mario.update(
            map_loader.get_blocks(current_section),
            map_loader.get_enemies(current_section),
            map_loader.get_powerups(current_section),
            map_loader.get_coins(current_section),
            reset_to_section_1,  # 함수 전달
            map_loader  # map_loader 전달
        )

        # 깃발 충돌 처리 (마지막 섹션에서만)
        if current_section == num_sections - 1:  # 마지막 섹션인지 확인
            for flag in map_loader.flags:
                flag_left, flag_bottom, flag_right, flag_top = flag.get_collision_box()
                if (
                        mario.x > flag_left and mario.x < flag_right and
                        mario.y > flag_bottom and mario.y < flag_top
                ):
                    print("Goal Reached!")
                    flag.is_active = False
                    mario.grab_flag(mario.is_big, flag.x)  # 깃발 x 좌표 전달

        # 파워업 업데이트
        for powerup in map_loader.get_powerups(current_section):
            powerup.update(map_loader.get_blocks(current_section))

        # 동전 애니메이션 업데이트
        for coin in map_loader.get_coins(current_section):
            coin.update()

        # 섹션 이동 처리
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
                        current_section += 1  # 다음 섹션으로 이동
                        mario.x = 40  # 마리오를 섹션 시작 위치로 이동하고 40 추가 이동
                        map_loader.reset_enemies(current_section)  # 현재 섹션의 적 상태 초기화
                    else:
                        # 마지막 섹션에서는 현재 위치 유지
                        mario.x = screen_width - 1

        delay(0.03)

    close_canvas()

if __name__ == '__main__':
    main()
