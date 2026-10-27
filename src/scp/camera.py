import pygame as pg

class Camera:

    def __init__(self, view_size, world_size):
        self.view = pg.Vector2(view_size)
        self.world = pg.Vector2(world_size)
        self.offset = pg.Vector2(0, 0)

    def follow(self, target):
        offset = pg.Vector2(target) - self.view / 2
        offset.x = max(0, min(offset.x, self.world.x - self.view.x))
        offset.y = max(0, min(offset.y, self.world.y - self.view.y))
        self.offset = offset

    def apply(self, rect):
        return rect.move(-round(self.offset.x), -round(self.offset.y))

    def to_screen(self, point):
        return pg.Vector2(point) - self.offset

    def to_world(self, point):
        return pg.Vector2(point) + self.offset
    