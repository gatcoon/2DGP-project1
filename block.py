from pico2d import *

class Block:
    def __init__(self, x, y, width, height, block_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_type = block_type
        self.image = self.load_image()
        self.is_activated = False  # 블록이 활성화되었는지 여부

    def load_image(self):
        if self.block_type == "block":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/block.png')
        elif self.block_type == "question_block":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/question_block.png')
        elif self.block_type == "solid":
            return load_image('C:/Githup_2024_2/2DGP-project1/sprites/solid_block.png')
        else:
            return None

    def activate(self):
        # 블록이 활성화될 때 이미지를 변경
        if not self.is_activated:
            self.is_activated = True
            self.image = load_image('C:/Githup_2024_2/2DGP-project1/sprites/solid_block.png')

    def draw(self, camera_left):
        if self.image:
            self.image.draw(self.x + 20, self.y + 10, self.width, self.height)

    def get_collision_box(self, camera_left):
        block_left = self.x
        block_bottom = self.y
        block_right = block_left + self.width
        block_top = block_bottom + self.height
        return block_left, block_bottom, block_right, block_top
