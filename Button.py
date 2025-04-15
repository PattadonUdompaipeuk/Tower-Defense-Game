import pygame as pg

class Button:
    def __init__(self, image, x, y, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True
            if self.single_click:
                self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, self.rect)

        return action


