import pygame as pg
from enemy_data import Enemy_data
from pygame.math import Vector2
from config import Config

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoint, img):
        super().__init__()
        self.__enemy_type = enemy_type
        if self.__enemy_type == "Fire_bug":
            self.__data = Enemy_data.fire_bug
        elif self.__enemy_type == "Leaf_bug":
            self.__data = Enemy_data.leaf_bug
        elif self.__enemy_type == "Magma_crab":
            self.__data = Enemy_data.magma_crab
        self.__img = img.get(enemy_type)
        self.__walk1 = []
        self.__walk2 = []
        self.load_frames_from_spritesheet(self.__data.get("num_width"), self.__data.get("num_height"))
        self.__walk_images = self.__walk1
        self.__waypoint = waypoint
        self.__pos = Vector2(self.__waypoint[0])
        self.__target = None
        self.__movement = 0
        self.__target_waypoint = 1
        self.__init_target = Vector2(self.__waypoint[self.__target_waypoint])

        self.__max_health = self.__data.get("health")
        self.__current_health = self.__data.get("health")
        self.__base_speed = self.__data.get("speed")
        self.__speed = self.__data.get("speed")
        self.__slow_until = 0
        self.__money_drop = self.__data.get("money_drop")

        self.__current_frame = 0
        self.__image = self.__walk_images[self.__current_frame]
        self.__move_forward = False
        self.__move_down = False
        self.__rect = self.__image.get_rect()
        self.__rect.center = self.__pos
        self.__animation_speed = 0.01
        self.__animation_timer = 0

    @property
    def current_health(self):
        return self.__current_health

    @current_health.setter
    def current_health(self, health):
        self.__current_health = health

    @property
    def pos(self):
        return self.__pos

    def load_frames_from_spritesheet(self, num_width, num_height):
        sheet_width, sheet_height = self.__img.get_size()
        frame_width = sheet_width // num_width
        frame_height = sheet_height // num_height

        for i in range(self.__data.get("row")):
            frame = pg.transform.scale(self.__img.subsurface(
                (i * frame_width, frame_height * self.__data.get("col")[0], frame_width, frame_height)
            ), self.__data.get("size"))
            self.__walk1.append(frame)

        for i in range(self.__data.get("row")):
            if self.__enemy_type not in ("Fire_bug", "Leaf_bug"):
                frame = pg.transform.flip(pg.transform.scale(self.__img.subsurface(
                    (i * frame_width, frame_height * self.__data.get("col")[1], frame_width, frame_height)
                ), self.__data.get("size")), True, False)
                self.__walk2.append(frame)
            else:
                frame = pg.transform.scale(self.__img.subsurface(
                    (i * frame_width, frame_height * self.__data.get("col")[1], frame_width, frame_height)
                ), self.__data.get("size"))
                self.__walk2.append(frame)

    def update(self, dt, screen, map):
        self.draw_health_bar(screen)
        self.check_alive(map)
        if pg.time.get_ticks() > self.__slow_until:
            self.__speed = self.__base_speed
        self.move(map)
        self.animate(dt)
        self.draw(screen)


    def move(self, map):
        if len(self.__waypoint) > self.__target_waypoint:
            self.__target = Vector2(self.__waypoint[self.__target_waypoint])
            self.__movement = self.__target - self.__pos
        else:
            map.hp -= self.__current_health
            map.missed_enemies += 1
            self.kill()

        distance = self.__movement.length()

        if distance >= self.__speed:
            direction = self.__movement.normalize()
            self.__pos += direction * self.__speed
            if direction.y > direction.x and not self.__move_down:
                self.__walk_images = self.__walk1
                self.__move_down = True
                self.__move_forward = False
            elif direction.x > direction.y and not self.__move_forward:
                self.__walk_images = self.__walk2
                self.__move_forward = True
                self.__move_down = False

        elif distance != 0:
            self.__pos += self.__movement.normalize() * self.__speed
            self.__target_waypoint += 1

        self.__rect.center = self.__pos

    def animate(self, dt):
        self.__animation_timer += dt
        if self.__animation_timer >= self.__animation_speed:
            self.__animation_timer = 0
            self.__current_frame = (self.__current_frame + 1) % len(self.__walk_images)
            self.__image = self.__walk_images[self.__current_frame]

    def draw(self, screen):
        if self.__current_health > 0:
            screen.blit(self.__image, self.__rect)

    def check_alive(self, map):
        if self.__current_health <= 0:
            map.money += self.__money_drop
            map.killed_enemies += 1
            self.kill()

    def apply_slow(self, factor, duration):
        self.__speed = self.__base_speed * factor
        self.__slow_until = pg.time.get_ticks() + duration

    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 10
        health_ratio = self.__current_health / self.__max_health
        fill_width = int(bar_width * health_ratio)
        bar_x = self.__rect.centerx - bar_width / 2
        bar_y = self.__rect.y - 10
        text_x = self.__rect.centerx - 5
        text_y = self.__rect.y - 10
        font = pg.font.Font('materials/Stacked pixel.ttf', 12)
        font_render = font.render(str(self.__current_health), True, Config.get("BLACK"))
        pg.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pg.draw.rect(surface, Config.get("RED"), (bar_x, bar_y, fill_width, bar_height))
        if self.__current_health >= 0:
            surface.blit(font_render, (text_x, text_y))








