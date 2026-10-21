import pygame as pg
from dataclasses import dataclass, field
from scp.game_loop import GameLoop, GameMenu, GameEditing
from scp.state import GameState, StateError
from scp.grid import TILE_WIDTH, TILE_HEIGHT, TILES_X, TILES_Y
from scp.sprite_manager import Spritemanager

SCREENRECT = pg.Rect(0, 0, TILE_WIDTH * TILES_X, TILE_HEIGHT * TILES_Y)

@dataclass
class ScpGame:
    screen: pg.Rect
    screen_rect: pg.Rect
    fullscreen: bool
    state: GameState
    game_menu: GameLoop = field(init=False, default = None)
    game_editing: GameLoop = field(init=False, default = None)

    @classmethod
    def create(cls, fullscreen = False):
        game = cls(
            screen = None,
            screen_rect = SCREENRECT,
            fullscreen = fullscreen,
            state = GameState.initializing,
        )
        game.init()
        return game
    
    def set_state(self, new_state):
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        if self.state not in expected_states:
            raise StateError(
                f"Expected the state to be one of {expected_states} not {self.state}"
            )
        
    def init(self):
        self.assert_state_is(GameState.initializing)
        pg.init()
        window_style = pg.FULLSCREEN if self.fullscreen else 0
        
        bit_depth = pg.display.mode_ok(self.screen_rect.size, window_style, 32)
        screen = pg.display.set_mode(self.screen_rect.size, window_style, bit_depth)
        pg.mixer.pre_init(
            frequency = 44100,
            size = 32,
            channels = 2,
            buffer = 512,
        )
        pg.font.init()
        self.screen = screen
        
        from scp.asset_loader import load_all_images, load_all_sounds
        load_all_images()
        load_all_sounds()

        self.set_state(GameState.initialized)
        self.game_menu = GameMenu(game = self)

        layers = pg.sprite.LayeredUpdates()
        self.game_editing = GameEditing(
            game = self,
            layers = layers,
            sprite_manager = Spritemanager.create(layers = layers, level = None),
            level = None,
        )
        
    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)
        self.loop()
        
    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                self.game_menu.loop()
            elif self.state == GameState.map_editing:
                self.game_editing.loop()
            elif self.state == GameState.game_playing:
                self.game_menu.loop()
        self.quit()
            
    def quit(self):
        pg.quit()
