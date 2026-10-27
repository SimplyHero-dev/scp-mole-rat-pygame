import pygame as pg
from scp.asset_loader import IMAGE_SPRITES
from scp.grid import TILES_X, TILES_Y, create_tile_map, tile_positions
from scp.sprites import Background

BACKGROUND_COLOUR = (35, 35, 35)

LAYOUT = [
    "." * TILES_X
    for _ in range(TILES_Y)
]

LEGEND = {
    ".": "blank"
    # "#": "wall",
}

def build_level():
    tile_map = create_tile_map()
    for gy, gx, x, y, in tile_positions():
        tile = Background.create_from_tile(
            groups = [],
            index = LEGEND[LAYOUT[gy][gx]],
        )
        tile.rect.topleft = (x, y)
        tile_map[gy][gx] = tile
    return tile_map

def render_level(tile_map, size):
    surface = pg.Surface(size, pg.SRCALPHA)
    surface.fill(BACKGROUND_COLOUR)
    for gy, gx, x, y in tile_positions():
        surface.blit(tile_map[gy][gx].image, (x, y))
    return surface
