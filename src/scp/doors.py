import pygame as pg
import math
from scp.sprites import Layer, Sprite

CLOSED_COLOUR = (86, 91, 102)
OPEN_COLOUR = (86, 91, 102)

class Door(Sprite):

    _layer = Layer.items

    def __init__(self, area, solid_rects, open_image, **kwargs):
        super().__init__(**kwargs)
        self.rect.topleft = area.topleft
        self.solid = pg.Rect(area)
        self.solid_rects = solid_rects
        self.closed_image = self.image
        self.open_image = open_image
        self.is_open = False
        solid_rects.append(self.solid)

    @classmethod
    def create(cls, area, groups, solid_rects):
        closed = pg.Surface(area.size)
        closed.fill(CLOSED_COLOUR)
        opened = pg.Surface(area.size, pg.SRCALPHA)
        pg.draw.rect(opened, OPEN_COLOUR, opened.get_rect(), 3)
        return cls.create_from_surface(
            groups=groups,
            surface=closed,
            position=area.center,
            area=area,
            solid_rects=solid_rects,
            open_image=opened,
        )

    def distance_to(self, point):
        dx = max(self.solid.left - point[0], 0, point[0] - self.solid.right)
        dy = max(self.solid.top - point[1], 0, point[1] - self.solid.bottom)
        return math.hypot(dx, dy)

    def toggle(self, blocker=None):
        if self.is_open:
            if blocker is not None and blocker.colliderect(self.solid):
                return False
            self.solid_rects.append(self.solid)
            self.image = self.closed_image
        else:
            self.solid_rects.remove(self.solid)
            self.image = self.open_image
        self.is_open = not self.is_open
        return True
