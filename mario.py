from pico2d import *
from time import time

import map_loader


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
        self.is_respawning = False  # 새로 추가: 죽은 후 리스폰 대기 상태
        self.last_movement_time = time()  # 마지막 움직임 시간을 초기화
        self.sitting = False  # 앉는 상태 여부를 나타내는 변수
        self.on_flag = False  # 깃발을 잡았는지 여부
        self.flag_target_y = 130  # 깃발에서 내려올 목표 Y 좌표
        self.flag_image = None  # 깃발 잡기 이미지
        self.stage_clear_music = None  # 스테이지 클리어 음악
        self.flag_stage_complete = False  # 깃발 동작 완료 여부
        self.walking_after_flag = False  # 깃발 이후 걷기 시작 여부
        self.walk_timer = None  # 깃발 이후 걷기 대기 시간
        # 효과음 로드
        self.small_jump_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_jump-small.wav')
        self.small_jump_sound.set_volume(26)

        self.super_jump_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_jump-super.wav')
        self.super_jump_sound.set_volume(26)

        self.powerup_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_powerup.wav')
        self.powerup_sound.set_volume(32)

        self.stomp_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_stomp.wav')
        self.stomp_sound.set_volume(32)

        self.block_hit_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_coin.wav')
        self.block_hit_sound.set_volume(32)

        self.death_sound = load_music('C:/Githup_2024_2/2DGP-project1/sounds/smb_mariodie.mp3')
        self.death_sound.set_volume(32)

        self.damage_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/mario-damage.wav')
        self.damage_sound.set_volume(16)

        self.coin_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_coin.wav')
        self.coin_sound.set_volume(16)

        self.break_block_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smw_break_block.wav')
        self.break_block_sound.set_volume(50)

    def update(self, blocks, enemies, powerups, coins, reset_to_section_1, map_loader):
        if self.is_dead:
            self.update_death(reset_to_section_1)
            return

        if self.is_respawning:
            return  # 리스폰 대기 상태에서는 업데이트 무시

        if self.on_flag:
            # 깃발 내려오는 동작
            if self.y > self.flag_target_y:
                self.y -= 2  # 천천히 내려오기
            elif not self.flag_stage_complete:
                self.flag_stage_complete = True
                self.walk_timer = time()  # 깃발 동작 완료 시간 기록

            # 깃발에서 내려온 후 3초 대기 후 걷기 시작
            if self.flag_stage_complete and time() - self.walk_timer >= 3:
                if not self.walking_after_flag:
                    # 스테이지 클리어 음악 재생
                    if not self.stage_clear_music:
                        self.stage_clear_music = load_music('C:/Githup_2024_2/2DGP-project1/sounds/smb_stage_clear.mp3')
                        self.stage_clear_music.set_volume(40)
                        self.stage_clear_music.play()

                    self.walking_after_flag = True  # 걷기 시작
                    self.velocity = 2  # 오른쪽으로 걷기 속도 설정

                # 걷기 동작 중 중력 적용
                self.jump_speed -= self.gravity
                self.y += self.jump_speed
                self.jump_speed = max(self.jump_speed, -18)

                # 블록 충돌 처리 (걷는 중에도 블록 위에 설 수 있도록)
                self.on_ground = False
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
                            block.activate(map_loader)
                            self.break_block_sound.play()
                        self.jump_speed = 0
                        self.y = block.y - (40 if self.is_big else 32)
                        break

                    # 낙사 판정 제거
                if not self.on_ground and not self.is_dead:
                    self.y += self.jump_speed
                    self.jump_speed -= self.gravity
                    self.jump_speed = max(self.jump_speed, -18)

                    # 낙사 처리 제거
                if not self.is_dead and self.y < -50:
                    self.handle_death(reset_to_section_1)

                if not self.on_ground:
                    self.is_jumping = True

                # 오른쪽으로 계속 걷기
                if self.x < 8200:  # 8200까지 걷기
                    self.x += self.velocity
                else:
                    self.velocity = 0  # 8200에 도달하면 멈추기
                    self.on_flag = False  # 깃발 동작 종료

                # 걷기 애니메이션 (프레임 업데이트)
                self.state = "walk"
                self.frame = (self.frame + 1) % 3 + 1

            return  # 다른 동작 무시

        # 무적 상태 지속 시간 확인
        if self.is_invincible and time() - self.invincible_start_time > 2:
            self.is_invincible = False

        # 가만히 있는 시간 확인 및 앉는 상태 전환
        if self.velocity == 0 and not self.is_jumping:
            if time() - self.last_movement_time > 3 and not self.sitting:
                self.sitting = True
                if self.is_big:
                    self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/big_mario_sit.png')
                else:
                    self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_sit.png')
        elif self.velocity != 0 or self.is_jumping:
            if self.sitting:
                self.sitting = False
                if self.is_big:
                    self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/big_mario_state.png')
                else:
                    self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')

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
                    block.activate(map_loader)
                    self.break_block_sound.play()
                self.jump_speed = 0
                self.y = block.y - (40 if self.is_big else 32)
                break

        # 블록 위에 있지 않고 공중 상태라면 점프 상태로 전환
        if not self.on_ground:
            self.is_jumping = True

        # 적과의 충돌 처리
        for enemy in enemies:
            collision_result = self.check_enemy_collision(enemy)
            if collision_result == "stomp":
                self.jump_speed = 10
                self.is_jumping = True
                enemy.handle_defeat()
                self.stomp_sound.play()
            elif collision_result == "collision" and not self.is_invincible:  # 적과 충돌 시
                if self.is_big:
                    self.is_big = False
                    self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
                    self.is_invincible = True
                    self.invincible_start_time = time()
                    self.damage_sound.play()  # 배경음악 중단 없이 효과음 재생
                else:
                    self.state = "death"
                    self.is_dead = True
                    self.frame = 5
                    self.jump_speed = 30
                    self.death_sound.play()  # 배경음악 중단 없이 사망음악 재생

        # 파워업 아이템 충돌 처리
        for powerup in powerups:
            if self.check_powerup_collision(powerup):
                self.handle_powerup(powerup)

        # 코인 충돌 처리
        for coin in coins:
            if self.check_coin_collision(coin):
                coin.is_active = False
                self.coin_sound.play()

        # 중력 적용 및 최대 낙하 속도 제한
        if not self.on_ground:
            self.y += self.jump_speed
            self.jump_speed -= self.gravity
            self.jump_speed = max(self.jump_speed, -18)

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
        """마리오가 죽을 때 호출되는 메서드."""
        if self.is_respawning:
            return  # 리스폰 대기 중이면 다시 죽지 않음

        self.state = "death"
        self.is_dead = True
        self.is_respawning = True  # 리스폰 대기 상태로 설정
        self.is_big = False
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/small_mario_state.png')
        self.frame = 5  # 죽는 애니메이션 프레임
        self.jump_speed = 25  # 초기 점프 속도 설정
        self.velocity = 0
        self.death_sound.play()

    def update_death(self, reset_to_section_1):
        """죽는 동안의 동작 처리."""
        if not self.is_dead:
            return

        # 위로 점프한 후 아래로 떨어짐
        self.y += self.jump_speed
        self.jump_speed -= self.gravity

        # 화면 아래로 사라지면 리스폰 처리
        if self.y < -50:
            self.is_dead = False
            self.state = "idle"
            self.frame = 0
            delay(2.0)  # 2초 대기
            self.is_respawning = False  # 리스폰 상태 해제
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

        is_colliding = (
            mario_left < enemy_right
            and mario_right > enemy_left
            and mario_bottom < enemy_top
            and mario_top > enemy_bottom
        )

        if is_colliding and self.is_jumping and mario_bottom < enemy_top:
            return "stomp"

        if is_colliding:
            return "collision"

        return None

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
            self.last_movement_time = time()
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
            self.last_movement_time = time()
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

        if self.on_flag:
            if self.walking_after_flag:
                # 걷기 애니메이션 출력
                frame_width = 17 if not self.is_big else 99 // 5
                self.image.clip_draw(
                    self.frame * frame_width, 0, frame_width, 16 if not self.is_big else 32,
                    self.x, self.y, 34 if not self.is_big else 40, 32 if not self.is_big else 80
                )
            else:
                # 깃발 잡기 이미지 출력
                self.flag_image.draw(self.x, self.y, 34 if not self.is_big else 40, 32 if not self.is_big else 80)
            return

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

    def grab_flag(self, is_big, flag_x, background):
        """깃발을 잡았을 때 호출."""
        self.on_flag = True
        self.velocity = 0  # 이동 중지
        self.state = "flag"  # 상태 전환
        self.x = flag_x  # x 좌표를 깃발의 x로 이동

        # 배경음악 중지
        background.bgm.stop()

        # 깃발 사운드 재생
        self.flagpole_sound = load_wav('C:/Githup_2024_2/2DGP-project1/sounds/effects/smb_flagpole.wav')
        self.flagpole_sound.set_volume(32)
        self.flagpole_sound.play()

        self.flag_image = load_image(
            'C:/Githup_2024_2/2DGP-project1/sprites/big_mario_flag_grab.png' if is_big
            else 'C:/Githup_2024_2/2DGP-project1/sprites/small_mario_flag_grab.png'
        )
