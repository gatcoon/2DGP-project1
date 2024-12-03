from block import Block
from enemy import Enemy
from powerup import PowerUp
from map_data import map_data

class MapLoader:
    def __init__(self):
        self.sections = []  # 각 섹션에 대한 블럭 리스트
        self.enemies = []   # 적 객체 리스트
        self.powerups = []  # 파워업 객체 리스트
        self.load_map()

    def load_map(self):
        # 블럭 데이터를 섹션별로 분리
        section_width = 800  # 각 섹션의 너비
        num_sections = max(data["x"] // section_width for data in map_data) + 1

        # 섹션 초기화
        for section in range(num_sections):
            self.sections.append([])
            self.enemies.append([])
            self.powerups.append([])

        for data in map_data:
            section_index = data["x"] // section_width
            if data["type"] in ["block", "question_block", "pipe", "invisible", "solid"]:
                block = Block(data["x"] % section_width, data["y"], data["width"], data["height"], data["type"])
                self.sections[section_index].append(block)
            elif data["type"] == "enemy":
                enemy = Enemy(data["x"] % section_width, data["y"])
                self.enemies[section_index].append(enemy)
            elif data["type"] == "powerup":
                powerup = PowerUp(data["x"] % section_width, data["y"], "mushroom")  # 파워업 유형 추가
                self.powerups[section_index].append(powerup)

    def reset_map(self):
        """맵을 초기 상태로 리셋"""
        self.sections = []  # 섹션 초기화
        self.enemies = []   # 적 리스트 초기화
        self.powerups = []  # 파워업 리스트 초기화
        self.load_map()     # 맵 데이터 다시 로드

    def reset_enemies(self, section):
        # 해당 섹션의 적을 초기 위치로 복구
        if 0 <= section < len(self.enemies):
            for enemy in self.enemies[section]:
                enemy.reset()

    def reset_powerups(self, section):
        # 해당 섹션의 파워업을 초기 위치로 복구
        if 0 <= section < len(self.powerups):
            for powerup in self.powerups[section]:
                powerup.is_active = True

    def draw(self, section):
        if 0 <= section < len(self.sections):
            for block in self.sections[section]:
                block.draw(0)  # 화면 고정, 카메라 이동 없음
            for enemy in self.enemies[section]:
                enemy.draw(0)  # 화면 고정, 카메라 이동 없음
            for powerup in self.powerups[section]:
                powerup.draw(0)  # 파워업 표시

    def get_blocks(self, section):
        return self.sections[section] if 0 <= section < len(self.sections) else []

    def get_enemies(self, section):
        return self.enemies[section] if 0 <= section < len(self.enemies) else []

    def get_powerups(self, section):
        return self.powerups[section] if 0 <= section < len(self.powerups) else []
