from pico2d import *

class Mario:
    def __init__(self):
        self.x, self.y = 300, 100
        self.velocity = 0
        self.jump_speed = 0
        self.is_jumping = False
        self.gravity = 1.8
        self.frame = 0
        self.facing_direction = 1
        self.state = "idle"
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
        self.on_ground = False
        self.running = False  # 달리기 상태 추가
        self.is_dead = False  # 죽음 상태

    def update(self, blocks, reset_to_section_1):
        if self.is_dead:
            self.handle_death(reset_to_section_1)
            return

        # 이동 처리
        move_speed = 1.4 if not self.running else 2.5  # 달리기 상태에서 이동 속도 증가
        self.x += self.velocity * move_speed

        # 상태 업데이트
        if self.is_jumping:
            self.state = "jump"
        elif self.velocity != 0:
            self.state = "run" if self.running else "walk"
        else:
            self.state = "idle"

        # 애니메이션 프레임 업데이트
        if self.state == "walk" or self.state == "run":
            self.frame = (self.frame + 1) % 4
        elif self.state == "idle":
            self.frame = 0
        elif self.state == "jump":
            self.frame = 5

        # 중력 및 충돌 처리
        self.on_ground = False
        next_y = self.y + self.jump_speed

        for block in blocks:
            collision_side = self.check_collision(block, next_y)
            if collision_side == "top":  # 블럭 위에 올라갔을 때
                self.on_ground = True
                self.is_jumping = False
                self.jump_speed = 0
                self.y = block.y + block.height
                break
            elif collision_side == "bottom":  # 점프 중 블럭 하단에 닿을 때
                self.jump_speed = 0
                self.y = block.y - 32
                break

        if not self.on_ground:
            self.y += self.jump_speed
            self.jump_speed -= self.gravity

        # 화면 아래로 떨어지면 죽음 상태로 전환
        if self.y < -50:
            self.state = "death"
            self.is_dead = True
            self.frame = 6
            self.jump_speed = 30  # 죽을 때 점프 속도

    def handle_death(self, reset_to_section_1):
        self.y += self.jump_speed
        self.jump_speed -= self.gravity

        if self.y < -100:  # 마리오가 충분히 떨어졌을 때 초기화
            self.reset_position()
            delay(0.5)
            reset_to_section_1()

    def check_collision(self, block, next_y):
        # Mario의 충돌 박스 계산
        mario_left = self.x - 15
        mario_right = self.x + 15
        mario_bottom = next_y - 16
        mario_top = next_y + 16

        # 블럭의 충돌 박스 계산
        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

        # 충돌 여부 확인
        if (
            mario_left < block_right
            and mario_right > block_left
            and mario_bottom < block_top
            and mario_top > block_bottom
        ):
            if mario_bottom < block_top and self.jump_speed > 0:
                return "bottom"
            elif mario_top > block_bottom and self.jump_speed <= 0:
                return "top"
        return None

    def reset_position(self):
        self.x, self.y = 300, 100
        self.velocity = 0
        self.jump_speed = 0
        self.is_jumping = False
        self.is_dead = False
        self.state = "idle"

    def handle_event(self, event):
        if self.is_dead:
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.velocity = 4
                self.facing_direction = 1
            elif event.key == SDLK_LEFT:
                self.velocity = -4
                self.facing_direction = -1
            elif event.key == SDLK_UP and not self.is_jumping and self.on_ground:
                self.is_jumping = True
                self.jump_speed = 25
                self.on_ground = False
            elif event.key == SDLK_z:  # 달리기 키 누름
                self.running = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT and self.velocity > 0:
                self.velocity = 0
            elif event.key == SDLK_LEFT and self.velocity < 0:
                self.velocity = 0
            elif event.key == SDLK_z:  # 달리기 키 뗌
                self.running = False

    def draw(self):
        if self.facing_direction == 1:
            self.image.clip_draw(self.frame * 38, 0, 38, 32, self.x, self.y)
        else:
            self.image.clip_composite_draw(
                self.frame * 38, 0, 38, 32, 0, 'h', self.x, self.y, 38, 32
            )
