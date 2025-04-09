import pygame as pg
from config import Config
from Enemy import Enemy
from fire_bug import Firebug
from map import Map
import json
from Tower import Tower
from Button import Button
from Tower_icon import TowerIcon


class GameManager:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Config.get("WIN_W") + Config.get("SIDE_PANEL"), Config.get("WIN_H")))
        # enemy_sprite = pg.image.load("materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/Firebug.png").convert_alpha()
        # self.enemy_image = Enemy_data.load_frames_from_spritesheet(enemy_sprite, 11, 9)
        self.fire_bug = Firebug()
        self.enemy_image = self.fire_bug.load_frames_from_spritesheet(11,9)

        tower_sprite = pg.image.load(
            "materials/tower/Foozle_2DS0019_Spire_TowerPack_3/Towers bases/PNGs/Tower 05.png")
        self.tower_image = pg.transform.scale(tower_sprite, (11 * 16, 11 * 16))
        self.icon_image = pg.transform.scale(tower_sprite, (4 * 16, 4 * 16))
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
        self.enemy = Enemy(self.map.waypoints, self.enemy_image)
        self.enemy_group.add(self.enemy)

        self.tower_group = pg.sprite.Group()
        self.tower_history = []
        self.placing_tower = False

        self.tower_icon = TowerIcon(self.icon_image,Config.get("WIN_W") + (Config.get("SIDE_PANEL")/4), 120)

        self.buy_button = Button("BUY", Config.get("WIN_W") + (Config.get("SIDE_PANEL")/4), 180, 50, 25,
                                 Config.get("BLUE"), Config.get("WHITE"), True)
        self.cancel_button = Button("CANCEL",Config.get("WIN_W") + (Config.get("SIDE_PANEL")/4),210, 50,
                                    25, Config.get("RED"), Config.get("WHITE"), True)

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

                if (mouse_tile_x, mouse_tile_y) not in self.tower_history:
                    self.tower_history.append((mouse_tile_x, mouse_tile_y))
                    self.tower = Tower(self.tower_image, mouse_tile_x, mouse_tile_y)
                    self.tower_group.add(self.tower)
                    print(self.tower_group)

    def run(self):
        while self.running:
            self.clock.tick(Config.get("FPS"))

            self.screen.fill(Config.get("WHITE"))

            self.map.draw(self.screen)

            # pg.draw.lines(self.screen, Config.get("BLACK"), False, self.map.waypoints)

            self.enemy_group.update(self.clock.tick(60)/1000)
            self.enemy_group.draw(self.screen)

            self.tower_group.draw(self.screen)
            self.tower_icon.draw(self.screen)

            if self.buy_button.draw(self.screen):
                self.placing_tower = True
                print("BUY")
            if self.placing_tower:
                cursor_rect = self.icon_image.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                self.screen.blit(self.icon_image, cursor_rect)
                if self.cancel_button.draw(self.screen):
                    self.placing_tower = False
                    print("CANCEL")

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    self.running = False
                if ev.type == pg.MOUSEBUTTONDOWN and ev.button == pg.BUTTON_LEFT:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0] < Config.get("WIN_W") and mouse_pos[1] < Config.get("WIN_H"):
                        self.create_tower(mouse_pos)

            pg.display.flip()

        pg.quit()

if __name__ == '__main__':
    TD_game = GameManager()
    TD_game.run()





                



