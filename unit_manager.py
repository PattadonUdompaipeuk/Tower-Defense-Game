import pygame as pg
from config import Config
class UnitManager:
    def __init__(self, x, y):
        self.__image = pg.image.load("materials/TD_map/Unit_manager.png")
        self.__x = x
        self.__y = y
        self.__font = pg.font.Font("materials/Stacked pixel.ttf", 48)
        self.__text_surface = self.__font.render("UNIT MANAGER", True, Config.get("WHITE"))
        self.__text_rect = self.__text_surface.get_rect()
        self.__text_rect.center = (self.__x + Config.get("SIDE_PANEL")/2, self.__y + Config.get("SIDE_PANEL")/8)

    def draw(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        screen.blit(self.__text_surface, self.__text_rect)
