import pygame as pg
import enum
from scp.asset_loader import IMAGE_SPRITES
from itertools import cycle

class AnimationState(enum.Enum):
    stopped = "stopped"
    walking = "walking"
    dying = "dying"
    exploding = "exploding"
    idle = "idle"
    
    @classmethod
    def state_kill_sprite(cls, state):
        return state in (cls.exploding, cls.dying)

class Sprite(pg.sprite.Sprite):
    """A sprite with rotation, tile swapping, and collision mask support
    
    Attribrutes:
        image: the surface currently drawn (already rotated).
        surface: The unrotated source surface.
        image_tiles: lookup of pre-loaded tile surfaces, keyed by (flipped_x, flipped_y, index). May be None.
        index: Tile index of the current image, or None if the sprite was created from a plain surface.
        rect: Position and size of the sprite (updated after rotation).
        mask: Collision mask generated from 'image'.
        orientation: Desired rotation in degrees (counter-clockwise)
        flipped_x = Whether the horizontal-flip tile variant is used.
        flipped_y = Whether the vertical-flip tile variant is used.
    """
    
    @classmethod
    def create_from_tile(
        cls,
        index,
        groups,
        image_tiles=IMAGE_SPRITES,
        flipped_x=False,
        flipped_y=False,
        **kwargs,
    ):
        """Create a sprite from a pre-loaded tile.

        Args:
            index: Tile index to look up in 'image_tiles'.
            groups: Sprite group(s) the new sprite is added to.
            image_tiles: Tile lookup, keyed by (flipped_x, flipped_y, index).
            flipped_x: Use the horizontal-flip tile variant.
            flipped_y: Use the vertical-flip tile variant.
            **kwargs: Passed to '__init__' (e.g. 'orientation', 'position').

        Returns:
            A new instance of 'cls'.
        """
        image = image_tiles[(flipped_x, flipped_y, index)]
        rect = image.get_rect()
        return cls(
            image = image,
            image_tiles = image_tiles,
            index = index,
            groups = groups,
            rect = rect,
            **kwargs,
        )
    
    @classmethod
    def create_from_surface(
        cls,
        groups,
        surface,
        **kwargs,
    ):
        """Create a sprite from an arbitrary pygame Surface.
        
        Args:
            groups: Sprite group(s) the new sprite is added to.
            sufrace: The surface to use as the sprite image.
            **kwargs: Passed to '__init__' (e.g. 'orientation', 'position').
            
        Returns:
            A new instance of 'cls' with 'index' set to None.
        """
        rect = surface.get_rect()
        return cls(
            groups = groups,
            image = surface,
            index = None,
            rect = rect,
            **kwargs,
        )
        
    def __init__(
        self,
        groups,
        image_tiles = None,
        index = None,
        rect = None,
        image = None,
        orientation = 0,
        position = (0, 0),
        flipped_x = False,
        flipped_y = False,
        animation_state = AnimationState.stopped,
        frames = None,
        animation_speed = 6,
        _animation_tick = 0,
        frame_source = None,
        frame_source_flipped = None,
    ):
        """Initialize the sprite. See the class docstrings for attributes.

        Args:
            groups: Sprite group(s) to add this sprite to.
            image_tiles: Tile lookup used by 'set_sprite_index'.
            index: tile index of 'image', if it came from a tile.
            rect: Initial rect. Normally 'image.get_rect()'.
            image: Initial surface. If None, no mask/rotation is set up.
            orientation: Initial rotation in degrees (counter-clockwise)
            position: Initial center position, or None to leave the rect-as-is.
            flipped_x: Horizontal flip flag for tile lookups.
            flipped_y: Vertical flip flag for tile lookups.
            animation_state: states of the animation.
            frames: animation frames.
            animation_speed: Framerate of the animation.
        """
        super().__init__(groups)
        self.image = image
        self.image_tiles = image_tiles
        self.index = index
        self.rect = rect
        self.orientation = orientation
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
        self.animation_state = animation_state
        self.frames = frames
        self.animation_speed = animation_speed
        self._animation_tick = _animation_tick
        self.frame_source = frame_source
        self.frame_source_flipped = frame_source_flipped
        self._last_angle = None
        if self.image is not None:
            self.mask = pg.mask.from_surface(self.image)
            self.surface = self.image.copy()
            self.rotate(self.orientation)
        if self.rect is not None and position is not None:
            self.move(position)

    def move(self, position, center: bool = True):
        """Move the sprite.

        Args:
            position: (x, y) target position.
            center: If True, 'position' is where the sprite's center goes;
            otherwise it is where the top-left corner goes.
        """
        if center:
            self.rect.center = position
        else:
            self.rect.topleft = position
        
    def rotate(self, angle):
        """Rotate the sprite around its center.

        Args:
            angle: Rotation in degrees, counter-clockwise. Wrapped to 0-359.
        """
        if angle == self._last_angle:
            return
        new_image = pg.transform.rotate(self.surface, angle % 360)
        new_rect = new_image.get_rect(center = self.rect.center)
        self.image = new_image
        self.rect = new_rect
        self.mask = pg.mask.from_surface(self.image)
        self._last_angle = angle
        
    def set_sprite_index(self, index):
        """Swap the sprite's image to another file, keeping position and angle.
        
        Uses the current 'flipped_x' / 'flipped_y' flags for the lookup.

        Args:
            index: Tile index to switch to.
        """
        self.image = self.image_sprites[(self.flipped_x, self.flipped_y, index)]
        self.surface = self.image.copy()
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)
        self.index = index
        self.rotate(self.orientation)
        
    def animate(self):
        if self.frames is not None:
            roll = self.frames.get(self.animation_state, None)
            if roll is not None:
                self._animation_tick += 1
                if self._animation_tick < self.animation_speed:
                    return
                self._animation_tick = 0
                
                try:
                    next_index = next(roll)
                    if next_index != self.index:
                        self.index = next_index
                        self.set_frame_by_index(next_index)
                except StopIteration:
                    if AnimationState.state_kill_sprite(self.animation_state):
                        self.kill()
                    self.animation_state = AnimationState.stopped
    
    def set_animation(self, state, source, source_flipped=None, loop=False):
        """Switch animation, showing frame 0 immediately.

        Args:
            state: The 'AnimationState' to switch to.
            source: List of surfaces for this animation.
            source_flipped: Mirrored surfaces, used when 'flipped_x' is set.
            loop: Repeat forever instead of stopping after one run.
        """
        self.frame_source = source
        self.frame_source_flipped = source_flipped
        if loop:
            # frame 0 is shown now, so the cycle starts at 1 and wraps to 0.
            order = list(range(1, len(source))) + [0]
            self.frames = {state: cycle(order)}
        else:
            self.frames = {state: iter(range(1, len(source)))}
        self.animation_state = state
        self._animation_tick = 0
        self.index = 0
        self.set_frame_by_index(0) 

    def set_frame_by_index(self, index):
        if self.flipped_x and self.frame_source_flipped is not None:
            frames = self.frame_source_flipped
        else:
            frames = self.frame_source
        self.surface = frames[index]
        self._last_angle = None
        self.rotate(self.orientation)

class Layer(enum.IntEnum):
    """Draw-order layers; higher values are drawn on top.

    Used via the '_layer' class attribute with pygame's LayeredUpdates.
    """
    
    background = 0
    items = 1
    enemies = 2
    player = 3
    bullets = 4
    effects = 5
    
class Background(Sprite):
    """Non-interactive sprite drawn behind everything else."""
    
    _layer = Layer.background

class Player(Sprite):
    _layer = Layer.player
    
class Bullet(Sprite):
    _layer = Layer.bullets
