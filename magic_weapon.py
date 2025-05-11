import pygame as pg
from config import Config
from tower_data import TowerData
class MagicWeapon(pg.sprite.Sprite):
    def __init__(self, tile_x, tile_y):
        super().__init__()
        pg.init()
        self.__tile_x = tile_x
        self.__tile_y = tile_y

        self.__set_y_center = 2

        self.__x = (self.__tile_x) * (Config.get("TILE_SIZE"))
        self.__y = (self.__tile_y - self.__set_y_center) * (Config.get("TILE_SIZE"))

        self.__level = 1
        self.__frame = []
        self.__weapon_spritesheets = []
        for x in range(1, Config.get("MAX_LEVEL") + 1):
            weapon_sheet = pg.image.load(f'materials/tower/Towers Weapons/Tower 05/'
                                         f'Spritesheets/Tower 05 - Level 0{x} - Weapon.png').convert_alpha()
            self.__weapon_spritesheets.append(weapon_sheet)

        self.__weapon_image = self.__weapon_spritesheets[self.__level - 1]

        self.load_frames_from_spritesheet(29,2)
        self.__current_frame = 0
        self.__image = self.__frame[self.__current_frame]
        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__x, self.__y)

        self.__damage = TowerData.Magic_Upgrade[self.__level - 1].get("damage")

        self.__fire_rate_timer = 0
        self.__fire_rate = TowerData.Magic_Upgrade[self.__level - 1].get("fire_rate")

        self.__is_cooling_down = False
        self.__cooldown = TowerData.Magic_Upgrade[self.__level - 1].get("cooldown")
        self.__cooldown_timer = 0

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def level(self):
        return self.__level

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        self.__frame = value

    @property
    def current_frame(self):
        return self.__current_frame

    @current_frame.setter
    def current_frame(self, value):
        self.__current_frame = value

    @property
    def cooldown(self):
        return self.__cooldown

    @cooldown.setter
    def cooldown(self, value):
        self.__cooldown = value

    @property
    def is_cooling_down(self):
        return self.__is_cooling_down

    @is_cooling_down.setter
    def is_cooling_down(self, value):
        self.__is_cooling_down = value

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.__weapon_image.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(8):
            frame = pg.transform.smoothscale(self.__weapon_image.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.__frame.append(frame)

        for i in range(29):
            frame = pg.transform.smoothscale(self.__weapon_image.subsurface(
                (i * frame_width, frame_height * 1, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.__frame.append(frame)

    def upgrade_level(self):
        self.__level += 1
        self.__current_frame = 0
        self.__set_y_center += 0.5
        self.__y = (self.__tile_y - self.__set_y_center) * (Config.get("TILE_SIZE"))
        self.__weapon_image = self.__weapon_spritesheets[self.__level - 1]
        self.__frame = []

        self.__weapon_image = self.__weapon_spritesheets[self.__level - 1]

        self.load_frames_from_spritesheet(29, 2)
        self.__current_frame += 1
        self.__image = self.__frame[self.__current_frame]
        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__x, self.__y)

        self.__damage = TowerData.Magic_Upgrade[self.__level - 1].get("damage")

        self.__fire_rate_timer = 0
        self.__fire_rate = TowerData.Magic_Upgrade[self.__level - 1].get("fire_rate")

        self.__is_cooling_down = False
        self.__cooldown = TowerData.Magic_Upgrade[self.__level - 1].get("cooldown")
        self.__cooldown_timer = 0

    def update(self, dt):
        if not self.__is_cooling_down:
            self.animate(dt)
        else:
            self.__cooldown_timer += dt
            if self.__cooldown_timer >= self.__cooldown:
                self.__is_cooling_down = False
                self.__cooldown_timer = 0
                self.reset_animation()

    def animate(self, dt):
        self.__fire_rate_timer += dt
        if self.__fire_rate_timer >= self.__fire_rate:
            self.__fire_rate_timer = 0
            self.__current_frame += 1

            if self.__current_frame >= len(self.__frame):
                self.__current_frame = len(self.__frame) - 1
                self.__is_cooling_down = True
            else:
                self.__image = self.__frame[self.__current_frame]

    def reset_animation(self):
        self.__current_frame = 0
        self.__image = self.__frame[self.__current_frame]

