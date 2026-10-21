import pygame as pg
from dataclasses import dataclass
from scp.sprites import Background


@dataclass
class Spritemanager:

    layers: pg.sprite.LayeredUpdates
    selected: pg.sprite.LayeredUpdates
    level: list

    @classmethod
    def create(cls, layers, level):
        return cls(layers = layers, level = level, selected = pg.sprite.LayeredUpdates())

    def create_background(self, position, orientation = None, index = None):
        background = Background.create_from_tile(
            #!sounds = None,
            groups = [self.layers],
            index = index,
            orientation = orientation,
            position = position,
        )
        return background

