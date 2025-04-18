import pygame as pg
from Enemy import Enemy
from pygame.math import Vector2
class Firebug(Enemy):
    def __init__(self, waypoint):
        pg.init()
        self.fire_bug = pg.image.load(
            "materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/Firebug.png").convert_alpha()

        self.walk1 = []
        self.walk2 = []
        self.load_frames_from_spritesheet(11, 9)

        super().__init__(waypoint, self.walk1)

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.fire_bug.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(8):
            frame = pg.transform.scale(self.fire_bug.subsurface(
                (i * frame_width, frame_height * 3, frame_width, frame_height)
            ), (88, 36))
            self.walk1.append(frame)

        for i in range(8):
            frame = pg.transform.scale(self.fire_bug.subsurface(
                (i * frame_width, frame_height * 5, frame_width, frame_height)
            ), (88, 36))
            self.walk2.append(frame)

