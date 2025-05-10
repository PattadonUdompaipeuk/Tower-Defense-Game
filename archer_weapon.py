import pygame as pg
from config import Config
from tower_data import TowerData
class ArcherWeapon(pg.sprite.Sprite):
    def __init__(self, tile_x, tile_y):
        pg.sprite.Sprite().__init__()
        pg.init()
        self.__tile_x = tile_x
        self.__tile_y = tile_y

        self.__set_y_center = 1.5

        self.__x = (self.__tile_x) * (Config.get("TILE_SIZE"))
        self.__y = (self.__tile_y - self.__set_y_center) * (Config.get("TILE_SIZE"))

        self.__level = 1
        self.__frame = []
        self.__weapon_spritesheets = []
        for x in range(1, Config.get("MAX_LEVEL") + 1):
            weapon_sheet = pg.image.load(f'materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers Weapons/Tower 06/'
                                         f'Spritesheets/Tower 06 - Level 0{x} - Weapon.png').convert_alpha()
            self.__weapon_spritesheets.append(weapon_sheet)

        self.__weapon_image = self.__weapon_spritesheets[self.__level - 1]

        self.load_frames_from_spritesheet(6, 1)
        self.__current_frame = 0
        self.__angle = 90
        self.__original_image = self.__frame[self.__current_frame]
        self.__image = pg.transform.rotate(self.__original_image, self.__angle)

        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__x, self.__y)

        self.__damage = TowerData.Archer_Upgrade[self.__level - 1].get("damage")

        self.__fire_rate_timer = 0
        self.__fire_rate = TowerData.Archer_Upgrade[self.__level - 1].get("fire_rate")

        self.__is_cooling_down = False
        self.__cooldown = TowerData.Archer_Upgrade[self.__level - 1].get("cooldown")
        self.__cooldown_timer = 0

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def frame(self):
        return self.__frame

    @property
    def current_frame(self):
        return self.__current_frame

    @property
    def cooldown(self):
        return self.__cooldown

    @property
    def is_cooling_down(self):
        return self.__is_cooling_down

    @property
    def level(self):
        return self.__level

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, damage):
        self.__damage = damage

    @property
    def original_image(self):
        return self.__original_image

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.__weapon_image.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(6):
            frame = pg.transform.scale(self.__weapon_image.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.__frame.append(frame)

    def upgrade_level(self):
        self.__level += 1
        self.__set_y_center += 0.5
        self.__y = (self.__tile_y - self.__set_y_center) * (Config.get("TILE_SIZE"))
        self.__weapon_image = self.__weapon_spritesheets[self.__level - 1]
        self.__frame = []
        self.load_frames_from_spritesheet(6, 1)

        self.__current_frame = 0
        self.__angle = 90
        self.__original_image = self.__frame[self.__current_frame]
        self.__image = pg.transform.rotate(self.__original_image, self.__angle)

        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__x, self.__y)

        self.__fire_rate_timer = 0
        self.__fire_rate = TowerData.Archer_Upgrade[self.__level - 1].get("fire_rate")

        self.__is_cooling_down = False
        self.__cooldown = TowerData.Archer_Upgrade[self.__level - 1].get("cooldown")
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
                self.__original_image = self.__frame[self.__current_frame]

    def reset_animation(self):
        self.__current_frame = 0
        self.__original_image = self.__frame[self.__current_frame]



