import pygame as pg
from config import Config
from map import Map
import json
from Tower import Tower
from Enemy import Enemy
from Button import Button
from spritesheet_data import SpriteSheet_data
from enemy_data import Enemy_data
from magic_tower import MagicTower
from archer_tower import ArcherTower
from slow_tower import SlowTower
from magic_weapon import MagicWeapon
from archer_weapon import ArcherWeapon
from slow_weapon import SlowWeapon
from unit_manager import UnitManager
from tower_icon import TowerIcon
from ui import UI
from Datalogger import DataLogger
from game_data_graph import GameDataGraphs, Application, run_frame

class GameManager:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Config.get("WIN_W") + Config.get("SIDE_PANEL"), Config.get("WIN_H")))
        self.__unit_bg = UnitManager(Config.get("WIN_W"), 0)
        #######################################################
        # Load image section
        #######################################################
        self.__game_icon = pg.image.load("materials/game_icon.png").convert_alpha()
        self.__game_start_img = pg.image.load("materials/TD_map/start-end bg.png").convert_alpha()
        self.__enemy_image = {
            "Fire_bug": pg.image.load("materials/monster/Spritesheets/"
                                      "Firebug.png").convert_alpha(),
            "Leaf_bug": pg.image.load("materials/monster/Spritesheets/"
                                      "Leafbug.png").convert_alpha(),
            "Magma_crab": pg.image.load("materials/monster/Spritesheets/"
                                        "Magma Crab.png").convert_alpha()
        }
        self.__bg = pg.image.load("materials/TD_map/map1.png")
        self.__bg_image = pg.transform.scale(self.__bg, (Config.get("WIN_W"), Config.get("WIN_H")))
        self.__button_image = pg.image.load("materials/tower/button UI.png")
        self.__cancel_img = SpriteSheet_data(self.__button_image, 5, 4, 16 * 1.5, 16 * 1.5)
        self.__cancel_img.load_frames_from_spritesheet(12, 12)
        #######################################################

        with open('materials/TD_map/way_map1.tmj') as file:
            map_data = json.load(file)

        pg.display.set_caption("Tower Defense Game")
        pg.display.set_icon(self.__game_icon)
        self.__map = Map(map_data, self.__bg_image)
        self.__map.process_data()
        self.__map.process_enemies()
        self.__waiting_for_next_wave = False
        self.__wave_wait_start = 0
        self.__last_wave = pg.time.get_ticks()
        self.__wave_popup_active = False
        self.__wave_popup_start_time = 0
        self.__wave_popup_duration = Config.get("WAVE_DELAY")

        self.__big_font = pg.font.Font("materials/Stacked pixel.ttf", 48)
        self.__font1 = pg.font.Font("materials/Stacked pixel.ttf", 24)

        # Enemy part
        self.__enemy_group = pg.sprite.Group()
        self.__last_spawn = pg.time.get_ticks()

        # Tower part
        self.__magic_tower = MagicTower(0, 0)
        self.__archer_tower = ArcherTower(0, 0)
        self.__slow_tower = SlowTower(0, 0)
        self.__tower_group = pg.sprite.Group()
        self.__tower_history = []
        self.__placing_magic = False
        self.__placing_archer = False
        self.__placing_slow = False
        self.__selected_tower = None

        # MagicTower buy button and cancel button
        self.__magic_icon = TowerIcon(self.__magic_tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 4, Config.get("WIN_H") / 5),
                                      (Config.get("WIN_W") + Config.get("SIDE_PANEL")/4, Config.get("WIN_H")/5 - 16))
        self.__magic_buy_button = Button(self.__magic_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 4),
                                         Config.get("WIN_H") / 5)
        self.__cancel_button = Button(self.__cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 4),
                                      (Config.get("WIN_H")/5) + 100)

        # ArcherTower buy button and cancel button
        self.__archer_icon = TowerIcon(self.__archer_tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2, Config.get("WIN_H") / 5),
                                       (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2, Config.get("WIN_H") / 5 - 10))
        self.__archer_buy_button = Button(self.__archer_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2),
                                          Config.get("WIN_H") / 5)
        self.__cancel_button2 = Button(self.__cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2),
                                       (Config.get("WIN_H")/5) + 100)

        # SlowTower buy button and cancel button
        self.__slow_icon = TowerIcon(self.__slow_tower,
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2 + 100, Config.get("WIN_H") / 5 - 32),
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2 + 100, Config.get("WIN_H") / 5 - 12))
        self.__slow_buy_button = Button(self.__slow_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2) + 100,
                                        Config.get("WIN_H") / 5 - 32)
        self.__cancel_button3 = Button(self.__cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2 + 100),
                                       (Config.get("WIN_H") / 5) + 100)

        start_img = pg.Surface((120, 60))
        start_img.fill(Config.get("BLACK"))
        self.__start_button = Button(start_img, 600, 400)

        data_stat_img = pg.Surface((240, 60))
        data_stat_img.fill(Config.get("BLACK"))
        self.__data_stat_button = Button(data_stat_img, 600, 550)

        skip_img = pg.Surface((80, 30))
        skip_img.fill("blue2")
        self.__skip_btn = Button(skip_img, Config.get("WIN_W") // 2, 100)

        self.__ui = UI(self)

        self.__running = True
        self.__game_start = False
        self.__game_over_lose = False
        self.__game_over_win = False

        self.__clock = pg.time.Clock()

        # To collect Data
        self.data_logger = DataLogger()
        self.tower_count = {"Archer": 0, "Magic": 0, "Slow": 0}
        self.money_used_this_wave = 0
        self.wave_start_time = 0

    def restart_game(self):
        self.data_logger = DataLogger()

        self.__enemy_group.empty()
        self.__tower_group.empty()
        self.__tower_history.clear()
        self.__map.reset()
        self.__map.process_enemies()

        self.__waiting_for_next_wave = False
        self.__selected_tower = None
        self.__placing_magic = False
        self.__placing_archer = False
        self.__placing_slow = False
        self.__game_over_lose = False
        self.__game_over_win = False
        self.__ui.start_wave_text(self.__map.wave)
        self.tower_count = {"Archer": 0, "Magic": 0, "Slow": 0}
        self.money_used_this_wave = 0
        self.wave_start_time = pg.time.get_ticks()

    # click tower icon in unit manager to place tower
    def create_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // (Config.get("TILE_SIZE"))
        mouse_tile_y = mouse_pos[1] // (Config.get("TILE_SIZE"))

        for able in Config.get("PLACEABLE"):
            if mouse_tile_x in able[0] and mouse_tile_y in able[1]:
                mouse_tile_x = able[0][2]
                mouse_tile_y = able[1][1]

                if (mouse_tile_x, mouse_tile_y) not in self.__tower_history:
                    self.__tower_history.append((mouse_tile_x, mouse_tile_y))
                    if self.__placing_magic:
                        self.__magic_tower = MagicTower(mouse_tile_x, mouse_tile_y)
                        self.__tower_group.add(self.__magic_tower)
                        self.__map.money -= self.__magic_tower.buy_cost
                        self.money_used_this_wave += self.__magic_tower.buy_cost
                        self.tower_count["Magic"] += 1
                    elif self.__placing_archer:
                        self.__archer_tower = ArcherTower(mouse_tile_x, mouse_tile_y)
                        self.__tower_group.add(self.__archer_tower)
                        self.__map.money -= self.__archer_tower.buy_cost
                        self.money_used_this_wave += self.__archer_tower.buy_cost
                        self.tower_count["Archer"] += 1
                    elif self.__placing_slow:
                        self.__slow_tower = SlowTower(mouse_tile_x, mouse_tile_y)
                        self.__tower_group.add(self.__slow_tower)
                        self.__map.money -= self.__slow_tower.buy_cost
                        self.money_used_this_wave += self.__slow_tower.buy_cost
                        self.tower_count["Slow"] += 1

    # to select tower on map
    def select_tower(self, mouse_pos):
        for tower in self.__tower_group:
            if tower.rect.collidepoint(mouse_pos):
                self.__selected_tower = tower

    # to deselect tower on map
    def clear_selection(self):
        for tower in self.__tower_group:
            tower.selected = False

    # go to next wave
    def go_next_wave(self):
        self.__waiting_for_next_wave = False
        self.__wave_popup_active = False
        self.wave_start_time = pg.time.get_ticks()
        self.__map.next_wave()
        self.__ui.start_wave_text(self.__map.wave)

    # check which type of tower is choose
    def check_tower_buy(self):
        if self.__magic_buy_button.draw(self.__screen) and self.__map.money >= self.__magic_tower.buy_cost:
            self.__placing_magic = True
            self.__placing_archer = False
            self.__placing_slow = False
        if self.__archer_buy_button.draw(self.__screen) and self.__map.money >= self.__archer_tower.buy_cost:
            self.__placing_archer = True
            self.__placing_magic = False
            self.__placing_slow = False
        if self.__slow_buy_button.draw(self.__screen) and self.__map.money >= self.__slow_tower.buy_cost:
            self.__placing_slow = True
            self.__placing_archer = False
            self.__placing_magic = False

    # draw text when the game end
    def draw_game_end_text(self, text, color):
        self.data_logger.save_to_csv()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.__running = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_r:
                    self.restart_game()
        self.__screen.blit(self.__game_start_img, (0, 0))
        self.__ui.draw_text(text, self.__ui.big_font, color, 600, 200, self.__screen)
        self.__ui.draw_text("PRESS R TO RESTART", self.__font1, Config.get("BLACK"), 600, 300, self.__screen)
        self.__ui.draw_text("STAT GRAPH", self.__big_font, Config.get("WHITE"), 600, 550, self.__screen)
        pg.display.flip()

    def run(self):
        while self.__running:
            if self.__game_start is False:
                for ev in pg.event.get():
                    if ev.type == pg.QUIT:
                        self.__running = False
                if self.__start_button.draw(self.__screen):
                    self.__game_start = True
                if self.__data_stat_button.draw(self.__screen):
                    run_frame()
                self.__screen.blit(self.__game_start_img, (0, 0))
                self.__ui.draw_text("TOWER DEFENSE", self.__ui.big_font, Config.get("BLACK"), 600, 150, self.__screen)
                self.__ui.draw_text("PLAY", self.__big_font, Config.get("WHITE"), 600, 400, self.__screen)
                self.__ui.draw_text("STAT GRAPH", self.__big_font, Config.get("WHITE"), 600, 550, self.__screen)
                pg.display.flip()
                continue

            if self.__map.hp <= 0:
                self.__game_over_lose = True
            if self.__game_over_lose:
                self.draw_game_end_text("GAME OVER", Config.get("RED"))
                if self.__data_stat_button.draw(self.__screen):
                    run_frame()
                self.__ui.draw_text("STAT GRAPH", self.__big_font, Config.get("WHITE"), 600, 550, self.__screen)
                continue
            if self.__game_over_win:
                self.draw_game_end_text("VICTORY!", "green4")
                if self.__data_stat_button.draw(self.__screen):
                    run_frame()
                self.__ui.draw_text("STAT GRAPH", self.__big_font, Config.get("WHITE"), 600, 550, self.__screen)
                continue

            self.__clock.tick(Config.get("FPS"))

            self.__screen.fill(Config.get("WHITE"))

            self.__map.draw(self.__screen)
            self.__unit_bg.draw(self.__screen)

            # update section
            self.__enemy_group.update(self.__clock.tick(Config.get("FPS")) / 1000, self.__screen, self.__map)
            self.__tower_group.update(self.__clock.tick(Config.get("FPS")) / 1000, self.__enemy_group, self.__screen)

            # check that tower is selected or not
            if self.__selected_tower:
                self.__selected_tower.selected = True
                if self.__selected_tower in self.__tower_group:
                    self.__ui.draw_tower_ui(self.__map, self.__selected_tower, self.__tower_group,
                                            self.__tower_history, self.__screen)

            self.__ui.draw_status(self.__map, self.__screen)

            if not self.__waiting_for_next_wave:
                if self.__map.wave <= len(Enemy_data.enemy_wave):
                    if self.__ui.wave_text and not self.__ui.is_done():
                        self.__ui.update()
                        self.__ui.draw_wave_text(self.__screen)
                        if self.__ui.is_done():
                            self.__ui.wave_text = None
                if pg.time.get_ticks() - self.__last_spawn > Config.get("SPAWN_DELAY"):
                    if self.__map.spawned_enemies < len(self.__map.enemy_list):
                        enemy_type = self.__map.enemy_list[self.__map.spawned_enemies]
                        self.__map.random_way()
                        self.__map.process_data()
                        self.enemy = Enemy(enemy_type, self.__map.waypoints, self.__enemy_image)
                        self.__enemy_group.add(self.enemy)
                        self.__map.spawned_enemies += 1
                        self.__last_spawn = pg.time.get_ticks()
                if self.__map.spawned_enemies == len(self.__map.enemy_list) and len(self.__enemy_group) == 0:
                    if self.__map.wave == len(Enemy_data.enemy_wave):
                        time_spent = (pg.time.get_ticks() - self.wave_start_time) / 1000
                        self.data_logger.log_wave(self.__map, self.tower_count, self.money_used_this_wave, time_spent)
                        self.__game_over_win = True
                    else:
                        self.__waiting_for_next_wave = True
                        self.__wave_wait_start = pg.time.get_ticks()
            elif self.__waiting_for_next_wave:
                if not self.__wave_popup_active:
                    self.__wave_popup_active = True
                    self.__wave_popup_start_time = pg.time.get_ticks()
                time_left = max(0, (self.__wave_popup_duration - (pg.time.get_ticks() - self.__wave_popup_start_time)) // 1000)
                self.__ui.draw_wave_delay_window(time_left, self.__screen)

                if self.__skip_btn.draw(self.__screen):
                    time_spent = (pg.time.get_ticks() - self.wave_start_time) / 1000
                    self.data_logger.log_wave(self.__map, self.tower_count, self.money_used_this_wave, time_spent)
                    self.money_used_this_wave = 0
                    self.go_next_wave()
                self.__ui.draw_text("SKIP", self.__font1, Config.get("WHITE"), Config.get("WIN_W") // 2, 100,
                                    self.__screen)
                if pg.time.get_ticks() - self.__wave_wait_start >= Config.get("WAVE_DELAY"):
                    time_spent = (pg.time.get_ticks() - self.wave_start_time) / 1000
                    self.data_logger.log_wave(self.__map, self.tower_count, self.money_used_this_wave, time_spent)
                    self.money_used_this_wave = 0
                    self.go_next_wave()

            # check which type of tower that player choose to buy
            self.check_tower_buy()

            if self.__placing_magic:
                if self.__map.money < self.__magic_tower.buy_cost or self.__cancel_button.draw(self.__screen):
                    self.__placing_magic = False
            else:
                self.__ui.draw_text(f"{self.__magic_tower.buy_cost}$", self.__font1, Config.get("BLACK"),
                                    self.__magic_buy_button.rect.centerx, self.__magic_buy_button.rect.centery + 90,
                                    self.__screen)

            if self.__placing_archer:
                if self.__map.money < self.__archer_tower.buy_cost or self.__cancel_button2.draw(self.__screen):
                    self.__placing_archer = False
            else:
                self.__ui.draw_text(f"{self.__archer_tower.buy_cost}$", self.__font1, Config.get("BLACK"),
                                    self.__archer_buy_button.rect.centerx, self.__archer_buy_button.rect.centery + 90,
                                    self.__screen)

            if self.__placing_slow:
                if self.__map.money < self.__slow_tower.buy_cost or self.__cancel_button3.draw(self.__screen):
                    self.__placing_slow = False
            else:
                self.__ui.draw_text(f"{self.__slow_tower.buy_cost}$", self.__font1, Config.get("BLACK"),
                                    self.__slow_buy_button.rect.centerx, self.__slow_buy_button.rect.centery + 122,
                                    self.__screen)

            self.__magic_icon.draw(self.__screen)
            self.__archer_icon.draw(self.__screen)
            self.__slow_icon.draw(self.__screen)

            # check event section
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    self.__running = False
                if ev.type == pg.MOUSEBUTTONDOWN and ev.button == pg.BUTTON_LEFT:
                    mouse_pos = pg.mouse.get_pos()
                    if (mouse_pos[0] < Config.get("WIN_W") and mouse_pos[1] < Config.get("WIN_H") or
                            mouse_pos[0] < Config.get("WIN_W") + Config.get("SIDE_PANEL") and
                            mouse_pos[1] < Config.get("WIN_H")/2):
                        self.__selected_tower = None
                        self.clear_selection()
                        if self.__placing_magic and self.__map.money >= self.__magic_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        elif self.__placing_archer and self.__map.money >= self.__archer_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        elif self.__placing_slow and self.__map.money >= self.__slow_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        else:
                            self.select_tower(mouse_pos)

            pg.display.flip()

        pg.quit()

if __name__ == '__main__':
    TD_game = GameManager()
    TD_game.run()