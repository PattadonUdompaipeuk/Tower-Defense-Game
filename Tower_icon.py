class TowerIcon:
    def __init__(self, image, x,y):
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
