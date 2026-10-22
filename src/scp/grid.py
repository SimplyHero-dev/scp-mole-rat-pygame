import pygame as pg
from dataclasses import dataclass, field
from typing import Tuple, Optional

TILE_HEIGHT = 32
TILE_WIDTH = 32

TILES_Y = 33
TILES_X = 40

def get_grid_rect(gx, gy):
    """Get the pixel rectangle covered by a grid cell.

    Args:
        gx: Column of the cell.
        gy: Row of the cell.

    Returns:
        A 'pg.Rect' with the cell's top-left corner and the tile size.
    """
    
    return pg.Rect(gx * TILE_WIDTH, gy * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

def tile_positions():
    """Iterate over every cell in the grid, row by row.

    Yields:
        A tuple '(gy, gx, x, y)': the cell's row and column, followed by
        the pixel position of its top-left corner.
    """
    for y in range(TILES_Y):
        for x in range(TILES_X):
            yield (y, x, x * TILE_WIDTH, y * TILE_HEIGHT)
            
def get_tile_positions(position):       #TODO Check for bounds before indexing
    """Convert a pixel position to the grid cell that contains it.

    Args:
        position: (x, y) pixel position, for example the mouse positions.

    Returns:
        A tuple '(gx, gy)' with the column and row of the cell.
    """
    x, y = position
    return x // TILE_WIDTH, y // TILE_HEIGHT

def create_tile_map(default_value = None) -> list:
    """Create an empty 2D grid with one entry per cell.

    Args:
        default_value: Value placed in every cell. The default leaves each
        cell empty.

    Returns:
        A list of 'TILES_Y' rows, each with 'TILES_X' entries, indexed as
        '[gy][gx]'.
    """
    return [[default_value for _ in range(TILES_X)] for _ in range(TILES_Y)]

@dataclass
class GridTile:
    """A tile in the grid, linked to its four neighbours.
    
    The neighbours links allow walking the grid from one tile to the next
    without going through coordinates.
    
    Attributes:
        tile: The sprite drawn for this tile.
        Positions: Grid positions of the tile as (gx, gy).
        east: Neighbour at gx + 1, or None if there is none.
        west: Neighbour at gx - 1, or None if there is none.
        north: Neighbour at gy - 1, or None if there is none.
        south: Neighbour at gy + 1, or None if there is none.
    """
    tile: pg.sprite.Sprite
    position: Tuple[int, int]
    east: Optional["GridTile"] = field(repr = False, default = None)
    west: Optional["GridTile"] = field(repr = False, default = None)
    north: Optional["GridTile"] = field(repr = False, default = None)
    south: Optional["GridTile"] = field(repr = False, default = None)
