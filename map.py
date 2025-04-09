import pygame as pg
import random
class Map:
    def __init__(self, map_data, map_image):
        self.waypoints = []
        self.map_data = map_data
        self.image = map_image

    def process_data(self):
        random_way = random.choice(["way1", "way2"])
        print(random_way)
        for layer in self.map_data["layers"]:
            if layer["name"] == random_way:
                for obj in layer["objects"]:
                    tmp_x = round(obj["x"], 2)
                    tmp_y = round(obj["y"], 2)
                    self.waypoints.append((tmp_x, tmp_y))

    def process_waypoints(self, data):
        for point in data:
            tmp_x = point.get('x')
            tmp_y = point.get('y')
            self.waypoints.append((tmp_x, tmp_y))

    def draw(self, surface):
        surface.blit(self.image, (0,0))

