from pico2d import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x, self.y = x, y
        self.width, self.height = 30, 30  # 크기 설정
        self.powerup_type = powerup_type
        self.image = self.load_image()
        self.is_active = True  # 아이템 활성화 상태
        self.velocity_x = 2  # 좌우 이동 속도
        self.velocity_y = 0  # 초기 수직 속도
        self.gravity = 1.0  # 중력 가속도
        self.screen_width = 800  # 화면 너비 (필요에 따라 조정)

    def load_image(self):
        if self.powerup_type == "mushroom":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/mushroom.png')
        return None

    def update(self, blocks):
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

        # 맵 경계 충돌 처리 (화면 경계를 넘지 않도록)
        self.handle_screen_boundary()

    def handle_collisions(self, blocks, next_x, next_y):
        for block in blocks:
            collision_side = self.check_collision(block, next_x, next_y)
            if collision_side == "top":
                self.velocity_y = 0
                self.y = block.y + block.height + 1  # 블록 위에 위치
            elif collision_side == "bottom":
                self.velocity_y = 0
                self.y = block.y - self.height - 1
            elif collision_side in ("left", "right"):
                if block.block_type == "pipe" or block.block_type == "block":
                    self.velocity_x *= -1  # 방향 전환
                break

    def handle_screen_boundary(self):
        if self.x <= 0:  # 왼쪽 경계
            self.x = 1
            self.velocity_x = abs(self.velocity_x)  # 오른쪽으로 방향 전환
        elif self.x >= self.screen_width - self.width:  # 오른쪽 경계
            self.x = self.screen_width - self.width - 1
            self.velocity_x = -abs(self.velocity_x)  # 왼쪽으로 방향 전환

    def check_collision(self, block, next_x, next_y):
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
        if self.is_active and self.image:
            self.image.draw(self.x - camera_left, self.y, self.width, self.height)

    def get_collision_box(self):
        if not self.is_active:
            return -100, -100, -100, -100
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2,
        )
