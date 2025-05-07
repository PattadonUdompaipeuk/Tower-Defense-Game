import pygame as pg
from config import Config
import math
from tower_data import TowerData
from Button import Button
from spritesheet_data import SpriteSheet_data
class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        super().__init__()
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - 1) * (Config.get("TILE_SIZE"))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.target = None
        self.level = 1
        self.upgrade_cost = 0

        self.range = 0
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.weapon = None

        self.selected = False

    def upgrade_level(self):
        pass

    def update(self, dt, enemy_group, screen):
        if self.target not in enemy_group:
            self.target = None
            self.weapon.reset_animation()
        if self.target:
            self.weapon.update(dt)
        self.pick_target(enemy_group)
        self.draw(screen)

    def pick_target(self, enemy_group):
        pass

    def draw(self, screen):
        if self.selected:
            clipped_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            clipped_surface.blit(self.range_image, self.range_rect)
            cropped = clipped_surface.subsurface((0, 0, Config.get("WIN_W"), screen.get_height()))
            screen.blit(cropped, (0, 0))

        screen.blit(self.image, self.rect)
        screen.blit(self.weapon.image, self.weapon.rect)

