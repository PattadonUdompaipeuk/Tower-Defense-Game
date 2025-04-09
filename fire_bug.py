import pygame as pg
class Firebug:
    def __init__(self):
        pg.init()
        self.fire_bug = pg.image.load(
            "materials/monster/Foozle_2DC0028_Spire_EnemyPack_2_Ground/Ground/Spritesheets/Firebug.png").convert_alpha()
    def load_frames_from_spritesheet(self, num_width, num_height):
        frames = []
        sheet_width, sheet_height = self.fire_bug.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        #
        for i in range(11):
            frame = pg.transform.scale(self.fire_bug.subsurface(
                (i * frame_width, frame_height * 6, frame_width, frame_height)
            ), (88, 36))
            frames.append(frame)

        return frames
