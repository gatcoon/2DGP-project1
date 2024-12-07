from pico2d import *


class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x, self.y = x, y
        self.initial_x, self.initial_y = x, y  # 초기 위치 저장
        self.width, self.height = 40, 40  # 버섯 크기
        self.powerup_type = powerup_type
        self.image = self.load_image()
        self.is_active = True
        self.velocity_x = 2  # 좌우 이동 속도
        self.velocity_y = 0  # 초기 수직 속도
        self.gravity = 1.0  # 중력 가속도
        self.screen_width = 800  # 화면 너비


    def load_image(self):
        """파워업 타입에 따른 이미지 로드."""
        if self.powerup_type == "mushroom":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/mushroom.png')
        return None

    def update(self, blocks):
        """파워업의 물리적 동작 및 충돌 처리."""
        if not self.is_active:
            return

        # 중력 적용
        self.velocity_y -= self.gravity
        next_y = self.y + self.velocity_y

        # 수평 이동
        next_x = self.x + self.velocity_x

        # 충돌 처리
        self.handle_collisions(blocks, next_x, next_y)

        # 위치 업데이트
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 화면 경계 처리
        self.handle_screen_boundary()

    def handle_collisions(self, blocks, next_x, next_y):
        for block in blocks:
            collision_side = self.check_collision(block, next_x, next_y)
            if collision_side == "top":
                self.velocity_y = 0
                self.y = block.y + block.height + 1
            elif collision_side == "bottom":
                self.velocity_y = 0
                self.y = block.y - self.height - 1
            elif collision_side in ("left", "right"):
                self.velocity_x *= -1  # 방향 전환
                break

    def handle_screen_boundary(self):
        """화면 경계 충돌 처리."""
        if self.x <= 0:
            self.x = 1
            self.velocity_x = abs(self.velocity_x)
        elif self.x >= self.screen_width - self.width:
            self.x = self.screen_width - self.width - 1
            self.velocity_x = -abs(self.velocity_x)

    def check_collision(self, block, next_x, next_y):
        """블록과의 충돌 확인."""
        powerup_left = next_x - self.width // 2
        powerup_right = next_x + self.width // 2
        powerup_bottom = next_y - self.height // 2
        powerup_top = next_y + self.height // 2

        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

        if (
            powerup_left < block_right
            and powerup_right > block_left
            and powerup_bottom < block_top
            and powerup_top > block_bottom
        ):
            if powerup_bottom < block_top and self.velocity_y > 0:
                return "bottom"
            elif powerup_top > block_bottom and self.velocity_y <= 0:
                return "top"
            elif powerup_left < block_right and self.velocity_x > 0:
                return "left"
            elif powerup_right > block_left and self.velocity_x < 0:
                return "right"
        return None

    def draw(self, camera_left):
        """파워업을 화면에 그리기."""
        if self.is_active and self.image:
            self.image.draw(self.x - camera_left, self.y, self.width, self.height)

    def get_collision_box(self):
        """파워업 충돌 박스 반환."""
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )