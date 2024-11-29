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

        for section in range(num_sections):
            section_blocks = []
            for data in map_data:
                if data["x"] // section_width == section:
                    # 누락된 width와 height 처리
                    width = data.get("width", 40)   # 기본값: 40
                    height = data.get("height", 40) # 기본값: 40

                    if data["type"] == "enemy":
                        # 적 객체 추가
                        self.enemies.append(Enemy(data["x"], data["y"]))
                    else:
                        # 블럭 추가
                        section_blocks.append(Block(data["x"] % section_width, data["y"], width, height, data["type"]))
            self.sections.append(section_blocks)

    def draw(self, section, camera_left=0):
        if 0 <= section < len(self.sections):
            for block in self.sections[section]:
                block.draw(camera_left)  # 블럭 그리기

        # 모든 적 그리기
        for enemy in self.enemies:
            enemy.draw(camera_left)  # camera_left를 인자로 전달

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.get_all_blocks())  # 적과의 충돌 체크

    def get_blocks(self, section):
        return self.sections[section] if 0 <= section < len(self.sections) else []

    def get_all_blocks(self):
        # 모든 섹션의 블럭 합치기
        all_blocks = []
        for section in self.sections:
            all_blocks.extend(section)
        return all_blocks
