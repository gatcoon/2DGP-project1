from pico2d import *
from mario import Mario
from map_loader import MapLoader

def main():
    open_canvas(800, 600)

    # 타이틀 화면 로드
    title_image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/title.png')
    screen_width, screen_height = 800, 600
    background_image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/stage_1_1.png')

    # 타이틀 화면 표시
    show_title_screen = True
    while show_title_screen:
        clear_canvas()
        # 타이틀 화면을 창 크기에 맞춰서 그리기
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

    # 이미지의 가로 길이를 6등분하여 섹션 계산
    scale = screen_height / background_image.h
    scaled_width = int(background_image.w * scale)
    section_width = screen_width  # 각 섹션의 화면 크기와 동일하게 설정
    num_sections = scaled_width // section_width  # 전체 섹션 개수
    current_section = 0

    running = True
    while running:
        clear_canvas()

        # 현재 섹션의 시작 위치
        section_start = current_section * section_width

        # 배경 그리기 (현재 섹션만 표시)
        background_image.draw_to_origin(-section_start, 0, scaled_width, screen_height)

        # 맵 데이터 그리기 (현재 섹션의 블럭만 표시)
        map_loader.draw(current_section)

        def reset_to_section_1():
            nonlocal current_section
            current_section = 0

        # 마리오 업데이트
        mario.update(map_loader.get_blocks(current_section), reset_to_section_1)

        # 섹션 이동 처리
        if mario.x >= screen_width:  # 다음 섹션으로 이동
            if current_section < num_sections - 1:  # 마지막 섹션이 아닌 경우
                current_section += 1
                mario.x = 0  # 마리오를 화면 왼쪽으로 이동
            else:  # 마지막 섹션인 경우 끝에서 멈춤
                mario.x = screen_width - 1

        elif mario.x <= 0:  # 이전 섹션으로 이동
            if current_section > 0:  # 첫 섹션이 아닌 경우
                current_section -= 1
                mario.x = screen_width  # 마리오를 화면 오른쪽으로 이동
            else:  # 첫 섹션인 경우 더 왼쪽으로 못 가게 함
                mario.x = 1

        # 마리오 그리기
        mario.draw()
        update_canvas()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
                mario.handle_event(event)

        delay(0.03)

    close_canvas()

if __name__ == '__main__':
    main()
