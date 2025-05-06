import pygame as pg
class SpriteSheet_data:
    def __init__(self, spritesheet, row, col, width, height):
        self.sheet = spritesheet
        self.frame = []
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.sheet.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height
        print(frame_width, frame_height)

        for i in range(self.row):
            frame = pg.transform.scale(self.sheet.subsurface(
                (i * frame_width, frame_height * self.col, frame_width, frame_height)
            ), (self.width, self.height))

            self.frame.append(frame)