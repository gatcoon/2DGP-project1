from pico2d import *
from time import time  # 시간 측정을 위해 사용

class Mario:
    def __init__(self):
        # 초기 설정
        self.x, self.y = 300, 100
        self.velocity = 0
        self.jump_speed = 0
        self.is_jumping = False
        self.gravity = 1.8
        self.frame = 0
        self.facing_direction = 1
        self.state = "idle"  # 상태: "idle", "walk", "jump", "death"
        self.is_big = False  # 파워업 상태를 나타내는 플래그
        self.is_invincible = False  # 무적 상태 여부
        self.invincible_start_time = 0  # 무적 상태 시작 시간
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')  # 작은 마리오 기본 스프라이트
        self.on_ground = False
        self.running = False
        self.is_dead = False

    def update(self, blocks, enemies, powerups, reset_to_section_1):
        if self.is_dead:
            self.handle_death(reset_to_section_1)  # 사망 처리
            return

        # 무적 상태 지속 시간 확인
        if self.is_invincible and time() - self.invincible_start_time > 2:
            self.is_invincible = False  # 무적 상태 해제

        # 이동 처리
        move_speed = 1.4 if not self.running else 2.5  # 걷기/달리기 속도
        self.x += self.velocity * move_speed

        # 상태 업데이트 및 프레임 설정
        if self.is_jumping:  # 점프 상태
            self.state = "jump"
            self.frame = 4  # 점프 프레임
        elif self.velocity != 0:  # 걷기 상태
            self.state = "walk"
            self.frame = (self.frame + 1) % 3 + 1  # 걷기 애니메이션: 1, 2, 3
        else:  # 대기 상태
            self.state = "idle"
            self.frame = 0  # 대기 프레임

        # 중력 및 충돌 처리
        self.on_ground = False
        next_y = self.y + self.jump_speed

        for block in blocks:
            collision_side = self.check_collision(block, next_y)
            if collision_side == "top":  # 블록 위에 닿음
                self.on_ground = True
                self.is_jumping = False
                self.jump_speed = 0
                self.y = block.y + block.height + (25 if self.is_big else 0)  # 큰 마리오는 더 높게 위치
                break
            elif collision_side == "bottom":  # 블록 아래에 닿음
                self.jump_speed = 0
                self.y = block.y - (40 if self.is_big else 32)  # 높이에 맞게 위치 조정
                break

        # 적과의 충돌 처리
        for enemy in enemies:
            if self.check_enemy_collision(enemy):  # 적과의 충돌 감지
                if self.is_invincible:
                    continue  # 무적 상태에서는 데미지 무시
                if self.jump_speed < 0:  # 떨어지면서 적을 밟을 경우
                    self.jump_speed = 10  # 튕겨 오름
                    enemy.handle_defeat()  # 적 제거 처리
                else:  # 적에게 데미지를 입음
                    if self.is_big:  # 큰 마리오 상태일 경우
                        self.is_big = False
                        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
                        self.is_invincible = True  # 무적 상태로 전환
                        self.invincible_start_time = time()  # 무적 상태 시작 시간 기록
                    else:  # 작은 마리오일 경우 사망
                        self.state = "death"
                        self.is_dead = True
                        self.frame = 5  # 사망 프레임
                        self.jump_speed = 30
                        break

        # 파워업 아이템 충돌 처리
        for powerup in powerups:
            if self.check_powerup_collision(powerup):  # 아이템 충돌 감지
                self.handle_powerup(powerup)

        # 중력 적용
        if not self.on_ground:
            self.y += self.jump_speed
            self.jump_speed -= self.gravity

        # 낙사 처리
        if self.y < -50:
            self.state = "death"
            self.is_dead = True
            self.is_big = False  # 낙사 시 항상 작은 마리오로 변경
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
            self.frame = 5
            self.jump_speed = 30

    def handle_powerup(self, powerup):
        if powerup.powerup_type == "mushroom":  # 버섯 아이템 처리
            self.is_big = True
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/big_mario_state.png')
            powerup.is_active = False  # 아이템 비활성화

    def handle_death(self, reset_to_section_1):
        self.y += self.jump_speed
        self.jump_speed -= self.gravity

        if self.y < -100:
            self.reset_position()
            delay(0.5)
            reset_to_section_1()

    def check_collision(self, block, next_y):
        mario_width = 15 if not self.is_big else 18
        mario_height = 16 if not self.is_big else 32

        mario_left = self.x - mario_width
        mario_right = self.x + mario_width
        mario_bottom = next_y - mario_height
        mario_top = next_y + mario_height

        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

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

    def check_enemy_collision(self, enemy):
        mario_left = self.x - (15 if not self.is_big else 20)
        mario_right = self.x + (15 if not self.is_big else 20)
        mario_bottom = self.y - (16 if not self.is_big else 40)
        mario_top = self.y + (16 if not self.is_big else 40)

        enemy_left, enemy_bottom, enemy_right, enemy_top = enemy.get_collision_box()

        current_collision = (
            mario_left < enemy_right
            and mario_right > enemy_left
            and mario_bottom < enemy_top
            and mario_top > enemy_bottom
        )

        previous_bottom = self.y + self.jump_speed - (16 if not self.is_big else 40)
        previous_top = self.y + self.jump_speed + (16 if not self.is_big else 40)

        previous_collision = (
            mario_left < enemy_right
            and mario_right > enemy_left
            and previous_bottom < enemy_top
            and previous_top > enemy_bottom
        )

        return current_collision or previous_collision

    def check_powerup_collision(self, powerup):
        if not powerup.is_active:
            return False

        mario_left = self.x - (15 if not self.is_big else 20)
        mario_right = self.x + (15 if not self.is_big else 20)
        mario_bottom = self.y - (16 if not self.is_big else 40)
        mario_top = self.y + (16 if not self.is_big else 40)

        powerup_left, powerup_bottom, powerup_right, powerup_top = powerup.get_collision_box()

        return (
            mario_left < powerup_right
            and mario_right > powerup_left
            and mario_bottom < powerup_top
            and mario_top > powerup_bottom
        )

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
            elif event.key == SDLK_z:
                self.running = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT and self.velocity > 0:
                self.velocity = 0
            elif event.key == SDLK_LEFT and self.velocity < 0:
                self.velocity = 0
            elif event.key == SDLK_z:
                self.running = False

    def draw(self):
        frame_width_small = 17
        frame_width_big = 99 // 5
        output_width = 34 if not self.is_big else 40
        output_height = 32 if not self.is_big else 80
        frame_width = frame_width_small if not self.is_big else frame_width_big

        if self.is_invincible and int(time() * 10) % 2 == 0:
            return

        if self.facing_direction == 1:
            self.image.clip_draw(
                self.frame * frame_width, 0, frame_width, 16 if not self.is_big else 32,
                self.x, self.y, output_width, output_height
            )
        else:
            self.image.clip_composite_draw(
                self.frame * frame_width, 0, frame_width, 16 if not self.is_big else 32,
                0, 'h', self.x, self.y, output_width, output_height
            )
