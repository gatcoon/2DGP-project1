from pico2d import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x, self.y = x, y
        self.width, self.height = 40, 40  # 크기 설정
        self.powerup_type = powerup_type
        self.image = self.load_image()
        self.is_active = True  # 아이템 활성화 상태

    def load_image(self):
        if self.powerup_type == "mushroom":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/mushroom.png')
        return None

    def draw(self, camera_left):
        if self.is_active and self.image:
            self.image.draw(self.x - camera_left, self.y, self.width, self.height)  # 크기를 40x40으로 설정

    def get_collision_box(self):
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )
