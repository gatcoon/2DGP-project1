from pico2d import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40  # 몬스터 표시 크기
        self.height = 40
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/goomba.png')
        self.frame = 0  # 첫 번째 프레임 유지
        self.velocity = -1  # 이동 방향 (왼쪽)
        self.image_frame_width = self.image.w // 3  # 이미지 프레임 가로 크기
        self.image_frame_height = self.image.h  # 이미지 프레임 세로 크기

    def update(self, blocks):
        # 이동
        self.x += self.velocity

        # 충돌 처리
        for block in blocks:
            if self.check_collision(block):
                self.velocity *= -1  # 이동 방향 반전
                break

    def check_collision(self, block):
        # Enemy의 충돌 박스
        enemy_left = self.x - self.width // 2
        enemy_right = self.x + self.width // 2
        enemy_bottom = self.y - self.height // 2
        enemy_top = self.y + self.height // 2

        # 블럭의 충돌 박스
        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

        # 충돌 여부 확인
        return (
            enemy_left < block_right and
            enemy_right > block_left and
            enemy_bottom < block_top and
            enemy_top > block_bottom
        )

    def draw(self, camera_left):
        # 40x40 크기로 이미지의 첫 번째 프레임을 표시
        self.image.clip_draw(
            self.frame * self.image_frame_width, 0,
            self.image_frame_width, self.image_frame_height,
            self.x - camera_left, self.y,
            self.width, self.height  # 그릴 크기를 40x40으로 설정
        )
