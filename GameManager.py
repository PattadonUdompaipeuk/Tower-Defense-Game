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

class GameManager:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Config.get("WIN_W") + Config.get("SIDE_PANEL"), Config.get("WIN_H")))
        self.unit_bg = UnitManager(Config.get("WIN_W"), 0)
        #######################################################
        # Load image section
        #######################################################
        self.game_icon = pg.image.load("materials/game_icon.png").convert_alpha()
        self.enemy_image = {
            "Fire_bug": pg.image.load("materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/"
                                      "Firebug.png").convert_alpha(),
            "Leaf_bug": pg.image.load("materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/"
                                      "Leafbug.png").convert_alpha(),
            "Magma_crab": pg.image.load("materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/"
                                      "Magma Crab.png").convert_alpha()
        }
        self.bg = pg.image.load("materials/TD_map/map1.png")
        self.bg_image = pg.transform.scale(self.bg, (Config.get("WIN_W"), Config.get("WIN_H")))
        self.button_image = pg.image.load("materials/tower/button UI.png")
        self.cancel_img = SpriteSheet_data(self.button_image, 5, 4, 16 * 1.5, 16 * 1.5)
        self.cancel_img.load_frames_from_spritesheet(12, 12)
        #######################################################

        with open('materials/TD_map/way_map1.tmj') as file:
            map_data = json.load(file)

        pg.display.set_caption("Tower Defense Game")
        pg.display.set_icon(self.game_icon)
        self.map = Map(map_data, self.bg_image)
        self.map.process_data()
        self.map.process_enemies()
        self.waiting_for_next_wave = False
        self.wave_wait_start = 0
        self.last_wave = pg.time.get_ticks()

        self.big_font = pg.font.Font("Stacked pixel.ttf", 48)
        self.font1 = pg.font.Font("Stacked pixel.ttf", 24)

        # Enemy part
        self.enemy_group = pg.sprite.Group()
        self.last_spawn = pg.time.get_ticks()

        # Tower part
        self.magic_tower = MagicTower(0, 0)
        self.archer_tower = ArcherTower(0, 0)
        self.slow_tower = SlowTower(0, 0)
        self.tower_group = pg.sprite.Group()
        self.tower_history = []
        self.placing_magic = False
        self.placing_archer = False
        self.placing_slow = False
        self.selected_tower = None

        # MagicTower buy button and cancel button
        self.magic_icon = TowerIcon(self.magic_tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL")/4, Config.get("WIN_H")/5),
                                    (Config.get("WIN_W") + Config.get("SIDE_PANEL")/4, Config.get("WIN_H")/5 - 16))
        self.magic_buy_button = Button(self.magic_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 4),
                                 Config.get("WIN_H") / 5)
        self.cancel_button = Button(self.cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL")/4),
                                    (Config.get("WIN_H")/5) + 100)

        # ArcherTower buy button and cancel button
        self.archer_icon = TowerIcon(self.archer_tower, (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2, Config.get("WIN_H") / 5),
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2, Config.get("WIN_H") / 5 - 10))
        self.archer_buy_button = Button(self.archer_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2),
                                 Config.get("WIN_H") / 5)
        self.cancel_button2 = Button(self.cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL")/2),
                                    (Config.get("WIN_H")/5) + 100)

        # SlowTower buy button and cancel button
        self.slow_icon = TowerIcon(self.slow_tower,
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2 + 100, Config.get("WIN_H") / 5 - 32),
                                     (Config.get("WIN_W") + Config.get("SIDE_PANEL") / 2 + 100, Config.get("WIN_H") / 5 - 12))
        self.slow_buy_button = Button(self.slow_tower.image, Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2) + 100,
                                        Config.get("WIN_H") / 5 - 32)
        self.cancel_button3 = Button(self.cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") / 2 + 100),
                                     (Config.get("WIN_H") / 5) + 100)

        self.ui = UI(self.tower_group, self.tower_history)

        self.running = True
        self.clock = pg.time.Clock()

    # click tower icon in unit manager to place tower
    def create_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // (Config.get("TILE_SIZE"))
        mouse_tile_y = mouse_pos[1] // (Config.get("TILE_SIZE"))

        for able in Config.get("PLACEABLE"):
            if mouse_tile_x in able[0] and mouse_tile_y in able[1]:
                mouse_tile_x = able[0][2]
                mouse_tile_y = able[1][1]

                if (mouse_tile_x, mouse_tile_y) not in self.tower_history:
                    self.tower_history.append((mouse_tile_x, mouse_tile_y))
                    print(self.tower_history)
                    if self.placing_magic:
                        self.magic_tower = MagicTower(mouse_tile_x, mouse_tile_y)
                        self.tower_group.add(self.magic_tower)
                        self.map.money -= self.magic_tower.buy_cost
                    elif self.placing_archer:
                        self.archer_tower = ArcherTower(mouse_tile_x, mouse_tile_y)
                        self.tower_group.add(self.archer_tower)
                        self.map.money -= self.archer_tower.buy_cost
                    elif self.placing_slow:
                        self.slow_tower = SlowTower(mouse_tile_x, mouse_tile_y)
                        self.tower_group.add(self.slow_tower)
                        self.map.money -= self.slow_tower.buy_cost
                    print(self.tower_group)

    # to select tower on map
    def select_tower(self, mouse_pos):
        for tower in self.tower_group:
            if tower.rect.collidepoint(mouse_pos):
                self.selected_tower = tower

    # to deselect tower on map
    def clear_selection(self):
        for tower in self.tower_group:
            tower.selected = False

    def run(self):
        while self.running:
            self.clock.tick(Config.get("FPS"))

            self.screen.fill(Config.get("WHITE"))

            self.map.draw(self.screen)
            self.unit_bg.draw(self.screen)

            # update section
            self.enemy_group.update(self.clock.tick(Config.get("FPS")) / 1000, self.screen, self.map)
            self.tower_group.update(self.clock.tick(Config.get("FPS")) / 1000, self.enemy_group, self.screen)

            # check that tower is selected or not
            if self.selected_tower:
                self.selected_tower.selected = True
                if self.selected_tower in self.tower_group:
                    self.ui.draw_tower_ui(self.map, self.selected_tower, self.screen)

            # draw section
            self.ui.draw_status(self.map, self.screen)
            # self.ui.draw_text(f"Money : {self.map.money}$", self.big_font, Config.get("WHITE"), 800 - 300, 0, self.screen)
            # self.ui.draw_text(f"HP : {self.map.hp}", self.big_font, Config.get("BLACK"), 800 - 300, 50, self.screen)

            if not self.waiting_for_next_wave:
                if self.map.wave < len(Enemy_data.enemy_wave):
                    if self.ui.wave_text and not self.ui.is_done():
                        self.ui.update()
                        self.ui.draw_wave_text(self.screen)
                        if self.ui.is_done():
                            self.ui.wave_text = None
                if pg.time.get_ticks() - self.last_spawn > Config.get("SPAWN_DELAY"):
                    if self.map.spawned_enemies < len(self.map.enemy_list):
                        enemy_type = self.map.enemy_list[self.map.spawned_enemies]
                        self.map.random_way()
                        self.map.process_data()
                        self.enemy = Enemy(enemy_type, self.map.waypoints, self.enemy_image)
                        self.enemy_group.add(self.enemy)
                        self.map.spawned_enemies += 1
                        self.last_spawn = pg.time.get_ticks()

                if self.map.spawned_enemies == len(self.map.enemy_list) and len(self.enemy_group) == 0:
                    self.waiting_for_next_wave = True
                    self.wave_wait_start = pg.time.get_ticks()

            elif self.waiting_for_next_wave:
                if pg.time.get_ticks() - self.wave_wait_start >= Config.get("WAVE_DELAY"):
                    self.waiting_for_next_wave = False
                    self.map.next_wave()
                    self.ui.start_wave_text(self.map.wave)

            if self.magic_buy_button.draw(self.screen) and self.map.money >= self.magic_tower.buy_cost:
                self.placing_magic = True
                self.placing_archer = False
                self.placing_slow = False
            if self.archer_buy_button.draw(self.screen) and self.map.money >= self.archer_tower.buy_cost:
                self.placing_archer = True
                self.placing_magic = False
                self.placing_slow = False
            if self.slow_buy_button.draw(self.screen) and self.map.money >= self.slow_tower.buy_cost:
                self.placing_slow = True
                self.placing_archer = False
                self.placing_magic = False

            if self.placing_magic:
                if self.map.money < self.magic_tower.buy_cost or self.cancel_button.draw(self.screen):
                    self.placing_magic = False
            else:
                self.ui.draw_text(f"{self.magic_tower.buy_cost}$", self.font1, Config.get("BLACK"),
                                  self.magic_buy_button.rect.centerx, self.magic_buy_button.rect.centery + 90,
                                  self.screen)

            if self.placing_archer:
                if self.map.money < self.archer_tower.buy_cost or self.cancel_button2.draw(self.screen):
                    self.placing_archer = False
            else:
                self.ui.draw_text(f"{self.archer_tower.buy_cost}$", self.font1, Config.get("BLACK"),
                                  self.archer_buy_button.rect.centerx, self.archer_buy_button.rect.centery + 90,
                                  self.screen)

            if self.placing_slow:
                if self.map.money < self.slow_tower.buy_cost or self.cancel_button3.draw(self.screen):
                    self.placing_slow = False
            else:
                self.ui.draw_text(f"{self.slow_tower.buy_cost}$", self.font1, Config.get("BLACK"),
                                  self.slow_buy_button.rect.centerx, self.slow_buy_button.rect.centery + 122,
                                  self.screen)

            self.magic_icon.draw(self.screen)
            self.archer_icon.draw(self.screen)
            self.slow_icon.draw(self.screen)

            # check event section
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    self.running = False
                if ev.type == pg.MOUSEBUTTONDOWN and ev.button == pg.BUTTON_LEFT:
                    mouse_pos = pg.mouse.get_pos()
                    if (mouse_pos[0] < Config.get("WIN_W") and mouse_pos[1] < Config.get("WIN_H") or
                            mouse_pos[0] < Config.get("WIN_W") + Config.get("SIDE_PANEL") and
                            mouse_pos[1] < Config.get("WIN_H")/2):
                        self.selected_tower = None
                        self.clear_selection()
                        if self.placing_magic and self.map.money >= self.magic_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        elif self.placing_archer and self.map.money >= self.archer_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        elif self.placing_slow and self.map.money >= self.slow_tower.buy_cost:
                            self.create_tower(mouse_pos)
                        else:
                            self.select_tower(mouse_pos)

            pg.display.flip()

        pg.quit()

if __name__ == '__main__':
    TD_game = GameManager()
    TD_game.run()





                



