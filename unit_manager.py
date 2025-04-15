import pygame as pg
from config import Config
class UnitManager:
    def __init__(self, x, y):
        self.image = pg.image.load("materials/TD_map/Unit_manager.png")
        self.x = x
        self.y = y
        self.font = pg.font.Font("Stacked pixel.ttf", 48)
        self.text_surface = self.font.render("UNIT MANAGER", True, Config.get("WHITE"))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x + Config.get("SIDE_PANEL")/2, self.y + Config.get("SIDE_PANEL")/8)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.text_surface, self.text_rect)


