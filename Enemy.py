import pygame as pg
from enemy_data import Enemy_data
from pygame.math import Vector2
from config import Config

class Enemy(pg.sprite.Sprite):
    def __init__(self,enemy_type, waypoint, img):
        super().__init__()
        if enemy_type == "Fire_bug":
            self.data = Enemy_data.fire_bug
        elif enemy_type == "Leaf_bug":
            self.data = Enemy_data.leaf_bug
        self.img = img.get(enemy_type)
        self.walk1 = []
        self.walk2 = []
        self.load_frames_from_spritesheet(self.data.get("num_width"), self.data.get("num_height"))
        self.walk_images = self.walk1
        self.waypoint = waypoint
        self.pos = Vector2(self.waypoint[0])
        self.target_waypoint = 1
        self.init_target = Vector2(self.waypoint[self.target_waypoint])

        self.max_health = self.data.get("health")
        self.current_health = self.data.get("health")
        self.speed = self.data.get("speed")
        self.money_drop = self.data.get("money_drop")

        self.current_frame = 0
        self.image = self.walk_images[self.current_frame]
        self.move_forward = False
        self.move_down = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.animation_speed = 0.01
        self.animation_timer = 0

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.img.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(self.data.get("row")):
            frame = pg.transform.scale(self.img.subsurface(
                (i * frame_width, frame_height * self.data.get("col")[0], frame_width, frame_height)
            ), self.data.get("size"))
            self.walk1.append(frame)

        for i in range(self.data.get("row")):
            frame = pg.transform.scale(self.img.subsurface(
                (i * frame_width, frame_height * self.data.get("col")[1], frame_width, frame_height)
            ), self.data.get("size"))
            self.walk2.append(frame)

    def update(self, dt, screen, map):
        self.check_alive(map)
        self.move(map)
        self.animate(dt)
        self.draw(screen)
        self.draw_health_bar(screen)

    def move(self, map):
        if len(self.waypoint) > self.target_waypoint:
            self.target = Vector2(self.waypoint[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            map.hp -= self.current_health
            self.kill()

        distance = self.movement.length()
        # print(distance)
        if distance >= self.speed:
            direction = self.movement.normalize()
            self.pos += direction * self.speed
            if direction.y > direction.x and not self.move_down:
                self.walk_images = self.walk1
                self.move_down = True
                self.move_forward = False
            elif direction.x > direction.y and not self.move_forward:
                self.walk_images = self.walk2
                self.move_forward = True
                self.move_down = False

        elif distance != 0:
            self.pos += self.movement.normalize() * self.speed
            self.target_waypoint += 1

        self.rect.center = self.pos

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_images)
            new_image = self.walk_images[self.current_frame]
            self.image = new_image

    def draw(self, screen):
        if self.current_health > 0:
            screen.blit(self.image, self.rect)

    def check_alive(self, map):
        if self.current_health <= 0:
            map.money += self.money_drop
            self.kill()

    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 10
        health_ratio = self.current_health / self.max_health
        fill_width = int(bar_width * health_ratio)

        bar_x = self.rect.centerx - bar_width / 2
        bar_y = self.rect.y - 10

        pg.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))

        pg.draw.rect(surface, Config.get("RED"), (bar_x, bar_y, fill_width, bar_height))







