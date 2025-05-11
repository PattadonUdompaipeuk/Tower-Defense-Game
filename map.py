import random
from enemy_data import Enemy_data
from config import Config
class Map:
    def __init__(self, map_data, map_image):
        self.__wave = 1
        self.__hp = Config.get("BASE_HP")
        self.__money = Config.get("MONEY")
        self.__waypoints = []
        self.__map_data = map_data
        self.__image = map_image
        self.__enemy_list = []
        self.__spawned_enemies = 0
        self.__killed_enemies = 0
        self.__missed_enemies = 0
        self.__way = random.choice(["way1", "way2"])

    @property
    def wave(self):
        return self.__wave

    @wave.setter
    def wave(self, value):
        self.__wave = value

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        self.__hp = value

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value

    @property
    def waypoints(self):
        return self.__waypoints

    @property
    def spawned_enemies(self):
        return self.__spawned_enemies

    @spawned_enemies.setter
    def spawned_enemies(self, value):
        self.__spawned_enemies = value

    @property
    def killed_enemies(self):
        return self.__killed_enemies

    @killed_enemies.setter
    def killed_enemies(self, value):
        self.__killed_enemies = value

    @property
    def missed_enemies(self):
        return self.__missed_enemies

    @missed_enemies.setter
    def missed_enemies(self, value):
        self.__missed_enemies = value

    @property
    def enemy_list(self):
        return self.__enemy_list

    @enemy_list.setter
    def enemy_list(self, value):
        self.__enemy_list = value

    def random_way(self):
        self.__waypoints = []
        self.__way = random.choice(["way1", "way2"])

    def process_data(self):
        for layer in self.__map_data["layers"]:
            if layer["name"] == self.__way:
                for obj in layer["objects"]:
                    tmp_x = round(obj["x"], 2)
                    tmp_y = round(obj["y"], 2)
                    self.__waypoints.append((tmp_x, tmp_y))

    def process_waypoints(self, data):
        for point in data:
            tmp_x = point.get('x')
            tmp_y = point.get('y')
            self.__waypoints.append((tmp_x, tmp_y))

    def process_enemies(self):
        enemies = Enemy_data.enemy_wave[self.__wave - 1]
        for enemy_type in enemies:
            enemies_spawning = enemies[enemy_type]
            for enemy in range(enemies_spawning):
                self.__enemy_list.append(enemy_type)
        random.shuffle(self.__enemy_list)
        print(self.enemy_list)

    def next_wave(self):
        if self.__wave < len(Enemy_data.enemy_wave):
            self.__wave += 1
            self.__money += Enemy_data.wave_money[self.__wave - 1]
            self.__enemy_list = []
            self.__spawned_enemies = 0
            self.__killed_enemies = 0
            self.__missed_enemies = 0
            self.random_way()
            self.process_data()
            self.process_enemies()

    def reset(self):
        self.__wave = 1
        self.__hp = Config.get("BASE_HP")
        self.__money = Config.get("MONEY")
        self.__enemy_list = []
        self.__spawned_enemies = 0
        self.__killed_enemies = 0
        self.__missed_enemies = 0

    def draw(self, surface):
        surface.blit(self.__image, (0,0))

