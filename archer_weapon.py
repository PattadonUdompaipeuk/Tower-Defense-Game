import pygame as pg
from config import Config
from tower_data import TowerData
class ArcherWeapon(pg.sprite.Sprite):
    def __init__(self, tile_x, tile_y):
        pg.sprite.Sprite().__init__()

        pg.init()
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.set_y_center = 1.5

        self.x = (self.tile_x) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - self.set_y_center) * (Config.get("TILE_SIZE"))

        self.level = 1
        self.frame = []
        self.weapon_spritesheets = []
        for x in range(1, Config.get("MAX_LEVEL") + 1):
            weapon_sheet = pg.image.load(f'materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers Weapons/Tower 06/'
                                         f'Spritesheets/Tower 06 - Level 0{x} - Weapon.png')
            self.weapon_spritesheets.append(weapon_sheet)

        self.weapon_image = self.weapon_spritesheets[self.level - 1]
        self.frame_width = 0
        self.frame_height = 0

        self.load_frames_from_spritesheet(6, 1)
        self.current_frame = 0
        self.angle = 90
        self.original_image = self.frame[self.current_frame]
        self.image = pg.transform.rotate(self.original_image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.damage = TowerData.Archer_Upgrade[self.level - 1].get("damage")

        self.fire_rate_timer = 0
        self.fire_rate = TowerData.Archer_Upgrade[self.level - 1].get("fire_rate")

        self.is_cooling_down = False
        self.cooldown = TowerData.Archer_Upgrade[self.level - 1].get("cooldown")
        self.cooldown_timer = 0

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.weapon_image.get_size()
        self.frame_width = sheet_width // num_width
        self.frame_height = sheet_height // num_height

        for i in range(6):
            frame = pg.transform.smoothscale(self.weapon_image.subsurface(
                (i * self.frame_width, self.frame_height * 0, self.frame_width, self.frame_height)
            ), (self.frame_width, self.frame_height))

            self.frame.append(frame)

    def upgrade_level(self):
        self.level += 1
        self.set_y_center += 0.5
        self.y = (self.tile_y - self.set_y_center) * (Config.get("TILE_SIZE"))
        self.weapon_image = self.weapon_spritesheets[self.level - 1]
        self.frame = []
        self.load_frames_from_spritesheet(6, 1)

        self.current_frame = 0
        self.angle = 90
        self.original_image = self.frame[self.current_frame]
        self.image = pg.transform.rotate(self.original_image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.fire_rate_timer = 0
        self.fire_rate = TowerData.Archer_Upgrade[self.level - 1].get("fire_rate")

        self.is_cooling_down = False
        self.cooldown = TowerData.Archer_Upgrade[self.level - 1].get("cooldown")
        self.cooldown_timer = 0

    def update(self, dt):
        if not self.is_cooling_down:
            self.animate(dt)
        else:
            self.cooldown_timer += dt
            if self.cooldown_timer >= self.cooldown:
                self.is_cooling_down = False
                self.cooldown_timer = 0
                self.reset_animation()

    def animate(self, dt):
        self.fire_rate_timer += dt
        if self.fire_rate_timer >= self.fire_rate:
            self.fire_rate_timer = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frame):
                self.current_frame = len(self.frame) - 1
                self.is_cooling_down = True
            else:
                self.original_image = self.frame[self.current_frame]

    def reset_animation(self):
        self.current_frame = 0
        self.original_image = self.frame[self.current_frame]



