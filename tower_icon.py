class TowerIcon:
    def __init__(self, tower, tower_base_rect, tower_weapon_rect):
        self.__tower_base_img = tower.image
        self.__tower_base_rect = self.__tower_base_img.get_rect()
        self.__tower_base_rect.center = tower_base_rect

        self.__tower_weapon_img = tower.weapon.frame[0]

        self.__tower_weapon_rect = self.__tower_weapon_img.get_rect()
        self.__tower_weapon_rect.center = tower_weapon_rect

    def draw(self, screen):
        screen.blit(self.__tower_base_img, self.__tower_base_rect)
        screen.blit(self.__tower_weapon_img, self.__tower_weapon_rect)
