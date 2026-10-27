import pygame as pg

WORLD_RECT = pg.Rect(0, 0, 1920, 1920)

BACKGROUND_COLOUR = (35, 35, 35)
WALL_COLOUR = (75, 75, 75)

def create_walls():
    w, h = WORLD_RECT.size
    t = 32 # wall thickness
    return [
        # Outer walls
        pg.Rect(0, 0, w, t),
        pg.Rect(0, h - t, w, t),
        pg.Rect(0, 0, t, h),
        pg.Rect(w - t, 0, t, h),

        # Example interior walls
        pg.Rect(300, 200, 300, 32),
        pg.Rect(600, 200, 32, 250),
        pg.Rect(900, 500, 400, 32),
    ]

def render_level(size, walls):
    surface = pg.Surface(size)
    surface.fill(BACKGROUND_COLOUR)

    for wall in walls:
        pg.draw.rect(surface, WALL_COLOUR, wall)
    return surface
