from block import Block
from enemy import Enemy
from map_data import map_data

class MapLoader:
    def __init__(self):
        self.sections = []  # 각 섹션에 대한 블럭 리스트
        self.enemies = []   # 적 객체 리스트
        self.load_map()

    def load_map(self):
        # 블럭 데이터를 섹션별로 분리
        section_width = 800  # 각 섹션의 너비
        num_sections = max(data["x"] // section_width for data in map_data) + 1

        # 섹션 초기화
        for section in range(num_sections):
            self.sections.append([])
            self.enemies.append([])

        for data in map_data:
            section_index = data["x"] // section_width
            if data["type"] in ["block", "question_block", "pipe", "invisible"]:
                block = Block(data["x"] % section_width, data["y"], data["width"], data["height"], data["type"])
                self.sections[section_index].append(block)
            elif data["type"] == "enemy":
                enemy = Enemy(data["x"] % section_width, data["y"])
                self.enemies[section_index].append(enemy)

    def draw(self, section):
        if 0 <= section < len(self.sections):
            for block in self.sections[section]:
                block.draw(0)  # 화면 고정, 카메라 이동 없음
            for enemy in self.enemies[section]:
                enemy.draw(0)  # 화면 고정, 카메라 이동 없음

    def get_blocks(self, section):
        return self.sections[section] if 0 <= section < len(self.sections) else []

    def get_enemies(self, section):
        return self.enemies[section] if 0 <= section < len(self.enemies) else []

    def update(self, section, screen_width):
        if 0 <= section < len(self.sections):
            for enemy in self.enemies[section]:
                enemy.update(self.sections[section], screen_width)
