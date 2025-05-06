import pygame as pg
from magic_weapon import MagicWeapon
from archer_weapon import ArcherWeapon
class TowerIcon:
    def __init__(self, tower, tower_base_rect, tower_weapon_rect):
        self.tower_base_img = tower.image
        self.tower_base_rect = self.tower_base_img.get_rect()
        self.tower_base_rect.center = tower_base_rect

        # if isinstance(tower.weapon, ArcherWeapon):
        #     self.tower_weapon_img = pg.transform.rotate(tower.weapon.image, tower.weapon.angle - 180)
        # else:
        #     self.tower_weapon_img = tower.weapon.frame[0]
        self.tower_weapon_img = tower.weapon.frame[0]

        self.tower_weapon_rect = self.tower_weapon_img.get_rect()
        self.tower_weapon_rect.center = tower_weapon_rect

    def draw(self, screen):
        screen.blit(self.tower_base_img, self.tower_base_rect)
        screen.blit(self.tower_weapon_img, self.tower_weapon_rect)

