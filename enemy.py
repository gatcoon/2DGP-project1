from pico2d import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40  # 몬스터 표시 크기
        self.height = 40
        self.velocity = 2
        self.direction = -1  # -1: 왼쪽, 1: 오른쪽
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/goomba.png')
        self.image_frame_width = self.image.w // 3  # 이미지 프레임 가로 크기
        self.image_frame_height = self.image.h  # 이미지 프레임 세로 크기
        self.frame = 0
        self.animation_speed = 0.1  # 애니메이션 속도 조절
        self.animation_timer = 0

    def update(self, blocks, screen_width):
        # 몬스터 이동
        self.x += self.velocity * self.direction

        # 화면 가장자리에서 방향 전환
        if self.x <= 0 or self.x + self.width >= screen_width:
            self.direction *= -1

        # 충돌 감지 (블럭 및 파이프)
        for block in blocks:
            if self.check_collision(block):
                self.direction *= -1  # 이동 방향 반전
                break

        # 애니메이션 업데이트
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % 2  # 0, 1 프레임 반복

    def check_collision(self, block):
        enemy_left = self.x
        enemy_right = self.x + self.width
        enemy_bottom = self.y
        enemy_top = self.y + self.height

        # 블럭의 충돌 박스
        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

        # 충돌 여부 확인
        return (
            enemy_right > block_left
            and enemy_left < block_right
            and enemy_bottom < block_top
            and enemy_top > block_bottom
        )

    def draw(self, camera_left):
        # 40x40 크기로 이미지의 첫 번째 프레임을 표시
        self.image.clip_draw(
            self.frame * self.image_frame_width, 0,
            self.image_frame_width, self.image_frame_height,
            self.x - camera_left, self.y,
            self.width, self.height  # 크기를 40x40으로 설정
        )
