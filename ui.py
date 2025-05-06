import pygame as pg
from config import Config
from tower_icon import TowerIcon
from magic_tower import MagicTower
from archer_tower import ArcherTower
from spritesheet_data import SpriteSheet_data
from Button import Button

class UI:
    def __init__(self, map, font, tower_group, tower_history):
        self.tower_group = tower_group
        self.tower_history = tower_history
        self.map = map
        self.font = font

        self.upgrade_img = SpriteSheet_data(Config.get("BUTTON"), 5, 2, 16 * 2, 16 * 2)
        self.upgrade_img.load_frames_from_spritesheet(12, 12)
        self.upgrade_btn = Button(self.upgrade_img.frame[4], Config.get("WIN_W") + 80,
                                  (Config.get("WIN_H")) - 60, True)

        self.max_img = pg.Surface((15 * 3, 15 * 2))
        self.max_img.fill("green3")

        self.sell_img = SpriteSheet_data(Config.get("BUTTON"), 6, 8, 16 * 2, 16 * 2)
        self.sell_img.load_frames_from_spritesheet(12, 12)
        self.sell_btn = Button(self.sell_img.frame[5], Config.get("WIN_W") + 240,
                                  (Config.get("WIN_H")) - 60, True)

    def draw_text(self, text, font, color, x, y, screen):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def draw_tower_ui(self, tower, screen):
        panel_rect = pg.Rect(Config.get("WIN_W"), (Config.get("WIN_H")/2), Config.get("SIDE_PANEL"), (Config.get("WIN_H")/2))
        pg.draw.rect(screen, (50, 50, 50), panel_rect)
        pg.draw.rect(screen, (255, 255, 255), panel_rect, 2)

        self.draw_text(f"{tower.name} Lv.{tower.level}", self.font, Config.get("WHITE"), Config.get("WIN_W") + 30,
                       (Config.get("WIN_H")/2) + 30, screen)

        self.draw_text(f"Range: {tower.range}", self.font, Config.get("WHITE"), Config.get("WIN_W") + 30,
                       (Config.get("WIN_H") / 2) + 80, screen)

        self.draw_text(f"Damage: {tower.weapon.damage}", self.font, Config.get("WHITE"), Config.get("WIN_W") + 260,
                       (Config.get("WIN_H") / 2) + 80, screen)

        if tower.level < Config.get("MAX_LEVEL"):
            screen.blit(self.font.render(f"{tower.upgrade_cost}$", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 100, Config.get("WIN_H") - 70))
            if self.upgrade_btn.draw(screen):
                if self.map.money >= tower.upgrade_cost:
                    self.map.money -= tower.upgrade_cost
                    tower.upgrade_level()
                    tower.weapon.upgrade_level()
        else:
            max_upgrade_btn = pg.Rect(Config.get("WIN_W") + 80, (Config.get("WIN_H") - 75), 60, 30)
            pg.draw.rect(screen, (0, 200, 0), max_upgrade_btn)
            screen.blit(self.font.render(f"MAX", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 90, Config.get("WIN_H") - 70))

        screen.blit(self.font.render(f"{tower.sell_cost}$", True, Config.get("WHITE")),
                    (Config.get("WIN_W") + 260, Config.get("WIN_H") - 70))
        if self.sell_btn.draw(screen):
            if (tower.tile_x, tower.tile_y) in self.tower_history:
                self.tower_history.remove((tower.tile_x, tower.tile_y))
                self.map.money += tower.sell_cost
                self.tower_group.remove(tower)

        set_weapon_center = 0
        if isinstance(tower, MagicTower):
            set_weapon_center = Config.get("SET_MAGIC_WEAPON")[tower.level - 1]
        elif isinstance(tower, ArcherTower):
            set_weapon_center = Config.get("SET_ARCHER_WEAPON")[tower.level - 1]

        manage_bar_tower = TowerIcon(tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL")/2,
                                             Config.get("WIN_H")/2 + Config.get("WIN_H")/4),
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL")/2,
                                      Config.get("WIN_H")/2 + Config.get("WIN_H")/4 - set_weapon_center))
        manage_bar_tower.draw(screen)