from pico2d import *

class Block:
    def __init__(self, x, y, width, height, block_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_type = block_type
        self.image = self.load_image()

    def load_image(self):
        if self.block_type == "block":
            return load_image('C:/Githup_2024_2/Drill/project_1/sprites/block.png')
        elif self.block_type == "question_block":
            return load_image('C:/Githup_2024_2/Drill/project_1/sprites/question_block.png')
        elif self.block_type == "pipe":
            return load_image('C:/Githup_2024_2/Drill/project_1/sprites/pipe.png')
        else:
            return None

    def draw(self, camera_left):
        # 이미지 표시 생략 (숨김)
        # if self.image:
        #     self.image.draw_to_origin(self.x - camera_left * 2.5, self.y, self.width, self.height)

        # 충돌 박스 시각화 (y축으로 10 픽셀 아래에 표시)
        block_left, block_bottom, block_right, block_top = self.get_collision_box(camera_left)
        adjusted_bottom = block_bottom - 10  # 사각형을 아래로 10 픽셀 이동
        adjusted_top = block_top - 10       # 사각형을 아래로 10 픽셀 이동
        draw_rectangle(block_left, adjusted_bottom, block_right, adjusted_top)

    def get_collision_box(self, camera_left):
        # 실제 충돌 박스 계산 (위치 변경 없음)
        block_left = self.x - camera_left * 2.5
        block_bottom = self.y
        block_right = block_left + self.width
        block_top = block_bottom + self.height
        return block_left, block_bottom, block_right, block_top
