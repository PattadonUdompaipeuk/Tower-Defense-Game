import pygame as pg

class Button:
    def __init__(self, image, x, y):
        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.center = (x, y)
        self.__clicked = False

    @property
    def rect(self):
        return self.__rect

    def draw(self, surface):
        action = False
        mouse_pos = pg.mouse.get_pos()

        if self.__rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.__clicked is False:
                action = True
                self.__clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.__clicked = False

        surface.blit(self.__image, self.__rect)

        return action


