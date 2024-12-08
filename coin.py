from pico2d import *

from utils import resource_path


class Coin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 30, 40  # 크기 조정
        self.image = load_image(resource_path('sprites/coin.png'))
        self.frame = 0
        self.frame_count = 4  # 총 4개의 프레임
        self.frame_delay = 0
        self.is_active = True

    def update(self):
        """프레임 애니메이션 업데이트."""
        if not self.is_active:
            return
        self.frame_delay += 0.05
        if self.frame_delay >= 0.2:  # 프레임 전환 속도 (0.1초마다 전환)
            self.frame = (self.frame + 1) % self.frame_count
            self.frame_delay = 0  # 딜레이 초기화

    def draw(self, camera_left):
        """동전을 화면에 그리기."""
        if self.is_active and self.image:
            frame_width = self.image.w // self.frame_count  # 이미지의 가로를 프레임 개수로 나눔
            self.image.clip_draw(
                self.frame * frame_width, 0, frame_width, self.image.h,  # 현재 프레임만 잘라서 그리기
                self.x - camera_left, self.y, self.width, self.height
            )

    def get_collision_box(self):
        """충돌 박스 계산."""
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )
