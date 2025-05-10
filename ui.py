import pygame as pg
from config import Config
from tower_icon import TowerIcon
from magic_tower import MagicTower
from archer_tower import ArcherTower
from slow_tower import SlowTower
from spritesheet_data import SpriteSheet_data
from Button import Button
from enemy_data import Enemy_data

class UI:
    def __init__(self, gm):
        self.__gm = gm

        self.__font = pg.font.Font("materials/Stacked pixel.ttf", 24)
        self.__medium_font = pg.font.Font("materials/Stacked pixel.ttf", 36)
        self.__big_font = pg.font.Font("materials/Stacked pixel.ttf", 120)

        self.__upgrade_img = SpriteSheet_data(Config.get("BUTTON"), 5, 2, 16 * 2, 16 * 2)
        self.__upgrade_img.load_frames_from_spritesheet(12, 12)
        self.__upgrade_btn = Button(self.__upgrade_img.frame[4], Config.get("WIN_W") + 80,
                                  (Config.get("WIN_H")) - 60)

        self.__max_img = pg.Surface((15 * 3, 15 * 2))
        self.__max_img.fill("green3")

        self.__sell_img = SpriteSheet_data(Config.get("BUTTON"), 6, 8, 16 * 2, 16 * 2)
        self.__sell_img.load_frames_from_spritesheet(12, 12)
        self.__sell_btn = Button(self.__sell_img.frame[5], Config.get("WIN_W") + 250,
                                  (Config.get("WIN_H")) - 60)

        self.__game_coin = pg.image.load("materials/TD_map/pixel_coin-removebg-preview.png").convert_alpha()
        self.__game_coin_img = pg.transform.scale(self.__game_coin, (340 / 10, 340 / 10))
        self.__game_coin_rect = self.__game_coin_img.get_rect()

        self.__base_hp = pg.image.load("materials/TD_map/pixel-heart.png").convert_alpha()
        self.__base_hp_img = pg.transform.smoothscale(self.__base_hp, (640 / 20, 640 / 20))
        self.__base_hp_rect = self.__base_hp_img.get_rect()

        self.__attack_icon = pg.image.load("materials/tower/attack.png").convert_alpha()
        self.__attack_icon_img = pg.transform.smoothscale(self.__attack_icon, (32, 32))
        self.__attack_icon_rect = self.__attack_icon_img.get_rect()
        self.__attack_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                          Config.get("WIN_H") / 2 + 120)

        self.__slow_icon = pg.image.load("materials/tower/slow.png").convert_alpha()
        self.__slow_icon_img = pg.transform.smoothscale(self.__slow_icon, (28, 28))
        self.__slow_icon_rect = self.__slow_icon_img.get_rect()
        self.__slow_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                            Config.get("WIN_H") / 2 + 120)

        self.__range_icon = pg.image.load("materials/tower/target.png").convert_alpha()
        self.__range_icon_img = pg.transform.smoothscale(self.__range_icon, (32, 32))
        self.__range_icon_rect = self.__range_icon_img.get_rect()
        self.__range_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                         Config.get("WIN_H") / 2 + 168)

        self.__cooldown_icon = pg.image.load("materials/tower/cooldown.png").convert_alpha()
        self.__cooldown_icon_img = pg.transform.smoothscale(self.__cooldown_icon, (32, 32))
        self.__cooldown_icon_rect = self.__cooldown_icon_img.get_rect()
        self.__cooldown_icon_rect.midright = (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4,
                                         Config.get("WIN_H") / 2 + 220)

        self.__wave_text = self.__big_font.render(f"WAVE 1", True, Config.get("BLACK"))
        self.__wave_text_rect = self.__wave_text.get_rect()
        self.__wave_text_rect.center = (Config.get("WIN_W") / 2, Config.get("WIN_H") / 2)
        self.__start_time = pg.time.get_ticks()
        self.__duration = 1000
        self.__fade_speed = 5
        self.__alpha = 255
        self.__wave_text.set_alpha(self.__alpha)
        self.__done = False

    @property
    def wave_text(self):
        return self.__wave_text

    @wave_text.setter
    def wave_text(self, value):
        self.__wave_text = value

    @property
    def big_font(self):
        return self.__big_font

    @property
    def medium_font(self):
        return self.__medium_font

    @property
    def font(self):
        return self.__font

    @property
    def done(self):
        return self.__done

    @done.setter
    def done(self, value):
        self.__done = value

    def update(self):
        if self.__done:
            return
        now = pg.time.get_ticks()
        elapsed = now - self.__start_time

        if elapsed >= self.__duration:
            self.__alpha -= self.__fade_speed
            self.__wave_text_rect.centery -= 1
            if self.__alpha <= 0:
                self.__alpha = 0
                self.__done = True

    def draw_text(self, text, font, color, x, y, screen):
        img = font.render(text, True, color)
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        screen.blit(img, img_rect)

    def draw_tower_ui(self, map, tower, tower_group, tower_history, screen):
        panel_rect = pg.Rect(Config.get("WIN_W"), (Config.get("WIN_H")/2), Config.get("SIDE_PANEL"), (Config.get("WIN_H")/2))
        pg.draw.rect(screen, (50, 50, 50), panel_rect)
        pg.draw.rect(screen, (255, 255, 255), panel_rect, 2)

        self.draw_text(f"{tower.name} Lv.{tower.level}", self.__medium_font, Config.get("WHITE"), Config.get("WIN_W")
                       + Config.get("SIDE_PANEL")/2, (Config.get("WIN_H")/2) + 40, screen)

        if tower.weapon.damage > 0:
            screen.blit(self.__attack_icon_img, self.__attack_icon_rect)
            self.draw_text(f"{tower.weapon.damage}", self.__font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL") / 4 + 30, (Config.get("WIN_H") / 2) + 120, screen)
        elif isinstance(tower, SlowTower):
            screen.blit(self.__slow_icon_img, self.__slow_icon_rect)
            self.draw_text(f"{tower.slow_factor}", self.__font, Config.get("WHITE"), Config.get("WIN_W") +
                           Config.get("SIDE_PANEL") / 4 + 30, (Config.get("WIN_H") / 2) + 120, screen)

        screen.blit(self.__range_icon_img, self.__range_icon_rect)
        self.draw_text(f"{tower.range}", self.__font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL")/4 + 30, (Config.get("WIN_H") / 2) + 170, screen)

        screen.blit(self.__cooldown_icon_img, self.__cooldown_icon_rect)
        self.draw_text(f"{tower.weapon.cooldown}", self.__font, Config.get("WHITE"), Config.get("WIN_W") +
                       Config.get("SIDE_PANEL") / 4 + 30, (Config.get("WIN_H") / 2) + 220, screen)

        if tower.level < Config.get("MAX_LEVEL"):
            screen.blit(self.__font.render(f"{tower.upgrade_cost}$", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 115, Config.get("WIN_H") - 70))
            if self.__upgrade_btn.draw(screen):
                if map.money >= tower.upgrade_cost:
                    map.money -= tower.upgrade_cost
                    self.__gm.money_used_this_wave += tower.upgrade_cost
                    tower.upgrade_level()
                    tower.weapon.upgrade_level()
        else:
            max_upgrade_btn = pg.Rect(Config.get("WIN_W") + 80, (Config.get("WIN_H") - 75), 60, 30)
            pg.draw.rect(screen, (0, 200, 0), max_upgrade_btn)
            screen.blit(self.__font.render(f"MAX", True, Config.get("WHITE")),
                        (Config.get("WIN_W") + 90, Config.get("WIN_H") - 70))

        screen.blit(self.__font.render(f"{tower.sell_cost}$", True, Config.get("WHITE")),
                    (Config.get("WIN_W") + 280, Config.get("WIN_H") - 70))
        if self.__sell_btn.draw(screen):
            if (tower.tile_x, tower.tile_y) in tower_history:
                tower_history.remove((tower.tile_x, tower.tile_y))
                map.money += tower.sell_cost
                tower_group.remove(tower)

                if tower.type == "Magic" and self.__gm.tower_count["Magic"] > 0:
                    self.__gm.tower_count["Magic"] -= 1
                elif tower.type == "Archer" and self.__gm.tower_count["Archer"] > 0:
                    self.__gm.tower_count["Archer"] -= 1
                elif tower.type == "Slow" and self.__gm.tower_count["Slow"] > 0:
                    self.__gm.tower_count["Slow"] -= 1

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

        self.__game_coin_rect.topright = (Config.get("WIN_W") - 14, 10)
        screen.blit(self.__game_coin_img, self.__game_coin_rect)

        self.__base_hp_rect.topright = (Config.get("WIN_W") - 16, 55)
        screen.blit(self.__base_hp_img, self.__base_hp_rect)

        self.draw_text(f"{map.money}", self.__font, Config.get("WHITE"), Config.get("WIN_W") - 90,28, screen)
        if map.hp >= 0:
            self.draw_text(f"{map.hp}", self.__font, Config.get("WHITE"), Config.get("WIN_W") - 90, 70, screen)

    def draw_wave_delay_window(self, time_left, screen):
        popup_rect = pg.Rect(Config.get("WIN_W") // 2 - 150, 0, 300, 150)
        pg.draw.rect(screen, (30, 30, 30), popup_rect)
        pg.draw.rect(screen, (255, 255, 255), popup_rect, 2)
        self.draw_text(f"Next wave in: {time_left}s", self.medium_font, Config.get("WHITE"),
                            Config.get("WIN_W") // 2, 40, screen)

    def draw_wave_text(self, screen):
        if not self.__done:
            temp = self.__wave_text.copy()
            temp.set_alpha(self.__alpha)
            screen.blit(temp, self.__wave_text_rect)

    def start_wave_text(self, wave_num):
        if wave_num > len(Enemy_data.enemy_wave):
            self.__wave_text = None
            self.__done = True
            return

        self.__wave_text = self.__big_font.render(f"WAVE {wave_num}", True, Config.get("BLACK"))
        self.__wave_text_rect = self.__wave_text.get_rect()
        self.__wave_text_rect.center = (Config.get("WIN_W") / 2, Config.get("WIN_H") / 2)
        self.__start_time = pg.time.get_ticks()
        self.__duration = 1000
        self.__fade_speed = 5
        self.__alpha = 255
        self.__wave_text.set_alpha(self.__alpha)
        self.done = False

    def is_done(self):
        return self.done
