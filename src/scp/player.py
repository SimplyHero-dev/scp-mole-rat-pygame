import pygame as pg
from scp.sprites import Sprite

class Player(Sprite):
    """The player-controlled character."""
    
    def __init__(self, solid_rects, factory, speed = 3, **kwargs):
        super().__init__(**kwargs)
        self.solid_rects = solid_rects
        self.factory = factory
        self.speed = speed
        self.ammo = 15
        self.health = 10
        
        self.hitbox = pg.Rect(0, 0, 24, 24)
        self.hitbox.center = self.rect.center
        
    def update(self):
        self._move()
        
    def _move(self):
        keys = pg.key.get_pressed()
        right = keys[pg.K_d] or keys[pg.K_RIGHT]
        left = keys[pg.K_a] or keys[pg.K_LEFT]
        down = keys[pg.K_s] or keys[pg.K_DOWN]
        up = keys[pg.K_w] or keys[pg.K_UP]
        
        dx = right - left
        dy = down - up
        if dx and dy:   # keep diagonal speed the same as straight
            dx *= 0.7071
            dy *= 0.7071
        self._move_axis(round(dx * self.speed), 0)
        self._move_axis(0, round(dy * self.speed))

    def _move_axis(self, dx, dy):
        self.hitbox.x += dx
        self.hitbox.y += dy
        for wall in self.solid_rects:
            if self.hitbox.colliderect(wall):
                if dx > 0:
                    self.hitbox.right = wall.left
                elif dx < 0:
                    self.hitbox.left = wall.right
                if dy > 0:
                    self.hitbox.bottom = wall.top
                elif dy < 0:
                    self.hitbox.top = wall.bottom
        self.rect.center = self.hitbox.center
