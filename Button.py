import pygame as pg
from config import Config
class Button:
    def __init__(self, txt, x, y, w, h, button_color, txt_color, single_click):
        # self.image = image
        self.button_color = button_color
        self.txt_color = txt_color
        self.font = pg.font.SysFont('Arial', 14)
        self.rect = pg.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.text = self.font.render(txt, True, self.txt_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
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

        # surface.blit(self.image, self.rect)
        pg.draw.rect(surface, self.button_color, self.rect)
        surface.blit(self.text, self.text_rect)

        return action
