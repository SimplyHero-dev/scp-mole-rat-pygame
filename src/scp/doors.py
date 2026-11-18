import pygame as pg
import math
from scp.sprites import Layer, Sprite

CLOSED_COLOUR = (86, 91, 102)
OPEN_COLOUR = (86, 91, 102)

class Door(Sprite):

    _layer = Layer.items

    def __init__(self, area, solid_rects, open_image, **kwargs):
        super().__init__(**kwargs)
        self.rect.topleft = area.topleft
        self.solid = pg.Rect(area)
        self.solid_rects = solid_rects
        self.closed_image = self.image
        self.open_image = open_image
        self.is_open = False
        solid_rects.append(self.solid)

    @classmethod
    def create(cls, area, groups, solid_rects):
        closed = pg.Surface(area.size)
        closed.fill(CLOSED_COLOUR)
        opened = pg.Surface(area.size, pg.SRCALPHA)
        pg.draw.rect(opened, OPEN_COLOUR, opened.get_rect(), 3)
        return cls.create_from_surface(
            groups=groups,
            surface=closed,
            position=area.center,
            area=area,
            solid_rects=solid_rects,
            open_image=opened,
        )

    def distance_to(self, point):
        dx = max(self.solid.left - point[0], 0, point[0] - self.solid.right)
        dy = max(self.solid.top - point[1], 0, point[1] - self.solid.bottom)
        return math.hypot(dx, dy)

    def toggle(self, blocker=None):
        if self.is_open:
            if blocker is not None and blocker.colliderect(self.solid):
                return False
            self.solid_rects.append(self.solid)
            self.image = self.closed_image
        else:
            self.solid_rects.remove(self.solid)
            self.image = self.open_image
        self.is_open = not self.is_open
        return True
    
    def interact(self, player):
        self.toggle(player.hitbox)
        return None
    
    
LOCKED_COLOUR = (90, 30, 30)

class LockedDoor(Door):
    def __init__(self, required_cards, unlocked_image, locked_message="It's locked.", **kwargs):
        
        super().__init__(**kwargs)
        self.required_cards = frozenset(required_cards)
        self.unlocked_image = unlocked_image
        self.locked_message = locked_message
        self.locked = True
        
    @classmethod
    def create(cls, area, groups, solid_rects, required_cards, locked_message="It's locked."):
        locked = pg.Surface(area.size)
        locked.fill(LOCKED_COLOUR)
        unlocked = pg.Surface(area.size)
        unlocked.fill(CLOSED_COLOUR)
        opened = pg.Surface(area.size, pg.SRCALPHA)
        pg.draw.rect(opened, OPEN_COLOUR, opened.get_rect(), 3)
        return cls.create_from_surface(
            groups=groups,
            surface=locked,
            position=area.center,
            area=area,
            solid_rects=solid_rects,
            open_image=opened,
            required_cards=required_cards,
            unlocked_image=unlocked,
            locked_message=locked_message,
        )
        
    def unlock(self):
        self.locked= False
        self.closed_image = self.unlocked_image
        if not self.is_open:
            self.image = self.closed_image
            
    def interact(self, player):
        if not self.locked:
            return super().interact(player)
        
        missing = player.missing_cards(self.required_cards)
        if missing:
            have = len(self.required_cards) - len(missing)
            return (
                f"{self.locked_message} "
                f"({have}/{len(self.required_cards)} keycards)"
            )
        self.unlock()
        self.toggle(player.hitbox)
        return "Access granted."
