import pygame as pg
from config import Config
class MagicWeapon(pg.sprite.Sprite):
    def __init__(self, tile_x, tile_y):
        super().__init__()
        pg.init()
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()

        self.x = (self.tile_x) * (Config.get("TILE_SIZE"))
        self.y = (self.tile_y - 2) * (Config.get("TILE_SIZE"))

        self.weapon_image = pg.image.load("materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers Weapons/Tower 05/"
                                          "Spritesheets/Tower 05 - Level 01 - Weapon.png")
        self.frame = []
        self.load_frames_from_spritesheet(29,2)
        self.current_frame = 0
        self.image = self.frame[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.animation_timer = 0
        self.animation_speed = 0.03

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.weapon_image.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height
        print(frame_width, frame_height)

        for i in range(8):
            frame = pg.transform.smoothscale(self.weapon_image.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.frame.append(frame)

        for i in range(29):
            frame = pg.transform.smoothscale(self.weapon_image.subsurface(
                (i * frame_width, frame_height * 1, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.frame.append(frame)

    def update(self, dt):
        self.animate(dt)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frame)
            new_image = self.frame[self.current_frame]
            self.image = new_image

