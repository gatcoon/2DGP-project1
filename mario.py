from pico2d import *
from time import time


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
        self.is_big = False
        self.is_invincible = False
        self.invincible_start_time = 0
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
        self.on_ground = False
        self.running = False
        self.is_dead = False

        # 효과음 로드
        self.small_jump_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_jump-small.wav')
        self.small_jump_sound.set_volume(32)

        self.super_jump_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_jump-super.wav')
        self.super_jump_sound.set_volume(32)

        self.powerup_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_powerup.wav')
        self.powerup_sound.set_volume(32)

        self.stomp_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_stomp.wav')
        self.stomp_sound.set_volume(32)

        self.block_hit_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_coin.wav')
        self.block_hit_sound.set_volume(32)

        self.death_sound = load_music('C:/Githup_2024_2/2DGP-project1/sounds/smb_mariodie.mp3')
        self.death_sound.set_volume(32)

        self.damage_sound = load_music('C:/Githup_2024_2/2DGP-project1/sounds/effects/mario-damage.mp3')
        self.damage_sound.set_volume(16)

        self.coin_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_coin.wav')
        self.coin_sound.set_volume(16)

    def update(self, blocks, enemies, powerups, coins, reset_to_section_1):
        if self.is_dead:
            self.handle_death(reset_to_section_1)
            return

        # 무적 상태 지속 시간 확인
        if self.is_invincible and time() - self.invincible_start_time > 2:
            self.is_invincible = False

        # 이동 처리
        move_speed = 1.4 if not self.running else 2.5
        self.x += self.velocity * move_speed

        # 상태 업데이트 및 프레임 설정
        if self.is_jumping:
            self.state = "jump"
            self.frame = 4
        elif self.velocity != 0:
            self.state = "walk"
            self.frame = (self.frame + 1) % 3 + 1
        else:
            self.state = "idle"
            self.frame = 0

        # 중력 및 충돌 처리
        self.on_ground = False
        next_y = self.y + self.jump_speed

        for block in blocks:
            collision_side = self.check_collision(block, next_y)
            if collision_side == "top":
                self.on_ground = True
                self.is_jumping = False
                self.jump_speed = 0
                self.y = block.y + block.height + (25 if self.is_big else 0)
                break
            elif collision_side == "bottom":
                if block.block_type in ["block", "question_block"] and not block.is_activated:
                    block.activate()
                    self.block_hit_sound.play()  # 블럭 히트 소리 재생
                self.jump_speed = 0
                self.y = block.y - (40 if self.is_big else 32)
                break

        # 적과의 충돌 처리
        for enemy in enemies:
            if self.check_enemy_collision(enemy):
                if self.jump_speed < 0:  # 적을 밟을 때
                    self.jump_speed = 10
                    enemy.handle_defeat()
                    self.stomp_sound.play()  # 적을 밟을 때 소리 재생
                elif not self.is_invincible:  # 무적 상태가 아닐 때만 데미지 처리
                    if self.is_big:
                        self.is_big = False
                        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
                        self.is_invincible = True
                        self.invincible_start_time = time()
                        self.damage_sound.play()  # 데미지 소리 재생
                    else:
                        self.state = "death"
                        self.is_dead = True
                        self.frame = 5
                        self.jump_speed = 30
                        self.death_sound.play()  # 사망 시 음악 재생
                        break

        # 파워업 아이템 충돌 처리
        for powerup in powerups:
            if self.check_powerup_collision(powerup):
                self.handle_powerup(powerup)

        # 코인 충돌 처리
        for coin in coins:
            if self.check_coin_collision(coin):
                coin.is_active = False
                self.coin_sound.play()

        # 중력 적용
        if not self.on_ground:
            self.y += self.jump_speed
            self.jump_speed -= self.gravity

        # 낙사 처리
        if self.y < -50:
            self.state = "death"
            self.is_dead = True
            self.is_big = False
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
            self.frame = 5
            self.jump_speed = 30
            self.death_sound.play()

    def handle_powerup(self, powerup):
        if powerup.powerup_type == "mushroom":
            self.is_big = True
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/big_mario_state.png')
            powerup.is_active = False
            self.powerup_sound.play()
            

    def handle_death(self, reset_to_section_1):
        self.y += self.jump_speed
        self.jump_speed -= self.gravity

        if self.y < -100:
            self.reset_position()
            delay(2.0)
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

        return (
            mario_left < enemy_right
            and mario_right > enemy_left
            and mario_bottom < enemy_top
            and mario_top > enemy_bottom
        )

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

    def check_coin_collision(self, coin):
        if not coin.is_active:
            return False

        mario_left = self.x - (15 if not self.is_big else 20)
        mario_right = self.x + (15 if not self.is_big else 20)
        mario_bottom = self.y - (16 if not self.is_big else 40)
        mario_top = self.y + (16 if not self.is_big else 40)

        coin_left, coin_bottom, coin_right, coin_top = coin.get_collision_box()

        return (
            mario_left < coin_right
            and mario_right > coin_left
            and mario_bottom < coin_top
            and mario_top > coin_bottom
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
                if self.is_big:
                    self.super_jump_sound.play()
                else:
                    self.small_jump_sound.play()
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
