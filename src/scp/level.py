import pygame as pg

WORLD_RECT = pg.Rect(0, 0, 7056, 4560)

BACKGROUND_COLOUR = (35, 35, 35)
WALL_COLOUR = (75, 75, 75)
WALL_THICKNESS = 32

def horizontal_wall(x, y, length):
    return pg.Rect(x, y, length, WALL_THICKNESS)

def vertical_wall(x, y, length):
    return pg.Rect(x, y, WALL_THICKNESS, length)

def create_walls():
    w, h = WORLD_RECT.size
    t = WALL_THICKNESS
    return [
        # Outer walls
        horizontal_wall(0, 0, w),
        horizontal_wall(0, h - t, w),
        vertical_wall(0, 0, h),
        vertical_wall(w - t, 0, h),

        # Interior walls
        horizontal_wall(t, 600, 1800),
        vertical_wall(600, 632, 632),
        vertical_wall(1200, 632, 632),
        vertical_wall(1800, 232, 1032),
        horizontal_wall(t, 1232, 200),
        horizontal_wall(400, 1232, 200),
        horizontal_wall(632, 1232, 200),
        horizontal_wall(1000, 1232, 200),
        horizontal_wall(1232, 1232, 200),
        horizontal_wall(1600, 1232, 200),

        # Courtyard
        horizontal_wall(1000, 2000, 1000),
        vertical_wall(1000, 2200, 800),
        vertical_wall(2000, 2000, 800),
        horizontal_wall(1032, 2968, 1000),

        # Left rooms
        horizontal_wall(t, 1800, 532),
        horizontal_wall(t, 2400, 532),
        horizontal_wall(t, 3000, 532),
        horizontal_wall(t, 3600, 532),
        vertical_wall(532, 1832, 400),
        vertical_wall(532, 2432, 400),
        vertical_wall(532, 3032, 400),
        vertical_wall(532, 3800, 728),

        # Lower rooms
        horizontal_wall(532, 3850, 1600),
        horizontal_wall(2332, 3850, 100),
        horizontal_wall(2632, 3850, 1600),
        vertical_wall(2367, 3850, 710),
        vertical_wall(4232, 3140, 1420),
        horizontal_wall(4232, 3140, 1600),
    ]

def render_level(size, walls):
    surface = pg.Surface(size)
    surface.fill(BACKGROUND_COLOUR)

    for wall in walls:
        pg.draw.rect(surface, WALL_COLOUR, wall)
    return surface
