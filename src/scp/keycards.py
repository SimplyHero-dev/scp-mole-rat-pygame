import pygame as pg
import enum
import math
from scp.sprites import Layer, Sprite

class CardId(enum.Enum):
    guard = "guard"
    records = "records"
    

CARD_NAMES = {
    CardId.guard: "Guard keycard",
    CardId.records: "Records keycard",
}

CARD_COLOURS = {
    CardId.guard: (60, 120, 200),
    CardId.records: (200, 160, 50),
}

class Keycard(Sprite):
    
    _layer = Layer.items
    
    def __init__(self, card_id, **kwargs):
        super().__init__(**kwargs)
        self.card_id = card_id
        
    @classmethod
    def create(cls, card_id, position, groups):
        surface = pg.Surface((20, 14))
        surface.fill(CARD_COLOURS[card_id])
        pg.draw.rect(surface, (20, 20, 20), surface.get_rect(), 1)
        return cls.create_from_surface(
            groups=groups,
            surface=surface,
            position=position,
            card_id=card_id,
        )
        
    def distance_to(self, point):
        dx = max(self.rect.left - point[0], 0 , point[0] - self.rect.right)
        dy = max(self.rect.top - point[1], 0, point[1] - self.rect.bottom)
        return math.hypot(dx, dy)
    
    def interact(self, player):
        player.add_card(self.card_id)
        self.kill()
        return f"Picked up: {CARD_NAMES[self.card_id]}"
    
        