from block import Block
from enemy import Enemy
from powerup import PowerUp
from coin import Coin
from map_data import map_data

class MapLoader:
    def __init__(self):
        self.sections = []  # 각 섹션에 대한 블럭 리스트
        self.enemies = []   # 적 객체 리스트
        self.powerups = []  # 파워업 객체 리스트
        self.coins = []     # 코인 객체 리스트
        self.load_map()

    def load_map(self):
        section_width = 800  # 각 섹션의 너비
        num_sections = max(data["x"] // section_width for data in map_data) + 1

        # 각 섹션 초기화
        for section in range(num_sections):
            self.sections.append([])
            self.enemies.append([])
            self.powerups.append([])
            self.coins.append([])

        # 데이터 로드 및 객체 생성
        for data in map_data:
            section_index = data["x"] // section_width  # 섹션 인덱스 계산
            if data["type"] in ["block", "question_block", "pipe", "invisible", "solid"]:
                block = Block(
                    data["x"] % section_width,  # 섹션 상대 X 좌표
                    data["y"],                 # Y 좌표는 그대로
                    data["width"],
                    data["height"],
                    data["type"],
                    section_index              # 섹션 인덱스 전달
                )
                self.sections[section_index].append(block)
            elif data["type"] == "enemy":
                enemy = Enemy(data["x"] % section_width, data["y"])
                self.enemies[section_index].append(enemy)
            elif data["type"] == "powerup":
                powerup = PowerUp(data["x"] % section_width, data["y"], "mushroom")
                self.powerups[section_index].append(powerup)
            elif data["type"] == "coin":
                coin = Coin(data["x"] % section_width, data["y"])
                self.coins[section_index].append(coin)

    def reset_map(self):
        """전체 맵 상태를 초기화."""
        for section_index in range(len(self.sections)):
            # 블럭 초기화
            for block in self.sections[section_index]:
                block.reset()

            # 적 초기화
            self.reset_enemies(section_index)

            # 코인 초기화
            self.reset_coins(section_index)

        # 모든 파워업 제거
        self.reset_powerups()

    def reset_enemies(self, section):
        """해당 섹션의 적 상태를 초기화."""
        if 0 <= section < len(self.enemies):
            for enemy in self.enemies[section]:
                enemy.reset()  # 적 초기화 메서드 호출

    def reset_powerups(self, section=None):
        """맵의 모든 파워업 상태를 초기화 및 제거."""
        if section is None:  # 모든 섹션의 파워업을 제거
            for powerup_list in self.powerups:
                powerup_list.clear()
        elif 0 <= section < len(self.powerups):  # 특정 섹션의 파워업만 제거
            self.powerups[section].clear()

    def reset_coins(self, section):
        """해당 섹션의 코인 상태를 초기화."""
        if 0 <= section < len(self.coins):
            for coin in self.coins[section]:
                coin.is_active = True

    def draw(self, section):
        """해당 섹션의 모든 객체를 그리기."""
        if 0 <= section < len(self.sections):
            for block in self.sections[section]:
                block.draw(0)
            for enemy in self.enemies[section]:
                enemy.draw(0)
            for powerup in self.powerups[section]:
                powerup.draw(0)
            for coin in self.coins[section]:
                coin.draw(0)

    def get_blocks(self, section):
        """해당 섹션의 블럭 리스트를 반환."""
        return self.sections[section] if 0 <= section < len(self.sections) else []

    def get_enemies(self, section):
        """해당 섹션의 적 리스트를 반환."""
        return self.enemies[section] if 0 <= section < len(self.enemies) else []

    def get_powerups(self, section):
        """해당 섹션의 파워업 리스트를 반환."""
        return self.powerups[section] if 0 <= section < len(self.powerups) else []

    def get_coins(self, section):
        """해당 섹션의 코인 리스트를 반환."""
        return self.coins[section] if 0 <= section < len(self.coins) else []

    def add_powerup(self, powerup, section_index):
        """특정 섹션에 파워업 추가."""
        if 0 <= section_index < len(self.powerups):
            self.powerups[section_index].append(powerup)