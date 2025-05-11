from Tower import Tower
import pygame as pg
import math
from archer_weapon import ArcherWeapon
from config import Config
from tower_data import TowerData
class ArcherTower(Tower):
    def __init__(self, tile_x, tile_y):
        pg.init()
        self.__archer_tower = pg.image.load("materials/tower/Towers bases/PNGs/Tower 06.png")
        self.__frame = []
        self.load_frames_from_spritesheet(3,1)
        self.__current_frame = 0
        image = self.__frame[self.__current_frame]
        super().__init__(image, tile_x, tile_y)
        self.name = "Archer Tower"
        self.type = "Archer"

        self.range = TowerData.Archer_Upgrade[self.level - 1].get("range")
        self.buy_cost = 200
        self.upgrade_cost = TowerData.Archer_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Archer_Upgrade[self.level - 1].get("sell_cost")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.weapon = ArcherWeapon(tile_x, tile_y)

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.__archer_tower.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(3):
            frame = pg.transform.smoothscale(self.__archer_tower.subsurface(
                (i * frame_width, frame_height * 0, frame_width, frame_height)
            ), (frame_width, frame_height))

            self.__frame.append(frame)

    def pick_target(self, enemy_group):
        for enemy in enemy_group:
            if enemy.current_health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range and enemy.current_health > 0:
                    self.target = enemy
                    self.weapon.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    if self.weapon.current_frame == 5 and self.weapon.is_cooling_down == False:
                        self.target.current_health -= self.weapon.damage
                    return
        self.target = None
        self.weapon.reset_animation()

    def upgrade_level(self):
        self.level += 1
        self.__current_frame += 1
        self.image = self.__frame[self.__current_frame]
        self.range = TowerData.Archer_Upgrade[self.level - 1].get("range")
        if self.level < Config.get("MAX_LEVEL"):
            self.upgrade_cost = TowerData.Archer_Upgrade[self.level].get("upgrade_cost")
        self.sell_cost = TowerData.Archer_Upgrade[self.level - 1].get("sell_cost")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.weapon.damage = TowerData.Archer_Upgrade[self.level - 1].get("damage")

    def draw(self, screen):
        self.weapon.image = pg.transform.rotate(self.weapon.original_image, self.weapon.angle - 90)
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.center = (self.weapon.x, self.weapon.y)
        if self.selected:
            clipped_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            clipped_surface.blit(self.range_image, self.range_rect)
            cropped = clipped_surface.subsurface((0, 0, Config.get("WIN_W"), screen.get_height()))
            screen.blit(cropped, (0, 0))

        screen.blit(self.image, self.rect)
        screen.blit(self.weapon.image, self.weapon.rect)





