from Tower import Tower
import pygame as pg
from slow_weapon import SlowWeapon
from config import Config
from tower_data import TowerData
import math
class SlowTower(Tower):
    def __init__(self, tile_x, tile_y):
        pg.init()
        self.__slow_tower = pg.image.load("materials/tower/Towers bases/PNGs/Tower 08.png")
        self.__frame = []
        self.load_frames_from_spritesheet(3,1)
        self.__current_frame = 0
        image = self.__frame[self.__current_frame]
        super().__init__(image, tile_x, tile_y)
        self.name = "Slow Tower"
        self.type = "Slow"

        self.x = (self.tile_x) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - 2.5) * (Config.get("TILE_SIZE"))
        self.rect.center = (self.x, self.y)

        self.level = 1
        self.range = TowerData.Slow_Upgrade[self.level - 1].get("range")
        self.buy_cost = 300
        self.upgrade_cost = TowerData.Slow_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Slow_Upgrade[self.level - 1].get("sell_cost")
        self.__targets = []
        self.__slow_factor = TowerData.Slow_Upgrade[self.level - 1].get("slow_factor")
        self.__slow_duration = TowerData.Slow_Upgrade[self.level - 1].get("slow_duration")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.range_rect.centery += 48

        self.weapon = SlowWeapon(tile_x, tile_y)

    @property
    def slow_factor(self):
        return self.__slow_factor

    @property
    def slow_duration(self):
        return self.__slow_duration

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.__slow_tower.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(3):
            frame = pg.transform.smoothscale(self.__slow_tower.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.__frame.append(frame)

    def update(self, dt, enemy_group, screen):
        self.pick_targets(enemy_group)
        if not self.__targets:
            self.weapon.reset_animation()
        else:
            self.weapon.update(dt)
            if self.weapon.is_cooling_down is False and self.weapon.current_frame == 9:
                self.attack()

        self.draw(screen)

    def attack(self):
        for enemy in self.__targets:
            enemy.apply_slow(self.__slow_factor, self.__slow_duration)

    def upgrade_level(self):
        self.level += 1
        self.__current_frame += 1
        self.image = self.__frame[self.__current_frame]
        self.range = TowerData.Slow_Upgrade[self.level - 1].get("range")
        self.weapon.damage = TowerData.Slow_Upgrade[self.level - 1].get("damage")
        if self.level < Config.get("MAX_LEVEL"):
            self.upgrade_cost = TowerData.Slow_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Slow_Upgrade[self.level - 1].get("sell_cost")
        self.__slow_factor = TowerData.Slow_Upgrade[self.level - 1].get("slow_factor")
        self.__slow_duration = TowerData.Slow_Upgrade[self.level - 1].get("slow_duration")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.range_rect.centery += 48

    def pick_targets(self, enemy_group):
        self.__targets = []
        for enemy in enemy_group:
            if enemy.current_health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.__targets.append(enemy)