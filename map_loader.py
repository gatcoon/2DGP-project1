from block import Block
from map_data import map_data

class MapLoader:
    def __init__(self):
        self.sections = []  # 각 섹션에 대한 블럭 리스트
        self.load_map()

    def load_map(self):
        # 블럭 데이터를 섹션별로 분리
        section_width = 800  # 각 섹션의 너비
        num_sections = max(data["x"] // section_width for data in map_data) + 1

        for section in range(num_sections):
            self.sections.append([
                Block(data["x"] % section_width, data["y"], data["width"], data["height"], data["type"])
                for data in map_data if data["x"] // section_width == section
            ])

    def draw(self, section):
        if 0 <= section < len(self.sections):
            for block in self.sections[section]:
                block.draw(0)  # 화면 고정, 카메라 이동 없음

    def get_blocks(self, section):
        return self.sections[section] if 0 <= section < len(self.sections) else []
