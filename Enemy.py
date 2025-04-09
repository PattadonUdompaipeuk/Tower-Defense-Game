import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoint, image):
        super().__init__()
        self.walk_images = image
        self.waypoint = waypoint
        self.pos = Vector2(self.waypoint[0])
        self.target_waypoint = 1
        self.init_target = Vector2(self.waypoint[self.target_waypoint])
        self.speed = 3
        self.current_frame = 0
        self.image = self.walk_images[self.current_frame]
        self.flipped_left = False
        self.flipped_right = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.animation_speed = 0.01
        self.animation_timer = 0

    def update(self, dt):
        self.move()
        self.animate(dt)

    def move(self):
        if len(self.waypoint) > self.target_waypoint:
            self.target = Vector2(self.waypoint[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()

        # print(self.movement)

        distance = self.movement.length()
        # print(distance)
        if distance >= self.speed:
            direction = self.movement.normalize()
            self.pos += direction * self.speed
            # print(self.movement.normalize())
            if direction.x < 0 and not self.flipped_left:
                self.flip()
                self.flipped_left = True
                self.flipped_right = False
            elif direction.x > 0 and not self.flipped_right:
                self.flip()
                self.flipped_right = True
                self.flipped_left = False

        elif distance != 0:
            self.pos += self.movement.normalize() * self.speed
            self.target_waypoint += 1

        self.rect.center = self.pos

    def flip(self):
        self.image = pg.transform.flip(self.image, True, False)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_images)
            new_image = self.walk_images[self.current_frame]

            if self.flipped_left:
                self.image = pg.transform.flip(new_image, True, False)
            else:
                self.image = new_image




