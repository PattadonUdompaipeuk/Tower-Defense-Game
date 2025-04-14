import pygame as pg
from config import Config
from fire_bug import Firebug
from leaf_bug import Leafbug
from map import Map
import json
from Tower import Tower
from Button import Button
from Tower_icon import TowerIcon
from spritesheet_data import SpriteSheet_data
from magic_tower import MagicTower
from archer_tower import ArcherTower
from magic_weapon import MagicWeapon
from archer_weapon import ArcherWeapon


class GameManager:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Config.get("WIN_W") + Config.get("SIDE_PANEL"), Config.get("WIN_H")))

        self.tower_sprite = pg.image.load(
            "materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers bases/PNGs/Tower 05.png")
        self.tower_sprite2 = pg.image.load(
            "materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers bases/PNGs/Tower 06.png")
        self.bg = pg.image.load("materials/TD_map/map1.png")
        self.bg_image = pg.transform.scale(self.bg, (Config.get("WIN_W"), Config.get("WIN_H")))

        with open('materials/TD_map/way_map1.tmj') as file:
            map_data = json.load(file)
        # print(map_data)

        pg.display.set_caption("Tower Defense Game")
        self.map = Map(map_data, self.bg_image)
        self.map.process_data()
        print(f"map way:{self.map.waypoints}")
        # self.waypoints = Config.get("WAYPOINTS")

        self.enemy_group = pg.sprite.Group()
        self.leaf_bug = Leafbug(self.map.waypoints)
        self.enemy_group.add(self.leaf_bug)

        self.tower_group = pg.sprite.Group()
        self.tower_history = []
        self.placing_magic = False
        self.placing_archer = False
        self.selected_tower = None

        self.weapon_group = pg.sprite.Group()

        self.tower_icon = TowerIcon(self.tower_sprite, 3,0,64,128)
        self.tower_icon.load_frames_from_spritesheet(3, 1)
        self.tower1_buy = Button(self.tower_icon.frame[0], Config.get("WIN_W") + (Config.get("SIDE_PANEL")//4), 100, True)
        self.cancel_img = SpriteSheet_data(pg.image.load("materials/tower/button UI.png"), 5, 4, 16 * 1.5, 16 * 1.5)
        self.cancel_img.load_frames_from_spritesheet(12, 12)
        self.cancel_button = Button(self.cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") // 4),
                                    200, True)

        self.tower_icon2 = TowerIcon(self.tower_sprite2, 3, 0, 64, 128)
        self.tower_icon2.load_frames_from_spritesheet(3, 1)
        self.tower2_buy = Button(self.tower_icon2.frame[0], Config.get("WIN_W") + (Config.get("SIDE_PANEL") // 2), 100,
                                 True)
        self.cancel_img2 = SpriteSheet_data(pg.image.load("materials/tower/button UI.png"), 5, 4, 16 * 1.5, 16 * 1.5)
        self.cancel_img2.load_frames_from_spritesheet(12, 12)
        self.cancel_button2 = Button(self.cancel_img.frame[4], Config.get("WIN_W") + (Config.get("SIDE_PANEL") // 2),
                                    200, True)

        self.running = True
        self.clock = pg.time.Clock()

        # print(f"waypoints:{self.waypoints}")

    def create_tower(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // (Config.get("TILE_SIZE"))
        mouse_tile_y = mouse_pos[1] // (Config.get("TILE_SIZE"))
        print(f"x:{mouse_tile_x}, y:{mouse_tile_y}")

        for able in Config.get("PLACEABLE"):
            if mouse_tile_x in able[0] and mouse_tile_y in able[1]:
                mouse_tile_x = able[0][2]
                mouse_tile_y = able[1][1]
                print(mouse_tile_x, mouse_tile_y)

                if (mouse_tile_x, mouse_tile_y) not in self.tower_history:
                    self.tower_history.append((mouse_tile_x, mouse_tile_y))
                    if self.placing_magic:
                        self.magic_tower = MagicTower(mouse_tile_x, mouse_tile_y)
                        self.magic_weapon = MagicWeapon(mouse_tile_x, mouse_tile_y)
                        self.tower_group.add(self.magic_tower)
                        self.weapon_group.add(self.magic_weapon)
                    elif self.placing_archer:
                        self.archer_tower = ArcherTower(mouse_tile_x, mouse_tile_y)
                        self.archer_weapon = ArcherWeapon(mouse_tile_x, mouse_tile_y)
                        self.tower_group.add(self.archer_tower)
                        self.weapon_group.add(self.archer_weapon)
                    print(self.tower_group)

    def select_tower(self, mouse_pos):
        for tower in self.tower_group:
            if tower.rect.collidepoint(mouse_pos):
                return tower

    def clear_selection(self):
        for tower in self.tower_group:
            tower.selected = False

    def run(self):
        while self.running:
            self.clock.tick(Config.get("FPS"))

            self.screen.fill(Config.get("WHITE"))

            self.map.draw(self.screen)

            self.weapon_group.update(self.clock.tick(Config.get("FPS")) / 1000)
            self.enemy_group.update(self.clock.tick(Config.get("FPS")) / 1000)

            if self.selected_tower:
                self.selected_tower.selected = True

            # self.tower_group.draw(self.screen)
            for tower in self.tower_group:
                tower.draw(self.screen)
            self.weapon_group.draw(self.screen)
            # for weapon in self.weapon_group:
            #     weapon.draw(self.screen)
            self.enemy_group.draw(self.screen)

            if self.tower1_buy.draw(self.screen):
                self.placing_magic = True
                self.placing_archer = False
            if self.tower2_buy.draw(self.screen):
                self.placing_archer = True
                self.placing_magic = False
            if self.placing_magic:
                cursor = self.tower_icon.frame[0].get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor.center = cursor_pos
                if cursor[0] <= Config.get("WIN_W"):
                    self.screen.blit(self.tower_icon.frame[0], cursor)
                if self.cancel_button.draw(self.screen):
                    self.placing_magic = False
            if self.placing_archer:
                cursor = self.tower_icon2.frame[0].get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor.center = cursor_pos
                if cursor[0] <= Config.get("WIN_W"):
                    self.screen.blit(self.tower_icon2.frame[0], cursor)
                if self.cancel_button2.draw(self.screen):
                    self.placing_archer = False

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    self.running = False
                if ev.type == pg.MOUSEBUTTONDOWN and ev.button == pg.BUTTON_LEFT:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0] < Config.get("WIN_W") and mouse_pos[1] < Config.get("WIN_H"):
                        self.selected_tower = None
                        self.clear_selection()
                        if self.placing_magic or self.placing_archer:
                            self.create_tower(mouse_pos)
                        else:
                            self.selected_tower = self.select_tower(mouse_pos)

            pg.display.flip()

        pg.quit()

if __name__ == '__main__':
    TD_game = GameManager()
    TD_game.run()





                



