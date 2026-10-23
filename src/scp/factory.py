import pygame as pg
from dataclasses import dataclass, field
from scp.bullets import Bullet

@dataclass
class SpriteFactory:
    """Creates bullets and enemies, and adds them to the right groups.
    
    Attributes:
        layers: Group that is updated and drawn every frame.
        bullets: Group holding only bullets, used for collision checks against
            enemies.
        bounds: Rect of the play area.
    """
    layers: pg.sprite.LayeredUpdates
    bullets: pg.sprite.Group
    solid_rects: list
    bounds: pg.Rect
    _bullet_image: pg.Surface = field(init=False, repr=False)
    
    def __post_init__(self):
        # drawn once and shared, instead of creating one new surface per shot
        self._bullet_image = pg.Surface((8, 8), pg.SRCALPHA)
        pg.draw.circle(self._bullet_image, (255, 220, 80), (4, 4), 4)
        
    def create_bullet(self, position, angle):
        """Create a bullet and add it to 'layers' and 'bullets'.

        Args:
            position: (x, y) pixel position where the bullets starts.
            angle: Direction in degrees, counter-clockwise, 0 = right.

        Returns:
            The new 'Bullet'.
        """
        return Bullet.create_from_surface(
            groups=[self.layers, self.bullets],
            surface=self._bullet_image,
            position=position,
            orientation=angle,
            solid_rects=self.solid_rects,
            bounds=self.bounds,
        )
