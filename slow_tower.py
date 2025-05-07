from Tower import Tower
import pygame as pg
from slow_weapon import SlowWeapon
from config import Config
from tower_data import TowerData
import math
class SlowTower(Tower):
    def __init__(self, tile_x, tile_y):
        pg.init()
        self.name = "Slow Tower"
        self.slow_tower = pg.image.load("materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers bases/PNGs/Tower 08.png")
        self.icon_frame = []
        self.load_frames_from_spritesheet(3,1)
        self.icon_index = 0
        self.image = self.icon_frame[self.icon_index]
        super().__init__(self.image, tile_x, tile_y)
        self.x = (self.tile_x) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - 2.5) * (Config.get("TILE_SIZE"))
        self.rect.center = (self.x, self.y)

        self.level = 1
        self.range = TowerData.Slow_Upgrade[self.level - 1].get("range")
        self.buy_cost = 300
        self.upgrade_cost = TowerData.Slow_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Slow_Upgrade[self.level - 1].get("sell_cost")
        self.targets = []
        self.slow_factor = TowerData.Slow_Upgrade[self.level - 1].get("slow_factor")
        self.slow_duration = TowerData.Slow_Upgrade[self.level - 1].get("slow_duration")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.range_rect.centery += 56

        self.weapon = SlowWeapon(tile_x, tile_y)

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.slow_tower.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(3):
            frame = pg.transform.smoothscale(self.slow_tower.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.icon_frame.append(frame)

    def update(self, dt, enemy_group, screen):
        self.pick_targets(enemy_group)  # <== ย้ายมาไว้บนสุด

        if not self.targets:
            self.weapon.reset_animation()
        else:
            self.weapon.update(dt)
            if self.weapon.is_cooling_down is False and self.weapon.current_frame == 9:
                self.attack()

        self.draw(screen)

    def attack(self):
        for enemy in self.targets:
            enemy.apply_slow(self.slow_factor, self.slow_duration)

    def upgrade_level(self):
        self.level += 1
        self.icon_index += 1
        self.image = self.icon_frame[self.icon_index]
        self.range = TowerData.Slow_Upgrade[self.level - 1].get("range")
        self.weapon.damage = TowerData.Slow_Upgrade[self.level - 1].get("damage")
        if self.level < Config.get("MAX_LEVEL"):
            self.upgrade_cost = TowerData.Slow_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Slow_Upgrade[self.level - 1].get("sell_cost")
        self.slow_factor = TowerData.Slow_Upgrade[self.level - 1].get("slow_factor")
        self.slow_duration = TowerData.Slow_Upgrade[self.level - 1].get("slow_duration")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        self.range_rect.centery += 56

    def pick_targets(self, enemy_group):
        self.targets = []
        for enemy in enemy_group:
            if enemy.current_health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.targets.append(enemy)