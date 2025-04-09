import pygame as pg
from config import Config
class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        super().__init__()
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 4.125) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - 1.5) * (Config.get("TILE_SIZE"))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)