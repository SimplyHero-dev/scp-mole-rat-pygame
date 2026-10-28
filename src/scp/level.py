import pygame as pg

WORLD_RECT = pg.Rect(0, 0, 3840, 6720)

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
        pg.Rect(t, 600, 1800, t),
        pg.Rect(600, 632, t, 632),
        pg.Rect(1200, 632, t, 632),
        pg.Rect(1800, 232, t, 1032),
        pg.Rect(t, 1232, 200, t),
        pg.Rect(400, 1232, 200, t),
        pg.Rect(632, 1232, 200, t),
        pg.Rect(1000, 1232, 200, t),
        pg.Rect(1232, 1232, 200, t),
        pg.Rect(1600, 1232, 200, t),
        # Courtyard
        pg.Rect(1000, 2000, 1000, t),
        pg.Rect(1000, 2200, t, 800),
        pg.Rect(2000, 2000, t, 800),
        pg.Rect(1032, 2968, 1000, t),
    ]

def render_level(size, walls):
    surface = pg.Surface(size)
    surface.fill(BACKGROUND_COLOUR)

    for wall in walls:
        pg.draw.rect(surface, WALL_COLOUR, wall)
    return surface
