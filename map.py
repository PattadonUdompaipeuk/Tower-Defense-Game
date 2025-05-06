import pygame as pg
import random
from enemy_data import Enemy_data
from config import Config
class Map:
    def __init__(self, map_data, map_image):
        self.wave = 1
        self.hp = Config.get("BASE_HP")
        self.money = Config.get("MONEY")
        self.waypoints = []
        self.map_data = map_data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.way = random.choice(["way1", "way2"])

    def random_way(self):
        self.waypoints = []
        self.way = random.choice(["way1", "way2"])

    def process_data(self):
        for layer in self.map_data["layers"]:
            if layer["name"] == self.way:
                for obj in layer["objects"]:
                    tmp_x = round(obj["x"], 2)
                    tmp_y = round(obj["y"], 2)
                    self.waypoints.append((tmp_x, tmp_y))

    def process_waypoints(self, data):
        for point in data:
            tmp_x = point.get('x')
            tmp_y = point.get('y')
            self.waypoints.append((tmp_x, tmp_y))

    def process_enemies(self):
        enemies = Enemy_data.enemy_wave[self.wave - 1]
        for enemy_type in enemies:
            enemies_spawning = enemies[enemy_type]
            for enemy in range(enemies_spawning):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)
        print(self.enemy_list)

    def next_wave(self):
        if self.wave < len(Enemy_data.enemy_wave):
            self.wave += 1
            self.money += Enemy_data.wave_money[self.wave - 1]
            self.enemy_list = []
            self.spawned_enemies = 0
            self.random_way()
            self.process_data()
            self.process_enemies()

    def draw(self, surface):
        surface.blit(self.image, (0,0))

