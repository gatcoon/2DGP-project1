from pico2d import draw_rectangle, SDLK_RIGHT, SDLK_LEFT

class Idle:
    @staticmethod
    def enter(mario, event):
        mario.frame = 0

    @staticmethod
    def exit(mario, event):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % 3
        mario.x += mario.velocity  # Idle 상태에서도 좌우 이동 가능

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(mario.frame * 40, 0, 40, 32, mario.x, mario.y)
        draw_rectangle(*mario.get_bb())


class Walk:
    @staticmethod
    def enter(mario, event):
        pass

    @staticmethod
    def exit(mario, event):
        pass

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % 3
        mario.x += mario.velocity  # Walk 상태에서도 지속 이동

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(mario.frame * 40, 0, 40, 32, mario.x, mario.y)
        draw_rectangle(*mario.get_bb())


class Jump:
    @staticmethod
    def enter(mario, event):
        if not mario.is_jumping:  # 점프 중이 아닐 때만 점프 시작
            mario.jump_speed = 10
            mario.is_jumping = True

    @staticmethod
    def exit(mario, event):
        pass

    @staticmethod
    def do(mario):
        mario.x += mario.velocity  # 점프 중에도 좌우 이동 유지
        mario.y += mario.jump_speed
        mario.jump_speed -= mario.gravity

        # 착지 처리
        if mario.y <= mario.ground_level:
            mario.y = mario.ground_level
            mario.is_jumping = False  # 점프 종료
            mario.state_machine.add_event(('LAND', None))

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(mario.frame * 40, 0, 40, 32, mario.x, mario.y)
        draw_rectangle(*mario.get_bb())
