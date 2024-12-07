from pico2d import *

from powerup import PowerUp


class Block:
    def __init__(self, x, y, width, height, block_type, section_index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_type = block_type
        self.initial_type = block_type  # 초기 타입 저장
        self.image = self.load_image()
        self.is_activated = False  # 블록이 활성화되었는지 여부
        self.contains_powerup = self.block_type == "question_block"  # 특정 블럭만 파워업 포함
        self.section_index = section_index  # 블럭이 속한 섹션 정보 저장

    def load_image(self):
        """블록 타입에 따른 이미지를 로드."""
        if self.block_type == "block":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/block.png')
        elif self.block_type == "question_block":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/question_block.png')
        elif self.block_type == "solid":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/solid_block.png')
        return None

    def activate(self, map_loader):
        """블록이 활성화되었을 때 호출."""
        if not self.is_activated and self.block_type in ["block", "question_block"]:
            self.is_activated = True
            self.block_type = "solid"  # 타입을 solid로 변경
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/solid_block.png')  # 이미지 변경

            # 파워업 생성 로직
            if self.contains_powerup:
                powerup_x = self.x + self.width // 2  # 블럭 중앙
                powerup_y = self.y + self.height + 20  # 블럭 위 20 위치
                powerup = PowerUp(powerup_x, powerup_y, "mushroom")
                map_loader.add_powerup(powerup, self.section_index)

    def reset(self):
        """블록을 초기 상태로 복구."""
        self.block_type = self.initial_type  # 초기 타입으로 복원
        self.is_activated = False
        self.image = self.load_image()  # 원래 이미지로 복원

    def draw(self, camera_left):
        """블록을 화면에 그리기."""
        if self.image:
            self.image.draw(self.x + 20, self.y + 10, self.width, self.height)

    def get_collision_box(self, camera_left):
        """충돌 박스 반환."""
        block_left = self.x - camera_left
        block_bottom = self.y
        block_right = block_left + self.width
        block_top = block_bottom + self.height
        return block_left, block_bottom, block_right, block_top
