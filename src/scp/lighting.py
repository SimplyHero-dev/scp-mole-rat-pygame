import pygame as pg
import math
from scp.player import FLASH_HALF_ANGLE, FLASH_RANGE

DARKNESS_ALPHA = 241
GLOW_RADIUS = 200
GLOW_STRENGTH = 200
FLASH_STRENGTH = 255
BLUR_SCALE = 4


def make_radial(radius, strength, power=2.0):
    """Create a round light around the player that fades out from the middle.

    Args:
        radius: Radius in pixels.
        strength: Alpha at the center (0-255); how much darkness it removes.
        power: Fall-off curve. Higher values concentrate light in the middle.

    Returns:
        A 'pg.Surface' whose alpha is the light intensity.
    """
    surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
    for r in range(radius, 0, -2):
        alpha = int(strength * (1 -r / radius) ** power)
        pg.draw.circle(surface, (255, 255, 255, alpha), (radius, radius), r)
    return surface

def make_cone(radius, half_angle, strength):
    """Create a flashlight cone, soft at the edges and far end.

    Args:
        radius: Radius in pixels.
        half_angle: Half the width of the cone, in degrees.
        strength: Alpha at the brightest point (0-255).

    Returns:
        A 'pg.Surface' whose alpha is the light intensity.
    """
    small_r = radius // BLUR_SCALE
    small = pg.Surface((small_r * 2, small_r * 2), pg.SRCALPHA)
    center = pg.Vector2((small_r, small_r))

    steps = 16
    for i in range(steps):
        half = half_angle * (1 - i / steps)
        alpha = int(255 * ((i + 1) / steps) ** 1.5)
        points = [center]
        for j in range(11):
            a = math.radians(-half + 2 * half * j / 10)
            points.append(center + pg.Vector2(math.cos(a), math.sin(a)) * small_r)
        pg.draw.polygon(small, (255, 255, 255, alpha), points)

    cone = pg.transform.smoothscale(small, (radius * 2, radius * 2))
    # fade out toward the far end, and apply the overall strength
    cone.blit(make_radial(radius, 255, power=0.7), (0, 0),
              special_flags=pg.BLEND_RGBA_MULT)
    cone.fill((255, 255, 255, strength), special_flags=pg.BLEND_RGBA_MULT)
    return cone


class Darkness:
    """Covers the screen in darkness, with soft light cut out of it."""
    def __init__(self, size):
        self.surface = pg.Surface(size, pg.SRCALPHA)
        self.glow = make_radial(GLOW_RADIUS, GLOW_STRENGTH)
        self.cone = make_cone(FLASH_RANGE, FLASH_HALF_ANGLE, FLASH_STRENGTH)

    def render(self, screen, player, camera):
        """Draw the darkness over the 'screen'. Call after drawing the world."""
        self.surface.fill((0, 0, 0, DARKNESS_ALPHA))
        self._cut(self.glow, camera.to_screen(player.hitbox.center))

        if player.flash_on:
            cone = pg.transform.rotate(self.cone, player.aim_angle)
            self._cut(cone, camera.to_screen(player.flash_origin))

        screen.blit(self.surface, (0, 0))

    def _cut(self, light, center):
        """Remove darkness where 'light' is bright, centered on 'center'."""
        rect = light.get_rect(center=(round(center.x), round(center.y)))
        self.surface.blit(light, rect, special_flags=pg.BLEND_RGBA_SUB)
