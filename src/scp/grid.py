import pygame as pg
from dataclasses import dataclass, field
from typing import Tuple, Optional

TILE_HEIGHT = 32
TILE_WIDTH = 32

TILES_Y = 33
TILES_X = 40

def get_grid_rect(gx, gy):
    
    return pg.Rect(gx * TILE_WIDTH, gy * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

def tile_positions():
    
    for y in range(TILES_Y):
        for x in range(TILES_X):
            yield (y, x, x * TILE_WIDTH, y * TILE_HEIGHT)
            
def get_tile_positions(position):
    
    x, y = position
    return x // TILE_WIDTH, y // TILE_HEIGHT

def create_tile_map(default_value = None) -> list:
    
    return [[default_value for _ in range(TILES_X)] for _ in range(TILES_Y)]

@dataclass
class GridTile:
    
    tile: pg.sprite.Sprite
    position: Tuple[int, int]
    east: Optional["GridTile"] = field(repr = False, default = None)
    west: Optional["GridTile"] = field(repr = False, default = None)
    north: Optional["GridTile"] = field(repr = False, default = None)
    south: Optional["GridTile"] = field(repr = False, default = None)
