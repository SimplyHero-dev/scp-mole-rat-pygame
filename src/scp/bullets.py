import pygame as pg
import math
from scp.sprites import Sprite

class Bullet(Sprite):
    """A bullet fired by the player that fires in a straight line until it hits something."""
    def __init__(self, solid_rects, bounds, speed=100, **kwargs):
        """Initialize the bullet.

        Args:
            solid_rects: Rects that stop the bullet.
            bounds: Rect of the play area.
            speed: Movement speed in pixels per frame.
            **kwargs: Passed to 'Sprite.__init__' (for example 'groups',
                'image', 'position' and 'orientation').
        """
        super().__init__(**kwargs)
        self.solid_rects = solid_rects
        self.bounds = bounds
        rad = math.radians(self.orientation)
        self.velocity = pg.Vector2(math.cos(rad), -math.sin(rad)) * speed
        self.pos = pg.Vector2(self.rect.center)
        
    def update(self):
        """Move forward, and remove the bullet if it hits a wall or goes out of bounds."""
        self.pos += self.velocity
        self.rect.center = self.pos
        hit_wall = self.rect.collidelist(self.solid_rects) != -1
        if hit_wall or not self.bounds.colliderect(self.rect):
            self.kill()
            
            