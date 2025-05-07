import pygame as pg
from config import Config
from tower_icon import TowerIcon
from magic_tower import MagicTower
from archer_tower import ArcherTower
from slow_tower import SlowTower
from spritesheet_data import SpriteSheet_data
from Button import Button

class UI:
    def __init__(self, tower_group, tower_history):
        self.tower_group = tower_group
        self.tower_history = tower_history

        self.font = pg.font.Font("Stacked pixel.ttf", 24)
        self.medium_font = pg.font.Font("Stacked pixel.ttf", 36)
        self.big_font = pg.font.Font("Stacked pixel.ttf", 120)

        self.upgrade_img = SpriteSheet_data(Config.get("BUTTON"), 5, 2, 16 * 2, 16 * 2)
        self.upgrade_img.load_frames_from_spritesheet(12, 12)
        self.upgrade_btn = Button(self.upgrade_img.frame[4], Config.get("WIN_W") + 80,
                                  (Config.get("WIN_H")) - 60)

        self.max_img = pg.Surface((15 * 3, 15 * 2))
        self.max_img.fill("green3")

        self.sell_img = SpriteSheet_data(Config.get("BUTTON"), 6, 8, 16 * 2, 16 * 2)
        self.sell_img.load_frames_from_spritesheet(12, 12)
        self.sell_btn = Button(self.sell_img.frame[5], Config.get("WIN_W") + 250,
                                  (Config.get("WIN_H")) - 60)

        self.game_coin = pg.image.load("materials/TD_map/pixel_coin-removebg-preview.png").convert_alpha()
        self.game_coin_img = pg.transform.scale(self.game_coin, (340 / 10, 340 / 10))
        self.game_coin_rect = self.game_coin_img.get_rect()

        self.base_hp = pg.image.load("materials/TD_map/pixel-heart.png").convert_alpha()
        self.base_hp_img = pg.transform.smoothscale(self.base_hp, (640 / 20, 640 / 20))
        self.base_hp_rect = self.base_hp_img.get_rect()

        self.attack_icon = pg.image.load("materials/tower/attack.png").convert_alpha()
        self.attack_icon_img = pg.transform.smoothscale(self.attack_icon, (32, 32))
        self.attack_icon_rect = self.attack_icon_img.get_rect()
        self.attack_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                          Config.get("WIN_H") / 2 + 120)

        self.range_icon = pg.image.load("materials/tower/target.png").convert_alpha()
        self.range_icon_img = pg.transform.smoothscale(self.range_icon, (32, 32))
        self.range_icon_rect = self.range_icon_img.get_rect()
        self.range_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                         Config.get("WIN_H") / 2 + 168)

        self.cooldown_icon = pg.image.load("materials/tower/cooldown.png").convert_alpha()
        self.cooldown_icon_img = pg.transform.smoothscale(self.cooldown_icon, (32, 32))
        self.cooldown_icon_rect = self.cooldown_icon_img.get_rect()
        self.cooldown_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                         Config.get("WIN_H") / 2 + 220)

        self.wave_text = self.big_font.render(f"WAVE 1", True, Config.get("BLACK"))
        self.wave_text_rect = self.wave_text.get_rect()
        self.wave_text_rect.center = (Config.get("WIN_W") / 2, Config.get("WIN_H") / 2)
        self.start_time = pg.time.get_ticks()
        self.duration = 1000
        self.fade_speed = 5
        self.alpha = 255
        self.wave_text.set_alpha(self.alpha)
        self.done = False

    def update(self):
        if self.done:
            return
        now = pg.time.get_ticks()
        elapsed = now - self.start_time

        if elapsed >= self.duration:
            self.alpha -= self.fade_speed
            self.wave_text_rect.centery -= 1
            if self.alpha <= 0:
                self.alpha = 0
                self.done = True

    def draw_text(self, text, font, color, x, y, screen):
        img = font.render(text, True, color)
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        screen.blit(img, img_rect)

    def draw_tower_ui(self, map, tower, screen):
        panel_rect = pg.Rect(Config.get("WIN_W"), (Config.get("WIN_H")/2), Config.get("SIDE_PANEL"), (Config.get("WIN_H")/2))
        pg.draw.rect(screen, (50, 50, 50), panel_rect)
        pg.draw.rect(screen, (255, 255, 255), panel_rect, 2)

        self.draw_text(f"{tower.name} Lv.{tower.level}", self.medium_font, Config.get("WHITE"), Config.get("WIN_W")
                       + Config.get("SIDE_PANEL")/2, (Config.get("WIN_H")/2) + 40, screen)

        screen.blit(self.attack_icon_img, self.attack_icon_rect)
        self.draw_text(f"{tower.weapon.damage}", self.font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL") / 4 + 30, (Config.get("WIN_H") / 2) + 120, screen)

        screen.blit(self.range_icon_img, self.range_icon_rect)
        self.draw_text(f"{tower.range}", self.font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL")/4 + 30, (Config.get("WIN_H") / 2) + 170, screen)

        screen.blit(self.cooldown_icon_img, self.cooldown_icon_rect)
        self.draw_text(f"{tower.weapon.cooldown}", self.font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL") / 4 + 30, (Config.get("WIN_H") / 2) + 220, screen)

        if tower.level < Config.get("MAX_LEVEL"):
            screen.blit(self.font.render(f"{tower.upgrade_cost}$", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 115, Config.get("WIN_H") - 70))
            if self.upgrade_btn.draw(screen):
                if map.money >= tower.upgrade_cost:
                    map.money -= tower.upgrade_cost
                    tower.upgrade_level()
                    tower.weapon.upgrade_level()
        else:
            max_upgrade_btn = pg.Rect(Config.get("WIN_W") + 80, (Config.get("WIN_H") - 75), 60, 30)
            pg.draw.rect(screen, (0, 200, 0), max_upgrade_btn)
            screen.blit(self.font.render(f"MAX", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 90, Config.get("WIN_H") - 70))

        screen.blit(self.font.render(f"{tower.sell_cost}$", True, Config.get("WHITE")),
                    (Config.get("WIN_W") + 280, Config.get("WIN_H") - 70))
        if self.sell_btn.draw(screen):
            if (tower.tile_x, tower.tile_y) in self.tower_history:
                self.tower_history.remove((tower.tile_x, tower.tile_y))
                map.money += tower.sell_cost
                self.tower_group.remove(tower)

        set_weapon_center = 0
        if isinstance(tower, MagicTower):
            set_weapon_center = Config.get("SET_MAGIC_WEAPON")[tower.level - 1]
        elif isinstance(tower, ArcherTower):
            set_weapon_center = Config.get("SET_ARCHER_WEAPON")[tower.level - 1]
        elif isinstance(tower, SlowTower):
            set_weapon_center = Config.get("SET_SLOW_WEAPON")[tower.level - 1]
        if not isinstance(tower, SlowTower):
            manage_bar_tower = TowerIcon(tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL") - 120,
                                             Config.get("WIN_H")/2 + Config.get("WIN_H")/4 - 30),
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") - 120,
                                      Config.get("WIN_H")/2 + Config.get("WIN_H")/4 - 30 - set_weapon_center))
            manage_bar_tower.draw(screen)
        else:
            manage_bar_tower = TowerIcon(tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL") - 120,
                                            Config.get("WIN_H") / 2 + Config.get("WIN_H") / 4 - 60),
                                    (Config.get("WIN_W") + Config.get("SIDE_PANEL") - 120,
                                     Config.get("WIN_H") / 2 + Config.get("WIN_H") / 4 - 30 - set_weapon_center))
            manage_bar_tower.draw(screen)

    def draw_status(self, map, screen):
        panel_rect = pg.Rect(0, 0, 140, 100)
        panel_rect.topright = (Config.get("WIN_W"), 0)
        pg.draw.rect(screen, (50, 50, 50), panel_rect)
        pg.draw.rect(screen, (255, 255, 255), panel_rect, 2)

        self.game_coin_rect.topright = (Config.get("WIN_W") - 14, 10)
        screen.blit(self.game_coin_img, self.game_coin_rect)

        self.base_hp_rect.topright = (Config.get("WIN_W") - 16, 55)
        screen.blit(self.base_hp_img, self.base_hp_rect)

        self.draw_text(f"{map.money}", self.font, Config.get("WHITE"), Config.get("WIN_W") - 90,28, screen)
        self.draw_text(f"{map.hp}", self.font, Config.get("WHITE"), Config.get("WIN_W") - 90, 70, screen)

    def draw_wave_text(self, screen):
        if not self.done:
            temp = self.wave_text.copy()
            temp.set_alpha(self.alpha)
            screen.blit(temp, self.wave_text_rect)

    def start_wave_text(self, wave_num):
        self.wave_text = self.big_font.render(f"WAVE {wave_num}", True, Config.get("BLACK"))
        self.wave_text_rect = self.wave_text.get_rect()
        self.wave_text_rect.center = (Config.get("WIN_W") / 2, Config.get("WIN_H") / 2)
        self.start_time = pg.time.get_ticks()
        self.duration = 1000
        self.fade_speed = 5
        self.alpha = 255
        self.wave_text.set_alpha(self.alpha)
        self.done = False

    def is_done(self):
        return self.done

