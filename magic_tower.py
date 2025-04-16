from Tower import Tower
import pygame as pg
from magic_weapon import MagicWeapon
import math
from tower_data import TowerData
class MagicTower(Tower):
    def __init__(self, tile_x, tile_y):
        pg.init()
        self.magic_tower = pg.image.load("materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers bases/PNGs/Tower 05.png")
        self.icon_frame = []
        self.load_frames_from_spritesheet(3,1)
        self.icon_index = 0
        self.image = self.icon_frame[self.icon_index]
        super().__init__(self.image, tile_x, tile_y)

        self.level = 1
        self.range = TowerData.Magic_Upgrade[self.level - 1].get("range")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.weapon = MagicWeapon(tile_x, tile_y)

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.magic_tower.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(3):
            frame = pg.transform.smoothscale(self.magic_tower.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.icon_frame.append(frame)

    def upgrade_level(self):
        self.level += 1
        self.icon_index += 1
        self.image = self.icon_frame[self.icon_index]
        self.range = TowerData.Magic_Upgrade[self.level - 1].get("range")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center



