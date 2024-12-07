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

        for section in range(num_sections):
            self.sections.append([])
            self.enemies.append([])
            self.powerups.append([])
            self.coins.append([])

        for data in map_data:
            section_index = data["x"] // section_width
            if data["type"] in ["block", "question_block", "pipe", "invisible", "solid"]:
                block = Block(data["x"] % section_width, data["y"], data["width"], data["height"], data["type"])
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
                block.reset()  # 각 블럭의 상태 초기화

            # 적 초기화
            self.reset_enemies(section_index)

            # 파워업 초기화
            self.reset_powerups(section_index)

            # 코인 초기화
            self.reset_coins(section_index)

    def reset_enemies(self, section):
        """해당 섹션의 적 상태를 초기화."""
        if 0 <= section < len(self.enemies):
            for enemy in self.enemies[section]:
                enemy.reset()  # 적 초기화 메서드 호출

    def reset_powerups(self, section):
        """해당 섹션의 파워업 상태를 초기화."""
        if 0 <= section < len(self.powerups):
            for powerup in self.powerups[section]:
                powerup.is_active = True

    def reset_coins(self, section):
        """해당 섹션의 코인 상태를 초기화."""
        if 0 <= section < len(self.coins):
            for coin in self.coins[section]:
                coin.is_active = True

    def draw(self, section):
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
        return self.sections[section] if 0 <= section < len(self.sections) else []

    def get_enemies(self, section):
        return self.enemies[section] if 0 <= section < len(self.enemies) else []

    def get_powerups(self, section):
        return self.powerups[section] if 0 <= section < len(self.powerups) else []

    def get_coins(self, section):
        return self.coins[section] if 0 <= section < len(self.coins) else []
