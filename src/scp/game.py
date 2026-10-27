import pygame as pg
from dataclasses import dataclass, field
from scp.game_loop import GameLoop, GameMenu, GamePlaying
from scp.display import Display
from scp.state import GameState, StateError
from scp.grid import TILE_WIDTH, TILE_HEIGHT, TILES_X, TILES_Y
from scp.factory import SpriteFactory
from scp.player import Player
from scp.sprites import AnimationState
from scp.camera import Camera
from scp.level import WORLD_RECT, create_walls, render_level

SCREENRECT = pg.Rect(0, 0, TILE_WIDTH * TILES_X, TILE_HEIGHT * TILES_Y)

@dataclass
class ScpGame:
    """The game: shared state display, and the loop for each screen.
    
    Create instances with 'ScpGame.create', which also runs 'init'. Then
    call 'start_game' to enter the main menu.
    
    Attributes:
        screen: The surface the game draws onto. None until 'init' runs.
        screen_rect: Size and position of the game area in pixels.
        fullscreen: Whether the display starts in fullscreen mode.
        state: The current 'GameState'. Loops watch this to know when to stop.
        game_menu: Loop for the main menu. Set by 'init'.
        game_playing: Loop for the gameplay. Set by 'init'.
        display: Display wrapper that presents the game surface and toggles 
        fullscreen. Created by 'init'.
    """
    screen: pg.Rect
    screen_rect: pg.Rect
    fullscreen: bool
    state: GameState
    game_menu: GameLoop = field(init=False, default = None)
    game_playing: GameLoop = field(init=False, default = None)

    @classmethod
    def create(cls, fullscreen = False):
        """Create a game and initialize pygame, the display, and assets.

        Args:
            fullscreen: Whether to start in fullscreen mode. The default
            starts in windowed.

        Returns:
            A fully initialized 'ScpGame', in the 'GameState.initialized'
            state and ready for 'start_game'.
        """
        game = cls(
            screen = None,
            screen_rect = SCREENRECT,
            fullscreen = fullscreen,
            state = GameState.initializing,
        )
        game.init()
        return game
    
    def set_state(self, new_state):
        """Change the game state.

        Args:
            new_state: A 'GameState' value.
        """
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        if self.state not in expected_states:
            raise StateError(
                f"Expected the state to be one of {expected_states} not {self.state}"
            )
        
    def init(self):
        self.assert_state_is(GameState.initializing)
        pg.init()

        pg.mixer.pre_init(
            frequency = 44100,
            size = 32,
            channels = 2,
            buffer = 512,
        )
        pg.font.init()
        
        self.display = Display(
            self.screen_rect.size,
            fullscreen = self.fullscreen
        )
        
        self.screen = self.display.game_surface
        
        # imported here due to loading needing the display to exist.
        from scp.asset_loader import load_all_images, load_all_sounds, load_all_animations, PLAYER_WALKING
        
        load_all_images()
        load_all_sounds()
        load_all_animations()
        
        self.walls = create_walls()
        self.level_surface = render_level(
            WORLD_RECT.size,
            self.walls,
        )

        self.set_state(GameState.initialized)
        self.game_menu = GameMenu(game = self)
        
        layers = pg.sprite.LayeredUpdates()
        bullets = pg.sprite.Group()
        solid_rects = self.walls
        factory = SpriteFactory(
            layers=layers,
            bullets=bullets,
            solid_rects=solid_rects,
            bounds=WORLD_RECT,
        )
        camera = Camera(self.screen_rect.size, WORLD_RECT.size)

        player = Player.create_from_surface(
            surface = PLAYER_WALKING[0],
            groups = [layers],
            position = (500, 500),
            solid_rects = solid_rects,
            factory = factory,
            animations={
                AnimationState.idle: [PLAYER_WALKING[0]],
                AnimationState.walking: PLAYER_WALKING,
            },
            animation_speed = 8,
        )
        
        self.game_playing = GamePlaying(
            game = self,
            layers = layers,
            player = player,
            camera = camera,
        )
        
    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)
        self.loop()
        
    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                self.game_menu.loop()
            elif self.state == GameState.game_playing:
                self.game_playing.loop()
        self.quit()
            
    def quit(self):
        pg.quit()
