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
        'PLACEABLE': [((8,9,10,11), (10,11,12,13)), ((21,22,23,24), (9,10,11,12)),
                      ((2,3,4,5), (39,40,41,42)),((21,22,23,24), (31,32,33,34)), ((21,22,23,24), (31,32,33,34)),
                      ((38,39,40,41), (18,19,20,21)), ((39,40,41,42), (31,32,33,34))]
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]