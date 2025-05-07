import pygame as pg
class Config:
    row, col = 50, 50

    __ALL_CONFIGS = {
        'TILE_SIZE': 16,
        'SIDE_PANEL': 400,
        'WIN_W': row * 16,
        'WIN_H': col * 16,
        'BLACK': (0, 0, 0),
        'GRASS GREEN': (124, 252, 0),
        'RED': (255, 0, 0),
        'BLUE': (0, 0, 255),
        'WHITE': (255, 255, 255),
        'FPS': 60,
        'PLACEABLE': [((10,11,12,13), (8,9,10,11)), ((20,21,22,23), (10,11,12,13)),((33,34,35,36), (19,20,21,22)),
                      ((42,43,44,45), (19,20,21,22)), ((2,3,4,5), (38,39,40,41)),((12,13,14,15), (29,30,31,32)),
                      ((23,24,25,26), (29,30,31,32)), ((33,34,35,36), (32,33,34,35)), ((43,44,45,46),(32,33,34,35))],
        'MAX_LEVEL': 3,
        'BUTTON': pg.image.load("materials/tower/button UI.png"),
        'SPAWN_DELAY': 1500,
        'WAVE_DELAY': 10000,
        'BASE_HP': 100,
        'MONEY': 1200,
        'SET_MAGIC_WEAPON': [16, 24, 32],
        'SET_ARCHER_WEAPON': [10, 15, 25],
        'SET_SLOW_WEAPON': [10, 25, 37]
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]