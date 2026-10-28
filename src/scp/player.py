import pygame as pg
import math
from scp.sprites import Sprite, AnimationState

ART_ANGLE = 90
TURN_SPEED = 3
MUZZLE_DISTANCE = 20
FLASH_FRAMES = 12
FLASH_RANGE = 540
FLASH_HALF_ANGLE = 44
FLASH_OFFSET = (64, 25) # pixels (forward, right) from the center to the gun.

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
    
    def __init__(self, solid_rects, factory, animations, speed = 20, **kwargs): # speed = 3 in final
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
        self.flash_on = False
        
        self.hitbox = pg.Rect(0, 0, 48, 48)
        self.hitbox.center = self.rect.center
        self.set_animation(
            AnimationState.idle, animations[AnimationState.idle], loop=True
        )
        
    def update(self):
        self._move()
        self._turn()
        self.flash_on = bool(pg.key.get_pressed()[pg.K_LSHIFT])
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
            gun_offset = pg.Vector2(0, 26).rotate(-self.aim_angle)
            muzzle = pg.Vector2(self.hitbox.center) + gun_offset + direction * MUZZLE_DISTANCE
            self.factory.create_bullet(muzzle, self.aim_angle)
    
    @property
    def flash_origin(self):
        forward = pg.Vector2(1, 0).rotate(-self.aim_angle)
        right = pg.Vector2(-forward.y, forward.x)
        return (
            pg.Vector2(self.hitbox.center)
            + forward * FLASH_OFFSET[0]
            + right * FLASH_OFFSET[1]
        )

    def lights(self, point):
        """Whether a point is inside the flash right now."""
        if not self.flash_on:
            return False
        origin = self.flash_origin
        dx = point[0] - origin.x
        dy = point[1] - origin.y
        if math.hypot(dx, dy) > FLASH_RANGE:
            return False
        angle = math.degrees(math.atan2(-dy, dx))
        diff = (angle - self.aim_angle + 180) % 360 - 180
        return abs(diff) <= FLASH_HALF_ANGLE
