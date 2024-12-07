from pico2d import *

class Coin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width, self.height = 20, 20
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/coin.png')
        self.frame = 0
        self.frame_count = 4  # 총 4개의 프레임
        self.frame_delay = 0
        self.is_active = True

    def update(self):
        if not self.is_active:
            return
        self.frame_delay += 0.05
        if self.frame_delay >= 0.1:  # 프레임 전환 속도 조절
            self.frame = (self.frame + 1) % self.frame_count
            self.frame_delay = 0

    def draw(self, camera_left):
        if self.is_active and self.image:
            frame_width = self.image.w // self.frame_count
            self.image.clip_draw(
                self.frame * frame_width, 0, frame_width, self.image.h,
                self.x - camera_left, self.y, self.width, self.height
            )

    def get_collision_box(self):
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )
