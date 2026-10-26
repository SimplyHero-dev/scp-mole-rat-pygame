import pygame as pg
import math
from scp.sprites import Sprite, AnimationState

ART_ANGLE = 90
TURN_SPEED = 3
MUZZLE_DISTANCE = 20

class Player(Sprite):
    """The player-controlled character.
    
    Attributes:
        solid_rects: Rects the player cannot walk through, such as walls.
        factory: Used to create bullets and other sprites the player spawns.
        speed: Movement speed in pixels per frame.
        ammo: Rounds left in magazine.
        health: Remaining health points.
        hitbox: Fixed-size rect used for wall collisions. 'rect' changes size
            when the sprite rotates, so it is not used for collisions.
    """
    
    def __init__(self, solid_rects, factory, animations, speed = 3, **kwargs):
        """Initialize the player.

        Args:
            solid_rects: Rects the player collides with. Pass an empty list
                for no walls.
            factory: Object with the methods the player uses to spawn sprites.
            speed: Movement speed in pixels per frame.
            **kwargs: Passed to 'Sprite.__init__' (for example 'groups',
                'image', 'rect' and 'position').
        """
        super().__init__(**kwargs)
        self.solid_rects = solid_rects
        self.factory = factory
        self.animations = animations
        self.speed = speed
        self.ammo = 210
        self.health = 10
        self.aim_angle = 0
        
        self.hitbox = pg.Rect(0, 0, 24, 24)
        self.hitbox.center = self.rect.center
        self.set_animation(
            AnimationState.idle, animations[AnimationState.idle], loop=True
        )
        
    def update(self):
        self._move()
        self._turn()
        self.animate()
        
    def _set_state(self, state):
        if state != self.animation_state:
            self.set_animation(state, self.animations[state], loop=True)
        
    def _move(self):
        keys = pg.key.get_pressed()
        right = keys[pg.K_d] or keys[pg.K_RIGHT]
        left = keys[pg.K_a] or keys[pg.K_LEFT]
        down = keys[pg.K_s] or keys[pg.K_DOWN]
        up = keys[pg.K_w] or keys[pg.K_UP]
        
        dx = right - left
        dy = down - up
        moving = bool(dx or dy)
        self._set_state(
            AnimationState.walking if moving else AnimationState.idle
        )
        if dx and dy:   # keep diagonal speed the same as straight
            dx *= 0.7071
            dy *= 0.7071
        self._move_axis(round(dx * self.speed), 0)
        self._move_axis(0, round(dy * self.speed))

    def _move_axis(self, dx, dy):
        """Move along one axis and push the hitbox out of any wall it hits.

        Args:
            dx: Horizontal movement in pixels.
            dy: Vertical movement in pixels.
        """
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
    
    def _turn(self):
        keys = pg.key.get_pressed()
        turn = keys[pg.K_j] - keys[pg.K_k]
        if turn:
            self.orientation = (self.orientation + turn * TURN_SPEED) % 360
            self.rotate(self.orientation)
        self.aim_angle = self.orientation + ART_ANGLE
    
    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            direction = pg.Vector2(1, 0).rotate(-self.aim_angle)
            gun_offset = pg.Vector2(0, 27).rotate(-self.aim_angle)
            muzzle = pg.Vector2(self.hitbox.center) + gun_offset + direction * MUZZLE_DISTANCE
            self.factory.create_bullet(muzzle, self.aim_angle)
