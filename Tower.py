import pygame as pg
from config import Config

class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        super().__init__()
        self.__name = ""
        self.__type = ""
        self.__tile_x = tile_x
        self.__tile_y = tile_y

        self.__x = (self.__tile_x) * (Config.get("TILE_SIZE"))
        self.__y = (self.__tile_y - 1) * (Config.get("TILE_SIZE"))

        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__x, self.__y)

        self.__target = None
        self.__level = 1
        self.__range = 0
        self.__buy_cost = 0
        self.__upgrade_cost = 0
        self.__sell_cost = 0

        self.__range_image = pg.Surface((self.__range * 2, self.__range * 2))
        self.__range_image.fill((0, 0, 0))
        self.__range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.__range_image, "gray100", (self.__range, self.__range), self.__range)
        self.__range_image.set_alpha(100)
        self.__range_rect = self.__range_image.get_rect()
        self.__range_rect.center = self.__rect.center

        self.__weapon = None

        self.__selected = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def tile_x(self):
        return self.__tile_x

    @tile_x.setter
    def tile_x(self, value):
        self.__tile_x = value

    @property
    def tile_y(self):
        return self.__tile_y

    @tile_y.setter
    def tile_y(self, value):
        self.__tile_y = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def rect(self):
        return self.__rect

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        self.__range = value

    @property
    def range_image(self):
        return self.__range_image

    @range_image.setter
    def range_image(self, value):
        self.__range_image = value

    @property
    def range_rect(self):
        return self.__range_rect

    @range_rect.setter
    def range_rect(self, value):
        self.__range_rect = value


    @property
    def buy_cost(self):
        return self.__buy_cost

    @buy_cost.setter
    def buy_cost(self, value):
        self.__buy_cost = value

    @property
    def upgrade_cost(self):
        return self.__upgrade_cost

    @upgrade_cost.setter
    def upgrade_cost(self, value):
        self.__upgrade_cost = value

    @property
    def sell_cost(self):
        return self.__sell_cost

    @sell_cost.setter
    def sell_cost(self, value):
        self.__sell_cost = value

    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, value):
        self.__weapon = value

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        self.__selected = value

    def upgrade_level(self):
        pass

    def update(self, dt, enemy_group, screen):
        if self.__target not in enemy_group:
            self.__target = None
            self.__weapon.reset_animation()
        if self.__target:
            self.__weapon.update(dt)
        self.pick_target(enemy_group)
        self.draw(screen)

    def pick_target(self, enemy_group):
        pass

    def draw(self, screen):
        if self.__selected:
            clipped_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            clipped_surface.blit(self.__range_image, self.__range_rect)
            cropped = clipped_surface.subsurface((0, 0, Config.get("WIN_W"), screen.get_height()))
            screen.blit(cropped, (0, 0))

        screen.blit(self.__image, self.__rect)
        screen.blit(self.__weapon.image, self.__weapon.rect)
