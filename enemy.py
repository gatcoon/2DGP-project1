from pico2d import *

class Enemy:
    def __init__(self, x, y):
        self.initial_x, self.initial_y = x, y  # 초기 위치 저장
        self.x, self.y = x, y
        self.width, self.height = 40, 40
        self.velocity = -2  # 초기 이동 방향 (왼쪽)
        self.frame = 0
        self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/goomba.png')
        self.is_defeated = False  # 적이 패배 상태인지 여부
        self.defeat_timer = 0  # 패배 상태 유지 시간
        self.frame_delay = 0  # 애니메이션 프레임 속도 조절용

    def update(self, blocks):
        # 적이 패배 상태인 경우 처리
        if self.is_defeated:
            self.defeat_timer -= 0.03  # 타이머 감소
            if self.defeat_timer <= 0:
                self.x, self.y = -100, -100  # 화면 밖으로 이동
            return

        # 걷기 애니메이션 (0, 1 프레임 반복) 속도 조절
        self.frame_delay += 0.03
        if self.frame_delay >= 0.15:  # 프레임 변경 간격 증가
            self.frame = (self.frame + 1) % 2
            self.frame_delay = 0

        # 좌우 이동 처리
        self.x += self.velocity

        # 블럭, 파이프와의 충돌 처리
        for block in blocks:
            if block.block_type != "invisible" and self.check_collision(block):
                self.velocity *= -1  # 이동 방향 반전
                self.x += self.velocity  # 충돌 후 약간 이동
                break

        # 화면 경계 충돌 처리 (왼쪽, 오른쪽 끝에 닿을 경우)
        if self.x <= 20:  # 화면 왼쪽 경계
            self.velocity = 2
        elif self.x >= 780:  # 화면 오른쪽 경계
            self.velocity = -2

    def reset(self):
        # 적의 상태를 초기화
        self.x, self.y = self.initial_x, self.initial_y
        self.velocity = -2  # 이동 방향 초기화
        self.is_defeated = False
        self.frame = 0
        self.defeat_timer = 0

    def handle_defeat(self):
        # 적 패배 상태 설정
        self.is_defeated = True
        self.frame = 2  # 패배 프레임
        self.defeat_timer = 1.0  # 1초 동안 유지

    def check_collision(self, block):
        if self.is_defeated:  # 패배 상태에서는 충돌 판정을 하지 않음
            return False

        # 적의 충돌 박스 계산
        enemy_left = self.x - self.width // 2
        enemy_right = self.x + self.width // 2
        enemy_bottom = self.y - self.height // 2
        enemy_top = self.y + self.height // 2

        # 블럭의 충돌 박스 계산
        block_left, block_bottom, block_right, block_top = block.get_collision_box(0)

        # 충돌 여부 확인
        return (
            enemy_left < block_right
            and enemy_right > block_left
            and enemy_bottom < block_top
            and enemy_top > block_bottom
        )

    def get_collision_box(self):
        # 적이 패배 상태인 경우 충돌 박스 제거
        if self.is_defeated:
            return -100, -100, -100, -100  # 충돌하지 않도록 설정

        # 적의 충돌 박스 반환
        enemy_left = self.x - self.width // 2
        enemy_bottom = self.y - self.height // 2
        enemy_right = self.x + self.width // 2
        enemy_top = self.y + self.height // 2
        return enemy_left, enemy_bottom, enemy_right, enemy_top

    def draw(self, camera_left):
        # 패배 상태에서는 2번 프레임 고정, 걷는 상태에서는 0, 1번 프레임 반복
        self.image.clip_draw(
            (2 if self.is_defeated else self.frame) * (self.image.w // 3), 0,
            self.image.w // 3, self.image.h,
            self.x - camera_left, self.y,
            self.width, self.height
        )