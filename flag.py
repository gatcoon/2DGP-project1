from pico2d import *

class Flag:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.is_active = True  # 깃발이 활성 상태인지 여부

    def draw(self, camera_left):
        pass

    def get_collision_box(self):
        """깃발의 충돌 박스 반환."""
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y,
            self.x + self.width // 2,
            self.y + self.height
        )
